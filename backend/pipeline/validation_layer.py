"""
Stage 4: Validation Layer - Validate generated configuration
"""
from typing import Dict, Any, List
from models import ValidationResult, ValidationError


class ValidationLayer:
    """Validate application configuration"""

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration"""
        try:
            errors = []
            warnings = []

            schema_errors = self._validate_schema(config)
            errors.extend(schema_errors)

            consistency_warnings = self._validate_consistency(config)
            warnings.extend(consistency_warnings)

            completeness_errors = self._validate_completeness(config)
            errors.extend(completeness_errors)

            logic_warnings = self._validate_business_logic(config)
            warnings.extend(logic_warnings)

            is_valid = len([e for e in errors if e["severity"] == "critical"]) == 0

            validation_result = ValidationResult(
                is_valid=is_valid,
                errors=[ValidationError(**e) for e in errors],
                warnings=warnings
            )

            return {
                "success": True,
                "data": validation_result.model_dump(),
                "error_count": len(errors),
                "warning_count": len(warnings)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _validate_schema(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate required schema fields"""
        errors = []

        required_fields = [
            "assumptions",
            "entities",
            "roles",
            "ui_schema",
            "api_schema",
            "database_schema"
        ]

        for field in required_fields:
            if field not in config:
                errors.append({
                    "field": field,
                    "error": f"Required field '{field}' is missing",
                    "severity": "critical"
                })

        if "app_name" in config and config["app_name"]:
            if not isinstance(config["app_name"], str):
                errors.append({
                    "field": "app_name",
                    "error": "app_name must be a string",
                    "severity": "critical"
                })

        return errors

    def _validate_consistency(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration consistency"""
        warnings = []

        roles = {r.get("name") for r in config.get("roles", []) if isinstance(r, dict)}
        permissions = config.get("permissions", {})

        if isinstance(permissions, dict):
            for role_name in permissions:
                if role_name not in roles and role_name != "default":
                    warnings.append(f"Role '{role_name}' in permissions not defined in roles list")

        return warnings

    def _validate_completeness(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate completeness"""
        errors = []

        entities = config.get("entities", [])
        if len(entities) < 1:
            errors.append({
                "field": "entities",
                "error": "Configuration should have at least 1 entity",
                "severity": "warning"
            })

        roles = config.get("roles", [])
        if len(roles) < 1:
            errors.append({
                "field": "roles",
                "error": "Configuration should have at least 1 role",
                "severity": "warning"
            })

        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        if len(api_endpoints) < 1:
            errors.append({
                "field": "api_schema.endpoints",
                "error": "Configuration should have API endpoints",
                "severity": "warning"
            })

        db_tables = config.get("database_schema", {}).get("tables", [])
        if len(db_tables) < 1:
            errors.append({
                "field": "database_schema.tables",
                "error": "Configuration should have database tables",
                "severity": "warning"
            })

        return errors

    def _validate_business_logic(self, config: Dict[str, Any]) -> List[str]:
        """Validate business logic warnings only"""
        warnings = []

        auth_rules = config.get("auth_rules", [])
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])

        protected_endpoints = [e for e in api_endpoints if e.get("auth_required")]

        if len(protected_endpoints) > 0 and len(auth_rules) == 0:
            warnings.append("API has protected endpoints but no auth rules defined")

        db_schema = config.get("database_schema", {})
        tables = db_schema.get("tables", [])
        relationships = db_schema.get("relationships", [])

        if len(tables) > 0 and len(relationships) == 0:
            warnings.append("Database tables defined but no relationships specified")

        return warning
