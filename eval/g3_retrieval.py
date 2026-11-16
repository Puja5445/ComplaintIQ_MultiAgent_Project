import re, numpy as np, pandas as pd
from g3_gold import GOLD_REG
from agents import REG_INDEX
from core import embed, tok

def hit(cid, pats): return any(re.match(p, cid) for p in pats)
missing = [g for it in GOLD_REG for g in it["gold"] if not any(re.match(g, c["chunk_id"]) for c in REG_INDEX.chunks)]
print("gold patterns with NO matching chunk (fix these):", missing)

def dense(q, k):
    _, I = REG_INDEX.faiss.search(embed([q]), k)
    return [REG_INDEX.chunks[i]["chunk_id"] for i in I[0] if i >= 0]
def bm25(q, k):
    s = REG_INDEX.bm25.get_scores(tok(q))
    return [REG_INDEX.chunks[i]["chunk_id"] for i in np.argsort(s)[::-1][:k]]
def hybrid(q, k):
    return [h["chunk_id"] for h in REG_INDEX.search(q, k=k)]

rows = []
for name, fn in {"dense": dense, "bm25": bm25, "hybrid": hybrid}.items():
    for item in GOLD_REG:
        ids = fn(item["q"], 8)
        ranks = [i for i, c in enumerate(ids, 1) if hit(c, item["gold"])]
        rows.append({"mode": name, "q": item["q"][:60], "hit5": int(bool(ranks) and ranks[0] <= 5),
                     "rr": round(1 / ranks[0], 3) if ranks else 0.0, "top5": ids[:5]})
df = pd.DataFrame(rows)
print(df.groupby("mode")[["hit5", "rr"]].mean().rename(columns={"hit5": "recall@5", "rr": "MRR"}))
print(df[(df["mode"] == "hybrid") & (df["hit5"] == 0)][["q", "top5"]].to_string())
df.to_csv("eval/g3_retrieval_results.csv", index=False)
