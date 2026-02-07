# Better Feishu for OpenClaw

增强版飞书/Lark 渠道插件，提供更好的消息格式和完整的飞书 API 支持。

**作者：** [@QianruTian](https://x.com/QianruTian) | **Agent：** [mushroom](https://moltbook.com/u/mushroom)

**兼容版本：** OpenClaw 2026.2.4+

**已有飞书插件？** 安装时会自动备份现有插件，支持一键回滚。

## 功能特性

### 消息格式优化
- **≤2000 字消息**：使用 `tag:md` 富文本格式，原生支持代码块、表格等 Markdown 语法
- **>2000 字消息**：自动转为卡片格式，避免消息过长被截断
- **话题回复**：支持在话题内回复，保持讨论上下文

### 群聊旁听模式
- **旁听消息前缀**：未被 @ 的群消息会添加 `[旁听，保持旁听不回复则输出no_reply]` 前缀
- **选择性回复**：agent 可根据上下文决定是否回复旁听消息，回复 `no_reply` 则不发送
- **需配合 SOUL.md**：在 workspace 的 SOUL.md 中配置旁听行为规则（见下方模板）

### 飞书 API 集成
- **表情回应**：对消息添加/移除表情（THUMBSUP、SMILE 等 50+ 表情）
- **消息操作**：Pin、编辑消息
- **群聊管理**：查询群成员、群信息
- **文档操作**：创建、读取、追加文档内容，管理文档权限
- **表格操作**：创建、读取、写入电子表格
- **附件自动下载**：飞书消息中的图片、附件自动下载并完成读取

---

# 安装指南

本文档供 OpenClaw agent 阅读，用于引导用户完成安装配置。

**不要使用子 agent 执行安装！** 安装过程需要与用户协作，子 agent 无法与用户交互。请在主对话中执行。

---

## 第一步：安装前沟通（需要用户确认）

**向用户发送以下内容确认：**

> 安装飞书插件前，请确认：
>
> **准备工作：**
> - 有飞书开放平台账号（https://open.feishu.cn）
> - 有权限创建企业自建应用
>
> **推荐配置（直接采用，除非你有特殊需求）：**
> - 私聊：所有人可私聊
> - 群聊：响应所有群，需要 @机器人
> - 旁听模式：启用（能看到群里所有消息，可选择性回复）
> - Workspace 模板：安装（包含表情规则、任务管理、工具速查等）
>
> *模板只会追加内容到你现有的 SOUL.md、AGENTS.md 等文件，不会覆盖你已有的配置。*
>
> 确认开始安装吗？如果有特殊需求可以告诉我。

**用户确认后，使用以下默认配置（除非用户明确提出修改）：**
- `dmPolicy`: `open`
- `groupPolicy`: `open`
- `requireMention`: `true`
- `passiveObserve`: `true`
- 安装 workspace 模板: `true`

---

## 第二步：获取插件 + 备份 + 安装（Agent 直接执行）

```bash
# 1. Clone 插件仓库
cd /tmp
rm -rf better-feishu-for-openclaw
git clone https://github.com/fleurytian/better-feishu-for-openclaw.git

# 2. 检查并备份现有插件
if [ -d ~/.openclaw/extensions/feishu ]; then
  BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
  mv ~/.openclaw/extensions/feishu ~/.openclaw/extensions/feishu.bak.$BACKUP_TIME
  echo "已备份到 ~/.openclaw/extensions/feishu.bak.$BACKUP_TIME"
fi

# 3. 安装新插件
mkdir -p ~/.openclaw/extensions/feishu/dist
mkdir -p ~/.openclaw/extensions/feishu/skills/feishu
cp /tmp/better-feishu-for-openclaw/dist/index.js ~/.openclaw/extensions/feishu/dist/
cp /tmp/better-feishu-for-openclaw/openclaw.plugin.json ~/.openclaw/extensions/feishu/
cp /tmp/better-feishu-for-openclaw/package.json ~/.openclaw/extensions/feishu/
cp /tmp/better-feishu-for-openclaw/skills/feishu/SKILL.md ~/.openclaw/extensions/feishu/skills/feishu/

echo "插件文件安装完成"
```

---

## 第三步：飞书后台配置 + 获取凭证（需要用户协作）

**向用户发送以下完整指引，让用户一次性完成所有飞书后台操作：**

> 请在飞书开放平台完成以下配置（按顺序操作）：
>
> **Step 1: 创建应用**
> 1. 访问 https://open.feishu.cn/app
> 2. 点击「创建企业自建应用」
> 3. 填写应用名称和描述
>
> **Step 2: 配置权限**
> 1. 进入应用 →「权限管理」
> 2. 点击「批量开通」，粘贴以下 JSON：
>
> ```json
> {
>   "scopes": {
>     "tenant": [
>       "cardkit:card:read", "cardkit:card:write", "comment_sdk:comment_sdk",
>       "component:url_preview", "contact:contact.base:readonly",
>       "contact:user.employee_id:readonly", "contact:user.id:readonly",
>       "docs:document.comment:read", "docs:document.comment:write_only",
>       "docs:document.content:read", "docs:document.media:upload",
>       "docs:document.subscription", "docs:document.subscription:read",
>       "docs:document:copy", "docs:document:import",
>       "docs:permission.member:auth", "docs:permission.member:create",
>       "docs:permission.member:retrieve", "docs:permission.member:update",
>       "docs:permission.setting:read", "docs:permission.setting:readonly",
>       "docs:permission.setting:write_only", "docs_tool:docs_tool",
>       "docx:document.block:convert", "docx:document:create",
>       "docx:document:readonly", "docx:document:write_only",
>       "drive:drive.metadata:readonly", "drive:drive.search:readonly",
>       "drive:drive:version:readonly", "drive:file.meta.sec_label.read_only",
>       "drive:file:favorite", "drive:file:favorite:readonly",
>       "drive:file:upload", "drive:file:view_record:readonly",
>       "event:failed_event:readonly", "event:ip_list",
>       "im:app_feed_card:write", "im:chat.access_event.bot_p2p_chat:read",
>       "im:chat.announcement:read", "im:chat.announcement:write_only",
>       "im:chat.chat_pins:read", "im:chat.chat_pins:write_only",
>       "im:chat.collab_plugins:read", "im:chat.collab_plugins:write_only",
>       "im:chat.managers:write_only", "im:chat.members:bot_access",
>       "im:chat.members:read", "im:chat.members:write_only",
>       "im:chat.menu_tree:read", "im:chat.menu_tree:write_only",
>       "im:chat.moderation:read", "im:chat.tabs:read",
>       "im:chat.tabs:write_only", "im:chat.top_notice:write_only",
>       "im:chat.widgets:read", "im:chat.widgets:write_only",
>       "im:chat:create", "im:chat:delete", "im:chat:moderation:write_only",
>       "im:chat:operate_as_owner", "im:chat:read", "im:chat:update",
>       "im:message.group_at_msg:readonly", "im:message.group_msg",
>       "im:message.p2p_msg:readonly", "im:message.pins:read",
>       "im:message.pins:write_only", "im:message.reactions:read",
>       "im:message.reactions:write_only", "im:message:readonly",
>       "im:message:recall", "im:message:send_as_bot",
>       "im:message:send_multi_depts", "im:message:send_multi_users",
>       "im:message:send_sys_msg", "im:message:update", "im:resource",
>       "im:url_preview.update", "im:user_agent:read",
>       "sheets:spreadsheet.meta:read", "sheets:spreadsheet.meta:write_only",
>       "sheets:spreadsheet:create", "sheets:spreadsheet:read",
>       "sheets:spreadsheet:write_only", "space:document.event:read",
>       "space:document:create", "space:document:shortcut"
>     ],
>     "user": ["docx:document:create"]
>   }
> }
> ```
>
> **Step 3: 启用机器人**
> 1. 进入「添加应用能力」→ 开启「机器人」
> 2. 进入「事件订阅」：
>    - 请求方式选择 **WebSocket**（重要！）
>    - 添加事件：`im.message.receive_v1`、`im.message.reaction.created_v1`、`im.message.reaction.deleted_v1`
>
> **Step 4: 发布应用**
> 1. 进入「版本管理与发布」
> 2. 创建版本 → 提交审核（企业内部应用通常自动通过）
>
> **Step 5: 获取凭证**
> 1. 回到「凭证与基础信息」页面
> 2. 复制 **App ID**（格式：`cli_xxxxxxxxxx`）和 **App Secret**
>
> ---
>
> 完成后，请把 **App ID** 和 **App Secret** 发给我。

**等待用户提供 `appId` 和 `appSecret`。**

---

## 第四步：写入配置 + 模板 + 重启（Agent 直接执行）

**1. 写入 openclaw.json 配置**

根据第一步收集的用户偏好，生成配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "用户提供的 App ID",
      "appSecret": "用户提供的 App Secret",
      "connectionMode": "websocket",
      "dmPolicy": "用户选择的私聊策略",
      "groupPolicy": "用户选择的群聊策略",
      "requireMention": true,
      "passiveObserve": true或false,
      "sendMarkdownAsCard": false
    }
  }
}
```

读取并更新 `~/.openclaw/openclaw.json`。

**2. 配置 workspace 模板（如果用户需要）**

将模板内容合并到用户的 workspace 文件：

```bash
# 读取模板
cat /tmp/better-feishu-for-openclaw/templates/SOUL.md
cat /tmp/better-feishu-for-openclaw/templates/AGENTS.md
cat /tmp/better-feishu-for-openclaw/templates/TOOLS.md
cat /tmp/better-feishu-for-openclaw/templates/USER.md
```

将模板内容追加或合并到：
- `~/.openclaw/workspace/SOUL.md`
- `~/.openclaw/workspace/AGENTS.md`
- `~/.openclaw/workspace/TOOLS.md`
- `~/.openclaw/workspace/USER.md`

**3. 重启 Gateway**

```bash
pkill -f "openclaw-gateway" || true
rm -f /tmp/openclaw-gateway.lock
cd ~/openclaw && nohup node openclaw.mjs gateway > /tmp/openclaw.log 2>&1 &
sleep 5
pgrep -f "openclaw-gateway" && echo "Gateway 已启动，飞书插件安装完成！"
```

**向用户确认：**

> 飞书插件已安装完成！你现在可以在飞书中搜索机器人名称，发送消息测试。

---

## 自检步骤（Agent 直接执行）

安装完成后，执行以下自检：

```bash
# 1. 检查插件文件是否完整
echo "=== 检查插件文件 ==="
ls -la ~/.openclaw/extensions/feishu/dist/index.js && echo "✓ index.js 存在" || echo "✗ index.js 缺失"
ls -la ~/.openclaw/extensions/feishu/openclaw.plugin.json && echo "✓ plugin.json 存在" || echo "✗ plugin.json 缺失"
ls -la ~/.openclaw/extensions/feishu/skills/feishu/SKILL.md && echo "✓ SKILL.md 存在" || echo "✗ SKILL.md 缺失"

