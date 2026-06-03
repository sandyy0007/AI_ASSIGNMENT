"""
Main FastAPI application for AI App Config Compiler
Orchestrates the 7-stage pipeline
"""
import time
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any

from models import UserPrompt, AIAppConfig
from database import init_db, save_compilation, save_pipeline_stage, get_compilation, get_compilation_history
from pipeline.intent_extraction import IntentExtractor
from pipeline.system_design import SystemDesigner
from pipeline.schema_generation import SchemaGenerator
from pipeline.validation_layer import ValidationLayer
from pipeline.repair_engine import RepairEngine
from pipeline.execution_simulator import ExecutionSimulator
from pipeline.evaluation_framework import EvaluationFramework

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="AI App Config Compiler",
    description="Convert open-ended product prompts into strict valid JSON app configurations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline stages
intent_extractor = IntentExtractor()
system_designer = SystemDesigner()
schema_generator = SchemaGenerator()
validation_layer = ValidationLayer()
repair_engine = RepairEngine()
execution_simulator = ExecutionSimulator()
evaluation_framework = EvaluationFramework()


class PipelineOrchestrator:
    """Orchestrates the full pipeline"""

    def __init__(self):
        self.stages = []
        self.config = {}

    def run(self, prompt: str, context: str = None) -> Dict[str, Any]:
        """Run full pipeline"""
        compilation_id = None
        try:
            # Stage 1: Intent Extraction
            start_time = time.time()
            intent_result = intent_extractor.extract(prompt)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "intent_extraction",
                "output": intent_result,
                "time": stage_time
            })

            if not intent_result.get("success"):
                raise Exception(f"Intent extraction failed: {intent_result.get('error')}")

            # Stage 2: System Design
            start_time = time.time()
            design_result = system_designer.design(intent_result)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "system_design",
                "output": design_result,
                "time": stage_time
            })

            if not design_result.get("success"):
                raise Exception(f"System design failed: {design_result.get('error')}")

            # Stage 3: Schema Generation
            start_time = time.time()
            schema_result = schema_generator.generate(design_result)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "schema_generation",
                "output": schema_result,
                "time": stage_time
            })

            if not schema_result.get("success"):
                raise Exception(f"Schema generation failed: {schema_result.get('error')}")

            # Prepare config
            self.config = {
                **intent_result.get("data", {}),
                **design_result.get("data", {}),
                **schema_result.get("data", {})
            }

            # Stage 4: Validation Layer
            start_time = time.time()
            validation_result = validation_layer.validate(self.config)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "validation_layer",
                "output": validation_result,
                "time": stage_time
            })

            # Stage 5: Repair Engine
            start_time = time.time()
            validation_errors = validation_result.get("data", {}).get("errors", [])
            repair_result = repair_engine.repair(self.config, validation_errors)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "repair_engine",
                "output": repair_result,
                "time": stage_time
            })

            if repair_result.get("data", {}).get("was_repaired"):
                self.config = repair_result.get("data", {}).get("repaired_config", self.config)

            # Stage 6: Execution Simulator
            start_time = time.time()
            simulation_result = execution_simulator.simulate(self.config)
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "execution_simulator",
                "output": simulation_result,
                "time": stage_time
            })

            # Stage 7: Evaluation Framework
            start_time = time.time()
            evaluation_result = evaluation_framework.evaluate(
                self.config,
                validation_result,
                simulation_result
            )
            stage_time = time.time() - start_time
            self.stages.append({
                "name": "evaluation_framework",
                "output": evaluation_result,
                "time": stage_time
            })

            # Build final config
            final_config = {
                "app_name": self.config.get("app_name", "GeneratedApp"),
                "timestamp": datetime.utcnow().isoformat(),
                "assumptions": self.config.get("assumptions", []),
                "entities": self.config.get("entities", []),
                "roles": self.config.get("roles", []),
                "permissions": self.config.get("permissions", {}),
                "ui_schema": self.config.get("ui_schema", {}),
                "api_schema": self.config.get("api_schema", {}),
                "database_schema": self.config.get("database_schema", {}),
                "auth_rules": self.config.get("auth_rules", []),
                "business_logic": self.config.get("business_logic", {}),
                "validation_report": validation_result.get("data", {}),
                "execution_simulation": simulation_result.get("data", {}),
                "evaluation_framework": evaluation_result.get("data", {})
            }

            # Save to database
            compilation_id = save_compilation(
                prompt=prompt,
                app_name=final_config.get("app_name"),
                config=final_config,
                validation_passed=validation_result.get("data", {}).get("is_valid", False),
                repair_applied=repair_result.get("data", {}).get("was_repaired", False),
                overall_score=evaluation_result.get("overall_score", 0.0)
            )

            # Save pipeline stages
            for stage in self.stages:
                save_pipeline_stage(
                    compilation_id=compilation_id,
                    stage_name=stage["name"],
                    stage_output=stage["output"],
                    execution_time=stage["time"]
                )

            return {
                "success": True,
                "compilation_id": compilation_id,
                "config": final_config,
                "pipeline_stages": self.stages
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "compilation_id": compilation_id
            }


# API Endpoints

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/compile")
async def compile_prompt(user_prompt: UserPrompt):
    """
    Compile a product prompt into AI App Configuration
    
    7-stage pipeline:
    1. Intent Extraction - Extract user intent
    2. System Design Layer - Design architecture
    3. Schema Generation - Generate schemas
    4. Validation Layer - Validate config
    5. Repair Engine - Fix issues
    6. Execution Simulator - Simulate execution
    7. Evaluation Framework - Evaluate quality
    """
    try:
        orchestrator = PipelineOrchestrator()
        result = orchestrator.run(user_prompt.prompt, user_prompt.context)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compilation/{compilation_id}")
async def get_compilation_result(compilation_id: int):
    """Get compilation result by ID"""
    try:
        result = get_compilation(compilation_id)
        if not result:
            raise HTTPException(status_code=404, detail="Compilation not found")

        # Parse JSON fields
        config = json.loads(result.get("config_json", "{}"))

        return {
            "id": result.get("id"),
            "prompt": result.get("prompt"),
            "app_name": result.get("app_name"),
            "config": config,
            "validation_passed": result.get("validation_passed"),
            "repair_applied": result.get("repair_applied"),
            "overall_score": result.get("overall_score"),
            "created_at": result.get("created_at")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history(limit: int = 50):
    """Get compilation history"""
    try:
        history = get_compilation_history(limit)
        return {
            "items": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/docs-config")
async def get_config_schema():
    """Get configuration schema documentation"""
    return {
        "schema": {
            "app_name": "string - Application name",
            "assumptions": "List[string] - System assumptions",
            "entities": "List[Entity] - System entities with attributes and relationships",
            "roles": "List[Role] - User roles with permissions",
            "permissions": "Dict[string, List[string]] - Role-based permissions",
            "ui_schema": "UISchema - User interface configuration",
            "api_schema": "APISchema - REST API configuration",
            "database_schema": "DatabaseSchema - Database structure",
            "auth_rules": "List[AuthRule] - Authentication/authorization rules",
            "business_logic": "BusinessLogic - Business rules and constraints",
            "validation_report": "ValidationResult - Validation results",
            "execution_simulation": "ExecutionSimulation - Execution simulation results",
            "evaluation_framework": "EvaluationFramework - Quality evaluation metrics"
        }
    }


# Error handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
