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
