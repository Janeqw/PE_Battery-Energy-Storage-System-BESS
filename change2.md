# change2.md — Fix the exit-value basis in the BESS direct-equity memo

**For:** Claude Code, executing inside the repo
`PE_Battery-Energy-Storage-System-BESS`, on top of the work already committed
by `change.md` (commits `ef8ef52`, `512c043`, `35208a8`).

**Why this brief exists.** Right now the company's exit equity value is modelled
as *net programme profit × a platform exit multiple (default 4.0×, a
`[[TO CONFIRM]]` placeholder)*. That single assumption is now the biggest swing
factor in the whole memo — bigger than the gate rates — and it has two problems:

1. **Wrong base.** "Net programme profit" looks like *cumulative* profit the
   company earns across its whole life. A buyer pays a multiple of **future,
   sustainable** earnings (what they keep earning after they buy), not profit
   already earned and likely distributed. Multiplying cumulative profit by a
   multiple quietly inflates the exit value.
2. **One load-bearing number.** A lone 4.0× multiple, unsourced and shown as a
   single placeholder, is carrying the recommendation.

**Goal of this brief:** make the exit value defensible by switching the
**primary** basis to risk-adjusted pipeline value, keeping the earnings multiple
and any comparable deals as **cross-checks**, fixing the earnings base, adding a
sensitivity table, and guarding against double-counting cash. Do **not**
fabricate values — use `[[TO CONFIRM: …]]` placeholders and collect them in the
existing "Inputs to confirm" section.

Work in order. Commit after each Part. Do **not** push.

---

## 0. Read before you start

- `IC_MEMO.md` — Sections 6 (Valuation & your stake) and 7 (Returns to your shares)
- `src/valuation_engine.py`, `src/build_model.py` — the rNPV and exit logic
- `config/assumptions.yaml` — the exit multiple and related inputs
- `financial_models/MODEL_PREVIEW.md`, `STAGE_COMPARISON.md`
- `tests/` — the exit / ownership tests

Confirm where the exit equity value is computed and how "net programme profit"
is defined in code before changing anything. Report that definition back in the
commit message for Part 1.

---

## PART 1 — Make risk-adjusted pipeline value the PRIMARY exit basis

A develop-and-flip company is a **development platform**: what a buyer pays for
is its **forward pipeline**, not its past profits. Reuse the rNPV engine you
already built (rNPV = risk-adjusted net present value — the discounted,
probability-weighted value of future projects).

### 1.1 New primary exit formula

```
Exit equity value (per scenario)
  = rNPV of the projects still in the pipeline at the exit date
  + net cash retained on the balance sheet at exit
  - any debt outstanding at exit
```

- The pipeline rNPV must use the **same gate decomposition**
  (approval × grid connection × sale) and the **same discount rate** already in
  the model — do not introduce a second, inconsistent set of assumptions.
- Add a `[[TO CONFIRM]]` input for **pipeline depth at exit** (how many
  projects are still in flight when we sell). This is the main sensitivity of
  this basis, so flag it clearly.
- Apply the existing **First-Chicago** scenario weights to this exit value, then
  flow it through the cap table exactly as now:
  `our proceeds = diluted ownership % × scenario exit equity value`,
  floored by the 1× liquidation preference.

### 1.2 Wire it in

- `config/assumptions.yaml`: add `exit_basis: pipeline_rnpv` (a switch),
  `pipeline_depth_at_exit` `[[TO CONFIRM]]`, and keep the old multiple inputs but
  move them under a clearly-named cross-check block (see Part 2).
- `src/valuation_engine.py` / `src/build_model.py`: implement the formula above
  as the default exit value; keep the code modular so the multiple basis (Part 2)
  and the comps basis (Part 3) can be selected for cross-checks.
- Regenerate `MODEL_PREVIEW.md`, `STAGE_COMPARISON.md`, figures, notebooks.

### 1.3 Update the memo

In `IC_MEMO.md` §6, state plainly: the company is valued as a development
platform on its forward pipeline (rNPV), because that is what a buyer of a
development business actually pays for. Show the three-layer basis
(data source → method → calculation) as the existing "Basis —" footnotes do.

---

## PART 2 — Demote the earnings multiple to a CROSS-CHECK, and fix it

Keep the earnings multiple, but as a sanity check on Part 1, not the primary
number. Two fixes make it defensible:

