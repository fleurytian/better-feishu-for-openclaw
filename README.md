# Better Feishu for OpenClaw

增强版飞书/Lark 渠道插件，提供更好的消息格式和完整的飞书 API 支持。

**作者：** [@QianruTian](https://x.com/QianruTian) | **Agent：** [mushroom](https://moltbook.com/u/mushroom)

**兼容版本：** OpenClaw 2026.2.4+（推荐 2026.2.26+）

**已有飞书插件？** 安装时会自动备份现有插件，支持一键回滚。

> **飞书 API 完整参考** → [`skills/feishu/SKILL.md`](skills/feishu/SKILL.md)
>
> 不需要安装整个插件也可以参考这份文档。包含所有 action 的调用格式、参数说明和完整工作流示例（表情回应、文档、电子表格、多维表格、话题帖子、云空间等）。

## 功能特性

### 消息格式优化
- **≤2000 字消息**：使用 `tag:md` 富文本格式，原生支持代码块、表格等 Markdown 语法
- **>2000 字消息**：自动转为卡片格式，避免消息过长被截断
- **话题回复**：支持在话题内回复，保持讨论上下文
- **配合 Block Streaming**：OpenClaw 2026.2.26+ 支持 `blockStreamingDefault: "on"`，LLM 输出会分块递送，体验更好

### 群聊旁听模式
- **自主旁听（autonomous）**：未被 @ 的群消息会添加 `[旁听]` 前缀，agent 自行判断是否回复，回复 `NO_REPLY` 则不发送
- **完全旁听（full，推荐）**：群消息**不触发 LLM 调用**（零成本），缓存在内存 buffer 中；被 @ 时 buffer 自动 flush 为上下文注入（最多 50 条）
- **需配合 SOUL.md**：在 workspace 的 SOUL.md 中配置旁听行为规则（见下方模板）
- **必须权限**：飞书应用需开通 `im:message.group_msg` 权限（接收群内所有消息），仅有 `im:message.group_at_msg:readonly` 无法接收未 @ 的消息，旁听模式将不生效

### 飞书 API 集成
- **表情回应**：对消息添加/移除表情（THUMBSUP、SMILE 等 50+ 表情）
- **@ 提及成员**：在消息中 @ 群聊成员（机器人除外，飞书群聊中机器人收不到其他机器人的消息）
- **发送图片和文件**：通过附件形式发送本地图片、文档等文件
- **消息操作**：Pin 消息
- **群聊管理**：查询群成员、群信息
- **文档操作**：创建、读取、追加文档内容（支持图片插入），管理文档权限
- **表格操作**：创建、读取、写入电子表格
- **多维表格**：创建多维表格、管理字段、CRUD 记录（自动清理默认空数据和字段）
- **话题帖子**：在话题群中发起新话题帖子
- **附件自动下载**：飞书消息中的图片、附件自动下载并完成读取

### 联系人记忆
- **自动识别发送者**：从消息中提取 `sender` (user_id)，关联到 USER.md 中的联系人
- **群聊分类**：支持将群聊标记为「工作群」或「朋友群」，配合 SOUL.md 调整回复积极度
- **联系人记录模板**：USER.md 模板帮助记录联系人信息和群聊分类

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
- `observeMode`: `"full"`（完全旁听，零 LLM 成本）
- 安装 workspace 模板: `true`

---

## 第二步：获取插件 + 一键安装（Agent 直接执行）

```bash
# 1. Clone 插件仓库
cd /tmp
rm -rf better-feishu-for-openclaw
git clone https://github.com/fleurytian/better-feishu-for-openclaw.git

# 2. 一键安装（备份旧插件 + 安装文件 + 打补丁 + 注入 workspace 模板）
bash /tmp/better-feishu-for-openclaw/setup.sh --openclaw-dir ~/openclaw
```

**setup.sh 会自动完成：**
1. 备份现有飞书插件（如有）
2. 安装插件文件到 `~/.openclaw/extensions/feishu/`
3. 给 OpenClaw 核心打运行时补丁（修复 target 处理 + 注入飞书交互规则）
4. 将飞书相关模板注入到 workspace 的 SOUL.md、TOOLS.md、AGENTS.md、USER.md

*模板注入是幂等的 — 重复运行 setup.sh 只会更新已有内容，不会重复添加。*

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
>       "sheets:spreadsheet:write_only",
>       "bitable:app", "bitable:app:readonly",
>       "space:document.event:read",
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
      "allowFrom": ["*"],
      "groupAllowFrom": ["*"],
      "requireMention": true,
      "passiveObserve": true,
      "observeMode": "full",
      "sendMarkdownAsCard": false
    }
  }
}
```

**⚠️ OpenClaw 2026.2.26+ 要求：** `dmPolicy: "open"` 的 channel 必须显式声明 `allowFrom: ["*"]` 和 `groupAllowFrom: ["*"]`，否则启动报 config validation 错误。

读取并更新 `~/.openclaw/openclaw.json`。

**2. workspace 模板已在第二步由 setup.sh 自动注入。** 如需手动重新注入：

```bash
python3 /tmp/better-feishu-for-openclaw/scripts/inject-templates.py \
    --workspace-dir ~/.openclaw/workspace \
    --templates-dir /tmp/better-feishu-for-openclaw/templates
