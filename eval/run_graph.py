import sys
from langgraph.types import Command
from agents import app, LEDGER
tid = sys.argv[1]
cfg = {"configurable": {"thread_id": tid}}
complaint = open("samples/complaint_01.txt").read()
for update in app.stream({"request": complaint}, cfg, stream_mode="updates"):
    print(list(update.keys()))               # live view of which node just ran
snapshot = app.get_state(cfg)
if snapshot.next:                            # paused at the human_node interrupt
    print(snapshot.tasks[0].interrupts[0].value["draft"][:600])
    final = app.invoke(Command(resume={"action": "approve"}), cfg)
    print(final["report_uri"], "| cost so far: $", LEDGER.usd())
open("docs/graph.mmd", "w").write(app.get_graph().draw_mermaid())   # for the report
