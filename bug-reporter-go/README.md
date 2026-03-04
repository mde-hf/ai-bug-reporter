# Bug Reporter - Go + React

Professional bug reporting tool for HelloFresh, rewritten in Go with React frontend following Agento's architecture patterns.

## Features

- **Bug Creation** with intelligent duplicate detection
- **Dashboard** with real-time metrics and trends
- **AI Test Case Generation** powered by AWS Bedrock (Claude)
- **Multi-Project Support** (Loyalty 2.0, Virality, Rewards squads)
- **Task Scheduler** for automated reports and cleanup
- **Notifications** via Slack and Email
- **File Uploads** (screenshots, videos)
- **Professional UI** with HelloFresh branding

## Tech Stack

- **Backend**: Go 1.21+ with Chi router
- **Frontend**: React 18 + TypeScript + Vite
- **Database**: SQLite for caching and history
- **AI**: AWS Bedrock (Claude 3.5 Sonnet)
- **Logging**: Structured JSON logs (slog)
- **Scheduler**: gocron for recurring tasks
- **Integrations**: Jira, Slack

## Requirements

- Go 1.21 or higher
- Node.js 18+ (for frontend development)
- Jira API credentials
- AWS Bedrock access (optional, for AI features)

## Quick Start

### Development

```bash
# Backend
make dev-backend

# Frontend (separate terminal)
make dev-frontend

# Open http://localhost:8990
```

### Production Build

```bash
make build

# Run the binary
./bin/bug-reporter
```

## Project Structure

```
bug-reporter-go/
├── cmd/bug-reporter/       # Application entrypoint
├── internal/
│   ├── api/                # HTTP handlers
│   ├── config/             # Configuration management
│   ├── service/            # Business logic layer
│   ├── storage/            # Database layer (SQLite)
│   ├── integrations/       # External services (Jira, Slack, Bedrock)
│   ├── scheduler/          # Task scheduling
│   ├── notification/       # Notification system
│   └── logger/             # Structured logging
├── web/                    # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   ├── hooks/          # Custom React hooks
│   │   └── styles/         # CSS/styling
│   └── public/             # Static assets
└── Makefile                # Build commands
```

## Configuration

All configuration via environment variables:

```bash
# Jira
JIRA_BASE_URL=https://hellofresh.atlassian.net
JIRA_EMAIL=your-email@hellofresh.com
JIRA_API_TOKEN=your-api-token
JIRA_CLOUD_ID=c563471e-8682-4abc-8fa9-5465b05abad5
EPIC_KEY=REW-323
PROJECT_KEY=REW

# AWS Bedrock (optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# Slack (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Server
PORT=8990
LOG_LEVEL=info
DATA_DIR=~/.bug-reporter
```

## Development

### Backend Development

```bash
# Install Go dependencies
go mod download

# Run with hot reload (using air)
go install github.com/cosmtrek/air@latest
air

# Run tests
make test

# Format code
make fmt

# Lint
make lint
```

### Frontend Development

```bash
cd web
npm install
npm run dev
```

## Building

### Single Binary (includes embedded frontend)

```bash
make build
```

This produces `./bin/bug-reporter` with the React frontend embedded.

### Docker

```bash
docker build -t bug-reporter .
docker run -p 8990:8990 --env-file .env bug-reporter
```

## Deployment

### Binary Deployment

```bash
# Build
make build

# Copy to server
scp bin/bug-reporter user@server:/usr/local/bin/

# Run as service (systemd example)
sudo systemctl start bug-reporter
```

### Docker Deployment

```bash
docker compose up -d
```

## Migration from Python Version

The original Python version is preserved in the parent directory. This Go rewrite includes all features plus:

- ✅ Better performance (compiled Go vs interpreted Python)
- ✅ Single binary deployment (no venv/pip needed)
- ✅ Built-in task scheduler
- ✅ Enhanced notification system
- ✅ SQLite for local caching and history
- ✅ Structured logging with slog
- ✅ Type safety
- ✅ Better concurrency with goroutines
- ✅ Modern React frontend

## Architecture

Following Agento's architecture patterns:

1. **Storage Layer**: SQLite with repositories for bugs, tasks, settings
2. **Service Layer**: Business logic separated from HTTP handlers
3. **API Layer**: RESTful endpoints with JSON responses
4. **Integration Layer**: External services (Jira, Slack, Bedrock)
5. **Event System**: Pub/sub for notifications and logging
6. **Scheduler**: Cron-based task execution

## License

MIT

## Maintained by

HelloFresh Loyalty & Virality Tribe
