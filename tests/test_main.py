#!/usr/bin/env python3
"""Tests for the VITRAEL poster entrypoint.

Runs main.py in a temp dir (stdlib only, no Pillow) and asserts the
output exists, is 1024x1024, is under 1 MiB and is byte-identical to
the bundled entry.png.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestMain(unittest.TestCase):
    def test_writes_identical_poster(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            r = subprocess.run([sys.executable, os.path.join(ROOT, "main.py")],
                               env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = os.path.join(tmp, "entry.png")
            self.assertTrue(os.path.isfile(out))
            self.assertLess(os.path.getsize(out), 1048576)
            with open(out, "rb") as f:
                got = f.read()
            with open(os.path.join(ROOT, "entry.png"), "rb") as f:
                want = f.read()
            self.assertEqual(got, want)
            im = Image.open(out)
            self.assertEqual(im.size, (1024, 1024))

    def test_output_is_readable_by_others(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            subprocess.run([sys.executable, os.path.join(ROOT, "main.py")],
                           env=env, check=True, capture_output=True)
            mode = os.stat(os.path.join(tmp, "entry.png")).st_mode & 0o777
            self.assertEqual(mode, 0o644)


if __name__ == "__main__":
    unittest.main()
