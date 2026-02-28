#!/bin/bash
set -e

# Better Feishu for OpenClaw - One-click Setup
#
# Installs plugin, applies patches, and injects workspace templates.
#
# Usage:
#   bash setup.sh [--openclaw-dir ~/openclaw]
#
# What it does:
#   1. Backs up existing feishu plugin (if any)
#   2. Installs plugin files to ~/.openclaw/extensions/feishu/
#   3. Applies runtime patches to OpenClaw core (fixes target handling + injects feishu rules)
#   4. Injects feishu-related templates into workspace md files (SOUL.md, TOOLS.md, AGENTS.md, USER.md)
#
# Templates are injected idempotently — running setup.sh again will update existing injections.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_DIR="${HOME}/openclaw"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --openclaw-dir)
            OPENCLAW_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: bash setup.sh [--openclaw-dir ~/openclaw]"
            echo ""
            echo "Options:"
            echo "  --openclaw-dir  Path to openclaw installation (default: ~/openclaw)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: bash setup.sh [--openclaw-dir ~/openclaw]"
            exit 1
            ;;
    esac
done

OPENCLAW_HOME="${HOME}/.openclaw"
EXTENSIONS_DIR="${OPENCLAW_HOME}/extensions/feishu"
WORKSPACE_DIR="${OPENCLAW_HOME}/workspace"

echo "=== Better Feishu for OpenClaw - Setup ==="
echo ""
echo "  Plugin source: ${SCRIPT_DIR}"
echo "  OpenClaw dir:  ${OPENCLAW_DIR}"
echo "  Extensions:    ${EXTENSIONS_DIR}"
echo "  Workspace:     ${WORKSPACE_DIR}"
echo ""

# Step 1: Backup existing plugin
if [ -d "${EXTENSIONS_DIR}" ]; then
    BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
    echo "[1/4] Backing up existing plugin → feishu.bak.${BACKUP_TIME}"
    cp -r "${EXTENSIONS_DIR}" "${EXTENSIONS_DIR}.bak.${BACKUP_TIME}"
else
    echo "[1/4] No existing plugin to backup"
fi

# Step 2: Install plugin files
echo "[2/4] Installing plugin files..."
mkdir -p "${EXTENSIONS_DIR}/dist"
mkdir -p "${EXTENSIONS_DIR}/skills/feishu"

cp "${SCRIPT_DIR}/dist/index.js" "${EXTENSIONS_DIR}/dist/"
cp "${SCRIPT_DIR}/openclaw.plugin.json" "${EXTENSIONS_DIR}/"
cp "${SCRIPT_DIR}/package.json" "${EXTENSIONS_DIR}/"
cp "${SCRIPT_DIR}/skills/feishu/SKILL.md" "${EXTENSIONS_DIR}/skills/feishu/"
echo "  Done"

# Step 3: Apply patches to OpenClaw core
echo "[3/4] Applying patches to OpenClaw core..."
if [ -d "${OPENCLAW_DIR}/dist" ]; then
    python3 "${SCRIPT_DIR}/patches/patch-channel-target.py" --openclaw-dir "${OPENCLAW_DIR}" 2>&1 | sed 's/^/  /'
    python3 "${SCRIPT_DIR}/patches/patch-feishu-messaging.py" --openclaw-dir "${OPENCLAW_DIR}" 2>&1 | sed 's/^/  /'
else
    echo "  WARNING: OpenClaw dist not found at ${OPENCLAW_DIR}/dist, skipping patches"
    echo "  You can apply patches later:"
    echo "    python3 ${SCRIPT_DIR}/patches/patch-channel-target.py --openclaw-dir /path/to/openclaw"
    echo "    python3 ${SCRIPT_DIR}/patches/patch-feishu-messaging.py --openclaw-dir /path/to/openclaw"
fi

# Step 4: Inject templates into workspace
echo "[4/4] Injecting workspace templates..."
python3 "${SCRIPT_DIR}/scripts/inject-templates.py" \
    --workspace-dir "${WORKSPACE_DIR}" \
    --templates-dir "${SCRIPT_DIR}/templates" 2>&1 | sed 's/^/  /'

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Configure feishu channel in ${OPENCLAW_HOME}/openclaw.json (appId, appSecret, etc.)"
echo "  2. Restart gateway: systemctl --user restart openclaw-gateway"
echo ""
echo "To update later, just run setup.sh again — templates are injected idempotently."
