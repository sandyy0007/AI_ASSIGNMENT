"""
Stage 1: Intent Extraction - Extract user intent from prompt
"""
import re
from typing import Dict, Any
from models import ExtractedIntent


class IntentExtractor:
    """Extract intent from user prompt"""

    def extract(self, prompt: str) -> Dict[str, Any]:
        """Extract intent from prompt"""
        try:
            # Analyze prompt to determine app type
            app_type = self._determine_app_type(prompt)
            primary_purpose = self._extract_primary_purpose(prompt)
            target_users = self._extract_target_users(prompt)
            key_features = self._extract_key_features(prompt)
            complexity_level = self._assess_complexity(prompt)

            intent = ExtractedIntent(
                app_type=app_type,
                primary_purpose=primary_purpose,
                target_users=target_users,
                key_features=key_features,
                complexity_level=complexity_level
            )

            return {
                "success": True,
                "data": intent.model_dump(),
                "confidence": self._calculate_confidence(prompt, intent)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def _determine_app_type(self, prompt: str) -> str:
        """Determine application type"""
        prompt_lower = prompt.lower()

        type_keywords = {
            "e-commerce": ["shop", "store", "buy", "sell", "product", "cart", "checkout"],
            "social": ["social", "community", "chat", "message", "follow", "friend", "network"],
            "crm": ["customer", "client", "manage", "sales", "lead", "opportunity"],
            "analytics": ["analytics", "dashboard", "report", "metric", "data", "analysis"],
            "project": ["project", "task", "workflow", "collaboration", "team", "sprint"],
            "content": ["content", "publish", "blog", "article", "media", "cms"],
            "marketplace": ["marketplace", "vendor", "listing", "auction", "bidding"],
            "productivity": ["todo", "note", "calendar", "schedule", "reminder", "productivity"],
            "education": ["learn", "course", "student", "teacher", "quiz", "education"],
            "healthcare": ["patient", "doctor", "appointment", "medical", "health", "clinic"]
        }

        scores = {}
        for app_type, keywords in type_keywords.items():
            scores[app_type] = sum(1 for kw in keywords if kw in prompt_lower)

        return max(scores, key=scores.get) if max(scores.values()) > 0 else "web_application"

    def _extract_primary_purpose(self, prompt: str) -> str:
        """Extract primary purpose"""
        sentences = prompt.split(".")
        return sentences[0].strip() if sentences else prompt

    def _extract_target_users(self, prompt: str) -> list:
        """Extract target users"""
        users = []
        prompt_lower = prompt.lower()

        user_keywords = {
            "businesses": ["business", "company", "enterprise", "organization"],
            "consumers": ["user", "consumer", "customer", "people", "individual"],
            "developers": ["developer", "programmer", "engineer", "api"],
            "admin": ["admin", "administrator", "manager", "staff"],
            "analyst": ["analyst", "analyst", "researcher", "scientist"]
        }

        for user_type, keywords in user_keywords.items():
            if any(kw in prompt_lower for kw in keywords):
                users.append(user_type)

        return users if users else ["users"]

    def _extract_key_features(self, prompt: str) -> list:
        """Extract key features"""
        features = []
        prompt_lower = prompt.lower()

        feature_patterns = {
            "Authentication": ["login", "auth", "signin", "signup", "password"],
            "User Management": ["user", "profile", "account", "manage user"],
            "Search": ["search", "find", "query", "filter"],
            "Notifications": ["notify", "alert", "notification", "message"],
            "Analytics": ["analytics", "report", "metric", "dashboard"],
            "Export": ["export", "download", "csv", "pdf"],
            "Real-time": ["real-time", "live", "instant", "websocket"],
            "Integration": ["integrate", "connect", "api", "sync"],
            "Payment": ["payment", "checkout", "purchase", "billing"],
            "Mobile": ["mobile", "app", "responsive", "ios", "android"]
        }

        for feature, keywords in feature_patterns.items():
            if any(kw in prompt_lower for kw in keywords):
                features.append(feature)

        return features if features else ["Core Features"]

    def _assess_complexity(self, prompt: str) -> str:
        """Assess complexity level"""
        complexity_indicators = {
            "high": ["integrate", "real-time", "algorithm", "ml", "ai", "complex", "advanced"],
            "medium": ["multi-user", "database", "api", "third-party"],
            "low": ["simple", "basic", "static", "single-user"]
        }

        prompt_lower = prompt.lower()

        for level, keywords in complexity_indicators.items():
            if any(kw in prompt_lower for kw in keywords):
                return level

        # Default complexity based on prompt length
        word_count = len(prompt.split())
        if word_count > 200:
            return "high"
        elif word_count > 100:
            return "medium"
        return "low"

    def _calculate_confidence(self, prompt: str, intent: ExtractedIntent) -> float:
        """Calculate extraction confidence"""
        confidence = 0.5

        # Increase confidence based on prompt quality
        if len(prompt) > 100:
            confidence += 0.2
        if len(intent.key_features) >= 3:
            confidence += 0.15
        if len(intent.target_users) >= 2:
            confidence += 0.15

        return min(1.0, confidence)
