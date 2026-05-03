#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "scripts" / "validate_station_chief_runtime_v2_5.py"), run_name="__main__")
