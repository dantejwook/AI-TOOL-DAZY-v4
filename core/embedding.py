import hashlib, openai
from pathlib import Path
from config import EMBEDDING_MODEL
from core.cache import load_cache, save_cache

CACHE_PATH = Path(".cache/embeddings.json")
_cache = load_cache(CACHE_PATH)

def _h(t): return hashlib.sha256(t.encode()).hexdigest()

def embed_texts(texts):
    missing = [t for t in texts if _h(t) not in _cache]
    if missing:
        r = openai.Embedding.create(model=EMBEDDING_MODEL, input=missing)
        for t, d in zip(missing, r["data"]):
            _cache[_h(t)] = d["embedding"]
        save_cache(CACHE_PATH, _cache)
    return [_cache[_h(t)] for t in texts]
