"""
Stage 3: Schema Generation - Generate UI, API, and Database schemas
"""
from typing import Dict, Any, List
from models import UISchema, APISchema, DatabaseSchema, SchemaGenerationOutput


class SchemaGenerator:
    """Generate application schemas"""

    def generate(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Generate schemas from system design"""
        try:
            ui_schema = self._generate_ui_schema(design["data"])
            api_schema = self._generate_api_schema(design["data"])
            database_schema = self._generate_database_schema(design["data"])

            output = SchemaGenerationOutput(
                ui_schema=ui_schema,
                api_schema=api_schema,
                database_schema=database_schema
            )

            return {
                "success": True,
                "data": output.model_dump(),
                "endpoint_count": len(api_schema.endpoints),
                "table_count": len(database_schema.tables)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _generate_ui_schema(self, design: Dict[str, Any]) -> UISchema:
        """Generate UI schema"""
        pages = self._generate_pages(design)
        components = self._generate_components(design)
        themes = self._generate_themes()

        return UISchema(pages=pages, components=components, themes=themes)

    def _generate_pages(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate UI pages"""
        pages = [
            {
                "name": "login",
                "route": "/login",
                "components": ["form", "text_input", "password_input", "submit_button"],
                "accessibility": "public"
            },
            {
                "name": "dashboard",
                "route": "/dashboard",
                "components": ["header", "sidebar", "main_content", "footer"],
                "accessibility": "authenticated",
                "layout": "two_column"
            },
            {
                "name": "profile",
                "route": "/profile",
                "components": ["profile_card", "edit_form", "change_password"],
                "accessibility": "authenticated"
            }
        ]

        # Add entity-specific pages
        for entity in design.get("entities", []):
            pages.extend([
                {
                    "name": f"{entity['name']}_list",
                    "route": f"/{entity['name']}s",
                    "components": ["data_table", "filters", "pagination", "add_button"],
                    "accessibility": "authenticated"
                },
                {
                    "name": f"{entity['name']}_detail",
                    "route": f"/{entity['name']}/:id",
                    "components": ["detail_view", "edit_button", "delete_button"],
                    "accessibility": "authenticated"
                }
            ])

        return pages

    def _generate_components(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate UI components"""
        components = [
            {
                "name": "form",
                "type": "container",
                "properties": ["className", "onSubmit", "method"],
                "children": []
            },
            {
                "name": "text_input",
                "type": "input",
                "properties": ["type", "placeholder", "value", "onChange", "required"],
                "validation": "text"
            },
            {
                "name": "data_table",
                "type": "display",
                "properties": ["columns", "rows", "sortable", "filterable"],
                "features": ["pagination", "search", "export"]
            },
            {
                "name": "modal",
                "type": "overlay",
                "properties": ["isOpen", "onClose", "title", "size"],
                "children": []
            },
            {
                "name": "notification",
                "type": "feedback",
                "properties": ["type", "message", "duration", "position"],
                "types": ["success", "error", "warning", "info"]
            }
        ]

        return components

    def _generate_themes(self) -> Dict[str, Any]:
        """Generate theme configuration"""
        return {
            "name": "dark_developer",
            "colors": {
                "primary": "#007AFF",
                "secondary": "#5AC8FA",
                "background": "#0F1419",
                "surface": "#1A1F2E",
                "text": "#E8EAED",
                "text_secondary": "#9AA0A6",
                "error": "#FF453A",
                "success": "#34C759",
                "warning": "#FF9500"
            },
            "typography": {
                "font_family": "'Fira Code', 'Monaco', monospace",
                "sizes": {"sm": "12px", "md": "14px", "lg": "16px", "xl": "20px"}
            },
            "spacing": {
                "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"
            },
            "shadows": {
                "sm": "0 1px 2px rgba(0,0,0,0.3)",
                "md": "0 4px 12px rgba(0,0,0,0.4)",
                "lg": "0 8px 24px rgba(0,0,0,0.5)"
            }
        }

    def _generate_api_schema(self, design: Dict[str, Any]) -> APISchema:
        """Generate API schema"""
        endpoints = self._generate_endpoints(design)
        authentication = self._generate_auth_config()
        rate_limiting = self._generate_rate_limiting()

        return APISchema(endpoints=endpoints, authentication=authentication, rate_limiting=rate_limiting)

    def _generate_endpoints(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate API endpoints"""
        endpoints = [
            {
                "method": "POST",
                "path": "/api/auth/login",
                "description": "User login",
                "request": {"email": "string", "password": "string"},
                "response": {"token": "string", "user": "object"},
                "auth_required": False
            },
            {
                "method": "POST",
                "path": "/api/auth/logout",
                "description": "User logout",
                "auth_required": True
            },
            {
                "method": "GET",
                "path": "/api/user/profile",
                "description": "Get current user profile",
                "response": {"user": "object"},
                "auth_required": True
            }
        ]

        # Add entity endpoints
        for entity in design.get("entities", []):
            entity_name = entity["name"]
            endpoints.extend([
                {
                    "method": "GET",
                    "path": f"/api/{entity_name}s",
                    "description": f"List all {entity_name}s",
                    "response": f"[{entity_name}]",
                    "auth_required": True,
                    "pagination": True
                },
                {
                    "method": "POST",
                    "path": f"/api/{entity_name}s",
                    "description": f"Create new {entity_name}",
                    "request": entity.get("attributes", {}),
                    "auth_required": True
                },
                {
                    "method": "GET",
                    "path": f"/api/{entity_name}s/:id",
                    "description": f"Get {entity_name} by ID",
                    "auth_required": True
                },
                {
                    "method": "PUT",
                    "path": f"/api/{entity_name}s/:id",
                    "description": f"Update {entity_name}",
                    "auth_required": True
                },
                {
                    "method": "DELETE",
                    "path": f"/api/{entity_name}s/:id",
                    "description": f"Delete {entity_name}",
                    "auth_required": True
                }
            ])

        return endpoints

    def _generate_auth_config(self) -> Dict[str, Any]:
        """Generate authentication configuration"""
        return {
            "type": "JWT",
            "token_expiry": "24h",
            "refresh_token_expiry": "30d",
            "algorithm": "HS256",
            "issuer": "ai_app_config_compiler",
            "audiences": ["api", "web"]
        }

    def _generate_rate_limiting(self) -> Dict[str, Any]:
        """Generate rate limiting configuration"""
        return {
            "enabled": True,
            "default_limit": "1000/hour",
            "endpoints": {
                "auth": "100/hour",
                "api": "1000/hour",
                "file_upload": "50/hour"
            }
        }

    def _generate_database_schema(self, design: Dict[str, Any]) -> DatabaseSchema:
        """Generate database schema"""
        tables = self._generate_tables(design)
        relationships = self._generate_relationships(design)
        indexes = self._generate_indexes(tables)

        return DatabaseSchema(tables=tables, relationships=relationships, indexes=indexes)

    def _generate_tables(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate database tables"""
        tables = [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "email", "type": "VARCHAR", "unique": True, "not_null": True},
                    {"name": "password_hash", "type": "VARCHAR", "not_null": True},
                    {"name": "role", "type": "ENUM", "default": "user"},
                    {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
                    {"name": "updated_at", "type": "TIMESTAMP"}
                ]
            },
            {
                "name": "sessions",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "user_id", "type": "UUID", "foreign_key": "users.id"},
                    {"name": "token", "type": "VARCHAR", "unique": True},
                    {"name": "expires_at", "type": "TIMESTAMP"},
                    {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
                ]
            }
        ]

        # Add entity tables
        for entity in design.get("entities", []):
            table = {
                "name": entity["name"] + "s",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    *[
                        {"name": k, "type": "VARCHAR" if v == "string" else v.upper()}
                        for k, v in entity.get("attributes", {}).items()
                        if k != "id"
                    ]
                ]
            }
            tables.append(table)

        return tables

    def _generate_relationships(self, design: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate table relationships"""
        relationships = [
            {
                "from_table": "sessions",
                "to_table": "users",
                "relationship_type": "foreign_key",
                "from_column": "user_id",
                "to_column": "id"
            }
        ]

        # Add entity relationships
        for entity in design.get("entities", []):
            for relationship in entity.get("relationships", []):
                relationships.append({
                    "from_table": entity["name"] + "s",
                    "description": relationship,
                    "relationship_type": "foreign_key"
                })

        return relationships

    def _generate_indexes(self, tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate database indexes"""
        indexes = []

        for table in tables:
            # Index on id (primary key)
            indexes.append({
                "table": table["name"],
                "column": "id",
                "type": "PRIMARY",
                "unique": True
            })

            # Index on common filter columns
            for column in table.get("columns", []):
                if column.get("unique"):
                    indexes.append({
                        "table": table["name"],
                        "column": column["name"],
                        "type": "UNIQUE"
                    })

        return indexes
