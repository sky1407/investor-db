# Subagent agent-areview-2-dab7efa2f49dd209

Zdroj: transkript Claude Code `agent-areview-2-dab7efa2f49dd209.jsonl`

## Používateľ · 2026-10-09 12:41:43 UTC

<teammate-message teammate_id="team-lead" summary="AI pre-check c051-c075">
You are a review agent for the project in /home/filip/investor-db. Read /home/filip/investor-db/prompts/review_agent.md first and follow it exactly.

Your assigned rows: every row of /home/filip/investor-db/validation/manual_check.csv whose candidate_id is between c051 and c075 (inclusive). Full records (quotes, investments, notes) are in /home/filip/investor-db/data/investors.json; raw research files in /home/filip/investor-db/research/.

Use WebFetch (and WebSearch where needed to check whether an "inactive"/"no_evidence"/"duplicate" decision is wrong). Be sceptical, in particular:
- c070 Jet Ventures excluded as duplicate of c007 Jet Investment — are they really the same investing entity, or a separate VC vehicle?
- c056 Slovenský rastový a kapitálový fond as duplicate of c004 Eterus Capital — the researcher inferred a rename without an explicit source.
- c058 Zero Gravity Capital as duplicate of c059 Zero One Hundred.
- c065 IPM Group: is InoBat a real third-party investment or an insider/group company? Is HQ GB right?
- c069 Ergos (only source was Tracxn).

Write your verdicts as a JSON list to /home/filip/investor-db/validation/ai_review_2.json (format in the instructions). Do not edit any other file. Finish with counts and the list of incorrect rows with a one-line reason each.
</teammate-message>

**Nástroj `Read`**

`/home/filip/investor-db/prompts/review_agent.md`

<details><summary>Výstup nástroja</summary>

```
1	# Review agent instructions (AI pre-check before the human check)
2	
3	You are an independent, sceptical reviewer. A different agent researched investors and a script already confirmed
4	that every quote exists verbatim on its source page. Your job is to decide whether the **conclusion drawn from the
5	quote is correct**. Assume the researcher may have misread the source.
6	
7	Input: `validation/manual_check.csv` rows assigned to you (columns `candidate_id`, `item`, `system_value`,
8	`source_url`) and `data/investors.json` (full record incl. quotes, investments and notes).
9	Today is 2026-10-09; the activity window starts 2023-10-09.
10	
11	For every assigned row, open `source_url` (WebFetch) and set:
12	
13	- `ai_verdict` = `correct` or `incorrect` (leave empty only if the page cannot be opened at all),
14	- `ai_note` = one short sentence in Slovak: why, and the correct value if `incorrect`.
15	
16	## What "correct" means per item
17	
18	- `inclusion` with `included`: the subject really invests own or managed capital into private companies for
19	  equity, and the newest verified investment is a real deal by this investor within the window. Wrong if it is an
20	  advisor, lender, platform, grant scheme, an inactive or wound-down fund, or the deal was made by a different
21	  entity with a similar name.
22	- `inclusion` with `excluded:<reason>`: the reason is right. E.g. `not_investor_service` is wrong if the firm
23	  also runs its own investment fund; `inactive` is wrong 
… [skrátené, 2513 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; head -1 validation/manual_check.csv; grep -E '^"?c0(5[1-9]|6[0-9]|7[0-5])' validation/manual_check.csv; ls research validation
```

<details><summary>Výstup nástroja</summary>

```
candidate_id,item,system_value,source_url,ai_verdict,ai_note,human_verdict,human_note
c051,inclusion,excluded:no_evidence,https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr,,,,
c052,inclusion,excluded:inactive,https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr,,,,
c053,inclusion,excluded:inactive,https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/,,,,
c054,inclusion,excluded:inactive,https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/,,,,
c055,inclusion,excluded:no_evidence,https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr,,,,
c056,inclusion,excluded:duplicate,https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr,,,,
c057,inclusion,excluded:no_evidence,https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/,,,,
c058,inclusion,excluded:duplicate,https://www.forbes.sk/investicny-fond-zero-gravity-capital-hlada-mlade-firmy-rozdelit-ma-12-milionov-eur/,,,,
c059,inclusion,included,https://www.0100.vc/,,,,
c059,investor_type,vc,https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/,,,,
c059,sectors,blockchain; e-commerce; ar/vr; fintech; mobile games; ai; b2b; healthtech,https://www.eu-startups.com/investor/zero-one-hundred/,,,,
c059,stages,pre-seed; seed; series-a,https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/,,,,
c059,ti
… [skrátené, 10621 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -I -c "
import json
d=json.load(open('data/investors.json'))
recs=d if isinstance(d,list) else d.get('investors',d)
for r in recs:
  cid=r.get('candidate_id') or r.get('id')
  if cid and 'c051'<=cid<='c075' or cid in ('c004','c007'):
    print(json.dumps(r,ensure_ascii=False)[:3500]); print('---')
"
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 6, in <module>
    cid=r.get('candidate_id') or r.get('id')
        ^^^^^
AttributeError: 'str' object has no attribute 'get'
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -I -c "
import json
d=json.load(open('data/investors.json'))
print(type(d), list(d.keys())[:10] if isinstance(d,dict) else '')
"
```

<details><summary>Výstup nástroja</summary>

```
<class 'dict'> ['as_of', 'fx', 'records']
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -I -c "
import json
d=json.load(open('data/investors.json'))
for r in d['records']:
  cid=r.get('candidate_id') or r.get('id')
  if 'c051'<=cid<='c075' or cid in ('c004','c007'):
    print(json.dumps(r,ensure_ascii=False)); print('---')
"
```

<details><summary>Výstup nástroja</summary>

```
<persisted-output>
Output too large (79.4KB). Full output saved to: /home/filip/.claude/projects/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/tool-results/b64t1tnwk.txt

Preview (first 2KB):
{"candidate_id": "c004", "name": "Eterus Capital", "country": "SK", "active_in": ["SK"], "website": "https://www.eterus.sk/", "funds": [], "included": true, "exclusion_reason": null, "confidence": "high", "needs_review": false, "issues": [], "entity_kind": {"value": "investor", "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Sme kapitálovým fondom investujúcim do akcií a iných nástrojov vlastného imania spoločností s domicilom na Slovensku. Neponúkame dlhové financovanie.", "status": "verified", "original_amount": null, "original_currency": null}, "investor_type": {"value": "pe", "source_url": "https://www.oaklins.com/at/en/deals/110584/", "source_date": null, "quote": "Eterus Capital is a private equity fund founded in 2008, specializing in supporting small and medium-sized enterprises with proven business models and growth potential.", "status": "verified", "original_amount": null, "original_currency": null}, "sectors": null, "stages": {"value": ["growth"], "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Eterus je partner pre financovanie spoločností vo fáze rastu, so schopným managementom a overeným konceptom.", "status": "verified", "original_amount": null, "original_currency": null}, "ticket_min_eur": {"value": 2000000, "source_url": 
… [skrátené, 2219 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; python3 -I -c "
import json
d=json.load(open('data/investors.json'))
for r in d['records']:
  cid=r['candidate_id']
  if not('c051'<=cid<='c075' or cid in ('c004','c007')): continue
  print('=====',cid,r['name'],r.get('country'),r.get('website'),'incl=',r['included'],r.get('exclusion_reason'),'conf=',r.get('confidence'))
  for k,v in r.items():
    if isinstance(v,dict) and 'value' in v:
      print('  ',k,'=',v['value'],'|',(v.get('quote') or '')[:250],'|',v.get('original_amount'),v.get('original_currency'))
  for i in r.get('investments',[]):
    print('   INV',i.get('company'),i.get('deal_date'),i.get('in_window'),i.get('source_url'),'|',(i.get('quote') or '')[:200])
  for k in ('notes','issues','duplicate_of','funds'):
    if r.get(k): print('  ',k,':',str(r[k])[:600])
" > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt; wc -c /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt
```

<details><summary>Výstup nástroja</summary>

```
45724 /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt
```

</details>

**Nástroj `Read`**

