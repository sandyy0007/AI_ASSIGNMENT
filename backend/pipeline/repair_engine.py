"""
Stage 5: Repair Engine - Repair failed validations
"""
from typing import Dict, Any, List
from models import RepairResult, RepairAction


class RepairEngine:
    """Repair configuration failures"""

    def repair(self, config: Dict[str, Any], validation_errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Repair configuration based on validation errors"""
        try:
            if not validation_errors:
                return {
                    "success": True,
                    "was_repaired": False,
                    "data": {
                        "was_repaired": False,
                        "actions": [],
                        "repaired_config": config
                    }
                }

            repaired_config = config.copy()
            actions = []

            for error in validation_errors:
                if error.get("severity") == "critical":
                    action = self._repair_field(repaired_config, error)
                    if action:
                        actions.append(action)

            repair_result = RepairResult(
                was_repaired=len(actions) > 0,
                actions=actions,
                repaired_config=repaired_config if len(actions) > 0 else None
            )

            return {
                "success": True,
                "data": repair_result.model_dump(),
                "repairs_applied": len(actions)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _repair_field(self, config: Dict[str, Any], error: Dict[str, Any]) -> RepairAction or None:
        """Repair specific field"""
        field = error.get("field")
        error_msg = error.get("error")

        if field == "app_name":
            if not config.get("app_name"):
                config["app_name"] = "GeneratedApp"
                return RepairAction(
                    field=field,
                    original_value=None,
                    repaired_value="GeneratedApp",
                    action="generated_default_value"
                )

        elif field == "assumptions":
            if not config.get("assumptions"):
                config["assumptions"] = self._generate_default_assumptions()
                return RepairAction(
                    field=field,
                    original_value=[],
                    repaired_value=config["assumptions"],
                    action="generated_default_value"
                )

        elif field == "entities":
            if not config.get("entities"):
                config["entities"] = self._generate_default_entities()
                return RepairAction(
                    field=field,
                    original_value=[],
                    repaired_value=config["entities"],
                    action="generated_default_entities"
                )

        elif field == "roles":
            if not config.get("roles"):
                config["roles"] = self._generate_default_roles()
                return RepairAction(
                    field=field,
                    original_value=[],
                    repaired_value=config["roles"],
                    action="generated_default_roles"
                )

        elif field == "permissions":
            if not config.get("permissions"):
                config["permissions"] = self._generate_default_permissions(config.get("roles", []))
                return RepairAction(
                    field=field,
                    original_value={},
                    repaired_value=config["permissions"],
                    action="generated_default_permissions"
                )

        elif field == "ui_schema":
            if not config.get("ui_schema"):
                config["ui_schema"] = self._generate_default_ui_schema()
                return RepairAction(
                    field=field,
                    original_value=None,
                    repaired_value=config["ui_schema"],
                    action="generated_default_ui_schema"
                )

        elif field == "api_schema":
            if not config.get("api_schema"):
                config["api_schema"] = self._generate_default_api_schema()
                return RepairAction(
                    field=field,
                    original_value=None,
                    repaired_value=config["api_schema"],
                    action="generated_default_api_schema"
                )

        elif field == "database_schema":
            if not config.get("database_schema"):
                config["database_schema"] = self._generate_default_database_schema()
                return RepairAction(
                    field=field,
                    original_value=None,
                    repaired_value=config["database_schema"],
                    action="generated_default_database_schema"
                )

        return None

    def _generate_default_assumptions(self) -> List[str]:
        """Generate default assumptions"""
        return [
            "All users must authenticate before accessing protected resources",
            "API follows REST conventions",
            "All data is encrypted in transit",
            "Daily backups are performed",
            "Rate limiting is enforced on all endpoints"
        ]

    def _generate_default_entities(self) -> List[Dict[str, Any]]:
        """Generate default entities"""
        return [
            {
                "name": "user",
                "attributes": {"id": "UUID", "email": "string", "role": "enum"},
                "relationships": ["owns:content"]
            },
            {
                "name": "content",
                "attributes": {"id": "UUID", "title": "string", "owner_id": "UUID"},
                "relationships": ["owned_by:user"]
            }
        ]

    def _generate_default_roles(self) -> List[Dict[str, Any]]:
        """Generate default roles"""
        return [
            {"name": "admin", "description": "Administrator", "permissions": ["read:all", "write:all"]},
            {"name": "user", "description": "Regular user", "permissions": ["read:own", "write:own"]},
            {"name": "guest", "description": "Guest user", "permissions": ["read:public"]}
        ]

    def _generate_default_permissions(self, roles: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate default permissions"""
        permissions = {}
        for role in roles:
            permissions[role.get("name", "user")] = role.get("permissions", ["read:public"])
        return permissions

    def _generate_default_ui_schema(self) -> Dict[str, Any]:
        """Generate default UI schema"""
        return {
            "pages": [
                {"name": "dashboard", "route": "/", "components": ["header", "content"]},
                {"name": "profile", "route": "/profile", "components": ["profile_card"]}
            ],
            "components": []
        }

    def _generate_default_api_schema(self) -> Dict[str, Any]:
        """Generate default API schema"""
        return {
            "endpoints": [
                {"method": "GET", "path": "/api/health", "auth_required": False},
                {"method": "POST", "path": "/api/auth/login", "auth_required": False}
            ],
            "authentication": {"type": "JWT"}
        }

    def _generate_default_database_schema(self) -> Dict[str, Any]:
        """Generate default database schema"""
        return {
            "tables": [
                {"name": "users", "columns": [{"name": "id", "type": "UUID"}]},
                {"name": "content", "columns": [{"name": "id", "type": "UUID"}]}
            ],
            "relationships": []
        }
