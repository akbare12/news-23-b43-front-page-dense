#!/usr/bin/env python3
"""news-23 b43 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("main.py: ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == here or os.path.abspath(out_dir).startswith(here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")

    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()

    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if depth != 8 or ctype not in (2, 6):
        fail("unexpected PNG bit depth %d / colour type %d" % (depth, ctype))
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        fail("entry.png has a malformed IEND trailer")

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    print("source entry.png: %d bytes, sha256 %s" % (len(data), hashlib.sha256(data).hexdigest()))
    with open(dst, "wb") as f:
        f.write(data)

    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
