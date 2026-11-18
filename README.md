# ComplaintIQ - multi-agent complaint intelligence (LangGraph + AWS Bedrock)

Turns bank-complaint text into triaged cases, SQL answers, cited regulatory answers and
**human-approved** drafts. Agentic AI capstone project (fictional "Harbourline Bank"; all data is public CFPB / eCFR data).

| Journey | Request | Output |
|---|---|---|
| J1 Triage | A complaint narrative | Product, issue, severity, vulnerable flag, SLA risk, similar cases, cited draft reply (human approval) |
| J2 Analytics | A data question | SQL, result rows, cited answer |
| J3 Regulation Q&A | A question about a regulation | Answer with `[C:chunk_id]` citations, or an abstention |
| J4 Brief | A monthly trend brief | Data trends + regulation context + actions (human approval) |

**Graph (12 nodes):** guard > router > triage > **sla** > cases > research / analyst > drafter > critic (max 2 revisions) > human `interrupt()` > publish; refuse for out-of-scope.
5 nodes call Claude (router, triage, analyst, drafter, critic); the rest are plain code, retrieval or the human step.
`sla` is my own addition (regulatory deadline risk, not in the brief). See `docs/agent_graph.png`, `docs/architecture.png`, `docs/graph.mmd`.

## Prerequisites
- AWS **SageMaker Studio JupyterLab**, region **us-east-1**, Python 3.12 (as used in Studio).
- **Bedrock access** in my account to: a Claude Sonnet model (worker), a Claude Opus model (judge) and
  Titan Text Embeddings v2. A non-Claude writer model (Amazon Nova Lite) is needed only to regenerate the fake stories.
  `models.json` lists the ids used in my lab; step 7 below re-probes them for my account.
- AWS credentials come from the Studio role. **No keys are stored in this repo.**
  `data.py` asks AWS (STS) for the account id, so run it inside the lab or with a configured AWS CLI profile.
- Cost: the Bedrock calls are billable (details under "Evaluation"). The LLM and embedding caches live in `state/` and `index/`,
  which are not in Git, so a fresh clone pays full price once.

## Run from a clean clone (10 commands)
```bash
git clone https://github.com/Puja5445/ComplaintIQ_MultiAgent_System.git      # 1
cd ComplaintIQ_MultiAgent_System                                             # 2
pip install -r requirements.txt                                              # 3  (dependency-conflict warnings about other Studio packages are harmless)
aws sts get-caller-identity                                                  # 4  check login (region must be us-east-1)
python data.py                                                               # 5  download 12 files + manifest.json, build DuckDB, 1,759 chunks (10+ min; the 924-page manual is slow)
python join_narratives.py                                                    # 6  join the 360 synthetic stories -> view v_narratives (expect train 300, test 60)
python -c "import core; core.probe_models(); core.probe_writer()"            # 7  OPTIONAL: re-probe models for your account (rewrites models.json)
PYTHONPATH=. python eval/smoke_retrieval.py                                  # 8  build the two search indexes (Titan embeddings) and run 5 law queries
PYTHONPATH=. python eval/run_graph.py case-0001                              # 9  demo J1: triage > pause at human > approve > report
PYTHONPATH=. python eval/run_all.py                                          # 10 J2, J3, J4, out-of-scope and injection requests
```
Wait for step 5 to finish before step 6 onward (the agents open DuckDB read-only). Do **not** run `python core.py` on its own: it re-runs the model probe and drops the `writer` entry from `models.json`.

**Expected output**
- Step 5: `12 files saved in data/manifest.json`, the product counts (about 93.7k complaints; CFPB updates its data, so counts can differ by a few), train/test counts, then `1759 chunks saved`.
- Step 8: 4 of 5 law queries print `HIT`; the query `12 CFR 1005.11` is a known miss (the section number is in the chunk id, not its text). Then 3 similar complaints.
- Step 9: node names in order (`guard, router, triage, sla, cases, research, drafter, critic`), the draft, then an `s3://.../reports/case-0001.md` path (a local copy is also written to `reports/`).
- Step 10: one line per request, e.g. J2 `analyst > drafter > critic > publish`, injection `refuse`.
- Use a new thread id for every run of step 9 (`case-0002`, ...); re-using one replays the old history.

