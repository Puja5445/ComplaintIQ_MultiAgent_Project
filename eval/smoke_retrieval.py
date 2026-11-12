import core
reg = core.HybridIndex(core.load_reg_chunks())
print("REG_INDEX built:", len(reg.chunks), "chunks", flush=True)
tests = [
  ("error resolution timeline electronic fund transfer", "12CFR1005.11"),
  ("billing error notice credit card", "12CFR1026.13"),
  ("furnisher duties after receiving a direct dispute from a consumer", "12CFR1022.43"),
  ("limits on how often a debt collector may call a consumer", "12CFR1006.14"),
  ("12 CFR 1005.11", "12CFR1005.11"),
]
for q, gold in tests:
    ids = [h["chunk_id"] for h in reg.search(q, k=5)]
    ok = any(i.startswith(gold + "-") for i in ids)
    print("HIT " if ok else "MISS", "|", q, "|", ids, flush=True)
cases = core.HybridIndex(core.load_case_docs())
print("CASE_INDEX built:", len(cases.chunks), "stories", flush=True)
for h in cases.search("someone used my debit card at an ATM and I never made it", k=3):
    print(h["complaint_id"], "|", h["product"], "|", h["issue"], "|", h["rrf"])
