package storage

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// DB wraps the SQL database connection
type DB struct {
	conn   *sql.DB
	logger *slog.Logger
}

// NewSQLiteDB creates a new SQLite database connection and runs migrations
func NewSQLiteDB(path string, logger *slog.Logger) (*DB, error) {
	conn, err := sql.Open("sqlite3", path+"?_journal_mode=WAL&_timeout=5000")
	if err != nil {
		return nil, fmt.Errorf("opening database: %w", err)
	}

	// Set connection pool settings
	conn.SetMaxOpenConns(25)
	conn.SetMaxIdleConns(5)
	conn.SetConnMaxLifetime(5 * time.Minute)

	// Test connection
	if err := conn.Ping(); err != nil {
		return nil, fmt.Errorf("pinging database: %w", err)
	}

	db := &DB{
		conn:   conn,
		logger: logger,
	}

	// Run migrations
	if err := db.migrate(); err != nil {
		return nil, fmt.Errorf("running migrations: %w", err)
	}

	logger.Info("database migrations completed")

	return db, nil
}

// Close closes the database connection
func (db *DB) Close() error {
	return db.conn.Close()
}

// migrate runs database migrations
func (db *DB) migrate() error {
	migrations := []string{
		// Bugs table
		`CREATE TABLE IF NOT EXISTS bugs (
			id TEXT PRIMARY KEY,
			key TEXT NOT NULL UNIQUE,
			title TEXT NOT NULL,
			description TEXT,
			steps TEXT,
			expected TEXT,
			actual TEXT,
			priority TEXT,
			environment TEXT,
			project TEXT,
			status TEXT,
			jira_url TEXT,
			similarity_score INTEGER,
			created_at DATETIME NOT NULL,
			updated_at DATETIME NOT NULL
		)`,
		`CREATE INDEX IF NOT EXISTS idx_bugs_created_at ON bugs(created_at)`,
		`CREATE INDEX IF NOT EXISTS idx_bugs_project ON bugs(project)`,
		`CREATE INDEX IF NOT EXISTS idx_bugs_status ON bugs(status)`,

		// Tasks table for scheduler
		`CREATE TABLE IF NOT EXISTS tasks (
			id TEXT PRIMARY KEY,
			name TEXT NOT NULL,
			description TEXT,
			cron_expression TEXT NOT NULL,
			agent_slug TEXT,
			prompt TEXT,
			status TEXT NOT NULL,
			last_run DATETIME,
			next_run DATETIME,
			run_count INTEGER DEFAULT 0,
			created_at DATETIME NOT NULL,
			updated_at DATETIME NOT NULL
		)`,
		`CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)`,
		`CREATE INDEX IF NOT EXISTS idx_tasks_next_run ON tasks(next_run)`,

		// Task executions history
		`CREATE TABLE IF NOT EXISTS task_executions (
			id TEXT PRIMARY KEY,
			task_id TEXT NOT NULL,
			started_at DATETIME NOT NULL,
			finished_at DATETIME,
			status TEXT NOT NULL,
			output TEXT,
			error TEXT,
			FOREIGN KEY (task_id) REFERENCES tasks(id)
		)`,
		`CREATE INDEX IF NOT EXISTS idx_task_executions_task_id ON task_executions(task_id)`,
		`CREATE INDEX IF NOT EXISTS idx_task_executions_started_at ON task_executions(started_at)`,

		// Settings table
		`CREATE TABLE IF NOT EXISTS settings (
			key TEXT PRIMARY KEY,
			value TEXT NOT NULL,
			updated_at DATETIME NOT NULL
		)`,

		// Duplicate cache (for performance)
		`CREATE TABLE IF NOT EXISTS duplicate_cache (
			title_hash TEXT PRIMARY KEY,
			bug_keys TEXT NOT NULL,
			created_at DATETIME NOT NULL
		)`,
		`CREATE INDEX IF NOT EXISTS idx_duplicate_cache_created_at ON duplicate_cache(created_at)`,
	}

	for _, migration := range migrations {
		if _, err := db.conn.Exec(migration); err != nil {
			return fmt.Errorf("executing migration: %w", err)
		}
	}

	return nil
}

// WithTx executes a function within a transaction
func (db *DB) WithTx(ctx context.Context, fn func(*sql.Tx) error) error {
	tx, err := db.conn.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("beginning transaction: %w", err)
	}

	if err := fn(tx); err != nil {
		if rbErr := tx.Rollback(); rbErr != nil {
			return fmt.Errorf("rolling back transaction: %v (original error: %w)", rbErr, err)
		}
		return err
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("committing transaction: %w", err)
	}

	return nil
}
