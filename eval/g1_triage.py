# G1 triage evaluation. Harness from PDF 7.2; data source and confusion printout are ours.
from sklearn.metrics import accuracy_score, f1_score
from agents import ro, triage_node
from core import LEDGER

# [MINE] 60 June synthetic stories, ground truth = real CFPB product and issue
holdout = ro.execute("""SELECT complaint_id, narrative, product, issue FROM v_narratives
                        WHERE split = 'test'""").df()
print("rows:", len(holdout), flush=True)

# [PDF 7.2]
preds = []
for row in holdout.itertuples():
    out = triage_node({"clean_request": row.narrative})["triage"]
    preds.append((out["product"], out["issue"]))

holdout["pred_product"], holdout["pred_issue"] = zip(*preds)
print("product accuracy :", accuracy_score(holdout["product"], holdout["pred_product"]))
print("issue macro-F1   :", f1_score(holdout["issue"], holdout["pred_issue"], average="macro"))
holdout.to_csv("eval/triage_results.csv", index=False)

# [MINE] which issues get confused most (for the report and viva)
wrong = holdout[holdout["issue"] != holdout["pred_issue"]]
print("\nmost confused (true issue -> predicted issue):")
print(wrong.groupby(["issue", "pred_issue"]).size().sort_values(ascending=False).head(10))
print("\nLLM calls so far:", LEDGER.summary())
