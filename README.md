# Reliable Investor Database (Assignment A)

A pilot investor database in which **code and evidence decide, not the LLM**. An AI agent finds sources and verbatim
quotes, a script verifies that each quote really appears on the page, deterministic rules decide on inclusion, and a
human reviews the result in a simple UI.

| Document | Contents |
|---|---|
| [`PLAN.md`](PLAN.md) | Who is in the database and who is not, how authenticity is verified, estimates of investor count and reliability |
| [`COSTS.md`](COSTS.md) | Cost estimate for worldwide coverage, extrapolated from values measured in the pilot |
| [`data/investors.csv`](data/investors.csv) | Included investors, with a source for every field |
| [`data/investors.json`](data/investors.json) | The same, including verbatim quotes, dates and all deals |
| [`data/excluded.csv`](data/excluded.csv) | Excluded candidates with reason and source |
| [`validation/manual_check.csv`](validation/manual_check.csv) | Review sheet: AI pre-review + manual review |
| [`validation/pilot-v1/`](validation/pilot-v1/) | **Accuracy measurement (v1):** sheet, metrics and the database exactly as reviewed by the human |
| [`validation/metrics.json`](validation/metrics.json) | Metrics after fixes (v2) |
| [`prompts/`](prompts/) | The exact instructions given to the AI agents |
| [`ai-log/`](ai-log/) | Export of the Claude Code conversations (in Slovak) |

## Pilot results

Pilot: **75 candidates** active in Slovakia → **29 included, 46 excluded**. **327 of 329** pieces of evidence verified
(the quote was found on the page); 2 URLs were unreachable.

**Accuracy is measured** on the 50 candidates headquartered in Slovakia. 100 % of them were reviewed (102 items:
inclusion or exclusion plus every filled-in field), no sampling. The review was done by a human in the UI on
2026-10-09, opening the source for every item.

| Metric (HQ in SK) | Manual review | AI pre-review (for comparison) |
|---|---|---|
| **Inclusion precision** (included entities really are active investors) | **10 / 10 = 100 %** | 7 / 8 |
| **Correct exclusion reason** | **36 / 40 = 90 %** | 28 / 33 |
| `investor_type` | 10 / 10 | |
| `sectors`, `stages` | 13 / 13 | |
| `ticket_min_eur`, `ticket_max_eur` | 13 / 13 | |
| `latest_investment` (documented deal with source and date) | 10 / 10 | |
| **`aum_eur`** | **5 / 6 = 83 %** | 2 / 4 |
| **All fields combined** | **51 / 52 = 98 %** | |
| AI pre-review agreement with the human | 75 / 78 = 96 % | |

**Errors found by the human** (all of them had also been flagged by the AI pre-review):

- **4× wrong exclusion reason** (SRF, Arca Capital, Limerock, Sociálni Inovátori): the entities are correctly
  excluded, but as `no_evidence` instead of `inactive`. Old investments are documented and the funds are closed.
- **1× AUM** (Across, c013): EUR 450 m is wealth-management client assets, not the size of a VC fund.

**Where the AI pre-review was wrong** (3 of 78 items): CB ESPRI (inclusion is correct under the 36-month rule),
CB Investment Management (2025 co-investment only appears in an aggregator; SIH confirms the investment period ended
in 2023) and 0100 Ventures (EUR 23 m is the actual Fund I; EUR 60 m is only the target of a new fund). So the AI
pre-review did not miss any errors, but it was stricter than the human.

**Field fill rate** for included SK entities: type 100 %, stages and `ticket_max` 70 %, sectors, `ticket_min` and
AUM 60 %.

**Interpretation:** the core requirement of the assignment ("every record is a real investor") is met on the sample
at 100 %. Identity, type and documented investment are reliable. The weak spots are AUM and the distinction between
"inactive" and "no evidence". This matches the estimate in `PLAN.md` (AUM: medium to low reliability). The sample is
small (10 included), so 100 % does not mean there will be no errors at scale. With 10 of 10, the 95 % confidence
interval for precision is roughly 69–100 %.

