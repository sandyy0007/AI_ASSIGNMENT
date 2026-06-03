"""
Stage 2: System Design Layer - Design system architecture based on intent
"""
from typing import Dict, Any, List
from models import SystemDesign, Role, Entity


class SystemDesigner:
    """Design system architecture"""

    def design(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Design system from intent"""
        try:
            roles = self._create_roles(intent["data"]["app_type"], intent["data"]["target_users"])
            entities = self._create_entities(intent["data"]["app_type"], intent["data"]["key_features"])
            workflows = self._design_workflows(roles, entities, intent["data"]["app_type"])
            assumptions = self._generate_assumptions(intent["data"])

            design = SystemDesign(
                roles=roles,
                entities=entities,
                workflows=workflows,
                assumptions=assumptions
            )

            return {
                "success": True,
                "data": design.model_dump(),
                "entity_count": len(entities),
                "role_count": len(roles)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _create_roles(self, app_type: str, target_users: List[str]) -> List[Role]:
        """Create system roles"""
        base_roles = [
            Role(
                name="admin",
                description="System administrator with full permissions",
                permissions=["read:all", "write:all", "delete:all", "manage:users"]
            ),
            Role(
                name="user",
                description="Regular user with standard permissions",
                permissions=["read:own", "write:own", "read:public"]
            ),
            Role(
                name="guest",
                description="Guest user with limited permissions",
                permissions=["read:public"]
            )
        ]

        # Add app-specific roles
        app_roles = self._get_app_specific_roles(app_type)
        return base_roles + app_roles

    def _get_app_specific_roles(self, app_type: str) -> List[Role]:
        """Get app-specific roles"""
        role_map = {
            "e-commerce": [
                Role(name="seller", description="Product seller", permissions=["write:products", "read:orders"]),
                Role(name="buyer", description="Product buyer", permissions=["read:products", "write:cart"])
            ],
            "social": [
                Role(name="moderator", description="Content moderator", permissions=["delete:content", "manage:users"]),
                Role(name="influencer", description="Content creator", permissions=["write:content", "analytics:own"])
            ],
            "crm": [
                Role(name="sales", description="Sales team member", permissions=["read:leads", "write:deals"]),
                Role(name="manager", description="Sales manager", permissions=["read:team", "manage:team"])
            ],
            "project": [
                Role(name="team_lead", description="Team lead", permissions=["write:project", "manage:team"]),
                Role(name="contributor", description="Project contributor", permissions=["write:tasks", "read:project"])
            ],
        }
        return role_map.get(app_type, [])

    def _create_entities(self, app_type: str, features: List[str]) -> List[Entity]:
        """Create system entities"""
        base_entities = [
            Entity(
                name="user",
                attributes={"id": "UUID", "email": "string", "name": "string", "role": "enum", "created_at": "datetime"},
                relationships=["owns:content", "has:permissions"]
            ),
            Entity(
                name="session",
                attributes={"id": "UUID", "user_id": "UUID", "token": "string", "expires_at": "datetime"},
                relationships=["belongs_to:user"]
            )
        ]

        # Add app-specific entities
        app_entities = self._get_app_specific_entities(app_type, features)
        return base_entities + app_entities

    def _get_app_specific_entities(self, app_type: str, features: List[str]) -> List[Entity]:
        """Get app-specific entities"""
        entity_map = {
            "e-commerce": [
                Entity(
                    name="product",
                    attributes={"id": "UUID", "name": "string", "price": "float", "stock": "int", "seller_id": "UUID"},
                    relationships=["created_by:user", "in:category", "has:reviews"]
                ),
                Entity(
                    name="order",
                    attributes={"id": "UUID", "user_id": "UUID", "total": "float", "status": "enum", "created_at": "datetime"},
                    relationships=["belongs_to:user", "contains:product"]
                )
            ],
            "social": [
                Entity(
                    name="post",
                    attributes={"id": "UUID", "user_id": "UUID", "content": "text", "likes": "int", "created_at": "datetime"},
                    relationships=["created_by:user", "has:comments"]
                ),
                Entity(
                    name="comment",
                    attributes={"id": "UUID", "post_id": "UUID", "user_id": "UUID", "content": "text", "created_at": "datetime"},
                    relationships=["belongs_to:post", "created_by:user"]
                )
            ],
            "project": [
                Entity(
                    name="project",
                    attributes={"id": "UUID", "name": "string", "owner_id": "UUID", "status": "enum", "created_at": "datetime"},
                    relationships=["owned_by:user", "has:tasks", "has:members"]
                ),
                Entity(
                    name="task",
                    attributes={"id": "UUID", "project_id": "UUID", "assignee_id": "UUID", "status": "enum", "due_date": "date"},
                    relationships=["belongs_to:project", "assigned_to:user"]
                )
            ]
        }
        return entity_map.get(app_type, [])

    def _design_workflows(self, roles: List[Role], entities: List[Entity], app_type: str) -> List[Dict[str, Any]]:
        """Design system workflows"""
        workflows = [
            {
                "name": "authentication_flow",
                "steps": ["input_credentials", "validate_credentials", "create_session", "issue_token"],
                "actors": ["guest", "user"],
                "entities_involved": ["user", "session"]
            },
            {
                "name": "authorization_flow",
                "steps": ["receive_request", "validate_token", "check_permissions", "execute_or_deny"],
                "actors": ["system"],
                "entities_involved": ["user", "session"]
            }
        ]

        # Add app-specific workflows
        app_workflows = self._get_app_specific_workflows(app_type)
        return workflows + app_workflows

    def _get_app_specific_workflows(self, app_type: str) -> List[Dict[str, Any]]:
        """Get app-specific workflows"""
        workflow_map = {
            "e-commerce": [
                {
                    "name": "product_purchase",
                    "steps": ["browse_products", "add_to_cart", "checkout", "payment", "order_confirmation"],
                    "actors": ["buyer"],
                    "entities_involved": ["product", "order", "user"]
                }
            ],
            "social": [
                {
                    "name": "post_creation",
                    "steps": ["write_content", "add_media", "set_privacy", "publish", "notify_followers"],
                    "actors": ["user"],
                    "entities_involved": ["post", "user"]
                }
            ],
            "project": [
                {
                    "name": "task_management",
                    "steps": ["create_task", "assign_task", "update_status", "complete_task"],
                    "actors": ["team_lead", "contributor"],
                    "entities_involved": ["project", "task", "user"]
                }
            ]
        }
        return workflow_map.get(app_type, [])

    def _generate_assumptions(self, intent_data: Dict[str, Any]) -> List[str]:
        """Generate system assumptions"""
        assumptions = [
            "All users must authenticate before accessing protected resources",
            "The system will be deployed on cloud infrastructure",
            "SSL/TLS encryption is used for all data in transit",
            "Database backups are performed daily",
            "API responses follow REST conventions",
            "Rate limiting is implemented for all endpoints"
        ]

        # Add context-specific assumptions
        if "real-time" in str(intent_data.get("key_features", [])).lower():
            assumptions.append("WebSocket connections are maintained for real-time updates")

        if "mobile" in str(intent_data.get("key_features", [])).lower():
            assumptions.append("Mobile clients use offline-first synchronization strategy")

        return assumptions
