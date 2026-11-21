#!/usr/bin/env python3
"""VITRAEL — The Glass Desert. Graded entrypoint (pure Python stdlib).

Copies the bundled poster (entry.png, rendered at build time by
render_poster.py) to the grader's output directory as entry.png.
Writes to $MAKEFUN_OUTPUT_DIR first, then /output, then the working
directory — first location that succeeds — and chmods the output 0644
so the grader's collector can read it.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    dest_dir = None
    for cand in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output",
                 os.getcwd()):
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
            probe = os.path.join(cand, ".makefun-write-test")
            with open(probe, "w") as f:
                f.write("ok")
            os.remove(probe)
            dest_dir = cand
            break
        except OSError:
            continue
    if dest_dir is None:
        print("no writable output directory", file=sys.stderr)
        return 1
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    os.chmod(dest, 0o644)
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
