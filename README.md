# Better Feishu for OpenClaw

增强版飞书/Lark 渠道插件，提供更好的消息格式和完整的飞书 API 支持。

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

---

## 第一步：检查并备份现有插件（Agent 直接执行）

先检查是否已有飞书插件：

```bash
ls -la ~/.openclaw/extensions/feishu 2>/dev/null && echo "发现已安装的飞书插件"
```

**如果已存在插件，先备份：**

```bash
# 创建带时间戳的备份
BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
mv ~/.openclaw/extensions/feishu ~/.openclaw/extensions/feishu.bak.$BACKUP_TIME
echo "已备份到 ~/.openclaw/extensions/feishu.bak.$BACKUP_TIME"
```

**向用户说明（如果有备份）：**

> 检测到你已安装飞书插件，我已将其备份到 `~/.openclaw/extensions/feishu.bak.时间戳`。
> 如果新版本有问题，可以随时回滚。继续安装吗？

---

## 第二步：复制插件文件（Agent 直接执行）

```bash
# 创建目录
mkdir -p ~/.openclaw/extensions/feishu/dist
mkdir -p ~/.openclaw/extensions/feishu/skills/feishu

# 复制文件（假设当前目录是插件根目录）
cp dist/index.js ~/.openclaw/extensions/feishu/dist/
cp openclaw.plugin.json ~/.openclaw/extensions/feishu/
cp package.json ~/.openclaw/extensions/feishu/
cp skills/feishu/SKILL.md ~/.openclaw/extensions/feishu/skills/feishu/
```

---

## 第三步：确认 SKILL.md 内容（需要用户确认）

SKILL.md 文件定义了 agent 可以使用的飞书工具和调用方式。安装后会注入到 agent 的知识库中。

**向用户说明：**

> 即将安装的飞书插件包含以下工具能力，请确认是否需要：
>
> **消息操作：**
> - `react` - 对消息添加表情回应
> - `listMessages` - 列出群聊消息
> - `pinMessage` / `unpinMessage` - Pin/取消Pin
> - `updateMessage` - 编辑消息
> - `sendAttachment` - 发送文件/图片
> - `replyInThread` - 话题回复
>
> **群聊操作：**
> - `getChatMembers` - 获取群成员
> - `getChatInfo` - 获取群信息
>
> **文档操作：**
> - `createDocument` - 创建文档
> - `readDocument` - 读取文档
> - `appendDocument` - 追加内容
> - `manageDocPermission` - 管理文档权限
>
> **表格操作：**
> - `createSpreadsheet` - 创建表格
> - `readSpreadsheet` - 读取表格
> - `writeSpreadsheet` - 写入表格
>
>
> 完整文档见 `skills/feishu/SKILL.md`。确认安装吗？

**如果用户想查看完整内容，读取并展示：**
```bash
cat skills/feishu/SKILL.md
```

---

## 第四步：获取飞书应用凭证（需要用户协作）

**向用户说明：**

> 请在飞书开放平台创建应用并提供凭证：
>
> 1. 访问 https://open.feishu.cn/app
> 2. 点击「创建企业自建应用」
> 3. 创建完成后，在「凭证与基础信息」页面找到：
>    - **App ID**（格式：`cli_xxxxxxxxxx`）
>    - **App Secret**（点击查看）
> 4. 把这两个值告诉我

**等待用户提供 `appId` 和 `appSecret`。**

---

## 第五步：配置应用权限（需要用户协作）

**向用户说明：**

> 请在飞书应用后台配置权限：
>
> 1. 进入你的应用 → 「权限管理」
> 2. 点击「批量开通」，粘贴以下 JSON：

