"""
Main Telegram Claude Code Bot Implementation
Provides vibe coding interface via Telegram
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import config
from auth import auth, security
from claude_code_bridge import bridge

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


class TelegramClaudeBot:
    """Main Telegram bot for Claude Code vibe coding"""

    def __init__(self):
        self.app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all message and command handlers"""

        # Commands
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("context", self.cmd_context))
        self.app.add_handler(CommandHandler("cancel", self.cmd_cancel))
        self.app.add_handler(CommandHandler("sessions", self.cmd_sessions))

        # Text messages (coding requests)
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Voice messages (using Telegram's built-in transcription)
        self.app.add_handler(
            MessageHandler(filters.VOICE, self.handle_voice)
        )

        # Callback queries (button presses)
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))

        # Error handler
        self.app.add_error_handler(self.error_handler)

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""

        if not auth.is_authorized(update):
            await update.message.reply_text(
                "❌ You are not authorized to use this bot.\n"
                f"Your Telegram ID: {update.effective_user.id}"
            )
            return

        welcome_msg = """
🤖 **ChefVision Dev Bot** - Vibe Coding with Claude Code

I'm your AI coding assistant powered by Claude!

**Quick Commands:**
/status - Check project status
/context backend|frontend|root - Switch working context
/sessions - View active sessions
/cancel - Cancel current operation
/help - Show this help

**Just chat naturally:**
• "Fix the billing API authentication bug"
• "Add tests for the new GDPR export feature"
• "What's the status of the mobile app?"
• "Review my latest changes"
• "Run the test suite"

**Voice messages work too!** 🎤
Just send a voice message with your request.

**Current context:** backend
**Ready to code!** 🚀
        """

        await update.message.reply_text(welcome_msg, parse_mode='Markdown')

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""

        if not auth.is_authorized(update):
            return

        help_msg = """
📚 **ChefVision Dev Bot - Help**

**Commands:**
/start - Start the bot and see welcome message
/status - Get comprehensive project status
/context <backend|frontend|root> - Switch working directory
/sessions - View your active coding sessions
/cancel - Cancel current operation
/help - Show this help

**Natural Language Coding:**
Just send a message describing what you want to do:

*Examples:*
• "Fix the Stripe webhook signature validation"
• "Add a new API endpoint for team analytics"
• "What tests are failing?"
• "Show me recent commits"
• "Deploy to staging"

**Voice Messages:**
Send a voice message! Telegram will transcribe it automatically
and I'll process your request.

**Contexts:**
• `backend` - Django/Python backend code
• `frontend` - React Native mobile app
• `root` - Full project access

**Features:**
✅ Natural conversation
✅ Automatic code changes
✅ Test execution
✅ Git operations
✅ Project status monitoring
✅ File diffs and previews

Have fun coding! 🚀
        """

        await update.message.reply_text(help_msg, parse_mode='Markdown')

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get comprehensive project status"""

        if not auth.is_authorized(update):
            return

        if not auth.check_rate_limit(update.effective_user.id):
            await update.message.reply_text("⚠️ Rate limit exceeded. Please wait a moment.")
            return

        await update.message.reply_chat_action("typing")

        try:
            # Get current context
            current_context = context.user_data.get('context', 'backend')
            working_dir = self._get_working_dir(current_context)

            # Get status from bridge
            status = await bridge.get_status(working_dir)

            # Format status message
            git_status = status.get('git', {})
            services = status.get('services', {})

            status_msg = f"""
📊 **Project Status**

**Context:** {current_context}
**Directory:** {working_dir}

**Git Status:**
"""

            if git_status.get('clean'):
                status_msg += "✅ Working tree clean\n"
            else:
                status_msg += f"""
Modified: {git_status.get('modified', 0)}
Added: {git_status.get('added', 0)}
Deleted: {git_status.get('deleted', 0)}
Untracked: {git_status.get('untracked', 0)}

