# TOOLS.md - 工具备忘（飞书相关部分模板）

> 将此内容合并到你的 `~/.openclaw/workspace/TOOLS.md`

## 飞书消息工具 (message)

`message` 工具是飞书操作的核心，通过 `action` 参数决定行为。

### 基础消息

| action | 用途 | 关键参数 |
|--------|------|----------|
| `send` | 发送消息 | `to: "chat:oc_xxx"`, `text: "内容"` |
| `reply` | 回复消息 | `to: "chat:oc_xxx"`, `messageId: "om_xxx"`, `text: "内容"` |
| `sendAttachment` | 发送文件/图片 | `to: "chat:oc_xxx"`, `path: "/本地文件路径"` |

### 表情回应

```json
{ "action": "react", "to": "chat:oc_xxx", "messageId": "om_xxx", "emoji": "THUMBSUP" }
```

常用表情：`THUMBSUP`, `FINGERHEART`, `SMILE`, `APPLAUSE`, `DONE`, `OnIt`, `Typing`

### 消息操作

| action | 用途 | 关键参数 |
|--------|------|----------|
| `pinMessage` | Pin 消息 | `messageId: "om_xxx"` |
| `unpinMessage` | 取消 Pin | `messageId: "om_xxx"` |
| `updateMessage` | 编辑消息 | `messageId: "om_xxx"`, `content: "新内容"` |
| `listMessages` | 列出消息 | `chatId: "oc_xxx"`, `pageSize: 20` |

### 话题回复

```json
{ "action": "replyInThread", "messageId": "om_xxx", "content": "话题内回复" }
```

### 群聊查询

| action | 用途 | 关键参数 |
|--------|------|----------|
| `getChatMembers` | 获取群成员 | `chatId: "oc_xxx"` |
| `getChatInfo` | 获取群信息 | `chatId: "oc_xxx"` |

## 飞书文档工具 (message)

### 文档操作

| action | 用途 | 关键参数 |
|--------|------|----------|
| `createDocument` | 创建文档 | `title: "标题"` → 返回 `documentId`, `url` |
| `appendDocument` | 追加内容 | `documentId: "doxcnXXX"`, `content: "内容"` ⚠️ 每次≤5000字 |
| `readDocument` | 读取文档 | `documentId: "doxcnXXX"` |
| `manageDocPermission` | 权限管理 | 见下方 |

### 权限管理

```json
// 查看权限
{ "action": "manageDocPermission", "docToken": "doxcnXXX", "action": "list" }

// 添加权限（用消息中的 sender 作为 memberId）
{ "action": "manageDocPermission", "docToken": "doxcnXXX", "action": "add", "memberId": "ou_xxx", "perm": "view" }
// perm: "view"（只读）或 "edit"（可编辑）
```

### 表格操作

| action | 用途 | 关键参数 |
|--------|------|----------|
| `createSpreadsheet` | 创建表格 | `title: "表格名"` → 返回 `spreadsheetToken` |
| `readSpreadsheet` | 读取表格 | `spreadsheetToken`, `sheetId`, `range: "A1:C10"` |
| `writeSpreadsheet` | 写入表格 | `spreadsheetToken`, `sheetId`, `range: "A1"`, `values: [[...]]` |

## 参数格式提醒

**`to` vs `chatId` 的区别（重要！）：**

- **`to`**（格式 `chat:oc_xxx`）— 只用于：`send`, `reply`, `react`, `sendAttachment`
- **`chatId`**（格式 `oc_xxx`，不带 `chat:` 前缀）— 用于其他所有飞书 action

**常见错误：** 自定义 action 传了 `to` 参数 → 框架报错