```json
{
  "scopes": {
    "tenant": [
      "cardkit:card:read",
      "cardkit:card:write",
      "comment_sdk:comment_sdk",
      "component:url_preview",
      "contact:contact.base:readonly",
      "contact:user.employee_id:readonly",
      "contact:user.id:readonly",
      "docs:document.comment:read",
      "docs:document.comment:write_only",
      "docs:document.content:read",
      "docs:document.media:upload",
      "docs:document.subscription",
      "docs:document.subscription:read",
      "docs:document:copy",
      "docs:document:import",
      "docs:permission.member:auth",
      "docs:permission.member:create",
      "docs:permission.member:retrieve",
      "docs:permission.member:update",
      "docs:permission.setting:read",
      "docs:permission.setting:readonly",
      "docs:permission.setting:write_only",
      "docs_tool:docs_tool",
      "docx:document.block:convert",
      "docx:document:create",
      "docx:document:readonly",
      "docx:document:write_only",
      "drive:drive.metadata:readonly",
      "drive:drive.search:readonly",
      "drive:drive:version:readonly",
      "drive:file.meta.sec_label.read_only",
      "drive:file:favorite",
      "drive:file:favorite:readonly",
      "drive:file:upload",
      "drive:file:view_record:readonly",
      "event:failed_event:readonly",
      "event:ip_list",
      "im:app_feed_card:write",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.announcement:read",
      "im:chat.announcement:write_only",
      "im:chat.chat_pins:read",
      "im:chat.chat_pins:write_only",
      "im:chat.collab_plugins:read",
      "im:chat.collab_plugins:write_only",
      "im:chat.managers:write_only",
      "im:chat.members:bot_access",
      "im:chat.members:read",
      "im:chat.members:write_only",
      "im:chat.menu_tree:read",
      "im:chat.menu_tree:write_only",
      "im:chat.moderation:read",
      "im:chat.tabs:read",
      "im:chat.tabs:write_only",
      "im:chat.top_notice:write_only",
      "im:chat.widgets:read",
      "im:chat.widgets:write_only",
      "im:chat:create",
      "im:chat:delete",
      "im:chat:moderation:write_only",
      "im:chat:operate_as_owner",
      "im:chat:read",
      "im:chat:update",
      "im:message.group_at_msg:readonly",
      "im:message.group_msg",
      "im:message.p2p_msg:readonly",
      "im:message.pins:read",
      "im:message.pins:write_only",
      "im:message.reactions:read",
      "im:message.reactions:write_only",
      "im:message:readonly",
      "im:message:recall",
      "im:message:send_as_bot",
      "im:message:send_multi_depts",
      "im:message:send_multi_users",
      "im:message:send_sys_msg",
      "im:message:update",
      "im:resource",
      "im:url_preview.update",
      "im:user_agent:read",
      "sheets:spreadsheet.meta:read",
      "sheets:spreadsheet.meta:write_only",
      "sheets:spreadsheet:create",
      "sheets:spreadsheet:read",
      "sheets:spreadsheet:write_only",
      "space:document.event:read",
      "space:document:create",
      "space:document:shortcut",
    ],
    "user": [
      "docx:document:create"
    ]
  }
}
```

> 3. 完成后告诉我

---

## 第六步：启用机器人能力（需要用户协作）

**向用户说明：**

> 请启用机器人功能：
>
> 1. 进入应用 → 「添加应用能力」→ 开启「机器人」
> 2. 进入「事件订阅」：
>    - 请求方式选择 **WebSocket**（重要！）
>    - 添加事件：
>      - `im.message.receive_v1`（接收消息）
>      - `im.message.reaction.created_v1`（表情回应）
>      - `im.message.reaction.deleted_v1`（取消表情）
> 3. 完成后告诉我

---

## 第七步：发布应用（需要用户协作）

**向用户说明：**

> 请发布应用：
>
> 1. 进入「版本管理与发布」
> 2. 创建版本 → 提交审核
> 3. 如果是企业内部应用，通常自动通过
> 4. 发布后告诉我

---

## 第八步：写入 OpenClaw 配置（Agent 直接执行）

读取现有配置：
```bash
cat ~/.openclaw/openclaw.json
```

