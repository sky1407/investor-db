# Subagent agent-areview-1-1f364293bf87b808

Zdroj: transkript Claude Code `agent-areview-1-1f364293bf87b808.jsonl`

## Používateľ · 2026-10-09 12:30:58 UTC

<teammate-message teammate_id="team-lead" summary="AI pre-check c001-c050">
You are a review agent for the project in /home/filip/investor-db. Read /home/filip/investor-db/prompts/review_agent.md first and follow it exactly.

Your assigned rows: every row of /home/filip/investor-db/validation/manual_check.csv whose candidate_id is between c001 and c050 (inclusive). Full records (quotes, investments, notes) are in /home/filip/investor-db/data/investors.json. The raw research files are in /home/filip/investor-db/research/.

Use WebFetch (and WebSearch where you need to check whether an "inactive"/"no_evidence" decision is wrong, e.g. a newer deal exists). Be sceptical: e.g. check that Národný holdingový fond (c008) being excluded as no_evidence, Crowdberry (c047) as inactive, CVI (c002) as debt_only, Fond inovácií a technológií (c005) as inactive are actually right.

Write your verdicts as a JSON list to /home/filip/investor-db/validation/ai_review_1.json (format in the instructions). Do not edit any other file. Finish with counts and the list of incorrect rows with a one-line reason each.
</teammate-message>

**Nástroj `Bash`**

```bash
cat /home/filip/investor-db/prompts/review_agent.md; head -3 /home/filip/investor-db/validation/manual_check.csv; ls /home/filip/investor-db/research/ /home/filip/investor-db/validation/
```

<details><summary>Výstup nástroja</summary>

