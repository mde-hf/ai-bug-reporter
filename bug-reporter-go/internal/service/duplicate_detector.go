package service

import (
	"context"
	"fmt"
	"log/slog"
	"strings"
	"time"

	"github.com/hellofresh/bug-reporter/internal/storage"
	"github.com/google/uuid"
)

// DuplicateResult represents a potential duplicate bug
type DuplicateResult struct {
	Key        string    `json:"key"`
	Summary    string    `json:"summary"`
	Status     string    `json:"status"`
	URL        string    `json:"url"`
	Similarity int       `json:"similarity"`
	Created    time.Time `json:"created"`
}

// DuplicateDetector handles intelligent duplicate bug detection
type DuplicateDetector struct {
	logger *slog.Logger
}

// NewDuplicateDetector creates a new duplicate detector
func NewDuplicateDetector(logger *slog.Logger) *DuplicateDetector {
	return &DuplicateDetector{logger: logger}
}

// CalculateSimilarity calculates similarity score between two bug titles
// Returns score between 0-100, with emphasis on title matching
func (d *DuplicateDetector) CalculateSimilarity(title1, title2, desc1, desc2 string) int {
	title1Lower := strings.ToLower(title1)
	title2Lower := strings.ToLower(title2)

	// Check for substring matches (very high similarity)
	if strings.Contains(title1Lower, title2Lower) || strings.Contains(title2Lower, title1Lower) {
		return 95 // SUBSTRING_MATCH_SCORE
	}

	// Split into words and clean
	title1Words := d.extractWords(title1Lower)
	title2Words := d.extractWords(title2Lower)

	// Filter common stop words
	stopWords := map[string]bool{
		"the": true, "a": true, "an": true, "and": true, "or": true,
		"but": true, "in": true, "on": true, "at": true, "to": true,
		"for": true, "is": true, "are": true, "was": true, "were": true,
	}

	title1Filtered := d.filterWords(title1Words, stopWords)
	title2Filtered := d.filterWords(title2Words, stopWords)

	// Calculate word overlap
	overlap := d.countOverlap(title1Filtered, title2Filtered)

	var similarity float64

	if overlap > 0 {
		// Start with 50% base if there's any overlap
		similarity = 50.0

		// Add points for each matching word
		similarity += float64(overlap * 15)

		// Boost for word length (longer words are more significant)
		for word := range title1Filtered {
			if title2Filtered[word] {
				if len(word) > 6 {
					similarity += 20 // Big boost for long words
				} else if len(word) > 4 {
					similarity += 15 // Medium boost
				} else if len(word) > 3 {
					similarity += 10 // Small boost
				} else {
					similarity += 5
				}
			}
		}
	} else {
		// No filtered overlap - check original words
		overlapOrig := d.countOverlap(title1Words, title2Words)
		maxLen := max(len(title1Words), len(title2Words))
		if maxLen > 0 {
			similarity = (float64(overlapOrig) / float64(maxLen)) * 100
		}
	}

	// Check for matching multi-word phrases (bigrams)
	title1List := strings.Fields(title1Lower)
	title2List := strings.Fields(title2Lower)

	title1Bigrams := d.extractBigrams(title1List)
	title2Bigrams := d.extractBigrams(title2List)

	// Big boost if phrases match
	phraseMatches := d.countOverlap(title1Bigrams, title2Bigrams)
	if phraseMatches > 0 {
		similarity += float64(phraseMatches * 30)
	}

	// Cap at 100
	if similarity > 100 {
		similarity = 100
	}

	return int(similarity)
}

// extractWords splits text into words
func (d *DuplicateDetector) extractWords(text string) map[string]bool {
	words := make(map[string]bool)
	fields := strings.Fields(text)
	for _, word := range fields {
		// Remove punctuation
		word = strings.Trim(word, ".,!?;:\"'()[]{}") 
		if len(word) > 0 {
			words[word] = true
		}
	}
	return words
}

// filterWords removes stop words from word set
func (d *DuplicateDetector) filterWords(words map[string]bool, stopWords map[string]bool) map[string]bool {
	filtered := make(map[string]bool)
	for word := range words {
		if !stopWords[word] && len(word) > 2 {
			filtered[word] = true
		}
	}
	return filtered
}

// countOverlap counts common elements between two sets
func (d *DuplicateDetector) countOverlap(set1, set2 map[string]bool) int {
	count := 0
	for item := range set1 {
		if set2[item] {
			count++
		}
	}
	return count
}

// extractBigrams creates bigrams (two-word sequences) from word list
func (d *DuplicateDetector) extractBigrams(words []string) map[string]bool {
	bigrams := make(map[string]bool)
	for i := 0; i < len(words)-1; i++ {
		bigram := words[i] + " " + words[i+1]
		bigrams[bigram] = true
	}
	return bigrams
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
