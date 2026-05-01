#!/usr/bin/env python3
from __future__ import annotations

import json

from station_chief_runtime import run_fixture_tests


def main() -> None:
    result = run_fixture_tests()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result.get("fixture_test_status") == "PASS" else 1)


if __name__ == "__main__":
    main()
