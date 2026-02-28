#!/usr/bin/env bash
# Better Feishu for OpenClaw — 一键安装脚本
# 用法: bash setup.sh [--openclaw-dir ~/openclaw] [--workspace-dir ~/.openclaw/workspace]
#
# 自动完成:
#   1. 安装插件到 ~/.openclaw/extensions/feishu/
#   2. 删除内置飞书插件（避免冲突）
#   3. 应用 OpenClaw framework patches
#   4. 部署 workspace 模板（不覆盖已有内容，追加飞书相关部分）
#   5. 重启 gateway

set -euo pipefail

# --- 颜色 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; exit 1; }

# --- 参数解析 ---
OPENCLAW_DIR="${HOME}/openclaw"
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
EXTENSIONS_DIR="${HOME}/.openclaw/extensions"
SKIP_RESTART=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --openclaw-dir)  OPENCLAW_DIR="$2"; shift 2 ;;
    --workspace-dir) WORKSPACE_DIR="$2"; shift 2 ;;
    --extensions-dir) EXTENSIONS_DIR="$2"; shift 2 ;;
    --skip-restart)  SKIP_RESTART=true; shift ;;
    -h|--help)
      echo "用法: bash setup.sh [选项]"
      echo ""
      echo "选项:"
      echo "  --openclaw-dir DIR    OpenClaw 安装目录 (默认: ~/openclaw)"
      echo "  --workspace-dir DIR   Workspace 目录 (默认: ~/.openclaw/workspace)"
      echo "  --extensions-dir DIR  Extensions 目录 (默认: ~/.openclaw/extensions)"
      echo "  --skip-restart        不自动重启 gateway"
      echo "  -h, --help            显示帮助"
      exit 0
      ;;
    *) error "未知参数: $1" ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Better Feishu for OpenClaw — 一键安装   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# --- 前置检查 ---
[[ -f "${SCRIPT_DIR}/dist/index.js" ]] || error "找不到 dist/index.js，请先 pnpm build"
[[ -d "${OPENCLAW_DIR}/dist" ]] || error "OpenClaw 目录不存在: ${OPENCLAW_DIR}/dist"

# --- Step 1: 安装插件 ---
echo ""
info "Step 1/5: 安装插件"

PLUGIN_DIR="${EXTENSIONS_DIR}/feishu"
mkdir -p "${PLUGIN_DIR}/dist"

# 备份旧版本
if [[ -f "${PLUGIN_DIR}/dist/index.js" ]]; then
  cp "${PLUGIN_DIR}/dist/index.js" "${PLUGIN_DIR}/dist/index.js.bak.$(date +%Y%m%d%H%M%S)"
  warn "已备份旧版本"
fi

cp "${SCRIPT_DIR}/dist/index.js" "${PLUGIN_DIR}/dist/index.js"
# 复制 package.json 和 plugin.json（如果有）
[[ -f "${SCRIPT_DIR}/openclaw.plugin.json" ]] && cp "${SCRIPT_DIR}/openclaw.plugin.json" "${PLUGIN_DIR}/openclaw.plugin.json"
[[ -f "${SCRIPT_DIR}/package.json" ]] && cp "${SCRIPT_DIR}/package.json" "${PLUGIN_DIR}/package.json"

info "插件已安装到 ${PLUGIN_DIR}/"

# --- Step 2: 删除内置飞书插件 ---
echo ""
info "Step 2/5: 检查内置飞书插件"

BUILTIN_FEISHU="${OPENCLAW_DIR}/extensions/feishu"
if [[ -d "${BUILTIN_FEISHU}" ]]; then
  mv "${BUILTIN_FEISHU}" "${BUILTIN_FEISHU}.disabled.$(date +%Y%m%d%H%M%S)"
  warn "已禁用内置飞书插件: ${BUILTIN_FEISHU} → .disabled.*"
else
  info "无内置飞书插件，跳过"
fi

# --- Step 3: 应用 Framework Patches ---
echo ""
info "Step 3/5: 应用 Framework Patches"

PATCH_DIR="${SCRIPT_DIR}/patches"
PATCHED=0

# patch-channel-target.py — 修复自定义 action 的 target 校验
if [[ -f "${PATCH_DIR}/patch-channel-target.py" ]]; then
  if python3 "${PATCH_DIR}/patch-channel-target.py" --openclaw-dir="${OPENCLAW_DIR}" 2>&1; then
    PATCHED=$((PATCHED + 1))
  fi
else
  warn "patch-channel-target.py 不存在，跳过"
fi

# patch-feishu-messaging.py — 注入飞书交互规则到 buildMessagingSection
if [[ -f "${PATCH_DIR}/patch-feishu-messaging.py" ]]; then
  if python3 "${PATCH_DIR}/patch-feishu-messaging.py" --openclaw-dir="${OPENCLAW_DIR}" 2>&1; then
    PATCHED=$((PATCHED + 1))
  fi
else
  warn "patch-feishu-messaging.py 不存在，跳过"
fi

info "Framework patches 完成 (${PATCHED} applied)"

# --- Step 4: 部署 Workspace 模板 ---
echo ""
info "Step 4/5: 部署 Workspace 模板"

python3 "${SCRIPT_DIR}/scripts/inject-templates.py" "${SCRIPT_DIR}/templates" "${WORKSPACE_DIR}"

# 复制 skills 目录
if [[ -d "${SCRIPT_DIR}/skills" ]]; then
  mkdir -p "${WORKSPACE_DIR}/skills"
  cp -r "${SCRIPT_DIR}/skills/"* "${WORKSPACE_DIR}/skills/" 2>/dev/null || true
  info "  Skills 已复制"
fi

# --- Step 5: 重启 Gateway ---
echo ""
if [[ "${SKIP_RESTART}" == "true" ]]; then
  warn "Step 5/5: 跳过重启（--skip-restart）"
else
  info "Step 5/5: 重启 Gateway"
  if systemctl --user restart openclaw-gateway 2>/dev/null; then
    info "Gateway 已重启"
  else
    warn "无法重启 gateway（systemctl 不可用或未配置）"
    warn "请手动重启: systemctl --user restart openclaw-gateway"
  fi
fi

# --- 完成 ---
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║           安装完成！                      ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "已完成:"
echo "  ✓ 插件安装到 ${PLUGIN_DIR}/"
echo "  ✓ Framework patches 已应用"
echo "  ✓ Workspace 模板已部署"
echo ""
echo "还需要手动配置 ~/.openclaw/openclaw.json 的 channels.feishu 部分:"
echo ""
echo '  "channels": {'
echo '    "feishu": {'
echo '      "appId": "你的飞书应用 App ID",'
echo '      "appSecret": "你的飞书应用 App Secret",'
echo '      "allowFrom": ["*"],'
echo '      "groupAllowFrom": ["*"]'
echo '    }'
echo '  }'
echo ""
echo "配置完成后重启 gateway: systemctl --user restart openclaw-gateway"
echo ""
