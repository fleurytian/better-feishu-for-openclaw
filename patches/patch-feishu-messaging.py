#!/usr/bin/env python3
"""Inject feishu interaction rules into buildMessagingSection in dist."""
import glob, sys, os

dist_dir = os.path.expanduser("~/openclaw/dist")
# Find the pi-embedded file that contains buildMessagingSection
targets = []
for f in glob.glob(os.path.join(dist_dir, "pi-embedded-*.js")):
    with open(f) as fh:
        if "buildMessagingSection" in fh.read():
            targets.append(f)

if not targets:
    print("ERROR: no pi-embedded file with buildMessagingSection found")
    sys.exit(1)

MARKER = '飞书交互规则'
ANCHOR = '...params.messageToolHints ?? []'

INJECTION = '''\t\t].filter(Boolean).join("\\n") : "",
\t\tparams.runtimeChannel === "feishu" ? [
\t\t\t"",
\t\t\t"### 飞书交互规则",
\t\t\t"",
\t\t\t"**表情回应（react）：** 通过 message 工具 `action: \\"react\\"`, `messageId`, `emoji`",
\t\t\t"飞书使用专有 emoji_type（不是 unicode），常用的有：",
\t\t\t"THUMBSUP / ThumbsDown / SMILE / LAUGH / LOL / HEART / Fire / APPLAUSE / THANKS / MUSCLE / PARTY / LOVE / CRY / SHOCKED / THINKING / DONE / JIAYI / OK / FISTBUMP / GLANCE / SALUTE / Coffee / Hundred / Trophy / LGTM / OnIt / GoGoGo",
\t\t\t"- 收到好消息、感谢 → react THUMBSUP 或 HEART",
\t\t\t"- 确认/同意 → DONE 或 THUMBSUP",
\t\t\t"- 搞笑内容 → LOL 或 LAUGH",
\t\t\t"- 不需要每条都回复文字，有时一个 react 就够了",
\t\t\t"- 取消 react: 加 `reactionId`, `remove: true`",
\t\t\t"",
\t\t\t"**文件发送 —— 绝对禁止给路径：**",
\t\t\t"用户无法访问你的 VM 文件系统。想分享文件必须用 `action: \\"sendAttachment\\"`, `to: \\"chat:oc_xxx\\"`, `path`。",
\t\t\t"单聊用 `to: \\"user:ou_xxx\\"`。绝对不要在消息里写文件路径。",
\t\t].join("\\n") : "",'''

for target in targets:
    with open(target) as fh:
        content = fh.read()
    if MARKER in content:
        print(f"SKIP {target}: already patched")
        continue
    if ANCHOR not in content:
        print(f"SKIP {target}: anchor not found")
        continue

    # Find the anchor line and the line after it (].filter...)
    old = ANCHOR + '\n\t\t].filter(Boolean).join("\\n") : "",'
    if old not in content:
        print(f"SKIP {target}: multi-line anchor not found")
        continue

    new = ANCHOR + '\n' + INJECTION
    content = content.replace(old, new, 1)
    with open(target, 'w') as fh:
        fh.write(content)
    print(f"PATCHED {target}")

