**ComplaintIQ – Multi-Agent Complaint Intelligence (LangGraph + AWS Bedrock)**
Turns bank complaints into triage, SQL answers, cited regulatory answers and human-approved drafts.

Prerequisites
AWS SageMaker Studio, region us-east-1, Bedrock model access (see models.json)
Python 3.10+
Run (≤10 commands)
git clone https://github.com/Puja5445/ComplaintIQ_MultiAgent_System.git   # 1
cd ComplaintIQ_MultiAgent_System                                          # 2
pip install -r requirements.txt                                           # 3
aws sts get-caller-identity                                               # 4 check credentials
aws s3 sync s3://<your-sagemaker-bucket>/complaintiq/ .                   # 5 restore data (or skip and re-download in step 6)
python data.py                                                            # 6 <confirm: download/build data and indexes>
python core.py                                                            # 7 <confirm: smoke test>
python agents.py                                                          # 8 <confirm: run the graph>
Folder map
data.py – data download, cleaning, DuckDB, indexes
core.py – shared helpers (Bedrock calls, retrieval, guards)
agents.py – LangGraph nodes and graph
models.json – probed Bedrock model IDs
DECISIONS.md – design decisions
docs/, eval/, reports/, samples/ – supporting material
Status
Phases 0–7 (up to gate G4) done.
Phases 7.3 and 8 (full evaluation) and the demo video were not completed because the lab budget ran out.
README steps were not re-tested in a new Studio space because the lab was unavailable.
