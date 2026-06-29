# change3.md — Add the entry-price finding & conditional framing, then ready for push

**For:** Claude Code, executing inside the repo
`PE_Battery-Energy-Storage-System-BESS`, on top of `change.md` and `change2.md`
(latest commit `563b113`).

**Why this brief exists.** The model is verified and consistent. Two small
additions make the memo more accurate and decision-ready before it's pushed:

1. The central-case result is underwater mainly because we'd **pay more than
   the company is worth on day one** (~$10.0m post-money vs ~$7.2m base-case
   pipeline value). That entry-price gap is the real finding and it isn't yet
   stated plainly. The actionable lever is **price**, not pipeline depth.
2. The headline ("−2.6% / value-destructive") rests on `[[TO CONFIRM]]`
   placeholders (pre-money $8m, pipeline depth 25, distribution fraction). It
   must read as **conditional analysis**, not a flat verdict on a real company.

These are small, surgical edits. No model re-architecture. Do **not** fabricate
values. Commit per Part. Do **not** push — stage for review.

---

## 0. Read before you start

- `IC_MEMO.md` — §1 (Recommendation), §6 (Valuation & your stake),
  §7 (Returns), §10 (Conditions)
- "Inputs to confirm" section
- `financial_models/MODEL_PREVIEW.md` (to confirm the post-money and base-case
  exit equity numbers you'll cite: ~$10.0m vs ~$7.2m)

Pull the exact current figures from the model — do not hard-code the numbers in
this brief; cite whatever the engine outputs.

---

## PART 1 — Add an "are we overpaying?" entry-price check

In §6, add a short, explicit comparison of **what we'd pay** vs **what the
company is worth** in the central case. Use a one-table block:

| | Amount | Basis |
|---|---|---|
| What we'd value the company at (post-money) | ~$10.0m | $8m pre-money `[[TO CONFIRM]]` + $2m in |
| What the company is worth — base case (pipeline rNPV) | ~$7.2m | engine, forward-pipeline basis |
| **Entry-price gap (overpayment)** | **~$2.8m** | post-money − base-case value |

Then one plain-English line: for a startup equity bet we want the company worth
**more** at exit than the post-money we paid; here it's worth **less** in the
central case, so the 1× liquidation preference is the only thing preventing a
loss. **This is an entry-price problem, not just an exit problem — the main
lever is the pre-money we negotiate, not pipeline depth.**

Echo the finding in **§1 (Recommendation)** as a single sentence and in
**§10 (Conditions)** as a concrete ask: *"Re-price the entry (lower pre-money)
and/or release our capital in milestone tranches as the pipeline converts,
rather than $10m post-money up front for a ~$7m base-case company."*

Add a `[[TO CONFIRM]]` line in "Inputs to confirm":
*"Pre-money that makes this value-accretive — solve for the entry price at which
base-case company value ≥ post-money."* (Optional: if quick, compute and show
that break-even pre-money; if not, leave as a flagged input.)

---

## PART 2 — Make the headline conditional, and flag the distribution risk

### 2.1 Conditional framing (§1 and §7)

Reword the headline so it reads as conditional analysis, not a fixed verdict.
Pattern:

> "On the current placeholder inputs — $8m pre-money, ~25 projects in the
> pipeline at exit, and pro-rata interim distributions — the central case is
> **−2.6% / 0.88×**, i.e. value-destructive. These three inputs are
> `[[TO CONFIRM]]` and each materially moves the result (see Exhibit D)."

Make clear the negative headline is a **finding about the current terms**, not a
judgement on the company's viability.

### 2.2 Distribution-fraction caveat (§7)

Add a short note: the model uses convention (b) — interim distributions **plus**
terminal sale. But minority shareholders in a founder-controlled startup often
do **not** receive pro-rata interim cash (founders reinvest, or distributions
skew to management). **If we only receive the terminal exit, −2.6% is the
optimistic read.** List "confirm we share pro-rata in interim distributions" as
a `[[TO CONFIRM]]` and a §10 question for the founders.

---

## PART 3 — Sharpen the recommendation logic (§1)

Make the recommendation logic explicit and decision-useful:

- The verdict is **pass-leaning on current terms**, driven by entry price.
- The two things that would change it: (a) a lower pre-money (or milestone
  tranches), and (b) confirmation of a deeper pipeline and pro-rata
  distributions.
- Note that even at 40 projects deep, Exhibit D tops out near **+0.8%** — so
  pipeline depth alone does **not** rescue the deal; **price is the lever.**

Keep it to a few tight sentences; do not bloat §1.

---

## PART 4 — Style, regenerate, verify

### Style
- Plain English; define terms in brackets on first use.
- Tables for comparisons; no lists buried in prose.
- Three-layer basis (data source → method → calculation) on the new entry-price
  table.
- No fabricated inputs; new `[[TO CONFIRM]]` items collected in "Inputs to
  confirm."

### Regenerate
- If any cited number is pulled live, regenerate previews/figures so the memo
  ties to the engine. (No engine logic changes expected in this brief — these
  are narrative + one display table.)

### Part D — verification checklist (report pass/fail)
- [ ] §6 has the entry-price table (post-money vs base-case value vs gap) with
      a plain-English read.
- [ ] §1 names the entry-price finding and frames the headline as conditional on
      the three placeholder inputs.
- [ ] §7 has the distribution-fraction caveat (terminal-only would be worse).
- [ ] §10 has the re-price / milestone-tranche ask and the pro-rata-distribution
      question.
- [ ] "Inputs to confirm" lists: break-even pre-money, pipeline depth,
      distribution fraction.
- [ ] §1 states that pipeline depth alone doesn't rescue the deal (Exhibit D
      ≈ +0.8% at 40) and price is the lever.
- [ ] All existing tests still pass; numbers tie to the engine.

When done, report the diff summary and confirm the memo now reads as conditional
analysis. **Then stage for review — the push is the user's call, not yours.**
