"""
Stage 7: Evaluation Framework - Evaluate generated configuration
"""
from typing import Dict, Any, List
from models import EvaluationFramework, EvaluationMetric


class EvaluationFramework:
    """Evaluate application configuration quality"""

    def evaluate(self, config: Dict[str, Any], validation_result: Dict[str, Any],
                simulation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate configuration"""
        try:
            metrics = []

            # Evaluate completeness
            completeness_score = self._evaluate_completeness(config)
            metrics.append(EvaluationMetric(
                name="completeness",
                score=completeness_score,
                description="Configuration has all required components",
                recommendations=self._get_completeness_recommendations(completeness_score)
            ))

            # Evaluate consistency
            consistency_score = self._evaluate_consistency(config)
            metrics.append(EvaluationMetric(
                name="consistency",
                score=consistency_score,
                description="Configuration components are consistent",
                recommendations=self._get_consistency_recommendations(consistency_score)
            ))

            # Evaluate security
            security_score = self._evaluate_security(config)
            metrics.append(EvaluationMetric(
                name="security",
                score=security_score,
                description="Configuration follows security best practices",
                recommendations=self._get_security_recommendations(security_score)
            ))

            # Evaluate scalability
            scalability_score = self._evaluate_scalability(config)
            metrics.append(EvaluationMetric(
                name="scalability",
                score=scalability_score,
                description="Configuration supports scalability",
                recommendations=self._get_scalability_recommendations(scalability_score)
            ))

            # Evaluate maintainability
            maintainability_score = self._evaluate_maintainability(config)
            metrics.append(EvaluationMetric(
                name="maintainability",
                score=maintainability_score,
                description="Configuration is maintainable and well-documented",
                recommendations=self._get_maintainability_recommendations(maintainability_score)
            ))

            # Evaluate validation success
            validation_score = self._evaluate_validation(validation_result)
            metrics.append(EvaluationMetric(
                name="validation_success",
                score=validation_score,
                description="Configuration passed validation checks",
                recommendations=[]
            ))

            # Evaluate execution readiness
            execution_score = self._evaluate_execution(simulation_result)
            metrics.append(EvaluationMetric(
                name="execution_readiness",
                score=execution_score,
                description="Configuration is ready for execution",
                recommendations=[]
            ))

            # Calculate overall score
            overall_score = sum(m.score for m in metrics) / len(metrics)

            # Generate overall recommendations
            recommendations = self._generate_overall_recommendations(metrics)

            evaluation = EvaluationFramework(
                metrics=metrics,
                overall_score=overall_score,
                recommendations=recommendations
            )

            return {
                "success": True,
                "data": evaluation.model_dump(),
                "overall_score": overall_score,
                "metric_count": len(metrics)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _evaluate_completeness(self, config: Dict[str, Any]) -> float:
        """Evaluate completeness"""
        score = 0.0
        required_fields = [
            "app_name", "assumptions", "entities", "roles", "permissions",
            "ui_schema", "api_schema", "database_schema", "auth_rules", "business_logic"
        ]

        present_fields = sum(1 for field in required_fields if field in config and config[field])
        score = (present_fields / len(required_fields)) * 100

        # Bonus for having additional fields
        if "validation_report" in config:
            score += 5
        if "execution_simulation" in config:
            score += 5

        return min(100, score)

    def _evaluate_consistency(self, config: Dict[str, Any]) -> float:
        """Evaluate consistency"""
        score = 50.0

        # Check role consistency
        roles = {r.get("name") for r in config.get("roles", [])}
        permissions = config.get("permissions", {})
        role_consistency = len([r for r in permissions if r in roles]) / max(len(permissions), 1)
        score += role_consistency * 20

        # Check entity consistency
        entities = {e.get("name") for e in config.get("entities", [])}
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        entity_mentions = sum(1 for e in api_endpoints for ent in entities if ent in e.get("path", ""))
        score += min(20, (entity_mentions / max(len(api_endpoints), 1)) * 20)

        # Check database-entity consistency
        db_tables = {t.get("name") for t in config.get("database_schema", {}).get("tables", [])}
        entity_coverage = len([ent for ent in entities if any(ent.lower() in t.lower() for t in db_tables)])
        score += (entity_coverage / max(len(entities), 1)) * 10

        return min(100, score)

    def _evaluate_security(self, config: Dict[str, Any]) -> float:
        """Evaluate security"""
        score = 0.0

        # Check for authentication
        if config.get("auth_rules"):
            score += 25
        if config.get("api_schema", {}).get("authentication"):
            score += 25

        # Check for authorization
        if config.get("roles") and len(config.get("roles", [])) >= 2:
            score += 25

        # Check for permissions
        if config.get("permissions"):
            score += 25

        return score

    def _evaluate_scalability(self, config: Dict[str, Any]) -> float:
        """Evaluate scalability"""
        score = 0.0

        # Check for stateless design (good for scaling)
        if config.get("api_schema", {}).get("authentication", {}).get("type") == "JWT":
            score += 25

        # Check for database design
        tables = config.get("database_schema", {}).get("tables", [])
        if len(tables) >= 3:
            score += 20
        if config.get("database_schema", {}).get("indexes"):
            score += 20

        # Check for horizontal scaling capability
        if config.get("assumptions"):
            assumptions_text = str(config.get("assumptions", "")).lower()
            if "load" in assumptions_text or "scale" in assumptions_text or "distributed" in assumptions_text:
                score += 15

        # Check for API pagination
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        paginated_endpoints = sum(1 for e in api_endpoints if e.get("pagination"))
        if paginated_endpoints > 0:
            score += 20

        return min(100, score)

    def _evaluate_maintainability(self, config: Dict[str, Any]) -> float:
        """Evaluate maintainability"""
        score = 0.0

        # Check for documentation (assumptions, descriptions)
        if config.get("assumptions") and len(config.get("assumptions", [])) >= 3:
            score += 25

        # Check for clear role/permission structure
        if config.get("roles") and config.get("permissions"):
            score += 25

        # Check for consistent naming patterns
        entities = {e.get("name", "").lower() for e in config.get("entities", [])}
        api_endpoints = config.get("api_schema", {}).get("endpoints", [])
        consistent_naming = sum(1 for e in api_endpoints for ent in entities
                               if ent in e.get("path", "").lower())
        if consistent_naming > 0:
            score += 25

        # Check for proper separation of concerns
        if (config.get("ui_schema") and config.get("api_schema") and
            config.get("database_schema")):
            score += 25

        return min(100, score)

    def _evaluate_validation(self, validation_result: Dict[str, Any]) -> float:
        """Evaluate validation success"""
        if not validation_result:
            return 50.0

        if validation_result.get("data", {}).get("is_valid"):
            return 100.0
        else:
            error_count = len(validation_result.get("data", {}).get("errors", []))
            return max(0, 100 - (error_count * 10))

    def _evaluate_execution(self, simulation_result: Dict[str, Any]) -> float:
        """Evaluate execution readiness"""
        if not simulation_result:
            return 50.0

        success_rate = simulation_result.get("data", {}).get("estimated_success_rate", 0.5)
        return success_rate * 100

    def _get_completeness_recommendations(self, score: float) -> List[str]:
        """Get completeness recommendations"""
        if score >= 90:
            return ["Configuration is complete"]
        elif score >= 70:
            return ["Add more business logic rules", "Define additional auth rules"]
        else:
            return ["Missing critical components", "Add assumptions and constraints"]

    def _get_consistency_recommendations(self, score: float) -> List[str]:
        """Get consistency recommendations"""
        if score >= 85:
            return ["Configuration is consistent"]
        else:
            return ["Ensure all entities have corresponding API endpoints",
                   "Verify role-permission mappings"]

    def _get_security_recommendations(self, score: float) -> List[str]:
        """Get security recommendations"""
        if score >= 90:
            return ["Security configuration looks good"]
        elif score >= 50:
            return ["Implement role-based access control", "Add rate limiting"]
        else:
            return ["Add authentication mechanism", "Define authorization rules"]

    def _get_scalability_recommendations(self, score: float) -> List[str]:
        """Get scalability recommendations"""
        if score >= 80:
            return ["Good scalability design"]
        else:
            return ["Consider using JWT for stateless auth",
                   "Add database indexing strategy",
                   "Implement API pagination"]

    def _get_maintainability_recommendations(self, score: float) -> List[str]:
        """Get maintainability recommendations"""
        if score >= 85:
            return ["Configuration is well-maintainable"]
        else:
            return ["Add more documentation",
                   "Use consistent naming conventions",
                   "Document assumptions clearly"]

    def _generate_overall_recommendations(self, metrics: List[EvaluationMetric]) -> List[str]:
        """Generate overall recommendations"""
        recommendations = []

        # Find lowest scoring metrics
        sorted_metrics = sorted(metrics, key=lambda m: m.score)
        for metric in sorted_metrics[:2]:
            recommendations.extend(metric.recommendations)

        if not recommendations:
            recommendations = ["Configuration meets quality standards"]

        return recommendations[:5]