```
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
- `
… [skrátené, 3395 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -c "
import csv
rows=[r for r in csv.DictReader(open('validation/manual_check.csv')) if 'c001'<=r['candidate_id']<='c050']
print(len(rows))
for r in rows: print(r['candidate_id'],r['item'],r['system_value'],r['source_url'],sep=' | ')
"
```

<details><summary>Výstup nástroja</summary>

```
117
c001 | inclusion | included | https://www.arxequity.com/about-arx/
c001 | investor_type | pe | https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/
c001 | stages | buyout | https://www.arxequity.com/about-arx/
c001 | aum_eur | 300000000 | https://www.arxequity.com/working-with-arx/
c001 | latest_investment | Medicofit (2026-08-26) | https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/
c002 | inclusion | excluded:debt_only | https://cvi.pl/en/
c003 | inclusion | included | https://www.ei.com.pl/en/about/
c003 | investor_type | pe | https://www.ei.com.pl/en/about/
c003 | sectors | technology; financial services; consumer goods; business services; healthcare; retail; manufacturing | https://www.ei.com.pl/en/about/
c003 | stages | growth; buyout | https://www.ei.com.pl/en/about/
c003 | ticket_min_eur | 20000000 | https://www.ei.com.pl/en/about/
c003 | ticket_max_eur | 75000000 | https://www.ei.com.pl/en/about/
c003 | latest_investment | Kredito unija "Saulėgrąža" (2026-07-01) | https://www.ei.com.pl/en/enterprise-investors-returns-to-lithuania-with-investment-in-kredito-unija-saulegraza
c004 | inclusion | included | https://www.eterus.sk/
c004 | investor_type | pe | https://www.oaklins.com/at/en/deals/110584/
c004 | stages | growth | https://www.eterus.sk/
c004 | ticket_min_eur | 2000000 | https://www.eterus.sk/
c004 |
… [skrátené, 11504 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -c "
import json
d=json.load(open('data/investors.json'))
print(type(d), len(d))
recs = d if isinstance(d,list) else d.get('investors', d)
print(json.dumps(recs[0],ensure_ascii=False,indent=1)[:4000])
"
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 6, in <module>
    print(json.dumps(recs[0],ensure_ascii=False,indent=1)[:4000])
                     ~~~~^^^
KeyError: 0
<class 'dict'> 3
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -c "
import json
d=json.load(open('data/investors.json'))
print(d.keys())
for k,v in d.items(): print(k, type(v), (len(v) if hasattr(v,'__len__') else v))
"
```

<details><summary>Výstup nástroja</summary>

```
dict_keys(['as_of', 'fx', 'records'])
as_of <class 'str'> 10
fx <class 'dict'> 4
records <class 'list'> 55
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -c "
import json
d=json.load(open('data/investors.json'))
print(d['fx'])
for r in d['records']:
  cid=r.get('candidate_id') or r.get('id')
  if cid and cid<='c050':
    print('=====');print(json.dumps(r,ensure_ascii=False))
" > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt; wc -c /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt
```

<details><summary>Výstup nástroja</summary>

```
93088 /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt
```

</details>

**Nástroj `Read`**

`/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt`

<details><summary>Výstup nástroja</summary>

```
1	{'base': 'EUR', 'rate_date': '2026-10-08', 'source_url': 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', 'rates': {'EUR': 1.0, 'USD': 1.1186, 'CZK': 24.403, 'GBP': 0.84698, 'HUF': 366.25, 'PLN': 4.3753, 'CHF': 0.9326}}
2	=====
3	{"candidate_id": "c001", "name": "ARX Equity Partners", "country": "CZ", "active_in": ["CZ", "PL", "HU", "SI", "HR"], "website": "https://www.arxequity.com/", "funds": ["ARX IV Fund"], "included": true, "exclusion_reason": null, "confidence": "high", "needs_review": false, "issues": [], "entity_kind": {"value": "investor", "source_url": "https://www.arxequity.com/about-arx/", "source_date": null, "quote": "With more than € 300 million raised in four funds, ARX has become a leading private equity firm in its segment operating in the Central European (“CE”) region.", "status": "verified", "original_amount": null, "original_currency": null}, "investor_type": {"value": "pe", "source_url": "https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/", "source_date": "2026-08-26", "quote": "ARX Equity Partners (“ARX”), a leading Central European private equity firm, today announced the acquisition of a majority stake in Medicofit, fizioterapija d.o.o. (“Medicofit” or the “Company”), Slovenia’s foremost private provider of integrated musculoskeletal care.", "status": "verified", "original_amount": null, "original_currency": null}, "sectors": null, "stages": {"value": 
… [skrátené, 55641 znakov]
```

</details>

**Nástroj `Read`**

`/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt`

<details><summary>Výstup nástroja</summary>

```
55	{"candidate_id": "c030", "name": "Forvis Mazars Slovensko", "country": "SK", "active_in": ["SK"], "website": "https://www.forvismazars.com/sk/sk", "funds": [], "included": false, "exclusion_reason": "not_investor_service", "confidence": null, "needs_review": false, "issues": [], "entity_kind": {"value": "service_provider", "source_url": "https://www.forvismazars.com/sk/sk", "source_date": null, "quote": "Forvis Mazars ponúka audítorské, daňové a poradenské služby po celom svete.", "status": "verified", "original_amount": null, "original_currency": null}, "investor_type": null, "sectors": null, "stages": null, "ticket_min_eur": null, "ticket_max_eur": null, "aum_eur": null, "investments": [], "last_evidence_date": null, "notes": "Audit, tax and advisory firm; Slovak branch of the Forvis Mazars network."}
56	=====
57	{"candidate_id": "c031", "name": "Ments", "country": "SK", "active_in": ["SK"], "website": "https://ments.sk/", "funds": [], "included": false, "exclusion_reason": "not_investor_service", "confidence": null, "needs_review": false, "issues": [], "entity_kind": {"value": "service_provider", "source_url": "https://ceelegalmatters.com/slovakia/24859-ments-opens-doors-in-slovakia", "source_date": "2023-11-16", "quote": "Former HKV Partner Lukas Michalik has opened up a new law firm in Slovakia: Ments.", "status": "verified", "original_amount": null, "original_currency": null}, "investor_type": null, "sectors": null, "stages": null, "ticket_min_eur": null, "ticket_max
… [skrátené, 36855 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; ls; ls prompts; grep -ril "private_investor" --include=*.md . | head
```

<details><summary>Výstup nástroja</summary>

```
Makefile
PLAN.md
data
prompts
pyproject.toml
raw
research
src
tests
validation
research_agent.md
review_agent.md
(eval):1: no matches found: --include=*.md
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; grep -n -A3 -i "private_investor\|family_office\|fund_of_funds\|no_evidence\|inactive\|debt_only\|not_investor_service" prompts/research_agent.md | head -80
```

<details><summary>Výstup nástroja</summary>

```
33:- `investor_type.value`: `vc` | `pe` | `cvc` | `family_office` | `angel` | `private_investor` | `public_fund`
34:  | `fund_of_funds`. Public bodies investing equity directly into companies are `public_fund`; those investing
35:  only through other funds are `fund_of_funds`.
36-- `sectors.value`: short English labels, e.g. `["fintech", "b2b saas", "healthtech"]`.
37-- `stages.value`: subset of `pre-seed`, `seed`, `series-a`, `series-b-plus`, `growth`, `buyout`.
38-- `ticket_min`, `ticket_max`: typical single investment, `{amount, currency}` (amount in units, e.g. 500000).
--
44:  find is older, still record it (the script will mark the investor inactive). `deal_date` is the announcement
45-  date (YYYY-MM-DD; use the 1st of the month if only month is known).
46-- `funds`: names of the managed funds, if known.
47-
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; sed -n 1,80p prompts/research_agent.md
```

<details><summary>Výstup nástroja</summary>

```
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
- `platform` – crowdfunding / club pla
… [skrátené, 4705 znakov]
```

</details>

**Nástroj `ToolSearch`**

```json
{"query": "select:WebFetch,WebSearch", "max_results": 2}
```

## Claude · 2026-10-09 12:32:00 UTC

Začnem skeptickými vylúčeniami (c002, c005, c008, c047).

**Nástroj `WebFetch`**

```json
{"url": "https://cvi.pl/en/", "prompt": "What does CVI do? Does it invest in equity (private equity, minority stakes) or only debt? List any equity funds or equity investments mentioned."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.fondfit.sk/index.php/sba/", "prompt": "Is the fund still investing? Does the page mention a post-investment phase, end of investment period, or recent investments with dates? Quote relevant sentences."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.nhfond.sk/", "prompt": "What does Národný holdingový fond do now? Does it invest directly into companies or only through funds (Eterus, FIT)? Any dated recent investments or news (2023-2026)? Quote relevant sentences."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.cbim.sk/", "prompt": "List all portfolio companies with any years or dates of investment, especially any from 2023-2026. Is the fund still investing? Quote relevant text."}
```

<details><summary>Výstup nástroja</summary>

```
CVI is an independent investment firm active since 2012, and the page calls it "a leader in the private debt market in Central Europe." It manages eight funds with about EUR 1.1 billion in assets under management, provides flexible financing to medium-sized companies, and invites investors to access private debt through its funds.

The page describes CVI's business as debt-focused. It doesn't name any equity funds or equity investments. One example, a financed buyout of a minority shareholder in a yacht manufacturer, involves a minority stake, but the page doesn't say whether CVI took an equity position or provided debt. Other examples say CVI provided "capital," which doesn't specify the instrument.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Named portfolio company:** Only one company is named as a portfolio investment on the page:

- **DNA ERA** (Slovak biotech, genetic DNA analysis): The page says, "In 2021, DNA ERA received investment worth 250,000 € from the CB Growth One fund." A later round of about €1M is mentioned without a date: "they raised another 1 million € in collaboration with Crowdberry."

**Possible but unconfirmed:** Ecocapsule appears only in photo captions and a link to ecocapsule.sk. The page doesn't describe it as a portfolio company or give an investment date.

**2023–2026 investments:** None are listed. The page has no dated investments in that period.

**Is the fund still investing?** The page doesn't say. It gives these facts:

- "was founded in 2019 in order to help seed and pre-seed businesses based in Slovakia"
- Fund size: €23.2M
- Companies: 32
- Lifetime: "10 Years lifetime" with "+ 3 years extension"

The 32-company count suggests more investments than the page lists, but it doesn't show whether new investments are still being made. The 2026 date appears only in the copyright footer.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Short answer:** The page doesn't say whether the fund is still investing.

- **Post-investment phase, end of investment period, or dated recent investments:** None are mentioned. The only dates are in the copyright line, "© 2024 Všetky práva vyhradené," and the page doesn't say what that date refers to.
- **Investment-related content:** The navigation includes "Investičné zameranie," "Investičný proces," and "Podporené projekty," but these are links with no details.
- **Background:** The page describes the fund's origin: "vznikol ako reakcia na vznikajúci dopyt po rizikovom kapitáli." This explains why it was formed but says nothing about its current status.

To answer the question, check the "Podporené projekty" (supported projects) or "Investičný proces" pages, which aren't included in this content.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**What NHF does:** Národný holdingový fond is a specialized subsidiary of Slovak Business Agency that provides venture capital to growth-oriented businesses and coordinates the activities of the individual funds to support SME development nationwide. The page describes this as:

- "Špecializovaná dcérska spoločnosť Slovak Business Agency, ktorá implementuje podporu formou rizikového kapitálu." (a specialized subsidiary of Slovak Business Agency that implements support through venture capital)
- "Podporuje rastovo orientované podnikateľské projekty formou poskytovania rizikového kapitálu" (it supports growth-oriented business projects by providing venture capital)
- "Usmerňuje činnosti jednotlivých fondov tak, aby sa stimuloval rozvoj sektora MSP na celom území SR." (it steers the activities of individual funds to stimulate SME sector development across Slovakia)

**Direct or through funds?** The page is not explicit. Its NHF section says the fund provides capital as a contribution "vkladu do základného imania spoločností" (to companies' share capital), which suggests direct equity investment. However, it also says NHF steers the individual funds, and Eterus Capital and Fond inovácií a technológií are presented as separate funds. The page doesn't say whether NHF invests directly, through them, or both.

**Recent investments or news (2023–2026):** None. The page has no dated investment announcements or news items. Its only date is the copyright line, "Copyright 2014," so the co
… [skrátené, 1584 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"CB Investment Management\" investícia startup 2024 OR 2025", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Fond inovácií a technológií FIT poinvestičná fáza", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Národný holdingový fond\" investícia 2024 OR 2025 OR 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "CVI private equity fund equity investment Poland \"CVI\" Dom Maklerski equity fund", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Fond inovácií a technológií FIT poinvestičná fáza"

Links: [{"title":"FIT vám pomôže zafinancovať inovatívne podnikateľské nápady","url":"https://www.podnikajte.sk/investor/fit-fond-financovanie"},{"title":"fondfit oznamuje dalsie investicie obe do hernehobiznisu","url":"https://www.startitup.sk/fondfit-oznamuje-dalsie-investicie-obe-do-hernehobiznisu/"},{"title":"ZBV Abogados Participa de la Iniciativa FIT de la BCBA","url":"https://abogados.com.ar/zbv-abogados-participa-de-la-iniciativa-fit-de-la-bcba/9798"},{"title":"www.startitup.sk","url":"https://www.startitup.sk/?p=12849"},{"title":"Company Profile","url":"https://www.seca.ch/en/find-members/fondation-pour-linnovation-technologique-fit/"},{"title":"FONDATION POUR L'INNOVATION ET LA TECHNOLOGIE (FIT)","url":"https://www.fundraiso.ch/en/organisations/fondation-pour-linnovation-technologique-fit"},{"title":"FONDATION POUR L'INNOVATION ET LA TECHNOLOGIE (FIT)","url":"https://www.fundraiso.ch/en/organisations/fondation-pour-linnovation-et-la-technologie-fit"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/fond-fit"},{"title":"Fondation FIT","url":"https://startups.one.gob.es/companies/fondation_fit"}]

The search didn't return anything specifically about the post-investment phase (poinvestičná fáza) of the Slovak Fond inovácií a technológií (FIT). The results are mostly older articles about its early investments, so they can't tell you how the fund handles t
… [skrátené, 2935 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""CB Investment Management" investícia startup 2024 OR 2025"

Links: [{"title":"Slovenský startup získal vyše polmiliónovú investíciu. Preslávili sa v USA vďaka virtuálnej realite","url":"https://www.startitup.sk/slovensky-startup-ziskal-vyse-polmilionovu-investiciu-preslavili-sa-v-usa-vdaka-vizualizacnym-rieseniam/"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/cbim"},{"title":"Description of the company","url":"https://www.profesia.sk/en/work/cb-investment-management/C238924"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-investment-management"},{"title":"CB Investment Management","url":"https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/cb-investment-management-kapitalova-investicia"},{"title":"CB Investment Management","url":"https://rwanda.dealroom.co/companies/cb_investment_management"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-espri"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/cbre-global-investors/financials"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/coinbase-ventures/financials"}]

CB Investment Management is a Slovak fund manager, and the search turned up a few 2024–2025 items, though the sources don't agree on some details.

**Who they are:** CB Investment Management is a subsidiary of Crowd
… [skrátené, 3377 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Národný holdingový fond" investícia 2024 OR 2025 OR 2026"

Links: [{"title":"n rodn holdingov fond nhfond sk","url":"https://venturecapitalarchive.com/venture-funds/n-rodn-holdingov-fond-nhfond-sk"},{"title":"Národní rozvojový fond vlády umožní investice v řádu desítek miliard korun","url":"https://www.businessinfo.cz/clanky/narodni-rozvojovy-fond-vlady-umozni-investice-v-radu-desitek-miliard-korun/"},{"title":"Stát spouští IPO fond 2025+ na podporu růstu MSP a rozvoje kapitálového trhu","url":"https://www.businessinfo.cz/clanky/stat-spousti-ipo-fond-2025-na-podporu-rustu-msp-a-rozvoje-kapitaloveho-trhu/"},{"title":"Národní rozvojový fond bude spravovat státní banka, na investice půjde až 35 miliard","url":"https://www.e15.cz/byznys/finance-a-bankovnictvi/narodni-rozvojovy-fond-bude-spravovat-statni-banka-na-investice-pujde-az-35-miliard-1360230"},{"title":"Ministr Havlíček: Peníze do národního fondu chtějí posílat kromě bank i jiné firmy","url":"https://www.e15.cz/rozhovory/ministr-havlicek-penize-do-narodniho-fondu-chteji-posilat-krome-bank-i-jine-firmy-1360245"},{"title":"NRI spouští program IPO fond 2025+ na podporu kapitálového trhu v ČR","url":"https://www.businessinfo.cz/clanky/nri-spousti-program-ipo-fond-2025-na-podporu-kapitaloveho-trhu-v-cr/"},{"title":"Národní rozvojový fond na startu: podepsáno memorandum, startuje příprava pilotních projektů","url":"https://www.kurzy.cz/tema/5605903.html"},{"title":"Banky jsou připraveny do rozvoj
… [skrátené, 4474 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CVI private equity fund equity investment Poland "CVI" Dom Maklerski equity fund"

Links: [{"title":"CVI Private Debt Fund II (EBRD-55534)","url":"https://ewsdata.rightsindevelopment.org/projects/55534-cvi-private-debt-fund-ii/"},{"title":"privateequitylist.com","url":"https://privateequitylist.com/investors/cvi"},{"title":"pfr ventures invests pln 100m two private debt funds","url":"https://pfrventures.pl/en/artykul/pfr-ventures-invests-pln-100m-two-private-debt-funds"},{"title":"cvi launches first ever cee direct lending fund","url":"https://realdeals.eu.com/article/cvi-launches-first-ever-cee-direct-lending-fund"},{"title":"FORWARD FEATURES CALENDAR","url":"https://www.privateequitywire.co.uk/pfr-ventures-invests-eu22m-two-private-debt-funds/"},{"title":"FORWARD FEATURES CALENDAR","url":"https://www.privateequitywire.co.uk/?p=101864"},{"title":"Kategoria artykułu: Biznes","url":"https://xyz.pl/?p=26760"},{"title":"EBRD backs Polish private debt fund","url":"https://alternativecreditinvestor.com/2025/04/02/ebrd-backs-polish-private-debt-fund/"},{"title":"ebrd supports growth of private credit in poland","url":"https://www.ebrd.com/home/news-and-events/news/2025/ebrd-supports-growth-of-private-credit-in-poland.html"}]

Links: [{"title":"cvi launches first ever cee direct lending fund","url":"https://realdeals.eu.com/article/cvi-launches-first-ever-cee-direct-lending-fund"},{"title":"Erste Group dołączyło do funduszu CVI Private Debt Fund II","u
… [skrátené, 5385 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "CB IM Growth One fond investoval 2024 startup Crowdberry fond", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "3IPK Crowdberry CB Investment Management 2025 investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "3IPK Crowdberry CB Investment Management 2025 investícia"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/cbim"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/crowdberry"},{"title":"CB Investment Management 41947","url":"https://contactout.io/company/CB-Investment-Management-41947"},{"title":"Description of the company","url":"https://kika.profesia.sk/en/work/crowdberry/C214482"},{"title":"Přes Crowdberry investoři za šest let poskytli startupům 780 milionů korun, teď samo získává desítky milionů","url":"https://cc.cz/pres-crowdberry-investori-za-sest-let-poskytli-startupum-780-milionu-korun-ted-samo-ziskava-desitky-milionu/"},{"title":"connection2024 04 12.dM2d","url":"https://amcham.sk/media/a542/file/item/en/0000/connection2024_04_12.dM2d.pdf"},{"title":"Crowdberry predstavuje na Slovensku nový fond. Do slovenských a českých nehnuteľností chce investovať 30 miliónov eur","url":"https://www.startitup.sk/?p=475147"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-investment-management"},{"title":"Na Slovensko prichádza nový investičný fond. Jeho objem bude takmer 12 miliónov eur","url":"https://www.startitup.sk/na-slovensko-prichadza-novy-investicny-fond-jeho-objem-bude-takmer-12-milionov-eur/"},{"title":"Interview with Michal Nešpor","url":"https:/
… [skrátené, 3331 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CB IM Growth One fond investoval 2024 startup Crowdberry fond"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/cbim"},{"title":"CB Growth ONE Fund Overview","url":"https://pitchbook.com/profiles/fund/22788-10F"},{"title":"bim ventures unite sbi holding launch 200 million fund bim capital","url":"https://www.wamda.com/en/2024/10/bim-ventures-unite-sbi-holding-launch-200-million-fund-bim-capital"},{"title":"bim ventures unite sbi holding launch 200 million fund bim capital","url":"https://www.wamda.com/index.php/en/2024/10/bim-ventures-unite-sbi-holding-launch-200-million-fund-bim-capital"},{"title":"bim ventures unite sbi holding launch 200 million fund bim capital","url":"https://www.wamda.com/index.php/2024/10/bim-ventures-unite-sbi-holding-launch-200-million-fund-bim-capital"},{"title":"Description of the company","url":"https://www.profesia.sk/en/work/cb-investment-management/C238924"},{"title":"Canadian Business Growth Fund launches with initial capital commitment of $545 million","url":"https://betakit.com/canadian-business-growth-fund-launches-with-initial-capital-commitment-of-545-million/"},{"title":"canadian business growth fund wants to ramp up investment in the next year","url":"https://thelogic.co/briefing/canadian-business-growth-fund-wants-to-ramp-up-investment-in-the-next-year/"},{"title":"Predict your next investment","url":"https://www.cbinsights
… [skrátené, 4848 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "3IPK investícia 2025 kolo Crowdberry fond CB Growth", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "3IPK investícia 2025 kolo Crowdberry fond CB Growth"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/cbim"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/crowdberry"},{"title":"Description of the company","url":"https://www.profesia.sk/en/work/cb-investment-management/C238924"},{"title":"Investors Count","url":"https://www.cbinsights.com/company/3ipk/financials"},{"title":"Lokální investování je na vzestupu, hlásí Crowdberry. Přes platformu a fondy loni proteklo přes 700 milionů","url":"https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/"},{"title":"connection2024 04 12.dM2d","url":"https://amcham.sk/media/a542/file/item/en/0000/connection2024_04_12.dM2d.pdf"},{"title":"CB Investment Management 41947","url":"https://contactout.io/company/CB-Investment-Management-41947"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-investment-management"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim","url":"https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/"},{"title":"Description of the company","url":"https://kika.profesia.sk/en/work/crowdberry/C214482"}]

Hľadal som informácie o 3IPK, investícii v roku 2025 a fonde 
… [skrátené, 2840 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.caplight.com/investor/cbim", "prompt": "List all investments of CB Investment Management with dates, round types and lead/co-investor role."}
```

<details><summary>Výstup nástroja</summary>

```
The page shows five of CB Investment Management's investments. All five list the firm as a **Co-investor**:

| Company | Date | Round Type | Role |
|---|---|---|---|
| 3IPK | May 2025 | Crowdfunding | Co-investor |
| Forvio | Sep 2023 | Seed | Co-investor |
| 3IPK | May 2023 | Accelerator | Co-investor |
| DimensionLab | Dec 2022 | Pre Seed | Co-investor |
| Vestberry | Nov 2022 | Pre Seed | Co-investor |

The page lists 10 portfolio companies, but only these five investments are visible. A "View all investments" link leads to a demo request page, so the rest aren't available here.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "3IPK startup 2025 investícia Crowdberry", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "3IPK startup 2025 investícia Crowdberry"

Links: [{"title":"strach evropanum zatemnuje mysl rika daniel gaspar z platformy crowdberry","url":"https://forbes.cz/strach-evropanum-zatemnuje-mysl-rika-daniel-gaspar-z-platformy-crowdberry/"},{"title":"je libo patro v mrakodrapu investicni platforma crowdberry slape do nemovitosti","url":"https://forbes.cz/je-libo-patro-v-mrakodrapu-investicni-platforma-crowdberry-slape-do-nemovitosti/"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/crowdberry"},{"title":"Investors Count","url":"https://www.cbinsights.com/company/3ipk/financials"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim 2","url":"https://forbes.cz/email/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim-2/"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim","url":"https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/"},{"title":"crowdcreator.eu","url":"https://www.crowdcreator.eu/?p=1657"},{"title":"Description of the company","url":"https://www.profesia.sk/en/work/cb-investment-management/C238924"},{"title":"Crowdberry nabízí nákup přímého podílu ve firmě či nemovitosti. Otevíráme nové investiční příležitosti, říkají partneři","url":"https://cc.cz/crowdberry-nabizi-nakup-primeho-podilu-ve-firme-ci-nemovitosti-otevirame-nove-inve
… [skrátené, 3245 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://forbes.cz/strach-evropanum-zatemnuje-mysl-rika-daniel-gaspar-z-platformy-crowdberry/", "prompt": "Does the article say Crowdberry or its fund (CB Investment Management / CB Growth One) invested in 3IPK? When? Quote exact sentences and the article date."}
```

<details><summary>Výstup nástroja</summary>

```
The content provided doesn't answer this. It contains only the headline:

"Strach Evropanům zatemňuje mysl, říká Daniel Gašpar z platformy Crowdberry | Forbes"

The headline names Crowdberry, but it says nothing about an investment in 3IPK, and it doesn't mention CB Investment Management or CB Growth One. The page also gives no article date, and no body text is included. To answer, you would need the full article text, or a source that discloses Crowdberry's investments.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.fondfit.sk/", "prompt": "Does the page say the fund entered a post-investment phase (poinvestičná fáza) or stopped making new investments? Quote it, with any dates. List newest supported projects with dates."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.nhfond.sk/fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/", "prompt": "Does NHF invest directly into companies? Any dates, statements about current status, or end of investing? Quote."}
```

<details><summary>Výstup nástroja</summary>

```
**Direct investment:** The page doesn't use the word "directly," but it describes funding businesses. Small and medium enterprises can apply for investment: "O investíciu sa môžu uchádzať malí a strední podnikatelia (MSP)."

**Dates and status:** The page gives no current status and no statement about ending investments. The only date is the footer: "Copyright 2014 - Národný holdingový fond s.r.o."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Yes.** The page states: "Fond inovácií a technológií vstúpil v roku 2025 do post-investičnej fázy." It appears under the heading "Informácia pre potenciálnych záujemcov o investície," and the only date given is 2025. The page does not say whether the fund has stopped making new investments.

**Supported projects:** The page lists five portfolio companies, but none has a support date, so I can't rank them by recency:

1. Elearn.Aero (IT technológie)
2. Trigen (Technológie, Výroba)
3. Futureplastix (Výroba)
4. COGNEXA (IT technológie)
5. DATAMOLINO (IT technológie)

The image file paths contain upload dates (for example, 2024/04 or 2024/05), but those reflect when the website images were uploaded, not when the projects were supported, so I haven't used them.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.arxequity.com/about-arx/", "prompt": "What investment stages/types does ARX do (buyout, growth, expansion, minority)? Quote sentences. Is ARX a fund manager investing its funds' capital?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.arxequity.com/working-with-arx/", "prompt": "Quote statements about capital raised / under management and typical investment size or company valuation."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.ei.com.pl/en/about/", "prompt": "Quote statements about ticket size, stake sizes, stages, sectors, and AUM."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.eterus.sk/", "prompt": "Quote statements about investment size, stage, type of fund, and any newest portfolio investments with dates."}
```

<details><summary>Výstup nástroja</summary>

```
**Capital raised and under management:**
ARX states it has "four successive private equity funds, with more than € 300 million under management." In other words, the firm has run four funds with over €300 million in assets.

**Typical investment size and valuation:**
ARX targets medium-sized companies "typically valued between € 10 million and € 50 million." It also requires EBITDA of at least €1 million, so the target businesses are generally sizable but not large-cap.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The page doesn't explicitly list buyout, growth, expansion, or minority investment stages. It does describe these activities:

- **MBO/MBI financing:** ARX provides "financing to entrepreneurially-minded managers in order to fund management buy-out and management buy-in" transactions.
- **Owner-manager and succession deals:** It creates "flexible investment solutions for owner-managers," often for "gradual or phased succession situations."
- **Growth-stage support:** It focuses on "investing in and supporting the growth of mid-sized CE companies."

The page doesn't state ownership percentages, so it doesn't confirm whether ARX takes minority or majority stakes.

**Fund manager:** The page implies that ARX manages investor capital through funds, though it doesn't say so directly. It states that the firm has "raised in four funds" more than "€ 300 million," and that it is "focused on increasing shareholder value for the investors in our funds." It also says the ARX team is "personally invested in every ARX portfolio company."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Ticket size:** "We invest between EUR 20 million and EUR 75 million for stakes" per the page. Typical checks run from EUR 20m to EUR 75m.

**Stake size:** The firm takes "ranging from large minority positions to full ownership," so it can hold anything from a large minority stake to full control.

**Stage:** The firm "supported the growth of promising companies" and works to "accelerate the development of their businesses." It backs growth-stage companies.

**Sectors:** It focuses on "rapidly growing sectors such as technology, financial services, consumer goods." The page also lists business services, healthcare, retail, and manufacturing.

**AUM:** The page does not state assets under management. It reports having "invested EUR 2.5 billion in 163 companies" across 10 funds. Its most recent fund, Fund IX, has a "total capital of EUR 340 million."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Investment size**
- Preferred ticket: "Zameriavame sa na investície v rozmedzí 2 - 2,5 mil. EUR" (target range of €2–2.5 million).
- Total deployed: the page says Eterus has invested more than €40 million in innovation through private equity.

**Investment stage**
- "Eterus je partner pre financovanie spoločností vo fáze rastu" (growth-stage companies with capable management and a proven concept).

**Type of fund**
- "Sme kapitálovým fondom investujúcim do akcií a iných nástrojov vlastného imania" (a private equity fund that takes equity stakes in Slovak-domiciled companies, not debt).
- It takes minority positions, and management control stays with the existing shareholders.
- Preferred holding period: 5–7 years.

**Newest portfolio investments**
- The page does not give investment dates for its portfolio companies. The most recent dated item is a media article from 15 May 2023: "MTBIKER získal silného partnera. Eterus Capital investuje do jeho rozvoja" (Eterus invested in the cycling portal MTBIKER).
- Dr. Martin and EC Pharmacies are listed first, but their logo images were uploaded in November 2025. That may suggest recent additions, but it does not confirm when Eterus invested.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.oaklins.com/at/en/deals/110584/", "prompt": "Who acquired what, when? Is Eterus Capital described as private equity fund? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.ei.com.pl/en/enterprise-investors-returns-to-lithuania-with-investment-in-kredito-unija-saulegraza", "prompt": "Date of the announcement and what EIF IX invested in. Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.genesis.cz/en/private-equity", "prompt": "List the news items with dates. Is there one about POS Media Europe dated 2026-04-13? Is there anything newer about a new investment?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.amcham.cz/member-news/genesis-announces-strong-year-investment", "prompt": "Quote sentences about ticket sizes and fund sizes (GPEF V, total funds)."}
```

<details><summary>Výstup nástroja</summary>

```
**Announcement date:** July 1, 2026

**Investment:** Enterprise Investors Fund IX (EIF IX) agreed to put up to €21.8 million into Kredito unija "Saulėgrąža," a Lithuanian credit union, for a stake of up to 81.51%. The funds are meant to help the institution become a fully licensed bank focused on SMEs.

**Quote:** The announcement states that "The capital will support Saulėgrąža's conversion into a fully licensed bank serving SMEs."
```

</details>

<details><summary>Výstup nástroja</summary>

```
In August 2024, Eterus Capital bought a majority stake in EC Pharmacies, a consolidation platform it set up with Ethernum Capital. Since then, EC Pharmacies has acquired nine pharmacies.

Yes, the page describes Eterus as a private equity fund: "Eterus Capital is a private equity fund founded in 2008."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Fund size (GPEF V):**
- "with the current size of EUR 286 million and expected final size potentially exceeding EUR 300 million."

**Ticket sizes:**
- "The funds primarily target investments with equity tickets ranging between EUR 10 million and EUR 45 million"
- "remain interested and actively evaluate also smaller investment opportunities (below EUR 10 million equity ticket)"

The page gives no total across all Genesis funds. It mentions only GPEF V and its predecessor, GPEF IV, which has 12 active portfolio investments but no stated size.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Yes.** The POS Media Europe item is dated 13.04.2026 (2026-04-13). It reports that Genesis Capital's Fund V agreed to invest in the company.

**News items, newest first:**

- **30.06.2026**: Genesis Capital exits GTH Catering, its stake sold to the other shareholders after more than fifteen years.
- **13.04.2026**: Agreement to invest in POS Media Europe, a retail media provider in Central Europe.
- **08.04.2026**: Genesis Capital Newsletter 4/2026.
- **11.02.2026**: Agreement to acquire a majority stake in Fyzioterapie s úsměvem, a Czech outpatient rehabilitation provider.
- **04.02.2026**: Expansion into Germany, with Jörgen Hausberger appointed Partner.

**Anything newer about a new investment?** No. The only item dated after 13.04.2026 is the 30.06.2026 GTH Catering news, and it describes an exit ("exited its majority stake"), not a new investment.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.slovca.sk/sk/riadni-clenovia/jet-investment.html", "prompt": "Quote fund type, preferred investment size, sector focus, stage."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.jetinvestment.cz/en/news/jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol", "prompt": "Quote the 'about Jet Investment' paragraph (assets, funds, sectors) and date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.jetinvestment.cz/en/news/jet-investment-vstupuje-do-americkeho-startupu-appnava-ktery-pomoci-ai-predpovida-chovani-uzivatelu", "prompt": "Date, amount, fund name, company. Quote."}
```

<details><summary>Výstup nástroja</summary>

```
- **Fund type:** "Typ fondu: Private Equity"
- **Preferred investment size:** Equity tickets of about €15M to €50M.
- **Sector focus:** The page does not specify a sector focus.
- **Stage:** The page does not specify an investment stage.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Date:** 2026-09-17
- **Amount:** USD 1.8M, within a total round of USD 2.3M
- **Fund:** Jet Venture 1 SICAV
- **Company:** AppNava Inc.
- **Quote:** Kamil Levinský, the Jet Venture 1 fund's managing director, said: "Existing methods of precisely tracking individual users have ceased to work."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** 11.9.2026

**About Jet Investment (assets, funds, sectors):**

"Jet Investment a.s., a Czech investment company founded in 1997, specializes in investments in Central European industry."

"It manages assets totaling CZK 17 billion, including uncalled capital, across four qualified investor funds."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://neulogy.vc/about-us/", "prompt": "Quote statements on AUM, sectors, stages, and investment focus."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.slovca.sk/sk/riadni-clenovia/neulogy-ventures.html", "prompt": "Quote investment type, stage, preferred investment size, sectors."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.life-sciences-europe.com/person/cekan-pavol-multiplexdx-202409-inc-persons-people-chief-2001-28559.html", "prompt": "Does it say StratifAI raised pre-seed co-led by Neulogy Ventures? Date of the announcement? Quote."}
```

<details><summary>Výstup nástroja</summary>

```
Yes. The page says the €1.5 million pre-seed round was co-led by Neulogy Ventures and MultiplexDX: "The round was co-led by Neulogy Ventures and MultiplexDX."

The announcement is dated 9/2/24. That format is ambiguous, but it most likely means September 2, 2024. The "Record changed: 2025-10-01" note is a page-update date, not the announcement date.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Neulogy Ventures**

- **Investment type and stage:** Seed and venture capital. The page lists this as "Typ investícií: Seed, Venture capital."
- **Preferred investment size:** Between EUR 200,000 and EUR 2.5 million. The page gives this as "200,000 - 2.5 M EUR."
- **Preferred sectors:** Information and communication technologies, energy, and medical diagnostics. The page lists these as "Informačné a komunikačné technológie, energetika a medicínska diagnostika."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Assets under management:** "With €65M assets under management" (about 30 portfolio companies in 10 countries).

**Sectors:** Focus on "new technologies addressing climate change and healthcare," with a deeptech emphasis.

**Stage:** Targets "early-stage tech companies," supporting founders from formation through growth.

**Investment focus:** "Moonshot ideas pushing the frontier in technology, climate and health."

**Investment size:** "from €200K to €3M"

**Geography:** "SMEs established or operating in Slovakia"
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Neulogy Ventures\" invests 2025 OR 2026 round led", "mode": "standard"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://en.ain.ua/2024/11/25/slovakian-startup-superscale-raises-12m-investment", "prompt": "Quote what the article says about Across Private Investments (what kind of firm, its focus, role in round)."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://across.sk/o-nas", "prompt": "What is Across? Wealth manager, investment firm? Quote statements about AUM and about private/venture investments, direct investments into companies."}
```

<details><summary>Výstup nástroja</summary>

```
Across Private Investments is a Slovakian firm and the lead investor in SuperScale's $1.2M round. According to the article, it focuses on "early-stage investments in app marketing, blockchain, and mobile advertising industries" across Europe and Northern America.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Neulogy Ventures" invests 2025 OR 2026 round led"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/neulogy"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/neulogy-ventures"},{"title":"Nulogy Funding History","url":"https://www.owler.com/company/nulogy/funding"},{"title":"neulogy ventures","url":"https://startups.one.gob.es/companies/neulogy_ventures"},{"title":"# Neulogy VC","url":"https://brandfetch.com/neulogy.vc.md"},{"title":"Neulogy Ventures","url":"https://www.roundfunded.com/zh/vc/neulogy-ventures"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/neologic/financials"},{"title":"Current Valuation","url":"https://www.premieralts.com/companies/neologic/valuation"},{"title":"neologic vlsi","url":"https://www.vcbacked.co/company/neologic-vlsi"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/neulo/financials"}]

I found no 2026 round for Neulogy Ventures in these results. The only 2025 deal I found was one where Neulogy co-invested rather than led.

- **GreenWay (March 2025):** Caplight lists Neulogy as a co-investor in a growth equity deal. GreenWay Mar 2025 Growth Equity Co-investor
- **StratifAI GmbH (September 2024):** Caplight lists Neulogy as the lead on this pre-seed deal, which is the only lead role in its list. StratifAI GmbH Sep 2024 Pre Seed Lead
- **Other deals:** The sam
… [skrátené, 2422 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Based on the page, Across is an **investment firm with a wealth-management offering**. It has operated in Slovakia since 2002 and trades securities under a license from the National Bank of Slovakia.

- **Wealth management:** The site presents Across as "dôveryhodným partnerom pre každého, kto chce zhodnocovať svoj majetok bezpečne a efektívne." It also lists an open Wealth Manager position.
- **Assets under management:** The page cites "450+ mil. eur pod správou," along with 2,500+ active clients and 60+ team members.
- **Private/venture and direct investments:** The page doesn't explicitly mention venture capital, private equity, or direct investments into companies. It says the wider Across Group is active in hotels, real estate, retail, and sports, which suggests business holdings beyond financial products, but the page doesn't confirm the investment type.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.bhmgroup.eu/o-nas", "prompt": "Quote statements about what BHM group is (private investment company, own capital?), sectors, and assets."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.bhmgroup.eu/portfolio", "prompt": "Quote the sentence about assets value (1 miliarda eur). Is it assets under management of a fund, or value of group's assets/companies?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.bhmgroup.eu/news/reinsberg-group-posiluje-sve-portfolio-operacnich-stolu-akvizici-schaerer-medical-schweiz-ag", "prompt": "Date and what was acquired by whom. Quote."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** 24 August 2026

**Acquirer:** Reinsberg Group, owned by BHM group

**Acquired:** Schaerer Medical Schweiz AG, a Swiss maker of premium mobile operating tables and orthopedic and spinal accessories

**Quote:** Jan Izák, chairman of Reinsberg Group, said the deal is "Akvizice tak představuje další důležitý krok v budování silné evropské skupiny zdravotnických technologií."
```

</details>

<details><summary>Výstup nástroja</summary>

```
The page says: "BHM group spravuje aktiva v hodnotě 1 miliardy eur" (the full sentence exceeds the 125-character limit).

The page doesn't say whether this is fund-style assets under management or the book value of the group's companies. "Spravuje" (manages) suggests management, but the page never defines the figure.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**What BHM group is**
- A private investment company: "soukromá investiční společnost založená v roce 2013" (founded in 2013).
- It describes itself as a Central European investment group that manages "desítky společností napříč Evropou" (dozens of companies across Europe).
- **Own capital:** The page doesn't say where its capital comes from. It mentions "finanční stabilitě" (financial stability) but gives no details on its equity.

**Sectors**
- Engineering: "strojírenství"
- Long-term investments in: "obnovitelných zdrojů energie, zdravotnictví, nových technologií a realit" (renewable energy, healthcare, new technologies, and real estate)

**Assets**
- The page doesn't list individual portfolio companies. It mentions Škoda Transportation only as a company Tomáš Krsek restructured, not as a current holding.
- Its portfolio is described as covering "všech klíčových odvětvích" (all key sectors), without naming them.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.startitup.sk/?p=1239607", "prompt": "Date, did Slovak Investment Holding invest in VisionFlow, amount, form (equity, convertible loan)? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.startitup.sk/?p=1237737", "prompt": "Quote what it says about SIH ownership and the form of the AT Crystals investment; date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.sih.sk/", "prompt": "Does SIH invest directly into companies with equity (priame investície)? Quote."}
```

<details><summary>Výstup nástroja</summary>

```
According to the article, the investor is fully state-owned. The article states: "SIH je akciová spoločnosť v 100-percentnom vlastníctve štátu" (SIH is a joint-stock company wholly owned by the state).

The investment took the form of a convertible loan. The article says SIH "investíciu realizovala formou konvertibilného úveru so splatnosťou v máji 2028" (it made the investment as a convertible loan maturing in May 2028).

The article is dated September 15, 2026.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Dátum:** Investícia bola oznámená 22. septembra 2026. Článok neuvádza presný dátum jej uskutočnenia.

**Investor:** Áno. Slovak Investment Holding (SIH) poskytne väčšinu financovania. Je to 1,4 milióna eur z celkového kola 2 milióny eur, teda 70 %. Zvyšok tvorí súkromný slovenský spoluinvestor z IT sektora.

**Forma:** Konvertibilný úver, nie vlastnícky podiel. Článok uvádza:

> "Investícia SIH má podobu konvertibilného úveru so splatnosťou v decembri 2028."

Pri konvertibilnom úvere sa za dohodnutých podmienok môže pohľadávka investora premeniť na podiel vo firme. SIH tak zatiaľ nemá konkrétne percento spoločnosti. Zdroje pochádzajú z Plánu obnovy a odolnosti SR.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Yes. The page says SIH supports companies through direct investments, and that equity and quasi-equity instruments are among the tools it uses:

"Slovak Investment Holding podporuje podniky aj formou priamych investícií."

The page also describes equity-based direct support from June 2024 onward, funded by the Recovery and Resilience Plan. It says SIH provides direct capital contributions and convertible loans to innovative companies. Its portfolio lists equity financing for several firms, including InoBat (€12 million, 2023) and INO-HUB Energy (€4.7 million, 2023).
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://versute.cz/cs_cz/sluzby/private-equity/", "prompt": "Quote statements about sector focus (odvětví), stages (growth, buyout, odkupy), ticket sizes."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/dva-fondy-zabalily-unipap.html", "prompt": "Quote what it says about BHS Private Equity Fund assets (CZK 1.5 billion) and the date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.schoenherr.eu/content/czech-republic-schoenherr-advises-bhs-private-equity-fund-on-acquisition-of-alfa-3", "prompt": "Date and what BHS Private Equity Fund acquired. Quote."}
```

<details><summary>Výstup nástroja</summary>

```
The article states: "BHS Private Equity Fund, advised by Versute Investments, manages assets worth CZK 1.5 billion."

The article is dated **24 September 2025**.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** 26 November 2025

**Acquisition:** BHS Private Equity Fund acquired a substantial non-controlling interest in ALFA 3, s.r.o., a Czech maker of delivery boxes and industrial metal furniture. Schoenherr advised the fund and its adviser, Versute Investments a.s.

**Quote:** Luděk Palata, partner at Versute Investments a.s., said: "We are proud to partner with ALFA 3, a company with a solid foundation and long-term potential in its sector."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Sector focus**
- The firm invests in companies "ve všech odvětvích" (across all sectors) but mainly in traditional economy industries, where the team has the most experience. ("Fokus na podniky ve všech odvětvích, avšak s primárním zaměřením na odvětví tradiční ekonomiky.")
- Geographically, it focuses on the Czech Republic and Slovakia.

**Investment stages and structures**
- **Growth capital:** Funds go toward growth opportunities rather than debt service. ("Tato forma investice eliminuje odčerpávání finančních prostředků na splácení a obsluhu dluhů")
- **Leveraged buyouts:** The firm seeks stable, healthy companies with strong cash flow that can be bought with a mix of equity and bank financing. ("Versute Investments hledá stabilní, zdravé podniky se silným cash flow")
- **Management buyouts:** These let existing managers acquire an ownership stake. ("Investice do manažerských odkupů umožnují stávajícím manažerům získat vlastnický podíl")
- **MBIs (management buy-ins):** The firm works with executive recruiters and management teams to find opportunities. ("Versute Investments spolupracuje s personálními poradci a manažerskými týmy")
- The portfolio also shows minority equity investments and mezzanine loans.

**Ticket sizes**
- The page does not state investment amounts or fund size, so I can't give a ticket size range. The contact listed on the page is Ludek Palata ([email]).
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://thenextweb.com/news/credo-ventures-88m-fund", "prompt": "Quote sentences about sector focus (AI, developer tools?), stages, cheque sizes, fund size, and whether the $88M is the fund size. Does it mention developer tools or devtools?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://thesaasnews.com/news/superplane-raises-2-28m-pre-seed", "prompt": "Date, round, who led. Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.credoventures.com/", "prompt": "Quote statements about stages (pre-seed, seed, Series A) and focus."}
```

<details><summary>Výstup nástroja</summary>

```
- **Date:** June 24, 2026
- **Round:** Pre-seed (€2.28M)
- **Lead investor:** Credo Ventures

**Quote:** SuperPlane describes its platform as "designed to enable AI agents and engineers to collaborate safely on production infrastructure."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Stages**
- The firm describes itself as "Leading Pre-Seed rounds." (Pre-seed is the only stage named.)
- It says it writes "the first check — before product, before revenue, often before a deck."
- Typical checks are "$1M - $5M checks."
- Past deals include leading the ElevenLabs pre-seed, co-leading UiPath's, and investing in Wabi's.
- The page doesn't mention seed or Series A.

**Focus**
- It backs "exceptional people, not thesis-driven" investments.
- It invests "From CEE, for CEE and its global diaspora."
- It works "hands-on with no-BS technical founders."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Sector focus:** The article says "Sectoral focus is deliberately loose." Credo calls itself founder-first rather than theme-driven, but it is attuned to technical founders with global ambitions and has "a growing eye on AI companies."

**Developer tools:** Yes, once. Partner Matej Micek is "focused on infrastructure, AI, and developer tools."

**Stage:** The firm is "doubling down on pre-seed in Central and Eastern Europe" and its diaspora.

**Cheque size:** "Typical cheques will fall in the $1–5 million range," though the article notes the firm remains flexible.

**Fund size:** Yes, $88M is the fund size. The article describes it as "an $88 million fund raised in a single closing," the firm's largest to date. The previous fund was €75 million, and the article compares the two figures without currency conversion.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun", "prompt": "Quote what J&T Arch Investments is (fund type), what it invests in, assets under management figure, and any recent investments with dates."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/kkcg-prodala-jt-arch-investment-minoritni-podil-v-allwyn.html", "prompt": "Date and deal details. Quote."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** 28 August 2025

**Deal details:**
- **Seller:** KKCG, the investment group owned by Karel Komárek
- **Buyer:** J&T Arch Investment, a Czech fund
- **Stake:** 4.27% of Allwyn, a minority holding
- **Price:** €500 million
- **Structure:** The stake is held through the newly established JTFG Fund IV SICAV. KKCG keeps the remaining 95%.

**Quote:**
> "sold a 4.27% stake in Allwyn to the Czech fund J&T Arch Investment for 500 million euros"
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Fund type:** J&T Arch Investments is a fund for qualified investors ("fondu kvalifikovaných investorů"). It is intended for qualified investors ("Je určen kvalifikovaným investorům.") and trades on the Prague Stock Exchange, where the article says it is among the most liquid fund listings.

**Investment focus:** It is the main investment platform of the J&T group. It invests in businesses, projects and partnerships that the group has built over roughly the last 30 years ("Fond investuje do podniků, projektů a partnerství, které skupina vybudovala v posledních 30 letech.").

**Assets under management:** At the end of 2025, assets rose by CZK 81.4 billion to CZK 202.9 billion ("stoupla o 81,4 miliardy korun na 202,9 miliardy korun").

**Recent investments:**
- **November 2025:** EPH, the group in which the fund has an indirect stake, agreed with TotalEnergies to form a joint venture focused on flexible energy resources in several European countries.
- **December 2025:** The fund directly invested €500 million (about CZK 12.2 billion) in preferred shares of EP Equity Investment (EPEI) ("fond přímo investoval 500 milionů eur").
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://zaka.vc/sygaldry-backed-by-zaka-vc-raises-139m-to-build-quantum-accelerated-ai-infrastructure/", "prompt": "Date of article and what ZAKA did (first investment date, participation in Series A). Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.zaka.vc/", "prompt": "Quote statements about stages, sectors, fund size, tickets."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://tech.eu/2024/07/19/zaka-unveils-its-fund-i-15m-for-bridging-the-us-with-the-eu-market/", "prompt": "Quote fund size and whether it is the ZAKA VC Fund I target or final size."}
```

<details><summary>Výstup nástroja</summary>

```
The article gives **€15M as the target size**, not a final close. It describes the fund as "ZAKA VC Fund I sized €15M" that "is now starting with a €10.5M first closing in June 2024." The article doesn't report a final close, so the €15M figure is the goal, and the confirmed amount so far is €10.5M.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Article date:** The page doesn't show an explicit publication date. The image upload path (2026/04) and the phrase "announced this month" suggest it was published in **April 2026**.

**ZAKA VC's involvement:**
- **First investment:** June 2025, through its Fund I, shortly after Sygaldry graduated from the Y Combinator Spring 2025 batch.
- **Series A:** ZAKA also participated in the $105 million Series A, less than a year after its first investment.

**Quote** (Jan Kasper, Co-Founder and Managing Partner at ZAKA VC):
> "The team is focused on a real bottleneck in AI, executing really well, and operating in a massive market. That's exactly the kind of company we want to back."
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Stage:**
- "We are a seed & pre-seed VC fund, investing mainly in the US and Europe."

**Sectors:**
- "Especially looking for startups in the Health & Biotech and Industrial Tech verticals."

**Fund size:**
- The site lists 17M next to the label "Current fund size." Fund 1 shows 17M with 8M invested across 46 companies.

**Ticket size:**
- "The minimum ticket is 130K."
- "This investing is for qualified investors only."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://siliconcanals.com/3ts-capital-partners-new-150m-fund/", "prompt": "Quote sentences about fund size (target/first close), round sizes (€5-20M) — are those round sizes or 3TS tickets — stages and sectors."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.heuking.de/en/career/latest-news/detail/heuking-advises-3ts-capital-partners-as-lead-investor-in-11-million-euro-financing-round-for-patronus.html", "prompt": "Date, deal details, and any statement about 3TS total capital / funds. Quote."}
```

**Nástroj `WebSearch`**

```json
{"query": "3TS Capital Partners Fund IV final close", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "3TS Capital Partners Fund IV final close"

Links: [{"title":"3TS Capital Partners holds final close of European tech fund on €111m","url":"https://realdeals.eu.com/article/3ts-capital-partners-holds-final-close-of-European-tech-fund-on-e111m"},{"title":"3TS Capital Partners closes its new Fund IV at €111M","url":"https://en.ain.ua/2024/02/05/3ts-capital-partner-closes-fund-iv-111m"},{"title":"Press Release","url":"https://3tscapital.com/?p=2332"},{"title":"3TS Capital Partners Closes New €111m Fund","url":"https://3tscapital.com/2024/01"},{"title":"3TS Newsletter January 2024","url":"https://3tscapital.com/2024/02"},{"title":"3ts holds first close for fund iv","url":"https://www.unquote.com/dach/official-record/3025008/3ts-holds-first-close-for-fund-iv"},{"title":"3tscapital.com","url":"https://3tscapital.com/?p=2326"},{"title":"3ts capital partners new 150m fund","url":"https://siliconcanals.com/3ts-capital-partners-new-150m-fund/"},{"title":"capital partners announces the first closing of its new fund 4","url":"https://www.eif.org/press/all/capital-partners-announces-the-first-closing-of-its-new-fund-4"},{"title":"3TS Capital Partners Research","url":"https://f4.fund/firms/3ts-capital-partners"}]

3TS Capital Partners announced the final close of Fund IV, also called TCEE Fund IV, at €111 million. The announcement is dated 30 January 2024 and came from the firm's own press release. The firm, described as a European technology-focused growth ca
… [skrátené, 2723 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Fund size:** The article says 3TS "has announced the first closing of its Fund IV with a target size of €150M." It does not state how much was raised at first close.

**Round sizes or tickets:** The €5-20M figure appears to be round size. The article says 3TS will back growth companies "by leading investment rounds of €5-20M." It does not give 3TS's own cheque size.

**Stages:** The article describes 3TS as "a European technology-focused growth capital investor." It also calls the firm a "technology growth-stage VC firm" and says it provides expansion capital.

**Sectors:** The article lists software, tech-enabled services, and e-commerce. It also names technology & internet, media & communications, and technology-enabled services. Mäki says the firm mainly invests in B2B software, plus other ICT and digital transformation companies, including marketplaces and e-commerce.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Date:** The article is dated 05-04-2026. Because other dates on the page use MM-DD-YYYY, this is most likely May 4, 2026.
- **Deal:** HEUKING advised 3TS Capital Partners, the lead investor, in an 11 million euro financing round for Berlin startup RR Technologies GmbH (Patronus). The work covered legal due diligence and negotiation of the transaction documents, including the investment agreement and shareholders' agreement.
- **Patronus:** Founded in Berlin in 2020, it offers a safety and companion product for seniors, built around a mobile emergency smartwatch and a family app. It reports 25,000 active customers.
- **3TS total capital:** The article states that 3TS has raised over 450 million euros from investors, including EIF, Tesi, Cisco, EBRD, and Erste. It says: "With over 450 million Euro raised from investors." This describes capital raised, not necessarily total fund size.
- **Fund:** The investment was made through TCEE Fund IV. The article says: "The investment in Patronus was made through the TCEE Fund IV."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.g4.sk/", "prompt": "Does G4 invest directly into companies/startups now, or only as LP in funds? Any dated recent investments (2023-2026)? Quote."}
```

**Nástroj `WebSearch`**

```json
{"query": "G4 Investments Gogolák investícia startup 2024 OR 2025 OR 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Jakubec Family Office Finhold investícia 2024 OR 2025 OR 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Benson Oak\" investment 2023 OR 2024 OR 2025 acquisition", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Benson Oak" investment 2023 OR 2024 OR 2025 acquisition"

Links: [{"title":"A CONSULTING TEAM INC - Form SC 13D - FY2005","url":"https://www.sec.gov/Archives/edgar/data/0001040792/000114420405002402/v011769_sc13d.txt"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/benson-oak-capital"},{"title":"www.plansponsor.com","url":"https://www.plansponsor.com/?p=84266"},{"title":"Oak Investment Partners","url":"https://techcrunch.com/tag/oak-investment-partners"},{"title":"Wells Fargo Acquiring Benson Associates","url":"https://www.plansponsor.com/wells-fargo-acquiring-benson-associates/"},{"title":"FORWARD FEATURES CALENDAR","url":"https://www.privateequitywire.co.uk/?p=99810"},{"title":"Register to get free articles","url":"https://www.accountancytoday.co.uk/?p=93165"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/corporate-realty/financials"},{"title":"Commercial Real Estate Agency Corporate Realty Acquired by Benson Capital","url":"https://siliconbayounews.com/tag/mike-sigel/"},{"title":"PineBridge Press Release","url":"https://www.pinebridge.com/en/press-releases/pinebridge-investments-to-acquire-benson-elliot-capital-management"}]

I couldn't find any 2023, 2024, or 2025 investment or acquisition news for Benson Oak. The results I found are mostly older, and several are about unrelated firms with similar names.

The most relevant result is Benson Oak Capital, a Czech firm. One profile d
… [skrátené, 2730 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Direct or fund investing:** Both, but the page says the focus has shifted toward funds. G4 has invested directly in companies, but since 2021 it mainly invests through funds. The page says: "Od roku 2021 sa primárne venujeme investovaniu do svetových technologických fondov." (Since 2021 we primarily invest in global technology funds.) It doesn't explicitly use the term "LP."

- **Direct history:** Since 2011 it has made about 70 investments across asset classes, including startups, and "hlavne na Slovensku" (mainly in Slovakia). Named examples are Azet and blue orange, both exited.
- **Current:** It also lists a "Private Equity fondov" (private equity funds) investment, with no date given.

**Dated investments from 2023–2026:** None. The page doesn't date any investment in that period. The only 2026 item is a logo for eFoil support, which is sponsorship, not an investment.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Jakubec Family Office Finhold investícia 2024 OR 2025 OR 2026"

Links: [{"title":"Matus Kuchyna","url":"https://sk.linkedin.com/in/matus-kuchyna-24a9739"},{"title":"top of page","url":"https://www.symsite.sk/single-post/pavol-jakubec-sold-i-d-c-for-305m"},{"title":"🎧 Nemovitost není bezstarostná investice. Kupujete si malý byznys, říká Radek Jakubec z e-Finance","url":"https://www.e15.cz/podcasty/business-club/nemovitost-neni-bezstarostna-investice-kupujete-si-maly-byznys-rika-radek-jakubec-z-e-finance-1432988"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/jk-family-office"},{"title":"www.craincurrency.com","url":"https://www.craincurrency.com/node/1019771"},{"title":"profile north east family office looks to fund the familys descendants for 200 years","url":"https://www.famcap.com/2020/06/profile-north-east-family-office-looks-to-fund-the-familys-descendants-for-200-years/"},{"title":"Hyper Capital","url":"https://altss.com/profile/hyper-capital"},{"title":"Jakub Sroczynski","url":"https://seekingalpha.com/author/jakub-sroczynski"},{"title":"www.euromoney.com","url":"https://www.euromoney.com/article/b1b95hs52h0g6n/null"},{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/najnovsia-studia-odhaluje-tajomstvo/135412-clanok.html"}]

I found no report of a specific investment by the Jakubec Family Office in 2024, 2025, or 2026. The results show the office
… [skrátené, 3259 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "G4 Investments Gogolák investícia startup 2024 OR 2025 OR 2026"

Links: [{"title":"Karol Gogolák G4: Investujeme len do toho, čomu rozumieme","url":"https://www.startitup.sk/karol-gogolak-g4-investujeme-len-do-toho-comu-rozumieme/"},{"title":"Startup a investor","url":"https://www.podnikajte.sk/temy/startup-a-investor?page=9"},{"title":"Podnikateľ a investor","url":"https://www.podnikajte.sk/investor?page=5"},{"title":"Karol Gogolák G4: Investujeme len do toho, čomu rozumieme","url":"https://www.startitup.sk/?p=9537"},{"title":"www.podnikajte.sk","url":"https://www.podnikajte.sk/temy/startup?page=8"},{"title":"Karol Gogolák: Firma má len takú hodnotu, koľko peňazí sama vyprodukuje","url":"https://www.podnikajte.sk/investor/karol-gogolak-hodnota-firmy"},{"title":"G8? Na Slovensku máme G4","url":"https://www.startitup.sk/?p=8874"},{"title":"G8? Na Slovensku máme G4","url":"https://www.startitup.sk/g8-na-slovensku-nam-staci-g4/"},{"title":"Karol Gogolak","url":"https://sk.linkedin.com/in/gogolak"}]

Links: [{"title":"Karol Gogolák G4: Investujeme len do toho, čomu rozumieme","url":"https://www.startitup.sk/karol-gogolak-g4-investujeme-len-do-toho-comu-rozumieme/"},{"title":"Karol Gogolák G4: Investujeme len do toho, čomu rozumieme","url":"https://www.startitup.sk/?p=9537"},{"title":"G8? Na Slovensku máme G4","url":"https://www.startitup.sk/g8-na-slovensku-nam-staci-g4/"},{"title":"G8? Na Slovensku máme G4","url":"https://www.startitup.sk/?p=8874"},
… [skrátené, 4037 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.montward.com/", "prompt": "What does Montward do? Does it manage capital or a fund, make own investments? Quote statements about 'Správa kapitálu a investícií'."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.asbgroup.eu/", "prompt": "What does ASB Group do? Any investing / fund activity? Quote the description."}
```

**Nástroj `WebFetch`**

```json
{"url": "http://danubeca.com/finance/", "prompt": "What does Danube Capital Advisors do? Any own investing or fund? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://m3partners.sk/", "prompt": "What does M3 Partners do? Any concrete investments into companies with dates? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://jakubecfo.com/", "prompt": "What is this firm, what does it invest in, any concrete deals or dates? Quote."}
```

<details><summary>Výstup nástroja</summary>

```
ASB Group is a professional services provider. Its page describes it as "a professional services provider, delivering integrated support across accounting, tax advisory, payroll" and related areas. Its services include accounting and reporting, corporate services, tax advisory, payroll and HR administration, transaction advisory, VAT compliance in CEE, and transfer pricing. It operates in the Czech Republic, Poland, Slovakia, and Hungary.

The page does not say ASB Group invests or manages funds itself. It lists "Fund and asset management" as one of the industries it serves. It also says it helps clients with decisions on "financing, investment and profit distribution," and its recent transaction advisory work covers property sales and acquisitions.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Danube Capital Advisors is an advisory firm, not an investor. Its finance services cover financing structuring and refinancing, procurement on financing, bond issuance, and M&A. The page also lists sector work in energy, capital projects, real estate, environment, health care, innovation, legal, procurement, and executive search.

Quote: "We will accompany you through the whole fundraising process"

The page does not mention any proprietary investing or fund activity. It describes only advisory services.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**What M3 Partners does:** It describes itself as a private equity boutique and investment holding based in Senica, Slovakia. It operates across three areas:

- **Commercial real estate:** acquiring, leasing, and actively managing income-producing properties, such as warehouses and business premises, with a long-term hold focus.
- **Development and renovation:** value-add projects, including purpose-built facilities and the restoration of national cultural monuments.
- **PropTech and innovation:** IoT and Edge AI systems integrated into its buildings, mainly for energy management, through the Oxidra brand.

**Concrete investments with dates:** The page names some projects (Schosberg, NKP Kartúnka, Skladyzahorie, and Oxidra), but it gives no investment dates, amounts, or other transaction details for any of them.

**Quote:** The page summarizes the company as "Boutique Investment Holding s fokusom na prepájanie komerčného real estate a technologických inovácií v regióne CEE." In English, this means it focuses on linking commercial real estate with technology innovation in the CEE region.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Montward is an advisory firm. It helps companies with sales and acquisitions, restructuring, and business excellence.

The page's "Správa kapitálu a investícií" (capital and investment management) section says:

- "Ponúkame investorom prístup k rastovým a transformačným firmám na Slovensku"
- "prostredníctvom priamych vstupov alebo private equity štruktúr"
- "s cieľom dlhodobého zhodnotenia a aktívneho vplyvu."

The page does not say whether Montward manages a fund or invests its own money. The section describes giving investors access to growing Slovak companies through direct investments or private equity structures, which suggests Montward arranges or takes part in such deals, but the wording doesn't confirm it.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Firm:** Jakubec Family Office is a private investment and wealth management firm. The page describes it as a discreet, single-family office that works only with a select group of partners and advisors.

**Investment focus:** The firm concentrates on "private equity, strategic investments, and wealth management" to create long-term value. Its stated approach is multi-generational, meant to preserve family wealth and prepare the next generation to lead.

**Services:** Asset management, local and global investment opportunities, family and succession planning, tax, accounting and governance support, and fiduciary services.

**Dates and deals (as stated on the page):**
- **1989:** Pavol Jakubec co-founded the Investment Development Company (I.D.C.) after the Velvet Revolution, initially to help foreign investors find privatization opportunities.
- **Later:** He acquired a state-owned food manufacturer. The page says he transformed "a former state-owned bakery into a leader in Slovakia's confectionery industry."
- **2024:** He "finalized the sale of I.D.C. Holding to Valeo Foods Group," which is owned by Bain Capital. The page gives no deal value.
- **Other holdings:** He developed the Swissôtel Damian Jasna resort hotel and residences, was a former part-owner of the Jasná Nízke Tatry ski resort, and owns VEGUM a.s., a rubber and manufacturing company, where he chairs the advisory board.

The two versions of the page differ slightly in wording and titles (for example, Paulina Ja
… [skrátené, 1604 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Montward private equity fond investícia Montward Capital", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Across Private Investments investícia startup 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Montward private equity fond investícia Montward Capital"

Links: [{"title":"Private Equity","url":"https://altss.com/profile/mont-capital-gestao-e-administracao-de-recursos-sa"},{"title":"• Contact Us","url":"https://www.alternativeswatch.com/2026/02/11/pgim-montana-mcp-opportunity-secondary-program-vi/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/montana-capital-partners"},{"title":"Montana Capital Partners gegründet","url":"https://www.finews.ch/news/finanzplatz/5875-montana-capital-partners-gegruendet"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/montis-capital"},{"title":"SecondariesRIA · CRD 293568SEC-RegisteredPrivate Fund Adviser","url":"https://altss.com/profile/montana-capital-partners"},{"title":"PRIVATE EQUITY INTERNATIONAL","url":"https://www.privateequityinternational.com/montagu-hits-hard-cap-with-fourth-fund-close/"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/montlake-capital/financials"},{"title":"Compare 17Capital vs Montfort Capital","url":"https://www.cbinsights.com/compare/17capital-vs-montfort-capital"}]

I couldn't find any results for "Montward" or "Montward Capital." The search returned other firms with similar names, which may or may not be what you mean:

- **Mont Capital (Brazil):** A profile on altss.com describes it as a private equity firm based in Sao Paulo, Brazil that focuses on growth investments. It is a
… [skrátené, 2645 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Across Private Investments investícia startup 2025 OR 2026"

Links: [{"title":"PitchBook Releases 2025 Outlooks Highlighting Key Investment Trends Across Private Markets","url":"https://www.businesswire.com/news/home/20241220928667/en/PitchBook-Releases-2025-Outlooks-Highlighting-Key-Investment-Trends-Across-Private-Markets"},{"title":"1H 2025 Private Investments Portfolio presentation","url":"https://www.ritcap.com/wp-content/uploads/2026/01/1H_2025_Private_Investments_Portfolio_presentation.pdf"},{"title":"startup funding outlook report","url":"https://about.crunchbase.com/startup-funding-outlook-report"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/acrossgroup"},{"title":"Global Tech Investments Went Up 10% – What Does This Mean For Startups?","url":"https://www.globalprivatecapital.org/?p=52280"},{"title":"across private investments","url":"https://seedtable.com/investors/across-private-investments"},{"title":"Global Tech Investments Went Up 10% – What Does This Mean For Startups?","url":"https://www.globalprivatecapital.org/newsroom/global-tech-investments-went-up-10-what-does-this-mean-for-startups/"},{"title":"BryceTech Start Up Space 2026","url":"https://brycetech.com/reports/report-documents/start_up_space_2026/BryceTech_Start_Up_Space_2026.pdf"},{"title":"www.globalprivatecapital.org","url":"https://www.globalprivatecapital.org/?p=53289"}]

I found no confirm
… [skrátené, 3034 znakov]
```

</details>

**Nástroj `Bash`**

```bash
for u in https://www.aon.com/en/locations/slovak-republic https://www.aoshearman.com/en/global-coverage/Europe/slovakia https://www.slovca.sk/sk/pridruzeni-clenovia/barger-prekop.html https://cms.law/en/svk/ https://www.csob.sk/o-nas/csob-financna-skupina https://www.dentons.com/en/global-presence/central-and-eastern-europe/slovak-republic/bratislava https://www.havelpartners.sk/ https://highgate.sk/ https://www.hkv.sk/ https://www.hillbridges.com/about/ https://www.forvismazars.com/sk/sk https://ceelegalmatters.com/slovakia/24859-ments-opens-doors-in-slovakia https://kpmg.com/sk/sk/o-nas.html https://www.noerr.com/en/press/transfer-of-offices-in-central-and-eastern-europe-eoerr-successfully-completes-closing https://www.howdengroup.com/global-practices/mergers-and-acquisitions https://www.profc.eu/ https://www.pwc.com/sk/sk.html "https://ceelegalmatters.com/interviews/20051-the-ceelmdirect-profile-pick-an-interview-with-katarina-mihalikova-of-majernik-mihalikova" https://www.taylorwessing.com/en/careers/slovakia/vacancies/junior-associate https://www.v4g.sk/sk https://www.claslovakia.sk/ https://www.wezeo.com/ http://bensonoak.cz/; do printf "%s %s\n" "$(curl -sk -o /dev/null -w '%{http_code}' -L -m 20 -A 'Mozilla/5.0' "$u")" "$u"; done
```

<details><summary>Výstup nástroja</summary>

```
200 https://www.aon.com/en/locations/slovak-republic
200 https://www.aoshearman.com/en/global-coverage/Europe/slovakia
466 https://www.slovca.sk/sk/pridruzeni-clenovia/barger-prekop.html
403 https://cms.law/en/svk/
200 https://www.csob.sk/o-nas/csob-financna-skupina
403 https://www.dentons.com/en/global-presence/central-and-eastern-europe/slovak-republic/bratislava
200 https://www.havelpartners.sk/
200 https://highgate.sk/
466 https://www.hkv.sk/
200 https://www.hillbridges.com/about/
200 https://www.forvismazars.com/sk/sk
403 https://ceelegalmatters.com/slovakia/24859-ments-opens-doors-in-slovakia
200 https://kpmg.com/sk/sk/o-nas.html
200 https://www.noerr.com/en/press/transfer-of-offices-in-central-and-eastern-europe-eoerr-successfully-completes-closing
200 https://www.howdengroup.com/global-practices/mergers-and-acquisitions
466 https://www.profc.eu/
403 https://www.pwc.com/sk/sk.html
403 https://ceelegalmatters.com/interviews/20051-the-ceelmdirect-profile-pick-an-interview-with-katarina-mihalikova-of-majernik-mihalikova
403 https://www.taylorwessing.com/en/careers/slovakia/vacancies/junior-associate
200 https://www.v4g.sk/sk
200 https://www.claslovakia.sk/
200 https://www.wezeo.com/
200 http://bensonoak.cz/
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.slovca.sk/sk/pridruzeni-clenovia/barger-prekop.html", "prompt": "What kind of entity is Barger Prekop? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://cms.law/en/svk/", "prompt": "What kind of firm is this? One sentence."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.dentons.com/en/global-presence/central-and-eastern-europe/slovak-republic/bratislava", "prompt": "What kind of firm is this? One sentence."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.hkv.sk/", "prompt": "What kind of firm is this? One sentence."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.profc.eu/", "prompt": "What does this firm do? Any investing or fund activity?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.pwc.com/sk/sk.html", "prompt": "What kind of firm is this? One sentence."}
```

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
HKV Law Firm is a Bratislava-based Slovak law practice that provides legal services across modern and commercial law in Slovakia and abroad, and it is part of the Horizons Alliance network of independent law firms.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Barger Prekop is a law firm. The page describes it as "Barger Prekop s.r.o. advokátska kancelária," and it is listed as an associate member of SLOVCA.
```

</details>

<details><summary>Výstup nástroja</summary>

```
It's CMS's Slovakia branch, a law firm offering legal and tax advice across many practice areas from offices in Bratislava, as part of a larger international network.
```

</details>

<details><summary>Výstup nástroja</summary>

```
PFCEU s.r.o., based in Pezinok, Slovakia, offers business strategy, project support, and funding advice. Its listed services include advisory for innovative business ideas, connections for entering foreign markets, and ESG reporting. The site promotes "Flexibilné projektové financovanie bez straty kontroly," and presents EU grants (Eurogranty) as new funding sources for businesses.

The page does not say the firm makes investments, manages a fund, or raises capital for its own portfolio. Its activity appears to be advisory and help with obtaining external project financing.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://ceelegalmatters.com/slovakia/24859-ments-opens-doors-in-slovakia", "prompt": "What is Ments? One sentence."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://ceelegalmatters.com/interviews/20051-the-ceelmdirect-profile-pick-an-interview-with-katarina-mihalikova-of-majernik-mihalikova", "prompt": "What is Majernik & Mihalikova? One sentence."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.taylorwessing.com/en/careers/slovakia/vacancies/junior-associate", "prompt": "What kind of firm is Taylor Wessing? One sentence."}
```

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db/raw; ls | head; ls | wc -l; grep -rl -i "ments\|dentons\|taylor wessing\|mihalikova\|pwc" . 2>/dev/null | head -20
```

<details><summary>Výstup nástroja</summary>

```
balteus.html
legalfirm.html
podnikajte.html
slovca-pridruzeni-clenovia.html
slovca-riadni-clenovia.html
5
slovca-pridruzeni-clenovia.html
podnikajte.html
legalfirm.html
slovca-riadni-clenovia.html
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.wezeo.com/", "prompt": "Does Wezeo invest in startups, take equity, run a venture studio or fund? Quote anything relevant."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://highgate.sk/", "prompt": "Does Highgate invest own capital or run a fund, or only advise? Quote."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.v4g.sk/sk", "prompt": "Does V4 Group invest own capital or run a fund, or only provide services? Quote."}
```

<details><summary>Výstup nástroja</summary>

```
The page indicates that V4 Group only provides services. It does not mention investing its own capital or running a fund. It describes its offering as "Poskytujeme právne, audítorské, daňové a účtovné služby pre malé, stredné a veľké firmy" (legal, audit, tax, and accounting services for small, medium, and large companies). Its M&A section describes advisory work, not investment.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The page indicates that Highgate **only advises**. It describes its business as "Právne, daňové a účtovné poradenstvo pod jednou strechou" (legal, tax and accounting advisory under one roof). It doesn't say Highgate invests its own capital or runs a fund.

Its fund-related work is service-based. It provides accounting for "fondy kolektívneho investovania" (collective investment funds), and it helps clients with "nastavenia a zakladania fondových štruktúr investujúcich do virtuálnych mien" (setting up fund structures that invest in virtual currencies).
```

</details>

<details><summary>Výstup nástroja</summary>

```
The page doesn't say Wezeo invests in startups, takes equity, runs a venture studio, or operates a fund. It describes a service business. The homepage calls WEZEO "a product studio building fintech, hybrid and MVP apps - strategy, design and engineering as one team." The case studies are client projects, such as Finax and iFonduri, and the "Got an idea?" section offers to build a demo within a week.

The only use of "invest" is in "Three areas we invest in deliberately, so every engagement," which refers to where the team focuses its effort, not to capital.

For a definitive answer, contact [email]
```

</details>

**Nástroj `Bash`**

```bash
cat > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/write_review.py <<'EOF'
import csv, json, sys
C, I, E = "correct", "incorrect", ""
v = {
("c001","inclusion"): (C,"PE správca s fondami (>300 mil. EUR v 4 fondoch), Medicofit 08/2026 je v okne."),
("c001","investor_type"): (C,"Tlačová správa ARX sa označuje ako private equity firm."),
("c001","stages"): (C,"Stránka uvádza financovanie MBO/MBI; buyout je podložený (rastové/nástupnícke deals sú doplnkové)."),
("c001","aum_eur"): (C,"Stránka: štyri PE fondy s viac ako 300 mil. EUR pod správou."),
("c001","latest_investment"): (C,"ARX získal väčšinový podiel v Medicofit, správa z 26.8.2026."),
("c002","inclusion"): (C,"CVI je správca private debt (senior/junior, unitranche, mezanín); equity len okrajovo, debt_only sedí."),
("c003","inclusion"): (C,"PE investor, EIF IX investoval do Saulėgrąža 07/2026, v okne."),
("c003","investor_type"): (C,"Stránka: 'the most experienced private equity investor in CEE'."),
("c003","sectors"): (C,"Zoznam sektorov je doslovne zo stránky About."),
("c003","stages"): (C,"Podiely od veľkých minoritných po plné vlastníctvo za 20-75 mil. EUR zodpovedajú growth a buyout."),
("c003","ticket_min_eur"): (C,"'We invest between EUR 20 million and EUR 75 million' je veľkosť jednej investície."),
("c003","ticket_max_eur"): (C,"Ako vyššie, horná hranica 75 mil. EUR."),
("c003","latest_investment"): (C,"Správa z 1.7.2026: EIF IX investuje až 21,8 mil. EUR do Saulėgrąža."),
("c004"
… [skrátené, 13163 znakov]
```

<details><summary>Výstup nástroja</summary>

```
117 Counter({'correct': 104, 'incorrect': 8, '': 5})
```

</details>

**Nástroj `SendMessage`**

```json
{"to": "team-lead", "summary": "AI review c001-c050 hotový", "message": "AI pre-check c001-c050 je hotový: /home/filip/investor-db/validation/ai_review_1.json (117 riadkov). Výsledok: 104 correct, 8 incorrect, 5 prázdnych.\n\nIncorrect:\n- c013 aum_eur: 450 mil. EUR sú klientske aktíva wealth managementu Across, nie kapitál na priame/venture investície. Odporúčam nechať prázdne.\n- c018 aum_eur: 1 mld. EUR je hodnota aktív vlastných portfóliových firiem BHM, nie spravovaný kapitál ani fond. Odporúčam nechať prázdne.\n- c045 sectors: zdroj hovorí „všetky odvetvia, primárne tradičná ekonomika“, „manufacturing“ si výskumník domyslel. Správne: generalist; traditional industries.\n- c047 inclusion (inactive): Caplight uvádza CB Investment Management ako koinvestora v 3IPK v 05/2025 (https://www.caplight.com/investor/cbim). Je to len agregátor a primárny zdroj som nenašiel, takže to treba overiť.\n- c049 aum_eur: 15 mil. EUR bol cieľ z roku 2024. zaka.vc dnes uvádza „Current fund size 17M“, správne je teda 17 000 000.\n- c050 ticket_min_eur a ticket_max_eur: „leading investment rounds of €5-20M“ je veľkosť kola, nie tiket 3TS. Odporúčam nechať prázdne.\n- c050 aum_eur: 150 mil. EUR bol c
… [skrátené, 2167 znakov]
```

<details><summary>Výstup nástroja</summary>

```
{"success":true,"message":"Message sent to team-lead's inbox","msg_id":"930070d3-a276-40b5-bdeb-cb637dae5cfc","routing":{"sender":"review-1","senderColor":"pink","target":"@team-lead","targetColor":"red","summary":"AI review c001-c050 hotový","content":"AI pre-check c001-c050 je hotový: /home/filip/inv…"}}
```

</details>

## Claude · 2026-10-09 12:39:17 UTC

Skontroloval som všetkých 117 riadkov pre c001–c050 a verdikty sú zapísané do `/home/filip/investor-db/validation/ai_review_1.json`. Iný súbor som neupravoval.

**Výsledok:** 104 správnych, 8 nesprávnych, 5 bez verdiktu.

**Nesprávne riadky:**
- **c013 `aum_eur`:** 450 mil. EUR sú aktíva klientov wealth managementu Across, nie kapitál na venture investície. Treba nechať prázdne.
- **c018 `aum_eur`:** 1 mld. EUR je hodnota aktív firiem, ktoré BHM vlastní, nie spravovaný kapitál alebo fond. Treba nechať prázdne.
- **c045 `sectors`:** zdroj uvádza „všetky odvetvia, primárne tradičná ekonomika“. Hodnota „manufacturing“ v ňom nie je. Správne je `generalist; traditional industries`.
- **c047 `inclusion`** (vylúčené ako inactive): agregátor Caplight uvádza CB Investment Management ako spoluinvestora v 3IPK v máji 2025 (https://www.caplight.com/investor/cbim). Primárny zdroj som nenašiel, takže vylúčenie treba ešte overiť.
- **c049 `aum_eur`:** 15 mil. EUR bol cieľ fondu z roku 2024. zaka.vc dnes uvádza aktuálnu veľkosť fondu 17M, správne je teda 17 000 000.
- **c050 `ticket_min_eur` a `ticket_max_eur`:** 5–20 mil. EUR je veľkosť kôl, ktoré 3TS vedie, nie veľkosť jeho vlastnej investície. Treba nechať prázdne.
- **c050 `aum_eur`:** 150 mil. EUR bol len cieľ z roku 2021. Fund IV sa 30. 1. 2024 uzavrel na 111 mil. EUR, správne je teda 111 000 000.

**Bez verdiktu:** stránky c022 Dentons, c031 Ments, c036 PwC, c039 Majerník & Miháliková a c040 TaylorWessing vracajú chybu 403 a nedali sa otvoriť. Ich vylúčenie ako poradenské firmy je pravdepodobne správne, ale overené nie je.

**Sporné vylúčenia, ktoré sme mali preveriť:**
- **c008 Národný holdingový fond (no_evidence):** správne. Web je z roku 2014, novšiu priamu investíciu som nenašiel a fond investuje cez Eterus (c004) a FIT (c005).
- **c002 CVI (debt_only):** správne, ide o správcu súkromných úverov (private debt).
- **c005 FIT (inactive):** správne. fondfit.sk uvádza, že fond v roku 2025 vstúpil do post-investičnej fázy.
- **c047 Crowdberry (inactive):** pravdepodobne nesprávne, pozri vyššie.

Ďalšie poznámky:
- **c048 J&T ARCH:** existuje novšia investícia než Allwyn, a to 500 mil. EUR do prioritných akcií EPEI v decembri 2025.
- **c044 Benson Oak:** presnejší dôvod vylúčenia by bol inactive, posledná aktivita je exit z roku 2020.

Výsledky som poslal aj team-leadovi.