# 2. 检查配置
echo "=== 检查 openclaw.json 配置 ==="
grep -A 10 '"feishu"' ~/.openclaw/openclaw.json

# 3. 检查 Gateway 进程
echo "=== 检查 Gateway 进程 ==="
pgrep -f "openclaw-gateway" && echo "✓ Gateway 运行中" || echo "✗ Gateway 未运行"

# 4. 检查最近日志
echo "=== 最近日志（飞书相关）==="
tail -30 /tmp/openclaw.log | grep -i "feishu\|websocket\|error" | tail -10
```

**根据自检结果处理：**

| 问题 | 处理方法 |
|------|----------|
| index.js 缺失 | 重新执行第二步的安装命令 |
| 配置中没有 feishu | 重新执行第四步写入配置 |
| Gateway 未运行 | 执行重启命令 |
| 日志有错误 | 见下方常见错误处理 |

---

## 常见错误处理

### 错误：`invalid app_id` 或 `invalid app_secret`

**诊断：**
```bash
grep -E "appId|appSecret" ~/.openclaw/openclaw.json
```

**处理：**
1. 让用户重新复制凭证（注意不要有多余空格或换行）
2. 更新 `~/.openclaw/openclaw.json` 中的值
3. 重启 Gateway

---

### 错误：`websocket connection failed` 或连接超时

**诊断：**
```bash
grep "connectionMode" ~/.openclaw/openclaw.json
```

**处理：**
1. 确认配置中 `connectionMode` 是 `websocket`
2. 让用户检查飞书后台「事件订阅」是否选择了 WebSocket（不是 HTTP）
3. 让用户检查应用是否已发布上线

---

### 错误：`permission denied` 或权限不足

**诊断：** 让用户在飞书后台「权限管理」页面截图

**处理：**
1. 让用户重新执行批量开通权限（第三步的 JSON）
2. 确认权限状态是「已开通」而非「待审核」
3. 如果是新开通的权限，可能需要重新发布应用版本

---

### 错误：Gateway 启动后立即退出

**诊断：**
```bash
cat /tmp/openclaw.log | tail -50
```

**处理：**
1. 检查 `openclaw.json` 是否有 JSON 语法错误（多余逗号、缺少引号等）
2. 用 `cat ~/.openclaw/openclaw.json | python3 -m json.tool` 验证 JSON 格式
3. 修复后重启 Gateway

---

### 错误：机器人不回复消息

**诊断：**
```bash
# 检查是否收到消息
tail -100 /tmp/openclaw.log | grep -i "receive\|message"
```

**处理：**
1. 如果没有收到消息日志 → WebSocket 连接问题，见上方
2. 如果收到但没回复 → 检查 `requireMention` 配置，群聊中是否 @了机器人
3. 让用户尝试私聊机器人测试

---

### 错误：表情 reaction 失败

**诊断：**
```bash
tail -50 /tmp/openclaw.log | grep -i "react\|emoji"
```

**处理：**
1. 确认 `im:message.reactions:write_only` 权限已开通
2. 确认 emoji_type 拼写正确（大小写敏感，如 `THUMBSUP` 不是 `thumbsup`）

---

## 回滚到旧版本（如需要）

```bash
# 查看可用备份
ls -la ~/.openclaw/extensions/ | grep feishu.bak

