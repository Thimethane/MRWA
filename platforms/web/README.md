# MRWA Web Dashboard

Production-quality React dashboard for MRWA workflow execution and monitoring.

## Features

- ✅ **Workflow Templates** - Pre-configured task templates
- ✅ **Custom Upload** - Upload files and add links
- ✅ **Real-Time Monitoring** - Live execution logs
- ✅ **Progress Visualization** - Step-by-step progress tracking
- ✅ **Validation Alerts** - Visual failure indicators
- ✅ **Self-Correction Display** - Shows correction strategies
- ✅ **Artifact Viewer** - Download and view outputs
- ✅ **Responsive Design** - Works on desktop and mobile

## Quick Start
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Configuration

### Environment Variables

Create `platforms/web/.env`:
```bash
REACT_APP_API_URL=http://localhost:8000/api
```

### API Connection

The dashboard connects to the MRWA API server. Make sure the server is running before starting the dashboard.

## Project Structure
