#!/bin/bash
#
# Management script for Telegram Claude Bot
# Run on EC2 instance
#

set -e

BOT_SERVICE="telegram-claude-bot"
BOT_DIR="/home/ubuntu/telegram-claude-bot"

show_help() {
    cat <<EOF
Telegram Claude Bot Management Script

Usage: $0 <command>

Commands:
    start       Start the bot service
    stop        Stop the bot service
    restart     Restart the bot service
    status      Show bot status
    logs        Show bot logs (follow mode)
    logs-tail   Show last 100 lines of logs
    enable      Enable bot to start on boot
    disable     Disable bot auto-start
    test        Test bot configuration
    update      Update bot code from repository
    backup      Backup bot configuration

Examples:
    $0 start
    $0 logs
    $0 status
EOF
}

check_service() {
    if ! systemctl list-units --full -all | grep -q "$BOT_SERVICE.service"; then
        echo "❌ Service not installed. Run setup first."
        exit 1
    fi
}

case "$1" in
    start)
        echo "🚀 Starting bot..."
        sudo systemctl start $BOT_SERVICE
        sleep 2
        sudo systemctl status $BOT_SERVICE --no-pager
        ;;

    stop)
        echo "🛑 Stopping bot..."
        sudo systemctl stop $BOT_SERVICE
        echo "✅ Bot stopped"
        ;;

    restart)
        echo "♻️  Restarting bot..."
        sudo systemctl restart $BOT_SERVICE
        sleep 2
        sudo systemctl status $BOT_SERVICE --no-pager
        ;;

    status)
        sudo systemctl status $BOT_SERVICE --no-pager
        ;;

    logs)
        echo "📋 Following logs (Ctrl+C to exit)..."
        sudo journalctl -u $BOT_SERVICE -f
        ;;

    logs-tail)
        echo "📋 Last 100 log lines..."
        sudo journalctl -u $BOT_SERVICE -n 100 --no-pager
        ;;

    enable)
        echo "✅ Enabling bot auto-start..."
        sudo systemctl enable $BOT_SERVICE
        echo "✅ Bot will start on boot"
        ;;

    disable)
        echo "❌ Disabling bot auto-start..."
        sudo systemctl disable $BOT_SERVICE
        echo "✅ Bot will not start on boot"
        ;;

    test)
        echo "🧪 Testing bot configuration..."
        cd $BOT_DIR
        source venv/bin/activate

        # Check .env file
        if [ ! -f .env ]; then
            echo "❌ .env file not found!"
            echo "Copy .env.template to .env and configure it"
            exit 1
        fi

        # Load .env
        export $(cat .env | grep -v '^#' | xargs)

        # Run validation
        python3 -c "from config import config; exit(0 if config.validate() else 1)"

        if [ $? -eq 0 ]; then
            echo "✅ Configuration valid!"
        else
            echo "❌ Configuration invalid. Check .env file"
            exit 1
        fi
        ;;

    update)
        echo "🔄 Updating bot code..."
        cd $BOT_DIR
        git pull
        source venv/bin/activate
        pip install -r requirements.txt --upgrade
        sudo systemctl restart $BOT_SERVICE
        echo "✅ Bot updated and restarted"
        ;;

    backup)
        BACKUP_FILE="/tmp/telegram-bot-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
        echo "💾 Creating backup..."
        tar -czf "$BACKUP_FILE" -C $BOT_DIR .env logs/
        echo "✅ Backup created: $BACKUP_FILE"
        ;;

    *)
        show_help
        exit 1
        ;;
esac
