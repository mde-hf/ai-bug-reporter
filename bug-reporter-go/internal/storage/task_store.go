package storage

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// TaskStatus represents the status of a scheduled task
type TaskStatus string

const (
	TaskStatusActive   TaskStatus = "active"
	TaskStatusInactive TaskStatus = "inactive"
	TaskStatusRunning  TaskStatus = "running"
)

// Task represents a scheduled task
type Task struct {
	ID             string     `json:"id"`
	Name           string     `json:"name"`
	Description    string     `json:"description"`
	CronExpression string     `json:"cron_expression"`
	AgentSlug      string     `json:"agent_slug,omitempty"`
	Prompt         string     `json:"prompt"`
	Status         TaskStatus `json:"status"`
	LastRun        *time.Time `json:"last_run,omitempty"`
	NextRun        *time.Time `json:"next_run,omitempty"`
	RunCount       int        `json:"run_count"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

// TaskExecution represents a task execution record
type TaskExecution struct {
	ID         string    `json:"id"`
	TaskID     string    `json:"task_id"`
	StartedAt  time.Time `json:"started_at"`
	FinishedAt *time.Time `json:"finished_at,omitempty"`
	Status     string    `json:"status"`
	Output     string    `json:"output,omitempty"`
	Error      string    `json:"error,omitempty"`
}

// TaskStore handles task persistence
type TaskStore struct {
	db *DB
}

// NewTaskStore creates a new TaskStore
func NewTaskStore(db *DB) *TaskStore {
	return &TaskStore{db: db}
}

// Create creates a new task
func (s *TaskStore) Create(ctx context.Context, task *Task) error {
	if task.ID == "" {
		task.ID = uuid.New().String()
	}
	task.CreatedAt = time.Now()
	task.UpdatedAt = time.Now()

	query := `
		INSERT INTO tasks (
			id, name, description, cron_expression, agent_slug,
			prompt, status, last_run, next_run, run_count,
			created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`

	_, err := s.db.conn.ExecContext(ctx, query,
		task.ID, task.Name, task.Description, task.CronExpression,
		task.AgentSlug, task.Prompt, task.Status, task.LastRun,
		task.NextRun, task.RunCount, task.CreatedAt, task.UpdatedAt,
	)

	if err != nil {
		return fmt.Errorf("creating task: %w", err)
	}

	return nil
}

// GetByID retrieves a task by ID
func (s *TaskStore) GetByID(ctx context.Context, id string) (*Task, error) {
	query := `
		SELECT id, name, description, cron_expression, agent_slug,
		       prompt, status, last_run, next_run, run_count,
		       created_at, updated_at
		FROM tasks
		WHERE id = ?
	`

	task := &Task{}
	err := s.db.conn.QueryRowContext(ctx, query, id).Scan(
		&task.ID, &task.Name, &task.Description, &task.CronExpression,
		&task.AgentSlug, &task.Prompt, &task.Status, &task.LastRun,
		&task.NextRun, &task.RunCount, &task.CreatedAt, &task.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("task not found: %s", id)
	}
	if err != nil {
		return nil, fmt.Errorf("querying task: %w", err)
	}

	return task, nil
}

// ListTasks retrieves all tasks
func (s *TaskStore) ListTasks(ctx context.Context) ([]*Task, error) {
	query := `
		SELECT id, name, description, cron_expression, agent_slug,
		       prompt, status, last_run, next_run, run_count,
		       created_at, updated_at
		FROM tasks
		ORDER BY created_at DESC
	`

	rows, err := s.db.conn.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("querying tasks: %w", err)
	}
	defer rows.Close()

	var tasks []*Task
	for rows.Next() {
		task := &Task{}
		err := rows.Scan(
			&task.ID, &task.Name, &task.Description, &task.CronExpression,
			&task.AgentSlug, &task.Prompt, &task.Status, &task.LastRun,
			&task.NextRun, &task.RunCount, &task.CreatedAt, &task.UpdatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("scanning task: %w", err)
		}
		tasks = append(tasks, task)
	}

	return tasks, rows.Err()
}

// Update updates a task
func (s *TaskStore) Update(ctx context.Context, task *Task) error {
	task.UpdatedAt = time.Now()

	query := `
		UPDATE tasks SET
			name = ?, description = ?, cron_expression = ?, agent_slug = ?,
			prompt = ?, status = ?, last_run = ?, next_run = ?,
			run_count = ?, updated_at = ?
		WHERE id = ?
	`

	_, err := s.db.conn.ExecContext(ctx, query,
		task.Name, task.Description, task.CronExpression, task.AgentSlug,
		task.Prompt, task.Status, task.LastRun, task.NextRun,
		task.RunCount, task.UpdatedAt, task.ID,
	)

	return err
}

// Delete deletes a task
func (s *TaskStore) Delete(ctx context.Context, id string) error {
	query := `DELETE FROM tasks WHERE id = ?`
	_, err := s.db.conn.ExecContext(ctx, query, id)
	return err
}

// CreateExecution creates a task execution record
func (s *TaskStore) CreateExecution(ctx context.Context, exec *TaskExecution) error {
	if exec.ID == "" {
		exec.ID = uuid.New().String()
	}

	query := `
		INSERT INTO task_executions (
			id, task_id, started_at, finished_at, status, output, error
		) VALUES (?, ?, ?, ?, ?, ?, ?)
	`

	_, err := s.db.conn.ExecContext(ctx, query,
		exec.ID, exec.TaskID, exec.StartedAt, exec.FinishedAt,
		exec.Status, exec.Output, exec.Error,
	)

	return err
}
