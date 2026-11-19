# app.py  ->  streamlit run app.py --server.port 8501
# Streamlit UI for ComplaintIQ. Template from the project brief, Phase 8 (Option B).
# Brief lines are marked [PDF]; our small additions are marked [MINE].
import uuid, streamlit as st
from langgraph.types import Command
from agents import app, LEDGER                      # [PDF] was: from complaintiq.graph import app, LEDGER

st.title("ComplaintIQ")                             # [PDF]
tid = st.session_state.setdefault("tid", str(uuid.uuid4()))   # [PDF]
cfg = {"configurable": {"thread_id": tid}}                    # [PDF]

if st.sidebar.button("New case"):                   # [MINE] fresh thread id, because the brief says use a new thread per case
    st.session_state["tid"] = str(uuid.uuid4())
    st.rerun()

req = st.text_area("Paste a complaint, or ask a question")    # [PDF]
if st.button("Run") and req:                                  # [PDF]
    with st.spinner("Running the agents..."):                 # [MINE]
        app.invoke({"request": req}, cfg)                     # [PDF]
    st.rerun()                                                # [MINE] show the new state straight away

snap = app.get_state(cfg)                                     # [PDF]
if snap.next:                                                 # [PDF] paused at the human node
    payload = snap.tasks[0].interrupts[0].value
    st.subheader("Draft awaiting approval"); st.markdown(payload["draft"])
    edited = st.text_area("Edit (optional)", payload["draft"])
    c1, c2, c3 = st.columns(3)
    if c1.button("Approve"):
        app.invoke(Command(resume={"action": "approve"}), cfg); st.rerun()       # [PDF] + [MINE] rerun
    if c2.button("Save edit"):
        app.invoke(Command(resume={"action": "edit", "text": edited}), cfg); st.rerun()
    if c3.button("Reject"):
        app.invoke(Command(resume={"action": "reject"}), cfg); st.rerun()
elif snap.values.get("draft"):                                # [PDF]
    st.markdown(snap.values["draft"])
    if snap.values.get("human_decision"):                     # [MINE] show what the human decided
        st.info(f"Human decision: {snap.values['human_decision'].get('action')}")
    if snap.values.get("report_uri"):                         # [MINE]
        st.success(f"Report saved: {snap.values['report_uri']}")
if snap.values.get("intent"):                                 # [MINE] journey, flags, labels, SLA in one place
    with st.expander("Details: journey, flags, triage, SLA, critic"):
        st.json({k: snap.values.get(k) for k in ("intent", "flags", "triage", "sla", "critique") if snap.values.get(k)})
with st.expander("Trace"): st.json(snap.values.get("trace", []))    # [PDF]
st.caption(f"Session cost: ${LEDGER.usd()}")                  # [PDF]
