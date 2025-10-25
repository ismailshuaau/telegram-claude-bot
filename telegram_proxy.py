#!/usr/bin/env python3
"""
Telegram Claude Code Proxy - Simple Version
Pure pass-through between Telegram and Claude Code CLI

This is a SIMPLE proxy that:
1. Receives messages from Telegram
2. Forwards to Claude Code CLI (persistent session)
3. Sends responses back to Telegram

NO restrictions, NO system prompts, NO special logic
Just like chatting with Claude Code directly!
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Reduce noise from httpx (Telegram API calls)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER_IDS = [int(uid) for uid in os.getenv('ALLOWED_USER_IDS', '').split(',') if uid]
PROJECT_DIR = os.getenv('PROJECT_DIR', os.getcwd())


class ClaudeCodeSession:
    """Maintains persistent Claude Code CLI session with streaming I/O"""

    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.process = None
        self.session_active = False
        self.claude_cmd = self._find_claude_command()
        self.message_counter = 0

    def _find_claude_command(self):
        """Find which Claude command is available (claude-code or claude)"""
        import subprocess

        # Try claude-code first (preferred)
        try:
            subprocess.run(['claude-code', '--version'], capture_output=True, check=True)
            return 'claude-code'
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # Try claude as fallback
        try:
            result = subprocess.run(['claude', '--version'], capture_output=True, check=True, text=True)
            # Make sure it's Claude Code, not the old claude CLI
            if 'Claude Code' in result.stdout:
                return 'claude'
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        return None

    async def start(self):
        """Initialize Claude Code session"""
        if not self.claude_cmd:
            logger.error("❌ Claude Code not found! Install with: npm install -g @anthropic-ai/claude-code")
            return False

        self.session_active = True
        logger.info(f"✅ Claude Code ready")
        return True

    async def send_message(self, message: str) -> str:
        """Send message to Claude Code and get response (optimized)"""

        if not self.session_active:
            await self.start()

        if not self.claude_cmd:
            return "❌ Claude Code not available"

        try:
            self.message_counter += 1

            # Use --print --continue for context persistence
            # Use --verbose to get full output
            cmd = [
                self.claude_cmd,
                '--print',
                '--continue',
                '--verbose',
                message
            ]

            # Run Claude Code command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env={**os.environ}
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=300  # 5 minutes max
                )

                # Decode outputs
                stdout_text = stdout.decode('utf-8') if stdout else ""
                stderr_text = stderr.decode('utf-8') if stderr else ""

                # Claude Code outputs to stderr in verbose mode
                # Combine both for full output
                full_output = ""
                if stderr_text:
                    full_output += stderr_text
                if stdout_text:
                    if full_output:
                        full_output += "\n"
                    full_output += stdout_text

                if process.returncode == 0:
                    return full_output.strip() if full_output.strip() else "No response received"
                else:
                    logger.error(f"Claude Code error (exit {process.returncode})")
                    return full_output.strip() if full_output.strip() else f"❌ Error: Process exited with code {process.returncode}"

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return "❌ Response timeout (>5 minutes)"

        except Exception as e:
            logger.error(f"Error communicating with Claude Code: {e}")
            return f"❌ Error: {str(e)}"

    async def stop(self):
        """Stop Claude Code session"""
        self.session_active = False
        logger.info(f"Claude Code session stopped (processed {self.message_counter} messages)")


class TelegramClaudeProxy:
    """Pure proxy between Telegram and Claude Code"""

    def __init__(self):
        self.claude_session = ClaudeCodeSession(PROJECT_DIR)
        self.app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    def _extract_clean_response(self, full_response: str) -> str:
        """Extract clean text response from Claude Code output (remove XML, thinking blocks, etc.)"""
        import re

        # Remove XML tags like <function_calls>, <budget>, <timing>, etc.
        clean = re.sub(r'<[^>]+>.*?</[^>]+>', '', full_response, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '', clean)

        # Remove standalone closing tags
        clean = re.sub(r'</[^>]+>', '', clean)

        # Clean up multiple newlines
        clean = re.sub(r'\n{3,}', '\n\n', clean)

        return clean.strip()

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""

        # Check authorization
        if ALLOWED_USER_IDS and update.effective_user.id not in ALLOWED_USER_IDS:
            await update.message.reply_text(
                f"❌ Unauthorized\n"
                f"Your Telegram ID: {update.effective_user.id}"
            )
            return

        welcome = """
🤖 **Telegram Claude Code Proxy**

I'm a direct connection to Claude Code CLI running on this machine!

**You can:**
✅ Chat naturally about anything
✅ Ask me to read/write/edit code
✅ Have long conversations
✅ Ask coding questions
✅ Get explanations
✅ Plan architecture
✅ Fix bugs
✅ EVERYTHING Claude Code can do!

