#!/usr/bin/env python3
"""Framing shim for tripsy-mcp stdio mode.

tripsy-mcp 1.6.2 rewrites tools/list responses through an annotation
normalizer that drops the trailing newline, which breaks newline-delimited
JSON-RPC framing and makes MCP clients hang waiting for the tool list.
This shim passes stdin through untouched and re-frames stdout by splitting
concatenated JSON documents and emitting exactly one per line.

The tripsy-mcp binary is located via $TRIPSY_MCP_BIN, then
~/.local/bin/tripsy-mcp, then $PATH.
"""

import codecs
import json
import os
import shutil
import subprocess
import sys
import threading


def find_binary():
    candidates = [
        os.environ.get("TRIPSY_MCP_BIN"),
        os.path.expanduser("~/.local/bin/tripsy-mcp"),
        shutil.which("tripsy-mcp"),
    ]
    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    sys.stderr.write(
        "tripsy-mcp-shim: tripsy-mcp binary not found; install with "
        "`curl -fsSL https://tripsy.app/install_cli | bash`\n"
    )
    sys.exit(1)


def pump_stdin(child):
    try:
        while True:
            chunk = sys.stdin.buffer.read(1)
            if not chunk:
                break
            child.stdin.write(chunk)
            child.stdin.flush()
    except (BrokenPipeError, OSError):
        pass
    finally:
        try:
            child.stdin.close()
        except OSError:
            pass


def reframe_stdout(child):
    decoder = json.JSONDecoder()
    utf8 = codecs.getincrementaldecoder("utf-8")(errors="replace")
    buf = ""
    out = sys.stdout.buffer
    while True:
        # read1 returns as soon as any bytes are available; read(n) would
        # block until n bytes arrive and stall on the tail of a response.
        chunk = child.stdout.read1(65536)
        if not chunk:
            break
        buf += utf8.decode(chunk)
        while True:
            stripped = buf.lstrip(" \t\r\n")
            if not stripped:
                buf = ""
                break
            try:
                doc, end = decoder.raw_decode(stripped)
            except json.JSONDecodeError:
                # Incomplete document; wait for more bytes.
                buf = stripped
                break
            out.write(
                json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            )
            out.write(b"\n")
            out.flush()
            buf = stripped[end:]


def main():
    child = subprocess.Popen(
        [find_binary()] + sys.argv[1:],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
    )
    threading.Thread(target=pump_stdin, args=(child,), daemon=True).start()
    reframe_stdout(child)
    sys.exit(child.wait())


if __name__ == "__main__":
    main()
