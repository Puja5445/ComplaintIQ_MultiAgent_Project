import json
CH = {}
for l in open("data/processed/reg_chunks.jsonl"):
    c = json.loads(l); CH[c["chunk_id"]] = c["text"]
rows = [r for r in json.load(open("eval/g3_answers.json")) if r["kind"] == "answerable" and r["cited"]]
pick = rows[::max(1, len(rows) // 10)][:10]
out = ["# For each answer: all claims supported by the EVIDENCE = F, any not supported = U\n"]
for n, r in enumerate(pick, 1):
    out.append(f"\n## {n}. {r['q']}\n\n**Answer:**\n{r['answer'][:2500]}\n")
    for c in dict.fromkeys(r["cited"]):
        out.append(f"\n**Evidence [{c}]:** {CH.get(c, '')[:1500]}\n")
json.dump([r["q"] for r in pick], open("eval/label_questions.json", "w"))
open("eval/label_sheet.md", "w").write("\n".join(out))
print(len(pick), "answers in eval/label_sheet.md")
