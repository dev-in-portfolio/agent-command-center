#!/usr/bin/env python3
import runpy
from pathlib import Path

if __name__ == "__main__":
    v15_path = Path(__file__).parent / "validate_station_chief_runtime_v1_5.py"
    runpy.run_path(str(v15_path), run_name="__main__")