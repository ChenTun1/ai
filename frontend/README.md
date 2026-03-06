# PetVoyage Frontend

React + Vite frontend for the PetVoyage AI Pet Travel Assistant.

## Tech Stack

- **React 18** - UI framework
- **Vite 5** - Build tool and dev server
- **Tailwind CSS 3** - Utility-first CSS framework
- **Axios** - HTTP client
- **Zustand** - State management
- **TanStack React Query** - Server state management

## Getting Started

```bash
# Install dependencies
npm install

# Start development server (port 3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
  src/
    api/
      client.js       # Axios instance with API proxy config
    pages/
      Home.jsx        # Home page component
    App.jsx           # Main app with navigation and layout
    main.jsx          # React entry point with QueryClient setup
    index.css         # Tailwind CSS imports and base styles
  index.html          # HTML entry point
  vite.config.js      # Vite config with API proxy to :8000
  tailwind.config.js  # Tailwind CSS config with custom colors
  postcss.config.js   # PostCSS config
  package.json        # Dependencies and scripts
```

## API Proxy

Development server proxies `/api/*` requests to `http://localhost:8000`, so the backend should be running on port 8000.
