"""
Authentication and security module for Telegram Claude Bot
"""

import time
import re
from typing import Optional, Dict
from telegram import Update
from config import config
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiting to prevent abuse"""

    def __init__(self, max_per_minute: int = 10):
        self.max_per_minute = max_per_minute
        self.user_requests: Dict[int, list] = {}

    def is_allowed(self, user_id: int) -> bool:
        """Check if user is within rate limit"""
        now = time.time()

        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        # Clean old requests (older than 1 minute)
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id]
            if now - t < 60
        ]

        # Check if limit exceeded
        if len(self.user_requests[user_id]) >= self.max_per_minute:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False

        # Add current request
        self.user_requests[user_id].append(now)
        return True

    def reset_user(self, user_id: int):
        """Reset rate limit for a user"""
        if user_id in self.user_requests:
            del self.user_requests[user_id]


class Auth:
    """Authentication handler"""

    def __init__(self):
        self.allowed_users = set(config.ALLOWED_USERS)
        self.rate_limiter = RateLimiter(config.MAX_REQUESTS_PER_MINUTE)

    def is_authorized(self, update: Update) -> bool:
        """Check if user is authorized to use the bot"""
        user_id = update.effective_user.id

        # If no allowed users configured, allow everyone (warning shown in config)
        if not self.allowed_users:
            return True

        if user_id not in self.allowed_users:
            logger.warning(f"Unauthorized access attempt from user {user_id}")
            return False

        return True

    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limit"""
        return self.rate_limiter.is_allowed(user_id)

    def add_user(self, user_id: int):
        """Add user to allowed list"""
        self.allowed_users.add(user_id)
        logger.info(f"Added user {user_id} to allowed list")

    def remove_user(self, user_id: int):
        """Remove user from allowed list"""
        if user_id in self.allowed_users:
            self.allowed_users.remove(user_id)
            logger.info(f"Removed user {user_id} from allowed list")


class SecurityFilter:
    """Filter sensitive information from outputs"""

    # Patterns to redact
    PATTERNS = [
        (r'sk_live_[a-zA-Z0-9_]+', '[STRIPE_LIVE_KEY]'),
        (r'sk_test_[a-zA-Z0-9_]+', '[STRIPE_TEST_KEY]'),
        (r'sk-[a-zA-Z0-9]{48}', '[OPENAI_API_KEY]'),
        (r'sk-ant-[a-zA-Z0-9_-]+', '[ANTHROPIC_API_KEY]'),
        (r'ghp_[a-zA-Z0-9]{36}', '[GITHUB_TOKEN]'),
        (r'gho_[a-zA-Z0-9]{36}', '[GITHUB_OAUTH]'),
        (r'(password|passwd|pwd)[\s:=]+[^\s,;]+', r'\1: [REDACTED]'),
        (r'(token|secret|api_key)[\s:=]+[^\s,;]+', r'\1: [REDACTED]'),
        (r'(Bearer|Basic)\s+[^\s]+', r'\1 [REDACTED]'),
        (r'postgres://[^\s]+', 'postgres://[REDACTED]'),
        (r'mysql://[^\s]+', 'mysql://[REDACTED]'),
        (r'mongodb://[^\s]+', 'mongodb://[REDACTED]'),
        (r'redis://[^\s]+', 'redis://[REDACTED]'),
        (r'(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)[\s:=]+[^\s]+', r'\1: [REDACTED]'),
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """Remove sensitive data from text"""
        if not text:
            return text

        sanitized = text
        for pattern, replacement in cls.PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @classmethod
    def sanitize_file_content(cls, content: str, file_path: str) -> str:
        """Sanitize file content based on file type"""
        # Don't show content of sensitive files at all
        sensitive_files = [
            '.env', '.env.local', '.env.production',
            'secrets.json', 'credentials.json',
            'id_rsa', 'id_ed25519', '.pem', '.key'
        ]

        for sensitive in sensitive_files:
            if sensitive in file_path:
                return "[SENSITIVE FILE CONTENT HIDDEN]"

        return cls.sanitize(content)


# Global auth instance
auth = Auth()
security = SecurityFilter()
