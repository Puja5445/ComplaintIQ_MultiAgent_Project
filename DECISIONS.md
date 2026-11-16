# Decisions

## D1 - Judge model
- Brief asks for Opus 4.8 as judge.
- Probe result: Opus 4.8 gives AccessDenied in the lab account.
- Decision: probe picked Opus 5.5 automatically. Still a different, stronger model than the worker (Sonnet 4.6), so the judge stays independent.

## D2 - No narrative column
- CFPB API/CSV returns only 15 columns; "Consumer complaint narrative" is missing.
- Impact: triage, cases agent, G1. Waiting for trainer's decision.

## D3 - Synthetic narratives (trainer approved)
- CFPB no longer publishes the narrative column.
- Fake stories are written from real labels by a non-Claude model (writer), so triage (Sonnet) never grades its own family's text.
- Labels stay the ground truth; stories must not use label words.
- Limitation: synthetic text is cleaner than real complaints, so accuracy may look optimistic. Noted in report.

## D4 - Writer prompt fix
- Writer (Nova) sometimes wrote several complaints in one, split by '---'.
- Fix: prompt rule "exactly ONE complaint". Removed the bad rows and regenerated them. Final check: 360 stories, 0 bad.

## D5 - Chunking and retrieval follow the brief
- Chunking replaced with brief 2.3-2.5 (paragraph chunks 3000/400, ids like 12CFR1005.11-c0, source/page kept for citations).
- New lab allows Opus 4.8 (the brief's judge), so D1 no longer applies.

## D6 - Injection regex widened
- The brief's INJECTION regex allows only one word between "ignore" and "instructions", so "Ignore all previous instructions" was not flagged.
- Fix: allow several words in between. Brief's own G4 example uses this sentence and expects the flag.

## D7 - Bedrock access (open issue)
- Sonnet call returned AccessDenied (AWS Marketplace subscription) in the new lab. To retry tomorrow.

## D8 - Models changed (supersedes D7)
- Sonnet 4.6 gives a Marketplace AccessDenied in this lab. The probe found Sonnet 5 and Opus 5.5 working.
- Worker = Sonnet 5, judge = Opus 5.5 (different and stronger than worker). Writer stays Nova Lite (non-Claude). Embeddings stay Titan v2.
- Brief names Sonnet 4.6 / Opus 4.8; deviation is due to lab access only.

## D9 - chat() reads all text blocks
- Sonnet 5 can return a non-text (reasoning) block first, so the brief's content[0]["text"] raised KeyError.
- Fix: join every block that has "text". Rest of chat() is unchanged from the brief.

## D10 - Larger token limits for reasoning models
- Brief uses max_tokens 1800 (drafter) and 800 (critic). Sonnet 5 / Opus 5.5 use part of the limit for reasoning, so replies were cut off or empty.
- Raised to 3000 for both. Logic unchanged.

## D11 - Critic sees the same evidence length as the drafter
- Drafter shows 1500 chars per chunk, critic 1200, so the critic rejected valid citations as "truncated". Critic raised to 1500.

## D12 - SLA node (our innovation, not in the brief)
- Plain-code node between triage and cases. Maps triage to Reg E (10 business days, 45 days) or Reg Z (30 days, 90 days), computes due dates, marks ON_TRACK / AT_RISK / BREACHED, and puts vulnerable customers first.
- Windows checked against our downloaded regulation chunks (1005.11 and 1026.13).
- Limits: business days ignore public holidays, and Reg E uses 45 days only (some transactions get 90).

## D13 - JSON schema sent on the first call
- Brief's chat_json shows the schema only in the repair call, so triage needed 2 calls per story (120 calls for 60 stories).
- Fix: put the schema in the system prompt on the first call. Now 60 calls.
- G1 after fix: product accuracy 1.0, issue macro-F1 0.811. Before: 0.983 / 0.652.
- Caveat: stories are synthetic and written from the labels, so scores are likely optimistic.

## D14 - Analyst fixes found by G2 (failure analyses 1 and 2)
- Q4: ILIKE '%monetary relief%' also matches 'non-monetary relief', so shares were inflated (26.22 vs 15.93). Fix: prompt lists exact company_response values and says use =. G2: 0.6 -> 0.8.
- Q2: model SQL ended with ';' and the brief's LIMIT wrapper put it inside brackets (syntax error). Fix: strip trailing ';' in guard_sql.
- Unanswerable (per 100k residents): model hardcoded census populations instead of refusing. Fix: prompt rule to start explanation with 'CANNOT ANSWER:'.

## D15 - G3 retrieval (15 questions)
- recall@5: BM25 0.93, dense 1.00, hybrid 1.00. MRR: 0.73 / 0.97 / 0.97. Hybrid ties dense on plain-English questions; BM25 is weaker. Set is 15 questions, not 20.

## D16 - Judge calibration (10 answers)
- Opus judge vs my labels: agreement 0.70, Cohen kappa 0.4. Judge faithfulness 0.6, my labels 0.5 (target 0.90 not met).
- Disagreements #1, #3, #6. I saw only cited chunks; the judge saw all 8 retrieved chunks (unconfirmed explanation).
- Not re-run because of the $5 lab budget.
