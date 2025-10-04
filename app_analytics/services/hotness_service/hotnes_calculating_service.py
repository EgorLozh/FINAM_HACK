"""
hotness_scoring_chroma.py

Версия скрипта с интеграцией ChromaDB.
Используется для расчёта hotness новостей с учётом истории из векторного хранилища.
"""

from typing import Optional, Dict, Any, List
import math, re, json, numpy as np

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# ====================== CONFIG ======================
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
CHROMA_COLLECTION = "news_hotness"

ALPHA = {
    "surprise": 0.25,
    "materiality": 0.25,
    "velocity": 0.15,
    "breadth": 0.15,
    "credibility": 0.20,
}

GAMMA_DUP = 2.0
DELTA_REGIME = 0.3

FIN_KEYWORDS = [
    "убыт", "прибыл", "earnings", "eps", "guidance", "дивиденд", "дефолт",
    "банкрот", "штраф", "санкц", "loss", "profit", "layoff", "revenue",
    "процент", "%", "облигац", "долг", "задолж", "снижен", "рост"
]

# ====================== INIT MODELS ======================
sentiment_pipe = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
embed_model = SentenceTransformer(EMBED_MODEL)

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=SentenceTransformerEmbeddingFunction(EMBED_MODEL)
)

# ====================== FEATURES ======================
def calc_sentiment(text: str) -> float:
    out = sentiment_pipe(text[:512])[0]
    label, score = out["label"].lower(), out["score"]
    if "neg" in label or "1" in label or "2" in label: return -score
    if "pos" in label or "4" in label or "5" in label: return score
    return 0.0

def calc_materiality(text: str) -> float:
    txt = text.lower()
    s = sum(1 for k in FIN_KEYWORDS if k in txt) * 0.05
    if re.search(r"\\d+\\s*%|млрд|миллиард|billion|trillion", txt):
        s += 0.2
    return min(1.0, s)

def calc_breadth(text: str) -> float:
    ents = set(re.findall(r"[A-ZА-ЯЁ][A-Za-zА-Яа-яёЁ\\-]{2,}", text))
    return min(1.0, len(ents) / 20)

def calc_velocity(recent: Optional[int], avg: Optional[float]) -> float:
    if not recent or not avg or avg == 0: return 0
    z = (recent - avg) / math.sqrt(avg + 1e-6)
    return 1 / (1 + math.exp(-0.5 * z))

def calc_credibility(source: Optional[str], confirmations: Optional[int]) -> float:
    base = 0.5
    if source and any(k in source.lower() for k in ["bloomberg", "reuters", "wsj", "vedomosti"]):
        base = 0.9
    c = confirmations or 0
    conf = 1 - math.exp(-0.3 * c)
    return 0.6 * base + 0.4 * conf

# ====================== CHROMA FEATURES ======================
def get_surprise_and_dup(text: str, limit: int = 50) -> Dict[str, float]:
    """Находит похожие новости в Chroma, вычисляет surprise и dup_ratio"""
    query = collection.query(query_texts=[text], n_results=limit)
    if not query["documents"]:
        return {"surprise": 0.5, "dup_ratio": 0.0}

    sims = query["distances"][0]  # cosine distances (0=identical)
    if len(sims) == 0: return {"surprise": 0.5, "dup_ratio": 0.0}

    # Chroma хранит distance ~ (1 - cos_sim)
    cos_sims = [1 - d for d in sims]
    avg_sim = np.mean(cos_sims)
    surprise = 1 - avg_sim
    dup_ratio = float(sum(1 for s in cos_sims if s > 0.9) / len(cos_sims))
    return {"surprise": max(0, min(1, surprise)), "dup_ratio": dup_ratio}

def add_to_chroma(text: str, meta: Dict[str, Any]):
    collection.add(
        ids=[meta.get("id", str(hash(text)))],
        documents=[text],
        metadatas=[meta]
    )

# ====================== HOTNESS ======================
def aggregate_hotness(f_sur, f_mat, f_vel, f_brd, f_cred, dup_ratio=0.0, regime_z=0.0):
    base = (ALPHA['surprise'] * f_sur + ALPHA['materiality'] * f_mat +
            ALPHA['velocity'] * f_vel + ALPHA['breadth'] * f_brd +
            ALPHA['credibility'] * f_cred)
    dup_pen = math.exp(-GAMMA_DUP * dup_ratio)
    regime_mult = 1 + DELTA_REGIME * regime_z
    return max(0.0, min(1.0, base * dup_pen * regime_mult))

# ====================== MAIN ======================
def score_article(
    text: str,
    source: Optional[str] = None,
    recent_count: Optional[int] = None,
    avg_count: Optional[float] = None,
    confirmations: Optional[int] = None,
    add_to_history: bool = True,
    regime_z: float = 0.0
) -> Dict[str, Any]:

    sent = calc_sentiment(text)
    mat = calc_materiality(text)
    brd = calc_breadth(text)
    vel = calc_velocity(recent_count, avg_count)
    cred = calc_credibility(source, confirmations)

    chroma_feats = get_surprise_and_dup(text)
    f_sur = chroma_feats["surprise"]
    dup_ratio = chroma_feats["dup_ratio"]

    hot = aggregate_hotness(f_sur, mat, vel, brd, cred, dup_ratio, regime_z)

    if add_to_history:
        add_to_chroma(text, {"source": source, "hotness": hot})

    return {
        "hotness": hot,
        "sentiment": sent,
        "surprise": f_sur,
        "materiality": mat,
        "velocity": vel,
        "breadth": brd,
        "credibility": cred,
        "dup_ratio": dup_ratio,
    }

# ====================== DEMO ======================
if __name__ == "__main__":
    sample_text = "Газпром сообщил об убытках за третий квартал 2025 года из-за падения экспорта."
    res = score_article(sample_text, source="t.me/finnews", recent_count=120, avg_count=5, confirmations=2)
    print(json.dumps(res, ensure_ascii=False, indent=2))
