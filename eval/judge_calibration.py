# Judge calibration: Opus checks 10 G3 answers; compared with YOUR hand labels.
import json
from typing import Literal
from pydantic import BaseModel
from sklearn.metrics import cohen_kappa_score
from core import chat_json, LEDGER

MODELS = json.load(open("models.json"))

class FaithOut(BaseModel):
    verdict: Literal["FAITHFUL", "UNFAITHFUL"]
    reason: str

JUDGE_SYS = ("You check an ANSWER against its EVIDENCE. FAITHFUL only if every factual claim "
             "in the ANSWER is supported by the EVIDENCE. UNFAITHFUL if any claim is unsupported "
             "or contradicted. Ignore style and length.")

CH = {}
for l in open("data/processed/reg_chunks.jsonl"):
    c = json.loads(l); CH[c["chunk_id"]] = c["text"]

qs = json.load(open("eval/label_questions.json"))
by_q = {r["q"]: r for r in json.load(open("eval/g3_answers.json")) if r["kind"] == "answerable"}
human = ["FAITHFUL" if x.strip() == "F" else "UNFAITHFUL"
         for x in open("eval/human_labels.txt").read().split(",")]
assert len(qs) == len(human) == 10, "need exactly 10 labels"

judge, reasons = [], []
for q in qs:
    r = by_q[q]
    ev = "\n\n".join(f"[{e['chunk_id']}] {CH.get(e['chunk_id'], e['text'])[:1500]}" for e in r["evidence"])
    out = chat_json(MODELS["judge"], JUDGE_SYS, f"EVIDENCE:\n{ev}\n\nANSWER:\n{r['answer']}",
                    FaithOut, max_tokens=3000)
    judge.append(out.verdict); reasons.append(out.reason)

print("faithfulness (judge, 10 answers):", sum(v == "FAITHFUL" for v in judge) / 10, "(target >= 0.90)")
print("faithfulness (your labels)      :", sum(v == "FAITHFUL" for v in human) / 10)
print("agreement with your labels:", sum(a == b for a, b in zip(human, judge)) / 10, "(need >= 0.70)")
print("Cohen kappa:", cohen_kappa_score(human, judge))
for n, (h, j, why) in enumerate(zip(human, judge, reasons), 1):
    if h != j:
        print(f"DISAGREE #{n}: you={h} judge={j} | {why[:200]}")
print("LLM calls:", LEDGER.summary())
