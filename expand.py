import json, hashlib, re, openai
from pathlib import Path
from config import EXPAND_MODEL
from core.cache import load_cache, save_cache
from core.extractors.registry import extract_text

CACHE_PATH = Path(".cache/expands.json")
_cache = load_cache(CACHE_PATH)

def _h(t): return hashlib.sha256(t.encode()).hexdigest()

def _title(name):
    base = name.rsplit(".", 1)[0]
    return re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", base)).strip()

def expand_document(file):
    key = _h(file.name)
    if key in _cache:
        return _cache[key]

    content = extract_text(file)
    fallback = _title(file.name)

    try:
        r = openai.ChatCompletion.create(
            model=EXPAND_MODEL,
            messages=[
                {"role": "system", "content": "문서를 분류하기 쉽게 정규화하라."},
                {"role": "user", "content": f"파일명:{file.name}\n내용:{content}"},
            ],
            temperature=0.2,
        )
        data = json.loads(r["choices"][0]["message"]["content"])
        if "embedding_text" not in data:
            raise ValueError
    except Exception:
        data = {
            "canonical_title": fallback,
            "keywords": fallback.split(),
            "domain": "기타",
            "embedding_text": f"제목: {fallback}",
        }

    _cache[key] = data
    save_cache(CACHE_PATH, _cache)
    return data
