---
name: feishu
description: >
  飞书/Lark 消息渠道工具集。通过 message 工具调用飞书 API，支持表情回应、消息操作、
  群聊查询、文档/表格创建与编辑、云空间搜索与上传。
metadata: {"openclaw":{"emoji":"\U0001f4ce"}}
---

# 飞书工具参考

所有飞书操作都通过 `message` 工具调用，核心参数是 `action`。

## 工具调用格式（重要）

**正确调用方式：** 将下面示例中的 JSON 对象作为 `message` 工具的参数直接传入，参数需要展开到顶层。

```
// 正确 ✓ - 参数展开到顶层
message(action="react", messageId="om_xxx", emoji="SMILE")

// 错误 ✗ - 不要把参数嵌套成字符串
message(path='{"action": "react", "messageId": "om_xxx", ...}')
```

## 核心规则：`to` vs `chatId`

**这是最常犯的错误，必须记住：**

- **`to`（格式 `chat:oc_xxx`）** — 只用于框架原生 action：`send`、`reply`、`react`、`sendAttachment`
- **`chatId`（格式 `oc_xxx`，不带 `chat:` 前缀）** — 用于所有其他飞书自定义 action
- **自定义 action 绝对不能传 `to` 参数**，否则框架报错

群消息正文开头有 `[chatId=oc_xxx sender=xxx]`，从这里取 `oc_xxx`：
- 给 react/sendAttachment 用时，拼成 `chat:oc_xxx` 传给 `to`
- 给其他 action 用时，直接传 `oc_xxx` 给 `chatId`

## 文件分享规则

**飞书渠道用户看不到 agent 本地文件！** 分享时必须选择以下方式：

1. **文件附件**（推荐普通文件）：`sendAttachment` action，把本地文件路径传给 `path`
2. **飞书文档/表格**（推荐结构化内容）：
   - 用 `createDocument` / `createSpreadsheet` 创建
   - **必须**用 `appendDocument` / `writeSpreadsheet` 写入内容
   - **必须**用 `manageDocPermission` 给用户开权限
   - 再把文档链接发给用户

**禁止：** 只发本地文件路径 / 创建文档后不开权限 / 只发文档 ID 不生成链接

## 表情 Reaction

```json
{ "action": "react", "to": "chat:oc_xxx", "messageId": "om_xxx", "emoji": "THUMBSUP" }
```

取消表情：加 `"reactionId": "xxx"` 和 `"remove": true`

**emoji_type 清单（大小写敏感）：**

| 场景 | emoji_type |
|------|-----------|
| 加油 | MUSCLE, SaluteFace, STRIVE, GoGoGo |
| 尴尬 | FACEPALM, LOL, NOSEPICK, DULL, GLANCE, INNOCENTSMILE, ENOUGH, SWEAT, SLIGHT |
| 心有灵犀 | SMIRK, FullMoonFace |
| 聪明 | WITTY, SMART |
| 反应不过来 | SCOWL, FROWN, WHAT |
| 深深赞同 | FINGERHEART, APPLAUSE, SMOOCH, DROOL, HIGHFIVE, JIAYI, THUMBSUP |
| 被夸 | PROUD, WINK, CRY, COMFORT |
| 惊讶 | SHOCKED, PETRIFIED, TERROR |
| 疲惫 | YAWN, SICK, Sigh |
| 工作中 | Typing, OneSecond, OnIt |
| 吃饭 | EatingFood |
| 搞定 | DONE |
| 不同意 | No, CrossMark, MinusOne, POOP, ClownFace |

## 消息操作

```json
// 列消息
{ "action": "listMessages", "chatId": "oc_xxx", "pageSize": 20 }

// Pin
{ "action": "pinMessage", "messageId": "om_xxx" }

// 取消Pin
{ "action": "unpinMessage", "messageId": "om_xxx" }

// 撤回
{ "action": "recallMessage", "messageId": "om_xxx" }

// 编辑
{ "action": "updateMessage", "messageId": "om_xxx", "content": "修改后的内容" }

// 发文件/图片（框架原生 action，用 to）
{ "action": "sendAttachment", "to": "chat:oc_xxx", "path": "/tmp/file.png" }
```

