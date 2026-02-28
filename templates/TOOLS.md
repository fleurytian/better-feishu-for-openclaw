<!-- [better-feishu] START -->

## 飞书（关键注意事项）

> 完整飞书 API 参见 feishu skill。这里只记高频踩坑点。

### action 的 target 规则（必读！）

**需要 `target`（格式 `chat:oc_xxx`）的 action：**
- `react`, `sendAttachment`, `pinMessage`, `unpinMessage`, `recallMessage`, `updateMessage`, `listMessages`, `getChatInfo`, `getChatMembers`, `addChatMembers`, `removeChatMembers`

**不要传 target 的 action（框架已 patch 不再报错，但仍建议不传）：**
- `readDocument`, `appendDocument`, `createDocument`, `manageDocPermission`
- `readSpreadsheet`, `writeSpreadsheet`, `createSpreadsheet`
- `createBitable`, `updateBitable`, `addBitableField`, `updateBitableField`, `deleteBitableField`, `uploadBitableFile`, `listBitableTables`, `listBitableRecords`, `createBitableRecord`, `updateBitableRecord`, `deleteBitableRecord`
- `createTopicPost`
- `getWikiNode`, `listWikiNodes`, `listWikiSpaces`
- `searchDrive`, `uploadFile`, `createFolder`
- `translateText`, `ocrImage`, `speechToText`
- `downloadImage`, `downloadFile`, `downloadAttachment`
- `createChat`, `listThreadMessages`, `replyInThread`

### 飞书文档和表格读取（必读！）

**收到飞书文档/表格链接时，必须用飞书扩展读取，不要用 browser 或 web_fetch！**

```
# 读取文档（不传 target）
message(action="readDocument", documentId="<token>")

# 读取表格（不传 target）
message(action="readSpreadsheet", spreadsheetToken="<token>", sheetId="Sheet1", range="A1:Z100")
```

**从链接提取 token：**
- 文档：`/docx/ABC123def` → documentId = `ABC123def`
- 表格：`/sheets/ABC123def` → spreadsheetToken = `ABC123def`
- Wiki：`/wiki/ABC123def` → documentId = `ABC123def`（直接用 readDocument）
- **token 不一定以 doxcn/shtcn 开头，直接从 URL 提取**

**飞书文档创建（推荐两步模式）：**
1. 先 createDocument 只传 title → 拿到 documentId
2. 再 appendDocument 传 content（每次最多约5000字，长内容分批 append）

**appendDocument 支持完整 markdown 格式：**
- 内联：**加粗** *斜体* ~~删除线~~ `行内代码` [链接](url)
- 块级：# 标题、- 列表、1. 有序列表、- [ ] todo、> 引用
- 代码块：` ```python ... ``` `（支持语言高亮）
- 分隔线：--- 或 ___
- 表格：标准 markdown 表格语法
- **图片：`![描述](路径或URL)`** — 支持本地路径和 HTTP(S) URL，自动上传到飞书

### 飞书文件分享规则（必读！反复犯错的地方）

**用户无法访问你的文件路径！** 不要给用户发路径，他们打不开。

**正确做法：用 sendAttachment 发送附件：**
```
message(action="sendAttachment", target="chat:oc_xxx", filePath="/path/to/file.png")
```

**target 格式：**
- 群聊：`chat:oc_xxx`
- 单聊（DM）：`user:ou_xxx`（不是 `chat:`！）

**常见错误：**
- ❌ 发一段文字说「文件在 ~/xxx.pdf」→ 用户打不开
- ❌ 忘记用 sendAttachment，直接在消息里写路径
- ❌ 单聊用 `chat:` 前缀 → 应该用 `user:`
- ✅ 先生成文件，再用 sendAttachment 发过去

### 群聊旁听模式

配置项：`channels.feishu.observeMode`，两种模式：

| 模式 | 值 | 行为 |
|------|------|------|
| 自主旁听 | `"autonomous"` | 实时收到每条群消息，加 [旁听] 前缀，自己判断要不要回复 |
| 完全旁听 | `"full"` | 群消息**不触发 LLM 调用**（零成本），缓存在内存 buffer 中；被 @ 时 buffer 自动 flush 为上下文注入（最多50条） |

**全局默认：完全旁听 (`full`)**

**如何分辨当前模式：**
- 自主旁听：你会收到每条群消息，带 `[旁听]` 前缀
- 完全旁听：你只在被 @ 时才会收到消息，同时附带历史上下文

**支持按群聊单独配置：**
```json
"channels": {
  "feishu": {
    "observeMode": "full",
    "groups": {
      "oc_xxx": { "observeMode": "autonomous" },
      "oc_yyy": { "observeMode": "full" }
    }
  }
}
```
优先级：`groups[chatId].observeMode` > `observeMode`（全局默认）

<!-- [better-feishu] END -->
