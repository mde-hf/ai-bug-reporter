package main

import (
	"context"
	"embed"
	"flag"
	"fmt"
	"log"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"github.com/hellofresh/bug-reporter/internal/api"
	"github.com/hellofresh/bug-reporter/internal/config"
	"github.com/hellofresh/bug-reporter/internal/integrations/bedrock"
	"github.com/hellofresh/bug-reporter/internal/integrations/jira"
	"github.com/hellofresh/bug-reporter/internal/integrations/slack"
	"github.com/hellofresh/bug-reporter/internal/logger"
	"github.com/hellofresh/bug-reporter/internal/scheduler"
	"github.com/hellofresh/bug-reporter/internal/service"
	"github.com/hellofresh/bug-reporter/internal/storage"
	"github.com/joho/godotenv"
)

//go:embed web/dist/*
var webFS embed.FS

var (
	Version   = "dev"
	BuildTime = "unknown"
)

func main() {
	// Parse command-line flags
	var (
		port    = flag.Int("port", 8990, "HTTP server port")
		dataDir = flag.String("data-dir", "", "Data directory (default: ~/.bug-reporter)")
		logLevel = flag.String("log-level", "info", "Log level: debug, info, warn, error")
		showVersion = flag.Bool("version", false, "Show version and exit")
	)
	flag.Parse()

	if *showVersion {
		fmt.Printf("Bug Reporter %s (built %s)\n", Version, BuildTime)
		os.Exit(0)
	}

	// Load environment variables from .env if present
	_ = godotenv.Load()

	// Override with command-line flags
	if *port != 8990 {
		os.Setenv("PORT", fmt.Sprintf("%d", *port))
	}
	if *dataDir != "" {
		os.Setenv("DATA_DIR", *dataDir)
	}
	if *logLevel != "info" {
		os.Setenv("LOG_LEVEL", *logLevel)
	}

	// Initialize logger
	log := logger.New(*logLevel)
	log.Info("starting bug reporter",
		"version", Version,
		"build_time", BuildTime,
	)

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Error("failed to load configuration", "error", err)
		os.Exit(1)
	}

	// Ensure data directory exists
	if err := os.MkdirAll(cfg.DataDir, 0755); err != nil {
		log.Error("failed to create data directory", "dir", cfg.DataDir, "error", err)
		os.Exit(1)
	}

	// Create logs directory
	logsDir := filepath.Join(cfg.DataDir, "logs")
	if err := os.MkdirAll(logsDir, 0755); err != nil {
		log.Error("failed to create logs directory", "dir", logsDir, "error", err)
		os.Exit(1)
	}

	log.Info("configuration loaded",
		"data_dir", cfg.DataDir,
		"port", cfg.Port,
		"jira_base_url", cfg.Jira.BaseURL,
	)

	// Initialize database
	dbPath := filepath.Join(cfg.DataDir, "bug-reporter.db")
	db, err := storage.NewSQLiteDB(dbPath, log)
	if err != nil {
		log.Error("failed to initialize database", "path", dbPath, "error", err)
		os.Exit(1)
	}
	defer db.Close()

	log.Info("database initialized", "path", dbPath)

	// Initialize stores
	bugStore := storage.NewBugStore(db)
	taskStore := storage.NewTaskStore(db)
	settingsStore := storage.NewSettingsStore(db)

	// Initialize integrations
	jiraClient := jira.NewClient(cfg.Jira, log)
	slackClient := slack.NewClient(cfg.Slack, log)
	
	var bedrockClient *bedrock.Client
	if cfg.Bedrock.Enabled {
		bedrockClient, err = bedrock.NewClient(cfg.Bedrock, log)
		if err != nil {
			log.Warn("failed to initialize bedrock client", "error", err)
		} else {
			log.Info("bedrock client initialized", "model", cfg.Bedrock.ModelID)
		}
	}

	// Initialize services
	bugService := service.NewBugService(bugStore, jiraClient, slackClient, log)
	testCaseService := service.NewTestCaseService(bedrockClient, jiraClient, log)
	taskService := service.NewTaskService(taskStore, log)

	// Initialize scheduler
	schedulerCfg := scheduler.Config{
		TaskStore:       taskStore,
		BugService:      bugService,
		TestCaseService: testCaseService,
		Logger:          log,
		MaxConcurrency:  3,
	}
	
	sched, err := scheduler.New(schedulerCfg)
	if err != nil {
		log.Error("failed to create scheduler", "error", err)
		os.Exit(1)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	if err := sched.Start(ctx); err != nil {
		log.Error("failed to start scheduler", "error", err)
		os.Exit(1)
	}
	defer sched.Stop()

	// Initialize API server
	apiCfg := api.Config{
		BugService:      bugService,
		TestCaseService: testCaseService,
		TaskService:     taskService,
		SettingsStore:   settingsStore,
		JiraClient:      jiraClient,
		Logger:          log,
		WebFS:           webFS,
	}

	srv := api.NewServer(apiCfg)

	// Create HTTP server
	httpServer := &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.Port),
		Handler:      srv,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 300 * time.Second, // Long timeout for streaming responses
		IdleTimeout:  60 * time.Second,
	}

	// Start HTTP server in goroutine
	go func() {
		log.Info("starting HTTP server", "addr", httpServer.Addr)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Error("HTTP server error", "error", err)
			os.Exit(1)
		}
	}()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info("shutting down server...")

	// Graceful shutdown with timeout
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer shutdownCancel()

	if err := httpServer.Shutdown(shutdownCtx); err != nil {
		log.Error("server forced to shutdown", "error", err)
	}

	log.Info("server stopped")
}
