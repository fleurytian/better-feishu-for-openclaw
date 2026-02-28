#!/usr/bin/env python3
"""Patch: fix target handling for custom plugin actions (e.g. createDocument).

Two issues in OpenClaw framework:
1. actionRequiresTarget() returns true for unknown actions (undefined !== "none")
2. applyTargetToParams() throws for unknown actions when target is provided

Run after every openclaw upgrade:
    python3 patch-channel-target.py [--openclaw-dir ~/openclaw]
"""
import argparse
import glob
import re

parser = argparse.ArgumentParser()
parser.add_argument("--openclaw-dir", default=None,
                    help="Path to openclaw installation (default: ~/openclaw)")
args = parser.parse_args()

import os
openclaw_dir = args.openclaw_dir or os.path.expanduser("~/openclaw")
files = glob.glob(os.path.join(openclaw_dir, "dist", "*.js"))
total = 0

for f in files:
    with open(f, "r") as fh:
        content = fh.read()
    changed = False

    # Fix 1: actionRequiresTarget - unknown actions should not require target
    old1 = r'return MESSAGE_ACTION_TARGET_MODE\[action\] !== "none";'
    new1 = 'var m = MESSAGE_ACTION_TARGET_MODE[action]; return m != null && m !== "none";'
    if re.search(old1, content):
        content = re.sub(old1, new1, content)
        changed = True

    # Fix 2: applyTargetToParams - silently ignore target for unknown actions
    old2 = r'throw new Error\(`Action \$\{params\.action\} does not accept a target\.`\);'
    new2 = "delete params.args.target; return;"
    if re.search(old2, content):
        content = re.sub(old2, new2, content)
        changed = True

    if changed:
        with open(f, "w") as fh:
            fh.write(content)
        total += 1
        print(f"  patched: {f}")

if total:
    print(f"Done. Patched {total} file(s). Restart gateway to apply.")
else:
    print("No files needed patching (already applied or pattern changed).")
