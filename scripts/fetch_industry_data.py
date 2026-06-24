"""Refresh the local industry-data cache and print its path as JSON.

Thin wrapper over the shared ``industry_map_client`` (the L3 consumer client
shipped from stock-industry-map-in). This replaces the previous hand-rolled
urllib/ETag fetcher that duplicated logic also present in ~4 sibling repos.

Output contract (unchanged, consumed by SKILL.md):
    {"success": true, "cache_path": "<abs path to cache json>"}

The cache path is kept at ``~/.stock_industry_map/industry_cache.json`` for
continuity with prior runs of this skill.

Requires the client to be installed once:
    pip install "industry-data-in @ git+https://github.com/eggmasonvalue/stock-industry-map-in.git"
"""

import json
import sys
from pathlib import Path

CACHE_PATH = Path.home() / ".stock_industry_map" / "industry_cache.json"


def main() -> int:
    try:
        from industry_map_client import IndustryMap
    except ImportError:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": (
                        "industry_map_client not installed. Install once with: "
                        'pip install "industry-data-in @ '
                        'git+https://github.com/eggmasonvalue/stock-industry-map-in.git"'
                    ),
                }
            )
        )
        return 1

    im = IndustryMap(cache_path=CACHE_PATH)
    im.refresh()  # ETag-conditional; falls back to cache on failure, never raises

    if not im.data and not im.cache_path.exists():
        print(json.dumps({"success": False, "error": "no data fetched and no cache exists"}))
        return 1

    print(json.dumps({"success": True, "cache_path": str(im.cache_path.absolute())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
