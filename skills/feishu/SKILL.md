---
name: feishu
description: >
  飞书/Lark 消息渠道工具集。通过 message 工具调用飞书 API，支持表情回应、消息操作、
  群聊查询、文档/表格创建与编辑（含图片插入）、多维表格、话题帖子、云空间搜索与上传。
metadata: {"openclaw":{"emoji":"\U0001f4ce"}}
---

# 飞书工具参考

> **本文档可独立使用。** 即使不安装 better-feishu 插件，也可以参考这里的 action 格式和工作流。
> 如需安装完整插件，请看 [README.md](../../README.md)。

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
   - **注意**：每次写入有字数限制（约 5000 字），长内容要分批 append
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

## @ 提及用户

在消息文本中 @ 用户，使用以下格式：

```
<at user_id="ou_xxx">用户名</at>
```

**示例：**
```json
{
  "action": "send",
  "to": "chat:oc_xxx",
  "text": "<at user_id=\"ou_abc123\">张三</at> 请查看这个文档"
}
```

**获取 user_id：**
- 从收到的消息中，`sender` 字段就是发送者的 `ou_xxx`
- 用 `getChatMembers` 可以获取群成员列表及其 user_id

**注意：**
- `user_id` 格式为 `ou_xxx`（open_id）
- 用户名可以是任意文字，但建议用真实姓名
- @ 多人时，连续写多个 `<at>` 标签即可

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

**限制：话题内不能发送附件（图片/文件）。** 如需发送附件，请直接发到群聊主界面。

## 话题帖子 (Topic Post)

在**话题群**（chat_mode 为 thread 的群聊）中发起新的话题帖子。

```json
// 发起话题帖子（支持 post 富文本格式）
{ "action": "createTopicPost", "chatId": "oc_xxx", "content": "# 标题\n帖子正文内容" }

// 纯文本话题帖子
{ "action": "createTopicPost", "chatId": "oc_xxx", "content": "帖子内容", "msgType": "text" }
```

**返回值：** `{ ok: true, messageId: "om_xxx", threadId: "omt_xxx" }`

**与 replyInThread 的区别：**
- `createTopicPost` — 在话题群中发起**新话题**（相当于论坛里发新帖）
- `replyInThread` — 在已有消息下创建/回复讨论串

**注意：** `createTopicPost` 只适用于话题群（chat_mode = "thread"），普通群请用 `send`。

## 群聊查询

```json
// 查群成员
{ "action": "getChatMembers", "chatId": "oc_xxx" }

// 查群详情
{ "action": "getChatInfo", "chatId": "oc_xxx" }
```

## 文档

**⚠️ 从飞书链接提取 token 的方法：**
- 文档：`https://xxx.feishu.cn/docx/ABC123def` → documentId = `ABC123def`
- 表格：`https://xxx.feishu.cn/sheets/ABC123def` → spreadsheetToken = `ABC123def`
- 表格带 sheet：`https://xxx.feishu.cn/sheets/ABC123def?sheet=0ab1c2` → spreadsheetToken = `ABC123def`, sheetId = `0ab1c2`
- Wiki 文档：`https://xxx.feishu.cn/wiki/ABC123def` → documentId = `ABC123def`（**URL 里有 /wiki/ 但它就是普通文档，直接用 readDocument**）
- **token 不一定以 `doxcn`/`shtcn` 开头**，直接从 URL 提取即可
- **表格链接没有 `?sheet=` 参数时，sheetId 可以省略或传 `"Sheet1"`**

**⚠️ 重要：创建文档后必须开权限，否则用户打不开！**

**appendDocument 支持图片插入：** 在 markdown 内容中使用 `![描述](路径或URL)` 语法即可插入图片。支持本地路径和 HTTP(S) URL，图片会自动上传到飞书。上传失败时会 fallback 为文字链接。

**完整工作流（创建 → 分批写入 → 开权限 → 发链接）：**

```json
// 第1步：创建文档（返回 documentId）
{ "action": "createDocument", "title": "标题" }
// 返回: { "documentId": "doxcnXXX", "url": "https://xxx.feishu.cn/docx/doxcnXXX" }

// 第2步：分批写入内容（每次 appendDocument 有字数限制，约 5000 字）
{ "action": "appendDocument", "documentId": "doxcnXXX", "content": "# 第一部分\n内容..." }
{ "action": "appendDocument", "documentId": "doxcnXXX", "content": "# 第二部分\n更多内容..." }
// 长文档必须分多次 append，每次控制在 5000 字以内

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

## 多维表格 (Bitable)

**⚠️ 从飞书链接提取 token 的方法：**
- 多维表格：`https://xxx.feishu.cn/base/ABC123def` → appToken = `ABC123def`

