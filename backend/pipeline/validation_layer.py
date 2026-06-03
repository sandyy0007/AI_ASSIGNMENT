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

            # Validate schema
            schema_errors = self._validate_schema(config)
            errors.extend(schema_errors)

            # Validate consistency
            consistency_warnings = self._validate_consistency(config)
            warnings.extend(consistency_warnings)

            # Validate completeness
            completeness_errors = self._validate_completeness(config)
            errors.extend(completeness_errors)

            # Validate business logic
            logic_errors = self._validate_business_logic(config)
            errors.extend(logic_errors)

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
        """Validate schema structure"""
        errors = []
        required_fields = [
            "app_name", "assumptions", "entities", "roles", "permissions",
            "ui_schema", "api_schema", "database_schema"
        ]

        for field in required_fields:
            if field not in config:
                errors.append({
                    "field": field,
                    "error": f"Required field '{field}' is missing",
                    "severity": "critical"
                })

        # Validate app_name
        if "app_name" in config:
            if not isinstance(config["app_name"], str) or len(config["app_name"]) == 0:
                errors.append({
                    "field": "app_name",
                    "error": "app_name must be a non-empty string",
                    "severity": "critical"
                })

        return errors

    def _validate_consistency(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration consistency"""
        warnings = []

        # Check if roles and entities match in permissions
        roles = {r["name"] for r in config.get("roles", [])}
        permissions = config.get("permissions", {})

        for role_name in permissions:
            if role_name not in roles and role_name != "default":
                warnings.append(f"Role '{role_name}' in permissions not defined in roles list")

        # Check if API endpoints match entities
        entities = {e["name"] for e in config.get("entities", [])}
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])

        for endpoint in api_endpoints:
            path = endpoint.get("path", "")
            # Simple check: if endpoint path contains an entity name
            for entity in entities:
                if entity in path.lower() and "auth" not in path:
                    break

        return warnings

    def _validate_completeness(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate completeness of configuration"""
        errors = []

        # Check minimum entities
        entities = config.get("entities", [])
        if len(entities) < 2:
            errors.append({
                "field": "entities",
                "error": "Configuration should have at least 2 entities",
                "severity": "warning"
            })

        # Check minimum roles
        roles = config.get("roles", [])
        if len(roles) < 2:
            errors.append({
                "field": "roles",
                "error": "Configuration should have at least 2 roles",
                "severity": "warning"
            })

        # Check API endpoints
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        if len(api_endpoints) < 5:
            errors.append({
                "field": "api_schema.endpoints",
                "error": "Configuration should have at least 5 API endpoints",
                "severity": "warning"
            })

        # Check database tables
        db_tables = config.get("database_schema", {}).get("tables", [])
        if len(db_tables) < 3:
            errors.append({
                "field": "database_schema.tables",
                "error": "Configuration should have at least 3 database tables",
                "severity": "warning"
            })

        return errors

    def _validate_business_logic(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate business logic"""
        errors = []

        # Check for authentication configuration
        auth_rules = config.get("auth_rules", [])
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])

        protected_endpoints = [e for e in api_endpoints if e.get("auth_required")]
        if len(protected_endpoints) > 0 and len(auth_rules) == 0:
            errors.append({
                "field": "auth_rules",
                "error": "API has protected endpoints but no auth rules defined",
                "severity": "warning"
            })

        # Check for database constraints
        db_schema = config.get("database_schema", {})
        tables = db_schema.get("tables", [])
        relationships = db_schema.get("relationships", [])

        if len(tables) > 0 and len(relationships) == 0:
            errors.append({
                "field": "database_schema.relationships",
                "error": "Database tables defined but no relationships specified",
                "severity": "info"
            })

        return errors