```

**3. 重启 Gateway**

```bash
systemctl --user restart openclaw-gateway
echo "Gateway 已重启，飞书插件安装完成！"
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

# 3. 检查 Gateway 服务
echo "=== 检查 Gateway 服务 ==="
systemctl --user is-active openclaw-gateway && echo "✓ Gateway 运行中" || echo "✗ Gateway 未运行"

# 4. 检查最近日志
echo "=== 最近日志（飞书相关）==="
journalctl --user -u openclaw-gateway --no-pager -n 30 | grep -i "feishu\|websocket\|error" | tail -10
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
journalctl --user -u openclaw-gateway --no-pager -n 50
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
journalctl --user -u openclaw-gateway --no-pager -n 100 | grep -i "receive\|message"
```

**处理：**
1. 如果没有收到消息日志 → WebSocket 连接问题，见上方
2. 如果收到但没回复 → 检查 `requireMention` 配置，群聊中是否 @了机器人
3. 让用户尝试私聊机器人测试

---

### 错误：旁听模式不生效（群里未 @ 的消息机器人看不到）

**诊断清单：**

1. **检查飞书权限** — 必须开通 `im:message.group_msg`（接收群内所有消息）。仅有 `im:message.group_at_msg:readonly` 只能收到 @ 机器人的消息，旁听模式无法工作。
2. **检查配置** — `openclaw.json` 中 `channels.feishu.passiveObserve` 必须为 `true`：
   ```bash
   grep passiveObserve ~/.openclaw/openclaw.json
   ```
3. **检查 SOUL.md** — workspace 中需要有旁听行为规则，agent 才知道何时回复 `NO_REPLY`。运行安装指南中的模板合并步骤。
4. **检查插件版本** — 确保 `openclaw.plugin.json` 的 `configSchema` 中声明了 `passiveObserve` 字段。旧版本遗漏了此声明，会导致框架 AJV 验证报错。

---

### 错误：表情 reaction 失败

**诊断：**
```bash
journalctl --user -u openclaw-gateway --no-pager -n 50 | grep -i "react\|emoji"
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
systemctl --user restart openclaw-gateway
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

- `scripts/inject-templates.py` - 幂等模板注入脚本
- `setup.sh` - 一键安装脚本（安装+补丁+模板注入）

**模板使用方式：** `setup.sh` 自动注入。模板内容用 `<!-- [better-feishu] -->` markers 包裹，支持幂等更新。

**关于 USER.md 群聊分类：**
- 记录群聊时标注「工作群」或「朋友群」
- SOUL.md 中的回复积极度规则会根据群聊性质调整行为
- 工作群更积极响应，朋友群更轻松随意

---

## 升级指南

