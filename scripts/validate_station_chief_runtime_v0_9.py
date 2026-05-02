#!/usr/bin/env python3
import runpy
from pathlib import Path

if __name__ == "__main__":
    v10_path = Path(__file__).parent / "validate_station_chief_runtime_v1_0.py"
    runpy.run_path(str(v10_path), run_name="__main__")