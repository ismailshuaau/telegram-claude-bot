#!/usr/bin/env python3
"""
Simple script to get your Telegram User ID
Just run this, then message the bot from Telegram
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Get bot token from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN not set!")
    print("\nSet it with:")
    print("  export TELEGRAM_BOT_TOKEN='your-bot-token'")
    exit(1)

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user their ID"""
    user = update.effective_user

    message = f"""
🆔 Your Telegram Information:

**User ID:** {user.id}
**First Name:** {user.first_name}
**Username:** @{user.username if user.username else 'None'}
**Language:** {user.language_code}

Copy this to use in ALLOWED_USER_IDS:
`{user.id}`
"""

    await update.message.reply_text(message, parse_mode='Markdown')

    # Also print to console
    print(f"\n{'='*50}")
    print(f"User ID: {user.id}")
    print(f"Name: {user.first_name}")
    print(f"Username: @{user.username if user.username else 'None'}")
    print(f"{'='*50}\n")

def main():
    """Run the ID getter bot"""
    print("\n" + "="*60)
    print("🆔 Telegram User ID Finder")
    print("="*60)
    print("\n📱 Send any message to your bot in Telegram")
    print("   You'll get your User ID back!\n")
    print("Press Ctrl+C to stop\n")
    print("="*60 + "\n")

    # Create application
    app = Application.builder().token(BOT_TOKEN).build()

    # Handle any message
    app.add_handler(MessageHandler(filters.ALL, show_id))

    # Run
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