**完整工作流（创建 → 加字段 → 写数据 → 开权限 → 发链接）：**

```json
// 第1步：创建多维表格（返回 appToken，自动清理默认空记录和默认字段）
{ "action": "createBitable", "name": "表格名" }
// 可选：指定云空间文件夹
{ "action": "createBitable", "name": "表格名", "folderToken": "fldcnXXX" }
// 返回: { "appToken": "XXX", "name": "表格名", "url": "https://xxx.feishu.cn/base/XXX" }

// 第2步：查看表结构（获取 tableId 和现有字段）
{ "action": "listBitableTables", "appToken": "XXX" }
// 返回每个 table 的 tableId、name 和 fields（含 fieldId、name、type）

// 第3步：按需添加字段
{ "action": "addBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldName": "书名", "fieldType": "text" }
{ "action": "addBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldName": "评分", "fieldType": "number" }
// select/multi_select 可带选项列表
{ "action": "addBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldName": "状态", "fieldType": "select", "options": ["待读", "在读", "已读"] }
{ "action": "addBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldName": "标签", "fieldType": "multi_select", "options": ["科幻", "文学", "历史"] }
// fieldType 可选: text(1), number(2), select(3), multi_select(4), date(5), checkbox(7), person(11), url(15), attachment(17)
// options 支持字符串数组 ["A","B"] 或对象数组 [{"name":"A","color":0}]，颜色 0-9

// 第4步：写入数据（fields 是字段名到值的映射）
{ "action": "createBitableRecord", "appToken": "XXX", "tableId": "tblXXX", "fields": {"书名": "三体", "评分": 9.5} }
```

**各字段类型的值格式：**

| 字段类型 | 值格式 | 示例 |
|---------|--------|------|
| text | 字符串 | `"三体"` |
| number | 数字 | `9.5` |
| select | 选项名字符串 | `"在读"` |
| multi_select | 选项名数组 | `["科幻", "文学"]` |
| date | 毫秒时间戳 | `1735084800000` |
| checkbox | 布尔 | `true` |
| person | **对象数组** | `[{"id": "ou_xxx"}]` |
| url | 字符串 | `"https://example.com"` |
| attachment | token数组 | `[{"file_token": "xxx"}]` |

**人员字段注意：** 必须是 `[{"id": "ou_xxx"}]` 格式（数组包对象），不能直接传 `"ou_xxx"` 字符串。`ou_xxx` 从消息的 `sender` 或 `getChatMembers` 获取。

```json

// 第5步：给用户开权限
{ "action": "manageDocPermission", "docToken": "XXX", "docType": "bitable", "action": "add", "memberId": "ou_xxx", "perm": "view" }

// 第6步：发送链接给用户
```

**给已有字段追加选项（不要新建字段！）：**

```json
// 先用 listBitableTables 获取 fieldId
{ "action": "listBitableTables", "appToken": "XXX" }
// 返回每个字段的 fieldId

// 给已有 select/multi_select 字段追加选项（自动合并，不会覆盖已有选项）
{ "action": "updateBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldId": "fldXXX", "addOptions": ["新选项A", "新选项B"] }

// 重命名字段
{ "action": "updateBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldId": "fldXXX", "fieldName": "新名称" }

// 删除字段（主字段不可删）
{ "action": "deleteBitableField", "appToken": "XXX", "tableId": "tblXXX", "fieldId": "fldXXX" }
```

**重要：** 当需要给单选/多选字段新增选项时，用 `updateBitableField` + `addOptions`，**不要用 `addBitableField` 新建同名字段**，否则会产生重复列。

**其他操作：**

```json
// 查询记录（支持 filter 筛选）
{ "action": "listBitableRecords", "appToken": "XXX", "tableId": "tblXXX" }
{ "action": "listBitableRecords", "appToken": "XXX", "tableId": "tblXXX", "filter": "CurrentValue.[评分] > 8" }

// 更新记录
{ "action": "updateBitableRecord", "appToken": "XXX", "tableId": "tblXXX", "recordId": "recXXX", "fields": {"评分": 10} }

// 删除记录
{ "action": "deleteBitableRecord", "appToken": "XXX", "tableId": "tblXXX", "recordId": "recXXX" }
```

**常见错误：**
- 创建表后不加字段就写数据 → 字段名不匹配报错。先用 `listBitableTables` 查看现有字段名
- 忘记开权限 → 用户打不开。多维表格开权限时 `docType` 要传 `"bitable"`

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