## 话题回复 (Thread)

在飞书中以话题形式回复消息，会创建一个独立的讨论串。

```json
// 话题形式回复（会创建话题或在已有话题中回复）
{ "action": "replyInThread", "messageId": "om_xxx", "content": "这是话题回复内容" }

// 指定消息类型（可选，默认 text）
{ "action": "replyInThread", "messageId": "om_xxx", "content": "回复内容", "msgType": "text" }

// 获取话题内的所有消息（threadId 从 replyInThread 响应或 listMessages 返回的消息中获取）
{ "action": "listThreadMessages", "threadId": "omt_xxx", "pageSize": 20 }
```

**返回值：**
- `replyInThread` 返回 `{ ok: true, messageId: "om_xxx", threadId: "omt_xxx" }`
- `listThreadMessages` 返回话题内所有消息列表

**使用场景：**
- 针对某条消息展开深入讨论
- 避免刷屏，将相关讨论集中在话题内
- 回复已是话题的消息会自动加入该话题

## 群聊查询

```json
// 查群成员
{ "action": "getChatMembers", "chatId": "oc_xxx" }

// 查群详情
{ "action": "getChatInfo", "chatId": "oc_xxx" }
```

## 文档

**⚠️ 重要：创建文档后必须开权限，否则用户打不开！**

**完整工作流（创建 → 写入 → 开权限 → 发链接）：**

```json
// 第1步：创建文档（返回 documentId）
{ "action": "createDocument", "title": "标题" }
// 返回: { "documentId": "doxcnXXX", "url": "https://xxx.feishu.cn/docx/doxcnXXX" }

// 第2步：写入内容
{ "action": "appendDocument", "documentId": "doxcnXXX", "content": "# 内容\n正文..." }

// 第3步：给用户开权限（用消息中的 sender 作为 memberId）
{ "action": "manageDocPermission", "docToken": "doxcnXXX", "action": "add", "memberId": "ou_xxx", "perm": "view" }
// perm 可选: "view"（只读）, "edit"（可编辑）

// 第4步：把链接发给用户
// 直接发送 url: https://xxx.feishu.cn/docx/doxcnXXX
```

**单独的 action：**

```json
// 读取文档
{ "action": "readDocument", "documentId": "doxcnXXX" }

// 查看当前权限
{ "action": "manageDocPermission", "docToken": "doxcnXXX", "action": "list" }
```

**常见错误：** 创建文档后直接发链接给用户，用户点开提示「无权限」→ 忘了第3步开权限！

## 电子表格

```json
// 创建
{ "action": "createSpreadsheet", "title": "表格名" }

// 读取（sheetId 是工作表名或 ID，range 如 "A1:C10"）
{ "action": "readSpreadsheet", "spreadsheetToken": "shtcnXXX", "sheetId": "Sheet1", "range": "A1:C10" }

// 写入（values 是二维数组）
{ "action": "writeSpreadsheet", "spreadsheetToken": "shtcnXXX", "sheetId": "Sheet1", "range": "A1", "values": [["姓名","分数"],["张三",95]] }
```

## 云空间

```json
// 搜索文件
{ "action": "searchDrive", "query": "周报" }

// 上传文件
{ "action": "uploadFile", "path": "/tmp/report.pdf", "parentToken": "fldcnXXX" }
```

## 消息附件（自动下载）

用户发送图片/文件时，系统会**自动下载**到本地：
- **单聊**：下载到 `workspace/chatdownload/` 目录
- **群聊**：下载到 `/tmp/` 目录

下载后的文件路径会自动设置到 `MediaPaths`，agent 可直接用 `read` 工具查看。