如果已经安装了旧版本，直接重新运行 setup.sh：

```bash
# 1. 拉取最新版本
cd /tmp
rm -rf better-feishu-for-openclaw
git clone https://github.com/fleurytian/better-feishu-for-openclaw.git

# 2. 一键升级（备份 + 安装 + 打补丁 + 更新模板）
bash /tmp/better-feishu-for-openclaw/setup.sh --openclaw-dir ~/openclaw

# 3. 重启 gateway
systemctl --user restart openclaw-gateway
```

<details>
<summary>手动升级（如果不想用 setup.sh）</summary>

```bash
# 备份当前版本
BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
cp ~/.openclaw/extensions/feishu/dist/index.js ~/.openclaw/extensions/feishu/dist/index.js.bak.$BACKUP_TIME

# 3. 更新文件
cp /tmp/better-feishu-for-openclaw/dist/index.js ~/.openclaw/extensions/feishu/dist/
cp /tmp/better-feishu-for-openclaw/openclaw.plugin.json ~/.openclaw/extensions/feishu/
cp /tmp/better-feishu-for-openclaw/skills/feishu/SKILL.md ~/.openclaw/extensions/feishu/skills/feishu/

# 4. 重启 Gateway
systemctl --user restart openclaw-gateway
```

**手动升级后检查清单：**
- [ ] `openclaw.json` 中 feishu channel 是否有 `allowFrom: ["*"]` 和 `groupAllowFrom: ["*"]`（v2.26+ 必需）
- [ ] 是否需要添加 `observeMode: "full"`（推荐，零成本旁听）
- [ ] 运行时 patch 是否需要重新应用
- [ ] workspace 模板是否有新内容需要合并
```
</details>

---

## Changelog

### 2026-02-28 (v2)

**多维表格、话题帖子、文档图片**

- **新增多维表格 (Bitable) 全生命周期** — `createBitable`（自动清理默认空记录和默认字段）、`addBitableField`（支持 9 种字段类型）、`listBitableTables`（含字段 schema）、`listBitableRecords`/`createBitableRecord`/`updateBitableRecord`/`deleteBitableRecord`
- **新增话题帖子** — `createTopicPost`：在话题群中发起新话题帖子（与 `replyInThread` 回复讨论串不同）
- **文档支持图片插入** — `appendDocument` 现在识别 `![alt](src)` markdown 图片语法，自动上传本地文件或远程 URL 到飞书文档，上传失败 fallback 为文字链接
- **表格写入可靠性提升** — 单元格逐个顺序写入（替换并发 Promise.all），避免内容错位/丢失
- **表格 separator 检测修复** — 放宽分隔行检测逻辑，兼容更多 markdown 表格格式
- **新增 `bitable:app` 权限声明** — feishu-scopes.json 和安装指引中补充多维表格所需权限
- **SKILL.md 更新** — 新增多维表格完整工作流、话题帖子文档、图片插入说明
- **templates/TOOLS.md 更新** — 新增 action 注册到 target 规则表

### 2026-02-28

**一键安装 (setup.sh)**

- **新增 `setup.sh`** — 一键完成：备份旧插件 → 安装文件 → 打补丁 → 注入 workspace 模板
- **新增 `scripts/inject-templates.py`** — 幂等模板注入脚本，用 `<!-- [better-feishu] -->` markers 标记，支持重复运行更新
- **更新 workspace 模板** — 对齐蘑菇实际 workspace：完整 emoji 表情清单（13 场景）、action target 规则、旁听模式配置、文件分享规则、文档工作流
- **更新 patches** — `patch-channel-target.py` 和 `patch-feishu-messaging.py` 支持 `--openclaw-dir` 参数
- **升级指南简化** — 升级只需 `git clone` + `bash setup.sh`

### 2026-02-27

**完全旁听模式 (observeMode: "full")**

- **新增 `observeMode` 配置项** — 支持 `"autonomous"`（自主旁听，每条消息触发 LLM）和 `"full"`（完全旁听，零 LLM 调用，@ 时批量注入）两种模式
- **openclaw.plugin.json 补充 configSchema** — 添加 `observeMode` 字段声明，避免框架 AJV 验证报错

**OpenClaw 2026.2.26 兼容性**

- **allowFrom/groupAllowFrom 必须显式声明** — v2.26 要求 `dmPolicy: "open"` 的 channel 必须显式声明 `allowFrom: ["*"]` 和 `groupAllowFrom: ["*"]`
- **更新 gateway 管理命令** — 统一使用 `systemctl --user restart openclaw-gateway`（不再使用 pkill + nohup）
- **更新日志命令** — 统一使用 `journalctl --user -u openclaw-gateway`

**文档更新**

- **新增升级指南** — 从旧版本升级的完整步骤和检查清单
- **更新 SKILL.md** — 同步最新的 action 参数说明和 target 规则
- **更新 workspace 模板** — SOUL.md 新增进度同步规则、markdown 使用指南、完整表情清单；TOOLS.md 新增旁听模式文档和密钥管理；AGENTS.md 新增 memory_search 黄金规则和 NOW.md 机制
- **更新 Known Issues** — 修正 patch 目标文件路径

### 2026-02-11

**重大修复：消除 agent 幻觉问题**

- **修复 18 个未接线的 action handler** — 之前 `handleAction` 只实现了 20/38 个声明的 action，调用未接线的 action 会直接报错 `"Action X is not supported for feishu"`。现已全部接线到对应的 helper 函数（群聊管理、多维表格、知识库、AI 服务、文件下载等）。
- **精简 messageToolHints** — 只保留实际在用的功能（react、消息管理、群聊查询、文档、电子表格、云空间），移除未启用权限的 action 声明（多维表格、知识库、AI 服务等），防止 agent 尝试调用不可用的 API。
- **补充遗漏的 action 文档** — `listThreadMessages`（话题消息列表）和 `replyInThread`（话题内回复）已有实现但未在 hints 中声明，现已补充。

**其他修复**

- **修复 markdownToPost 空段落导致 API 400 错误** — 飞书 post 格式不允许空段落（会触发 error code 230001），现在跳过空段落而非插入空 text 元素。
- **修复 sendText 定时任务发送格式** — 定时任务发送消息现在使用 post 富文本格式而非纯 text，保持格式一致。

---

## Known Issues

### `Action readDocument does not accept a target` (OpenClaw 框架 bug)

**症状：** 调用 `readDocument`、`appendDocument`、`createDocument` 等飞书自定义 action 时报错 `"Action xxx does not accept a target"`，即使 agent 没有传 `target` 参数。

**根因：** OpenClaw 框架的 `actionRequiresTarget()` 函数对未注册在 `MESSAGE_ACTION_TARGET_MODE` 中的 action 返回 `true`（因为 `undefined !== "none"` = `true`），导致框架从当前会话 context 自动注入 `target`，然后 `applyTargetToParams()` 因 mode 为 `"none"` 而抛出错误。

**影响版本：** OpenClaw 2026.2.4 ~ 2026.2.26（截至目前未修复）

**解决方案：** 应用以下两个运行时 patch：

```bash
# patch-action-spec.py — 注册所有飞书自定义 action 到 MESSAGE_ACTION_TARGET_MODE
python3 patch-action-spec.py ~/openclaw/dist/infra/outbound/message-action-spec.js

# patch-channel-target.py — 安全网：未知 action 传了 target 时静默忽略而非报错
python3 patch-channel-target.py ~/openclaw/dist/infra/outbound/channel-target.js

# 重启 gateway 生效
systemctl --user restart openclaw-gateway
```

**注意：**
- 每次 OpenClaw 升级后需重新应用这些 patch（dist 目录会被覆盖）
- patch 脚本是幂等的，重复执行不会出错
- dist 文件名可能因版本不同而变化，如果上述路径不存在，用 `grep -rl "actionRequiresTarget" ~/openclaw/dist/` 查找目标文件
