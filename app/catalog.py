import json
import re
from typing import Any, Dict, List

def _safe_list(x):
    if isinstance(x, list):
        return [str(i) for i in x if i]
    if isinstance(x, str) and x.strip():
        return [x.strip()]
    return []

def _clean_text(x):
    if not x:
        return ""
    return re.sub(r"\s+", " ", str(x)).strip()

def _read_raw(path: str) -> Any:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text)
    return json.JSONDecoder(strict=False).decode(text)

def load_catalog(path: str) -> List[Dict[str, Any]]:
    raw = _read_raw(path)
    items = raw if isinstance(raw, list) else raw.get("data", [])

    out = []
    seen = set()

    for x in items:
        if not isinstance(x, dict):
            continue

        name = _clean_text(x.get("name", ""))
        url = _clean_text(x.get("link") or x.get("url") or "")
        if not name or not url or url in seen:
            continue

        seen.add(url)

        keys = _safe_list(x.get("keys"))
        job_levels = _safe_list(x.get("job_levels"))
        languages = _safe_list(x.get("languages"))
        desc = _clean_text(x.get("description", ""))

        test_type = "Other"
        joined = " ".join(keys).lower()
        if "knowledge" in joined:
            test_type = "K"
        elif "personality" in joined or "behavior" in joined:
            test_type = "P"
        elif "ability" in joined or "aptitude" in joined:
            test_type = "A"
        elif "simulation" in joined:
            test_type = "S"

        out.append({
            "entity_id": str(x.get("entity_id", "")),
            "name": name,
            "url": url,
            "link": url,
            "description": desc,
            "keys": keys,
            "job_levels": job_levels,
            "languages": languages,
            "duration": _clean_text(x.get("duration", "")),
            "remote": _clean_text(x.get("remote", "")),
            "adaptive": _clean_text(x.get("adaptive", "")),
            "test_type": test_type,
            "search_text": " ".join([
                name,
                desc,
                " ".join(keys),
                " ".join(job_levels),
                " ".join(languages),
                _clean_text(x.get("duration", "")),
                _clean_text(x.get("remote", "")),
                _clean_text(x.get("adaptive", "")),
            ])
        })

    return out
