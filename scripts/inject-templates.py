#!/usr/bin/env python3
"""Idempotent injection of better-feishu templates into OpenClaw workspace md files.

If a template section already exists (detected by markers), it will be replaced.
If not, the template content will be appended to the end of the file.

Usage:
    python3 inject-templates.py [--workspace-dir ~/.openclaw/workspace] [--templates-dir ./templates]
"""
import argparse
import os
import re

MARKER_START = "<!-- [better-feishu] START -->"
MARKER_END = "<!-- [better-feishu] END -->"

TEMPLATE_FILES = ["SOUL.md", "TOOLS.md", "AGENTS.md", "USER.md"]


def inject_template(workspace_file, template_content):
    """Inject template content into workspace file. Idempotent."""
    if os.path.exists(workspace_file):
        with open(workspace_file, "r") as f:
            existing = f.read()
    else:
        existing = ""

    if MARKER_START in existing and MARKER_END in existing:
        # Replace existing injection
        pattern = re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END)
        new_content = re.sub(pattern, template_content.strip(), existing, flags=re.DOTALL)
        action = "updated"
    else:
        # Append to end
        separator = "\n\n" if existing.strip() else ""
        new_content = existing.rstrip() + separator + template_content.strip() + "\n"
        action = "injected"

    with open(workspace_file, "w") as f:
        f.write(new_content)
    return action


def main():
    parser = argparse.ArgumentParser(description="Inject better-feishu templates into workspace")
    parser.add_argument("--workspace-dir", default=os.path.expanduser("~/.openclaw/workspace"))
    parser.add_argument("--templates-dir", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
    ))
    args = parser.parse_args()

    workspace_dir = args.workspace_dir
    templates_dir = args.templates_dir

    if not os.path.isdir(templates_dir):
        print(f"ERROR: templates directory not found: {templates_dir}")
        return 1

    os.makedirs(workspace_dir, exist_ok=True)

    for filename in TEMPLATE_FILES:
        template_path = os.path.join(templates_dir, filename)
        workspace_path = os.path.join(workspace_dir, filename)

        if not os.path.exists(template_path):
            print(f"  SKIP {filename}: template not found")
            continue

        with open(template_path, "r") as f:
            template_content = f.read()

        # Extract only the content between markers
        if MARKER_START in template_content and MARKER_END in template_content:
            start_idx = template_content.index(MARKER_START)
            end_idx = template_content.index(MARKER_END) + len(MARKER_END)
            template_content = template_content[start_idx:end_idx]

        action = inject_template(workspace_path, template_content)
        print(f"  {action}: {workspace_path}")

    print("Done.")
    return 0


if __name__ == "__main__":
    exit(main())