1. **Fix the base.** Replace *cumulative* programme profit with **forward
   run-rate annual development profit** (the yearly stream an acquirer inherits),
   plus any cash actually retained. Rename the variable so the intent is obvious
   (e.g. `run_rate_annual_dev_profit`, not `net_programme_profit`).
2. **Make the multiple a sourced range, not a lone 4.0×.** Replace the single
   `[[TO CONFIRM]]` multiple with a **low / base / high** range, each tied to a
   `[[TO CONFIRM: cite comp or sector benchmark]]`. No bare number may drive the
   memo.

In `IC_MEMO.md` §6, present the multiple result beside the pipeline result as a
cross-check: "On an earnings-multiple basis the company is worth roughly X —
broadly consistent with / above / below the pipeline value." If the two
diverge materially, say so and explain why.

---

## PART 3 — Comparable transactions as a second cross-check (only if comps exist)

If real comparable M&A deals for similar developer platforms are available, add
a **direct per-scenario exit value** drawn from those comps as a third basis.
- Each comp must be a `[[TO CONFIRM: source]]` entry in Appendix A.
- If no credible comps exist, **do not invent them** — add a one-line note in §6
  that comps were not available and the pipeline basis stands as primary.

---

## PART 4 — Add an exit-value sensitivity table

The exit assumption is now the single biggest swing factor in the memo. Show it
as a range, not a buried placeholder.

- Add **Exhibit D** in Appendix C: our equity **IRR and MOIC** across a grid of
  the two exit drivers — **pipeline depth at exit** (rows) × **discount rate or
  multiple** (columns). Mirror the style of the existing returns-sensitivity
  exhibit.
- In §1 (Recommendation) and §7 (Returns), add one sentence naming the exit
  basis as the dominant sensitivity and pointing to Exhibit D.

---

## PART 5 — Guard against double-counting cash

A develop-and-flip company throws off cash every cycle. Our return can come from
**distributions along the way**, the **terminal share sale**, or both — but the
exit value must not credit us for profit we have already pulled out.

- Decide and document the convention in §7: are returns modelled as
  (a) terminal sale only, (b) distributions + terminal sale, or
  (c) distributions only? Default to (b) if unclear, and state it.
- Ensure the exit equity value uses **retained** cash only (cash not yet
  distributed). Add a check (Part 6) that distributions + terminal proceeds are
  not double-counting the same dollar of profit.

---

## PART 6 — Style, tests, verification

### Style (apply to IC_MEMO.md)
- Plain English; define terms in brackets on first use.
- Simple summary first, then detail; tables for comparisons; no lists buried in
  paragraphs.
- Every key number shows its three layers (data source → method → calculation)
  and is verifiable (cite the config field, data file, or source).
- No fabricated inputs — `[[TO CONFIRM: …]]`, collected in "Inputs to confirm."

### Tests
- Add a test that the primary exit value equals pipeline rNPV + retained cash −
  debt for a known set of inputs.
- Add a test that distributions + terminal proceeds do not exceed total
  lifetime profit (the double-count guard).
- Keep all existing tests green; update any that referenced the old
  `net_programme_profit × multiple` exit.

### Part D — verification checklist (report pass/fail on each)
- [ ] Primary exit basis is pipeline rNPV + retained cash − debt; the switch
      `exit_basis` defaults to it.
- [ ] Earnings multiple is a **cross-check** only, uses **forward run-rate**
      profit (not cumulative), and is a **sourced low/base/high range**.
- [ ] Comps cross-check added with sourced comps, OR a note that none exist.
- [ ] Exhibit D sensitivity table added; §1 and §7 name exit as the dominant
      sensitivity.
- [ ] Double-count convention stated in §7; exit uses retained cash only; guard
      test passes.
- [ ] Model runs; previews/figures/notebooks regenerated and tie to the engine.
- [ ] Every new `[[TO CONFIRM]]` is listed in "Inputs to confirm."
- [ ] All tests pass.

Final consistency check — confirm the headline expected return still ties out
to the scenario values under the new exit basis, and report the before/after
numbers so the change in the recommendation (if any) is visible:

```
# show expected MOIC/IRR before vs after, and the new per-scenario exit values
```

Leave commits local (per Part 1–6). Do **not** push — stage for review and
report the before/after headline so the impact on the recommendation is clear.
