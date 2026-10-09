# Plan: a reliable investor database

Status as of 2026-10-09. Pilot: VC funds active in Slovakia.

## 1. Who is in the database and who is not

### Investor definition

An entity is an **investor** if all of the following hold:

1. **Capital:** it invests its own capital or capital it manages on behalf of investors (LPs).
2. **Instrument:** it invests in **private companies** through an ownership stake or quasi-equity (convertible loan, SAFE).
3. **Recurrence:** it has an investment strategy or at least 2 publicly documented investments.
4. **Activity:** it has at least 1 publicly documented investment or a new fund within the last **36 months**. Checked as of the collection date.

### Types (`investor_type` field)

| Type | Additional criterion |
|---|---|
| `vc` | Invests from pre-seed to growth stage, typically a minority stake |
| `pe` | Buyout or growth, typically a majority or significant stake, established companies |
| `cvc` | Corporate investment unit with its own brand or mandate |
| `family_office` | Manages the wealth of one (SFO) or several (MFO) families and invests directly in companies |
| `angel` | Individual with at least 2 documented investments of their own money |
| `private_investor` | Private investment holding or high-net-worth individual that does not fit the types above |
| `public_fund` | State or supranational fund that invests equity in companies **directly** (SIH, NHF) |
| `fund_of_funds` | Invests only in other funds (e.g. EIF). Included, but flagged, because it does not invest in companies directly |

### Exclusion (`exclusion_reason` field)

| Code | Who | Why |
|---|---|---|
| `not_investor_service` | Lawyers, auditors, M&A advisers, consultants (e.g. SLOVCA associate members) | They do not invest capital, they only provide services to investors |
| `debt_only` | Banks, leasing, non-bank lenders | They do not acquire an ownership stake |
| `platform_only` | Crowdfunding platforms that only act as intermediaries | Third parties invest. If a platform has its own fund (Crowdberry, CB Investment Management), the **fund** is included, not the platform |
| `grant_only` | Grant schemes, subsidies | They do not acquire a stake |
| `public_markets_only` | Hedge funds, mutual funds investing in public equities | They do not invest in private companies |
| `inactive` | No documented investment or new fund within 36 months | The data could be misleading |
| `no_evidence` | No verifiable public evidence of an investment was found | Authenticity cannot be verified |
| `duplicate` | The same entity under a different name (manager vs. fund) | One record per investment platform |

### Granularity

One record = **investment platform (manager)**, not an individual fund. For example, "Neulogy Ventures" is one record and its funds are in the `funds` field. Reason: in practice, database users want to approach the manager, and funds change every few years.

**Edge case:** a fund that is a separate legal entity with its own team (Venture to Future Fund) is a separate record.

### Geography

A record's country is the **manager's headquarters**. A foreign fund actively investing in Slovakia (Jet Ventures, Credo) gets its `country` by HQ, and `SK` is added to `active_in`. In the pilot we build a list of "VC active in Slovakia", but **accuracy is measured only on funds headquartered in Slovakia**, so that the sample is unambiguous.

## 2. Record fields and sources

Every factual field has its own evidence `{value, source_url, source_date, retrieved_at, quote}`:

| Field | Meaning |
|---|---|
| `name`, `legal_name`, `ico` / `reg_no`, `country`, `website` | Identity |
| `investor_type` | See the table above |
| `sectors` | Sectors it invests in (e.g. fintech, B2B SaaS, deep tech) |
| `stages` | pre-seed / seed / A / B+ / growth / buyout |
| `ticket_min_eur`, `ticket_max_eur` | Typical size of a single investment |
| `aum_eur` | Total investment capital (size of the fund or funds) |
| `evidence_investments[]` | At least 1 documented investment: company, date, URL |
| `confidence` | `high` / `medium` / `low` |

`quote` is a verbatim excerpt from the source. It makes it possible to verify automatically that the claim really is on the page (see section 3).

## 3. How I verify authenticity and inclusion

**Pipeline (concept C, hybrid):**

1. **Candidates** (`data/candidates.csv`) from three types of sources, each with the URL where the candidate was found:
   - **associations:** SLOVCA, Invest Europe, CVCA,
   - **public programmes:** SIH, NHF, EIF, NRF (National Development Fund),
   - **deal-first:** press releases and media coverage of funding rounds (Forbes, Startitup, The Recursive, Vestbee).
