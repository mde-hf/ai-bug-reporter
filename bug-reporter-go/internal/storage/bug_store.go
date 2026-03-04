package storage

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// Bug represents a bug report
type Bug struct {
	ID              string    `json:"id"`
	Key             string    `json:"key"`
	Title           string    `json:"title"`
	Description     string    `json:"description"`
	Steps           string    `json:"steps"`
	Expected        string    `json:"expected"`
	Actual          string    `json:"actual"`
	Priority        string    `json:"priority"`
	Environment     string    `json:"environment"`
	Project         string    `json:"project"`
	Status          string    `json:"status"`
	JiraURL         string    `json:"jira_url"`
	SimilarityScore int       `json:"similarity_score,omitempty"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// BugStore handles bug persistence
type BugStore struct {
	db *DB
}

// NewBugStore creates a new BugStore
func NewBugStore(db *DB) *BugStore {
	return &BugStore{db: db}
}

// Create creates a new bug record
func (s *BugStore) Create(ctx context.Context, bug *Bug) error {
	if bug.ID == "" {
		bug.ID = uuid.New().String()
	}
	bug.CreatedAt = time.Now()
	bug.UpdatedAt = time.Now()

	query := `
		INSERT INTO bugs (
			id, key, title, description, steps, expected, actual,
			priority, environment, project, status, jira_url,
			similarity_score, created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`

	_, err := s.db.conn.ExecContext(ctx, query,
		bug.ID, bug.Key, bug.Title, bug.Description, bug.Steps,
		bug.Expected, bug.Actual, bug.Priority, bug.Environment,
		bug.Project, bug.Status, bug.JiraURL, bug.SimilarityScore,
		bug.CreatedAt, bug.UpdatedAt,
	)

	if err != nil {
		return fmt.Errorf("creating bug: %w", err)
	}

	return nil
}

// GetByKey retrieves a bug by its Jira key
func (s *BugStore) GetByKey(ctx context.Context, key string) (*Bug, error) {
	query := `
		SELECT id, key, title, description, steps, expected, actual,
		       priority, environment, project, status, jira_url,
		       similarity_score, created_at, updated_at
		FROM bugs
		WHERE key = ?
	`

	bug := &Bug{}
	err := s.db.conn.QueryRowContext(ctx, query, key).Scan(
		&bug.ID, &bug.Key, &bug.Title, &bug.Description, &bug.Steps,
		&bug.Expected, &bug.Actual, &bug.Priority, &bug.Environment,
		&bug.Project, &bug.Status, &bug.JiraURL, &bug.SimilarityScore,
		&bug.CreatedAt, &bug.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("bug not found: %s", key)
	}
	if err != nil {
		return nil, fmt.Errorf("querying bug: %w", err)
	}

	return bug, nil
}

// List retrieves bugs with optional filters
func (s *BugStore) List(ctx context.Context, project string, limit int) ([]*Bug, error) {
	query := `
		SELECT id, key, title, description, steps, expected, actual,
		       priority, environment, project, status, jira_url,
		       similarity_score, created_at, updated_at
		FROM bugs
		WHERE project = ?
		ORDER BY created_at DESC
		LIMIT ?
	`

	rows, err := s.db.conn.QueryContext(ctx, query, project, limit)
	if err != nil {
		return nil, fmt.Errorf("querying bugs: %w", err)
	}
	defer rows.Close()

	var bugs []*Bug
	for rows.Next() {
		bug := &Bug{}
		err := rows.Scan(
			&bug.ID, &bug.Key, &bug.Title, &bug.Description, &bug.Steps,
			&bug.Expected, &bug.Actual, &bug.Priority, &bug.Environment,
			&bug.Project, &bug.Status, &bug.JiraURL, &bug.SimilarityScore,
			&bug.CreatedAt, &bug.UpdatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("scanning bug: %w", err)
		}
		bugs = append(bugs, bug)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterating bugs: %w", err)
	}

	return bugs, nil
}

// Update updates a bug record
func (s *BugStore) Update(ctx context.Context, bug *Bug) error {
	bug.UpdatedAt = time.Now()

	query := `
		UPDATE bugs SET
			title = ?, description = ?, steps = ?, expected = ?,
			actual = ?, priority = ?, environment = ?, project = ?,
			status = ?, jira_url = ?, similarity_score = ?, updated_at = ?
		WHERE key = ?
	`

	result, err := s.db.conn.ExecContext(ctx, query,
		bug.Title, bug.Description, bug.Steps, bug.Expected,
		bug.Actual, bug.Priority, bug.Environment, bug.Project,
		bug.Status, bug.JiraURL, bug.SimilarityScore, bug.UpdatedAt,
		bug.Key,
	)

	if err != nil {
		return fmt.Errorf("updating bug: %w", err)
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("getting rows affected: %w", err)
	}

	if rows == 0 {
		return fmt.Errorf("bug not found: %s", bug.Key)
	}

	return nil
}

// CountByProject returns the count of bugs for a project
func (s *BugStore) CountByProject(ctx context.Context, project string) (int, error) {
	query := `SELECT COUNT(*) FROM bugs WHERE project = ?`

	var count int
	err := s.db.conn.QueryRowContext(ctx, query, project).Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("counting bugs: %w", err)
	}

	return count, nil
}
