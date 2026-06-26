# change.md — Reframe & consolidate the BESS investment repo

**For:** Claude Code, executing inside the repo
`PE_Battery-Energy-Storage-System-BESS`.

**Two goals:**

1. **Reframe** the whole analysis from *"we invest as a passive limited
   partner in someone else's develop-and-flip fund"* to *"we directly buy
   shares in one new startup company that develops batteries."*
2. **Consolidate** the four overlapping report files into **one** main
   report (`IC_MEMO.md`) plus a **short** `README.md` front page.

Do the work in order. Commit after each Part with a clear message. Do **not**
push — leave commits local for review.

---

## 0. Read before you start

Read these so you understand the current content before changing it:

- `README.md`
- `COMMITTEE_REPORT.md`
- `INDUSTRY_REPORT.md`
- `SOURCES.md`
- `financial_models/MODEL_PREVIEW.md`, `financial_models/STAGE_COMPARISON.md`
- `config/assumptions.yaml`
- `src/build_model.py`, `src/valuation_engine.py`, `src/stage_analysis.py`,
  `src/make_report.py`

**Do not invent numbers.** Where the reframe needs a new input that does not
yet exist (e.g. pre-money valuation, ownership %), insert a clearly-labelled
placeholder `[[TO CONFIRM: …]]` and list it in the new
**"Inputs to confirm"** section of the IC memo. Never silently fabricate.

---

## PART A — Consolidate the four reports into one

### A1. Create the single report `IC_MEMO.md`

Create a new file `IC_MEMO.md` with exactly these sections:

```
1. Recommendation (bottom line up front)
2. The deal & the thesis
3. The company & what you're buying        <-- new, equity-specific
4. Industry & market
5. Business model & value-chain choice
6. Valuation & your stake                   <-- reframed
7. Returns to your shares                    <-- reframed
8. Risks & protections                       <-- expanded
9. Exit — how you get your money back
10. Conditions & questions for the founders
Appendix A — Methods & sources
Appendix B — Glossary
Appendix C — Exhibits
Inputs to confirm                            <-- collects every [[TO CONFIRM]]
```

### A2. Move existing content into the new sections

Map old content into `IC_MEMO.md` as follows. Carry the content over, then
reframe per Part B. Do not duplicate — each block lives in one place only.

| Source | Destination section in IC_MEMO.md |
|---|---|
| `README.md` §1 Recommendation | 1. Recommendation |
| `README.md` §2 opportunity/reframe | 2. The deal & the thesis |
| `COMMITTEE_REPORT.md` §3 strategy overview | 3. The company & what you're buying |
| **All of `INDUSTRY_REPORT.md`** (§§ market, niche, buyers, execution) | 4. Industry & market |
| `README.md` §5 / `COMMITTEE_REPORT.md` §8 value chain | 5. Business model & value-chain choice |
| `COMMITTEE_REPORT.md` §6 valuation + `README.md` §4 returns | 6. Valuation & your stake |
| `README.md` §4 returns table | 7. Returns to your shares |
| `README.md` §6 / `COMMITTEE_REPORT.md` §9 risks | 8. Risks & protections |
| `COMMITTEE_REPORT.md` §10 exit | 9. Exit |
| `README.md` §7 / `COMMITTEE_REPORT.md` §11 conditions | 10. Conditions & questions |
| **All of `SOURCES.md`** + `README.md` appendix + `COMMITTEE_REPORT.md` Exhibit 4 | Appendix A — Methods & sources |
| `COMMITTEE_REPORT.md` Exhibit 5 glossary | Appendix B — Glossary |
| `COMMITTEE_REPORT.md` Exhibits 1–3 | Appendix C — Exhibits |

### A3. Shrink `README.md` to a front page

Replace `README.md` entirely with a short signpost (~half a page):

- Title.
- One-line headline recommendation.
- A 3-row "at a glance" table (expected return, single biggest risk, status).
- A link to `IC_MEMO.md` ("→ Read the full Investment Committee memo").
- A short "How to reproduce the model" block (the `make`/`python` commands
  already documented in the current README appendix).

### A4. Delete the now-absorbed files

Once their content is confirmed inside `IC_MEMO.md`:

```
git rm COMMITTEE_REPORT.md INDUSTRY_REPORT.md SOURCES.md
```

Keep `financial_models/MODEL_PREVIEW.md` and
`financial_models/STAGE_COMPARISON.md` (they are model outputs, not reports) —
just link to them from Appendix A.

### A5. Fix all internal links

The old files cross-reference each other. After deletion, search the repo for
links to the deleted files and to the old section anchors, and repoint them at
the new `IC_MEMO.md` sections. Also update `src/make_report.py` if it writes or
names any of the deleted files.

```
grep -rn "COMMITTEE_REPORT\|INDUSTRY_REPORT\|SOURCES.md" .
```

No broken links may remain.

---

## PART B — Reframe: fund investor → direct shareholder

Apply this reframe across `IC_MEMO.md` **and** the model code.

### B1. Remove (fund-only machinery)

Delete these concepts and every figure derived from them, in the docs and in
`build_model.py` / `valuation_engine.py` / `config/assumptions.yaml`:

- Management fee (2%/yr)
- Carried interest (20%)
- Preferred return / hurdle (8%)
- Entry fee (2%)
- "Investor IRR **net of fees and carry**" → becomes plain "return on your
  shareholding"
- Limited-partner / general-partner (LP/GP) framing and "commitment to a fund"

### B2. Add (direct-equity machinery)

Add a new **Section 3 "The company & what you're buying"** containing:

