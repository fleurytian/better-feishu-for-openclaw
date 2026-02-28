#!/usr/bin/env python3
"""Inject better-feishu templates into workspace md files.

Usage: python3 inject-templates.py <template_dir> <workspace_dir>

Idempotent: uses marker comments to replace existing injections.
Safe: never overwrites user content outside the markers.
"""
import os, sys

MARKER_START = "<!-- BETTER-FEISHU-START -->"
MARKER_END = "<!-- BETTER-FEISHU-END -->"

def inject(template_path, target_path):
    name = os.path.basename(template_path)

    with open(template_path, "r") as f:
        template_content = f.read()

    inject_block = f"\n{MARKER_START}\n{template_content}\n{MARKER_END}\n"

    if not os.path.exists(target_path):
        # 文件不存在，直接创建
        with open(target_path, "w") as f:
            f.write(inject_block)
        return "created"

    with open(target_path, "r") as f:
        existing = f.read()

    if MARKER_START in existing:
        # 替换旧内容
        before = existing[:existing.index(MARKER_START)]
        after_marker = existing[existing.index(MARKER_END) + len(MARKER_END):]
        with open(target_path, "w") as f:
            f.write(before.rstrip("\n") + inject_block + after_marker.lstrip("\n"))
        return "updated"
    else:
        # 追加到末尾
        with open(target_path, "a") as f:
            f.write("\n" + inject_block)
        return "appended"


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <template_dir> <workspace_dir>")
        sys.exit(1)

    template_dir = sys.argv[1]
    workspace_dir = sys.argv[2]
    os.makedirs(workspace_dir, exist_ok=True)

    for fname in sorted(os.listdir(template_dir)):
        if not fname.endswith(".md"):
            continue
        template_path = os.path.join(template_dir, fname)
        target_path = os.path.join(workspace_dir, fname)
        result = inject(template_path, target_path)
        print(f"  {result}: {fname}")


if __name__ == "__main__":
    main()
