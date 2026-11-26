#!/usr/bin/env python3
"""News-image entry runner for the 26 November 2026 front page.

The repository ships the finished front page as entry.png. This program
copies it, unchanged, to the output directory the harness names, after
checking the file's fingerprint first. It needs nothing from the network
and nothing beyond the Python standard library, so two runs always write
the same bytes.
"""

from hashlib import sha256
from pathlib import Path
from shutil import copyfile
import os
import sys

# Fingerprint of the front page as rendered for this entry ("THE WORLD
# TODAY", 33 stories from Thursday 26 November 2026). The copy is refused
# unless the shipped file matches it exactly.
FRONT_PAGE_SHA256 = "b13b18e6fc2cc419267ebd8a26de554ab792c77a42ce5161a6e85bb06a94909d"
FRONT_PAGE_NAME = "entry.png"


def fingerprint(path):
    """Return the hex SHA-256 of the file at *path*."""
    digest = sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 16)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def copy_entry():
    """Copy the shipped front page to the harness output directory."""
    here = Path(__file__).resolve().parent
    source = here / FRONT_PAGE_NAME
    if fingerprint(source) != FRONT_PAGE_SHA256:
        print("refusing: shipped entry.png fingerprint mismatch", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / FRONT_PAGE_NAME
    copyfile(source, target)
    if fingerprint(target) != FRONT_PAGE_SHA256:
        print("refusing: written entry.png fingerprint mismatch", file=sys.stderr)
        return 1
    print(f"wrote {target} sha256 {FRONT_PAGE_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(copy_entry())