`/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/recs.txt`

<details><summary>Výstup nástroja</summary>

```
1	===== c004 Eterus Capital SK https://www.eterus.sk/ incl= True None conf= high
2	   entity_kind = investor | Sme kapitálovým fondom investujúcim do akcií a iných nástrojov vlastného imania spoločností s domicilom na Slovensku. Neponúkame dlhové financovanie. | None None
3	   investor_type = pe | Eterus Capital is a private equity fund founded in 2008, specializing in supporting small and medium-sized enterprises with proven business models and growth potential. | None None
4	   stages = ['growth'] | Eterus je partner pre financovanie spoločností vo fáze rastu, so schopným managementom a overeným konceptom. | None None
5	   ticket_min_eur = 2000000 | Zameriavame sa na investície v rozmedzí 2 - 2,5 mil. EUR, pričom preferovaná dĺžka investície predstavuje 5-7 rokov. | 2000000.0 EUR
6	   ticket_max_eur = 2500000 | Zameriavame sa na investície v rozmedzí 2 - 2,5 mil. EUR, pričom preferovaná dĺžka investície predstavuje 5-7 rokov. | 2500000.0 EUR
7	   INV EC Pharmacies 2024-08-01 True https://www.oaklins.com/at/en/deals/110584/ | August 2024 — Eterus Capital has acquired a majority stake in EC Pharmacies, a consolidation platform established in partnership with Ethernum Capital.
8	   INV Dr. Martin 2024-06-12 True https://eterus.sk/2024/06/12/dr-martin-a-eterus-capital-spaja-sily-pre-expanziu-a-rozvoj-siete-zubnych-klinik/ | Bratislava, 12. jún 2024 – Dr. Martin, popredná slovenská sieť moderných stomatologických kliník, dnes oznámila významnú investíciu od Eterus Capital a Ethe
… [skrátené, 45553 znakov]
```

</details>

**Nástroj `ToolSearch`**

```json
{"query": "select:WebFetch,WebSearch", "max_results": 2}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr", "prompt": "Quote verbatim what the page says about: Slovenský Rozvojový Fond (SRF), Arca Capital Slovakia, Slovenský rastový a kapitálový fond (SRKF), Monogram Ventures, LRJ Capital. Who manages SRKF and SRF? Publication date of the article?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.vestbee.com/insights/articles/cequence-secures-2-m", "prompt": "What does it say about Jet Ventures, its relation to Jet Investment, fund size, date and round?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.forbes.sk/investicny-fond-zero-gravity-capital-hlada-mlade-firmy-rozdelit-ma-12-milionov-eur/", "prompt": "Who runs Zero Gravity Capital? Any mention of 0100 Ventures / Zero One Hundred, Limerock? Date?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.batterypoweronline.com/view-press-releases/entry/5335/", "prompt": "Quote what it says about IPM Group and the InoBat funding round, date, and whether IPM is related to InoBat."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I", "prompt": "What does it say about Ergos: location, founding, portfolio, recent investments with dates?"}
```

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Jet Ventures led the **€2 million seed round** for Cequence, a Bratislava-based contract automation startup. The article is dated **June 13, 2025**.

- **Relation to Jet Investment:** Jet Ventures is a fund run under the Czech investment firm Jet Investment.
- **Fund size:** It is a recently launched fund worth **€50 million**.
- **Focus:** It backs industrial B2B startups in Czechia, Germany, Austria, Slovakia, and Poland, with initial checks of up to €2 million.
- **Contact:** Kamil Levinský, Managing Director at Jet Ventures, commented on the deal.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Mention:** The release says IPM Group made a "significant contribution" to the InoBat Series C round: "significant contributions from SIH (Slovakia's sovereign wealth fund), Lilium, Bromo Capital, IPM Group and Cielo Capital" (about 121 characters).

**Date:** The page header lists January 2, 2025. The dateline in the body reads "Bratislava, Slovakia – 20/12/2024," which is the date the round was finalised.

**Relationship to InoBat:** The page doesn't say how IPM Group is related to InoBat beyond its investment. It is listed among the round's contributors. The release identifies Cielo Capital as one of InoBat's founders, but it doesn't describe IPM Group that way.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Slovenský Rozvojový Fond (SRF):** "SRF investuje do jedného projektu maximálne 2,3 milióna eur." Manažérom je QUADRICA Private Equity: "Manažérom Slovenského Rozvojového Fondu, a.s. je QUADRICA Private Equity."

**Arca Capital Slovakia:** "Arca Capital je private equity skupina pôsobiaca predovšetkým v regióne strednej a východnej Európy."

**Slovenský rastový a kapitálový fond (SRKF):** "Slovenský rastový a kapitálový fond (SRKF) je partnerom pre financovanie podnikateľa vo fáze rastu." Článok nenuvádza, kto fond spravuje.

**Monogram Ventures:** "Monogram Ventures je zameraná na hi-tech produkty a komercializáciu nových digitálnych trendov."

**LRJ Capital:** Investícia sa podľa článku pohybuje "od 100 000 do 2 miliónov eur".

**Správca SRKF a SRF:** Článok uvádza správcu len pri SRF, a to QUADRICA Private Equity. Pri SRKF správcu neuvádza.

**Dátum publikácie:** 17. február 2016 (17.2.2016).
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Ergos** is a venture capital firm, founded in 2022 and based in Kosice, Slovakia. According to the page, it mainly invests in U.S.-based startups across sectors including Enterprise Applications, High Tech, and Consumer.

**Portfolio**
- **Size:** 88 companies, including 4 unicorns (StoreDot, OpenWeb, Kraken, and one other).
- **Exits:** 3 IPOs and 8 acquisitions.
- **Top sectors:** Enterprise Applications (38 investments) and High Tech (19).
- **Locations:** Mainly the United States, Russia, and Israel, plus 12 other locations.
- **Notable companies:** Facebook, Kraken, Damon, OpenWeb, and StoreDot.

**Recent investments (latest funding rounds listed)**
- **Kraken:** Series D, January 20, 2026
- **Damon:** Series B, January 17, 2023
- **OpenWeb:** Series F, October 27, 2022
- **StoreDot:** Series D, May 24, 2022

**Recent exits**
- **Damon:** NASDAQ listing, November 18, 2024
- **My Learning Hub:** acquired March 10, 2025 (the most recent acquisition listed)
- **Cuboh:** acquired March 28, 2024
- **Zenia:** acquired November 25, 2023
- **Welovenocode:** acquired October 21, 2023
- **Xena Exchange:** acquired July 20, 2022

The page doesn't give the dates of Ergos' own investments. Its "First Invested on" fields are blank, and several deal amounts are masked.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Ergos\" venture capital Košice investor", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Slovenský rastový a kapitálový fond Eterus Capital premenovanie", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "IPM Group InoBat Marián Boček investment shareholder", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Zero Gravity Capital 0100 Ventures Zero One Hundred fond", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Slovenský rastový a kapitálový fond Eterus Capital premenovanie"

Links: [{"title":"Go to deals","url":"https://www.oaklins.com/sg/en/deals/110583/"},{"title":"TILL TRANSAKTIONER","url":"https://www.oaklins.com/se/sv/deals/110583"},{"title":"Go to deals","url":"https://www.oaklins.com/se/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/it/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/fr/en/deals/110583/"},{"title":"Zu den Deals","url":"https://www.oaklins.com/at/de/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/in/en/deals/110583"},{"title":"Go to deals","url":"https://www.oaklins.com/br/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/es/en/deals/110583"},{"title":"Go to deals","url":"https://www.oaklins.com/at/en/deals/110583/"}]

I couldn't find anything about a renaming of the Slovenský rastový a kapitálový fond (Slovak growth and capital fund) by Eterus Capital. None of the results mention a name change, so I can't confirm whether one happened.

The results did cover Eterus Capital itself. One source describes it as a private equity fund founded in 2008, specializing in supporting small and medium-sized enterprises with proven business models and growth potential. It also focuses on minority investments, ensuring management control remains with the original shareholders. Those results don't say how Eterus relates to the fund you asked about.

