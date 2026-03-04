package service

import (
	"context"
	"fmt"
	"log/slog"
	"time"

	"github.com/hellofresh/bug-reporter/internal/storage"
)

// BugService handles bug-related business logic
type BugService struct {
	bugStore        *storage.BugStore
	jiraClient      JiraClient
	slackClient     SlackClient
	duplicateDetector *DuplicateDetector
	logger          *slog.Logger
}

// JiraClient interface for Jira operations
type JiraClient interface {
	SearchDuplicates(ctx context.Context, title, description string) ([]DuplicateResult, error)
	CreateBug(ctx context.Context, bug *BugRequest) (*BugResponse, error)
	GetEpicStats(ctx context.Context, epicKey string) (*EpicStats, error)
}

// SlackClient interface for Slack notifications
type SlackClient interface {
	SendNotification(ctx context.Context, message string) error
}

// BugRequest represents a bug creation request
type BugRequest struct {
	Title       string   `json:"title"`
	Description string   `json:"description"`
	Steps       string   `json:"steps"`
	Expected    string   `json:"expected"`
	Actual      string   `json:"actual"`
	Priority    string   `json:"priority"`
	Environment string   `json:"environment"`
	Project     string   `json:"project"`
	Attachments [][]byte `json:"-"` // File contents
}

// BugResponse represents a bug creation response
type BugResponse struct {
	Key     string `json:"key"`
	URL     string `json:"url"`
	Message string `json:"message"`
}

// EpicStats represents dashboard statistics
type EpicStats struct {
	TotalCount      int                    `json:"total_count"`
	OpenCount       int                    `json:"open_count"`
	InProgressCount int                    `json:"in_progress_count"`
	ResolvedCount   int                    `json:"resolved_count"`
	ClosedCount     int                    `json:"closed_count"`
	ByStatus        map[string]int         `json:"by_status"`
	ByPriority      map[string]int         `json:"by_priority"`
	ByPlatform      map[string]int         `json:"by_platform"`
	PriorityMatrix  map[string]map[string]int `json:"priority_matrix"`
	CreationTrend   []TrendData            `json:"creation_trend"`
	AvgResolutionDays string               `json:"avg_resolution_days"`
}

// TrendData represents time-series data
type TrendData struct {
	Date  string `json:"date"`
	Count int    `json:"count"`
}

// NewBugService creates a new BugService
func NewBugService(
	bugStore *storage.BugStore,
	jiraClient JiraClient,
	slackClient SlackClient,
	logger *slog.Logger,
) *BugService {
	return &BugService{
		bugStore:         bugStore,
		jiraClient:       jiraClient,
		slackClient:      slackClient,
		duplicateDetector: NewDuplicateDetector(logger),
		logger:           logger,
	}
}

// SearchDuplicates searches for potential duplicate bugs
func (s *BugService) SearchDuplicates(ctx context.Context, title, description string) ([]DuplicateResult, error) {
	s.logger.Info("searching for duplicates", "title", title)

	// Search via Jira API
	duplicates, err := s.jiraClient.SearchDuplicates(ctx, title, description)
	if err != nil {
		return nil, fmt.Errorf("searching jira: %w", err)
	}

	s.logger.Info("found potential duplicates", "count", len(duplicates))
	return duplicates, nil
}

// CreateBug creates a new bug in Jira and stores it locally
func (s *BugService) CreateBug(ctx context.Context, req *BugRequest) (*BugResponse, error) {
	s.logger.Info("creating bug", "title", req.Title, "project", req.Project)

	// Create in Jira
	resp, err := s.jiraClient.CreateBug(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("creating jira bug: %w", err)
	}

	// Store locally for history
	bug := &storage.Bug{
		Key:         resp.Key,
		Title:       req.Title,
		Description: req.Description,
		Steps:       req.Steps,
		Expected:    req.Expected,
		Actual:      req.Actual,
		Priority:    req.Priority,
		Environment: req.Environment,
		Project:     req.Project,
		Status:      "On Hold",
		JiraURL:     resp.URL,
	}

	if err := s.bugStore.Create(ctx, bug); err != nil {
		s.logger.Warn("failed to store bug locally", "key", resp.Key, "error", err)
		// Don't fail the request if local storage fails
	}

	// Send Slack notification (fire and forget)
	go func() {
		notifCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		
		message := fmt.Sprintf("🐛 New Bug Created: %s\n%s\nPriority: %s | Environment: %s\n%s",
			req.Title, resp.Key, req.Priority, req.Environment, resp.URL)
		
		if err := s.slackClient.SendNotification(notifCtx, message); err != nil {
			s.logger.Warn("failed to send slack notification", "error", err)
		}
	}()

	s.logger.Info("bug created successfully", "key", resp.Key)
	return resp, nil
}

// GetDashboardStats retrieves epic statistics
func (s *BugService) GetDashboardStats(ctx context.Context, epicKey string) (*EpicStats, error) {
	return s.jiraClient.GetEpicStats(ctx, epicKey)
}
