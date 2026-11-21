"""Deliver the finished front page for make.fun's 20 November 2026 news-image bounty.

The artwork (entry.png) sits beside this script, already rendered. Running
this program copies that image, byte for byte, into the output directory the
harness asks for, then proves the copy is faithful by comparing SHA-256
digests before reporting success.
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
CHUNK = 1024 * 256


def digest_of(path: Path) -> str:
    """Return the SHA-256 hex digest of a file, read in blocks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            hasher.update(block)
    return hasher.hexdigest()


def choose_output_dir(here: Path) -> Path:
    """Pick the destination folder: explicit env var, /output, or local."""
    from_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if from_env:
        return Path(from_env).expanduser()
    shared = Path("/output")
    if shared.is_dir():
        return shared
    return here


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        print(f"error: expected the front page at {source}, but it is not there",
              file=sys.stderr)
        return 1

    target_dir = choose_output_dir(here)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME

    payload = source.read_bytes()
    expected = hashlib.sha256(payload).hexdigest()

    if target.is_file() and digest_of(target) != expected:
        print(f"error: {target} already exists with different content; "
              "refusing to overwrite it", file=sys.stderr)
        return 1

    target.write_bytes(payload)
    actual = digest_of(target)
    if actual != expected:
        print(f"error: copy failed verification (sha256 {actual} != {expected})",
              file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(payload)} bytes, sha256 {actual})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
