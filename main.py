"""Entrypoint: copy the finished front page to the output folder.

The image itself is drawn by render23.py at authoring time and ships
in this repository as entry.png. This program only moves those bytes
into place, so it needs nothing but the standard library and writes
the same file on every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

os.makedirs(TARGET_DIR, exist_ok=True)
shutil.copyfile(SOURCE, os.path.join(TARGET_DIR, "entry.png"))
