# Cost estimate for worldwide expansion

Status as of 2026-10-09. The estimate is based on **measured** values from the pilot (75 candidates, Slovakia), not on a rough guess.

## 1. Measured in the pilot

I extracted token usage from the subagent transcripts in Claude Code. Responses are deduplicated by message ID, because a single response is written to several lines in the log. Prices are Claude API list prices for `claude-opus-5-5` (as of 2026-10-06):

| Price | Value |
|---|---|
| Input | $4 / 1M tokens |
| Output | $20 / 1M tokens |
| Cache read | $0.20 / 1M tokens |
| Cache write (1 h) | $8 / 1M tokens |
| Web search | $10 / 1,000 searches |

The pilot ran under a Claude Code subscription. The amounts below are therefore the **equivalent at API prices**, not the amount actually paid.

| Phase | Agents | Time (wall clock) | Cache read | Cache write | Output* | Searches | Cost |
|---|---|---|---|---|---|---|---|
| Research of 75 candidates | 5 in parallel | 6–20 min per agent | 66.1 M | 1.03 M | 23 k | 142 | **≈ $23.3** |
| AI pre-review c001–c050 | 1 | 8 min | 4.7 M | 0.18 M | 2 k | 15 (+61 fetches) | **≈ $2.6** |
| AI pre-review c051–c075 | 1 | 6 min | – | – | – | 68 tool calls | ≈ 120 k tokens total |
| `verify.py` (329 pieces of evidence, 260 URLs) | – | < 1 min | – | – | – | – | $0 |

\* Output tokens in the log are underreported (probably recorded at the start of the stream). Treat them as a lower bound. Even a 10× increase would not change the total by more than $5.

**Unit costs:**
- research: **≈ $0.31 per candidate**,
- pre-review: **≈ $0.05 per candidate**,
- total **≈ $0.36 per candidate**.

About 95 % of the cost is cache reads and writes, i.e. repeatedly re-reading the context in the agent loop. Output and search are negligible.

## 2. How many candidates need to be processed

According to `PLAN.md`, the database comes to roughly **15–20 thousand institutional investors** (VC, PE, CVC, FO) and **5–20 thousand angel investors** with a public footprint.

In the pilot, **29 of 75 candidates (39 %)** passed inclusion. This figure is skewed, however: 31 candidates were SLOVCA associate members, mostly lawyers and auditors. Without them the yield is 29 of 44, i.e. **66 %**.

For worldwide collection (associations, public programmes, deal-first sources) I assume a yield of **40–60 %**. That means **50–90 thousand candidates**, of which 30–40 thousand are investors.

## 3. Scenarios

### A. Naive scaling of the current approach

The approach stays the same: Opus 5.5, one agent per candidate, AI pre-review of every record.

| Item | Calculation | Cost |
|---|---|---|
| Research | 50–90 k × $0.31 | $15–28 k |
| Pre-review | 30–40 k included × $0.05 × 1.5 (more fields) | $2–3 k |
| **LLM total** | | **$17–31 k** |

### B. Optimised approach (recommended)

1. **Deterministic pre-filter.** Association members who are lawyers, auditors or banks are excluded by a rule based on keywords and registers (NACE code, licence type). In the pilot this would have removed 31 of 75 candidates.
2. **Short context instead of a long agent loop.** Page fetching is handled by code and the model only receives the text of the candidate's pages. Estimated 5–10× fewer cache tokens.
3. **Model per task.** Extraction is done by Claude Sonnet 5.5 ($2 / $10), and pre-review covers only a sample plus items flagged by the script. Opus 5.5 is kept only for edge cases.
4. **Batch API** (−50 %) for everything that is not interactive.

| Item | Cost |
|---|---|
| LLM (extraction + targeted pre-review) | **$3–6 k** |
| Search (2–3 queries per candidate) | $1–3 k |

### Human review (in both scenarios)

In the pilot I review 100 % of records. At worldwide scale a **stratified sample** by type and region is used: 5 types × 6 regions × 60 records, **≈ 1,800 records** in total. With precision around 95 %, a sample of 60 records gives a confidence interval of ±5.5 pp per cell, and the 1,800-record sample ±1 pp overall.

On top of that, items flagged as incorrect by the AI pre-review must be resolved manually. In the pilot that was 15 of 211 items, i.e. **≈ 7 %**.

| Item | Calculation | Hours | Cost at €25/h |
|---|---|---|---|
| Sample review | 1,800 records × ~4 items × 0.5 min | ≈ 60 h | ≈ €1,500 |
| Resolving flagged items | 35 k × 4 items × 7 % × 3 min | ≈ 490 h | ≈ €12,000 |
| **Total** | | **≈ 550 h** | **≈ €13–14 k** |

Human work is therefore **the most expensive item**, not the LLM. The biggest savings lie in better instructions for the AI. The most common AI error (AUM that is not managed capital) can largely be eliminated with a more precise definition in the agent instructions.

## 4. Maintenance

- **Activity check every 6 months.** `verify.py` is HTTP only, so it costs almost nothing. New deals are tracked via deal-first sources (RSS, press releases), at ≈ $0.02–0.05 per investor per year, **≈ $1–2 k per year** in total.
- **Stale links:** in the pilot, 2 of 329 pieces of evidence (0.6 %) were unreachable. I assume 5–10 % per year will need refreshing.

## 5. Summary

| | One-off | Per year |
|---|---|---|
| LLM + search (scenario B) | $4–9 k | $1–2 k |
| Human review | ≈ €13–14 k | ≈ €3–5 k |
| **Total** | **≈ €17–23 k** | **≈ €4–7 k** |

**Uncertainties:**
- yield outside Slovakia,
- share of pages blocked against bots (1 of 260 URLs in the pilot; will be higher in the US and UK),
- angel investors, whose public footprint is weak: estimated 1–5 % of active ones, see `PLAN.md`.