- **Pre-money valuation** — company value before our money goes in. `[[TO CONFIRM]]`
- **Post-money valuation** = pre-money + our investment.
- **Our ownership %** = our investment ÷ post-money.
  - Worked example, plain English: "$8m pre-money + $2m from us = $10m
    post-money → we own 2 ÷ 10 = **20%**."
- **Price per share** and **number of shares**.
- **Share class** — ordinary vs preferred — and key terms.
- **Cap table** (who owns what %) **before and after** our investment, as a table.

Add **downside terms** (Section 8) and feed them into the returns maths:

- **Liquidation preference** (e.g. 1× non-participating: we get our money back
  first on a sale, before founders). Define it in one plain sentence.
- **Anti-dilution protection**.
- **Option pool** (shares reserved for staff — dilutes us; state the %).

Add **governance** (Section 3 or 10): board seat? information rights? veto over
major decisions?

Add **dilution** to the returns logic (Section 7): our exit proceeds
= our **diluted** % × exit equity value, **then** adjusted for our liquidation
preference.

### B3. Reframe the valuation engine (Section 6 + code)

- Stop calling it a "fund funnel / fund NAV." Reframe the same project-pipeline
  maths as **the company's own business plan** (its expected project profits
  over time = the company's value).
- Keep the **First-Chicago method** — it fits direct startup equity better than
  it fit the fund. Apply it to the **company's exit equity value** (success /
  base / failure scenarios, weighted), then:
  `our stake value = our diluted % × scenario exit equity value, capped/floored
  by the liquidation preference`.
- Keep the gate decomposition (approval × grid connection × sale) unchanged — it
  still drives the company's value.

### B4. Reframe returns (Section 7)

- Report **equity IRR** and **MOIC** (multiple of money) **on our shares**, not
  net-of-fee fund returns.
- IRR = cash out today for shares → cash back at exit from selling shares.
- Apply dilution and liquidation preference before reporting our proceeds.

### B5. Reframe risks (Section 8)

- **Remove / shrink:** fee drag, fund-manager alignment.
- **Add / elevate:** founder & key-person risk; single-company concentration
  (we are tied to one company now); down-round / dilution risk; minority-
  shareholder rights; no liquidity until exit; governance.
- **Keep:** the BESS market, development/approval gates, and exit/buyer risk for
  the underlying batteries — these still drive company value.
- Add a one-line note: a brand-new startup warrants a **heavier weight on the
  failure scenario** in First-Chicago and **stronger downside terms** than a
  diversified fund would.

### B6. Reframe the value-chain section (Section 5)

Reframe "where to invest across the value chain" as **"which business model is
this startup pursuing, and is it the right one to back?"** Keep the four stages
(develop-and-flip / build-and-sell / own-and-operate / integrated). Keep the
existing conclusion that a pure develop-and-flip play is the weakest risk-
adjusted model.

### B7. Update the model code & config

- `config/assumptions.yaml`: remove `mgmt_fee`, `carry`, `hurdle`, `entry_fee`
  (or equivalents). Add `pre_money`, `investment_amount`, `option_pool_pct`,
  `liquidation_preference_x`, `future_round_dilution_pct`. Use clearly-labelled
  placeholder values and list them under **Inputs to confirm**.
- `src/build_model.py` / `src/valuation_engine.py`: delete the fee-and-carry
  waterfall; add cap-table, dilution, and liquidation-preference logic so the
  output is **our** equity IRR/MOIC.
- `src/stage_analysis.py`: keep, but relabel fund language as company/business-
  model language.
- Re-run the model and regenerate `MODEL_PREVIEW.md`, `STAGE_COMPARISON.md`,
  and the figures so the docs and the model agree.
- `tests/test_data_validation.py`: update any assertions that reference removed
  fund fields; add a basic check that ownership % = investment ÷ post-money.

---

## PART C — Style rules (apply to IC_MEMO.md)

- Plain English. Define every finance/technical term in brackets on first use.
- Simple summary first, then detail.
- Tables for any comparison; do not bury lists inside paragraphs.
- Every key number shows its **three layers**: data source → method →
  calculation (keep the existing "Basis —" footnotes pattern).
- Every figure must be verifiable: cite the config field, data file, or source.
- Conservative, defensible numbers. Flag manager/founder claims as
  "claim to verify."
- No fabricated inputs — use `[[TO CONFIRM: …]]` and collect them in the
  "Inputs to confirm" section.

---

## PART D — Verification before you finish

Run through this checklist and report pass/fail on each:

- [ ] Only these report files remain: `IC_MEMO.md`, `README.md` (short).
      `COMMITTEE_REPORT.md`, `INDUSTRY_REPORT.md`, `SOURCES.md` are gone.
- [ ] `IC_MEMO.md` has all 10 sections + 3 appendices + "Inputs to confirm."
- [ ] No remaining mentions of management fee, carried interest, hurdle, entry
      fee, LP/GP, or "commitment to a fund" anywhere (grep to confirm).
- [ ] Section 3 has pre-money, post-money, ownership %, cap table.
- [ ] Returns are reported as equity IRR/MOIC on our shares, after dilution and
      liquidation preference.
- [ ] Model code runs; regenerated previews/figures match the memo numbers.
- [ ] `grep -rn "COMMITTEE_REPORT\|INDUSTRY_REPORT\|SOURCES.md" .` returns
      nothing (no broken links).
- [ ] Every `[[TO CONFIRM]]` placeholder is listed in "Inputs to confirm."
- [ ] Tests pass (`make test` or `pytest`).

Final grep to prove the fund framing is gone:

```
grep -rin "carried interest\|management fee\|limited partner\|\bLP\b\|\bGP\b\|hurdle" \
  --include=*.md --include=*.py --include=*.yaml .
```

Report anything this returns and confirm each hit is intentional (e.g. inside a
glossary entry explaining why the structure changed) or remove it.
