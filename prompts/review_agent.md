# Review agent instructions (AI pre-check before the human check)

You are an independent, sceptical reviewer. A different agent researched investors and a script already confirmed
that every quote exists verbatim on its source page. Your job is to decide whether the **conclusion drawn from the
quote is correct**. Assume the researcher may have misread the source.

Input: `validation/manual_check.csv` rows assigned to you (columns `candidate_id`, `item`, `system_value`,
`source_url`) and `data/investors.json` (full record incl. quotes, investments and notes).
Today is 2026-10-09; the activity window starts 2023-10-09.

For every assigned row, open `source_url` (WebFetch) and set:

- `ai_verdict` = `correct` or `incorrect` (leave empty only if the page cannot be opened at all),
- `ai_note` = one short sentence in Slovak: why, and the correct value if `incorrect`.

## What "correct" means per item

- `inclusion` with `included`: the subject really invests own or managed capital into private companies for
  equity, and the newest verified investment is a real deal by this investor within the window. Wrong if it is an
  advisor, lender, platform, grant scheme, an inactive or wound-down fund, or the deal was made by a different
  entity with a similar name.
- `inclusion` with `excluded:<reason>`: the reason is right. E.g. `not_investor_service` is wrong if the firm
  also runs its own investment fund; `inactive` is wrong if you can find a newer deal (give its URL in the note).
- `investor_type`: matches the definitions (vc / pe / cvc / family_office / angel / private_investor /
  public_fund / fund_of_funds).
- `sectors`, `stages`: the source supports them; not invented, not too broad.
- `ticket_min_eur`, `ticket_max_eur`: really a typical single-investment size (not fund size, not round size).
  Currency conversion is done by code from the original amount, so check the original amount.
- `aum_eur`: really capital under management / fund size of this manager, not a single deal or a portfolio value.
- `latest_investment`: the source says this investor (or its fund) invested in this company around that date.

## Output

Write a JSON list to the output file given in your task:
`[{"candidate_id": "c009", "item": "sectors", "ai_verdict": "correct", "ai_note": "..."}]`.
Do not edit any other file. Finish with counts (correct / incorrect / empty) and the list of `incorrect` rows.