Outside the SK sample, the human reviewed only the 7 items the AI pre-review had flagged as disputed, and confirmed
all of them: 3TS (ticket is the round size, AUM is the fund target), ZAKA (outdated AUM), BHM (AUM is the group's
asset value), BHS (sector too narrow) and Fil Rouge (missing `series-a`). These items are not part of the metrics,
because the measured sample consists of entities headquartered in Slovakia.

> The table above is **measurement v1** (`validation/pilot-v1/metrics.json`), i.e. the accuracy of the pipeline
> output before any fixes. The metrics have two branches: `human` (human verdicts only, used for the table) and
> `combined` (human verdict, otherwise AI).

### Fixes after manual review (v2)

I fixed the errors from the SK sample in `research/*.json` and re-ran the pipeline (`verify` → `build` → `metrics`):

| Record | Fix | How |
|---|---|---|
| c013 Across | AUM removed | EUR 450 m is client assets. The agent wrote this in its own note but filled in the field anyway |
| c051 SRF, c055 Arca, c057 Limerock | `no_evidence` → `inactive` | Added an old investment with a verbatim quote (podnikajte.sk 2016, SITA 2015). The exclusion reason was then determined by the rule, not by a manual override. `verify` confirmed all 3 quotes on the live page |
| c063 Sociálni Inovátori | **not fixed** | The source gives no specific dated investment, only the end of the investment period on 31 Dec 2023. That is still within the 36-month window, so it is the same edge case as CB ESPRI. I do not make up deal dates |

After the fixes (`validation/metrics.json`): correct exclusion reason **39 / 40**, AUM **5 / 5** (AUM fill rate dropped
to 50 %). The human confirmed the fixed rows based on their notes from v1. Errors outside the SK sample (3TS, ZAKA,
BHM, BHS, Fil Rouge) are not fixed yet.

## How it works

```
candidates.csv ──► AI research ──► research/cXXX.json ──► verify ──► build ──► data/investors.*
 (SLOVCA, SIH,     (5 agents,      (every field:           (HTTP +    (inclusion  data/excluded.csv
  NHF, EIF, media)  prompts/)       URL + quote + date)     quote)     rules)           │
                                                                                        ▼
                                     metrics.json ◄── manual_check.csv ◄── AI pre-review + human (UI)
```

1. **Candidates** (`data/candidates.csv`, 75): full and associate members of SLOVCA, public programmes (SIH, NHF,
   EIF, NRF) and deal-first sources (news about funding rounds). Each has the URL where it was found.
2. **Research** (AI agent, `prompts/research_agent.md`): one JSON per candidate. Every claim has a `source_url`, a
   `source_date` and a **verbatim quote** from the page.
3. **`verify`**: downloads every URL and searches for the quote in the page text (normalised whitespace, quotation
   marks, diacritics). A quote that is not on the page is treated as a hallucination and the field is dropped.
4. **`build`**: deterministic rules from `PLAN.md` (investor? equity? activity within 36 months?) assign `included`
   or an exclusion reason. Amounts are converted by code using `data/fx_rates.json`, not by the model.
5. **Review**: AI pre-review (`prompts/review_agent.md`, a different agent from the one that did the research),
   followed by manual review in the UI at `localhost:8000`. Metrics use the human verdict wherever it exists.

## Running

Python 3.12+.

```bash
make install    # venv + dependencies
make test       # 87 tests (pytest)
make pipeline   # verify → build → metrics
make serve      # UI at http://localhost:8000 (browsing + manual review)
PYTHONPATH=src .venv/bin/python -m investordb.cli import-review validation/ai_review_2.json
```

The review UI and the source quotes are in Slovak, as the pilot covers the Slovak market.

## How I worked with AI

The whole project was built in Claude Code (Opus 5.5). The conversations are in `ai-log/`.

### Division of work

