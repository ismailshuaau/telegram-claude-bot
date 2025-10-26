#!/bin/bash
# Verify Agent Awareness Integration

echo "======================================================================"
echo "🔍 Verifying Agent Awareness Integration"
echo "======================================================================"
echo ""

# Check 1: PROJECT_DIR is set and points to ChefVision
echo "1. Checking PROJECT_DIR environment variable..."
if [ -z "$PROJECT_DIR" ]; then
    echo "   ⚠️  PROJECT_DIR not set"
    echo "   📝 Set it with: export PROJECT_DIR='/home/ubuntu/projects/chefvision-analytics-platform'"
else
    echo "   ✅ PROJECT_DIR set to: $PROJECT_DIR"
fi
echo ""

# Check 2: Agent system exists
echo "2. Checking for agent system..."
if [ -z "$PROJECT_DIR" ]; then
    AGENT_PATH="/home/ubuntu/projects/chefvision-analytics-platform/.claude/agents"
else
    AGENT_PATH="$PROJECT_DIR/.claude/agents"
fi

if [ -d "$AGENT_PATH" ]; then
    echo "   ✅ Agent system found at: $AGENT_PATH"
else
    echo "   ❌ Agent system NOT found at: $AGENT_PATH"
    echo "   📝 Make sure you're pointing to the ChefVision project"
    exit 1
fi
echo ""

# Check 3: Agent learnings exist
echo "3. Checking for agent learnings..."
LEARNINGS_COUNT=$(find "$AGENT_PATH/learnings" -name "*.md" -type f 2>/dev/null | wc -l)
if [ "$LEARNINGS_COUNT" -gt 0 ]; then
    echo "   ✅ Found $LEARNINGS_COUNT agent learning files:"
    find "$AGENT_PATH/learnings" -name "*.md" -type f -exec basename {} \; | sed 's/^/      - /'
else
    echo "   ⚠️  No agent learnings found (will create as you use the bot)"
fi
echo ""

# Check 4: Agent context directory exists
echo "4. Checking for agent context..."
if [ -d "$AGENT_PATH/context" ]; then
    echo "   ✅ Agent context directory exists"
else
    echo "   ⚠️  Agent context directory not found (will be created as needed)"
fi
echo ""

# Check 5: Agent handoffs file exists
echo "5. Checking for agent handoffs..."
if [ -f "$AGENT_PATH/shared/handoffs.json" ]; then
    echo "   ✅ Agent handoffs file exists"
else
    echo "   ⚠️  Agent handoffs file not found (will be created as needed)"
fi
echo ""

# Check 6: telegram_proxy.py has agent awareness
echo "6. Checking telegram_proxy.py for agent awareness..."
if grep -q "_get_agent_aware_prompt" telegram_proxy.py; then
    echo "   ✅ Agent awareness code found in telegram_proxy.py"
else
    echo "   ❌ Agent awareness code NOT found"
    echo "   📝 The enhancement may not have been applied"
    exit 1
fi
echo ""

# Summary
echo "======================================================================"
echo "📊 Summary"
echo "======================================================================"
echo ""

if [ -d "$AGENT_PATH" ] && grep -q "_get_agent_aware_prompt" telegram_proxy.py; then
    echo "✅ Agent awareness is READY!"
    echo ""
    echo "Next steps:"
    echo "1. Make sure PROJECT_DIR is set:"
    echo "   export PROJECT_DIR='/home/ubuntu/projects/chefvision-analytics-platform'"
    echo ""
    echo "2. Start the bot:"
    echo "   ./start-local.sh"
    echo ""
    echo "3. Test via Telegram:"
    echo "   'what agent learnings are available?'"
    echo "   'what has aws-infrastructure-specialist learned?'"
    echo "   'deploy to staging'"
    echo ""
else
    echo "❌ Agent awareness NOT ready"
    echo ""
    echo "Issues found:"
    if [ ! -d "$AGENT_PATH" ]; then
        echo "- Agent system not found at $AGENT_PATH"
    fi
    if ! grep -q "_get_agent_aware_prompt" telegram_proxy.py; then
        echo "- Agent awareness code not in telegram_proxy.py"
    fi
fi

echo "======================================================================"
