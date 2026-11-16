# ComplaintIQ report resume-test-1

# A. Internal Case Note

**Case Type:** Alleged unauthorized EFT (debit card ATM withdrawals) – Regulation E / EFTA
**Severity:** CRITICAL
**Vulnerable Customer Flag:** YES — customer reports being 72 years old; alleged fraud reportedly outstanding approximately 3 weeks [per triage/customer statement]

**Summary of Allegation:**
Customer alleges two unauthorized $500 ATM withdrawals on debit card, dated 3/3 per customer's statement. Customer states notice was given to the institution the same day. Customer states no resolution has been issued as of this review, roughly three weeks post-notice per customer's account. These are customer allegations only; they have not been independently verified or admitted by the institution. [Note: DATA provided for this case was empty — all dates/amounts above are drawn solely from the customer's narrative and must be confirmed against internal systems before being treated as fact.]

**Regulatory Context:**
- 12 CFR 1005.11 defines what constitutes an "error" under Regulation E and sets out the steps a consumer must take to assert an error, as well as the procedures a financial institution must follow in response [C:exam_manual-p699-c1].
- Regulation E specifies that a consumer gives valid notice when reasonable steps are taken to inform the institution, regardless of which employee receives it, and that notice may be given in person, by phone, or in writing [C:exam_manual-p699-c0]. This provision addresses notice for purposes of limiting consumer liability under 1005.6; it does not itself establish when the institution's error-resolution review clock begins under 1005.11, and no chunk in evidence addresses that timing. This should be confirmed against the institution's own Reg E procedures.
- Consumer liability for unauthorized EFTs depends on the timing of the consumer's notice to the institution relative to discovery of loss/theft of the access device, and the EFTA imposes no bright-line reporting deadline [C:exam_manual-p697-c0]. Regulation E prohibits using certain other factors (e.g., an institution-consumer agreement purporting to impose greater liability) as a basis for liability beyond what the regulation permits [C:exam_manual-p697-c0]. Specific maximum-liability tiers based on notice timing are set out in the consumer liability chart [C:exam_manual-p698-c0]. This framework governs consumer liability exposure; it does not constitute an admission of institutional fault or delay.

**Action Items:**
1. **Urgent**: Confirm date/time/method of original fraud notice in call logs, branch notes, or app/online dispute submission; verify against customer's stated 3/3 notice date.
2. Pull ATM transaction logs, camera footage (if available), and card-present data for the two disputed $500 withdrawals.
3. Confirm current investigation/provisional-credit status per internal Reg E procedures; escalate to Fraud/Reg E Compliance team if outstanding beyond internal SLA, flagging elderly/vulnerable customer status.
4. Confirm whether a written/formal error notice (vs. verbal) was required and obtained, per institution's Reg E procedures.
5. Prepare investigation findings letter; do not characterize the withdrawals as confirmed fraud — refer to them as "the disputed transactions" pending investigation outcome.
6. Elder financial exploitation protocol: given vulnerable customer flag, route to specialized elder-fraud review team per internal policy, in addition to standard Reg E path.
7. Do not communicate any admission of institutional delay or liability to customer; all communications should reference "investigation in progress" language only.

**Risk Note:** If elapsed time since notice is confirmed and exceeds internal/regulatory timeframes without resolution, this poses regulatory and reputational risk (CFPB complaint potential, elder abuse scrutiny). Recommend compliance/legal review within 24 hours.

---

# B. Customer Reply

Dear [Customer Name],

Thank you for reaching out, and I'm sorry to hear about the stress this situation has caused. I understand you are reporting two $500 ATM withdrawals from your debit card on March 3rd that you say you did not make, and that you notified us the same day. I want to assure you we are taking this seriously and are actively looking into it.

I want to be clear that at this stage, these withdrawals are being treated as a *reported* issue under review — our team has not yet made a final determination, and I can't confirm or speculate on the outcome until the investigation is complete.

Here's what you should know about the process:

- Under federal consumer protection rules (Regulation E), when a customer asserts a potential error on an electronic fund transfer, there are defined steps the customer takes to report it and defined procedures we must follow to investigate it [C:exam_manual-p699-c1].
- Notice can be given in person, by phone, or in writing, and is considered given as soon as a customer takes reasonable steps to provide the relevant information to us — so you reporting this to us the same day it occurred is meaningful and has been factored into how we're handling your case [C:exam_manual-p699-c0].

I'm escalating your case for priority review today. You should hear from a member of our fraud resolution team within **[X] business days** with either a status update, a provisional credit, or a final determination.

In the meantime, please let us know if you'd like to:
- Request a written summary of your original fraud report for your records, or
- Have a family member or trusted representative included in further conversations about this case.

We appreciate your patience, and we're committed to getting you a clear answer as quickly as possible.

Sincerely,
[Name]
[Institution] Customer Resolutions Team

## Trace
```json
[
  {
    "node": "guard",
    "flags": []
  },
  {
    "node": "router",
    "intent": "TRIAGE",
    "reason": "Customer describes a specific unauthorized ATM withdrawal complaint and unresolved refund issue needing classification and response drafting."
  },
  {
    "node": "triage",
    "severity": "CRITICAL"
  },
  {
    "node": "cases",
    "n": 5
  },
  {
    "node": "research",
    "ids": [
      "exam_manual-p699-c1",
      "exam_manual-p699-c0",
      "exam_manual-p697-c0",
      "exam_manual-p698-c0",
      "exam_manual-p695-c0",
      "exam_manual-p691-c0",
      "exam_manual-p719-c0",
      "exam_manual-p677-c0"
    ]
  },
  {
    "node": "drafter",
    "revision": 0
  },
  {
    "node": "critic",
    "pass": false,
    "problems": 1
  },
  {
    "node": "drafter",
    "revision": 1
  },
  {
    "node": "critic",
    "pass": false,
    "problems": 0
  },
  {
    "node": "human",
    "action": "approve"
  }
]
```
