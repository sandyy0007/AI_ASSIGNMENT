# AI App Config Compiler - Project Instructions

## Quick Start

### Option 1: Automated Start (Recommended)

**Windows:**
```bash
./start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Then open: http://localhost:5173

## Architecture Overview

### 7-Stage Pipeline Architecture

1. **Intent Extraction** - Parse user intent
2. **System Design Layer** - Design architecture
3. **Schema Generation** - Generate UI/API/DB schemas
4. **Validation Layer** - Validate configuration
5. **Repair Engine** - Auto-fix issues
6. **Execution Simulator** - Simulate execution
7. **Evaluation Framework** - Quality assessment

### Output Includes

- app_name
- assumptions
- entities with attributes and relationships
- roles with permissions
- ui_schema (pages, components, themes)
- api_schema (endpoints, auth, rate limiting)
- database_schema (tables, relationships, indexes)
- auth_rules
- business_logic
- validation_report
- execution_simulation
- evaluation_framework with metrics

## File Structure

```
backend/
├── app.py                 # FastAPI server
├── models.py              # Pydantic models
├── database.py            # SQLite setup
├── test_prompts.py        # 20 test cases
├── requirements.txt
└── pipeline/
    ├── intent_extraction.py
    ├── system_design.py
    ├── schema_generation.py
    ├── validation_layer.py
    ├── repair_engine.py
    ├── execution_simulator.py
    └── evaluation_framework.py

frontend/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── index.html
└── src/
    ├── App.jsx
    ├── api.js
    └── components/
        ├── PromptInput.jsx
        ├── PipelineViewer.jsx
        ├── ConfigViewer.jsx
        ├── ValidationReport.jsx
        ├── EvaluationDashboard.jsx
        └── History.jsx
```

## Key Features

✓ 7 modular pipeline stages  
✓ Automatic error repair  
✓ Professional dark UI  
✓ Real-time pipeline visualization  
✓ Quality metrics dashboard  
✓ 20 test prompts (10 normal + 10 edge cases)  
✓ SQLite persistent storage  
✓ Comprehensive JSON configuration  
✓ Responsive design  
✓ Type-safe with Pydantic  

## API Endpoints

- `POST /compile` - Compile a prompt
- `GET /compilation/{id}` - Get result
- `GET /history` - Get compilation history
- `GET /health` - Health check
- `GET /docs-config` - Configuration schema

## Example Prompt

```
Build an e-commerce platform where customers can browse products, 
add them to a shopping cart, and checkout with payment processing. 
The system should support multiple product categories, user reviews, 
and seller management.
```

## Testing

Use any of the 20 provided test prompts in test_prompts.py

## Troubleshooting

### Backend won't start
```bash
cd backend
pip install -r requirements.txt
```

### Frontend won't connect
- Check backend is running on http://localhost:8000
- Check browser Network tab

### Database errors
```bash
cd backend
rm app_config.db
python app.py
```

## Development Notes

- Backend: Python 3.8+, FastAPI, Uvicorn
- Frontend: React 18, Vite, Tailwind CSS
- Database: SQLite (auto-created)
- No external ML/AI services required

## Performance

- ~1-3 seconds per compilation
- 7 stages run sequentially
- All data stored locally
- No API rate limits in dev mode

## Next Steps

1. Run the application
2. Enter a product prompt
3. Click "Generate Configuration"
4. Explore the generated config through different tabs
5. Try edge case prompts to test robustness

## Documentation

- README.md - Full project documentation
- backend/SETUP.md - Backend configuration guide
- frontend/SETUP.md - Frontend configuration guide