在配置中添加或更新 `channels.feishu` 部分：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "用户提供的 App ID",
      "appSecret": "用户提供的 App Secret",
      "connectionMode": "websocket",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "requireMention": true
    }
  }
}
```

**配置项说明（可询问用户偏好）：**
- `dmPolicy`: 私聊策略
  - `open` = 所有人可私聊（默认）
  - `pairing` = 需要配对码
  - `allowlist` = 仅白名单用户
- `groupPolicy`: 群聊策略
  - `open` = 响应所有群（默认）
  - `allowlist` = 仅白名单群
  - `disabled` = 禁用群聊
- `requireMention`: 群聊是否需要 @机器人（建议 `true`）

---

## 第九步：重启 Gateway（Agent 直接执行）

```bash
# 停止现有进程
pkill -f "openclaw-gateway" || true
rm -f /tmp/openclaw-gateway.lock

# 启动
cd ~/openclaw  # 或 OpenClaw 安装目录
nohup node openclaw.mjs gateway > /tmp/openclaw.log 2>&1 &

# 等待启动
sleep 5

# 检查状态
pgrep -f "openclaw-gateway" && echo "Gateway 已启动"
```

---

## 第十步：验证安装（需要用户协作）

**向用户说明：**

> 请测试机器人：
>
> 1. 在飞书中搜索你的机器人名称
> 2. 发送一条消息（如「你好」）
> 3. 告诉我机器人是否回复了

**如果不回复，检查日志：**
```bash
tail -50 /tmp/openclaw.log | grep -i "feishu\|error"
```

---

## 常见错误处理

### 错误：权限不足
→ 让用户检查飞书后台权限是否已全部开通并生效

### 错误：WebSocket 连接失败
→ 让用户确认「事件订阅」中选择的是 WebSocket 而非 HTTP

### 错误：appId/appSecret 无效
→ 让用户重新复制凭证，注意不要有多余空格

---

## 回滚到旧版本（如需要）

如果新版本有问题，可以回滚到备份版本：

```bash
# 查看可用备份
ls -la ~/.openclaw/extensions/ | grep feishu.bak

# 回滚（替换 YYYYMMDD_HHMMSS 为实际备份时间戳）
rm -rf ~/.openclaw/extensions/feishu
mv ~/.openclaw/extensions/feishu.bak.YYYYMMDD_HHMMSS ~/.openclaw/extensions/feishu

# 重启 Gateway
pkill -f "openclaw-gateway" || true
rm -f /tmp/openclaw-gateway.lock
cd ~/openclaw && nohup node openclaw.mjs gateway > /tmp/openclaw.log 2>&1 &
```

**向用户说明（如果需要回滚）：**

> 已回滚到之前的飞书插件版本。请再次测试是否正常工作。

---

## 旁听模式配置（SOUL.md 模板）

旁听模式让 agent 能看到群里所有消息，但可以选择性回复。需要在 `~/.openclaw/workspace/SOUL.md` 中配置行为规则。

**向用户说明：**

> 飞书插件支持「旁听模式」——agent 可以看到群里所有消息，但会根据规则决定是否回复。
>
> 需要在 workspace 的 SOUL.md 中添加以下配置来定义旁听行为：

**SOUL.md 旁听配置模板（让用户添加到他们的 SOUL.md）：**

```markdown
## 飞书群聊旁听规则

如果没有 @ 你，消息前面会注明 `[旁听，保持旁听不回复则输出no_reply]`。

**旁听时的行为：**
- 被 @ 时必须回复
- 旁听到感兴趣/相关的话题可以选择插话
- 不想回复时，回复 `no_reply`（不会发送到群里）
- 不要对同一条消息反复回复

**判断是否回复的参考：**
- 话题与我相关吗？
- 我有有价值的信息要补充吗？
- 这是闲聊还是需要帮助？
- 插话会不会打断别人的对话？
```

**openclaw.json 中启用旁听：**

```json
{
  "channels": {
    "feishu": {
      "passiveObserve": true,
      "requireMention": false
    }
  }
}
```

- `passiveObserve: true` - 启用旁听模式
- `requireMention: false` - 不强制 @ 才响应（配合旁听使用）

---

## 文件说明

- `dist/index.js` - 插件主代码
- `openclaw.plugin.json` - 插件元数据
- `feishu-scopes.json` - 飞书权限列表（用户可导入）
- `skills/feishu/SKILL.md` - 飞书工具使用文档（安装后 agent 可参考）
