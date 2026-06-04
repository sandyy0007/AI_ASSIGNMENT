"""
Stage 4: Validation Layer - Validate generated configuration
"""
from typing import Dict, Any, List


class ValidationLayer:
    """Validate application configuration"""

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration safely and always return valid data."""
        errors: List[Dict[str, Any]] = []
        warnings: List[str] = []

        required_fields = [
            "assumptions",
            "entities",
            "roles",
            "ui_schema",
            "api_schema",
            "database_schema"
        ]

        for field in required_fields:
            if field not in config or config.get(field) in [None, "", [], {}]:
                errors.append({
                    "field": field,
                    "error": f"Required field '{field}' is missing",
                    "severity": "critical"
                })

        if not config.get("app_name"):
            warnings.append("app_name missing, default app name will be used")

        if not config.get("permissions"):
            warnings.append("permissions missing, repair engine can generate default permissions")

        if not config.get("auth_rules"):
            warnings.append("auth_rules missing, repair engine can generate default auth rules")

        ui_pages = config.get("ui_schema", {}).get("pages", [])
        if len(ui_pages) == 0:
            warnings.append("UI schema has no pages")

        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        if len(api_endpoints) == 0:
            warnings.append("API schema has no endpoints")

        db_tables = config.get("database_schema", {}).get("tables", [])
        if len(db_tables) == 0:
            warnings.append("Database schema has no tables")

        is_valid = len(errors) == 0

        return {
            "success": True,
            "data": {
                "is_valid": is_valid,
                "errors": errors,
                "warnings": warnings
            },
            "error_count": len(errors),
            "warning_count": len(warnings)
        }
