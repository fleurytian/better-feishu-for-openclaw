# TOOLS.md - 飞书工具备忘

## 飞书文档和表格读取（重要）

**收到飞书文档/表格链接时，必须使用飞书扩展读取，不要用 browser 或 web_fetch！**

```
# 读取飞书文档
message(action="readDocument", documentId="<token>")

# 读取飞书表格
message(action="readSpreadsheet", spreadsheetToken="<token>", sheetId="Sheet1", range="A1:Z100")
```

**如何从飞书链接提取 token：**
- 文档：`/docx/ABC123def` → documentId = `ABC123def`
- 表格：`/sheets/ABC123def` → spreadsheetToken = `ABC123def`
- 表格带 sheet：`/sheets/ABC123def?sheet=0ab1c2` → sheetId = `0ab1c2`
- Wiki：`/wiki/ABC123def` → documentId = `ABC123def`（直接用 readDocument）
- **token 不一定以 doxcn/shtcn 开头，直接从 URL 提取即可**

## 飞书消息工具 (message)

`message` 工具通过 `action` 参数决定行为。

### 表情回应

```json
{ "action": "react", "to": "chat:oc_xxx", "messageId": "om_xxx", "emoji": "THUMBSUP" }
```

**飞书使用专有 emoji_type（不是 unicode emoji）。** 常用：
- 认可: THUMBSUP, DONE, JIAYI, APPLAUSE, FINGERHEART
- 加油: MUSCLE, GoGoGo, STRIVE, OnIt
- 好笑: LOL, LAUGH, SMIRK
- 惊讶: SHOCKED, WHAT, PETRIFIED
- 尴尬: FACEPALM, NOSEPICK, DULL, GLANCE, SWEAT
- 工作中: Typing, OneSecond, OnIt
- 不同意: No, CrossMark, MinusOne
- 取消: 加 `reactionId` + `remove: true`

### 消息管理

| action | 用途 | 关键参数 |
|--------|------|----------|
| `send` | 发送消息 | `to: "chat:oc_xxx"`, `message: "内容"` |
| `sendAttachment` | 发送文件/图片 | `to: "chat:oc_xxx"`, `path: "/文件路径"` |
| `pinMessage` | Pin 消息 | `messageId` |
| `recallMessage` | 撤回消息 | `messageId` |
| `updateMessage` | 编辑消息 | `messageId`, `content` |
| `listMessages` | 列出消息 | `chatId: "oc_xxx"`, `pageSize?` |
| `replyInThread` | 话题内回复 | `messageId`, `content` |
| `getChatMembers` | 群成员列表 | `chatId: "oc_xxx"` |
| `getChatInfo` | 群聊详情 | `chatId: "oc_xxx"` |

### 文档操作

**推荐两步创建：先 createDocument 只传 title 拿到 documentId，再 appendDocument 传 content。**

| action | 用途 | 关键参数 |
|--------|------|----------|
| `createDocument` | 创建文档 | `title` → 返回 `documentId`, `url` |
| `appendDocument` | 追加内容 | `documentId`, `content`(markdown) ⚠️每次≤5000字 |
| `readDocument` | 读取文档 | `documentId` |
| `manageDocPermission` | 权限管理 | `docToken`, `permAction`("add"/"remove"/"list"), `memberId?`, `perm?`("view"/"edit") |

**appendDocument 支持完整 markdown：**
- 内联：**加粗** *斜体* ~~删除线~~ `行内代码` [链接](url)
- 块级：# 标题、- 列表、1. 有序列表、- [ ] todo、> 引用
- 代码块：```python ... ```（支持 68 种语言高亮）
- 分隔线：--- 或 ___
- 表格：标准 markdown 表格语法

### 表格操作

| action | 用途 | 关键参数 |
|--------|------|----------|
| `createSpreadsheet` | 创建表格 | `title?`, `folderToken?` |
| `readSpreadsheet` | 读取表格 | `spreadsheetToken`, `sheetId?`, `range?` |
| `writeSpreadsheet` | 写入表格 | `spreadsheetToken`, `sheetId`, `range?`, `values`(二维数组) |

### 云空间

| action | 用途 | 关键参数 |
|--------|------|----------|
| `searchDrive` | 搜索文件 | `query`, `fileType?`, `folderToken?` |
| `uploadFile` | 上传文件 | `path`, `parentToken`/`folderToken`, `fileName?` |
| `createFolder` | 创建文件夹 | `name`, `parentToken?` |

### 多维表格 (Bitable)

| action | 用途 | 关键参数 |
|--------|------|----------|
| `listBitableTables` | 列出数据表 | `appToken` |
| `listBitableRecords` | 列出记录 | `appToken`, `tableId`, `filter?`, `pageSize?` |
| `createBitableRecord` | 创建记录 | `appToken`, `tableId`, `fields` |
| `updateBitableRecord` | 更新记录 | `appToken`, `tableId`, `recordId`, `fields` |
| `deleteBitableRecord` | 删除记录 | `appToken`, `tableId`, `recordId` |

### Wiki

| action | 用途 | 关键参数 |
|--------|------|----------|
| `listWikiSpaces` | 列出知识库 | — |
| `listWikiNodes` | 列出节点 | `spaceId` |
| `getWikiNode` | 获取节点 | `spaceId`, `nodeToken` |

### 其他工具

| action | 用途 | 关键参数 |
|--------|------|----------|
| `translateText` | 翻译文本 | `text`, `sourceLang`, `targetLang` |
| `ocrImage` | 图片OCR | (自动识别消息中的图片) |
| `speechToText` | 语音转文字 | `speech`/`fileId` |
| `downloadImage` | 下载图片 | `imageKey`, `savePath`, `messageId?` |
| `downloadFile` | 下载文件 | `fileKey`, `savePath`, `messageId?` |

## 参数格式提醒（重要）

**`to` vs `chatId` 的区别：**
- **`to`**（格式 `chat:oc_xxx` 或 `user:ou_xxx`）— 只用于：`send`, `reply`, `react`, `sendAttachment`
- **`chatId`**（格式 `oc_xxx`，不带前缀）— 用于其他所有 action
- **自定义 action（文档/表格/Bitable/Wiki/云空间/翻译/OCR/下载等）不传 to 参数**，否则报错

## 群聊旁听模式

| 模式 | 值 | 行为 |
|------|------|------|
| 自主旁听 | `"autonomous"` | 实时收到每条群消息，加 [旁听] 前缀，自己判断回不回复 |
| 完全旁听 | `"full"` | 不触发 LLM，被 @ 时 flush 缓存消息为上下文 |