```
{git_status.get('output', '')}
```
"""

            status_msg += "\n**Services:**\n"
            for service, running in services.items():
                emoji = "✅" if running else "❌"
                status_msg += f"{emoji} {service.capitalize()}: {'Running' if running else 'Stopped'}\n"

            # Add action buttons
            keyboard = [
                [
                    InlineKeyboardButton("🧪 Run Tests", callback_data='run_tests'),
                    InlineKeyboardButton("🔨 Build", callback_data='run_build')
                ],
                [
                    InlineKeyboardButton("📊 Git Log", callback_data='git_log'),
                    InlineKeyboardButton("🔄 Pull Latest", callback_data='git_pull')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                status_msg,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

        except Exception as e:
            logger.error(f"Status command failed: {e}", exc_info=True)
            await update.message.reply_text(f"❌ Error getting status: {str(e)}")

    async def cmd_context(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Switch working context"""

        if not auth.is_authorized(update):
            return

        # Get requested context
        args = context.args
        if not args:
            current = context.user_data.get('context', 'backend')
            await update.message.reply_text(
                f"Current context: **{current}**\n\n"
                f"Usage: `/context backend|frontend|root`",
                parse_mode='Markdown'
            )
            return

        new_context = args[0].lower()
        valid_contexts = ['backend', 'frontend', 'root']

        if new_context not in valid_contexts:
            await update.message.reply_text(
                f"❌ Invalid context. Choose from: {', '.join(valid_contexts)}"
            )
            return

        # Update context
        context.user_data['context'] = new_context
        working_dir = self._get_working_dir(new_context)

        await update.message.reply_text(
            f"✅ Switched to **{new_context}** context\n"
            f"Working directory: `{working_dir}`",
            parse_mode='Markdown'
        )

    async def cmd_sessions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View active sessions"""

        if not auth.is_authorized(update):
            return

        user_id = update.effective_user.id
        user_sessions = [
            s for s in bridge.sessions.values()
            if s.user_id == user_id
        ]

        if not user_sessions:
            await update.message.reply_text("No active sessions.")
            return

        msg = "**Your Active Sessions:**\n\n"
        for session in user_sessions:
            age = (datetime.now() - session.last_activity).total_seconds()
            msg += f"• **{session.context}** (idle {int(age)}s)\n"
            msg += f"  Commands: {len(session.history)}\n\n"

        await update.message.reply_text(msg, parse_mode='Markdown')

    async def cmd_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation"""

        if not auth.is_authorized(update):
            return

        await update.message.reply_text("✅ Operation cancelled")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (coding requests)"""

        if not auth.is_authorized(update):
            await update.message.reply_text(
                f"❌ Unauthorized. Your ID: {update.effective_user.id}"
            )
            return

        user_id = update.effective_user.id

        if not auth.check_rate_limit(user_id):
            await update.message.reply_text(
                "⚠️ Slow down! You've hit the rate limit. Try again in a minute."
            )
            return

        message = update.message.text
        logger.info(f"User {user_id} request: {message[:100]}")

        # Send typing indicator
        await update.message.reply_chat_action("typing")

        # Get current context
        current_context = context.user_data.get('context', 'backend')

        try:
            # Execute via Claude Code bridge
            result = await bridge.execute_command(user_id, message, current_context)

            # Format and send response
            response = self._format_response(result)

            # Sanitize sensitive data
            response = security.sanitize(response)

            # Generate action buttons
            keyboard = self._generate_action_buttons(result)
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

            await update.message.reply_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

            # Send file diffs if applicable
            if result.get('files_changed'):
                await self._send_diffs(update, result['files_changed'], current_context)

        except Exception as e:
            logger.error(f"Message handling failed: {e}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error: {str(e)}\n\n"
                "Try rephrasing your request or use /help for guidance."
            )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages (using Telegram's built-in transcription)"""

        if not auth.is_authorized(update):
            return

        # Telegram provides automatic transcription in the caption or via API
        # First, check if transcription is available
        voice_text = None

        # Method 1: Check caption (if user has voice-to-text enabled)
        if update.message.caption:
            voice_text = update.message.caption

        # Method 2: Some clients provide it in different fields
        # (This depends on Telegram client implementation)

        if voice_text:
            logger.info(f"Voice transcription received: {voice_text[:100]}")
            await update.message.reply_text(
                f"🎤 You said: _{voice_text}_\n\nProcessing...",
                parse_mode='Markdown'
            )

            # Process as text message
            update.message.text = voice_text
            await self.handle_message(update, context)
        else:
            await update.message.reply_text(
                "🎤 Voice message received! Unfortunately, I couldn't get the transcription.\n\n"
                "**Tip:** Make sure voice-to-text is enabled in your Telegram settings, "
                "or send a text message instead."
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button presses"""

        query = update.callback_query
        await query.answer()

        if not auth.is_authorized(update):
            return

        action = query.data
        logger.info(f"Callback action: {action}")

        try:
            if action == 'run_tests':
                await self._run_tests(query, context)
            elif action == 'run_build':
                await self._run_build(query, context)
            elif action == 'git_log':
                await self._git_log(query, context)
            elif action == 'git_pull':
                await self._git_pull(query, context)
            elif action.startswith('approve_'):
                await self._approve_action(query, action)
            elif action.startswith('reject_'):
                await self._reject_action(query, action)

        except Exception as e:
            logger.error(f"Callback handling failed: {e}", exc_info=True)
            await query.edit_message_text(f"❌ Error: {str(e)}")

    async def _run_tests(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Run test suite"""
        current_context = context.user_data.get('context', 'backend')
        user_id = query.from_user.id

        await query.edit_message_text("🧪 Running tests...")

        result = await bridge.execute_command(
            user_id,
            "Run the full test suite and show results",
            current_context
        )

        response = self._format_response(result)
        await query.edit_message_text(response, parse_mode='Markdown')

    async def _run_build(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Run build"""
        current_context = context.user_data.get('context', 'backend')
        user_id = query.from_user.id

        await query.edit_message_text("🔨 Running build...")

        result = await bridge.execute_command(
            user_id,
            "Run the build process",
            current_context
        )

        response = self._format_response(result)
        await query.edit_message_text(response, parse_mode='Markdown')

    async def _git_log(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Show git log"""
        await query.edit_message_text("📊 Fetching git log...")

        current_context = context.user_data.get('context', 'backend')
        working_dir = self._get_working_dir(current_context)

        process = await asyncio.create_subprocess_exec(
            'git', 'log', '--oneline', '-10',
            cwd=working_dir,
            stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()
        log = stdout.decode()

        await query.edit_message_text(
            f"**Recent Commits:**\n```\n{log}\n```",
            parse_mode='Markdown'
        )

    async def _git_pull(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Git pull latest"""
        await query.edit_message_text("🔄 Pulling latest changes...")

        current_context = context.user_data.get('context', 'backend')
        working_dir = self._get_working_dir(current_context)

        process = await asyncio.create_subprocess_exec(
            'git', 'pull',
            cwd=working_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        output = stdout.decode() + stderr.decode()

        await query.edit_message_text(
            f"✅ Git pull complete:\n```\n{output[:500]}\n```",
            parse_mode='Markdown'
        )

    async def _approve_action(self, query, action: str):
        """Approve pending action"""
        await query.edit_message_text("✅ Approved")

    async def _reject_action(self, query, action: str):
        """Reject pending action"""
        await query.edit_message_text("❌ Rejected")

    async def _send_diffs(self, update: Update, files: list, context: str):
        """Send file diffs"""
        working_dir = self._get_working_dir(context)

        for file_path in files[:5]:  # Limit to 5 files
            try:
                process = await asyncio.create_subprocess_exec(
                    'git', 'diff', file_path,
                    cwd=working_dir,
                    stdout=asyncio.subprocess.PIPE
                )

                stdout, _ = await process.communicate()
                diff = stdout.decode()

                if not diff:
                    continue

                # Sanitize diff
                diff = security.sanitize_file_content(diff, file_path)

                if len(diff) > 3500:
                    # Send as file
                    diff_file = f"/tmp/diff_{int(datetime.now().timestamp())}.patch"
                    with open(diff_file, 'w') as f:
                        f.write(diff)

                    await update.message.reply_document(
                        document=open(diff_file, 'rb'),
                        filename=f"{file_path.split('/')[-1]}.patch"
                    )
                else:
                    await update.message.reply_text(
                        f"📝 **{file_path}**\n```diff\n{diff}\n```",
                        parse_mode='Markdown'
                    )

            except Exception as e:
                logger.error(f"Failed to send diff for {file_path}: {e}")

    def _format_response(self, result: dict) -> str:
        """Format Claude Code result for Telegram"""

        if not result.get('success'):
            return f"❌ {result.get('error', 'Unknown error')}\n\n{result.get('output', '')[:1000]}"

        output = result.get('output', 'Done')
        files_changed = result.get('files_changed', [])
        tests = result.get('tests_run', {})

        response = f"🤖 {output[:2000]}\n\n"

        if files_changed:
            response += f"📝 **Modified {len(files_changed)} file(s):**\n"
            for f in files_changed[:10]:
                response += f"  • `{f}`\n"
            if len(files_changed) > 10:
                response += f"  ... and {len(files_changed) - 10} more\n"

        if tests.get('ran'):
            passed = tests.get('passed', 0)
            total = tests.get('total', 0)
            failed = tests.get('failed', 0)

            emoji = "✅" if passed == total else "⚠️"
            response += f"\n{emoji} **Tests:** {passed}/{total} passed"
            if failed > 0:
                response += f", {failed} failed"
            response += "\n"

        return response

    def _generate_action_buttons(self, result: dict) -> list:
        """Generate action buttons based on result"""

        buttons = []

        if result.get('files_changed'):
            buttons.append([
                InlineKeyboardButton("✅ Commit Changes", callback_data='approve_commit'),
                InlineKeyboardButton("❌ Revert", callback_data='reject_revert')
            ])

        return buttons

    def _get_working_dir(self, context: str) -> str:
        """Get working directory for context"""
        paths = {
            'backend': config.BACKEND_PATH,
            'frontend': config.FRONTEND_PATH,
            'root': config.PROJECT_ROOT,
        }
        return paths.get(context, config.PROJECT_ROOT)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error("Exception while handling update:", exc_info=context.error)

        # Notify user if possible
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. "
                "Please try again or contact support."
            )

    def run(self):
        """Start the bot"""
        logger.info("🤖 Starting Telegram Claude Code Bot...")
        logger.info(f"Allowed users: {config.ALLOWED_USERS}")
        logger.info(f"Project root: {config.PROJECT_ROOT}")

        # Cleanup old sessions periodically
        async def cleanup_sessions(context):
            bridge.cleanup_old_sessions(config.SESSION_TIMEOUT)

        self.app.job_queue.run_repeating(cleanup_sessions, interval=300, first=60)

        # Run bot
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""

    # Validate configuration
    if not config.validate():
        logger.error("❌ Invalid configuration. Please check your environment variables.")
        return 1

    # Create and run bot
    bot = TelegramClaudeBot()
    bot.run()


if __name__ == '__main__':
    main()