**Restore from S3 instead of step 5** (only if you have the author's backup): `aws s3 sync s3://sagemaker-complaintiq-<account>/complaintiq/data/ data/`

### Pause and resume across a restart (J1 stops at the human step)
```bash
PYTHONPATH=. python -c "
from agents import app
cfg={'configurable':{'thread_id':'resume-test-1'}}
for u in app.stream({'request':open('samples/complaint_01.txt').read()},cfg,stream_mode='updates'): print(list(u.keys()))
print('PAUSED, next =', app.get_state(cfg).next)"
# new process = simulated restart; state comes back from state/checkpoints.sqlite
PYTHONPATH=. python -c "
from agents import app
from langgraph.types import Command
cfg={'configurable':{'thread_id':'resume-test-1'}}
print('after restart, next =', app.get_state(cfg).next)
print(app.invoke(Command(resume={'action':'approve'}),cfg)['report_uri'])"
```

## Evaluation (`eval/`)
Run from the repo root with `PYTHONPATH=.`. Costs are our estimates at list prices; the usage page lagged, so check your own budget first.

| Script | What it measures | Size run | Notes |
|---|---|---|---|
| `g1_triage.py` | G1 product accuracy, issue macro-F1 | 60 June synthetic stories | 60 Sonnet calls |
| `g2_sql.py` (+ `g2_gold.py`) | G2 SQL execution accuracy, refusal of unanswerable | 5 + 1 unanswerable | |
| `g3_retrieval.py` (+ `g3_gold.py`) | G3 recall@5 and MRR, dense vs BM25 vs hybrid (A2) | 15 questions | free after step 8 |
| `g3_e2e.py` | G3 through the full graph: citation validity, abstention, latency | 15 + 3 not in corpus | 84 calls, about $1.4-2.7 |
| `make_label_sheet.py`, `judge_calibration.py` | Opus faithfulness judge vs the author's 10 hand labels (`human_labels.txt`) | 10 answers | about $0.31 |
| `g4_run.py vuln1 inj1` | G4 end-to-end: vulnerable customer and injection attempt | 2 of 10 written | about $0.17 |

Saved outputs: `eval/results/`, `eval/triage_results.csv`, `eval/g3_answers.json`, `eval/g4_outputs.md`.

| Metric | Target | Result |
|---|---|---|
| G1 product accuracy / issue macro-F1 | >= 0.85 / >= 0.45 | 1.00 / 0.811 (optimistic: stories were written from the labels) |
| G2 execution accuracy | >= 0.80 | 1.00 on 5 questions (0.6 before two fixes) |
| G3 recall@5 (hybrid) | >= 0.80 | 1.00 on 15 (BM25 0.93, dense 1.00) |
| G3 citation validity | 1.00 | 1.00 |
| Judge faithfulness / agreement / Cohen's kappa | >= 0.90 / >= 0.70 | 0.6 / 0.70 / 0.40 (not met) |
| G3 p95 latency | <= 60 s | 59.9 s |

## Repository layout
```
data.py              config, download (12 files + manifest.json), DuckDB views, chunking
core.py              model probe, Bedrock wrapper (retries, cache, cost ledger, chat_json), fake-story writer, Titan + FAISS + BM25 + RRF
agents.py            state, guard, router, triage, sla, cases, analyst, research, drafter, critic, human, publish, refuse, graph + SQLite checkpointer
join_narratives.py   creates view v_narratives (labels + 360 synthetic stories)
models.json          output of the model probe (no secrets)
DECISIONS.md         why each choice was made and what broke
eval/  samples/  reports/  docs/
```
Layout differs from the brief's `src/` example: three modules instead of many small files. Data (`data/raw`, `data/processed`, DuckDB) and caches are rebuilt by script and are not in Git; `data/manifest.json` and `data/processed/narratives.jsonl` are.

## Data note: synthetic narratives
CFPB no longer publishes the *Consumer complaint narrative* column, so the 15 columns we get are labels only. With the trainer's approval,
360 customer stories (300 Jan-May, 60 June) were generated from the **real labels** by a **different model family** (Nova Lite) than the one used for triage (Claude).
The labels stay the ground truth. See `docs/data_card.md` and `DECISIONS.md` (D3, D4).

## Safety controls
PII redaction in the guard and re-check in the critic; `<request>` tags plus an injection flag; citation ids verified in code; SQL guard (single SELECT, allow-listed view, LIMIT, read-only connection);
`interrupt()` before publishing J1/J4; one audit line per request without raw request text. Region is fixed to us-east-1 and all inference goes through Bedrock.

## Status and known limitations
- **Done:** phases 0-6 and most of phase 7: G1 (60), G2 (5 of 20), G3 (15 of 20), A2 retrieval comparison, judge calibration, and the **G4 golden set** for 2 of 10 complaints.
- **Not done:** baselines B0, B1 and A1; full-size golden sets; Streamlit UI; demo video. The lab budget ($5) was exceeded (usage page showed $8.17) and the lab was suspended.
- **Open defects:** the critic sent 8 of 15 G3 answers to a human after two rejections; one G4 draft came back empty (likely hit its output-token limit); section-number queries miss in retrieval; short numbers like `555-0142` are not redacted; the SLA node ignores public holidays and uses Reg E's 45-day window only.
- **README not re-tested:** the commands above come from what ran in the lab, but a fresh Studio space was not available to re-run them end to end.
- Report: `docs/report.pdf`.