2. **Research (AI agent):** for each candidate, finds the website, portfolio and at least 1 dated deal. Writes the evidence, including verbatim quotes, to JSON.
3. **Automated check (`verify.py`):**
   - the URL responds with HTTP 2xx,
   - the verbatim `quote` appears in the page text (normalised whitespace and diacritics). This catches **hallucinated sources**, the most common LLM error,
   - the evidence date is within the 36-month window,
   - schema (pydantic): ticket_min ≤ ticket_max, currency converted to EUR, types from the code list.
4. **Inclusion rules (`build.py`):** deterministically assign `included` or an `exclusion_reason` from the verified evidence. Code decides, not the LLM.
5. **Manual review:** a human opens the source and fills in `validation/manual_check.csv` for every record.
   - For every included record: is it a real active investor? Is the type correct?
   - For every field: does it match the source?
   - For excluded records: is the exclusion reason correct?

**Metrics (`metrics.py`):**
- **Inclusion precision** = correctly included / all included. This is the core requirement of the assignment ("every record is a real investor").
- **Exclusion correctness** = correctly excluded / all excluded.
- **Field accuracy** = correct values / filled values, separately for `investor_type`, `sectors`, ticket and AUM.
- **Field fill rate** = share of records where the field is not empty.
- **Recall** cannot be measured exactly, because no complete list exists. I estimate it via **capture-recapture**: how many funds from the deal-first sources were already in the association sources.

## 4. Estimate: how many investors can be obtained from public sources

| Type | Estimated number active worldwide | Source of estimate | Publicly verifiable (my estimate) | Expected reliability |
|---|---|---|---|---|
| VC | 4,000 – 7,000 | Decile Group, "guesstimate" from panel data | 80 – 90 % (funds publish their portfolio) | high |
| PE | ~ 7,000 (of which ~ 6,000 in the US) | American Investment Council via Vault; Preqin 2009: 4,270 to 6,000 | 70 – 85 % (deal PR, SEC Form ADV in the US) | high |
| CVC | 2,300 – 3,100 | Global Corporate Venturing 2024/2025 | 70 – 80 % | high |
| Single family office | ~ 8,000 (2024) | Deloitte, Defining the Family Office Landscape | **10 – 25 %** (FOs deliberately stay private) | medium |
| Angel | ~ 445,000 active in the US alone (2024) | UNH Center for Venture Research | **1 – 5 %** (≥2 publicly documented investments) | low to medium |

**Realistic database size:** roughly 15–20 thousand institutional investors (VC, PE, CVC, FO), plus 5–20 thousand angel investors with a public footprint.

**Limitations of the estimates:** the figures come from different years and definitions and partly overlap (VC and PE). This is an order-of-magnitude estimate, not a census.

**Expected reliability by field:**
- identity and activity: high, because they are backed by a URL and a date,
- sector and stage: high, because funds declare them themselves,
- ticket: medium, often missing or outdated,
- AUM: medium to low, because PE firms and FOs often do not disclose it.

**Fill rate:**
- ticket expected for 50–70 % of VCs,
- AUM for 60–80 % of VCs (fund size is usually in a press release),
- for FOs and angel investors AUM will be almost entirely missing.

## 5. Pilot (Slovakia, VC)

**Size estimate:** 15–30 active VCs headquartered in Slovakia and 20–40 foreign ones investing in Slovakia.

**Background:**
- 12 full members of SLOVCA, some of which are PE and some headquartered in CZ or PL,
- Invest Europe: only EUR 7 m of VC went to Slovakia in 2025.

**Steps:**
1. Collect candidates from SLOVCA, public programmes and deal-first sources.
2. Research and `verify.py` on **all** candidates.
3. Manual review of **100 %** of included and excluded Slovak records. The sample is small, so I do not sample.
4. Resulting metrics, a list of AI errors and their causes.

## 6. Worldwide cost estimate

Extrapolated from values measured in the pilot:
- tokens and time per record,
- share of records needing manual intervention,
- manual review time per record.

Cost model:

`cost = N_candidates × (LLM research + search API) + N_included × manual review share × time × hourly rate + maintenance (re-checking activity every 6–12 months)`

Concrete figures are in `COSTS.md`.
