package storage

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

// SettingsStore handles application settings persistence
type SettingsStore struct {
	db *DB
}

// NewSettingsStore creates a new SettingsStore
func NewSettingsStore(db *DB) *SettingsStore {
	return &SettingsStore{db: db}
}

// Get retrieves a setting value by key
func (s *SettingsStore) Get(ctx context.Context, key string) (string, error) {
	query := `SELECT value FROM settings WHERE key = ?`

	var value string
	err := s.db.conn.QueryRowContext(ctx, query, key).Scan(&value)
	if err == sql.ErrNoRows {
		return "", fmt.Errorf("setting not found: %s", key)
	}
	if err != nil {
		return "", fmt.Errorf("querying setting: %w", err)
	}

	return value, nil
}

// Set stores or updates a setting
func (s *SettingsStore) Set(ctx context.Context, key, value string) error {
	query := `
		INSERT INTO settings (key, value, updated_at)
		VALUES (?, ?, ?)
		ON CONFLICT(key) DO UPDATE SET
			value = excluded.value,
			updated_at = excluded.updated_at
	`

	_, err := s.db.conn.ExecContext(ctx, query, key, value, time.Now())
	if err != nil {
		return fmt.Errorf("setting value: %w", err)
	}

	return nil
}

// Delete removes a setting
func (s *SettingsStore) Delete(ctx context.Context, key string) error {
	query := `DELETE FROM settings WHERE key = ?`
	_, err := s.db.conn.ExecContext(ctx, query, key)
	return err
}

// GetAll retrieves all settings
func (s *SettingsStore) GetAll(ctx context.Context) (map[string]string, error) {
	query := `SELECT key, value FROM settings`

	rows, err := s.db.conn.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("querying settings: %w", err)
	}
	defer rows.Close()

	settings := make(map[string]string)
	for rows.Next() {
		var key, value string
		if err := rows.Scan(&key, &value); err != nil {
			return nil, fmt.Errorf("scanning setting: %w", err)
		}
		settings[key] = value
	}

	return settings, rows.Err()
}
