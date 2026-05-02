#!/usr/bin/env python3
import runpy
from pathlib import Path

if __name__ == "__main__":
    v16_path = Path(__file__).parent / "validate_station_chief_runtime_v1_6.py"
    runpy.run_path(str(v16_path), run_name="__main__")