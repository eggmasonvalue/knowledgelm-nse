import json
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
import sys

def main():
    cache_dir = Path.home() / ".stock_industry_map"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "industry_cache.json"
    url = "https://raw.githubusercontent.com/eggmasonvalue/stock-industry-map-in/main/out/industry_data.json"

    cached_data = {"metadata": [], "data": {}, "etag": None}
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
        except Exception:
            pass

    headers = {}
    if cached_data.get("etag"):
        headers["If-None-Match"] = cached_data["etag"]

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            new_data = json.loads(response.read().decode("utf-8"))
            etag = response.headers.get("ETag")

            # Update cache file
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({
                    "metadata": new_data.get("metadata", []),
                    "data": new_data.get("data", {}),
                    "etag": etag
                }, f, indent=2)
    except Exception as e:
        # In urllib, a 304 raises an HTTPError
        if isinstance(e, HTTPError) and e.code == 304:
            pass
        elif not cache_path.exists():
            print(json.dumps({"success": False, "error": f"Failed to fetch and no cache exists: {e}"}))
            sys.exit(1)

    print(json.dumps({
        "success": True,
        "cache_path": str(cache_path.absolute())
    }))

if __name__ == "__main__":
    main()
