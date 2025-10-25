"""
Configuration for Telegram Claude Code Bot
"""

import os
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class BotConfig:
    """Bot configuration"""

    # Telegram Bot Token (get from @BotFather)
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')

    # Authentication Method: 'api', 'cli', or 'auto'
    # - 'api': Use Anthropic API (requires ANTHROPIC_API_KEY)
    # - 'cli': Use Claude Code CLI (requires logged-in Claude account)
    # - 'auto': Auto-detect (prefers CLI if available, falls back to API)
    AUTH_METHOD: str = os.getenv('AUTH_METHOD', 'auto')

    # Anthropic API Key for Claude (required if AUTH_METHOD='api')
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')

    # OpenAI API Key (optional, for Whisper voice transcription)
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    # Allowed Telegram User IDs (get from @userinfobot)
    ALLOWED_USERS: List[int] = [
        int(uid) for uid in os.getenv('ALLOWED_USER_IDS', '').split(',') if uid
    ]

    # Project paths
    PROJECT_ROOT: str = os.getenv('PROJECT_ROOT', '/home/ubuntu/project')
    BACKEND_PATH: str = os.path.join(PROJECT_ROOT, 'transcription-platform')
    FRONTEND_PATH: str = os.path.join(PROJECT_ROOT, 'expo-voice-analytics-mobile-app')

    # Claude Code settings
    CLAUDE_MODEL: str = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
    CLAUDE_TIMEOUT: int = int(os.getenv('CLAUDE_TIMEOUT', '300'))  # 5 minutes

    # Voice transcription settings
    VOICE_MODEL: str = os.getenv('VOICE_MODEL', 'whisper-1')  # or 'base', 'small', 'medium', 'large'
    USE_LOCAL_WHISPER: bool = os.getenv('USE_LOCAL_WHISPER', 'true').lower() == 'true'

    # Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '10'))

    # Session management
    SESSION_TIMEOUT: int = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
    MAX_PARALLEL_SESSIONS: int = int(os.getenv('MAX_PARALLEL_SESSIONS', '3'))

    # Notification settings
    ENABLE_NOTIFICATIONS: bool = os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true'
    NOTIFY_ON_ERROR: bool = os.getenv('NOTIFY_ON_ERROR', 'true').lower() == 'true'
    NOTIFY_ON_COMPLETION: bool = os.getenv('NOTIFY_ON_COMPLETION', 'true').lower() == 'true'

    # Git settings
    GIT_AUTO_COMMIT: bool = os.getenv('GIT_AUTO_COMMIT', 'false').lower() == 'true'
    GIT_AUTO_PUSH: bool = os.getenv('GIT_AUTO_PUSH', 'false').lower() == 'true'

    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', '/var/log/telegram-claude-bot/bot.log')

    @classmethod
    def is_claude_cli_available(cls) -> bool:
        """Check if Claude Code CLI is installed and authenticated"""
        import subprocess
        try:
            # Check if claude-code command exists
            result = subprocess.run(
                ['which', 'claude-code'],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                return False

            # Check if authenticated (try --version as a simple check)
            result = subprocess.run(
                ['claude-code', '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    @classmethod
    def get_auth_method(cls) -> str:
        """Determine which authentication method to use"""
        config = cls()

        if config.AUTH_METHOD == 'api':
            return 'api'
        elif config.AUTH_METHOD == 'cli':
            return 'cli'
        else:  # 'auto'
            # Prefer CLI if available, fall back to API
            if cls.is_claude_cli_available():
                return 'cli'
            elif config.ANTHROPIC_API_KEY:
                return 'api'
            else:
                return 'none'

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        config = cls()

        if not config.TELEGRAM_BOT_TOKEN:
            print("❌ TELEGRAM_BOT_TOKEN not set!")
            return False

        # Check authentication method
        auth_method = cls.get_auth_method()

        if auth_method == 'none':
            print("❌ No authentication method available!")
            print("   Please either:")
            print("   1. Set ANTHROPIC_API_KEY for API authentication")
            print("   2. Login to Claude CLI with: claude-code login")
            return False
        elif auth_method == 'api':
            if not config.ANTHROPIC_API_KEY:
                print("❌ AUTH_METHOD='api' but ANTHROPIC_API_KEY not set!")
                return False
            print(f"✅ Using Anthropic API authentication")
        elif auth_method == 'cli':
            if not cls.is_claude_cli_available():
                print("❌ AUTH_METHOD='cli' but Claude CLI not available!")
                print("   Install with: npm install -g @anthropic-ai/claude-code")
                print("   Login with: claude-code login")
                return False
            print(f"✅ Using Claude Code CLI authentication")

        if not config.ALLOWED_USERS:
            print("⚠️  Warning: ALLOWED_USER_IDS not set - bot will accept requests from anyone!")

        if not os.path.exists(config.PROJECT_ROOT):
            print(f"❌ PROJECT_ROOT does not exist: {config.PROJECT_ROOT}")
            return False

        return True

# Singleton config instance
config = BotConfig()