**Just chat naturally - no commands needed!**

Try:
• "What files are in this project?"
• "Explain how the authentication works"
• "Fix the bug in billing.py"
• "What should I work on today?"

Ready! 🚀
        """

        await update.message.reply_text(welcome, parse_mode='Markdown')

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""

        help_text = """
📚 **How to Use**

Just chat naturally! Examples:

**General conversation:**
• "Explain how webhooks work"
• "What's the difference between async and sync?"
• "Tell me about this codebase"

**Code reading:**
• "What files are in the billing module?"
• "Explain the authentication flow"
• "Show me the database schema"

**Code editing:**
• "Fix the bug in payment validation"
• "Add logging to all API endpoints"
• "Refactor the user model"

**Planning:**
• "How should I implement real-time notifications?"
• "Review my architecture"
• "What are the security risks?"

**No limits, no restrictions - full Claude Code!** 🤖
        """

        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Forward message to Claude Code, return response"""

        # Check authorization
        if ALLOWED_USER_IDS and update.effective_user.id not in ALLOWED_USER_IDS:
            await update.message.reply_text(
                f"❌ Unauthorized. Your ID: {update.effective_user.id}"
            )
            return

        user_message = update.message.text
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or f"User {user_id}"

        # Print user message to console (exactly like Claude Code shows it)
        print("\n" + "="*70)
        print(f"You: {user_message}")
        print("="*70 + "\n")

        # Show typing indicator
        await update.message.reply_chat_action("typing")

        # Forward to Claude Code CLI and print response exactly as it appears
        full_response = await self.claude_session.send_message(user_message)

        # Print the full Claude Code output to terminal (includes thinking, tokens, time, etc.)
        print(full_response)
        print("\n" + "="*70 + "\n")

        # Extract clean response for Telegram (remove XML tags, thinking blocks, etc.)
        clean_response = self._extract_clean_response(full_response)

        # Send clean response back to Telegram
        # Split into chunks if too long (Telegram has 4096 char limit)
        if len(clean_response) <= 4096:
            await update.message.reply_text(clean_response)
        else:
            # Split into chunks
            chunks = [clean_response[i:i+4000] for i in range(0, len(clean_response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception: {context.error}", exc_info=context.error)

        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again."
            )

    async def startup(self, application):
        """Initialize on startup"""
        print("\n" + "="*60)
        print("🚀 Telegram Claude Code Proxy Started!")
        print("="*60)
        print(f"📁 Project: {PROJECT_DIR}")
        print(f"👥 Allowed users: {ALLOWED_USER_IDS}")
        print("="*60)
        print("📱 Waiting for messages from Telegram...")
        print("="*60 + "\n")

        # Start Claude Code session
        started = await self.claude_session.start()
        if not started:
            logger.error("Failed to start Claude Code session!")

    async def shutdown(self, application):
        """Cleanup on shutdown"""
        print("\n" + "="*60)
        print("👋 Shutting down Telegram Claude Code Proxy...")
        print("="*60 + "\n")
        await self.claude_session.stop()

    def run(self):
        """Start the bot"""

        # Validate config
        if not TELEGRAM_BOT_TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
            return

        # Add handlers
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Error handler
        self.app.add_error_handler(self.error_handler)

        # Startup/shutdown hooks
        self.app.post_init = self.startup
        self.app.post_shutdown = self.shutdown

        # Run
        logger.info("✅ Bot starting...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""

    # Check for required env vars
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set!")
        print("\nSet it with:")
        print("  export TELEGRAM_BOT_TOKEN='your-bot-token'")
        return 1

    if not ALLOWED_USER_IDS:
        print("⚠️  Warning: ALLOWED_USER_IDS not set - bot will accept anyone!")
        print("Set it with:")
        print("  export ALLOWED_USER_IDS='123456789,987654321'")

    # Check if claude-code or claude is installed
    import subprocess
    claude_cmd = None

    # Try claude-code first
    try:
        subprocess.run(['claude-code', '--version'], capture_output=True, check=True)
        claude_cmd = 'claude-code'
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Try claude as fallback
        try:
            result = subprocess.run(['claude', '--version'], capture_output=True, check=True, text=True)
            if 'Claude Code' in result.stdout:
                claude_cmd = 'claude'
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    if not claude_cmd:
        print("❌ Error: Claude Code not found!")
        print("\nInstall with:")
        print("  npm install -g @anthropic-ai/claude-code")
        print("\nThen login with:")
        print("  claude-code login  (or: claude login)")
        return 1
    else:
        print(f"✅ Found Claude Code: {claude_cmd}")

    # Create and run proxy
    proxy = TelegramClaudeProxy()
    proxy.run()


if __name__ == '__main__':
    main()