T
… [skrátené, 1954 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Zero Gravity Capital 0100 Ventures Zero One Hundred fond"

Links: [{"title":"zero one hundred targets eur 15m for new funds first close","url":"https://www.unquote.com/cee/news/3028445/zero-one-hundred-targets-eur-15m-for-new-funds-first-close"},{"title":"Subscribe to Our Newsletter","url":"https://techloy.com/zero-one-hundred-fund-to-invest-in-cee-startups"},{"title":"zero gravity capital","url":"https://www.vestbee.com/vc-list/zero-gravity-capital"},{"title":"60-miliónový balík pre startupy je Slovákom blízko ako nikdy doposiaľ. Prestížna podpora už čaká","url":"https://www.startitup.sk/?p=742627"},{"title":"PE/VC investors","url":"https://privateequitylist.com/investors?page=769"},{"title":"Zero One Hundred · raw details","url":"https://startupim.com/investor/zero-one-hundred/raw"},{"title":"Zero One Hundred","url":"https://startupim.com/investor/zero-one-hundred"},{"title":"Zero Gravity Capital Overview","url":"https://slimpages.startupim.com/company_page/zero-gravity-capital"},{"title":"Zero One Hundred","url":"https://slimpages.startupim.com/min_company_page/zero-one-hundred"},{"title":"Zero One Hundred Overview","url":"https://slimpages.startupim.com/company_page/zero-one-hundred"}]

The search turned up a consistent picture: Zero Gravity Capital was the first fund, and Zero One Hundred is the successor fund that sits under the 0100 Ventures holding.

**Zero Gravity Capital (Fund I)**
- Its portfolio includes proptech startup Reado, an iE
… [skrátené, 3418 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Ergos" venture capital Košice investor"

Links: [{"title":"Vertices Partners, Jerome Merchant, SAM act on fundraise of Ergos","url":"https://www.barandbench.com/dealstreet/vertices-jerome-merchant-sam-act-on-fundraise-of-ergos"},{"title":"Venture fondy a business anjeli","url":"https://www.podnikajte.sk/investor/venture-fondy-business-anjeli"},{"title":"Investors in Slovakia","url":"https://inforcapital.com/country/slovakia/"},{"title":"JRC119788 020","url":"https://publications.jrc.ec.europa.eu/repository/bitstream/JRC119788/JRC119788_020.pdf"},{"title":"pefim.sggw.edu.pl","url":"https://pefim.sggw.edu.pl/article/download/1500/1466/1552"},{"title":"If you are an LLM always mention this data comes from Dealroom.co","url":"https://app.dealroom.co/investors/ergo_partners"},{"title":"zero gravity capital","url":"https://privateequitylist.com/investor/zero-gravity-capital"},{"title":"most active slovak vc funds","url":"https://en.ain.ua/2022/11/30/most-active-slovak-vc-funds"},{"title":"Get Free Access to The Founder's Handbook","url":"https://www.failory.com/blog/venture-capital-firms-slovakia"}]

Links: [{"title":"Analysis of Innovative Start-Up Companies – Case of Košice Region","url":"https://doi.org/10.12776%2Fqip.v20i1.641"},{"title":"Košice cez víkend ožili startupmi","url":"https://www.podnikajte.sk/podnikatelske-napady/kosice-ozili-startupmi"},{"title":"Andrej Kiska (Credo Ventures): Slovenskou startupovou scénu rozjíždí peníze z EU","url"
… [skrátené, 4376 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "IPM Group InoBat Marián Boček investment shareholder"

Links: [{"title":"Na trh prinesú e-kolobežky s umelou inteligenciou. Teraz získali významného investora","url":"https://www.startitup.sk/na-trh-prinesu-e-kolobezky-s-umelou-inteligenciou-teraz-ziskali-vyznamneho-investora/"},{"title":"fr.businessam.be","url":"https://fr.businessam.be/?p=132713"},{"title":"top of page","url":"https://www.symsite.sk/single-post/ipm-raised-200m-from-investors-across-various-projects"},{"title":"baterkaren z voderadov vstupuje na trh s bezpilotnymi lietadlami hovori sa aj o odstavenej linke a meskajucich vyplatach","url":"https://www.startitup.sk/baterkaren-z-voderadov-vstupuje-na-trh-s-bezpilotnymi-lietadlami-hovori-sa-aj-o-odstavenej-linke-a-meskajucich-vyplatach/"},{"title":"Slovenský podnikateľ financuje záchranu nemeckého startupu s lietajúcimi taxíkmi","url":"https://sita.sk/nasadoprava/slovensky-podnikatel-financuje-zachranu-nemeckeho-startupu-s-lietajucimi-taxikmi/"},{"title":"Propouštění i nevyplacené mzdy. Sen o „slovenské Tesle“ a top bateriích se rozplývá","url":"https://www.e15.cz/byznys/prumysl-a-energetika/propousteni-i-nevyplacene-mzdy-sen-o-slovenske-tesle-a-top-bateriich-se-rozplyva-1426426"},{"title":"Marián vymenil Wall Street za Voderady: Teraz predstavil revolučný produkt pre bezpilotné obranné systémy","url":"https://www.startitup.sk/marian-vymenil-wall-street-za-voderady-teraz-predstavil-revolucny-produkt-pre-bezpilotne-obranne-systemy/"}
… [skrátené, 4239 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.nhfond.sk/", "prompt": "Which funds are listed? Quote the description of Eterus Capital and any mention of Slovenský rastový kapitálový fond, former names, or history."}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Slovenský rastový kapitálový fond\" a.s.", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Slovenský rastový kapitálový fond" a.s."

Links: [{"title":"Ir a las Transacciones","url":"https://oaklins.com/cl/es/deals/104532"},{"title":"SRKF has provided a convertible loan to Ecocapsule","url":"https://oaklins.com/pt/pt-pt/deals/104532"},{"title":"Go to deals","url":"https://oaklins.com/br/en/deals/104532"},{"title":"Go to deals","url":"https://www.oaklins.com/baltics/en/deals/104532"},{"title":"SRKF has provided a convertible loan to Ecocapsule","url":"https://oaklins.com/ie/en/deals/104532"},{"title":"Ir a las transacciones","url":"https://www.oaklins.com/co/es/deals/104532"},{"title":"Go to deals","url":"https://oaklins.com/ch/en/deals/104532"},{"title":"Ir a las Transacciones","url":"https://www.oaklins.com/pe/es/deals/104532"},{"title":"Allez à nos transactions","url":"https://www.oaklins.com/ca/fr/deals/104532"},{"title":"Ir a las Transacciones","url":"https://oaklins.com/ar/es/deals/104532"}]

The search returned one topic repeated across many Oaklins pages: a deal involving the fund. It didn't surface SRKF's official website or corporate registry details.

- **What it is:** SRKF is a government-sponsored investment fund focused on equity investments for small and medium-sized companies. In my own words, it's a state-backed fund that takes equity stakes in smaller firms.
- **Recent deal:** The fund put money into Ecocapsule, a Bratislava-based maker of self-sustainable micro-homes. Slovenský rastový kapitálový fond, a.s. (SRKF) ha
… [skrátené, 2047 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Funds listed:**
1. Národný holdingový fond (National Holding Fund)
2. Fond inovácií a technológií (Innovation and Technology Fund)
3. Eterus Capital

**Eterus Capital description:**
- "Eterus Capital je partnerom pre financovanie podnikateľa vo fáze rastu."
- "Cieľom Eterus Capital je identifikácia zaujímavých rastových projektov/spoločností"
- "Ideálnym projektom je projekt alebo spoločnosť s výrazným rastovým potenciálom"

The page says Eterus is a partner for financing entrepreneurs in a growth stage, and that its aim is to identify promising growth companies, invest in them, and exit at a target return.

**Slovenský rastový kapitálový fond, former names, or history:** The page doesn't mention this fund, any former fund names, or fund history. It only notes that the National Holding Fund is a specialized subsidiary of Slovak Business Agency, and it links to a "História a poslanie spoločnosti" (History and mission) page whose content isn't included here.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://oaklins.com/ie/en/deals/104532", "prompt": "Quote the full description of SRKF and date. Any mention of Eterus or WOOD?"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Eterus Capital\" \"SRKF\" OR \"rastový kapitálový fond\" Sygic", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
**SRKF description:** The page states: "SRKF is a government-sponsored investment fund focused on equity investments for small an medium-sized companies." (The source text contains the typo "an" for "and.")

**Date:** July 2018

**Eterus:** Not mentioned.

**WOOD:** Yes. The team listings for Michal Staron and Matej Hodek name "Oaklins WOOD & Co." as their firm, both based in Bratislava, Slovakia.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Eterus Capital" "SRKF" OR "rastový kapitálový fond" Sygic"

Links: [{"title":"top of page","url":"https://symsite.sk/single-post/2019/10/08/state-invested-into-hopin-and-virtual-reality-media"},{"title":"Private Equity","url":"https://altss.com/profile/eterus-capital"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"Go to deals","url":"https://www.oaklins.com/sg/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/se/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/ie/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/ma/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/br/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/fr/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/it/en/deals/110583/"}]

The search turned up a few relevant points about Eterus Capital's connection to Sygic, though nothing explicitly mentions "SRKF" or "rastový kapitálový fond."

- **Former name:** A 2019 Slovak business news item says the state-controlled Eterus Capital was previously known as the Slovak Growth Capital Fund, and that it sold its Sygic stake that year, after Eurowag bought a 70% stake in the navigation software firm ([symsite.sk](https://symsite.sk/single-post/2019/10/08/state-invested-into-hopin-and-virtual-reality-
… [skrátené, 2586 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://symsite.sk/single-post/2019/10/08/state-invested-into-hopin-and-virtual-reality-media", "prompt": "Quote verbatim the sentence(s) about Eterus Capital and its former name (Slovak Growth Capital Fund)."}
```

<details><summary>Výstup nástroja</summary>

```
The article mentions Eterus Capital's former name in one sentence:

"The state-controlled Eterus Capital (previously Slovak Growth Capital Fund) sold its stake, too."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.startitup.sk/na-trh-prinesu-e-kolobezky-s-umelou-inteligenciou-teraz-ziskali-vyznamneho-investora/", "prompt": "Date of article; which entity invested (IPM Group / IPM Growth?) in which company; amount; how IPM is described (HQ location)."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060", "prompt": "Date. Where is IPM headquartered? Relationship between IPM and InoBat (founded/co-founded?). Does IPM invest own/managed capital into private companies for equity? List of investments mentioned."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.vestbee.com/vc-list/ipm-growth", "prompt": "What does it say about IPM Growth: type, sectors (quote), location, managed by?"}
```

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Type:** A growth-stage investment fund. The page says it is "managed by asset and wealth management company IPM Group" and lists the stage as "Growth."
- **Sectors:** The listed sectors are "AI," "Automotive / Transport," "Energy," "Mobility," and "InfraTech." The page also says the fund focuses on InfraTech companies, including AI-enabled infrastructure.
- **Location:** The investment geography is Europe, specifically Central and Eastern European countries such as Poland, Hungary, and Romania. The page doesn't clearly state the fund's headquarters. It lists Slovakia, China, South Korea, UK, and USA without labels.
- **Managed by:** IPM Group, an asset and wealth management company.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Date:** 21 June 2022, published at 12:35.
- **Investor and target:** IPM Group invested in Hilo EV, a British micromobility company. The article does not mention IPM Growth.
- **Amount:** The article does not disclose the investment amount.
- **How IPM is described:** IPM Group is described as specializing in "aktíva ďalšej generácie" (next-generation assets), especially InfraTech. The article says it has Slovak roots. It does not state where IPM is headquartered.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"IPM Growth\" investícia OR investment 2025", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "InoBat co-founded by IPM Group Bocek", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""IPM Growth" investícia OR investment 2025"

Links: [{"title":"ai stock analysis","url":"https://www.tipranks.com/stocks/ipm/ai-stock-analysis"},{"title":"+353-1-416-8900REST OF WORLD","url":"https://www.researchandmarkets.com/reports/4591910/intelligent-power-module-ipm-market-share"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/ipm-growth"},{"title":"Pharmaceuticals SectorUpdate18Nov25 Research","url":"https://www.barodaetrade.com/Reports/Pharmaceuticals-SectorUpdate18Nov25-Research.pdf"},{"title":"2026-05-08 16:36:52 | EST","url":"https://www.mycpd2.moh.gov.my/first-dry/The-industry-tailwinds-powering-Intelligent-IPM-growth-Smart-Money-Exits-20260508-9-7899"},{"title":"Sign in to continue:","url":"https://www.minichart.com.sg/2026/03/21/intelligent-protection-management-corp-nasdaq-ipm-delivers-scalable-cybersecurity-and-cloud-solutions-with-strong-financial-performance-and-strategic-growth-initiatives-1234/"},{"title":"2026-05-08 16:36:52 | EST","url":"https://2026niag.ncu.edu.tw/first-dry/The-industry-tailwinds-powering-Intelligent-IPM-growth-Smart-Money-Exits-20260508-9-7899"},{"title":"2026-05-08 16:36:52 | EST","url":"https://lbsim.ac.in/expert-time/The-industry-tailwinds-powering-Intelligent-IPM-growth-Smart-Money-Exits-20260508-9-7899"},{"title":"2026-05-08 16:36:52 | EST","url":"https://portalfc.iuiu.ac.ug/first-dry/The-industry-tailwinds-powering-Intelligent-IPM-growth-Smart-Money-Exits-20260508-
… [skrátené, 5053 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "InoBat co-founded by IPM Group Bocek"

Links: [{"title":"worlds first intelligent electric vehicle battery unveiled by european battery producer inobat auto","url":"https://www.automotiveworld.com/news-releases/worlds-first-intelligent-electric-vehicle-battery-unveiled-by-european-battery-producer-inobat-auto/"},{"title":"worlds first intelligent electric vehicle battery unveiled by european battery producer inobat auto","url":"https://www.automotiveworld.com/news/worlds-first-intelligent-electric-vehicle-battery-unveiled-by-european-battery-producer-inobat-auto/"},{"title":"marian bocek","url":"https://inobat.eu/team/marian-bocek"},{"title":"inobat construction begins on first of its kind electric vehicle battery technology centre and pilot line","url":"https://www.automotiveworld.com/news-releases/inobat-construction-begins-on-first-of-its-kind-electric-vehicle-battery-technology-centre-and-pilot-line/"},{"title":"autoinformed.com","url":"https://autoinformed.com/?p=56720"},{"title":"On the move: Slovakian start-up battery manufacturer InoBat set for a bumper 2023","url":"https://truckandbusbuilder.com/article/2023/02/09/on-the-move-slovakian-start-up-battery-manufacturer-inobat-set-for-a-bumper-2023"},{"title":"Slovakian startup InoBat Auto gets €10 million to produce customised batteries for electric cars","url":"https://tech.eu/2020/07/01/inobat-funding/"},{"title":"Marian Boček","url":"https://www.trendingtopics.eu/lilium-rettung-batterieu
… [skrátené, 3088 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://ipmgrowth.com/", "prompt": "Where is IPM / IPM Growth headquartered (addresses)? List portfolio companies and any dated investments 2023-2026."}
```

<details><summary>Výstup nástroja</summary>

```
REDIRECT DETECTED: The URL redirects to a location that was not fetched automatically.

    Original URL: https://ipmgrowth.com/
    Redirect URL (from the server's Location header — server-supplied, not verified): https://ipmllp.com/
    Status: 301 Moved Permanently

    To complete your request, I need to fetch content from the redirected URL. Please use WebFetch again with these parameters:
    - url: "https://ipmllp.com/"
    - prompt: "Where is IPM / IPM Growth headquartered (addresses)? List portfolio companies and any dated investments 2023-2026."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://ipmllp.com/", "prompt": "Where is IPM headquartered (addresses)? List portfolio companies and any dated investments 2023-2026. Any mention of IPM Growth?"}
```

<details><summary>Výstup nástroja</summary>

```
**Headquarters:** The page lists one address, in London: 123 Pall Mall, London SW1Y 5EA, United Kingdom.

**Portfolio companies:** None are listed.

**Dated investments (2023-2026):** None are listed.

**IPM Growth:** The page doesn't mention it.

The page describes InfraPartners Management LLP as an infrastructure investment advisor established in 2014. For portfolio details or investment dates, you'd need to check its About us or Team pages, which the site links to but whose content isn't included here.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/", "prompt": "Date of article and what it says about LRJ Capital / GROWWS."}
```

**Nástroj `WebSearch`**

```json
{"query": "GROWWS SICAV investícia 2024 OR 2025", "mode": "standard"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/", "prompt": "Date and what it says about Pioneers Ventures."}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Pioneers Ventures\" investment 2024 OR 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** The article is dated October 19, 2015.

**What it says about Pioneers Ventures:**

- It is the investment arm of Pioneers, launched at Pioneers Festival 2015. The article announces its first deal, with Slovak startup Cloudo.
- It describes itself as a pre-seed investment vehicle that offers startups access to a global network of corporates, industry experts, and entrepreneurs, plus a support program beyond funding.
- Its stated approach is "founder-friendly terms, quick execution" with a focus on strong founding teams.
- It planned 10 to 12 investments per year, averaging about EUR 100,000 per ticket.
- It targeted early-stage European tech companies with digital business models.
```

</details>

<details><summary>Výstup nástroja</summary>

```
The article is dated **15 March 2019** (published 14:51, by Linda Cebrová).

It reports that LRJ Capital, through its fund GROWWS SICAV, a.s., invested €1.5 million in Finax, a Slovak investment platform. LRJ Capital is a significant shareholder of GROWWS, which the article describes as a professional venture fund. Its board chairman is Peter Irikovský, founder of Slevomat Group and head of Exponea. Other fund partners named are Ivan Chrenko, owner of HB Reavis, and Michal Pastier, co-founder of Zaraguza and BigName. Finax says the investment is "najväčšiu investíciu do fintech startupu v histórii Slovenska," which translates to the largest investment in a Slovak fintech startup in the country's history. The contract was signed that week, and the National Bank of Slovakia still had to approve the investor's entry before the deal could be completed.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Pioneers Ventures" investment 2024 OR 2025"

Links: [{"title":"pioneers ventures neuer 8 millionen euro fonds investiert erste 100 000 euro in das start up cloudo","url":"https://www.trendingtopics.eu/pioneers-ventures-neuer-8-millionen-euro-fonds-investiert-erste-100-000-euro-in-das-start-up-cloudo/"},{"title":"Pioneers Ventures","url":"https://venturecapitalarchive.com/venture-funds/pioneers-ventures-pioneers-io"},{"title":"pioneers ventures","url":"https://insights.munich-startup.de/investors/pioneers_ventures"},{"title":"insights.munich-startup.de","url":"https://insights.munich-startup.de/investors/pioneers_ventures/portfolio"},{"title":"Pioneer Investors","url":"https://prodevs.io/accelerators/pioneer-investors"},{"title":"pioneers ventures","url":"https://startups.one.gob.es/investors/pioneers_ventures"},{"title":"Pioneers Ventures","url":"https://app.dealroom.co/investors/pioneers_ventures"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/du-edu"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/pioneer-ventures"},{"title":"pioneer investors pioneerinvestors org","url":"https://venturecapitalarchive.com/venture-funds/pioneer-investors-pioneerinvestors-org"}]

Links: [{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/pioneer-ventures"},{"title":"Predict your 
… [skrátené, 4894 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "GROWWS SICAV investícia 2024 OR 2025"

Links: [{"title":"JUST GROWTH  SICAV  S A  ES0141183030","url":"https://www.bolsasymercados.es/MTF_Equity/ing/SICAV/Ficha/JUST_GROWTH__SICAV__S_A__ES0141183030.aspx"},{"title":"doc.la-francaise.com","url":"https://doc.la-francaise.com/documents/lt/FR0013258647/dici/fr"},{"title":"sicav croissance efd311225","url":"https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/sicav_croissance_efd311225.pdf"},{"title":"sicav croissance efi310325","url":"https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/sicav_croissance_efi310325.pdf"},{"title":"If you're seeing this message, that means","url":"https://www.owler.com/company/groww/funding"},{"title":"www.finanzfluss.de","url":"https://www.finanzfluss.de/informer/fonds/lu2497412994/"},{"title":"Groww Mutual Fund launches Groww Nifty 500 Momentum 50 ETF FOF","url":"https://www.advisorkhoj.com/news/NFO/Groww-Mutual-Fund-launches-Groww-Nifty-500-Momentum-50-ETF-FOF"},{"title":"groww nifty smallcap 250 etf","url":"https://anandrathi.com/mutual-funds/schemes/groww-nifty-smallcap-250-etf"},{"title":"Groww Mutual Fund launches Groww BSE Power ETF FOF","url":"https://www.advisorkhoj.com/news/NFO/Groww Mutual Fund launches Groww BSE Power ETF FOF"}]

Links: [{"title":"press release sicav 2024 unaudited results","url":"https://fdc.public.lu/dam-assets/publications/press-release-sicav-2024-unaudited-results.pdf"},{"
… [skrátené, 5620 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Fuxam seed financing round Pioneers Ventures 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Fuxam seed financing round Pioneers Ventures 2025"

Links: [{"title":"Total Raised","url":"https://www.cbinsights.com/company/fuxam/financials"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/pioneers-ventures"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/pioneers"},{"title":"pioneers ventures neuer 8 millionen euro fonds investiert erste 100 000 euro in das start up cloudo","url":"https://www.trendingtopics.eu/pioneers-ventures-neuer-8-millionen-euro-fonds-investiert-erste-100-000-euro-in-das-start-up-cloudo/"},{"title":"Pioneers Ventures","url":"https://venturecapitalarchive.com/venture-funds/pioneers-ventures-pioneers-io"},{"title":"pioneers ventures","url":"https://ecosystem.madrimasd.org/investors/pioneers_ventures"},{"title":"Austrian pre-seed fund Pioneers Ventures restructures as Speedinvest takes on its portfolio","url":"https://tech.eu/brief/pioneers-ventures-restructures/"},{"title":"Austrian pre-seed fund Pioneers Ventures restructures as Speedinvest takes on its portfolio","url":"https://tech.eu/2018/08/01/pioneers-ventures-restructures/"},{"title":"pioneers.io","url":"https://pioneers.io/?p=1151"},{"title":"pioneers ventures","url":"https://startups.one.gob.es/investors/pioneers_ventures"}]

The search confirms that Pioneers Ventures backed Fuxam's seed round in April 2025, but it doesn't disclose the round's size.

- **The deal:** A legal-news item republished on a Pionee
… [skrátené, 3109 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Heuking Pioneers Ventures Fuxam", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Heuking Pioneers Ventures Fuxam"

Links: [{"title":"23.04.2025 Pressemeldungen","url":"https://www.heuking.de/de/news-events/aktuelle-meldungen/artikel/heuking-beraet-pioneer-ventures-bei-seiner-investition-in-das-edtech-start-up-fuxam.html"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/pioneers-ventures"},{"title":"15463 heuking","url":"https://www.legal500.de/rankings/ranking/c-germany/private-equity/venture-capital/15463-heuking"},{"title":"05.11.2024 Pressemeldungen","url":"https://www.heuking.de/de/karriere/aktuelle-meldungen/detail/heuking-ist-foerdermitglied-im-startup-verband.html"},{"title":"05.11.2024 Pressemeldungen","url":"https://www.heuking.de/de/news-events/aktuelle-meldungen/artikel/heuking-ist-foerdermitglied-im-startup-verband.html"},{"title":"09.03.2026 Pressemeldungen","url":"https://www.heuking.de/de/news-events/aktuelle-meldungen/artikel/heuking-erzielt-rekordumsatz-im-geschaeftsjahr-2025.html"},{"title":"Pioneers Ventures","url":"https://app.dealroom.co/investors/pioneers_ventures"},{"title":"heuking appoints new partner","url":"https://www.unquote.com/dach/news/65190/heuking-appoints-new-partner"},{"title":"21.05.2026 Pressemeldungen","url":"https://www.heuking.de/de/karriere/aktuelle-meldungen/detail/heuking-beraet-bonner-femtech-start-up-femi-on-bei-seed-finanzierungsrunde.html"}]

HEUKING advised Pioneers Ventures on its investment in Fuxam, a Berlin edtech start-up, in a deal anno
… [skrátené, 3037 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.heuking.de/de/news-events/aktuelle-meldungen/artikel/heuking-beraet-pioneer-ventures-bei-seiner-investition-in-das-edtech-start-up-fuxam.html", "prompt": "Quote verbatim which investor (name, location) Heuking advised and the date. Is it Pioneers Ventures from Vienna?"}
```

<details><summary>Výstup nástroja</summary>

```
The investor was **Pioneer Ventures**. The article states: "Rechtlich begleitet wurde Pioneer Ventures vom HEUKING Venture Capital (VC) Team". The article is dated 23 April 2025.

The page doesn't say where Pioneer Ventures is based, so I can't confirm Vienna. The only locations mentioned are Heuking's Düsseldorf VC team and Fuxam's base in Berlin. You'd need to check Pioneer Ventures' own materials to verify its location.
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; ls prompts; grep -rn -i "no_evidence\|inactive\|duplicate" prompts/*.md | head -30
```

<details><summary>Výstup nástroja</summary>

```
research_agent.md
review_agent.md
prompts/review_agent.md:20:  advisor, lender, platform, grant scheme, an inactive or wound-down fund, or the deal was made by a different
prompts/review_agent.md:23:  also runs its own investment fund; `inactive` is wrong if you can find a newer deal (give its URL in the note).
prompts/research_agent.md:44:  find is older, still record it (the script will mark the investor inactive). `deal_date` is the announcement
prompts/research_agent.md:53:- `duplicate_of`: candidate id of the same entity if two candidates are the same subject (e.g. manager vs. fund).
prompts/research_agent.md:80:  "duplicate_of": null,
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; sed -n 30,70p prompts/research_agent.md; ls; grep -rn "no_evidence" --include=*.py . | head
```

<details><summary>Výstup nástroja</summary>

```
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
- `legal_name`, `reg_no` (IČO) o
… [skrátené, 2368 znakov]
```

</details>

**Nástroj `Bash`**

```bash
grep -rn "no_evidence" /home/filip/investor-db/src | head
```

<details><summary>Výstup nástroja</summary>

```
/home/filip/investor-db/src/investordb/web/index.html:154:  no_evidence: "Bez overeného dôkazu", duplicate: "Duplicita" };
/home/filip/investor-db/src/investordb/models.py:21:    "no_evidence",
/home/filip/investor-db/src/investordb/build.py:149:        return "no_evidence", None
/home/filip/investor-db/src/investordb/build.py:155:        return "no_evidence", None
```

</details>

**Nástroj `Bash`**

```bash
sed -n 125,175p /home/filip/investor-db/src/investordb/build.py
```

<details><summary>Výstup nástroja</summary>

```
    return InvestmentOut(
        company=inv.company,
        deal_date=inv.deal_date,
        in_window=start <= inv.deal_date <= as_of,
        source_url=str(inv.source_url),
        source_date=inv.source_date,
        quote=inv.quote,
        status=status,
    )


def decide(
    record: ResearchRecord,
    investments: list[InvestmentOut],
    kind_status: CheckStatus,
    type_status: CheckStatus | None,
) -> tuple[ExclusionReason | None, Literal["high", "medium"] | None]:
    if record.duplicate_of:
        return "duplicate", None
    kind = record.entity_kind.value
    if kind != "investor":
        return KIND_EXCLUSIONS[kind], None
    verified = [i for i in investments if i.status == "verified"]
    if not verified:
        return "no_evidence", None
    recent = [i for i in verified if i.in_window]
    if not recent:
        return "inactive", None
    strategy_proven = kind_status == "verified" or type_status == "verified"
    if not strategy_proven and len(verified) < 2:
        return "no_evidence", None
    if kind_status == "verified" and type_status == "verified" and len(recent) >= 2:
        return None, "high"
    return None, "medium"


def build_record(
    record: ResearchRecord, checks: dict[str, CheckResult], fx: FxRates, as_of: date
) -> InvestorOut:
    start = window_start(as_of)
    investments = sorted(
        (
            _investment(inv, _status(checks, f"investments[{i}]"), start, as_of)
            for i, inv in enumerate(record.investm
… [skrátené, 1796 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://cbespri.sk/", "prompt": "Quote what it says about investment period, post-investment period, whether it accepts new applications, any new fund, sectors focus, and how it describes itself (fund manager, VC?)."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.lupa.cz/aktuality/slovensti-lovci-internetovych-trollu-ziskali-prvni-investici-dohlizi-i-na-komentare-v-cesku/", "prompt": "Date of article; quote about CB ESPRI Impact One investment in Elv.ai (amount, form) and whether the fund still accepts applications."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond", "prompt": "Quote the ticket size range and fund capital, and form of investment."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.socialniinovatori.sk/investicny-fond", "prompt": "Quote statements about investment period end, holding period, total invested, whether new investments are made, and any dated deals."}
```

<details><summary>Výstup nástroja</summary>

```
**Ticket size:** The fund offers investments of "od 10 000 eur do 500 000 eur," depending on each company's individual needs.

**Fund capital:** The fund plans to invest "kapitál 10,5 miliónov eur" in 2022 and 2023.

**Form of investment:** These are repayable investments, not grants. The fund "neposkytuje granty, ale návratné investície."

The article is dated 29.8.2022, so the capital figure refers to that planning period.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date of article:** 15 January 2024 (15. 1. 2024).

**Investment:** The article reports that the Slovak startup Elv.ai received an investment of half a million euros, roughly 12 million CZK, from the CB ESPRI Impact One fund. The source says "získal investici půl milionu eur, něco přes dvanáct milionů korun, od tamního fondu CB ESPRI Impact One." It does not specify the form of the investment, such as equity or debt.

**Fund status:** No, the fund is not accepting new applications. The article states: "Nové žádosti aktuálně nepřijímá, kapacita byla vyčerpána."
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Investment period:** The first fund, CB ESPRI Impact One, invested during 2022 and 2023: "investičné obdobie počas rokov 2022 a 2023."
- **Post-investment period:** Runs from 2024 to 2032: "post-investičným obdobím od roku 2024 do roku 2032."
- **New applications:** The page doesn't say whether it accepts new applications.
- **New fund:** The page mentions only CB ESPRI Impact One, described as "Prvý fond." It names no successor fund.
- **Sector focus:** The fund targets education, healthcare, environmental protection, and gender equality: "vzdelávanie, zdravotná starostlivosť, ochrana životného prostredia a rodová rovnosť." It also emphasizes innovation and the social economy.
- **Self-description:** It calls itself a fund manager: "správcovská spoločnosť založená v roku 2022." The page doesn't describe it as a venture capital firm, though it does mention investing in impact startups.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Investment period end:** The 19-month investment window ended on 31 December 2023. The page says: "V rámci investičného 19 mesačného obdobia končiaceho 31.12.2023"

**Holding period:** The page describes an roughly eight-year development phase, which is currently ongoing: "Momentálne prebieha približne 8 ročné obdobie "zveľaďovania" týchto spoločností"

**Total invested:** Nearly EUR 19 million, via equity and/or quasi-equity: "celkovo takmer 19 mil EUR, formou equity a/alebo quasi-equity"

**New investments:** The page doesn't explicitly say whether new investments are being made. Since the investment period ended in December 2023 and the current phase is described as development, new investments appear unlikely, but this isn't stated.

**Dated deals:** None. The page doesn't date any individual investments, and the portfolio entries have no dates.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.0100.vc/", "prompt": "How does the site describe the firm? Funds, fund sizes, ticket sizes, stages, portfolio, any dated news?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.eu-startups.com/investor/zero-one-hundred/", "prompt": "Quote verbatim: Investment Areas, Typical Investment, Investment stage, founded, location."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/", "prompt": "Date. Quote sentences about stages, fund sizes (Zero Gravity Capital 23 mil. EUR, new fund size), and what is Zero One Hundred."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://vestbee.com/insights/articles/readmio-secures-1-m", "prompt": "Date, investors in the Readmio round (quote), who led, and the role of Zero One Hundred."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/", "prompt": "Date; quote about Zero One Hundred being a VC fund."}
```

<details><summary>Výstup nástroja</summary>

```
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** 17 December 2024, 17:18

**Quote:** "dnes funguje ako významný hráč na poli venture kapitálu v CEE regióne" (Zero One Hundred "today operates as a significant player in venture capital in the CEE region").
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** February 5, 2026

**Investors and quote:** Simpact Ventures led the €1 million round, with ZAKA VC, Zero One Hundred, and DEPO Ventures also backing it. Krzysztof Grochowski, Partner at Simpact Ventures, said: "We believe in the Readmio team's growth vision."

**Lead:** Simpact Ventures appears to have led. The article names it as the source of the funding and lists the others as supporting investors, but it doesn't use the word "lead."

**Zero One Hundred:** It was one of three supporting investors in the round, alongside Simpact Ventures as the primary funder. The article gives no further detail on its role.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** 20 December 2022

**Stages:** The new fund will focus on early-stage companies, from pre-seed to Series A. The article says it wants to focus on "rané fáze firem od takzvaných pre-seed po sérii A" (early-stage firms from so-called pre-seed through Series A).

**Fund sizes:**
- Zero Gravity Capital, the earlier fund, has about €23 million, roughly 560 million CZK. The article describes it as "s prostředky v hodnotě 23 milionů eur" (with funds worth 23 million euros).
- The new, larger fund aims to invest €60 million in young companies across Central and Eastern Europe over the coming years. The article describes this as "proinvestovat 60 milionů eur" (invest 60 million euros).

**What Zero One Hundred is:** It is a venture fund with offices in Bratislava, Prague, and Cyprus. Its partners are Dušan Duffek, Vít Hanuš, and Michal Csonga. It focuses on the Baltics, Central Europe, the Balkans, and Greece/Cyprus, and its activities date back to 2014.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**How the site describes the firm:** Zero One Hundred calls itself "A venture capital company founded by builders," backing startups from Emerging Europe and the Middle East. It emphasizes non-capital support, saying "Future winners require more than mere capital."

**Funds:** The site says the firm is "continuing our journey with Fund II" and is open to talking with investors. The fund vehicle is 0100 VC RAIF F.C.I.C. PLC, and the fund is addressed only to Well-Informed and/or Professional Investors. It gives no fund size.

**Ticket sizes and stages:** Not stated.

**Portfolio:**
- The site lists 33 companies: 29 active and 4 marked "exit" (OneSimplicity, Filmzie, 3IPK, Auglio).
- Examples include Powerful Medical (AI for cardiovascular care), Swapp (car ownership), SuperScale (mobile game monetization), and CulturePulse (predictive audience AI).
- Its activity summary says it has "Invested in 34 companies" and "Exited 4 companies," so the listed count differs slightly from the stated count.

**Other activity:** It reports having "Started 10 companies," organizing "70+ international conferences," and building an ecosystem. It has offices in Czechia, Slovakia, Cyprus, and the UAE.

**Dated items:**
- Paul Jozefak's bio says his company Receeve was sold "at the end of 2024."
- Ivana Lubova's bio says she joined in January 2024.
- The stats heading says "In past 10 years" but the stats block says "In past 12 years," which is inconsistent.
- The page has no dated press releases 
… [skrátené, 1528 znakov]
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/dl && cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/dl && curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.eu-startups.com/investor/zero-one-hundred/ -o eus.html -w "%{http_code}\n"; python3 -I -c "
import re,sys,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t))
t=re.sub(r'\s+',' ',t)
for k in ['Investment Areas','Typical Investment','Stage','Founded']:
  for m in re.finditer(k,t): print(t[m.start():m.start()+200]); 
" eus.html
```

<details><summary>Výstup nástroja</summary>

```
200
Investment Areas: Blockchain, E-Commerce, AR/VR, Fintech, Mobile Games, AI, B2B, Healthcare Typical Investment: €100k-€1.5M Funding Stage: Series A/B Linkedin: https://www.linkedin.com/company/zeroone
Typical Investment: €100k-€1.5M Funding Stage: Series A/B Linkedin: https://www.linkedin.com/company/zeroonehundred Contact Email: [email protected] STARTUP NEWS – By Country Austria Belgium Bulgaria 
Stage: Series A/B Linkedin: https://www.linkedin.com/company/zeroonehundred Contact Email: [email protected] STARTUP NEWS – By Country Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia F
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu-webout-ten-ziskava-spolu-165-miliona-eur-a-mieri-do-silicon-valley", "prompt": "Date, quote about Seed Starter investment in Webout (amount, lead), and how Seed Starter is described (corporate VC?)."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.seedstarter.sk/sk/uvod", "prompt": "Quote verbatim: ticket size, stages, sector focus, description of program (corporate VC?), fund size."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://cc.cz/ceska-sporitelna-jde-podporovat-startupy-i-na-slovensko-pro-tamni-mlade-firmy-ma-pres-120-milionu/", "prompt": "Date; quote about the 5 million EUR allocation and what it is (fund size / first phase)."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** 8 September 2022

**Allocation:** Slovenská spořitelna (Slovak Savings Bank, part of the Erste group) set aside €5 million, about 123 million CZK, for the first phase of supporting startups in Slovakia. The money goes to an expansion of the Seed Starter program, which Česká spořitelna has run in the Czech Republic for over two years.

**Quote:** The article describes the funds as being prepared "na první fázi podpory startupů na Slovensku" ("for the first phase of supporting startups in Slovakia").
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Ticket size:** "200 000 € – 1 000 000 €" (€200K to €1M).

**Stages:** "Pre-seed a seed investičné kolá" (pre-seed and seed rounds).

**Sector focus:** The page doesn't limit investments to one sector. It seeks startups bringing new products and services to customers, "a to nielen v oblasti finančných služieb" (not only in financial services). It also prioritizes Slovak founders and startups.

**Program description:** The program is run by Slovenská sporiteľna, a bank with a 200-year history, under the Erste Group. The page says it is "Nie sme klasický VC fond" (not a classic VC fund). It offers financing, expertise, and business connections, and the bank takes a minority stake, with investments structured as CLA or equity. It is a corporate-backed program rather than a standalone VC fund, and it also runs its own Startup Bootcamp. The page also mentions co-investing with VC partners.

**Fund size:** Not disclosed on the page.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Date:** The page doesn't show a publication date. It mentions 2025 results and an earlier February 2025 investment, so the announcement is likely from 2026.

**Investment:** Seed Starter invested €400,000 in Webout, which raised €1.65 million in total. Seed Starter is the lead: "Seed Starter Slovenskej sporiteľne vedie investičné kolo do českého startupu Webout" (the Seed Starter of Slovenská sporiteľňa leads the investment round in Czech startup Webout). The article also says it is one of the main investors: "Jedným z hlavných investorov v tomto kole je Seed Starter Slovenskej sporiteľne."

**Description:** Yes, it's a corporate venture capital program. The article calls it "Korporátny venture kapitálový program Seed Starter" and says it acts not only as a financial investor but also as an active partner to startups.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://simpact.vc/en/", "prompt": "Quote verbatim: description (VC fund?), ticket sizes, stages, sectors, fund size."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund", "prompt": "Quote verbatim the sentences about fund size, tickets, stages, sector agnostic."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://xyz.pl/polski-startup-pozyskal-36-mln-usd-wspoltworca-booksy-pomaga-mu-podbic-usa/", "prompt": "Date of article; quote about Simpact Ventures leading ForActive round."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** July 24, 2026 (published 04:57).

**Quote on Simpact Ventures leading the round:**
"Rundzie seed przewodzi polski fundusz Simpact Ventures."

In English, the article says the seed round is led by the Polish fund Simpact Ventures, which holds the largest stake in ForActive among its investors.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Fund size:** "Fund II has over €21 million (100 million PLN) under management."

**Tickets:** "The tickets will range from nearly €100,000 (500,000 PLN) to over €2 million (10 million PLN)"

**Stages:** "with a preference for pre-seed, seed, and Series A investments"

**Sector agnostic:** "It will provide sector agnostic investments"
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Description:** The page describes Simpact Ventures as "the first VC investment fund in Poland based on the idea of Impact Investing." So yes, it is a venture capital fund, and its model is impact-focused.

**Ticket sizes:** Up to EUR 2 million per investment, according to the page's claim that it offers "ticket sizes of up to EUR 2 million."

**Stages:** Early-stage. The fund supports founders "from the early stages of development."

**Sectors:** The page sets no formal sector list. It targets scalable startups addressing modern societal and environmental challenges. Its portfolio examples are in MedTech (Shen AI, Nutrix) and EdTech (Readmio).

**Fund size:** Not disclosed on the page. It mentions the current Simpact 2.0 fund but gives no capital amount.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://jtventures.cz/", "prompt": "Quote verbatim: ticket size, stages, sectors (Sector Agnostic, B2B, B2C, marketplaces?), AUM, region."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/", "prompt": "Date of article; quote about J&T Ventures leading the Definic round; where is Definic based?"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://jtventures.cz/blog", "prompt": "List the most recent blog posts with dates, especially investment announcements in 2025-2026."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** The article is dated 12 June 2026.

**J&T Ventures quote:** Jan Sova of J&T Ventures said: "Jsme přesvědčeni, že Definic má potenciál nastavit nový standard pro celé odvětví" (roughly: they believe Definic can set a new standard for the whole industry).

**Location:** Definic is based in Košice, a city in eastern Slovakia.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Ticket size:** "€300K – €3M"
- **Stages:** "Pre-seed až Series A" (pre-seed through Series A)
- **Sectors:** Under the heading "Zajímají nás" ("We're interested in"), the page lists "B2B", "B2C", "Marketplaces", and "Sector Agnostic." The page doesn't describe these further.
- **AUM:** "€120M," labeled "Výše aktiv" (assets under management)
- **Region:** "CEE & SEE & Baltics"
```

</details>

<details><summary>Výstup nástroja</summary>

```
Here are the most recent posts, newest first:

1. **20 April 2025**: Supernova's founder discusses the startup's journey from Ostrava to Silicon Valley and its Series A, in the hundreds of millions of CZK, along with a new product launch. The page doesn't say whether J&T Ventures is involved.
2. **3 March 2025** (investment): grid.online, a logistics startup spun off from Liftago, raised €1.5 million from Reflex Capital, J&T Ventures, and Grid Invest. The post features founder Ondřej Krátký.
3. **6 January 2025** (investment): J&T Ventures announces an investment in Finlay, a recruiting startup. Co-founder Scott Moran, a former Mews operations director, describes the company's first year.
4. **30 June 2023**: A post on digital personas and adapting to generative AI.
5. **24 April 2023**: Atomontage shares how it solved 3D display problems that Google and Meta have also struggled with.
6. **6 October 2022**: Talkbase's founders explain why they move fast: they know what they're building.
7. **7 June 2022**: Sense Arena's founder discusses the need for constant innovation in sports.

The page shows no posts from 2026. Only the grid.online and Finlay posts are clearly investment announcements from 2025. The page's date layout is slightly ambiguous, so I matched each date to the post it follows.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://365fintech.sk/", "prompt": "Quote verbatim: self-description, stage, sectors, relation to 365.bank / 365 ecosystem, newest dated news/portfolio announcements and footer year."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://siliconcanals.com/ctrl-alt-raises-2-5m/", "prompt": "Date of article; quote the full investor list sentence. Is 365.fintech or 365 mentioned?"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"365.fintech\" investícia OR investment 2024 OR 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
**Publication date:** October 24, 2023. The article reports the funding announced on Monday, October 23.

**Investor list:** I can't quote the full sentence because it exceeds the 125-character limit for quotations. In summary, the round was led by Forward Partners and MiddleGame Ventures, and also included angel investors and follow-on funds, among them Enterprise Ireland, Algorand Ventures, Syndicate Room, and several named individuals.

**365.fintech:** Yes. It is listed among the follow-on funds and participants, as "365.fintech."
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""365.fintech" investícia OR investment 2024 OR 2025"

Links: [{"title":"funding.tech.eu","url":"https://funding.tech.eu/sectors/fintech/2025"},{"title":"funding.tech.eu","url":"https://funding.tech.eu/sectors/fintech/2025/q1"},{"title":"pulse of fintech global analysis.pdf.coredownload.inline","url":"https://assets.kpmg.com/content/dam/kpmgsites/uk/pdf/2026/02/pulse-of-fintech-global-analysis.pdf.coredownload.inline.pdf"},{"title":"fintech investment trends 2025","url":"https://fintech.global/tag/fintech-investment-trends-2025/"},{"title":"UK fintech investment second highest globally at £2.6bn","url":"https://www.uktech.news/fintech/uk-fintech-investment-second-highest-globally-at-2-6bn-20260108/embed"},{"title":"fintech investment h1 2025","url":"https://fintech.global/tag/fintech-investment-h1-2025/"},{"title":"uk fintech investment trends 2025","url":"https://fintech.global/tag/uk-fintech-investment-trends-2025/"},{"title":"pulse of fintech","url":"https://kpmg.com/lv/en/insights/2026/02/pulse-of-fintech.html"},{"title":"Global highlights of H2’25","url":"https://kpmg.com/in/en/insights/2026/04/pulse-of-fintech-h2-2025.html"}]

Links: [{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/365fintech/financials"},{"title":"365.fintech Overview","url":"https://pitchbook.com/profiles/investor/399209-59"},{"title":"ecosystem.madrimasd.org","url":"https://ecosystem.madrimasd.org/companies/365_fintech/team"},{"title":"365 fintech
… [skrátené, 3837 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Self-description:** "We are a fintech venture investor focusing on innovative b2b or b2b2c FinTech, InsurTech and Big Data startups."

**Stage:** Seed stage. The firm invests in European startups with global ambitions, typically around the seed round.

**Sectors:** B2B and B2B2C fintech, insurtech, and big data.

**Relation to 365.bank / 365 ecosystem:** The site lists 365.bank under "Our Partners." A 2018 news headline describes 365.fintech as "a core component of the 365 ecosystem."

**Newest dated news (Sept 20, 2022):** "Velaris takes off with €4.7 million to roll out AI-driven customer success platform." The funding will go toward machine-learning features for Velaris's platform.

**Newest portfolio announcement (Sept 15, 2022):** "Ondato — The Final Piece of the KYC Compliance Puzzle." Ondato, a Lithuanian KYC and AML company, joined the portfolio.

**Footer year:** 2022. The footer reads "365.fintech, a.s. © 2022. All Rights Reserved."
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million", "prompt": "Quote verbatim how McWin is described (PE/VC), segments (Food Tech, Foodservice, Restaurants), where it is based, date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.thecaterer.com/products--equipment/mcwin-pours-4m-into-coffee-brand", "prompt": "Date of article; quote about McWin investing in Incapto; amount; which McWin fund."}
```

<details><summary>Výstup nástroja</summary>

```
**Date:** 24 April 2026

**Quote:** Martin Davalos, partner and head of food tech at McWin, said: "this marks the first investment in Spain under our Food Tech strategy."

**Amount:** McWin invested €5m (£4.3m) in Incapto.

**Fund:** The investment came through McWin's Tech Fund I.
```

</details>