| Step | Who | Why |
|---|---|---|
| Plan, inclusion rules, type definitions | me + Claude in dialogue | Claude proposed 3 concepts (pure LLM, pure scraping, hybrid); I chose the hybrid |
| Pipeline code (`src/`) | Claude, in small steps with tests | `pytest` + `ruff` after every step, commit only after green tests |
| Research of 75 candidates | 5 parallel subagents, 15 candidates each | Instructions: `prompts/research_agent.md` |
| Quote verification | `verify` script | Hallucinations should be caught by code, not by another model |
| Inclusion / exclusion | `build` script | Same input = same result; the rules are readable and tested |
| Pre-review of conclusions | separate review agent, 2 batches (c001–c050, c051–c075) | Instructions: `prompts/review_agent.md`, "sceptical reviewer" |
| Manual review | me in the UI | The only source of "truth" for the metrics |

### Instructions given to the agents

Key rules in `prompts/research_agent.md`:

- **Never make anything up.** A missing field is fine; a wrong field is a failure.
- **Quote verbatim, in the original language, 8–600 characters.** That is what lets the script verify it.
- Avoid LinkedIn, Crunchbase, PDFs and pages behind a login, because the script cannot download them.
- Never take numbers from memory. Currency conversion is done by code.
- Classify the entity first (`investor` / `service_provider` / `lender` / `platform` / …), only then fill fields.

The review agent (`prompts/review_agent.md`) does not check whether the quote exists (the script already did that),
but **whether the conclusion drawn from the quote is correct**: whether the AUM really is managed capital, whether
the ticket is not actually the round size, etc.

### How I checked the output

1. **Schema** (pydantic, `check-schema`): types from the code list, `ticket_min ≤ ticket_max`, valid dates.
2. **Quote existence** (`verify`): 327 of 329 pieces of evidence verified, 2 URLs unreachable (HTTP error).
3. **A second, independent agent** checked the interpretation.
4. **Manual review** in the UI: for every item a link to the source, the AI verdict and note, and correct/incorrect
   buttons.
   - **Source language:** quotes are verbatim, in the language in which the agent found them on the page.
     Multilingual websites (e.g. funds headquartered in SK or CZ) often show a Slovak browser the Slovak version,
     even though both the agent and the script received the English one. Ctrl+F then does not find the text until
     the page is switched to English. **This is not an evidence error.** The UI shows a warning for English
     quotes. I deliberately do not translate quotes, because the script could not verify translated text.
5. **Tests** for the inclusion rules, text normalisation, verification and metrics (87 tests).

### Where the AI got it wrong

| Error | How it showed up | How I caught it | Resolution |
|---|---|---|---|
| **AUM is not managed capital** (most common) | Recorded as AUM: wealth-management client assets (Across, c013), asset value of portfolio companies (BHM, c018), target fund size instead of the actual close (3TS, ZAKA) | Review agent | Field marked as incorrect; the instructions for the next round need a more precise AUM definition |
| **Round size instead of ticket** | 3TS: "leads rounds of EUR 5–20 m" recorded as the fund's ticket | Review agent | Leave the ticket empty |
| **Sector too specific** | BHS: "manufacturing", although the source says "all sectors, primarily the traditional economy" | Review agent | Proposed fix: generalist |
| **Review agent: false alarms** | CB Investment Management: "active" according to the Caplight aggregator, no primary source exists. CB ESPRI: "inactive", although the latest deal is within the 36-month window. 0100 Ventures: AUM "outdated", although the new fund is only a target | Manual review | The reviewing agent makes mistakes too, which is why the human decides the metrics. AI–human agreement was 96 % |
| **Activity based on deal date, not fund status** (a rule limitation, not a data error) | CB ESPRI (c062) is correctly included under the rule (Elv.ai 01/2024). However, since 2024 the fund has been in its post-investment period and makes no new investments | Review agent | The activity rule needs extending: if the source states the investment period has ended and there is no new fund, `inactive` |
| **`no_evidence` instead of `inactive`** | SRF, Arca Capital, Limerock, Sociálni Inovátori: the agent correctly noted that the entity is inactive (liquidation, bankruptcy, investment period over), but did not record the old investments even though the prompt required it. Without investments the rule returns "no evidence" | Review agent | The exclusion is correct, the reason is not. Fix: make recording the latest old deal mandatory, or add a `status_evidence` field with a quote about the liquidation |
| **Page language version** (a bug in my script, not the model) | The agent quoted the English version, the script downloaded the Slovak one (based on `Accept-Language`) → quote "not found", a false negative | Manually, on the first `verify` run | Commit `eb6542a`: on a mismatch, also try the English variant of the page |
| **Shared agent scratchpad** | Parallel research agents overwrote each other's helper scripts in a shared working directory | Agent 1's report | The outputs (`research/cXXX.json`) were not affected; parallel agents need isolated directories. The review agent is forbidden to write outside its own output file |
| **Prompt injection** | A search result (Dealroom) contained a hidden instruction for the AI | Agent 5 ignored it and mentioned it in its report | Dealroom was not used as a source; the second review round was told that page content is data, not instructions |
| **Duplicates do not merge evidence** | Slovenský rastový a kapitálový fond (c056) is probably the former name of Eterus Capital (c004). The `duplicate` rule excludes it, but its evidence is not attached to c004 | While browsing excluded records | Known limitation, see below |
| **Manager of multiple funds** | NHF (c008) manages Eterus and Fond inovácií a technológií, which are separate records. It is not a duplicate, but not a separate active investor either | Agent's note | Decided by the granularity rule in `PLAN.md` (separate team = separate record) |

