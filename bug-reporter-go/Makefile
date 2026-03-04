.PHONY: help build dev-backend dev-frontend test fmt lint clean install-deps

# Default target
.DEFAULT_GOAL := help

# Build configuration
BINARY_NAME=bug-reporter
BUILD_DIR=bin
GO_FILES=$(shell find . -name '*.go' -type f)
VERSION=$(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
BUILD_TIME=$(shell date -u '+%Y-%m-%d_%H:%M:%S')
LDFLAGS=-ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME)"

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-deps: ## Install Go and Node dependencies
	@echo "Installing Go dependencies..."
	go mod download
	go mod tidy
	@echo "Installing Node dependencies..."
	cd web && npm install

build: ## Build production binary with embedded frontend
	@echo "Building frontend..."
	cd web && npm run build
	@echo "Building backend..."
	mkdir -p $(BUILD_DIR)
	go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/bug-reporter
	@echo "Binary created: $(BUILD_DIR)/$(BINARY_NAME)"

build-backend-only: ## Build backend without frontend
	@echo "Building backend..."
	mkdir -p $(BUILD_DIR)
	go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/bug-reporter

dev-backend: ## Run backend with hot reload (requires air)
	@which air > /dev/null || (echo "Installing air..." && go install github.com/cosmtrek/air@latest)
	air

dev-frontend: ## Run frontend dev server
	cd web && npm run dev

dev: ## Run both backend and frontend (requires tmux or run in separate terminals)
	@echo "Run these in separate terminals:"
	@echo "  Terminal 1: make dev-backend"
	@echo "  Terminal 2: make dev-frontend"

test: ## Run tests
	@echo "Running Go tests..."
	go test -v -race -coverprofile=coverage.out ./...
	@echo "Running frontend tests..."
	cd web && npm run test

test-coverage: ## Run tests with coverage report
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: coverage.html"

fmt: ## Format code
	@echo "Formatting Go code..."
	go fmt ./...
	gofmt -s -w .
	@echo "Formatting frontend code..."
	cd web && npm run format

lint: ## Run linters
	@echo "Running golangci-lint..."
	@which golangci-lint > /dev/null || (echo "Installing golangci-lint..." && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest)
	golangci-lint run ./...
	@echo "Running frontend lint..."
	cd web && npm run lint

clean: ## Clean build artifacts
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR)
	rm -rf web/dist
	rm -rf web/node_modules
	rm -f coverage.out coverage.html
	@echo "Clean complete"

run: build ## Build and run the application
	./$(BUILD_DIR)/$(BINARY_NAME)

docker-build: ## Build Docker image
	docker build -t bug-reporter:$(VERSION) .

docker-run: ## Run Docker container
	docker run -p 8990:8990 --env-file .env bug-reporter:$(VERSION)

# Development helpers
watch-backend: ## Watch Go files and rebuild (manual alternative to air)
	@which entr > /dev/null || (echo "entr not found. Install with: brew install entr" && exit 1)
	find . -name '*.go' | entr -r sh -c 'go build -o $(BUILD_DIR)/$(BINARY_NAME) ./cmd/bug-reporter && $(BUILD_DIR)/$(BINARY_NAME)'

deps-upgrade: ## Upgrade all dependencies
	@echo "Upgrading Go dependencies..."
	go get -u ./...
	go mod tidy
	@echo "Upgrading Node dependencies..."
	cd web && npm update

# Database migrations (if needed in future)
migrate-up: ## Run database migrations
	@echo "Running migrations..."
	# Add migration tool here

migrate-down: ## Rollback database migrations
	@echo "Rolling back migrations..."
	# Add migration tool here
