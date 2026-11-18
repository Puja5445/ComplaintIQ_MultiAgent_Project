# join_narratives.py
# Purpose: create the DuckDB view v_narratives = v_complaints + the 360 synthetic stories
# (data/processed/narratives.jsonl, committed in Git). Run once after `python data.py`.
# The raw CSV is never changed; stories are joined by complaint_id.
import pathlib, sys, duckdb

ROOT = pathlib.Path(__file__).resolve().parent
DB = ROOT / "data" / "complaintiq.duckdb"
STORIES = ROOT / "data" / "processed" / "narratives.jsonl"

if not DB.exists():
    sys.exit("data/complaintiq.duckdb not found - run `python data.py` first and wait for it to finish.")
if not STORIES.exists():
    sys.exit("data/processed/narratives.jsonl not found - it is committed in Git; re-clone or restore it.")

con = duckdb.connect(str(DB))
con.execute(f"""CREATE OR REPLACE VIEW v_narratives AS
    SELECT c.*, n.narrative, n.split FROM v_complaints c
    JOIN read_json_auto('{STORIES}') n ON c.complaint_id = n.complaint_id""")
counts = dict(con.execute("SELECT split, COUNT(*) FROM v_narratives GROUP BY 1").fetchall())
con.close()
print("stories joined:", counts, "(expected train 300, test 60)")
if counts.get("train") != 300 or counts.get("test") != 60:
    print("WARNING: fewer stories than expected. CFPB updates its data, so a few complaint ids may "
          "have changed since the stories were written.")
