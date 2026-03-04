package config

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// Config holds all application configuration
type Config struct {
	Port    int
	DataDir string
	LogLevel string
	
	Jira    JiraConfig
	Slack   SlackConfig
	Bedrock BedrockConfig
}

// JiraConfig holds Jira API configuration
type JiraConfig struct {
	BaseURL  string
	CloudID  string
	Email    string
	APIToken string
	EpicKey  string
	ProjectKey string
}

// SlackConfig holds Slack webhook configuration
type SlackConfig struct {
	WebhookURL string
	Enabled    bool
}

// BedrockConfig holds AWS Bedrock configuration
type BedrockConfig struct {
	Region    string
	AccessKey string
	SecretKey string
	ModelID   string
	Enabled   bool
}

// Load reads configuration from environment variables
func Load() (*Config, error) {
	cfg := &Config{
		Port:     getEnvInt("PORT", 8990),
		DataDir:  expandHome(getEnv("DATA_DIR", "~/.bug-reporter")),
		LogLevel: getEnv("LOG_LEVEL", "info"),
	}

	// Jira configuration
	cfg.Jira = JiraConfig{
		BaseURL:    getEnv("JIRA_BASE_URL", "https://hellofresh.atlassian.net"),
		CloudID:    getEnv("JIRA_CLOUD_ID", "c563471e-8682-4abc-8fa9-5465b05abad5"),
		Email:      getEnv("JIRA_EMAIL", ""),
		APIToken:   getEnv("JIRA_API_TOKEN", ""),
		EpicKey:    getEnv("EPIC_KEY", "REW-323"),
		ProjectKey: getEnv("PROJECT_KEY", "REW"),
	}

	// Validate required Jira fields
	if cfg.Jira.Email == "" || cfg.Jira.APIToken == "" {
		return nil, fmt.Errorf("JIRA_EMAIL and JIRA_API_TOKEN are required")
	}

	// Slack configuration
	slackWebhook := getEnv("SLACK_WEBHOOK_URL", "")
	cfg.Slack = SlackConfig{
		WebhookURL: slackWebhook,
		Enabled:    slackWebhook != "",
	}

	// Bedrock configuration
	awsRegion := getEnv("AWS_REGION", "us-east-1")
	awsAccessKey := getEnv("AWS_ACCESS_KEY_ID", "")
	awsSecretKey := getEnv("AWS_SECRET_ACCESS_KEY", "")
	
	cfg.Bedrock = BedrockConfig{
		Region:    awsRegion,
		AccessKey: awsAccessKey,
		SecretKey: awsSecretKey,
		ModelID:   getEnv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
		Enabled:   awsAccessKey != "" && awsSecretKey != "",
	}

	return cfg, nil
}

// Helper functions

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func expandHome(path string) string {
	if !strings.HasPrefix(path, "~") {
		return path
	}
	
	home, err := os.UserHomeDir()
	if err != nil {
		return path
	}
	
	if path == "~" {
		return home
	}
	
	return filepath.Join(home, path[2:])
}
