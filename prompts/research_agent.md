# Research agent instructions

You research candidate investors for a reliability-first investor database (pilot: VC active in Slovakia).
For every candidate assigned to you, write exactly one file `research/<candidate_id>.json`.
Today is 2026-10-09. The activity window starts 2023-10-09 (36 months).

## Hard rules

1. **Never invent anything.** Every fact needs `source_url` + `quote`. If you cannot find a source, leave the
   field out (or `null`). A missing field is fine; a wrong field is a failure.
2. **`quote` must be copied verbatim** (character for character, original language) from the text of the page at
   `source_url`, 8–600 characters. Do not translate, paraphrase, merge sentences or fix typos. A script will
   download the URL and search for the quote; a quote that is not on the page is treated as a hallucination.
3. Use pages whose text is in the static HTML (press releases, news articles, the fund's own site). Avoid
   LinkedIn, Crunchbase, PitchBook, Tracxn, PDFs and pages behind login or cookie walls.
4. `source_date` = publication date of the source page if visible, else omit it.
5. Only public sources. Do not guess numbers from memory.

## Classification (`entity_kind.value`)

- `investor` – invests own or managed capital into private companies for equity / quasi-equity.
- `service_provider` – law firm, auditor, M&A / corporate finance advisor, consultant, insurer, software agency.
- `lender` – bank, leasing, only debt.
- `platform` – crowdfunding / club platform that only intermediates (if it runs its own fund, research the fund).
- `grant_scheme` – grants / subsidies only.
- `public_markets_manager` – mutual / hedge fund investing only in listed securities.

The `entity_kind` quote must be the sentence that shows what the subject does (e.g. "We are a venture capital
fund investing in...", "advokátska kancelária").

## Investor fields (only when `entity_kind.value == "investor"`)

- `investor_type.value`: `vc` | `pe` | `cvc` | `family_office` | `angel` | `private_investor` | `public_fund`
  | `fund_of_funds`. Public bodies investing equity directly into companies are `public_fund`; those investing
  only through other funds are `fund_of_funds`.
- `sectors.value`: short English labels, e.g. `["fintech", "b2b saas", "healthtech"]`.
- `stages.value`: subset of `pre-seed`, `seed`, `series-a`, `series-b-plus`, `growth`, `buyout`.
- `ticket_min`, `ticket_max`: typical single investment, `{amount, currency}` (amount in units, e.g. 500000).
  A range "0.5–3 mil. EUR" gives both fields with the same quote.
- `aum`: total capital under management as stated by a source. If only individual fund sizes are known, use the
  most recent fund size and explain it in `notes`.
- `investments`: 1–3 most recent deals, each `{company, deal_date, source_url, quote}`; the quote must name the
  investor (or its fund) and the company. Prefer deals within the activity window; if the newest deal you can
  find is older, still record it (the script will mark the investor inactive). `deal_date` is the announcement
  date (YYYY-MM-DD; use the 1st of the month if only month is known).
- `funds`: names of the managed funds, if known.

## Identity fields

- `country`: ISO code of the manager's headquarters. `active_in`: ISO codes where it invests (include `SK` if it
  invests in Slovakia).
- `legal_name`, `reg_no` (IČO) only if you found them on a source; otherwise omit.
- `duplicate_of`: candidate id of the same entity if two candidates are the same subject (e.g. manager vs. fund).
- `notes`: 1–3 sentences: anything ambiguous, what you could not find.
- `researched_at`: "2026-10-09".

## JSON shape

```json
{
  "candidate_id": "c009",
  "name": "Neulogy Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ"],
  "website": "https://...",
  "entity_kind": {"value": "investor", "source_url": "https://...", "source_date": null, "quote": "..."},
  "investor_type": {"value": "vc", "source_url": "https://...", "quote": "..."},
  "sectors": {"value": ["deep tech"], "source_url": "https://...", "quote": "..."},
  "stages": {"value": ["seed", "series-a"], "source_url": "https://...", "quote": "..."},
  "ticket_min": {"amount": 300000, "currency": "EUR", "source_url": "https://...", "quote": "..."},
  "ticket_max": {"amount": 3000000, "currency": "EUR", "source_url": "https://...", "quote": "..."},
  "aum": {"amount": 40000000, "currency": "EUR", "source_url": "https://...", "quote": "..."},
  "funds": ["Neulogy Ventures Fund I"],
  "investments": [
    {"company": "X", "deal_date": "2025-05-01", "source_url": "https://...", "source_date": "2025-05-02",
     "quote": "..."}
  ],
  "duplicate_of": null,
  "notes": "",
  "researched_at": "2026-10-09"
}
```

Allowed currencies: EUR, USD, CZK, GBP, HUF, PLN, CHF. Unknown keys are rejected.

## Before you finish

Run `.venv/bin/python -m investordb.cli check-schema research/<id>.json` (with `PYTHONPATH=src`) for every file you
wrote and fix every `FAIL`. Then report: one line per candidate (`id | entity_kind | type | #investments |
missing fields`).
