# G3 end to end through the full graph. Questions come from g3_gold.py. Code is ours.
import json, re, time
import numpy as np
from g3_gold import GOLD_REG, ABSTAIN
from agents import app, LEDGER

PHRASES = ("insufficient", "not contain", "does not address", "do not address", "not enough",
           "no information", "cannot answer", "not covered", "unable to", "not in the")

def run(q, tag):
    cfg = {"configurable": {"thread_id": f"g3-{tag}-{int(time.time())}"}}
    t0, nodes = time.time(), []
    for u in app.stream({"request": q}, cfg, stream_mode="updates"):
        nodes += list(u.keys())
    snap = app.get_state(cfg)
    return snap.values, nodes, round(time.time() - t0, 1), bool(snap.next)

jobs = [("answerable", it["q"]) for it in GOLD_REG] + [("abstain", q) for q in ABSTAIN]
rows = []
for i, (kind, q) in enumerate(jobs):
    try:
        v, nodes, secs, paused = run(q, f"{kind}{i}")
    except Exception as e:
        print("ERROR", i, type(e).__name__, str(e)[:120], flush=True)
        continue
    draft = v.get("draft", "")
    known = {e["chunk_id"] for e in v.get("evidence", [])}
    cited = re.findall(r"\[C:([^\]]+)\]", draft)
    bad = [c for c in cited if c not in known]
    rows.append({"kind": kind, "q": q, "intent": v.get("intent"), "answer": draft,
                 "evidence": [{"chunk_id": e["chunk_id"], "text": e["text"][:800]} for e in v.get("evidence", [])],
                 "cited": cited, "bad_cites": bad, "paused": paused,
                 "critic_pass": v.get("critique", {}).get("pass"), "revisions": v.get("revisions"),
                 "abstained": v.get("intent") == "OUT_OF_SCOPE" or any(p in draft.lower() for p in PHRASES),
                 "seconds": secs, "nodes": nodes})
    print(i, kind, v.get("intent"), "| cites", len(cited), "| bad", len(bad), "|", secs, "s", flush=True)

json.dump(rows, open("eval/g3_answers.json", "w"), indent=1)
ans = [r for r in rows if r["kind"] == "answerable"]
ab = [r for r in rows if r["kind"] == "abstain"]
print("\nanswerable run:", len(ans), "| routed to REG_QA:", sum(r["intent"] == "REG_QA" for r in ans))
print("citation validity:", sum(not r["bad_cites"] for r in ans) / len(ans), "(target 1.00)")
print("answers with at least one citation:", sum(bool(r["cited"]) for r in ans), "/", len(ans))
print("escalated to human after 2 revisions:", sum(r["paused"] for r in ans))
print("latency p50/p95 (s):", np.percentile([r["seconds"] for r in rows], [50, 95]))
for r in ab:
    print("\nABSTAINED?", r["abstained"], "| intent", r["intent"], "|", r["q"][:50], "\n  ", r["answer"][:250].replace("\n", " "))
print("LLM calls:", LEDGER.summary())
