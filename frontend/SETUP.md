# Frontend Setup Guide

## Installation

1. **Install Node.js dependencies**
   ```bash
   npm install
   ```

2. **Verify installation**
   ```bash
   npm --version
   node --version
   ```

## Running the Frontend

### Development Mode
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Build for Production
```bash
npm run build
```

Output goes to `dist/` directory

### Preview Production Build
```bash
npm run preview
```

## Configuration

### API Endpoint
Update `vite.config.js` to change backend URL:
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:8000',
      // ...
    }
  }
}
```

### Tailwind CSS
Customize theme in `tailwind.config.js`:
- Colors
- Typography
- Spacing
- Shadows

### Build Configuration
Modify `vite.config.js` for:
- Port configuration
- Build output
- Environment variables

## Component Structure

```
src/
├── App.jsx                    # Main component & routing
├── api.js                     # API client
├── index.css                  # Global styles
├── main.jsx                   # Entry point
└── components/
    ├── PromptInput.jsx        # Input form
    ├── PipelineViewer.jsx     # Pipeline visualization
    ├── ConfigViewer.jsx       # Config browser
    ├── ValidationReport.jsx   # Validation display
    ├── EvaluationDashboard.jsx # Metrics
    └── History.jsx            # History list
```

## Development Workflow

1. **Start backend** (in another terminal)
   ```bash
   cd backend && python app.py
   ```

2. **Start frontend**
   ```bash
   npm run dev
   ```

3. **Make changes** - Hot reload enabled
4. **Test** - Open http://localhost:5173

## Building for Production

```bash
# Build
npm run build

# Output is in dist/

# Deploy dist/ folder to your hosting
```

## Customization

### Adding New Components
```jsx
// src/components/MyComponent.jsx
export default function MyComponent() {
  return (
    <div className="card p-6">
      {/* Your component */}
    </div>
  );
}
```

### Styling with Tailwind
- Use built-in Tailwind classes
- Dark theme defined in `tailwind.config.js`
- Custom CSS in `src/index.css`

### API Integration
- All API calls through `src/api.js`
- Modify endpoints as needed
- Add error handling as required

## Performance

- Vite provides instant HMR (Hot Module Replacement)
- Tailwind CSS purges unused styles in production
- React lazy loading for components (optional)

## Troubleshooting

### Port Already in Use
```bash
# Use different port
npm run dev -- --port 5174
```

### Can't Connect to Backend
- Verify backend is running on http://localhost:8000
- Check CORS settings in backend
- Check browser console for errors

### Styles Not Loading
```bash
# Rebuild Tailwind
npm run dev

# Clear Vite cache
rm -rf node_modules/.vite
```

### Build Size Too Large
- Check for unused dependencies
- Configure tree-shaking in vite.config.js
- Use dynamic imports for large components

## Browser Support

- Chrome/Edge: Latest
- Firefox: Latest
- Safari: Latest 2 versions
- Modern browsers with ES2020+ support

## Environment Setup

### Recommended Editor Extensions

**VS Code:**
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets
- Vite

### Node.js Version
- Node 16+ recommended
- Node 18+ for best performance

## Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Deploy dist/ folder
```

### Self-Hosted
```bash
npm run build
# Serve dist/ with your web server
```

## Testing

Add testing with Vitest:
```bash
npm install -D vitest
```

## Debugging

### React DevTools
Install React Developer Tools browser extension

### Vite Debug Mode
```bash
DEBUG=vite:* npm run dev
```

### API Debugging
Check browser Network tab in DevTools