Lesson learned: **hallucinated sources** (the most common LLM risk) barely appeared in the pilot, because the script
catches them. The errors that remained are **interpretation errors** of a genuine source. Only a second agent or a
human catches those.

## Decisions on ambiguities in the assignment

| Ambiguity | Decision | Reason |
|---|---|---|
| What is a "real investor" | 4 conditions: capital, equity, recurrence, activity within 36 months | The assignment stresses reliability; an inactive fund with outdated data would mislead the user |
| One record = fund or manager? | Manager (investment platform), funds in the `funds` field | Database users approach the manager; funds change every few years |
| "VC funds in one country" | Collected VC (and PE) active in Slovakia, **accuracy measured only on entities headquartered in Slovakia** | A small country makes it possible to review 100 % of the sample; HQ is an unambiguous criterion |
| PE in the pilot | Kept | The assignment also lists PE; SLOVCA does not distinguish them and the rules must be able to classify them correctly |
| Fund of funds (EIF) | Included with type `fund_of_funds` | It is an investor, but does not invest in companies directly, hence the flag |
| Investment size | Ticket as a `min`–`max` range in EUR, AUM separately | The assignment asks for both "how much" and "total capital"; these are two different numbers that the AI confused most often |
| Source for every data point | Every field has its own URL, source date, retrieval date and quote | With one URL per record it would be impossible to verify where a specific number came from |

## What the solution is missing

- **Manual review outside SK:** for entities headquartered outside Slovakia (CZ, PL, AT…) the human reviewed only
  the items flagged as disputed by the AI. The rest have only the AI pre-review.
- **Recall** was not measured. The capture-recapture approach in `PLAN.md` requires a second independent list (e.g.
  a Dealroom export), which is not publicly and freely available in machine-readable form.
- **Fixes outside the SK sample** (7 items confirmed by the human) and **updated agent instructions** (AUM
  definition, mandatory recording of old deals) are not done yet. Fixes in the SK sample are in the section
  "Fixes after manual review".
- **Duplicate merging:** a `duplicate` record is excluded, but its evidence is not attached to the main record.
- **Manager → funds relationship** (NHF → Eterus, FIT) is not modelled, only described in a note.
- **The activity rule** does not take an ended investment period into account (the CB ESPRI case).
- **Angel investors and family offices** are not in the pilot. The pilot covers VC/PE; these types have a weak public
  footprint (estimate in `PLAN.md`) and would require different sources (beneficial ownership registers,
  presentations at events).
- **10 items without an AI verdict**, because the source returns HTTP 403 (Forbes, PwC, law firms). They need to be
  opened in a browser during manual review.
