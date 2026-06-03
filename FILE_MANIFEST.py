#!/usr/bin/env python3
"""
File manifest for AI App Config Compiler
Complete list of all files and their purposes
"""

FILES_MANIFEST = {
    "ROOT": [
        ("README.md", "Complete project documentation with all features explained"),
        ("PROJECT_SUMMARY.md", "Project completion summary and quick reference"),
        ("start.bat", "Windows startup script - runs backend and frontend"),
        ("start.sh", "Unix/Mac startup script - runs backend and frontend"),
        (".gitignore", "Git ignore patterns for node_modules, __pycache__, etc."),
    ],
    ".GITHUB": [
        (".github/copilot-instructions.md", "Development guidelines and quick start"),
    ],
    "BACKEND": [
        ("backend/app.py", "Main FastAPI application with 5 API endpoints"),
        ("backend/models.py", "20+ Pydantic models for strict type validation"),
        ("backend/database.py", "SQLite database setup and CRUD operations"),
        ("backend/test_prompts.py", "20 test prompts (10 normal + 10 edge cases)"),
        ("backend/test_runner.py", "Test suite to validate pipeline stages"),
        ("backend/requirements.txt", "Python dependencies (fastapi, uvicorn, pydantic)"),
        ("backend/SETUP.md", "Backend installation and configuration guide"),
    ],
    "BACKEND PIPELINE": [
        ("backend/pipeline/__init__.py", "Pipeline package initialization"),
        ("backend/pipeline/intent_extraction.py", "Stage 1: Extract intent from prompts"),
        ("backend/pipeline/system_design.py", "Stage 2: Design system architecture"),
        ("backend/pipeline/schema_generation.py", "Stage 3: Generate UI/API/DB schemas"),
        ("backend/pipeline/validation_layer.py", "Stage 4: Validate configuration"),
        ("backend/pipeline/repair_engine.py", "Stage 5: Auto-repair failed sections"),
        ("backend/pipeline/execution_simulator.py", "Stage 6: Simulate execution flow"),
        ("backend/pipeline/evaluation_framework.py", "Stage 7: Evaluate quality metrics"),
    ],
    "FRONTEND": [
        ("frontend/package.json", "npm dependencies and build scripts"),
        ("frontend/vite.config.js", "Vite configuration with API proxy"),
        ("frontend/tailwind.config.js", "Tailwind CSS theme configuration"),
        ("frontend/postcss.config.js", "PostCSS configuration for CSS processing"),
        ("frontend/index.html", "Main HTML entry point"),
        ("frontend/SETUP.md", "Frontend installation and development guide"),
    ],
    "FRONTEND SRC": [
        ("frontend/src/main.jsx", "React entry point - ReactDOM.createRoot"),
        ("frontend/src/App.jsx", "Main App component with tab navigation"),
        ("frontend/src/api.js", "API client with Axios interceptors"),
        ("frontend/src/index.css", "Global Tailwind CSS and custom styles"),
    ],
    "FRONTEND COMPONENTS": [
        ("frontend/src/components/PromptInput.jsx", "Prompt input form with examples"),
        ("frontend/src/components/PipelineViewer.jsx", "7-stage pipeline visualization"),
        ("frontend/src/components/ConfigViewer.jsx", "Config viewer with multiple tabs"),
        ("frontend/src/components/ValidationReport.jsx", "Validation errors and warnings display"),
        ("frontend/src/components/EvaluationDashboard.jsx", "Quality metrics with score gauges"),
        ("frontend/src/components/History.jsx", "Compilation history browser"),
    ],
}

def print_manifest():
    """Print the complete file manifest"""
    print("\n" + "="*80)
    print(" AI APP CONFIG COMPILER - COMPLETE FILE MANIFEST")
    print("="*80 + "\n")

    total_files = 0
    for section, files in FILES_MANIFEST.items():
        print(f"\n📁 {section}")
        print("-" * 80)
        for filename, description in files:
            print(f"  ✓ {filename:<45} {description}")
            total_files += 1

    print("\n" + "="*80)
    print(f"Total Files Created: {total_files}")
    print("="*80 + "\n")

    # Statistics
    print("\n📊 PROJECT STATISTICS\n")
    print("  Backend Files:        15")
    print("    - Core:            8 (app.py, models.py, database.py, etc.)")
    print("    - Pipeline Stages: 7 (intent, design, schema, validation, repair, simulator, evaluation)")
    print("")
    print("  Frontend Files:       13")
    print("    - Core:            4 (main.jsx, App.jsx, api.js, index.css)")
    print("    - Components:      6 (PromptInput, PipelineViewer, ConfigViewer, etc.)")
    print("    - Config:          3 (vite, tailwind, postcss)")
    print("")
    print("  Documentation:       5")
    print("    - README.md, PROJECT_SUMMARY.md, backend/SETUP.md, frontend/SETUP.md")
    print("")
    print("  Config & Scripts:    3")
    print("    - .gitignore, start.bat, start.sh")
    print("")
    print("  Test Data:           2")
    print("    - test_prompts.py (20 prompts), test_runner.py (test suite)")
    print("\n")

if __name__ == "__main__":
    print_manifest()