# 回滚（替换时间戳）
rm -rf ~/.openclaw/extensions/feishu
mv ~/.openclaw/extensions/feishu.bak.YYYYMMDD_HHMMSS ~/.openclaw/extensions/feishu

# 重启 Gateway
pkill -f "openclaw-gateway" || true
rm -f /tmp/openclaw-gateway.lock
cd ~/openclaw && nohup node openclaw.mjs gateway > /tmp/openclaw.log 2>&1 &
```

---

## 文件说明

- `dist/index.js` - 插件主代码
- `openclaw.plugin.json` - 插件元数据
- `feishu-scopes.json` - 飞书权限列表（用户可导入）
- `skills/feishu/SKILL.md` - 飞书工具使用文档（安装后 agent 可参考）
- `templates/` - workspace 配置模板：
  - `SOUL.md` - 行为准则模板（飞书表情、旁听规则、不同群的回复积极度）
  - `AGENTS.md` - 工作方法模板（任务管理、文档工作流）
  - `TOOLS.md` - 工具备忘模板（飞书 action 速查表）
  - `USER.md` - 联系人与群聊模板（user_id 记录、群聊分类）

**模板使用方式：** 将 `templates/` 中的内容合并到用户的 `~/.openclaw/workspace/` 对应文件中。

**关于 USER.md 群聊分类：**
- 记录群聊时标注「工作群」或「朋友群」
- SOUL.md 中的回复积极度规则会根据群聊性质调整行为
- 工作群更积极响应，朋友群更轻松随意
