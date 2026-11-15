# G2 analytics evaluation. same_result and the scoring loop are from PDF 7.2.
# The NaN clean-up, error handling and the unanswerable check are ours.
import math
from g2_gold import GOLD_SQL, UNANSWERABLE
from agents import run_sql, analyst_node, ANALYST_SYS, SQLOut, MODELS
from core import chat_json, LEDGER

# [PDF 7.2]
def same_result(a_rows, b_rows, ndigits=2):
    norm = lambda rows: sorted(tuple(round(v, ndigits) if isinstance(v, float) else v
                                     for v in r.values()) for r in rows)
    return norm(a_rows) == norm(b_rows)

# [MINE] NaN != NaN, so two identical results containing a NULL would look different
def clean(rows):
    return [{k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in r.items()}
            for r in rows]

score = []
for i, item in enumerate(GOLD_SQL, 1):          # [PDF 7.2] loop, with error handling added
    try:
        gold = clean(run_sql(item["gold_sql"]))
    except Exception as e:
        print(f"Q{i} GOLD SQL ERROR:", str(e)[:150]); score.append(False); continue
    res = analyst_node({"clean_request": item["q"], "intent": "ANALYTICS"})
    try:
        ok = same_result(gold, clean(res["sql_rows"]))
    except Exception:
        ok = False
    score.append(ok)
    print(f"Q{i}", "PASS" if ok else "FAIL", "| attempts:", res["trace"][0]["attempts"],
          "| gold rows:", len(gold), "| pred rows:", len(res["sql_rows"]), flush=True)
    if not ok:
        print("   pred SQL:", " ".join(res["sql"].split())[:300])
print("execution accuracy:", sum(score) / len(score), "(target >= 0.80)")

# [MINE] unanswerable questions: the PDF gives no code. The analyst should say in its
# 'explanation' that the data is missing. This keyword check is crude, so READ the printed text.
KEYS = ("not available", "no population", "not in the view", "cannot", "can't",
        "does not contain", "doesn't contain", "no data", "unable", "not contain")
ref = []
for q in UNANSWERABLE:
    out = chat_json(MODELS["worker"], ANALYST_SYS, q, SQLOut)
    ok = any(k in out.explanation.lower() for k in KEYS)
    ref.append(ok)
    print("UNANSWERABLE", "REFUSED" if ok else "NOT REFUSED", "|", q[:45], "|", out.explanation[:200])
print("correct refusals:", sum(ref), "/", len(ref))
print("LLM calls:", LEDGER.summary())
