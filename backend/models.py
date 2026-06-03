"""
Pydantic models for the AI App Config Compiler
"""
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime


# Input Models
class UserPrompt(BaseModel):
    """Input prompt from user"""
    prompt: str = Field(..., min_length=10, description="Product prompt description")
    context: Optional[str] = Field(None, description="Additional context")


# Intent Extraction Models
class ExtractedIntent(BaseModel):
    """Result of intent extraction"""
    app_type: str
    primary_purpose: str
    target_users: List[str]
    key_features: List[str]
    complexity_level: str  # low, medium, high


# System Design Models
class Role(BaseModel):
    """Role definition"""
    name: str
    description: str
    permissions: List[str]


class Entity(BaseModel):
    """Entity definition"""
    name: str
    attributes: Dict[str, str]
    relationships: List[str]


class SystemDesign(BaseModel):
    """System design layer output"""
    roles: List[Role]
    entities: List[Entity]
    workflows: List[Dict[str, Any]]
    assumptions: List[str]


# Schema Generation Models
class UISchema(BaseModel):
    """UI Schema definition"""
    pages: List[Dict[str, Any]] = Field(default_factory=list)
    components: List[Dict[str, Any]] = Field(default_factory=list)
    themes: Dict[str, Any] = Field(default_factory=dict)


class APISchema(BaseModel):
    """API Schema definition"""
    endpoints: List[Dict[str, Any]] = Field(default_factory=list)
    authentication: Dict[str, Any] = Field(default_factory=dict)
    rate_limiting: Dict[str, Any] = Field(default_factory=dict)


class DatabaseSchema(BaseModel):
    """Database Schema definition"""
    tables: List[Dict[str, Any]] = Field(default_factory=list)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    indexes: List[Dict[str, Any]] = Field(default_factory=list)


class SchemaGenerationOutput(BaseModel):
    """Output from schema generation stage"""
    ui_schema: UISchema
    api_schema: APISchema
    database_schema: DatabaseSchema


# Validation Models
class ValidationError(BaseModel):
    """Validation error details"""
    field: str
    error: str
    severity: str  # critical, warning, info


class ValidationResult(BaseModel):
    """Result of validation"""
    is_valid: bool
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# Repair Models
class RepairAction(BaseModel):
    """Action taken during repair"""
    field: str
    original_value: Any
    repaired_value: Any
    action: str


class RepairResult(BaseModel):
    """Result of repair engine"""
    was_repaired: bool
    actions: List[RepairAction] = Field(default_factory=list)
    repaired_config: Optional[Dict[str, Any]] = None


# Execution Simulation Models
class SimulationStep(BaseModel):
    """Single step in execution simulation"""
    step: int
    action: str
    expected_result: str
    status: str  # success, warning, error


class ExecutionSimulation(BaseModel):
    """Result of execution simulator"""
    total_steps: int
    steps: List[SimulationStep] = Field(default_factory=list)
    estimated_success_rate: float
    potential_issues: List[str] = Field(default_factory=list)


# Evaluation Models
class EvaluationMetric(BaseModel):
    """Single evaluation metric"""
    name: str
    score: float  # 0-100
    description: str
    recommendations: List[str] = Field(default_factory=list)


class EvaluationFramework(BaseModel):
    """Result of evaluation framework"""
    metrics: List[EvaluationMetric] = Field(default_factory=list)
    overall_score: float
    recommendations: List[str] = Field(default_factory=list)


# Auth & Business Logic Models
class AuthRule(BaseModel):
    """Authentication/Authorization rule"""
    role: str
    resource: str
    action: str
    allowed: bool


class BusinessLogic(BaseModel):
    """Business logic rules"""
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    triggers: List[Dict[str, Any]] = Field(default_factory=list)


# Final Output Model
class AIAppConfig(BaseModel):
    """Complete AI App Configuration"""
    app_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    assumptions: List[str]
    entities: List[Entity]
    roles: List[Role]
    permissions: Dict[str, List[str]] = Field(default_factory=dict)
    ui_schema: UISchema
    api_schema: APISchema
    database_schema: DatabaseSchema
    auth_rules: List[AuthRule] = Field(default_factory=list)
    business_logic: BusinessLogic
    validation_report: ValidationResult
    execution_simulation: ExecutionSimulation
    evaluation_framework: EvaluationFramework
    pipeline_metadata: Dict[str, Any] = Field(default_factory=dict)

    def json_schema(self) -> Dict[str, Any]:
        """Return JSON schema"""
        return self.model_json_schema()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump(by_alias=True)
