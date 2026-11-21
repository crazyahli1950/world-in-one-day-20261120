#!/usr/bin/env python3
"""Deliver the finished front page for make.fun's 20 November 2026 news-image bounty.

The image itself lives beside this file as entry.png. Running this script
copies those exact bytes to the output path make.fun expects, using only
the standard library, so the result is identical on every machine and
needs no network access.
"""
import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, SOURCE_NAME)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (
        "/output" if os.path.isdir("/output") else folder
    )
    target = os.path.join(target_dir, SOURCE_NAME)
    if os.path.abspath(source) == os.path.abspath(target):
        print("already at", target)
        return
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(source, target)
    if sha256_of(source) != sha256_of(target):
        print("copy mismatch", file=sys.stderr)
        raise SystemExit(1)
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
