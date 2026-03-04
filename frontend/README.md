# Bug Reporter - React Frontend

Modern React + TypeScript frontend for the HelloFresh Bug Reporter tool.

## 🎯 Features

- **Report Bugs** with intelligent duplicate detection
- **Dashboard** with real-time metrics and charts
- **AI Test Case Generator** powered by AWS Bedrock (Claude)
- **Multi-Project Support** (Loyalty 2.0, Virality, Rewards squads)
- **File Uploads** for screenshots and videos
- **HelloFresh Branding** with professional styling

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- Python backend running on `http://localhost:5000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
# Start React dev server (with proxy to Python backend)
npm run dev

# Frontend will run on http://localhost:3000
# API calls to /api/* will proxy to http://localhost:5000
```

### Build for Production

```bash
npm run build

# Output will be in ./dist folder
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── Header.tsx       # Navigation header
│   │   ├── BugForm.tsx      # Bug creation form
│   │   ├── DuplicatesList.tsx # Duplicate bugs display
│   │   ├── Dashboard.tsx    # Metrics dashboard
│   │   └── TestCaseGenerator.tsx # AI test generator
│   ├── pages/               # Page components
│   │   ├── ReportBugPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── TestCasesPage.tsx
│   ├── services/            # API clients
│   │   └── api.ts          # Axios instance & endpoints
│   ├── types/               # TypeScript types
│   │   └── api.ts          # API type definitions
│   ├── styles/              # Global styles
│   │   └── globals.css     # HelloFresh brand styling
│   ├── App.tsx              # Main app component
│   └── main.tsx             # React entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

## 🔧 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **CSS** - Styling with HelloFresh brand colors

## 🎨 HelloFresh Brand Colors

```css
--hf-green: #91C11E
--hf-green-dark: #7DA91A
--hf-orange: #FF6C37
```

## 🔗 API Integration

The frontend connects to the Python backend at `http://localhost:5000`:

### Endpoints Used

- `POST /api/check-duplicates` - Check for duplicate bugs
- `POST /api/create-bug` - Create a new bug
- `GET /api/epic-stats` - Get dashboard statistics
- `POST /api/generate-test-cases` - Generate AI test cases

### Proxy Configuration

Development server proxies `/api/*` requests to Python backend:

```ts
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    },
  },
}
```

## 🚀 Running with Python Backend

### Terminal 1: Python Backend
```bash
cd "/Users/mde/bug creation"
./start.sh
# Backend runs on http://localhost:5000
```

### Terminal 2: React Frontend
```bash
cd "/Users/mde/bug creation/frontend"
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

Open **http://localhost:3000** in your browser!

## 📦 Production Deployment

### Option 1: Serve from Python Backend

Build the React app and serve it from Flask:

```bash
# Build frontend
cd frontend
npm run build

# Copy dist to Python static folder
cp -r dist ../static/react

# Update Flask to serve from /static/react
```

### Option 2: Separate Deployment

Deploy frontend and backend separately:

- Frontend → Vercel/Netlify
- Backend → Python server

Update API base URL in production build.

## 🧪 Development

### Hot Reload

Vite provides instant hot module replacement (HMR). Changes to components reflect immediately.

### TypeScript

All API calls and components are fully typed. TypeScript catches errors at compile time.

### React Query

Automatic caching, refetching, and state management for API calls:

```ts
const { data, isLoading } = useQuery({
  queryKey: ['epic-stats'],
  queryFn: () => bugApi.getEpicStats(),
  refetchInterval: 15 * 60 * 1000, // Auto-refresh every 15 min
});
```

## 📝 Available Scripts

```bash
npm run dev       # Start dev server
npm run build     # Build for production
npm run preview   # Preview production build
npm run lint      # Run ESLint
```

## 🐛 Troubleshooting

### Port 3000 already in use
```bash
# Change port in vite.config.ts or use:
PORT=3001 npm run dev
```

### API calls fail
- Ensure Python backend is running on port 5000
- Check proxy configuration in `vite.config.ts`
- Verify CORS is enabled in Python backend

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🎉 Features Implemented

✅ Project selection (Loyalty 2.0, Virality, etc.)  
✅ Real-time duplicate detection (debounced)  
✅ Complete bug form with all fields  
✅ File upload for screenshots/videos  
✅ Duplicate bugs display with severity colors  
✅ Dashboard with stats cards  
✅ Priority × Status matrix  
✅ Platform distribution  
✅ Bug creation trend chart (Chart.js)  
✅ AI test case generator  
✅ Copy to clipboard functionality  
✅ HelloFresh branding and styling  
✅ Responsive design  
✅ TypeScript type safety  
✅ React Query state management  

## 📄 License

MIT - HelloFresh Loyalty & Virality Tribe
