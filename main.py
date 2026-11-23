"""Entry point: copy the bundled front page to the output directory.

The sheet itself is `entry.png` beside this file (rendered by
`render23.py`). The harness runs this program twice and both runs
must write the same bytes, so this just copies the file byte for byte.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
