# Subagent agent-aresearch-1-084188ff690aa5d8

Zdroj: transkript Claude Code `agent-aresearch-1-084188ff690aa5d8.jsonl`

## Používateľ · 2026-10-09 12:20:03 UTC

<teammate-message teammate_id="team-lead" summary="Research candidates c001-c012">
You are a research agent for the project in /home/filip/investor-db. Read /home/filip/investor-db/prompts/research_agent.md first and follow it exactly. Candidate list: /home/filip/investor-db/data/candidates.csv (columns: candidate_id, name, discovery_source, discovery_url).

Your assigned candidates: c001 to c012 (inclusive). Most are full members of SLOVCA (Slovak Venture Capital Association) — some are VC, some PE, some public funds, some HQ'd in CZ/PL.

Use WebSearch and WebFetch to find sources. Write one JSON file per candidate to /home/filip/investor-db/research/<candidate_id>.json. Do not touch any other files. Validate each file with:
cd /home/filip/investor-db && PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/<id>.json

Remember: quotes must be verbatim from the page text at source_url (a script will check it); missing data is better than wrong data. Finish with the one-line-per-candidate report described in the instructions, plus a short list of anything you were unsure about.
</teammate-message>

**Nástroj `Bash`**

```bash
cat /home/filip/investor-db/prompts/research_agent.md; head -14 /home/filip/investor-db/data/candidates.csv; ls /home/filip/investor-db/research/ 2>/dev/null
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
… [skrátené, 6589 znakov]
```

</details>

**Nástroj `ToolSearch`**

```json
{"query": "select:WebSearch,WebFetch", "max_results": 2}
```

**Nástroj `Bash`**

```bash
ls src/investordb && PYTHONPATH=src .venv/bin/python -m investordb.cli --help; grep -n "def \|quote" src/investordb/*.py | grep -i "quote\|fetch\|normal" | head -40
```

<details><summary>Výstup nástroja</summary>

```
__init__.py
__pycache__
cli.py
io.py
models.py
usage: investordb [-h] {check-schema} ...

positional arguments:
  {check-schema}
    check-schema  validate research JSON files

options:
  -h, --help      show this help message and exit
src/investordb/models.py:24:CheckStatus = Literal["verified", "quote_not_found", "http_error", "fetch_error", "unsupported_content"]
src/investordb/models.py:37:    quote: str = Field(min_length=8, max_length=600)
src/investordb/models.py:39:    @field_validator("quote")
src/investordb/models.py:41:    def quote_not_blank(cls, value: str) -> str:
src/investordb/models.py:43:            raise ValueError("quote must not be blank")
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/pages
cat > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/page.py <<'EOF'
import sys, re, html, hashlib, os, urllib.request
from html.parser import HTMLParser
PAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages")
class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.skip=0
    def handle_starttag(self, tag, a):
        if tag in ("script","style","noscript"): self.skip+=1
        if tag in ("p","div","br","li","h1","h2","h3","h4","tr","section","article"): self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script","style","noscript") and self.skip: self.skip-=1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
def norm(s): return re.sub(r"\s+"," ",s.replace("\xa0"," ")).strip()
def fetch(url):
    p=os.path.join(PAGES, hashlib.md5(url.encode()).hexdigest()+".txt")
    if os.path.exists(p): return open(p,encoding="utf-8").read()
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"sk,en;q=0.8"})
    raw=urllib.request.urlopen(req,timeout=30).read()
    try: s=raw.decode("utf-8")
    except UnicodeDecodeError: s=raw.decode("cp1250","r
… [skrátené, 2780 znakov]
```

<details><summary>Výstup nástroja</summary>

```
Vedení účetnictví zpracování mezd a daňové poradenství
Pay us a visit and let's discuss your accounting in confidence
Search
Home
Services
Book-keeping
Tax accounting
Income-tax return
Wages administration
Tax consultancy
Accounting consultancy
Publication of final accounts
Price list
Contacts
Keeping accounts,
elaboration of payroll, tax consultant services.
accounting company ARX
We gladly answer your enquieres about book-keeping or tax.
Make an appointment with us and assure yourself we are the book-keeping company suitable for you.
Small businessmen
Tax accountning (formerly single entry accountning) in the classification necessary to determine income tax base, elaboration of value added tax return including the prescribed (specified) records, wages administration. Declaration for income tax of natural persons, reporting for the Czech Social Security Administration and health insurance companies.
More information
Small and medium business
Running a business mainly in trade and services.
Book-keeping including yearly book closing, eventually preparation of data for audits, processing of wages administration and all tax returns necessary.
More information
Subsidiary company of outlandish companies
External book-keeping, wages administration and processing of all tax returns necessary, preparation of corporate statements (returns) according to IFRS/IAS for the home company including its presentation to a fixed monthly or yearly date, preparation of data for audit.
More infor
… [skrátené, 3000 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.arxequity.com/ https://www.cvi.sk/ https://www.ei.com.pl/en/ https://www.eterus.sk/ https://www.ventureinvest.sk/ https://www.gcap.eu/ https://www.jetinvestment.cz/ https://nhf.sk/ https://www.neulogy.vc/ https://www.sandbergcapital.sk/ https://www.vtff.sk/ https://www.visionventures.sk/; do echo "=== $u"; timeout 40 python3 -I page.py show "$u" 600 2>&1 | tail -c 700; done
```

<details><summary>Výstup nástroja</summary>

```
=== https://www.arxequity.com/
Home - ARX
Toggle navigation
About ARX
Working with ARX
Team
Investments
News
Contact
Toggle navigation
About ARX
Working with ARX
Team
Investments
News
Contact
en
cz
pl
Toggle navigation
About ARX
Working with ARX
Team
Investments
News
Contact
en
cz
pl
en
cz
pl
We are proud of our 20-year track record building great companies in successful partnerships with business owners and managers
About ARX
News
ARX Equity Partners Acquires Majority Stake in Medicofit, Slovenia’s Leading Private Physiotherapy Provider
2026/08/26
ARX Equity Partners Invests in Direct4me
2026/03/17
ARX Equity Partners Acqu
=== https://www.cvi.sk/
Váš certifikačný orgán
SK | EN | IT | RO
[email]
+421 948 037 277
O nás
Certifikáty
Partneri
Všeobecné informácie
Kontakt
O nás
Certifikáty
Partneri
Všeobecné informácie
Kontakt
Certifikačný orgánsystémovmanažérstva
Certifikačný orgánsystémov manažérstva
pracuje na základe akreditácie SNASpre certifikáciu systémov manažérstva...
pracuje na základe akreditácie SNASpre certifikáciu systémov manažérstva...
O nás
O nás
Váš prehliadač nepodporuje prehranie tohto videa.
Certifikujenasledovnéoblasti
Certifikujenasledoné oblasti
ISO 9001, ISO 13485, ISO 14001ISO 14064, ISO 17100, ISO 20000
ISO 9001
=== https://www.ei.com.pl/en/
Enterprise Investors
About us
Team
Investment team
Founders
Investments
News
Press releases
Annual summaries
Contact
LP login
Search
PL
EN
We finance the development of
dynamically growing companies
About us
We ar
… [skrátené, 8260 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "CVI Central European venture investor Slovakia CVI SLOVCA", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Fond inovácií a technológií a.s. FIT venture kapitál web", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Národný holdingový fond NHF investícia", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"Venture to Future Fund\" Slovakia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Národný holdingový fond NHF investícia"

Links: [{"title":"nh fund","url":"https://altss.com/profile/nh-fund.md"},{"title":"n rodn holdingov fond nhfond sk","url":"https://venturecapitalarchive.com/venture-funds/n-rodn-holdingov-fond-nhfond-sk"},{"title":"National Homeownership Fund Ghana: Complete Institutional Profile","url":"https://ownkey.com/gh/blog/national-homeownership-fund-ghana-profile"},{"title":"Wybrane aspekty gospodarki finansowej Narodowego Funduszu Ochrony Zdrowia (NFOZ)","url":"https://dspace.uni.lodz.pl/handle/11089/6774"},{"title":"Národní rozvojový fond přichází. Podpoří projekty v infrastruktuře","url":"https://www.businessinfo.cz/clanky/narodni-rozvojovy-fond-prichazi-podpori-projekty-v-infrastrukture/"},{"title":"Compare · NHF vs PAND","url":"https://new.quantisnow.com/compare/PAND/vs/NHF"},{"title":"Compare · NHF vs SAF","url":"https://new.quantisnow.com/compare/SAF/vs/NHF"},{"title":"Compare · BAF vs NHF","url":"https://new.quantisnow.com/compare/BAF/vs/NHF"},{"title":"Compare · BF vs NHF","url":"https://new.quantisnow.com/compare/BF/vs/NHF"}]

Národný holdingový fond (NHF) is a Slovak state-linked risk-capital investor. The results are mostly from third-party profile sites, so I'd check details against the official site, nhfond.sk.

- **Ownership:** NHF is a wholly owned subsidiary of the Slovak Business Agency, which coordinates EU and state support for small and medium enterprises. NH Fund is a wholly owned subsidiary
… [skrátené, 2930 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Fond inovácií a technológií a.s. FIT venture kapitál web"

Links: [{"title":"FIT vám pomôže zafinancovať inovatívne podnikateľské nápady","url":"https://www.podnikajte.sk/investor/fit-fond-financovanie"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital?page=7"},{"title":"Podnikateľ a investor","url":"https://www.podnikajte.sk/investor?page=5"},{"title":"eif icf and grow venture partners sign agreement to set up the fondo de inversion en tecnologia avanzada fita","url":"https://www.eif.org/press/all/eif-icf-and-grow-venture-partners-sign-agreement-to-set-up-the-fondo-de-inversion-en-tecnologia-avanzada-fita"},{"title":"Fondation pour l'Innovation Technologique Overview","url":"https://pitchbook.com/profiles/advisor/54632-44"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"el fei icf y grow venture partners firman el acuerdo de puesta en marcha del fons d inversi en tecnologia avan ada fita","url":"https://capital-riesgo.es/en/articles/el-fei-icf-y-grow-venture-partners-firman-el-acuerdo-de-puesta-en-marcha-del-fons-d-inversi-en-tecnologia-avan-ada-fita-/"},{"title":"FONDATION POUR L'INNOVATION ET LA TECHNOLOGIE (FIT)","url":"https://www.fundraiso.ch/en/organisations/fondation-pour-linnovation-technologique-fit"},{"title":"www.startitup.sk","url":"https://www.startitup.sk/?p=12
… [skrátené, 2969 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Venture to Future Fund" Slovakia"

Links: [{"title":"Venture to Future Fund","url":"https://www.sih.sk/en/stranky/cinnosti/venture-to-future-fund"},{"title":"Slovakia Venture to Future Fund","url":"https://app.dealroom.co/investors/slovakia_venture_to_future_fund"},{"title":"Venture to Future Fund increases capital by EUR 15.3 million to support Slovak startups","url":"https://www.sih.sk/en/aktuality/venture-to-future-fund-increases-capital-by-eur-15-3-million-to-support-slovak-startups"},{"title":"Venture to Future Fund Overview","url":"https://pitchbook.com/profiles/investor/461930-23"},{"title":"venture to future fund a s","url":"https://superscout.co/investor/venture-to-future-fund-a-s"},{"title":"Luxembourg, 14.11.2019","url":"https://www.eib.org/attachments/registers/125282376.pdf"},{"title":"vff sk","url":"https://superscout.co/investor/vff-sk"},{"title":"venture to future fund navysuje kapital o 15 3 miliona eur na podporu slovenskych startupov","url":"https://www.sih.sk/en/aktuality/venture-to-future-fund-navysuje-kapital-o-15-3-miliona-eur-na-podporu-slovenskych-startupov"},{"title":"Venture Capital","url":"https://altss.com/profile/venture-to-future-fund"}]

Venture to Future Fund (VFF) is a Bratislava-based venture capital fund that invests in Slovak companies. The sources agree on its basic purpose, but they disagree on its size and portfolio.

**Purpose and strategy:** The Slovak Investment Holding (SIH) describes VFF as a fund se
… [skrátené, 3486 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CVI Central European venture investor Slovakia CVI SLOVCA"

Links: [{"title":"Popularita private equity a venture kapitálu na Slovensku","url":"https://www.podnikajte.sk/investor/private-equity-venture-kapital-na-slovensku"},{"title":"Founded Year","url":"https://www.cbinsights.com/company/slovca"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/slovca/financials"},{"title":"HAVEL PARTNERS Recognised for Best Venture Capital Investment in Slovakia at CVCA SLOVCA Awards 2025","url":"https://amcham.sk/news/274322/havel-partners-recognised-for-best-venture-capital-investment-in-slovakia-at-cvca-slovca-awards-2025"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital?page=1"},{"title":"alternatives competitors","url":"https://www.cbinsights.com/company/slovca/alternatives-competitors"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital"},{"title":"Venture Capital","url":"https://altss.com/profile/venture-to-future-fund"},{"title":"Venture Capital in Central and Eastern Europe - Slovakian Case","url":"https://ceeol.com/search/article-detail?id=1125823"}]

The search didn't return anything for "CVI" as an organization. The closest match is the **CVCA SLOVCA Awards**, which appear in a 2025 AmCham item. The results don't say what CVCA stands for, so I can't confirm that it is "Central European" or "Czech
… [skrátené, 3306 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL -A "Mozilla/5.0" https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html | grep -oiE 'href="https?://[^"]+"' | sort -u | grep -viE 'slovca|facebook|linkedin|twitter|google'
```

<details><summary>Výstup nástroja</summary>

```
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp && curl -sL -A "Mozilla/5.0" https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html | grep -iE -B3 -A12 'CVI' | head -60
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html", "prompt": "List every member with any website URL or description shown, especially CVI, Fond inovácií a technológií, Národný holdingový fond, Venture to Future Fund, Sandberg Capital, Genesis Capital."}
```

<details><summary>Výstup nástroja</summary>

```
The page lists 12 full members. None shows an external website URL or a description. Each entry has only a name, a logo, and a link to its SLOVCA profile page, shown as a relative path below.

| Member | Profile link (SLOVCA page) |
|---|---|
| ARX Equity Partners | /sk/riadni-clenovia/arx-equity-partners.html |
| CVI | /sk/riadni-clenovia/cvi.html |
| Enterprise Investors | /sk/riadni-clenovia/enterprise-investors.html |
| Eterus Capital | /sk/riadni-clenovia/eterus-capital.html |
| Fond inovácií a technológií | /sk/riadni-clenovia/fond-inovacii-a-technologii.html |
| Genesis Capital | /sk/riadni-clenovia/genesis-capital.html |
| Jet Investment | /sk/riadni-clenovia/jet-investment.html |
| Národný holdingový fond s.r.o. | /sk/riadni-clenovia/narodny-holdingovy-fond-s-r-o.html |
| Neulogy Ventures | /sk/riadni-clenovia/neulogy-ventures.html |
| Sandberg Capital | /sk/riadni-clenovia/sandberg-capital.html |
| Venture to Future Fund | /sk/riadni-clenovia/venture-to-future-fund.html |
| Vision Ventures | /sk/riadni-clenovia/vision-ventures.html |

For the six you asked about (CVI, Fond inovácií a technológií, Národný holdingový fond, Venture to Future Fund, Sandberg Capital, Genesis Capital), the content contains only the name, logo, and SLOVCA profile link. The actual member websites and descriptions would be on those linked profile pages, which aren't included in the content above.
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for s in cvi fond-inovacii-a-technologii narodny-holdingovy-fond-s-r-o venture-to-future-fund sandberg-capital genesis-capital; do echo "=== $s"; u=https://www.slovca.sk/sk/riadni-clenovia/$s.html; curl -sL -A "Mozilla/5.0" $u | grep -oiE 'href="https?://[^"]+"' | grep -viE 'slovca|facebook|linkedin|twitter|google|cdnjs|instagram|youtube'; timeout 30 python3 -I page.py show $u 4000 | sed -n '/Riadni/,$p' | head -40; done
```

<details><summary>Výstup nástroja</summary>

```
=== cvi
Riadni členovia
Pridružení členovia
Partnerskí členovia
Partneri
Etický kódex
Prihláška
Private Equity & Venture Capital
Vysvetlenie pojmov
Kapitálové investície vs pôžičky
Kontakt
SK
EN
CVI
CVI Dom Maklerski Sp. Z O.O.
Adresa: Plac Europejski 2, bldg C, 00-844 Varšava, Poľsko
Email: [email]
Web: www.cvi.eu
Informácie o spoločnosti:
Objem prostriedkov v správe:
800 miliónov EUR
Typ investícii:
Direct Lending, Senior Debt, Mezzanine, Výnimočne minoritná ekvitná investícia
Preferovaná výška jednej investícii:
2 – 15 miliónov EUR
Preferované odvetvie:
bez preferencie
Geografické zameranie:
CEE
Prílohy na stiahnutie
Znak_podstawowy.jpg(veľkosť 64 KB, formát jpg)
Riadni členovia
ARX Equity Partners
CVI
Enterprise Investors
Eterus Capital
Fond inovácií a technológií
Genesis Capital
Jet Investment
Národný holdingový fond s.r.o.
Neulogy Ventures
=== fond-inovacii-a-technologii
Riadni členovia
Pridružení členovia
Partnerskí členovia
Partneri
Etický kódex
Prihláška
Private Equity & Venture Capital
Vysvetlenie pojmov
Kapitálové investície vs pôžičky
Kontakt
SK
EN
Fond inovácií a technológií
Investičný horizont: 4 až 6 rokov
Výška investície: od 20 000 EUR do 1 500 000 EUR
Územná pôsobnosť: sídlo investičného cieľa a aspoň časť aktivít na území Slovenskej republiky
Zameranie na seed spoločnosti, start-up a spin-off spoločnosti, expansion spoločnosti
Web: https://www.fondfit.sk/
Prílohy na stiahnutie
fit.JPG(veľkosť 18 KB, formát JPG)
Riadni členovia
ARX Equity P
… [skrátené, 6784 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for s in arx-equity-partners enterprise-investors eterus-capital jet-investment neulogy-ventures vision-ventures; do echo "=== $s"; u=https://www.slovca.sk/sk/riadni-clenovia/$s.html; timeout 30 python3 -I page.py show $u 4000 | sed -n '/^EN$/,/Prílohy/p' | head -30; done; echo ====CVI; timeout 30 python3 -I page.py show https://www.cvi.eu/ 4000; 
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
=== arx-equity-partners
EN
ARX Equity Partners
Preferovaná výška investície : EUR 10-50 mil.
Objem prostriedkov v správe: EUR 300 mil. (total commitments since inception)
Preferované odvetvie: bez preference
Geografické zameranie: Central Europe
Kontakná osoba : Michal Aron
Email: [email]
Web: https://arxequity.com/
Prílohy na stiahnutie
=== enterprise-investors
EN
Enterprise Investors
Adresa: Warsaw Financial Center, 53 Emilii Plater St., 00-113 Varšava, Poľsko
Tel.: +421 911 320 087
Web: https://www.ei.com.pl/sk/
E-mail: [email]
Preferovaná výška jednej investície: 20 - 50 miliónov eur
Geografické zameranie: CEE region
Počet transakcií v SR: 4 ( NAY, STD DONIVO, ORANGE, CBA Slovakia )
Typy transakcií: Buyout, Expanzívne financovanie, Leveraged buyout, Management buyout, Pre IPO
Preferované odvetvie: spotrebný tovar a maloobchod, priemyselný tovar a služby, IT a telekomunikácie, finančné služby, farmácia a zdravotná starostlivosť, stavebníctvo
Informačné pdf o Enterprise Investors na stiahnutie nižšie
Prílohy na stiahnutie
=== eterus-capital
EN
Eterus Capital
Adresa: Laurinská 18, 811 01 Bratislava, Slovensko
Mobil: +421 914 32 00 65
E-mail: [email]
Web: www.eterus.sk
Typ investícií: Private equity
Preferovaná výška investície: 500 tis. Eur až 5 mil. Eur.
Preferované odvetvie: Odvetvia s vyššou pridanou hodnotou, investície do príležitostí v rozvojovom štádiu životného cyklu v odvetviach so silným rastovým potenciálom
… [skrátené, 3199 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.cvi.eu/ https://cvi.eu/en/ ; do echo "== $u"; timeout 30 python3 -I page.py show $u 5000 2>&1 | tail -60; done
```

<details><summary>Výstup nástroja</summary>

```
== https://www.cvi.eu/
    self.endheaders(body, encode_chunked=encode_chunked)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/http/client.py", line 1362, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/http/client.py", line 1122, in _send_output
    self.send(msg)
    ~~~~~~~~~^^^^^
  File "/usr/lib/python3.14/http/client.py", line 1066, in send
    self.connect()
    ~~~~~~~~~~~~^^
  File "/usr/lib/python3.14/http/client.py", line 1508, in connect
    self.sock = self._context.wrap_socket(self.sock,
                ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
                                          server_hostname=server_hostname)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sock=sock,
        ^^^^^^^^^^
    ...<5 lines>...
        session=session
        ^^^^^^^^^^^^^^^
    )
    ^
  File "/usr/lib/python3.14/ssl.py", line 1076, in _create
    self.do_handshake()
    ~~~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.14/ssl.py", line 1372, in do_handshake
    self._sslobj.do_handshake()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not
… [skrátené, 6176 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && sed -i 's/^    txt=fetch(url)$/    try: txt=fetch(url)\n    except Exception as e: print("ERR",repr(e)[:200]); sys.exit(1)/' page.py && for u in https://cvi.pl/en/ https://www.cvi.pl/ https://sandbergcapital.com/ https://www.nhfond.sk/ https://vff.sk/ https://www.fondfit.sk/ https://www.genesis.cz/ https://www.visionventures.vc/; do echo "== $u"; timeout 30 python3 -I page.py show $u 1500; done
```

<details><summary>Výstup nástroja</summary>

```
== https://cvi.pl/en/
Home page - CVI Dom Maklerski sp. z o.o.
Skip to main content
Hit enter to search or ESC to close
Close Search
Menu
About us
Team
News
ESG policy
Regulations
Career
Looking for financing
Why CVI?
How can we help?
What do we finance
Investment process
Industries
Looking to invest
Private debt
Strategies and funds
Partners
Contact
EN
PL
EN
We provide flexible capital solutions
in Central Europe Read more
CVI is a leader in the private debt market in Central Europe
CVI is an independent investment company operating since 2012. CVI manages portfolios for 8 investment funds with a total AUM of EUR 1,1 mld. CVI provides flexible financing solutions for medium-sized companies to meet a wide range of capital needs.
What can we help you with?
Looking for financing
We finance the development of small and medium-sized enterprises from Central EuropeRead more
Looking to invest
We invite you to invest in the private debt market through investment funds managed by usRead more
CVI in numbers
Private debt investments value
EUR 3.3 billion
Assets under management
EUR 1.1 billion
Private debt investments
850+
CEE countries with CVI investments
10
CVI team members
45
Funds
8
We are an investor, a partner in business
We provide flexible
financing in Central EuropeRead more
News
Filter
AllNews
Financing for REGESTA S.A.2026-09-29
Tomasz Lubowiecki, founder of 7R, on the role of external capital in the company’s growth2026-09-29
Rafał Lis speaks at Property Forum 20262026-09-
… [skrátené, 12217 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL -A "Mozilla/5.0" https://www.arxequity.com/ | grep -oE 'href="[^"]*"' | sort -u | grep -i arx | head -40; python3 -I page.py show https://www.arxequity.com/ 4000 | sed -n '30,80p'
```

<details><summary>Výstup nástroja</summary>

```
href="https://www.arxequity.com/"
href="https://www.arxequity.com/about-arx/"
href="https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-hlb-proxy/"
href="https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/"
href="https://www.arxequity.com/arx-equity-partners-invests-in-direct4me/"
href="https://www.arxequity.com/comments/feed/"
href="https://www.arxequity.com/contact/"
href="https://www.arxequity.com/cz/"
href="https://www.arxequity.com/feed/"
href="https://www.arxequity.com/home/feed/"
href="https://www.arxequity.com/investments/"
href="https://www.arxequity.com/news/"
href="https://www.arxequity.com/pl/"
href="https://www.arxequity.com/sustainability-reports/"
href="https://www.arxequity.com/team/"
href="https://www.arxequity.com/working-with-arx/"
href="https://www.arxequity.com/wp-content/uploads/2016/06/arxfav.png"
href="https://www.arxequity.com/wp-json/"
href="https://www.arxequity.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.arxequity.com%2F&#038;format=xml&#038;lang=en"
href="https://www.arxequity.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.arxequity.com%2F&#038;lang=en"
href="https://www.arxequity.com/wp-json/wp/v2/pages/2"
href="https://www.arxequity.com/xmlrpc.php"
href="https://www.arxequity.com/xmlrpc.php?rsd"
cz
pl
We are proud of our 20-year track record building great companies in successful partnerships with business owners and managers
About AR
… [skrátené, 2213 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.arxequity.com/about-arx/ https://www.arxequity.com/working-with-arx/ https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/ https://www.arxequity.com/arx-equity-partners-invests-in-direct4me/ https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-hlb-proxy/; do echo "=== $u"; python3 -I page.py show $u 9000 | sed -n '/^pl$/,$p' | grep -v -E '^(en|cz|pl|Toggle navigation|About ARX|Working with ARX|Team|Investments|News|Contact)$' | head -25; done
```

<details><summary>Výstup nástroja</summary>

```
=== https://www.arxequity.com/about-arx/
With more than € 300 million raised in four funds, ARX has become a leading private equity firm in its segment operating in the Central European (“CE”) region. We have a 20-year track-record investing in and supporting the growth of mid-sized CE companies.
Headquartered in Prague, the firm’s activities are managed by an experienced and multinational team of investment professionals, combining a wide range of international expertise plus in-depth local knowledge. This combination of a locally based team of decision-makers, coupled with substantial international capabilities, is key to the success of ARX and its investee companies.
Our core objective is to form successful partnerships with owners, managers and other stakeholders with the aim of realising the full potential of our portfolio companies, while achieving superior returns for the firm‘s investors and partner entrepreneurs. ARX itself reflects the value of partnership, as our firm is structured as a partnership of complementary individuals.
The core elements of the ARX investment philosophy
Partnership. At ARX we believe in the power of successful partnerships. Our primary goal is to partner with owners and managers in releasing growth potential and developing businesses. Our firm also provides financing to entrepreneurially-minded managers in order to fund management buy-out and management buy-in (MBO & MBI) transactions.
Aligned Incentives. We are focused on increasing shareh
… [skrátené, 17140 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I page.py grep https://www.arxequity.com/investments/ 'slova|slovak|hungar|poland|polsk|croat|sloven|country|countries' ; python3 -I page.py grep https://www.arxequity.com/about-arx/ 'Slovak|countries|Czech'; python3 -I page.py grep https://www.arxequity.com/contact/ 'Bratislava|Slovak|Warsaw|Budapest|s\.r\.o|a\.s\.|IČ|ID'
```

<details><summary>Výstup nástroja</summary>

```
- With more than € 300 million raised in four funds and investments completed in five CE countries, ARX has become a leading private equity firm in its region.
- ARX has completed more than 20 platform investments over the past two decades in five CE countries, plus more than 10 complementary add-on acquisitions. Our industry knowledge, investment experience and international resources, provide a valuable edge in identifying and creating value in CE companies.
- Slovenia / 2026
- Slovenia / 2026
- Croatia / 2025
- Slovenia / 2022
- Hungary / 2022
- Slovenia / 2021
- Slovenia / 2019
- Hungary / 2018
- Slovenia / 2015
- Poland / 2014
- Hungary / 2014
- Poland / 2010
- Poland / 2010
- Poland / 2009
- Slovenia / 2008
- Slovenia / 2007
- Hungary / 2007
- Poland / 2006
- Slovenia / 2006
- Poland / 2003
- Insty-Prints (Print Polska)
- Poland / 2000
- Hungarocamion
- Hungary / 1998
- Poland / 1998
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I page.py grep https://www.arxequity.com/investments/ 'czech|slovakia|austria' ; python3 -I page.py show https://www.arxequity.com/contact/ 3000 | sed -n '/^pl$/,$p' | head -30
```

<details><summary>Výstup nástroja</summary>

```
- Czech Republic / 2026
- Czech Republic / 2022
- Czech Republic / 2021
- Czech Republic / 2019
- Czech Republic / 2019
- Czech Republic / 2019
- Czech Republic / 2017
- Czech Republic / 2013
- Czech Republic / 2011
- Czech Republic / 2011
- Czech Republic / 2011
- Czech Republic / 2011
- Czech Republic / 2010
- Czech Republic / 2010
- Czech Republic / 2009
- Czech Republic / 2008
- Czech Republic / 2008
- Czech Republic / 2006
- Czech Republic / 2000
- Czech on Line
- Czech Republic / 1998
pl
ARX Czech Republic
Ehlenův dům, 28. října 12 110 00 Praha 1
Tel.: +420 22 423 5399
Email: [email]
ARX Poland
ul. Niecała 14 05-510 Konstancin-Jeziorna
Tel: +48 602 451 284
Email: [email]
ARX Equity Partners
© 2012-2026 All rights reserved.
The ARX IV Fund benefits from the support of the European Union under the Equity Facility for Growth established under Regulation (EU) No 1287/2013 of the European Parliament and the Council establishing a Programme for the Competitiveness of Enterprises and small and medium enterprises (COSME) (2014-2026)
About ARX
Working with ARX
Team
Investments
News
Contact
SFDR disclosure
Sustainability Reports
×
```

</details>

**Nástroj `Bash`**

```bash
cat src/investordb/models.py | head -150; ls research/
```

<details><summary>Výstup nástroja</summary>

```
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator

InvestorType = Literal[
    "vc", "pe", "cvc", "family_office", "angel", "private_investor", "public_fund", "fund_of_funds"
]
EntityKind = Literal[
    "investor", "service_provider", "lender", "platform", "grant_scheme", "public_markets_manager"
]
Stage = Literal["pre-seed", "seed", "series-a", "series-b-plus", "growth", "buyout"]
Currency = Literal["EUR", "USD", "CZK", "GBP", "HUF", "PLN", "CHF"]
ExclusionReason = Literal[
    "not_investor_service",
    "debt_only",
    "platform_only",
    "grant_only",
    "public_markets_only",
    "inactive",
    "no_evidence",
    "duplicate",
]
CheckStatus = Literal["verified", "quote_not_found", "http_error", "fetch_error", "unsupported_content"]

INVESTOR_TYPES: tuple[str, ...] = InvestorType.__args__
EXCLUSION_REASONS: tuple[str, ...] = ExclusionReason.__args__


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Evidence(Strict):
    source_url: HttpUrl
    source_date: date | None = None
    quote: str = Field(min_length=8, max_length=600)

    @field_validator("quote")
    @classmethod
    def quote_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("quote must not be blank")
        return value.strip()


class KindFact(Evidence):
    value: EntityKind


class TypeFact(Evidence):
    value: Investor
… [skrátené, 3920 znakov]
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p /home/filip/investor-db/research && cat > /home/filip/investor-db/research/c001.json <<'EOF'
{
  "candidate_id": "c001",
  "name": "ARX Equity Partners",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "PL", "HU", "SI", "HR"],
  "website": "https://www.arxequity.com/",
  "entity_kind": {"value": "investor", "source_url": "https://www.arxequity.com/about-arx/", "source_date": null, "quote": "With more than € 300 million raised in four funds, ARX has become a leading private equity firm in its segment operating in the Central European (“CE”) region."},
  "investor_type": {"value": "pe", "source_url": "https://www.arxequity.com/arx-equity-partners-acquires-majority-stake-in-medicofit-slovenias-leading-private-physiotherapy-provider/", "source_date": "2026-08-26", "quote": "ARX Equity Partners (“ARX”), a leading Central European private equity firm, today announced the acquisition of a majority stake in Medicofit, fizioterapija d.o.o. (“Medicofit” or the “Company”), Slovenia’s foremost private provider of integrated musculoskeletal care."},
  "sectors": null,
  "stages": {"value": ["buyout"], "source_url": "https://www.arxequity.com/about-arx/", "source_date": null, "quote": "Our firm also provides financing to entrepreneurially-minded managers in order to fund management buy-out and management buy-in (MBO & MBI) transactions."},
  "ticket_min": null,
  "ticket_max": null,
  "aum": {"amount": 300000000, "currency": "EUR", "source_url": "h
… [skrátené, 3705 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c001.json
c001 entity_kind: OK
c001 investor_type: OK
c001 stages: OK
c001 aum: OK
c001 inv0: OK
c001 inv1: OK
c001 inv2: OK
```

</details>

**Nástroj `Bash`**

```bash
ls -la /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/ /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools; cat /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py
```

<details><summary>Výstup nástroja</summary>

```
/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/:
total 4
drwx------ 5 filip filip  120 Oct  9 14:20 .
drwx------ 4 filip filip   80 Oct  9 14:15 ..
drwxr-xr-x 2 filip filip  140 Oct  9 14:22 bin
-rw-r--r-- 1 filip filip  515 Oct  9 14:19 c009.json
drwxr-xr-x 2 filip filip 1400 Oct  9 14:22 pages
drwxr-xr-x 3 filip filip  120 Oct  9 14:22 tools

/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools:
total 12
drwxr-xr-x 3 filip filip  120 Oct  9 14:22 .
drwx------ 5 filip filip  120 Oct  9 14:20 ..
drwxr-xr-x 2 filip filip   60 Oct  9 14:22 __pycache__
-rw-r--r-- 1 filip filip 1636 Oct  9 14:20 fetch.py
-rw-r--r-- 1 filip filip 1766 Oct  9 14:21 page.py
-rw-r--r-- 1 filip filip  574 Oct  9 14:20 verify.py
import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import text_of
norm = lambda s: re.sub(r"\s+"," ",s).strip()
for f in sys.argv[1:]:
    d = json.load(open(f))
    items = [(k, d[k]) for k in ("entity_kind","investor_type","sectors","stages","ticket_min","ticket_max","aum") if d.get(k)]
    items += [(f"inv{i}", v) for i, v in enumerate(d.get("investments", []))]
    for k, e in items:
        ok = norm(e["quote"]) in norm(text_of(e["source_url"]))
        print(f"{d['candidate_id']} {k}: {'OK' if ok else 'MISSING'}")
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad; mkdir -p $S/r1/tools $S/r1/pages; cat $S/tools/page.py | head -5; cat $S/tools/fetch.py
```

<details><summary>Výstup nástroja</summary>

```
import sys, re, html, hashlib, os, urllib.request
from html.parser import HTMLParser
PAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages")
class T(HTMLParser):
    def __init__(self):
import sys, hashlib, subprocess, re, html, os
from html.parser import HTMLParser
PAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages")
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, t, a):
        if t in ("script","style","noscript","svg"): self.skip+=1
        if t in ("p","div","br","li","h1","h2","h3","h4","tr","section","article"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script","style","noscript","svg") and self.skip: self.skip-=1
        if t in ("p","div","li","h1","h2","h3","h4"): self.out.append("\n")
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
def text_of(url):
    h = hashlib.md5(url.encode()).hexdigest()[:12]
    path = os.path.join(PAGES, h + ".txt")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    raw = subprocess.run(["curl","-sL","--max-time","30","-A","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",url],capture_output=True).stdout
    s = raw.decode("utf-8", errors="replace")
    p = P(); p.feed(s)
    t = "".join(p.out)
    t = re.sub(r"[ \t\xa0]+"," ",t)
    t = re.sub(r"\n\s*\n+","\n",t)
    open(
… [skrátené, 1856 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad; cp $S/tools/page.py $S/r1/tools/page.py; cat > $S/r1/tools/verify.py <<'EOF'
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import fetch, norm
for f in sys.argv[1:]:
    d=json.load(open(f))
    items=[(k,v) for k,v in d.items() if isinstance(v,dict) and "quote" in v]
    items+= [("inv:"+i["company"],i) for i in d.get("investments") or []]
    for k,v in items:
        try: txt=norm(fetch(v["source_url"]))
        except Exception as e: print(f, k, "FETCHERR", e); continue
        print(os.path.basename(f), k, "OK" if norm(v["quote"]) in txt else "MISSING")
EOF
cd /home/filip/investor-db && python3 -I $S/r1/tools/verify.py research/c001.json
```

<details><summary>Výstup nástroja</summary>

```
c001.json entity_kind OK
c001.json investor_type OK
c001.json stages OK
c001.json aum OK
c001.json inv:Medicofit OK
c001.json inv:Direct4me OK
c001.json inv:HLB PROXY OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0" https://cvi.pl/en/ | grep -oE 'href="https://cvi.pl/en/[^"]*"' | sort -u | head -40
```

<details><summary>Výstup nástroja</summary>

```
href="https://cvi.pl/en/"
href="https://cvi.pl/en/career/"
href="https://cvi.pl/en/contact/"
href="https://cvi.pl/en/esg-policy/"
href="https://cvi.pl/en/feed/"
href="https://cvi.pl/en/looking-for-financing/"
href="https://cvi.pl/en/looking-for-financing/how-can-we-help/"
href="https://cvi.pl/en/looking-for-financing/industries/"
href="https://cvi.pl/en/looking-for-financing/investment-process/"
href="https://cvi.pl/en/looking-for-financing/what-do-we-finance/"
href="https://cvi.pl/en/looking-for-financing/why-cvi/"
href="https://cvi.pl/en/looking-to-invest/"
href="https://cvi.pl/en/looking-to-invest/partners/"
href="https://cvi.pl/en/looking-to-invest/private-debt/"
href="https://cvi.pl/en/looking-to-invest/strategies-and-funds/"
href="https://cvi.pl/en/news/"
href="https://cvi.pl/en/news/financing-for-regesta-s-a/"
href="https://cvi.pl/en/news/rafal-lis-speaks-at-property-forum-2026/"
href="https://cvi.pl/en/news/tomasz-lubowiecki-founder-of-7r-on-the-role-of-external-capital-in-the-companys-growth/"
href="https://cvi.pl/en/regulations/"
href="https://cvi.pl/en/team/"
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for u in https://cvi.pl/en/looking-for-financing/what-do-we-finance/ https://cvi.pl/en/looking-for-financing/how-can-we-help/ https://cvi.pl/en/looking-to-invest/strategies-and-funds/; do echo "=== $u"; python3 -I $S/page.py show $u 8000 | sed -n '/^EN$/,$p' | sed -n '3,45p'; done; python3 -I $S/page.py grep https://cvi.pl/en/ 'slovak|equity|bond|loan'
```

<details><summary>Výstup nástroja</summary>

```
=== https://cvi.pl/en/looking-for-financing/what-do-we-finance/
EN
Home page » Looking for financing » What do we finance
What do we finance?
We can solve a wide spectrum of capital needs for companies operating in Central Europe
Working capital
Ensuring an appropriate working capital level is crucial for every company, especially the ones that expect strong revenue growth, have long production cycle, are exposed to sales seasonality or require flexible solutions for suppliers and clients. CVI understands that additional and often unpredictable elements also come into play, such as one-off sizeable contract or liquidity shortages that require a quick response.
CVI can provide funds to strengthen working capital through a range of instruments, from senior financing to subordinated financing to minority equity investments. CVI financing can be launched as new financing, to pay down existing debt, or to supplement existing financing in the company, including bank financing.
Capital expenditure (capex)
CVI finances capital expenditures related to product or service development, production or warehousing capacity extension, etc. CVI can base its analysis not only on historical results, but also on projected results that include additional growth from the utilisation of the agreed capital expenditure. This differentiates CVI from banks which typically base their analysis solely on historical figures and require heavy additional collateral.
CVI can provide funds for investment throu
… [skrátené, 12263 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://cvi.pl/en/news/ 'slovak|czech|hungar|croat|romania'; python3 -I $S/page.py grep https://cvi.pl/en/looking-for-financing/why-cvi/ 'slovak|countries|czech'; python3 -I $S/page.py grep https://cvi.pl/en/contact/ 'KRS|NIP|REGON|Bratislava|Prague|Praha'
```

<details><summary>Výstup nástroja</summary>

```
- Private debt investments in Romania2025-07-04
- KRS: 0000424707, NIP: 9542738238, REGON: 242949739 Company registered in the District Court for the City of Warsaw | XIII Economic Department | Share capital: PLN 1,929,500.00
- Prague
- Praha 1, 110 00
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c002.json <<'EOF'
{
  "candidate_id": "c002",
  "name": "CVI",
  "legal_name": "CVI Dom Maklerski sp. z o.o.",
  "reg_no": null,
  "country": "PL",
  "active_in": ["PL", "CZ", "RO"],
  "website": "https://cvi.pl/en/",
  "entity_kind": {"value": "lender", "source_url": "https://cvi.pl/en/", "source_date": null, "quote": "CVI is a leader in the private debt market in Central Europe"},
  "investor_type": null,
  "sectors": null,
  "stages": null,
  "ticket_min": null,
  "ticket_max": null,
  "aum": null,
  "funds": [],
  "investments": [],
  "duplicate_of": null,
  "notes": "Warsaw-based private debt manager (8 funds, AUM EUR 1.1 bn per cvi.pl); instruments are mainly senior/junior debt, unitranche, mezzanine and private bonds, with minority equity only as an add-on, so classified as lender rather than investor. Polish KRS 0000424707 (no IČO). No Slovak deal found on its site; SLOVCA lists CEE as geographic focus.",
  "researched_at": "2026-10-09"
}
EOF
cd /home/filip/investor-db && PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c002.json && python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c002.json
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c002.json
c002.json entity_kind OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0" https://www.ei.com.pl/en/ | grep -oE 'href="[^"]*"' | sort -u | grep -iE 'news|about|invest' | head -30; python3 -I $S/page.py show https://www.ei.com.pl/en/ 6000 | sed -n '18,70p'
```

<details><summary>Výstup nástroja</summary>

```
href="/en/18gym-and-stay-fit-gym-join-forces-with-backing-from-enterprise-investors"
href="/en/about/"
href="/en/ei-re-enters-the-renewables-sector-with-majority-investment-in-art-wind"
href="/en/enterprise-investors-returns-to-lithuania-with-investment-in-kredito-unija-saulegraza"
href="/en/enterprise-investors-to-sell-moya-owner-anwim-to-stonepeak-and-energy-equation-partners"
href="https://www.ei.com.pl/en/about/"
href="https://www.linkedin.com/company/enterprise-investors"
We are the most experienced private equity investor in Central and Eastern Europe.
Since 1990, we have been supporting the development of high-potential companies by providing the capital and expertise necessary to implement ambitious growth strategies.
Read more
News
October 06, 2026
18GYM and Stay Fit Gym join forces with backing from Enterprise Investors
Read more
July 01, 2026
Enterprise Investors returns to Lithuania with investment in Kredito unija "Saulėgrąža"
Read more
June 11, 2026
Enterprise Investors to sell MOYA owner Anwim to Stonepeak and Energy Equation Partners
Read more
March 16, 2026
EI re-enters the renewables sector with majority investment in Art Wind
Read more
Varso Tower
69 Chmielna Street, 34th floor
00-801 Warsaw
tel.: +48 22 458 85 00
About us
Team
Investments
News
Contact
LP login
GDPR information
clause
Get directions
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in about/ 18gym-and-stay-fit-gym-join-forces-with-backing-from-enterprise-investors enterprise-investors-returns-to-lithuania-with-investment-in-kredito-unija-saulegraza ei-re-enters-the-renewables-sector-with-majority-investment-in-art-wind; do echo "=== $p"; python3 -I $S/page.py show https://www.ei.com.pl/en/$p 7000 | sed -n '/^EN$/,$p' | sed -n '2,22p'; done
```

<details><summary>Výstup nástroja</summary>

```
=== about/
Home
›
About us
Enterprise Investors is the most experienced private equity investor in Central and Eastern Europe. Since 1990, our firm has supported the growth of promising companies by providing the capital and expertise they need to implement ambitious growth strategies.
The firm has raised 10 funds and invested EUR 2.5 billion in 163 companies, focusing on rapidly growing sectors such as technology, financial services, consumer goods, business services, healthcare, retail and manufacturing. We invest between EUR 20 million and EUR 75 million for stakes ranging from large minority positions to full ownership and we take a long-term perspective, our involvement typically lasting five to eight years.
Decades of market presence have allowed us to build exceptional cross-sector expertise and a strong network of contacts, thanks to which we can effectively identify and grow the region’s best businesses.
The firm has raised 10 funds and invested EUR 2.5 billion in 163 companies, focusing on rapidly growing sectors such as technology, financial services, consumer goods, business services, healthcare, retail and manufacturing. We invest between EUR 20 million and EUR 75 million for stakes ranging from large minority positions to full ownership and we take a long-term perspective, our involvement typically lasting five to eight years.
Decades of market presence have allowed us to build exceptional cross-sector expertise and a strong network of contacts, thanks to which 
… [skrátené, 14363 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c003.json <<'EOF'
{
  "candidate_id": "c003",
  "name": "Enterprise Investors",
  "legal_name": null,
  "reg_no": null,
  "country": "PL",
  "active_in": ["PL", "RO", "LT", "SK"],
  "website": "https://www.ei.com.pl/en/",
  "entity_kind": {"value": "investor", "source_url": "https://www.ei.com.pl/en/about/", "source_date": null, "quote": "Enterprise Investors is the most experienced private equity investor in Central and Eastern Europe."},
  "investor_type": {"value": "pe", "source_url": "https://www.ei.com.pl/en/about/", "source_date": null, "quote": "Enterprise Investors is the most experienced private equity investor in Central and Eastern Europe."},
  "sectors": {"value": ["technology", "financial services", "consumer goods", "business services", "healthcare", "retail", "manufacturing"], "source_url": "https://www.ei.com.pl/en/about/", "source_date": null, "quote": "The firm has raised 10 funds and invested EUR 2.5 billion in 163 companies, focusing on rapidly growing sectors such as technology, financial services, consumer goods, business services, healthcare, retail and manufacturing."},
  "stages": {"value": ["growth", "buyout"], "source_url": "https://www.ei.com.pl/en/about/", "source_date": null, "quote": "We invest between EUR 20 million and EUR 75 million for stakes ranging from large minority positions to full ownership"},
  "ticket_min": {"amount": 20000000, "currency": "EUR", "source_url": "https://www.ei.com.pl/en/about/",
… [skrátené, 3801 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c003.json
c003.json entity_kind OK
c003.json investor_type OK
c003.json sectors OK
c003.json stages OK
c003.json ticket_min OK
c003.json ticket_max OK
c003.json inv:Kredito unija "Saulėgrąža" OK
c003.json inv:Art Wind OK
c003.json inv:18GYM OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0" https://www.eterus.sk/ | grep -oE 'href="https://www.eterus.sk[^"]*"' | sort -u | head -30; python3 -I $S/page.py show https://www.eterus.sk/ 8000 | sed -n '20,90p'
```

<details><summary>Výstup nástroja</summary>

```
Do inovácií sme formou private equity investovali
už viac než 40 mil. EUR.
Hľadám investora
Tomáš Červenka, CEO
„Eterus Capital sme oslovili koncom roku 2021 a oceňujeme korektnú a promptnú komunikáciu v celom procese transakcie, fér...
ový prístup (najmä s ohľadom na radikálnu zmenu makroekonomického prostredia počas prípravy investície) a long-term pohľad, ktorý je dôležitý v rýchlo sa meniacom svete. Našu biznisovú spoluprácu začíname s dobrými vzťahmi a v partnerskom duchu, čo nie je pri podobných transakciach samozrejmosťou.”
Zobraziť viac
Michal Štencl
„Moje skúsenosti s Eterus Capital sú nadštandardné. Eterus bol pre nás vždy korektným partnerom a za spoločnú histór...
iu od roku 2011 si nespomeniem na jeden moment, v ktorom by sme boli v nezhode, čo je v prípade iných privátnych fondov skôr výnimkou. Mal som tú česť osobne spoznať Michala Staroňa a Borisa Kostíka, ktorí v našej firme figurujú/figurovali na rôznych pozíciách v predstavenstve / dozornej rade a vždy sme u nich našli podporu, ktorú sme potrebovali na ďalší rast našej spoločnosti.”
Zobraziť viac
Martin Winkler
„Eterus Capital vystupoval počas našich rokovaní ako zodpovedný a férový partner a som rád, že sme nakoniec dosiahli k...
onsenzus a budeme spoločne podnikať ako partneri. Samotnú transakciu sme vedeli uzatvoriť veľmi rýchlo, bez zbytočných komplikácií a „korporátnych“ zdržovaní, taktík a vo veľmi korektnom duchu. Verím, že spoločná budúcnosť nám, navzdory množstvu podnikateľských výziev, prinesie ve
… [skrátené, 5115 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0" https://www.eterus.sk/ | grep -oE 'href="[^"]*"' | sort -u | grep -viE 'wp-|\.css|\.js|fonts|#' | head -30
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.eterus.sk/ -o /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/eterus.html; wc -c /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/eterus.html; grep -oE "href=['\"][^'\"]*['\"]" /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/eterus.html | sort -u | grep -viE 'wp-content|wp-includes|\.css|fonts' | head -40
```

<details><summary>Výstup nástroja</summary>

```
88541 /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/eterus.html
href="/"
href="#contact-form"
href="https://ecocapsule.com/sk/ecocapsule/"
href="https://ecpharmacies.sk/"
href="https://eterus.sk/"
href="https://eterus.sk/2021/06/16/private-equity-je-partnerstvo-v-dobrom-aj-zlom-na-niekolko-rokov/"
href="https://eterus.sk/2021/07/06/pandemia-odhalila-nutnost-mat-zdravotnicku-vyrobu-doma-pod-kontrolou/"
href="https://eterus.sk/2021/08/18/firma-z-vychodu-slovenska-dobyja-svet-marketingoveho-prieskumu/"
href="https://eterus.sk/2021/10/12/sef-hopinu-cena-250-eur-za-jazdu-nedava-zmysel-vodicovi-ani-zakaznikovi/"
href="https://eterus.sk/2021/10/24/najazdil-40-milionov-kilometrov-dnes-hopin-spaja-dopravu-a-mieri-do-zahranicia/"
href="https://eterus.sk/2021/11/30/pribeh-legendarnej-indulony-poklad-zo-socializmu-ma-vyse-70-rokov-svoj-recept-nezmenil-ani-raz/"
href="https://eterus.sk/2022/05/26/slovensko-americky-startup-je-svetovou-spickou-v-prieskume-trhu-veria-mu-aj-investori/"
href="https://eterus.sk/2022/07/27/rasto-zo-spisskej-vyvija-umelu-inteligenciu-v-kalifornii-slovenska-ai-sa-snazi-lepsie-pochopit-ludske-nazory/"
href="https://eterus.sk/2023/05/15/mtbiker-ziskal-silneho-partnera-eterus-capital-investuje-do-jeho-rozvoja/"
href="https://eterus.sk/2023/05/16/kostik-z-eterus-capital-pri-debate-s-firmami-sme-v-roli-diablovho-advokata/"
href="https://eterus.sk/en/private-equity-fund/"
href="https://eterus.sk/hladam-investora/"
href="https://eterus.
… [skrátené, 2351 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://eterus.sk/v-mediach/ 5000 | sed -n '/V médiách/,$p' | sed -n '3,40p'; echo =====; python3 -I $S/page.py show https://eterus.sk/portfolio/ 6000 | sed -n '/Portfólio/,$p' | sed -n '3,60p'; echo ====; python3 -I $S/page.py show https://eterus.sk/en/private-equity-fund/ 6000 | sed -n '14,50p'
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
Hľadám investora
Private equity
Portfólio
V médiách
Kontakt
Slovenčina
English
×
Hľadám investora
Private equity
Portfólio
V médiách
Kontakt
Slovenčina
English
V médiách
Vízia firmy: Čo chcú private equity investori počuť na prvom stretnutí
V dynamickom svete podnikania môže byť stretnutie s private equity (PE) investorom zlomovým momentom,...
Čítať viac
Firemná kultúra má silu rozhodnúť o osude miliónových private equity investícií
Nespomína sa to často, ale firemná kultúra môže byť jedným z najväčších tvorcov, ale zároveň aj...
Čítať viac
Dr. Martin a Eterus Capital spája sily pre expanziu a rozvoj siete zubných kliník
Bratislava, 12. jún 2024 – Dr. Martin, popredná slovenská sieť moderných stomatologických kliník,...
Čítať viac
Život private equity investície: Prvé stretnutia, due diligence až po predaj firmy
Vo svete financií, kde rýchlosť a pružnosť rozhodovania môžu významne ovplyvniť úspech firmy,...
Čítať viac
Odliv mozgov a ekonomický rast. Private equity čakajú výzvy a príležitosti
Posledné roky sa s firmami na Slovensku a po celom svete skutočne nemaznali. Svetová ekonomika čelila...
Čítať viac
7 vecí, ktoré by ste mali vedieť o private equity
Zvažujete financovanie rozvoja vášho biznisu prostredníctom private equity? Prečítajte si, čo všetko...
Čítať viac
Každá firma potrebuje „diablovho advokáta“. Private equity kladie otázky, ktoré posúvajú biznis dopredu.
Boris Kostík. investičný riaditeľ Eterus Capital hovorí o dôležitej úlohe private equity v pozí
… [skrátené, 1567 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://eterus.sk/v-mediach/ | grep -oE "href=['\"]https://eterus.sk/20[^'\"]*['\"]" | sort -u | tail -15
```

<details><summary>Výstup nástroja</summary>

```
href="https://eterus.sk/2023/05/15/mtbiker-ziskal-silneho-partnera-eterus-capital-investuje-do-jeho-rozvoja/"
href="https://eterus.sk/2023/05/16/kostik-z-eterus-capital-pri-debate-s-firmami-sme-v-roli-diablovho-advokata/"
href="https://eterus.sk/2023/06/23/private-equity-prinasa-kapital-aj-know-how-pre-ktore-firmy-je-vhodne-2/"
href="https://eterus.sk/2023/06/26/financovanie-cez-private-equity/"
href="https://eterus.sk/2023/08/16/kapital-na-rozvoj-firmy-vyhody-private-equity-oproti-inym-formam-financovania/"
href="https://eterus.sk/2023/09/13/co-spaja-hopin-sanecu-a-mtbiker-kapital-a-know-how-cez-private-equity/"
href="https://eterus.sk/2023/09/22/private-equity-prinasa-stabilitu-a-know-how/"
href="https://eterus.sk/2023/10/24/co-je-to-private-equity/"
href="https://eterus.sk/2023/11/24/kazda-dobra-firma-potrebuje-diablovho-advokata/"
href="https://eterus.sk/2023/12/15/7-veci-ktore-by-ste-mali-vediet-o-private-equity/"
href="https://eterus.sk/2024/04/12/odliv-mozgov-a-ekonomicky-rast-private-equity-cakaju-vyzvy-a-prilezitosti/"
href="https://eterus.sk/2024/05/14/zivot-private-equity-investicie-prve-stretnutia-due-diligence-az-po-predaj-firmy/"
href="https://eterus.sk/2024/06/12/dr-martin-a-eterus-capital-spaja-sily-pre-expanziu-a-rozvoj-siete-zubnych-klinik/"
href="https://eterus.sk/2024/07/10/firemna-kultura-ma-silu-rozhodnut-o-osude-milionovych-private-equity-investicii/"
href="https://eterus.sk/2024/09/30/vizia-firmy-co-chcu-private-equity-investori-pocut-na-prvom-stretnut
… [skrátené, 1503 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://eterus.sk/2024/06/12/dr-martin-a-eterus-capital-spaja-sily-pre-expanziu-a-rozvoj-siete-zubnych-klinik/ 8000 | sed -n '/^Dr. Martin a Eterus/,$p' | head -20; python3 -I $S/page.py grep https://eterus.sk/2023/05/15/mtbiker-ziskal-silneho-partnera-eterus-capital-investuje-do-jeho-rozvoja/ 'Eterus'; python3 -I $S/page.py grep https://eterus.sk/portfolio/ 'pharm|lekár|Eterus'
```

<details><summary>Výstup nástroja</summary>

```
Dr. Martin a Eterus Capital spája sily pre expanziu a rozvoj siete zubných kliník – Eterus Capital
Skip to content
Hľadám investora
Private equity
Portfólio
V médiách
Kontakt
Slovenčina
English
×
Hľadám investora
Private equity
Portfólio
V médiách
Kontakt
Slovenčina
English
18. decembra 2025
Dr. Martin a Eterus Capital spája sily pre expanziu a rozvoj siete zubných kliník
Bratislava, 12. jún 2024 – Dr. Martin, popredná slovenská sieť moderných stomatologických kliník, dnes oznámila významnú investíciu od Eterus Capital a Ethernum Capital. Táto investícia podporí expanziu a ďalší rozvoj siete Dr. Martin, ktorý už teraz poskytuje komplexnú zubnú starostlivosť v štyroch lokalitách a v ďalších dvoch v príprave na západnom Slovensku.
- MTBIKER získal silného partnera. Eterus Capital investuje do jeho rozvoja – Eterus Capital
- MTBIKER získal silného partnera. Eterus Capital investuje do jeho rozvoja
- Jeden z najväčších a najnavštevovanejších cyklistických portálov v strednej Európe MTBIKER získal pre svoj ďalší rast silného partnera. Do spoločnosti vstupuje private equity fond Eterus Capital.
- „Transakcia bola jedna z tých komplikovanejších svojím rozsahom, ale podarilo sa nám nastaviť adekvátnu štruktúru. Z pohľadu externých rizík nebolo jednoduché realizovať obchod predovšetkým v kontexte budúceho vývoja e-commerce, dopadu vojny na Ukrajine a horšieho makroekonomického prostredia vplývajúceho na nákupné správanie zákazníkov,“ vysvetľuje Boris Kostík, investičný riaditeľ fondu 
… [skrátené, 2951 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Eterus Capital EC Pharmacies lekárne investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Eterus Capital EC Pharmacies lekárne investícia"

Links: [{"title":"Zu den Deals","url":"https://www.oaklins.com/at/de/deals/110584/"},{"title":"Transaktionen anzeigen","url":"https://oaklins.com/ch/de/deals/110584"},{"title":"Go to deals","url":"https://www.oaklins.com/ro/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/se/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/au/en/deals/110584/"},{"title":"Go to deals","url":"https://oaklins.com/co/en/deals/110584"},{"title":"Go to deals","url":"https://www.oaklins.com/dk/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/fi/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/bg/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/at/en/deals/110584/"}]

The search returned one source, an Oaklins deal page (it appears in several regional versions). It describes EC Pharmacies as a Slovak pharmacy consolidation vehicle and says nothing about current status or later deals.

- **Deal:** In August 2024, Eterus Capital took a majority stake in EC Pharmacies, which it set up with Ethernum Capital. August 2024 — Eterus Capital has acquired a majority stake in EC Pharmacies, a consolidation platform established in partnership with Ethernum Capital.
- **Purpose:** The vehicle is a joint venture meant to consolidate Slovakia's pharmacy market using a "buy-and-build" approach. EC Pharmacies is a joint
… [skrátené, 3183 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.oaklins.com/at/en/deals/110584/ 'Eterus|August|2024'
```

<details><summary>Výstup nástroja</summary>

```
- Eterus Capital and Ethernum Capital have partnered to consolidate the Slovak pharmacy market | Deals | Oaklins Austria: Mid-market M&A and financial advice globally
- Eterus Capital and Ethernum Capital have partnered to consolidate the Slovak pharmacy market
- August 2024 — Eterus Capital has acquired a majority stake in EC Pharmacies, a consolidation platform established in partnership with Ethernum Capital.
- Eterus Capital is a private equity fund founded in 2008, specializing in supporting small and medium-sized enterprises with proven business models and growth potential. The fund focuses on minority investments, ensuring management control remains with the original shareholders. Over the years, Eterus Capital has provided more than US$41 million (€40 million) in funding to over 20 companies. Its portfolio includes prominent brands such as Sygic, HOPIN, eyerim, Saneca Pharmaceuticals, Groupsolver and MTBIKER.
- EC Pharmacies is a joint venture between Eterus Capital and Ethernum Capital, established to consolidate the Slovak pharmacy market through a "buy-and-build" strategy. The objective is to acquire 25–50 targeted pharmacies, improve operational performance, centralize marketing and supply chains and ultimately sell the established network to a strategic partner. Since its inception, EC Pharmacies has acquired nine pharmacies with an estimated annual portfolio revenue of US$6.2 million (€6 million). The company plans to expand its network by launching and acquirin
… [skrátené, 1586 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c004.json <<'EOF'
{
  "candidate_id": "c004",
  "name": "Eterus Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.eterus.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Sme kapitálovým fondom investujúcim do akcií a iných nástrojov vlastného imania spoločností s domicilom na Slovensku. Neponúkame dlhové financovanie."},
  "investor_type": {"value": "pe", "source_url": "https://www.oaklins.com/at/en/deals/110584/", "source_date": null, "quote": "Eterus Capital is a private equity fund founded in 2008, specializing in supporting small and medium-sized enterprises with proven business models and growth potential."},
  "sectors": null,
  "stages": {"value": ["growth"], "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Eterus je partner pre financovanie spoločností vo fáze rastu, so schopným managementom a overeným konceptom."},
  "ticket_min": {"amount": 2000000, "currency": "EUR", "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Zameriavame sa na investície v rozmedzí 2 - 2,5 mil. EUR, pričom preferovaná dĺžka investície predstavuje 5-7 rokov."},
  "ticket_max": {"amount": 2500000, "currency": "EUR", "source_url": "https://www.eterus.sk/", "source_date": null, "quote": "Zameriavame sa na investície v rozmedzí 2 - 2,5 mil. EUR, pričom preferovaná dĺžka investície pr
… [skrátené, 3301 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c004.json
c004.json entity_kind OK
c004.json investor_type OK
c004.json stages OK
c004.json ticket_min OK
c004.json ticket_max OK
c004.json inv:EC Pharmacies OK
c004.json inv:Dr. Martin OK
c004.json inv:MTBIKER OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0" https://www.fondfit.sk/ | grep -oE "href=['\"]https://www.fondfit.sk[^'\"]*['\"]" | sort -u; 
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.fondfit.sk/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'wp-|css|json|xml' | head -30
```

<details><summary>Výstup nástroja</summary>

```
href='#'
href='//cdn.datatables.net'
href='//fonts.googleapis.com'
href="//gmpg.org/xfn/11"
href="https://cookiedatabase.org/tcf/purposes/"
href='https://fonts.gstatic.com'
href="https://www.fondfit.sk/"
href="https://www.fondfit.sk/index.php/analytic-solutions/"
href="https://www.fondfit.sk/index.php/comments/feed/"
href="https://www.fondfit.sk/index.php/feed/"
href="https://www.fondfit.sk/index.php/financovanie-kapitalu/"
href="https://www.fondfit.sk/index.php/investicny-proces/"
href="https://www.fondfit.sk/index.php/kontakt/"
href="https://www.fondfit.sk/index.php/mentoring/"
href="https://www.fondfit.sk/index.php/o-nas/"
href="https://www.fondfit.sk/index.php/our-team/"
href="https://www.fondfit.sk/index.php/portfolio/b2b-lead-generation/"
href="https://www.fondfit.sk/index.php/portfolio/brand-loyalty-built/"
href="https://www.fondfit.sk/index.php/portfolio-category/it-technology/"
href="https://www.fondfit.sk/index.php/portfolio-category/technologie/"
href="https://www.fondfit.sk/index.php/portfolio-category/vyroba/"
href="https://www.fondfit.sk/index.php/portfolio/elearn-aero/"
href="https://www.fondfit.sk/index.php/portfolio-podporenych-projektov/"
href="https://www.fondfit.sk/index.php/portfolio/uctovnictvo/"
href="https://www.fondfit.sk/index.php/portfolio/umela-inteligencia/"
href="https://www.fondfit.sk/index.php/sba/"
href="https://www.fondfit.sk/index.php/sluzby/analytic-solutions/"
href="https://www.fondfit.sk/index.php/sluzby/financovanie-kapitalu/"
href="http
… [skrátené, 1624 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in o-nas/ sba/ sluzby/financovanie-kapitalu/ portfolio-podporenych-projektov/; do echo "=== $p"; python3 -I $S/page.py show https://www.fondfit.sk/index.php/$p 8000 | sed -n '/^Hľadať:/,$p' | sed -n '30,70p'; done
```

<details><summary>Výstup nástroja</summary>

```
=== o-nas/
Služby
Financovanie kapitálu
Mentoring
Analýza zámeru
Vyhlásenie o udržateľnosti
Kontaktné údaje
Fond inovácií a technológií, a.s.
Trnavská cesta 100, 821 01 Bratislava
[email]
Zásady spracúvania osobných údajov SK
Zásady spracúvania osobných údajov (SK)
Information on personal data processing (EN)
© 2024 Všetky práva vyhradené. Fond inovácií a technológií, a.s. zastrešuje Slovak Business Agency.
Zásady používania súborov cookie (EÚ)
Spravovať Súhlas
Na poskytovanie tých najlepších skúseností používame technológie, ako sú súbory cookie na ukladanie a/alebo prístup k informáciám o zariadení. Súhlas s týmito technológiami nám umožní spracovávať údaje, ako je správanie pri prehliadaní alebo jedinečné ID na tejto stránke. Nesúhlas alebo odvolanie súhlasu môže nepriaznivo ovplyvniť určité vlastnosti a funkcie.
Funkčné Funkčné Vždy aktívny
Technické uloženie alebo prístup sú nevyhnutne potrebné na legitímny účel umožnenia použitia konkrétnej služby, ktorú si účastník alebo používateľ výslovne vyžiadal, alebo na jediný účel vykonania prenosu komunikácie cez elektronickú komunikačnú sieť. Predvoľby Predvoľby
Technické uloženie alebo prístup je potrebný na legitímny účel ukladania preferencií, ktoré si účastník alebo používateľ nepožaduje. Štatistiky Štatistiky
Technické úložisko alebo prístup, ktorý sa používa výlučne na štatistické účely. Technické úložisko alebo prístup, ktorý sa používa výlučne na anonymné štatistické účely. Bez predvolania, dobrovoľného plnenia
… [skrátené, 11237 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.podnikajte.sk/investor/fit-fond-financovanie 'štát|akcion|Datamolino|investuje|20 000|FIT|Publikované|[0-9]{2}\.[0-9]{2}\.20[0-9]{2}' | head -30; python3 -I $S/page.py grep "https://www.startitup.sk/?p=12849" 'FIT|Fond inov|Bitmap|Joint|Investeers' | head
```

<details><summary>Výstup nástroja</summary>

```
- FIT vám pomôže zafinancovať inovatívne podnikateľské nápady | Podnikajte.sk
- - Krása a fitness
- FIT vám pomôže zafinancovať inovatívne podnikateľské nápady
- Prvou investíciou Fondu inovácií a technológií je startup Datamolino. FIT doň investoval 500 000 eur. Ak dokážete, že váš biznis má skutočný potenciál a inovatívnu myšlienku FIT môže byť pre vás dobrým partnerom pre biznis.
- Financovanie začínajúcich inovatívnych projektov je dnes často pretriasanou témou. Ich podporou sa rozvíja nielen ekonomika, ale nové podnikateľské nápady pomáhajú iným často krát uľahčiť život. Jeden z fondov, ktorý podporuje takéto podniky je aj FIT (Fond inovácií a technológií), ktorý vznikol spojením štátu ako majoritného akcionára a súkromného investora. Jeho poslaním je formou venture kapitálu podporovať a rozvíjať podnikanie, zamestnanosť a inovatívnu ekonomiku. Fond poskytuje investície od 20 000 do 1 500 000 eur, no mladým podnikateľom ponúka okrem kapitálu aj mentoring. Zaujímalo nás ako vidí stav inovatívneho podnikania a jeho financovania na Slovensku Rastislav Roško, podpredseda
- Poslaním FIT fondu je podporiť projekty prispievajúce k tvorbe inovatívnej ekonomiky. Koľko projektov ste posudzovali od vzniku fondu?
- Myslím si, že základom úspechu väčšiny mladých spoločností je silný tím, ktorí vie spolupracovať a sedí si po odbornej aj ľudskej stránke. Ale na druhej strane, je to aj častý dôvod, prečo sú spoločnosti odmietnuté na financovanie. Investor už v začiatkoch investuje do ľu
… [skrátené, 6665 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp; for u in "https://www.startitup.sk/?p=12849" https://www.podnikajte.sk/investor/fit-fond-financovanie; do curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" "$u" | grep -oE '(datePublished|article:published_time)[^,>]{0,60}' | head -3; done
```

<details><summary>Výstup nástroja</summary>

```
article:published_time" content="2015-06-30T13:38:54+00:00" /
datePublished":"2015-06-30T13:38:54+00:00"
datePublished":"2015-06-30T13:38:54+00:00"
article:published_time" content="2014-09-22T22:00:00+02:00" /
datePublished": "2014-09-22T22:00:00+02:00"
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Fond inovácií a technológií\" investoval startup 2021 OR 2022 OR 2023 OR 2024", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Fond inovácií a technológií" investoval startup 2021 OR 2022 OR 2023 OR 2024"

Links: [{"title":"FIT vám pomôže zafinancovať inovatívne podnikateľské nápady","url":"https://www.podnikajte.sk/investor/fit-fond-financovanie"},{"title":"fondfit oznamuje dalsie investicie obe do hernehobiznisu","url":"https://www.startitup.sk/fondfit-oznamuje-dalsie-investicie-obe-do-hernehobiznisu/"},{"title":"www.startitup.sk","url":"https://www.startitup.sk/?p=12849"},{"title":"Nový DeepTech fond podpoří vysoce inovativní startupy. V první fázi půjde až o miliardu korun","url":"https://www.businessinfo.cz/clanky/novy-deeptech-fond-podpori-vysoce-inovativni-startupy-v-prvni-fazi-pujde-az-o-miliardu-korun/"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital?page=7"},{"title":"V Brně vznikl fond pro startupy, který bude investovat i peníze kraje","url":"https://www.lupa.cz/aktuality/v-brne-vznikl-fond-pro-startupy-ktery-bude-investovat-i-penize-kraje/"},{"title":"Sony otevírá investiční fond pro startupy. Celkem do nich vloží kolem 185 milionů dolarů","url":"https://cc.cz/sony-otevira-investicni-fond-pro-startupy-celkem-do-nich-vlozi-kolem-185-milionu-dolaru/"},{"title":"Nizozemsko posiluje podporu technologických startupů, ukazuje cestu i Česku","url":"https://www.businessinfo.cz/clanky/nizozemsko-posiluje-podporu-technologickych-startupu-ukazuje-cestu-i-cesku/"},{"title":"V Česku vytvoria nový fond 
… [skrátené, 2994 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c005.json <<'EOF'
{
  "candidate_id": "c005",
  "name": "Fond inovácií a technológií",
  "legal_name": "Fond inovácií a technológií, a.s.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.fondfit.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://www.fondfit.sk/index.php/sba/", "source_date": null, "quote": "Fond inovácií a technológií, a.s. vznikol ako reakcia na vznikajúci dopyt po rizikovom kapitáli na podporu podnikateľov s nápadmi. Je výsledkom spolupráce Slovak Business Agency (SBA) s investormi."},
  "investor_type": {"value": "public_fund", "source_url": "https://www.podnikajte.sk/investor/fit-fond-financovanie", "source_date": "2014-09-22", "quote": "Jeden z fondov, ktorý podporuje takéto podniky je aj FIT (Fond inovácií a technológií), ktorý vznikol spojením štátu ako majoritného akcionára a súkromného investora."},
  "sectors": {"value": ["environment", "renewable energy", "industrial innovation", "e-commerce", "it", "telecommunications", "software"], "source_url": "https://www.fondfit.sk/index.php/sluzby/financovanie-kapitalu/", "source_date": null, "quote": "Oblasti, ktorým venujeme osobitnú pozornosť sú životné prostredie, obnoviteľné zdroje energie, priemyselné inovácie, e-commerce, informačné technológie, telekomunikácie, technológie, ktoré zlepšia život alebo softvérové riešenia."},
  "stages": {"value": ["seed", "growth"], "source_url": "https://www.fondfit.sk/index
… [skrátené, 3770 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c005.json
c005.json entity_kind OK
c005.json investor_type OK
c005.json sectors OK
c005.json stages OK
c005.json ticket_min OK
c005.json ticket_max OK
c005.json inv:Bitmap Galaxy OK
c005.json inv:Joint Custody OK
c005.json inv:Datamolino OK
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.genesis.cz/en/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg' | head -40; S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://www.genesis.cz/en/ 5000 | sed -n '8,40p'
```

<details><summary>Výstup nástroja</summary>

```
href="/de/?do=changeLocale"
href="/?do=changeLocale"
href="/en/"
href="/en/about-genesis-capital"
href="/en/career"
href="/en/contacts"
href="/en/?do=changeLocale"
href="/en/growth-equity"
href="/en/private-equity"
href="/files/smernice_GDPR_2020.pdf"
href="/frontend/images/site.webmanifest"
href="mailto:[email]"
href="mailto:[email]"
href="/pl/?do=changeLocale"
EN
DE
PL
Private equity
Funds aimed at investments into small and medium sized companies in the Czech Republic, Slovakia, Poland, Hungary, Austria and Germany.
More information
Growth equity
Funds focused on investments into smaller and mid-size companies in the Czech Republic and Slovakia with a significant growth potential.
More information
Your browser does not support HTML5 video.
1999
Since 1999, we have been supporting the development of small and medium-sized enterprises with strong growth potential but limited financial resources.
We have supported the growth and development of over 90 companies, covering a range of diverse sectors and businesses. Many of the supported companies became the business leaders in their respective segments.
More about Genesis Capital
Our Funds
We follow clear investment criteria. We use capital of reputable institutional investors to add value to growing businesses.
Since our foundation in 1999, we have worked on seven private equity funds with a cumulative size of over 550 million euros, or 8 billion Czech crowns.
Private Equity Funds
At present, the investmen
… [skrátené, 2088 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Genesis Capital fond investice 2026 GPEF V získal podíl", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Genesis Capital fond investice 2026 GPEF V získal podíl"

Links: [{"title":"Genesis announces strong year of investment","url":"https://www.amcham.cz/member-news/genesis-announces-strong-year-investment"},{"title":"na pocatku bylo slovo a miliardy genesis capital spousti ambiciozni fond","url":"https://forbes.cz/na-pocatku-bylo-slovo-a-miliardy-genesis-capital-spousti-ambiciozni-fond/"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/genesis-capital-launches-225m-fund"},{"title":"sest miliard na investice genesis capital spustila svuj dosud nejvetsi private equity fond","url":"https://forbes.cz/sest-miliard-na-investice-genesis-capital-spustila-svuj-dosud-nejvetsi-private-equity-fond/"},{"title":"Skupina Genesis Capital spustila miliardový fond. Chystá investice do středoevropských firem","url":"https://www.e15.cz/byznys/finance-a-bankovnictvi/skupina-genesis-capital-spustila-miliardovy-fond-chysta-investice-do-stredoevropskych-firem-1383058"},{"title":"genesis capital","url":"https://realdeals.eu.com/articles/tags/genesis capital"},{"title":"Genesis Capital to launch a new private equity fund with a target size of EUR 250 million","url":"https://psik.org.pl/en/research-and-reports/market-information/genesis-capital-to-launch-a-new-private-equity-fund-with-a-target-size-of-eur-250-million"},{"title":"Brozura KB PEF6","url":"https://www.amundi-kb.cz/storage/app/media/Brozura/Brozura-KB-PEF6.pdf"},{"title":"Predict your next in
… [skrátené, 5547 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.amcham.cz/member-news/genesis-announces-strong-year-investment 'Genesis|acqui|invest' | head -30; for u in https://forbes.cz/investice-do-trutnovskeho-prumyslu-genesis-capital-koupil-podil-firmy-kasper-kovo/ https://forbes.cz/akvizice-z-oceli-rodinny-vyrobce-obrabenych-sestav-miri-pod-genesis-capital/; do echo "== $u"; python3 -I $S/page.py grep $u 'Genesis' | head -6; curl -sL -A "Mozilla/5.0" $u | grep -oE 'datePublished"?[^,]{0,40}' | head -2; done
```

<details><summary>Výstup nástroja</summary>

```
- Genesis announces strong year of investment | American Chamber of Commerce in the Czech Republic
- Genesis announces strong year of investment
- Genesis announces strong year of investment
- Genesis Capital is approaching a year since it successfully launched Genesis Private Equity Fund V (GPEF V), its largest fund to date, with the current size of EUR 286 million and expected final size potentially exceeding EUR 300 million. GPEF V has been successful in deployment of capital and the investment pace, currently approaching 25% deployment.
- In addition, the predecessor fund GPEF IV is invested in 12 active portfolio investments and still has the time of further five years for growth including by way of add-on acquisitions and utilisation of market consolidation potential.
- The funds primarily target investments with equity tickets ranging between EUR 10 million and EUR 45 million but remain interested and actively evaluate also smaller investment opportunities (below EUR 10 million equity ticket) in the context of add-on acquisitions and buy-and-build strategies.
- Genesis Capital therefore remains interested in and active across a wide range of investment opportunities of varying sizes. This is not affected by Genesis Capital’s recent decision not to replicate for a successor fund the co-operation with a separate team established in connection with Genesis Growth Equity Fund I (GGEF I), which covered the lower mid-market SME segment. While operations of GGEF I remain unch
… [skrátené, 4531 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Genesis Capital Slevomat majoritní podíl", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Genesis Capital Slevomat majoritní podíl"

Links: [{"title":"Slevomat po sedmi letech mění majitele. Většinu kupuje Genesis Capital, firma se vrací do českých rukou","url":"https://www.e15.cz/byznys/slevomat-po-sedmi-letech-meni-majitele-vetsinu-kupuje-genesis-capital-firma-se-vraci-do-ceskych-rukou-1428906"},{"title":"Slevomat od Britů kupuje elitní fond, přidávají se manažeři firmy a jedna z nejbohatších Češek","url":"https://cc.cz/slevomat-od-britu-kupuje-elitni-fond-pridavaji-se-manazeri-firmy-a-jedna-z-nejbohatsich-cesek/"},{"title":"Středa 05. srpna 2026 11:26","url":"https://www.fxstreet.cz/klicova-slova+genesis.html"},{"title":"Hlavní obsah","url":"https://www.novinky.cz/clanek/ekonomika-vetsinu-slevomatu-budou-opet-vlastnit-cesi-40549437"},{"title":"Obľúbený zľavový portál mení majiteľa. Na trhu sa schyľuje k veľkým zmenám","url":"https://www.startitup.sk/?p=1145510"},{"title":"„Zpátky do českých rukou“. Slevomat má nového majitele, většinu v něm koupil Genesis Capital","url":"https://www.lupa.cz/aktuality/zpatky-do-ceskych-rukou-slevomat-ma-noveho-majitele-vetsinu-v-nem-koupil-genesis-capital/"},{"title":"Středa 26. srpna 2026 01:48","url":"https://www.fxstreet.cz/klicova-slova+gpef.html"},{"title":"Pondělí 21. září 2026 05:19","url":"https://www.fxstreet.cz/klicova-slova+cupr.html"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/genesis-capital-acquires-majority-in-slevomat"}]

Genesis Capital agreed in November 2
… [skrátené, 3139 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.lupa.cz/aktuality/zpatky-do-ceskych-rukou-slevomat-ma-noveho-majitele-vetsinu-v-nem-koupil-genesis-capital/ 'Genesis|listopad|2025' | head -8; echo ===; python3 -I $S/page.py grep https://www.fxstreet.cz/klicova-slova+gpef.html 'Genesis|GPEF' | head -20
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
- „Zpátky do českých rukou“. Slevomat má nového majitele, většinu v něm koupil Genesis Capital - Lupa.cz
- „Zpátky do českých rukou“. Slevomat má nového majitele, většinu v něm koupil Genesis Capital
- 19. 11. 2025
- Většina ve skupině Slevomat přešla do rukou Genesis Capital, skupiny fondů, za níž jako investoři stojí mimo jiné Česká spořitelna, členové Erste Group, Tatra Banka, SPM Capital nebo Naše Česko (fond skupiny J&T). Pro Genesis Capital představuje tato transakce první podepsanou investici nejnovějšího fondu Genesis Private Equity Fund V (GPEF V) o aktuální velikosti 270 milionů eur. Stávající management Slevomatu se investice také účastnil a bude i nadále řídit skupinu. Na investici se podílí také family office Jitky Cechlové Komárkové.
- „Osobně mám velkou radost z toho, že se skupina Slevomat, kterou založil český podnikatel Tomáš Čupr, vrací do českých rukou. Už při našem prvním setkání s kolegy z Genesis jsem cítil, že si vzájemně velmi sedíme,“ říká Tomáš Braverman, CEO Slevomatu. Podle něj na exitu tým pracoval skoro rok. Nyní je vizí umělá inteligence a „app first“ přístup.
- „Skupina Slevomat je silná a dobře řízená společnost s vedoucím postavením na českém a slovenském trhu. Dlouhodobě roste a dokazuje, že si umí udržet svou pozici i v silně konkurenčním online prostředí,“ doplňuje ho Tomáš Sýkora, Investment Director v Genesis Capital Equity. Věří, že se bude tržní pozice značky dál posilovat.
- Genesis Capital funguje od roku 1999 a je to sk
… [skrátené, 1849 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Genesis Capital\" akvizice 2026 fond GPEF V druhá investice", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Genesis Capital" akvizice 2026 fond GPEF V druhá investice"

Links: [{"title":"Genesis announces strong year of investment","url":"https://www.amcham.cz/member-news/genesis-announces-strong-year-investment"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/genesis-capital-launches-225m-fund"},{"title":"genesis capital","url":"https://realdeals.eu.com/articles/tags/genesis capital"},{"title":"Skupina Genesis Capital spustila miliardový fond. Chystá investice do středoevropských firem","url":"https://www.e15.cz/byznys/finance-a-bankovnictvi/skupina-genesis-capital-spustila-miliardovy-fond-chysta-investice-do-stredoevropskych-firem-1383058"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/genesis-capital-sro"},{"title":"Genesis Capital to launch a new private equity fund with a target size of EUR 250 million","url":"https://psik.org.pl/en/research-and-reports/market-information/genesis-capital-to-launch-a-new-private-equity-fund-with-a-target-size-of-eur-250-million"},{"title":"sest miliard na investice genesis capital spustila svuj dosud nejvetsi private equity fond","url":"https://forbes.cz/sest-miliard-na-investice-genesis-capital-spustila-svuj-dosud-nejvetsi-private-equity-fond/"},{"title":"GENESIS CAPITAL: Pomáhají firmám růst","url":"https://www.ceskenoviny.cz/zpravy/1819664"},{"title":"GENESIS CAPITAL: Pomáhají firmám růst","url":"https://www.ceskenoviny.cz/zpravy/genesis-capital-pomahaj
… [skrátené, 3304 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://www.genesis.cz/en/private-equity 5000 | sed -n '8,40p'; curl -sL -A "Mozilla/5.0" https://www.amcham.cz/member-news/genesis-announces-strong-year-investment | grep -oE '(datePublished|published_time|date)[^<]{0,60}' | head -5; python3 -I $S/page.py grep https://www.amcham.cz/member-news/genesis-announces-strong-year-investment '2026|Posted|June'
```

<details><summary>Výstup nástroja</summary>

```
DE
PL
About GPEF
Our team
Investment with Us
Our Funds
Our Portfolio
Responsible investing
News
Genesis Capital exits GTH Catering, marking the end of a successful investment partnership of more than fifteen years
More information
Genesis Capital signed an agreement to invest in POS Media Europe, the leading company in retail media solutions with a strong footprint across Central Europe
More information
Genesis Capital signed an agreement to acquire a majority stake in Fyzioterapie s úsměvem, one of the leading private providers of outpatient rehabilitation services in the Czech Republic
More information
Genesis Capital expands its regional reach to Germany bringing long-term colleague Jörgen Hausberger on board as Partner
More information
6
investment funds
EUR 500 mil.
for companies
80
investments
About GPEF
Investing with GC
Our Funds
Our Investments
We are a member of
News
30.06.2026
Genesis Capital exits GTH Catering, marking the end of a successful investment partnership of more than fifteen years
Genesis Private Equity Fund III, a fund from the private equity group Genesis Capital, exited its majority stake in GTH Catering to the Company's other current shareholders, concluding a successful investment partnership spanning over more than fifteen years. During this period, GTH Catering has grown into the largest provider of corporate catering services in the Czech Republic.
13.04.2026
date field--type-ds field--label-hidden field--item">10 Jun 2026
date, with the current
… [skrátené, 1556 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://www.genesis.cz/en/private-equity 12000 | sed -n '/^30.06.2026/,$p' | head -30; curl -sL -A "Mozilla/5.0" https://www.genesis.cz/en/private-equity | grep -oE "href=['\"][^'\"]*['\"]" | grep -i news | sort -u | head
```

<details><summary>Výstup nástroja</summary>

```
30.06.2026
Genesis Capital exits GTH Catering, marking the end of a successful investment partnership of more than fifteen years
Genesis Private Equity Fund III, a fund from the private equity group Genesis Capital, exited its majority stake in GTH Catering to the Company's other current shareholders, concluding a successful investment partnership spanning over more than fifteen years. During this period, GTH Catering has grown into the largest provider of corporate catering services in the Czech Republic.
13.04.2026
Genesis Capital signed an agreement to invest in POS Media Europe, the leading company in retail media solutions with a strong footprint across Central Europe
POS Media Europe is an established provider of retail media solutions across Europe. Since its founding in 1998, the company has grown into a recognized partner for major retail chains and FMCG brands, offering a broad portfolio of retail media solutions. Genesis Private Equity Fund V (GPEF V), a private equity fund from the Genesis Capital group, has agreed to invest in POS Media Europe with the aim of supporting its further development and strengthening its position in European markets. Following completion, Mr. Richard van het Bolscher, the founder and CEO, will remain the majority owner, while GPEF V will hold a significant minority stake alongside the management team. Completion of the transaction is subject to approval by the relevant competition authorities.
08.04.2026
Genesis Capital Newsletter 4/20
… [skrátené, 3306 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c006.json <<'EOF'
{
  "candidate_id": "c006",
  "name": "Genesis Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK", "PL", "HU", "AT", "DE"],
  "website": "https://www.genesis.cz/en/",
  "entity_kind": {"value": "investor", "source_url": "https://www.genesis.cz/en/private-equity", "source_date": "2026-02-04", "quote": "Genesis Capital, one of the leading private equity firms in Central Europe, announces the expansion of its investment activities into Germany and the strengthening of its partnership through the appointment of Jörgen Hausberger as Partner."},
  "investor_type": {"value": "pe", "source_url": "https://www.lupa.cz/aktuality/zpatky-do-ceskych-rukou-slevomat-ma-noveho-majitele-vetsinu-v-nem-koupil-genesis-capital/", "source_date": "2025-11-19", "quote": "Genesis Capital funguje od roku 1999 a je to skupina fondů private equity, které poskytují malým a středním podnikům ve střední Evropě financování jejich dalšího růstu a rozvoje."},
  "sectors": null,
  "stages": null,
  "ticket_min": {"amount": 10000000, "currency": "EUR", "source_url": "https://www.amcham.cz/member-news/genesis-announces-strong-year-investment", "source_date": "2026-06-10", "quote": "The funds primarily target investments with equity tickets ranging between EUR 10 million and EUR 45 million"},
  "ticket_max": {"amount": 45000000, "currency": "EUR", "source_url": "https://www.amcham.cz/member-news/genesis-announces-
… [skrátené, 4177 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c006.json
c006.json entity_kind OK
c006.json investor_type OK
c006.json ticket_min OK
c006.json ticket_max OK
c006.json aum OK
c006.json inv:POS Media Europe OK
c006.json inv:Fyzioterapie s úsměvem OK
c006.json inv:Slevomat Group OK
```

</details>

**Nástroj `Bash`**

```bash
python3 - <<'EOF'
import json
p="research/c006.json"; d=json.load(open(p))
d["investments"][2]["quote"]="Většina ve skupině Slevomat přešla do rukou Genesis Capital, skupiny fondů, za níž jako investoři stojí mimo jiné Česká spořitelna, členové Erste Group, Tatra Banka, SPM Capital nebo Naše Česko (fond skupiny J&T)."
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c006.json && python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c006.json | grep Slevomat
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c006.json
c006.json inv:Slevomat Group OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.jetinvestment.cz/en/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg|\.svg' | head -50; python3 -I $S/page.py show https://www.jetinvestment.cz/en/ 5000 | sed -n '8,50p'
```

<details><summary>Výstup nástroja</summary>

```
href="/"
href="/en"
href="/en/about-us"
href="/en/about-us/our-team"
href="/en/career"
href="/en/contact"
href="/en/cookie-settings"
href="/en/important-notices"
href="/en/news"
href="/en/news/czech-funds-poland-investment-banks"
href="/en/news/czech-vc-funds-free-riders-levinsky"
href="/en/news/jet-investment-announces-eu2-1-million-investment-in-berlin-ai-startup-phantasma-labs"
href="/en/news/jet-investment-announces-usd-750-000-investment-in-us-ai-startup-hermetiqq"
href="/en/news/jet-investment-decisionrules"
href="/en/news/jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol"
href="/en/news/jet-investment-invests-eu2-1-million-in-swedish-deep-tech-company-gigascan"
href="/en/news/jet-investment-vstupuje-do-americkeho-startupu-appnava-ktery-pomoci-ai-predpovida-chovani-uzivatelu"
href="/en/news/why-sell-perfect-company-private-equity"
href="/en/partnering"
href="/en/privacy-policy"
href="/en/private-equity"
href="/en/real-estate"
href="/en/regulatory-informations"
href="/en/sustainability"
href="/en/venture-capital"
href="/en/whistleblowing"
href="https://cdn.prod.website-files.com"
href="https://jetwebportal.azurewebsites.net/"
href="https://www.instagram.com/jet.investment/"
href="https://www.jetinvestment.cz/"
href="https://www.jetinvestment.cz/en"
href="https://www.jetinvestment.cz/pl"
href="https://www.jetinvestment.eu/"
href="https://www.jetinvestment.pl/"
href="https://www.linkedin.com/company/jet-investment/"
href="https://www.optimio.cz/"
hre
… [skrátené, 3329 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in private-equity venture-capital; do echo "=== $p"; python3 -I $S/page.py show https://www.jetinvestment.cz/en/$p 6000 | sed -n '/^PL$/,$p' | sed -n '2,30p'; done; for p in jet-investment-vstupuje-do-americkeho-startupu-appnava-ktery-pomoci-ai-predpovida-chovani-uzivatelu jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol jet-investment-announces-eu2-1-million-investment-in-berlin-ai-startup-phantasma-labs; do echo "=== $p"; python3 -I $S/page.py grep https://www.jetinvestment.cz/en/news/$p 'Jet' | head -5; done
```

<details><summary>Výstup nástroja</summary>

```
=== private-equity
Private Equity
We help the new generation of European industry leaders succeed. We build thriving businesses that bring cutting-edge products to market.
Fund currently open for investment
Jet 4
More about the fund
Chci zjistit více
Individual and institutional investors participate with us in the building and growth of Central European industry through Jet private equity funds.
€530m+
AUM
private equity funds
(including co-investors)
35+
projects in 25+ years
20+ %
p.a.
internal rate of return since 1998
Funds
Private Equity
1997-2015
Family Office
Family Office
Learn more
€ 135m of invested capital
2015
Jet 1
Jet 1
Learn more
€ 135m of invested capital
€ 165m of invested capital
=== venture-capital
Venture Capital
We prepare European business for the future. We support Central European technology start-ups that can transform entire industries.
Fund currently open for investment
Jet Venture 1
More about the fund
Chci zjistit více
Thanks to venture capital funds, investors become part of the transformation of European industry and directly participate in the creation of innovative leaders of the future.
€50m.
target size of Jet Venture 1 fund
20%
p. a.
target return of the Jet Venture 1 fund
16-20
target number
of projects in the Jet Venture fund 1
Funds
Venture Capital
Fund currently open for investment
2024
Jet Venture 1
target amount €50 million
Fund currently open for investment
Learn more
Fund currently open for investment
Jet Venture 1
I want to learn 
… [skrátené, 5583 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.jetinvestment.cz/en/about-us '700|AUM|manage|billion|Slovak'; python3 -I $S/page.py grep https://www.jetinvestment.cz/en/contact 'ID|IČ|a\.s\.|s\.r\.o|SE'
```

<details><summary>Výstup nástroja</summary>

```
- Strength grows from partnership. We are a meeting point for investors, experts, owners, and top company managers. Here, opportunities, expertise, and capital come together in ways that would not intersect elsewhere.
- 420 724 357 700
- Igor founded Jet Investment in 1997 and, together with three other partners, he is still the head of the investment company. As a member of the investment committees, he is responsible for the management and control of the investments of all Jet funds and, as a member of the boards of directors, supervisory boards or boards of executives, he also oversees the strategic development of portfolio companies.
- Marek joined Jet Investment in 2010 and has been involved in the strategic development of the investment company as a partner since 2013. He is an active member of the investment committees of Jet funds and, as a member of the boards of directors of portfolio companies, sets their long-term strategy. In the past, he sought out acquisitions, successfully managed portfolio companies and their exits.
- Libor was involved in founding Jet Investment in 1997 and has continuously participated in the management of a number of projects, including real estate, and has actively worked to strengthen synergistic effects between projects. In addition to membership in the investment committees of Jet funds, he is currently primarily involved in fundraising and relations with individual and institutional investors.
- Elisabeta manages marketing and PR for 
… [skrátené, 3669 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in jet-investment-vstupuje-do-americkeho-startupu-appnava-ktery-pomoci-ai-predpovida-chovani-uzivatelu jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol; do python3 -I $S/page.py grep https://www.jetinvestment.cz/en/news/$p 'About Jet|AUM|billion|million euro|EUR|CZK|€|portfolio' | head -8; done
```

<details><summary>Výstup nástroja</summary>

```
- Founded in 2022, AppNava has grown into an international company serving studios developing mobile apps and games across Europe, Asia, and the U.S. Its hybrid machine-learning-based platform provides predictions at the individual-user level – lifetime value, churn, and monetization – with high accuracy; it integrates with leading analytics and advertising platforms within minutes and continuously retrains itself as user behavior changes. The company has demonstrated strong customer retention and healthy unit economics, along with 120% year-over-year growth in the number of customers. Its platform is validated by partnerships with leading advertising and analytics platforms, including Meta an
- The transaction aligns with Jet Investment’s strategy to expand its venture capital portfolio with innovative technology companies. The investment in AppNava follows previous investments in Digicust, Partory, International Automotive Group, Cequence, Boost.space, Headmade Materials, DecisionRules, Hermetiq, GigaScan and Phantasma Labs.
- The equity investment in AppNava is the next step in Jet Investment’s venture capital activities, for which the group established a new fund, Jet Venture 1, in October 2024. Jet Investment aims to build the Jet Venture 1 fund’s portfolio through equity investments in innovative early-stage companies in the Czech Republic and other Central European countries, totaling up to 50 million EUR. The Czech Republic and the broader region are among AppNava’s k
… [skrátené, 4317 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c007.json <<'EOF'
{
  "candidate_id": "c007",
  "name": "Jet Investment",
  "legal_name": "Jet Investment, a.s.",
  "reg_no": "03890333",
  "country": "CZ",
  "active_in": ["CZ", "SK", "AT", "DE", "PL"],
  "website": "https://www.jetinvestment.cz/en",
  "entity_kind": {"value": "investor", "source_url": "https://www.jetinvestment.cz/en/news/jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol", "source_date": "2026-09-11", "quote": "Jet Investment’s private equity funds invest in medium-sized industrial companies in Central Europe with strong growth potential."},
  "investor_type": {"value": "pe", "source_url": "https://www.slovca.sk/sk/riadni-clenovia/jet-investment.html", "source_date": null, "quote": "Typ fondu: Private Equity"},
  "sectors": {"value": ["industrial"], "source_url": "https://www.jetinvestment.cz/en/news/jet-investment-expands-nas-chleb-with-ostrava-based-bakery-pekari-a-spol", "source_date": "2026-09-11", "quote": "Jet Investment a.s., a Czech investment company founded in 1997, specializes in investments in Central European industry."},
  "stages": null,
  "ticket_min": {"amount": 15000000, "currency": "EUR", "source_url": "https://www.slovca.sk/sk/riadni-clenovia/jet-investment.html", "source_date": null, "quote": "Preferovaná výška jednej investície: min. 15 mil. EUR equity, max. 50 mil. EUR equity investícia"},
  "ticket_max": {"amount": 50000000, "currency": "EUR", "source_url": "https://www.sl
… [skrátené, 4082 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c007.json
c007.json entity_kind OK
c007.json investor_type OK
c007.json sectors OK
c007.json ticket_min OK
c007.json ticket_max OK
c007.json aum OK
c007.json inv:AppNava OK
c007.json inv:PEKAŘI a spol. OK
c007.json inv:Phantasma Labs MISSING
```

</details>

**Nástroj `Bash`**

```bash
sed -i 's/The Jet Investment has made its eleventh investment through the Jet Venture 1 SICAV/The Jet Investment has made its tenth investment through the Jet Venture 1 SICAV/' research/c007.json && PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c007.json && python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c007.json | grep Phant
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c007.json
c007.json inv:Phantasma Labs OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.nhfond.sk/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg|\.svg' | head -50; python3 -I $S/page.py show https://www.nhfond.sk/ 8000 | sed -n '16,60p'
```

<details><summary>Výstup nástroja</summary>

```
href="/clanky/"
href="/cookies"
href="/favicon.ico"
href="FondLink3"
href="/fondy-rizikoveho-kapitalu/"
href="/fondy-rizikoveho-kapitalu/eterus/podmienky-poskytnutia/"
href="/fondy-rizikoveho-kapitalu/fond-inovacii-a-technologii/podmienky-poskytnutia/"
href="fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/"
href="https://www.nhfond.sk/"
href="https://www.npc.sk/sk/mikropozickovy-program"
href="http://www.nhfond.sk"
href="http://www.sbagency.sk/erasmus-podnikatelia#.XAZSoWhKhPa"
href="http://www.sbagency.sk/kalendar-udalosti"
href="mailto:[email]"
href="/mikropozicky/dokumenty-na-stiahnutie/"
href="/mikropozicky/faq/"
href="/mikropozicky/mikropozicky/"
href="/mikropozicky/podmienky-poskytnutia-uveru/"
href="/mikropozicky/postup-poskytnutia-uveru/"
href="/mikropozicky/pripadova-studia-mikropozicky/"
href="/o-nas/historia-a-poslanie-spolocnosti/"
href="/o-nas/kontakt/"
href="/o-nas/nas-tim/"
href="/o-nas/sbagency/"
href="/o-nas/slovca/"
href="/Podpora-MSP/co-je-rizikovy-kapital/"
href="/Podpora-MSP/legislativa-slovenskej-republiky/"
href="/Podpora-MSP/novinky-o-financiach/"
href="/Podpora-MSP/podpora-msp-na-slovensku/"
href="/Podpora-MSP/slovnik-investora/"
href="/verejne-obstaravania/"
Zobraziť
Eterus Capital
Eterus Capital je partnerom pre financovanie podnikateľa vo fáze rastu.
Cieľom Eterus Capital je identifikácia zaujímavých rastových projektov/spoločností, následná realizácia investície a exit pri požadovanej návratnosti vložený
… [skrátené, 3237 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in o-nas/historia-a-poslanie-spolocnosti/ fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/ fondy-rizikoveho-kapitalu/; do echo "=== $p"; python3 -I $S/page.py show https://www.nhfond.sk/$p 9000 | sed -n '/^Zobraziť$/,$p' | head -50 | grep -vE '^(Zobraziť|Podpora MSP|Mikropôžičky)$' ; done 2>&1 | head -120
```

<details><summary>Výstup nástroja</summary>

```
=== o-nas/historia-a-poslanie-spolocnosti/
=== fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/
=== fondy-rizikoveho-kapitalu/
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in o-nas/historia-a-poslanie-spolocnosti/ fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/; do echo "=== $p"; python3 -I $S/page.py show https://www.nhfond.sk/$p 9000 | awk 'length($0)>60' | head -30; done
```

<details><summary>Výstup nástroja</summary>

```
=== o-nas/historia-a-poslanie-spolocnosti/
Zakladateľom Národného holdingového fondu, s.r.o. (NHF, s.r.o.) je Slovak Business Agency. Spoločnosť NHF, s.r.o. (12/1994 – 04/2006 Seed Capital Company, s.r.o., 04/2006 - 03/2014 Fond fondov, s.r.o.) bola založená v roku 1994 za účelom spravovania Fondu štartovacieho kapitálu (FŠK).
Za obdobie svojej existencie spoločnosť poskytla finančné prostriedky viac než 140 firmám v celkovej hodnote 10 mil. EUR a investíciami pomohla vytvoriť viac než 1 000 pracovných miest.
V súčasnosti spoločnosť Národný holdingový fond s.r.o. spravuje dva fondy rizikového kapitálu so samostatnou právnou subjektivitou (Eterus Capital a.s. a Fond inovácií a technológií, a.s.).
Portfólio spravovaných fondov dotvára Mikropôžičkový fond, ktorého prostriedky sa poskytujú formou úverov malým a stredným podnikateľom. Viac informácií TU.
Spoločnosť je jedným zo zakladajúcich členov SLOVCA (Slovak Venture Capital & Private Equity Association).
rozumným usmerňovaním činnosti jednotlivých fondov stimulovať rozvoj sektora malých a stredných podnikov,
zhodnocovať objem finančných prostriedkov jednotlivých fondov,
dosiahnuté zisky používať na ďalšiu podporu malých a stredných podnikov.
poskytovanie odborných konzultácií žiadateľom o financovanie týkajúce sa predkladaných projektov,
poradenstvo firmám nachádzajúcim sa v portfóliu spoločnosti,
zabezpečenie spolufinancovania pre žiadateľov požadujúcich vyššiu finančnú čiastku ako je maximálna povolená hranica jednotlivých 
… [skrátené, 5785 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Národný holdingový fond\" investícia spoločnosť vklad 2023 OR 2024 OR 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Národný holdingový fond" investícia spoločnosť vklad 2023 OR 2024 OR 2025"

Links: [{"title":"Národní rozvojový fond vlády umožní investice v řádu desítek miliard korun","url":"https://www.businessinfo.cz/clanky/narodni-rozvojovy-fond-vlady-umozni-investice-v-radu-desitek-miliard-korun/"},{"title":"Národní rozvojový fond bude spravovat státní banka, na investice půjde až 35 miliard","url":"https://www.e15.cz/byznys/finance-a-bankovnictvi/narodni-rozvojovy-fond-bude-spravovat-statni-banka-na-investice-pujde-az-35-miliard-1360230"},{"title":"Ministr Havlíček: Peníze do národního fondu chtějí posílat kromě bank i jiné firmy","url":"https://www.businessinfo.cz/clanky/ministr-havlicek-penize-do-narodniho-fondu-chteji-posilat-krome-bank-i-jine-firmy/"},{"title":"Ministr Havlíček: Peníze do národního fondu chtějí posílat kromě bank i jiné firmy","url":"https://www.e15.cz/rozhovory/ministr-havlicek-penize-do-narodniho-fondu-chteji-posilat-krome-bank-i-jine-firmy-1360245"},{"title":"Stát spouští IPO fond 2025+ na podporu růstu MSP a rozvoje kapitálového trhu","url":"https://www.businessinfo.cz/clanky/stat-spousti-ipo-fond-2025-na-podporu-rustu-msp-a-rozvoje-kapitaloveho-trhu/"},{"title":"www.economy.gov.sk","url":"https://www.economy.gov.sk/uploads/files/gM8laDDP.pdf"},{"title":"26 Mar 2025 17:40","url":"https://interfax.com/newsroom/top-stories/110607/"},{"title":"25 Sep 2025 11:48","url":"https://interfax.com/newsroom/top-stories/113971/"},{"title":"N
… [skrátené, 2975 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c008.json <<'EOF'
{
  "candidate_id": "c008",
  "name": "Národný holdingový fond",
  "legal_name": "Národný holdingový fond, s.r.o.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.nhfond.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://www.nhfond.sk/", "source_date": null, "quote": "Podporuje rastovo orientované podnikateľské projekty formou poskytovania rizikového kapitálu (vkladu do základného imania spoločností)."},
  "investor_type": {"value": "public_fund", "source_url": "https://www.nhfond.sk/", "source_date": null, "quote": "Špecializovaná dcérska spoločnosť Slovak Business Agency, ktorá implementuje podporu formou rizikového kapitálu."},
  "sectors": {"value": ["industrial manufacturing", "manufacturing services", "tourism", "innovative companies", "business services"], "source_url": "https://www.nhfond.sk/fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/", "source_date": null, "quote": "priemyselná výroba, výrobné služby, aktívny cestovný ruch, inovatívne podniky, obchodné služby."},
  "stages": {"value": ["seed", "growth"], "source_url": "https://www.nhfond.sk/fondy-rizikoveho-kapitalu/narodny-holdingovy-fond/podmienky-poskytnutia-investicie/", "source_date": null, "quote": "počiatočné, štartovacie a rozvojové štádium / inovatívne projekty."},
  "ticket_min": {"amount": 200000, "currency": "EUR", "source_url": "https://www.slovca.sk/sk/
… [skrátené, 2799 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c008.json
c008.json entity_kind OK
c008.json investor_type OK
c008.json sectors OK
c008.json stages OK
c008.json ticket_min OK
c008.json ticket_max OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.neulogy.vc/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep neulogy | grep -vE 'wp-|css|\.js|feed' | head -40; python3 -I $S/page.py show https://www.neulogy.vc/ 9000 | awk 'length($0)>50' | head -30
```

<details><summary>Výstup nástroja</summary>

```
href="https://dashboard.neulogy.vc/"
href="https://neulogy.vc"
href="https://neulogy.vc/about-us/"
href="https://neulogy.vc/careers/"
href="https://neulogy.vc/contact/"
href="https://neulogy.vc/portfolio/"
href="https://neulogy.vc/portfolio/anvesana/"
href="https://neulogy.vc/portfolio/beit/"
href="https://neulogy.vc/portfolio/biteberry/"
href="https://neulogy.vc/portfolio/diagnose-me/"
href="https://neulogy.vc/portfolio/excalibur/"
href="https://neulogy.vc/portfolio/eyerim/"
href="https://neulogy.vc/portfolio/ga-drilling/"
href="https://neulogy.vc/portfolio/greenway/"
href="https://neulogy.vc/sfdr-disclosure/"
href="https://www.crunchbase.com/organization/neulogy-ventures"
href="https://www.linkedin.com/company/neulogy-ventures/"
Deeptech investments leveraging CEE engineering talent.
Moonshot ideas pushing the frontier in technology, climate and health.About us
Anvesana is leveraging RNAseq analysis platform to treat rare genetic disorders caused by gene dosage effects.
BeiT is a unified platform for managing financial and operational processes in residential and commercial properties.
BiteBerry uses AI to boost restaurant efficiency with a voice ordering system integrated into POS systems.
Diagnose.me is a digital platform for medical diagnosis by international medical specialists.
Eyerim is a leading online eye-wear retailer in CEE.
Excalibur offers cyber security as a service with a range of enterprise-grade security solutions.
GA Drilling develops technology for ultra-d
… [skrátené, 3829 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://neulogy.vc/about-us/ 9000 | awk 'length($0)>50' | head -25
```

<details><summary>Výstup nástroja</summary>

```
Neulogy Ventures was established in 2014 as a Luxembourg-based regulated venture capital fund, targeting investment opportunities in early-stage tech companies established or operating in Slovakia. Built by entrepreneurs for entrepreneurs, the fund seeks to nurture the next generation of innovators to transition toward a knowledge economy.
With €65M assets under management, about 30 portfolio companies spread across 10 countries, and a strong track record investing in new technologies addressing climate change and healthcare, Neulogy Ventures is one of the leading deeptech investors in the CEE region.
Moonshot ideas pushing the frontier in technology, climate and health. Mission-driven entrepreneurs with bold ambitions taking audacious bets.
Our investors include 40+ key players in the local entrepreneurial ecosystem, joined by the European Investment Fund (EIF), the Slovak Investment Holding (SIH) and Tatra banka (RBI Group) as institutional investors.
Our funds are regulated by the Luxembourg financial sector regulator CSSF.
are entrepreneurs ourselves, looking for passion and ambition.
invest in real innovation, and don’t just blindly follow the hype.
are fast and transparent about our decision process.
help with fundraising, strategic guidance and business development.
keep the founders in the driving seat and align interests with them.
care about each entrepreneurial story, not just about aggregated portfolio returns.
take a long term view, with no pressure for fast exit
… [skrátené, 2863 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Neulogy Ventures\" investment round 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Neulogy Ventures investuje startup 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Neulogy Ventures" investment round 2026"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/neulogy"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/neulogy-ventures"},{"title":"Nulogy Funding History","url":"https://www.owler.com/company/nulogy/funding"},{"title":"neulogy ventures","url":"https://www.vestbee.com/vc-list/neulogy-ventures"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/neulogy"},{"title":"Neulogy Ventures","url":"https://www.seedtable.com/investors/neulogy-ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/neulogy-ventures"},{"title":"neulogy ventures","url":"https://startups.one.gob.es/companies/neulogy_ventures"},{"title":"# Neulogy VC","url":"https://brandfetch.com/neulogy.vc.md"},{"title":"Neulogy Ventures","url":"https://www.roundfunded.com/zh/vc/neulogy-ventures"}]

I couldn't find any reporting of a 2026 investment round by Neulogy Ventures. The results are mostly profile pages, and none describe a new round this year.

What the results do show about the firm:

- **Background:** Neulogy is a Bratislava-based VC firm that is a Luxembourg-regulated venture capital fund and focuses on early-stage tech companies, particularly those established or operating in Slovakia and the wider CEE region.
- **Fund size:** One profile puts its assets at €65 million, while another cit
… [skrátené, 2367 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Neulogy Ventures investuje startup 2025"

Links: [{"title":"neulogy ventures","url":"https://www.vestbee.com/vc-list/neulogy-ventures"},{"title":"Neulogy Ventures a ich úvodný event ako sa patrí","url":"https://www.startitup.sk/neulogy-ventures-a-ich-uvodny-event-ako-sa-patri/"},{"title":"Neulogy Ventures","url":"https://privateequitylist.com/public/investor/neulogy-ventures"},{"title":"About Neulogy","url":"https://trustburn.com/about/neulogy"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/neulogy-ventures"},{"title":"neulogy ventures","url":"https://privateequitylist.com/investor/neulogy-ventures"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/neulogy"},{"title":"Neulogy Ventures","url":"https://www.seedtable.com/investors/neulogy-ventures"},{"title":"# Neulogy VC","url":"https://brandfetch.com/neulogy.vc.md"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/neulogy"}]

I found several sources on Neulogy Ventures' 2025 activity, though they don't fully agree with each other.

**2025 deals**
- **GreenWay:** Caplight lists a March 2025 growth equity investment in GreenWay, with Neulogy as co-investor. Caplight's investment list shows GreenWay (Mar 2025, Growth Equity, Co-investor).
- **GA Drilling:** CB Insights reports a Series D round for GA Drilling on July 31, 2025, of $44.6M, which it lists as Neulogy's latest investm
… [skrátené, 2979 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "GA Drilling Series D 2025 investors Neulogy", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "BiteBerry Neulogy investícia", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Anvesana Neulogy Ventures investment", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "BiteBerry Neulogy investícia"

Links: [{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/neulogy-ventures"},{"title":"# Neulogy VC","url":"https://brandfetch.com/neulogy.vc.md"},{"title":"neulogy ventures","url":"https://startups.one.gob.es/companies/neulogy_ventures"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/nitin-bagamane"},{"title":"bite stream secures funding from newspring capital hiF8","url":"https://tirto.id/bite-stream-secures-funding-from-newspring-capital-hiF8"},{"title":"Berry, fintech argentina, cierra ronda de US$2M con Coinbase","url":"https://ecosistemastartup.com/?p=114969"},{"title":"app.dealroom.co","url":"https://app.dealroom.co/companies/bite_investments/team"},{"title":"iocharts.io","url":"https://iocharts.io/sk/crypto/berry"},{"title":"STEPHEN DE BERRY A0W8AX","url":"https://es.marketscreener.com/insider/STEPHEN-DE-BERRY-A0W8AX/"}]

I found no results linking BiteBerry to Neulogy. The search returned general information about Neulogy Ventures, but nothing mentioning a BiteBerry investment, so I can't confirm whether one exists.

**What the results say about Neulogy:**
- Neulogy Ventures is a Slovak fund manager. One profile describes it as a Slovakia-based management company that runs fully regulated seed and VC funds.
- Another source says the firm was established in 2014 and is a regulated fund based in Luxembourg, focusing on early-stage tech comp
… [skrátené, 2656 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "GA Drilling Series D 2025 investors Neulogy"

Links: [{"title":"Total Raised","url":"https://www.cbinsights.com/company/ga-drilling/financials"},{"title":"other 2025 07","url":"https://seedtable.com/companies/ga-drilling/funding-rounds/other-2025-07"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/neulogy-ventures"},{"title":"GA Drilling Secures $15M First Close from Nabors, alfa8, Underground Ventures, Neulogy Ventures and Thomas von Koch","url":"https://www.privsource.com/acquisitions/deal/YBSvjg"},{"title":"Compare AZIWELL vs GA Drilling","url":"https://www.cbinsights.com/compare/aziwell-vs-ga-drilling"},{"title":"GA Drilling: Competitive Response","url":"https://www.robotics.press/news/ga-drilling-competitive-response/"},{"title":"ga drilling a s","url":"https://sih.sk/en/portfolio/ga-drilling-a-s"},{"title":"taylor wessing advises ga drilling in an investment agreement with nabors industries","url":"https://www.taylorwessing.com/en/insights-and-events/news/media-centre/press-releases/2022/07/taylor-wessing-advises-ga-drilling-in-an-investment-agreement-with-nabors-industries"},{"title":"ga drilling","url":"https://bouncewatch.com/company/ga-drilling"}]

The search turned up a Series D round in 2025 with Neulogy Ventures named as a lead, but the sources disagree on the amount and the other investors. I found no primary press release, so treat these aggregator figures with caution.

**Neulogy's role:** Neul
… [skrátené, 3359 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Anvesana Neulogy Ventures investment"

Links: [{"title":"neulogy ventures","url":"https://www.vestbee.com/vc-list/neulogy-ventures"},{"title":"Neulogy Ventures","url":"https://www.seedtable.com/investors/neulogy-ventures"},{"title":"About Neulogy","url":"https://trustburn.com/about/neulogy"},{"title":"Neulogy Ventures","url":"https://privateequitylist.com/public/investor/neulogy-ventures"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/neulogy"},{"title":"Neulogy Ventures","url":"https://privateequitylist.com/investors/neulogy-ventures"},{"title":"neulogy ventures","url":"https://startups.one.gob.es/companies/neulogy_ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/neulogy-ventures"},{"title":"# Neulogy VC","url":"https://brandfetch.com/neulogy.vc.md"},{"title":"Neulogy VC","url":"https://venturecapitalarchive.com/venture-funds/neulogy-vc-neulogy-vc"}]

Links: [{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/anvesana"},{"title":"harsha majety","url":"https://india.entrepreneur.com/topic/harsha-majety"},{"title":"Anveshan Raises INR 150 Cr in Series B Led by Vertex Ventures","url":"https://india.entrepreneur.com/?p=96762"},{"title":"Anveshan Raises INR 150 Cr in Series B Led by Vertex Ventures","url":"https://india.entrepreneur.com/business-news/anveshan-raises-inr-150-cr-in-series-b-led-by-vertex-ventures"},{"title":"Chandhiok & Mahajan advises Wipro on investment in Anveshan Farm Tech"
… [skrátené, 4030 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in ga-drilling greenway biteberry anvesana beit; do echo "== $p"; python3 -I $S/page.py show https://neulogy.vc/portfolio/$p/ 6000 | awk 'length($0)>40' | head -8; done
```

<details><summary>Výstup nástroja</summary>

```
== ga-drilling
GA Drilling develops technology for ultra-deep geothermal as the only viable large-scale baseload solution.
GA Drilling, with its patented PLASMABIT® technology, offers a solution for a local and independent source of electricity, heating, clean water, and food production in an unstable world. The company will provide scalable, modular, solutions to zero-carbon emissions energy production. Geothermal energy is the only renewable source of clean and baseload energy, available 24/7/365. It works regardless of weather conditions or the day-night cycle. PLASMABIT® brings a significant reduction in operational time and cost savings, drilling faster, deeper, and cheaper through any material, including hard rock and steel.
The co-founder and CEO, Igor Kočiš, as well as the whole GA Drilling team, brings an extensive experience in engineering, R&D, business development, and managerial leadership experience to the company.
GA Drilling is headquartered in Bratislava (Slovakia) with branches in Bristol (UK), Houston (USA) and Abu Dhabi (UAE).
2026 Neulogy Ventures, All rights reserved.
== greenway
GreenWay is a provider of charging infrastructure for e-vehicles in the CEE.
GreenWay is a provider of charging infrastructure for e-vehicles in the CEE. With a strong foothold in Poland and Slovakia, it strives to become #1 in the CEE. GreenWay is dedicated to making the use of electric vehicles a realistic and preferred transportation option for people throughout the CEE. It b
… [skrátené, 3946 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "GreenWay 2025 investícia Neulogy kapitál nabíjacie stanice", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "GA Drilling raises Nabors alfa8 Underground Ventures Neulogy Ventures Thomas von Koch", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "GA Drilling raises Nabors alfa8 Underground Ventures Neulogy Ventures Thomas von Koch"

Links: [{"title":"GA Drilling Secures $15M First Close from Nabors, alfa8, Underground Ventures, Neulogy Ventures and Thomas von Koch","url":"https://www.privsource.com/acquisitions/deal/YBSvjg"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/ga-drilling/financials"},{"title":"ga drilling","url":"https://bouncewatch.com/company/ga-drilling"},{"title":"other 2025 07","url":"https://seedtable.com/companies/ga-drilling/funding-rounds/other-2025-07"},{"title":"ga drilling a s","url":"https://sih.sk/en/portfolio/ga-drilling-a-s"},{"title":"26. Juli 2022","url":"https://www.taylorwessing.com/de/insights-and-events/news/media-centre/press-releases/2022/07/taylor-wessing-advises-ga-drilling-in-an-investment-agreement-with-nabors-industries"},{"title":"taylor wessing advises ga drilling in an investment agreement with nabors industries","url":"https://www.taylorwessing.com/en/insights-and-events/news/media-centre/press-releases/2022/07/taylor-wessing-advises-ga-drilling-in-an-investment-agreement-with-nabors-industries"},{"title":"GA Drilling: Competitive Response","url":"https://www.robotics.press/news/ga-drilling-competitive-response/"},{"title":"top of page","url":"https://www.symsite.sk/single-post/ga-drilling-landed-7-3m-investment-from-us-based-nabors"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/undergro
… [skrátené, 3493 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "GreenWay 2025 investícia Neulogy kapitál nabíjacie stanice"

Links: [{"title":"Investícia vo výške 85 miliónov EUR do rastu siete pre priekopníka GreenWay","url":"https://touchit.sk/investicia-vo-vyske-85-milionov-eur-do-rastu-siete-a-dalsiu-expanziu-pre-priekopnika-e-mobility-spolocnost-greenway/401298/"},{"title":"e mobility pioneer greenway raises 85 million euros to grow company and expand network","url":"https://ceenergynews.com/transport/e-mobility-pioneer-greenway-raises-85-million-euros-to-grow-company-and-expand-network/"},{"title":"top of page","url":"https://symsite.sk/single-post/greenway-raised-85m-from-investors"},{"title":"balkangreenenergynews.com","url":"https://balkangreenenergynews.com/?p=79431"},{"title":"GreenWay collects €85 million from investors","url":"https://electrive.com/2022/02/23/greenway-collects-e85-million-from-investors"},{"title":"GreenWay NetworkBlogE-mobility pioneer GreenWay raises €85 million to grow company and expand network","url":"https://greenwaynetwork.com/?p=91924"},{"title":"20. March 2025 at 23:33","url":"https://spectator.sme.sk/business/c/slovakia-s-ev-charging-leader-attracts-major-global-investor"},{"title":"Mirova injects €50 million in charging specialist GreenWay","url":"https://www.electrive.com/2025/03/17/mirova-injects-e50-million-in-charging-specialist-greenway"},{"title":"Duże przejęcie na polskim rynku stacji ładowania","url":"https://www.gramwzielone.pl/?p=108283"},{"title":"Duże zmia
… [skrátené, 3387 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "StratifAI pre-seed Neulogy Ventures", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.privsource.com/acquisitions/deal/YBSvjg 'Neulogy|2024|April'
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "StratifAI pre-seed Neulogy Ventures"

Links: [{"title":"Christian Mandl","url":"https://sk.linkedin.com/in/christianmandl"},{"title":"cekan pavol multiplexdx 202409 inc persons people chief 2001 28559","url":"https://www.life-sciences-europe.com/person/cekan-pavol-multiplexdx-202409-inc-persons-people-chief-2001-28559.html"},{"title":"app.foundernest.com","url":"https://app.foundernest.com/public/space/7678/companies/10190350?page=11"},{"title":"Recently FundedEUR 1.5MTechnology, Information and Internet","url":"https://www.trysignalbase.com/news/funding/stratifai-secures-1.5-million-in-pre-seed-funding-to-revolutionize-precision-oncology-with-ai-driven-biomarkers"},{"title":"Funding Stage","url":"https://seedtable.com/companies/stratifai"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/stratifai-secures-12-5m-funding-round"},{"title":"Back to Stories","url":"https://aiworld.eu/story/stratifai-raises-125m-to-make-cancer-treatment-more-precise-with-ai"},{"title":"Major Investements for","url":"https://digitalhealth.tu-dresden.de/?p=13630"},{"title":"rocketlist.ai","url":"https://rocketlist.ai/companies/stratifai"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/stratifai"}]

StratifAI's €1.5M pre-seed round was announced in September 2024, and Neulogy Ventures was one of the lead investors. The search results describe the round consistently, but they differ on some details of the company's later funding.

**
… [skrátené, 3189 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
- GA Drilling Secures $15M First Close from Nabors, alfa8, Underground Ventures, Neulogy Ventures and Thomas von Koch | PrivSource
- GA Drilling Secures $15M First Close from Nabors, alfa8, Underground Ventures, Neulogy Ventures and Thomas von Koch
- GA Drilling Secures $15M First Close from Nabors, alfa8, Underground Ventures, Neulogy Ventures and Thomas von Koch
- April 25, 2024
- GA Drilling, a developer of deep geothermal drilling technology, announced a first close of $15 million to commercialize its PLASMABIT drilling systems and scale deployment. Investors in the round include Nabors, Christian Oldendorff’s family office alfa8, geothermal fund Underground Ventures, Neulogy Ventures and investor Thomas von Koch; proceeds will accelerate commercialization and global rollout of deep geothermal solutions.
- Nabors, alfa8, Thomas von Koch, Underground Ventures, Neulogy Ventures
- Renewable Energy Acquisitions in 2024
- Growth Capital Investments in 2024
- January 9, 2024
- Kerogen Capital (through its CelerateX platform) and Thrive Renewables plc provided £15 million of funding to Geothermal Engineering Limited (GEL) — £12 million from Kerogen and £3 million from Thrive — to advance the United Downs deep geothermal project in Cornwall and accelerate GEL's UK geothermal portfolio. The capital will fund completion of the United Downs plant (targeting electricity production by 2024) and support GEL's goal of delivering 25 MWe of baseload electricity and 100 MWth of heat across
… [skrátené, 1523 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep "https://www.trysignalbase.com/news/funding/stratifai-secures-1.5-million-in-pre-seed-funding-to-revolutionize-precision-oncology-with-ai-driven-biomarkers" 'Neulogy|2024'; python3 -I $S/page.py grep "https://digitalhealth.tu-dresden.de/?p=13630" 'Neulogy|2024'
```

<details><summary>Výstup nástroja</summary>

```
- Funding news·Published September 2, 2024
- Neulogy Ventures
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"StratifAI\" \"co-led by Neulogy Ventures and MultiplexDX\"", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""StratifAI" "co-led by Neulogy Ventures and MultiplexDX""

Links: [{"title":"Christian Mandl","url":"https://sk.linkedin.com/in/christianmandl"},{"title":"cekan pavol multiplexdx 202409 inc persons people chief 2001 28559","url":"https://www.life-sciences-europe.com/person/cekan-pavol-multiplexdx-202409-inc-persons-people-chief-2001-28559.html"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/stratifai"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/company/stratifai"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/stratifai-secures-12-5m-funding-round"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/multiplexdx/financials"},{"title":"Back to Stories","url":"https://aiworld.eu/story/stratifai-raises-125m-to-make-cancer-treatment-more-precise-with-ai"},{"title":"Funding Stage","url":"https://seedtable.com/companies/stratifai"},{"title":"app.foundernest.com","url":"https://app.foundernest.com/public/space/7678/companies/10190350?page=5"},{"title":"StratifAI is a precision oncology company developing the next generation of biomarkers to advance cancer diagnostics","url":"https://f4.fund/startups/stratifai"}]

The query matches a pre-seed round from September 2024. StratifAI raised €1.5 million, with Neulogy Ventures and MultiplexDX as co-leads. A LinkedIn post by a company-linked account announced the round as led by Neulogy
… [skrátené, 3151 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep "https://www.life-sciences-europe.com/person/cekan-pavol-multiplexdx-202409-inc-persons-people-chief-2001-28559.html" 'Neulogy|9/2/24|StratifAI Raises'
```

<details><summary>Výstup nástroja</summary>

```
- StratifAI GmbH. (9/2/24). "Press Release: StratifAI Raises €1.5M in Pre-seed Funding to Advance AI-based Precision Oncology".
- StratifAI, a pioneering provider of AI-powered digital oncology solutions, today announced it has raised €1.5 million in pre-seed funding. The round was co-led by Neulogy Ventures and MultiplexDX, with participation from Debiopharm Innovation Fund, Arve Capital, as well as angel investor Christoph Haarburger.
- "We firmly believe that advances in artificial intelligence have the potential to significantly improve outcomes for cancer patients and substantially decrease the cost of cancer treatment. The team behind StratifAI has been instrumental in laying the groundwork for computational pathology and is perfectly positioned to leverage this deep domain expertise to build efficient companion diagnostics (CDx) products. Starting with a breast cancer prognostication test, the StratifAI pipeline has the potential to scale across various indications and biomarkers. Neulogy Ventures is very proud to have the opportunity to support StratifAI as a pre-seed investor."
- Partner at Neulogy Ventures
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c009.json <<'EOF'
{
  "candidate_id": "c009",
  "name": "Neulogy Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://neulogy.vc/",
  "entity_kind": {"value": "investor", "source_url": "https://neulogy.vc/about-us/", "source_date": null, "quote": "Neulogy Ventures was established in 2014 as a Luxembourg-based regulated venture capital fund, targeting investment opportunities in early-stage tech companies established or operating in Slovakia."},
  "investor_type": {"value": "vc", "source_url": "https://neulogy.vc/about-us/", "source_date": null, "quote": "We are a venture capital firm focused on supporting visionary founders at the early-stages of company formation and growth."},
  "sectors": {"value": ["deep tech", "climate", "healthtech"], "source_url": "https://neulogy.vc/about-us/", "source_date": null, "quote": "With €65M assets under management, about 30 portfolio companies spread across 10 countries, and a strong track record investing in new technologies addressing climate change and healthcare, Neulogy Ventures is one of the leading deeptech investors in the CEE region."},
  "stages": {"value": ["seed"], "source_url": "https://www.slovca.sk/sk/riadni-clenovia/neulogy-ventures.html", "source_date": null, "quote": "Typ investícií: Seed, Venture capital"},
  "ticket_min": {"amount": 200000, "currency": "EUR", "source_url": "https://www.slovca.sk/sk/riadni-clenovia/neulogy
… [skrátené, 3992 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c009.json
c009.json entity_kind OK
c009.json investor_type OK
c009.json sectors OK
c009.json stages OK
c009.json ticket_min OK
c009.json ticket_max OK
c009.json aum OK
c009.json inv:StratifAI OK
c009.json inv:GA Drilling OK
```

</details>

**Nástroj `Bash`**

```bash
python3 - <<'EOF'
import json
p="research/c009.json"; d=json.load(open(p))
q="GA Drilling, a developer of deep geothermal drilling technology, announced a first close of $15 million to commercialize its PLASMABIT drilling systems and scale deployment. Investors in the round include Nabors, Christian Oldendorff’s family office alfa8, geothermal fund Underground Ventures, Neulogy Ventures and investor Thomas von Koch; proceeds will accelerate commercialization and global rollout of deep geothermal solutions."
print(len(q))
d["investments"][1]["quote"]=q
d["notes"]=d["notes"].replace(" the GA Drilling quote does not name the company in the same sentence (company is in the page headline).", " GA Drilling source is an aggregator (PrivSource).")
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c009.json && python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c009.json | grep GA; grep notes research/c009.json
```

<details><summary>Výstup nástroja</summary>

```
433
OK    research/c009.json
c009.json inv:GA Drilling OK
  "notes": "Bratislava-based deeptech VC with Luxembourg (CSSF) regulated funds; invests also outside SK (e.g. StratifAI in Germany). Individual fund names not found. Aggregators mention a 2025 GA Drilling Series D led by Neulogy, but no primary source was found; GA Drilling source is an aggregator (PrivSource). Newer portfolio companies (BiteBerry, Anvesana, BeiT) have no dated deal source.",
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://sandbergcapital.com/en | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg|\.svg' | head -60
```

<details><summary>Výstup nástroja</summary>

```
href="/en"
href="http://localhost:8000/portfolio.html"
href="http://sandbergcapital.com/en/contact/"
href="http://sandbergcapital.com/en/kontakt/"
href="http://sandbergcapital.com/en/portfolio/agriculture/"
href="http://sandbergcapital.com/en/portfolio/information-technologies/"
href="http://sandbergcapital.com/en/portfolio/retail/"
href="http://sandbergcapital.com/portfolio/?lang=en"
href="https://gmpg.org/xfn/11"
href="https://sandbergcapital.com/"
href="https://sandbergcapital.com/en/"
href="https://sandbergcapital.com/en/about-us/"
href="https://sandbergcapital.com/en/contact/"
href="https://sandbergcapital.com/en/for-investors/"
href="https://sandbergcapital.com/en/how-we-invest/"
href="https://sandbergcapital.com/en/media/"
href="https://sandbergcapital.com/en/our-fonds/"
href="https://sandbergcapital.com/en/portfolio/"
href="https://sandbergcapital.com/en/portfolio/agriculture/"
href="https://sandbergcapital.com/en/portfolio/education/"
href="https://sandbergcapital.com/en/portfolio/information-technologies/"
href="https://sandbergcapital.com/en/portfolio/retail/"
href="https://sandbergcapital.com/en/portfolio/telecommunication/"
href="https://sandbergcapital.com/en/pravne-informacie-a-gdpr/"
href="https://sandbergcapital.com/en/we-support/"
href="https://sandbergcapital.com/en/work-with-us/"
href="mailto:[email]"
href="mailto:[email]"
href="tel:+421259418181"
href="tel:+421918046121"
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in about-us how-we-invest our-fonds media; do echo "=== $p"; python3 -I $S/page.py show https://sandbergcapital.com/en/$p/ 9000 | awk 'length($0)>40' | head -30; done
```

<details><summary>Výstup nástroja</summary>

```
=== about-us
We are an alternative investment fund management company that focuses on investing in small and medium-sized companies in the region of Central and Eastern Europe, with a primary focus on Slovakia and Czech Republic. We invest in ambitious companies managed or owned by ambitious leaders. We create partnerships with people whom our capital and experience will help to achieve the highest goals.
Sandberg Capital was established in 2014.
We manage assets in the value of more than 500 mil. EUR.
Our portfolio consists of investments in the IT, agriculture, telecommunications, retail and education sectors. Portfolio companies employ more than 3,000 employees.
The founder of Sandberg Capital. He led his first transaction while studying at the Faculty of Management of Comenius University in 1996. At that time, he was one of the youngest, today he is one of the most experienced. He has been involved in acquisitions, mainly in the areas of media, telecommunications, IT and energy, for more than 20 years. He likes to spend time with his family and friends, ideally in the mountains, whether walking, skiing or cycling.
Michal studied business management at the Technical University in Zvolen and law at the University of Matej Bel in Banská Bystrica, He has over 10 years of experience in M&A and has participated in dozens of acquisitions primarily in the IT and telecommunications sectors. He is a partner at Sandberg Capital since 2016. His best relax is when running, playing hoc
… [skrátené, 15066 znakov]
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://sandbergcapital.com/en/media/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -iE 'carrot|hoteltime|rentlio|hausmann' 
```

<details><summary>Výstup nástroja</summary>

```
href="https://sandbergcapital.com/en/sandberg-acquires-a-majority-stake-in-czech-technology-company-hoteltime/"
href="https://sandbergcapital.com/en/sandberg-and-arx-continue-hospitality-tech-consolidation-with-the-acquisition-of-croatias-rentlio/"
href="https://sandbergcapital.com/en/sandberg-enters-the-polish-market-through-the-acquisition-of-a-majority-stake-in-carrot/"
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in sandberg-acquires-a-majority-stake-in-czech-technology-company-hoteltime sandberg-and-arx-continue-hospitality-tech-consolidation-with-the-acquisition-of-croatias-rentlio sandberg-enters-the-polish-market-through-the-acquisition-of-a-majority-stake-in-carrot; do echo "== $p"; python3 -I $S/page.py show https://sandbergcapital.com/en/$p/ 9000 | awk 'length($0)>30' | head -6; done
```

<details><summary>Výstup nástroja</summary>

```
== sandberg-acquires-a-majority-stake-in-czech-technology-company-hoteltime
SANDBERG ACQUIRES A MAJORITY STAKE IN CZECH TECHNOLOGY COMPANY HOTELTIME - Sandberg Capital
SANDBERG ACQUIRES A MAJORITY STAKE IN CZECH TECHNOLOGY COMPANY HOTELTIME
Sandberg Capital, a private equity investment group, is entering HotelTime, a leading provider of hotel software, through its second fund, Sandberg Investment Fund II (SIF2). The goal of acquiring a majority stake is to accelerate the company’s growth, support its expansion into international markets, and develop it into one of the key technological platforms in the hotel segment.
HotelTime is one of the globally recognised providers of cloud-based property management systems (PMS). According to the HotelTechReport ranking, it is among the top five PMS systems in the world. The company is the market leader in its segment in the Czech Republic, and its solutions are used by more than 700 hotels in 20 countries worldwide. It holds a strong position not only in Europe but also successfully operates in several countries in Africa and Southeast Asia.
The acquisition of HotelTime fits into Sandberg’s long-term strategy to grow its presence in the Travel & Hospitality Tech sector, which the group initiated with the acquisition of Croatian company Phobs. HotelTime naturally expands this direction as a new platform investment with significant international potential.
“HotelTime has an excellent international product, highly satisfied customers, and
… [skrátené, 6362 znakov]
```

</details>

**Nástroj `Bash`**

```bash
for p in sandberg-acquires-a-majority-stake-in-czech-technology-company-hoteltime sandberg-enters-the-polish-market-through-the-acquisition-of-a-majority-stake-in-carrot; do curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://sandbergcapital.com/en/$p/ | grep -oE '(article:published_time|datePublished)"?[^,>]{0,50}' | head -2; done
```

<details><summary>Výstup nástroja</summary>

```
article:published_time" content="2025-12-12T16:06:14+00:00" /
datePublished":"2025-12-12T16:06:14+00:00"
article:published_time" content="2026-09-01T21:20:05+00:00" /
datePublished":"2026-09-01T21:20:05+00:00"
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c010.json <<'EOF'
{
  "candidate_id": "c010",
  "name": "Sandberg Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ", "PL", "HR", "SI"],
  "website": "https://sandbergcapital.com/en/",
  "entity_kind": {"value": "investor", "source_url": "https://sandbergcapital.com/en/about-us/", "source_date": null, "quote": "We are an alternative investment fund management company that focuses on investing in small and medium-sized companies in the region of Central and Eastern Europe, with a primary focus on Slovakia and Czech Republic."},
  "investor_type": {"value": "pe", "source_url": "https://sandbergcapital.com/en/sandberg-acquires-a-majority-stake-in-czech-technology-company-hoteltime/", "source_date": "2025-12-12", "quote": "Sandberg Capital, a private equity investment group, is entering HotelTime, a leading provider of hotel software, through its second fund, Sandberg Investment Fund II (SIF2)."},
  "sectors": {"value": ["it", "agriculture", "telecommunications", "retail", "education"], "source_url": "https://sandbergcapital.com/en/about-us/", "source_date": null, "quote": "Our portfolio consists of investments in the IT, agriculture, telecommunications, retail and education sectors."},
  "stages": {"value": ["growth"], "source_url": "https://sandbergcapital.com/en/how-we-invest/", "source_date": null, "quote": "are in the growth or mature stage of the company´s life cycle."},
  "ticket_min": null
… [skrátené, 4177 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c010.json
c010.json entity_kind OK
c010.json investor_type OK
c010.json sectors OK
c010.json stages OK
c010.json ticket_max OK
c010.json aum OK
c010.json inv:Carrot OK
c010.json inv:Rentlio OK
c010.json inv:HotelTime OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://vff.sk/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg|\.svg' | head -40; python3 -I $S/page.py show https://vff.sk/ 12000 | awk 'length($0)>40' | sed -n '1,40p'
```

<details><summary>Výstup nástroja</summary>

```
href="/"
href="#ava"
href="/data/files/esg-politika-udrzatelnosti-7.pdf"
href="/data/files/informacie_o_spracuvani_osobnych_udajov_vff-6.pdf"
href="/data/files/logo-2.pdf"
href="/data/files/ochrana-sukromia-1.pdf"
href="/data/files/vff-excel-na-web-faktury_2026-4.pdf"
href="/data/files/vff_objednavky-3.pdf"
href="/en/"
href="/favicon.ico"
href="https://nettle.ai/"
href="https://vff.sk"
href="https://www.crz.gov.sk/"
href="https://www.eib.org/en/index.htm"
href="https://www.linkedin.com/company/venturetofuturefund"
href="https://www.linkedin.com/in/juraj-sloboda-3ab53a46/"
href="https://www.linkedin.com/in/martin-bansky-0570a6b/"
href="https://www.linkedin.com/in/martin-mecele-a503b9161/"
href="https://www.linkedin.com/in/matej-%C5%99%C3%ADha-a8131a1b/ "
href="https://www.linkedin.com/in/miriamakovacova/"
href="https://www.linkedin.com/in/romanhorvath/"
href="https://www.linkedin.com/in/vladimira-capkova/"
href="https://www.mfsr.sk/sk/ "
href="https://www.openstreetmap.org/copyright"
href="https://www.sih.sk/stranky/cinnosti/national-development-fund-i/o-spolocnosti-ndf-i "
href="https://www.sih.sk/stranky/cinnosti/slovak-asset-management"
href="#icon-analytics"
href="#icon-close"
href="#icon-lightBulb"
href="#icon-linkedin"
href="#icon-oclock"
href="#icon-place3"
href="#icon-puzzle"
href="#icon-swipe-right-black"
href="#icon-target"
href="javascript:;"
href="/novinky/ako-ziskat-kapital-na-svoj-dalsi-rast-zistite-na-webinari-s-venture-to-future-fund-4"
href="/novinky/cesky-sta
… [skrátené, 11117 znakov]
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://vff.sk/novinky | grep -oE "href=['\"]/novinky/[^'\"]*['\"]" | sort -u | head -60
```

<details><summary>Výstup nástroja</summary>

```
href="/novinky/ako-ziskat-kapital-na-svoj-dalsi-rast-zistite-na-webinari-s-venture-to-future-fund-4"
href="/novinky/cvca-slovca-awards-2023-pozna-svojich-vitazov-21"
href="/novinky/davame-slovenskym-inovativnym-firmam-ferovu-sancu-na-uspech-14"
href="/novinky/liptovska-firma-sec-technologies-ziskala-investiciu-3-miliony-eur-5"
href="/novinky/na-boj-s-hoaxami-a-podporu-komunikacie-medzi-mestom-a-obyvatelmi-ziskal-startup-simplicity-investiciu-7-milionov-eur-9"
href="/novinky/nase-investicne-portfolio-sa-rozsirilo-o-spolocnost-product-fruits-ktora-ziskala-investiciu-vo-vyske-1-6-miliona-eur-19"
href="/novinky/nizsie-riziko-nekvalitneho-naboru-vdaka-background-skriningu-scaut-ziskava-milion-eur-na-rozvoj-od-fondu-vff-a-skupiny-investorov-23"
href="/novinky/patenty-z-dielne-sec-technologies-su-pychou-slovenska-18"
href="/novinky/podpora-buducnosti-robotiky-v-podobe-novej-investicie-do-spolocnosti-spinbotics-26"
href="/novinky/sensoneo-ziskalo-investiciu-2-miliony-eur-z-fondu-europskej-rady-pre-inovacie-a-venture-to-future-fund-11"
href="/novinky/slovenska-technologicka-firma-nettle-ai-ziskala-milionovu-investiciu-6"
href="/novinky/slovensky-digital-twin-startup-twinzo-ziskal-investiciu-vo-vyske-2-3-miliona-eur-25"
href="/novinky/slovensky-startup-agevolt-so-svojim-ekosystemom-nabijania-elektromobilov-ziskal-investiciu-1-2-miliona-eur-8"
href="/novinky/slovensky-startup-nexineo-inovujuci-pocitacove-ucebne-ziskal-milionove-financovanie-a-planuje-expanziu-20"
href="/novinky/slovensk
… [skrátené, 2036 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; for p in cesky-startup-patron-go-ziskava-investiciu-v-hodnote-1-milion-eur-30 podpora-buducnosti-robotiky-v-podobe-novej-investicie-do-spolocnosti-spinbotics-26 slovensky-digital-twin-startup-twinzo-ziskal-investiciu-vo-vyske-2-3-miliona-eur-25; do echo "== $p"; python3 -I $S/page.py show https://vff.sk/novinky/$p 9000 | awk 'length($0)>25' | grep -vE 'cookie|Cookie' | sed -n '1,8p'; python3 -I $S/page.py grep https://vff.sk/novinky/$p '20(2[3-6])' | head -4; done
```

<details><summary>Výstup nástroja</summary>

```
== cesky-startup-patron-go-ziskava-investiciu-v-hodnote-1-milion-eur-30
Venture to Future Fund - Český startup Patron GO získava investíciu v hodnote 1 milión eur
Český startup Patron GO získava investíciu v hodnote 1 milión eur
Praha, 12. augusta 2024 – Najnovšia investícia do startupu Patron GO, chytrej aplikácie na optimalizáciu osobných financií, prichádza zo Slovenska. Slovenský fond Venture to Future Fund sa vo štvrtom investičnom kole pridáva k ďalším investorom a do aplikácie spoločne vkladajú celkom 1 milión eur. Investícia pomôže pri súčasnej expanzii do Poľska a tiež lepšiemu pokrytiu existujúcich trhov.
„V Patron GO chceme byť prvou voľbou klienta v oblasti riešení osobných financií, čo dokazuje aj naše nedávne ocenenie 3. miesta v kategórii Fintech v rámci súťaže Zlatá Koruna 2024 alebo ocenenie Startup roka 2023 v súťaži Central European Startup Awards. Chytré riešenie osobných financií užívateľa baví aj vďaka gamifikácii – potvrdzuje nám to časté umiestnenie Patron GO na popredných priečkach rebríčkov sťahovania mobilných aplikácií. Investícia nám uľahčí už prebiehajúcu expanziu do Poľska. To v poslednom čase zaznamenáva ekonomický rast a životná úroveň jeho obyvateľov sa zvyšuje, preto na trh prichádzame v správny čas,“ uvádza Lukáš Vršecký, CEO a spoluzakladateľ Patron GO.
Patron GO v Českej republike a na Slovensku zmapoval už viac ako 17 miliónov transakcií pre takmer 250 tisíc používateľov, a tak je expanzia do Poľska prirodzeným krokom v rozširovaní podni
… [skrátené, 9599 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Venture to Future Fund\" investícia 2025 Talentiqa OR BiteBerry OR \"International Automotive Group\" OR Terratico", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Venture to Future Fund" investícia 2025 Talentiqa OR BiteBerry OR "International Automotive Group" OR Terratico"

Links: [{"title":"Venture to Future Fund Overview","url":"https://pitchbook.com/profiles/investor/461930-23"},{"title":"Venture to Future Fund Overview","url":"https://pitchbook.com/profiles/fund/18944-11F"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/venture-to-future-fund"},{"title":"Brandfetch's icon's iconVenture to Future Fund's icon","url":"https://brandfetch.com/vff.sk"},{"title":"the future fund","url":"https://seedtable.com/investors/the-future-fund"},{"title":"Future Wealth Investments launches $50m venture fund","url":"https://www.dealstreetasia.com/stories/future-wealth-investments-477591"},{"title":"Future Ventures logo","url":"https://www.everythingstartups.com/vc-funds/future-ventures"},{"title":"startup-seeker.com","url":"https://startup-seeker.com/vc/future~ventures"},{"title":"www.arounddeal.com","url":"https://www.arounddeal.com/c/venture-to-future-fund-a-s/r7kaorpjcd"}]

The search turned up 2025 deal records for all four companies, all linked to Venture to Future Fund (VFF), a Bratislava-based venture investor. Terratico's deal was in late 2024.

- **Talentiqa (2025):** PitchBook dates the deal to 23 June 2025. A later report describes a €1M round for the Prague-based recruitment startup, equally backed by Purple Ventures and Venture to Future Fund. That report is dated 30 
… [skrátené, 2581 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Talentiqa Purple Ventures Venture to Future Fund 1 milion eur", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "International Automotive Group IAG investícia Venture to Future Fund Jet Investment", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Talentiqa Purple Ventures Venture to Future Fund 1 milion eur"

Links: [{"title":"seed 2025 09","url":"https://seedtable.com/companies/talentiqa/funding-rounds/seed-2025-09"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/venture-to-future-fund"},{"title":"a recruitment automation startup out of Prague","url":"https://funding.tech.eu/companies/1E41EC39-48C9-47F9-A358-22371BC67603"},{"title":"Subscribe to Our Newsletter","url":"https://www.thesaasnews.com/news/talentiqa-raises-1-million-in-funding/"},{"title":"Purple Ventures launches €40M fund for early-stage software startups","url":"https://tech.eu/2024/06/27/purple-ventures-launches-eur40m-fund-for-early-stage-software-startups/"},{"title":"purple ventures 40m fund ii investments smart energy cloud hr hybrid events","url":"https://en.ain.ua/2024/06/28/purple-ventures-40m-fund-ii-investments-smart-energy-cloud-hr-hybrid-events"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/purple-ventures"},{"title":"Purple Ventures II Overview","url":"https://pitchbook.com/profiles/fund/24052-06F"},{"title":"CEE VC SUMMIT 2025","url":"https://vestbee.com/blog/articles/purple-ventures-launches-40-m-fund-ii"}]

The round was €1 million, split equally between Purple Ventures and Venture to Future Fund, and it was reported in late September 2025.

**The deal**
- Talentiqa, an AI recruitment-automation startup, raised about €1 million. The company plans to use it 
… [skrátené, 2914 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "International Automotive Group IAG investícia Venture to Future Fund Jet Investment"

Links: [{"title":"Má velké plány s fotbalem, dál se ale poohlíží i po startupech. Miliardáře Faita teď zaujaly autodíly","url":"https://cc.cz/ma-velke-plany-s-fotbalem-dal-se-ale-poohlizi-i-po-startupech-miliardare-faita-zaujaly-autodily/"},{"title":"international automotive group raises e5m from jet ventures","url":"https://startuprise.co.uk/international-automotive-group-raises-e5m-from-jet-ventures/"},{"title":"ED825E4A 48D5 49A1 9112 4B9FD16E830E","url":"https://funding.tech.eu/companies/ED825E4A-48D5-49A1-9112-4B9FD16E830E"},{"title":"www.air journal","url":"https://www.air-journal.fr/?p=261524"},{"title":"IAG to invest 200 million in aviation startups","url":"https://www.businesstravelnewseurope.com/Air-Travel/IAG-to-invest-200-million-in-aviation-startups"},{"title":"# International Airlines Group announces $218m CVC fund","url":"https://globalventuring.com/corporate/corporate-venturer/international-airlines-group-announces-e200m-cvc-fund/?format=md"},{"title":"IAG intends to invest in companies across all global markets through IAGi Ventures","url":"https://avitrader.com/tag/iagi/"},{"title":"iag investiert mit 200 millionen in firmen die das kundenerlebnis verbessern und die betriebliche effizienz steigern helfen","url":"https://www.aerotelegraph.com/iag-investiert-mit-200-millionen-in-firmen-die-das-kundenerlebnis-verbessern-und-die-betriebliche-effiz
… [skrátené, 3685 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.thesaasnews.com/news/talentiqa-raises-1-million-in-funding/ 'Venture to Future|2025'; echo ===; python3 -I $S/page.py grep https://cc.cz/ma-velke-plany-s-fotbalem-dal-se-ale-poohlizi-i-po-startupech-miliardare-faita-zaujaly-autodily/ 'Venture to Future|Jet|2025'; curl -sL -A "Mozilla/5.0" https://cc.cz/ma-velke-plany-s-fotbalem-dal-se-ale-poohlizi-i-po-startupech-miliardare-faita-zaujaly-autodily/ | grep -oE 'datePublished"?[^,]{0,40}' | head -2
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
- October 07, 2025
- The funding round was backed equally by Purple Ventures and Venture to Future Fund.
- Venture to Future Fund is a Slovak fund that invests in Slovak and European SMEs with innovative solutions, focusing on Series A and later rounds. Investments typically range from €500,000 to €4.5 million.
- Funding Date: October 2025
- Additional Investors: Venture to Future Fund
- Source: https://en.ain.ua/2025/09/30/talentiqa-raises-eur1m/
- October 07, 2025
(eval):1: == not found
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://en.ain.ua/2025/09/30/talentiqa-raises-eur1m/ 'Venture to Future|Talentiqa'; python3 -I $S/page.py grep https://startuprise.co.uk/international-automotive-group-raises-e5m-from-jet-ventures/ 'Venture to Future|2025'
```

<details><summary>Výstup nástroja</summary>

```
- Talentiqa raises €1M to expand AI-powered recruitment platform across Europe
- Czech startup Talentiqa raises...
- Czech startup Talentiqa raises €1M to expand AI-powered recruitment platform across Europe
- Talentiqa, a Czech recruitment automation startup, has secured €1 million in funding to expand its AI-powered hiring assistant. The round was backed by Purple Ventures and Venture to Future Fund, EU-Startups reports.
- About Talentiqa
- Talentiqa is a Prague-based recruitment tech startup, founded in 2021 by Marek Dian and Miro Šmelko, that provides an AI-powered platform to automate initial candidate screening.
- “We founded Talentiqa to speed up the initial interview and increase its success rate. Thanks to AI, we can now automate the most difficult part at scale – the first contact, verifying interest, and quickly connecting the right people with the right companies,” says Marek Dian, co-founder and CEO of Talentiqa.
- The round was equally backed by Purple Ventures and Venture to Future Fund.
- Venture to Future Fund is a Slovak fund which invests in Slovak and European SMEs with innovative solutions, focusing on Series A and later rounds. Investments typically range from €500,000 to €4.5 million.
- Talentiqa will use fresh funding to expand its AI-powered pre-screening and interview automation platform across Europe and beyond.
- May 23, 2025 | By Kailee Rainse
- May 29, 2025
- Jet Investment is contributing €2.4M of the total funding. Other investors include Ventu
… [skrátené, 1573 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://startuprise.co.uk/international-automotive-group-raises-e5m-from-jet-ventures/ 'International Automotive|IAG' | head
```

<details><summary>Výstup nástroja</summary>

```
- International Automotive Group Raises €5M from Jet Ventures
- International Automotive Group Raises €5M from Jet Ventures
- Prague-based International Automotive Group, a B2B e-commerce and distribution platform for automotive spare parts, has raised €5 million in funding.
- Prague-based International Automotive Group, a B2B e-commerce and distribution platform for automotive spare parts, has raised €5 million in funding.
- IAG is the second startup backed by Jet Investment, which had earlier invested in Partory.
- Kamil Levinsky, Executive Director of Jet Ventures, says, “We are excited to support the IAG team and its innovative strategy. We believe that their e-commerce platform and focus on efficient distribution will allow them to fully exploit the potential of the European market. This investment fits perfectly with our strategy of supporting fast-growing B2B technology companies with strong market potential and a product that precisely matches customer requirements.”
- The money will help IAG grow in the European automotive aftermarket, improve its e-catalog services, and make logistics and invoicing easier.
- International Automotive Group (IAG) helps garages get spare parts faster and easier through a digital platform.
- From 2022 to 2024, IAG’s revenue grew more than five times.
- Kamil Levinsky, Executive Director of Jet Ventures, says, “We are excited to support the IAG team and its innovative strategy. We believe that their e-commerce platform and focus on effic
… [skrátené, 1779 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c011.json <<'EOF'
{
  "candidate_id": "c011",
  "name": "Venture to Future Fund",
  "legal_name": "Venture to Future Fund, a.s.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ"],
  "website": "https://vff.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://vff.sk/", "source_date": null, "quote": "Sme slovenský venture kapitálový fond so zameraním na podporu inovatívnych lokálnych podnikov."},
  "investor_type": {"value": "public_fund", "source_url": "https://vff.sk/novinky/cesky-startup-patron-go-ziskava-investiciu-v-hodnote-1-milion-eur-30", "source_date": "2024-08-14", "quote": "Fond s počiatočným kapitálom 40,4 miliónov eur bol založený v roku 2019 ako výsledok spoločnej iniciatívy Európskej investičnej banky a Ministerstva financií SR prostredníctvom Slovak Investment Holding."},
  "sectors": null,
  "stages": {"value": ["seed", "series-a", "series-b-plus"], "source_url": "https://vff.sk/", "source_date": null, "quote": "Cielime na malé a stredné podniky v rastovej fáze od neskoršieho Seed kola po Series A,B s aspoň čiastočne funkčným produktom, ktorý je životaschopný, bol otestovaný na trhu a má už prvých platiacich zákazníkov alebo dojednané zmluvné vzťahy."},
  "ticket_min": {"amount": 400000, "currency": "EUR", "source_url": "https://vff.sk/", "source_date": null, "quote": "Minimálna výška našej investície je 400tis. EUR, aj keď optimálne investujeme medzi 1,5 – 2,0 mil. EUR."},
  "ticket_max": {"
… [skrátené, 3925 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c011.json
c011.json entity_kind OK
c011.json investor_type OK
c011.json stages OK
c011.json ticket_min OK
c011.json ticket_max OK
c011.json aum OK
c011.json inv:Talentiqa OK
c011.json inv:Patron GO OK
c011.json inv:Spinbotics OK
```

</details>

**Nástroj `Bash`**

```bash
python3 - <<'EOF'
import json
p="research/c011.json"; d=json.load(open(p))
d["investments"][1]["quote"]="Najnovšia investícia do startupu Patron GO, chytrej aplikácie na optimalizáciu osobných financií, prichádza zo Slovenska. Slovenský fond Venture to Future Fund sa vo štvrtom investičnom kole pridáva k ďalším investorom a do aplikácie spoločne vkladajú celkom 1 milión eur."
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c011.json && python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c011.json | grep Patron
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c011.json
c011.json inv:Patron GO OK
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.visionventures.vc/ | grep -oE "href=['\"][^'\"]*['\"]" | sort -u | grep -vE 'css|\.js|fonts|\.png|\.jpg|\.svg|wp-' | head -40; python3 -I $S/page.py show https://www.visionventures.vc/ 12000 | awk 'length($0)>40' | sed -n '1,40p'
```

<details><summary>Výstup nástroja</summary>

```
href="/#about-us"
href="#contact-us"
href="#content"
href="#elementor-action%3Aaction%3Dpopup%3Aclose%26settings%3DeyJkb19ub3Rfc2hvd19hZ2FpbiI6IiJ9"
href="#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6IjU0NyIsInRvZ2dsZSI6ZmFsc2V9"
href="https://biteberry.com"
href="https://cequence.io/"
href="https://gmpg.org/xfn/11"
href="https://seerlinq.com"
href="https://spinbotics.com/"
href="https://visionventures.vc/"
href="https://visionventures.vc/comments/feed/"
href="https://visionventures.vc/feed/"
href="https://visionventures.vc/portfolio-companies/"
href="https://visionventures.vc/xmlrpc.php?rsd"
href="https://www.airvolute.com/"
href="https://www.closerocket.com"
href="https://www.crunchbase.com/organization/vision-ventures-9b12"
href="https://www.linkedin.com/company/visionventures/"
href="https://www.linkedin.com/in/gabriel-horvath-cfa-a63722a1/"
href="https://www.linkedin.com/in/jakubdvorsky/"
href="https://www.linkedin.com/in/tomas-bel-44212026/"
href="https://www.sloneek.com/"
href="https://www.tramatm.com/"
href="mailto:[email]"
href="/#our-strategy"
href="/#portfolio"
href="/#team"
Supporting courageous and passionate entrepreneurs with bold ambitions to build a business on a global scale.
VC fund focused on pre-seed and seed investments in Slovakia.
We invest in Slovak's most ambitious start-ups:
Vision Ventures is a VC investor focused on pre-seed and seed investments in Slovakia, providing investment up to EUR 1.6 million. We support c
… [skrátené, 9417 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Vision Ventures\" investícia startup Seerlinq OR Airvolute OR Spinbotics OR BiteBerry OR Cequence", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Vision Ventures" investícia startup Seerlinq OR Airvolute OR Spinbotics OR BiteBerry OR Cequence"

Links: [{"title":"vision ventures","url":"https://www.vcbacked.co/directory/investors/vision-ventures"},{"title":"Vision Ventures (Slovakia) Overview","url":"https://pitchbook.com/profiles/investor/436353-58"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/browse/v?page=2"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/sector/ai-deep-tech?page=53"},{"title":"VISION VENTURES","url":"https://app.mergerlinks.com/companies/envision-ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/vision-ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/vision-venture-partners"},{"title":"Back to Vision Ventures","url":"https://seedtable.com/investors/vision-ventures/portfolio"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/vision-ventures-2"}]

I found investment records for four of the five companies, all tied to the Slovak firm Vision Ventures. I found nothing on Spinbotics.

**The firm:** PitchBook describes Vision Ventures (Slovakia) as a venture capital investment firm based in Bratislava, Slovakia, founded in 2019, and says the firm prefers to invest in early-stage and seed-stage companies. Waveup says it primarily invests in pre-seed and seed rounds, with an average check size of up to EUR 1.6 million.

**The companies:**
- **
… [skrátené, 3035 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Cequence slovenský startup investícia Vision Ventures 2023", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Seerlinq získal investíciu Vision Ventures", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Cequence slovenský startup investícia Vision Ventures 2023"

Links: [{"title":"Vision Ventures (Slovakia) Overview","url":"https://pitchbook.com/profiles/investor/436353-58"},{"title":"vision ventures","url":"https://vestbee.com/vc-list/vision-ventures"},{"title":"Česko-slovenský startup Sloneek nabírá miliony od Vision Ventures. Se svým personálním systémem míří do Evropy","url":"https://cc.cz/cesko-slovensky-startup-sloneek-nabira-miliony-od-vision-ventures-se-svym-personalnim-systemem-miri-do-evropy/"},{"title":"Venture Capital","url":"https://altss.com/profile/vision-ventures-slovakia"},{"title":"Slovenské startupy dobýjajú svet: 5 firiem, ktoré pomocou AI a dát menia obchod aj vesmír","url":"https://www.startitup.sk/?p=1066829"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/cequence"},{"title":"Česko-slovenský startup Sloneek nabírá miliony od Vision Ventures. Se svým personálním systémem míří do Evropy","url":"https://cc.cz/2020/11/cesko-slovensky-startup-sloneek-nabira-miliony-od-vision-ventures-se-svym-personalnim-systemem-miri-do-evropy/"},{"title":"slovakia cequence secures 2m","url":"https://siliconcanals.com/slovakia-cequence-secures-2m/"},{"title":"vision ventures","url":"https://prod.actual.seedtable.com/investors/vision-ventures"}]

The search supports a Vision Ventures investment in Cequence in late 2023, but the sources don't give the amount or any details of that round.

- **The 2023 deal:** PitchBook's prof
… [skrátené, 3001 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Seerlinq získal investíciu Vision Ventures"

Links: [{"title":"Vision Ventures (Slovakia) Overview","url":"https://pitchbook.com/profiles/investor/436353-58"},{"title":"vision ventures","url":"https://seedtable.com/investors/vision-ventures"},{"title":"Vision Ventures","url":"https://privateequitylist.com/investors/vision-ventures"},{"title":"Vision Ventures","url":"https://privateequitylist.com/investor/vision-ventures"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/vision-ventures"},{"title":"VISION VENTURES","url":"https://app.mergerlinks.com/companies/envision-ventures"},{"title":"vision ventures","url":"https://vestbee.com/vc-list/vision-ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/vision-ventures"},{"title":"Vision Ventures (Seoul) Overview","url":"https://pitchbook.com/profiles/investor/512540-11"},{"title":"SVC invests $15m in Vision Ventures to fuel startups","url":"https://arab.news/bmusm"}]

Links: [{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/seerlinq"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/seerlinq/financials"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/seer/financials"},{"title":"Seer Funding History","url":"https://www.owler.com/company/seer/funding"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/linqalpha"},{"title":"2023 10 01 seerai seed","url":"https://startupintros.com/news/202
… [skrátené, 3509 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Spinbotics investícia Vision Ventures Venture to Future Fund 2024", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "BiteBerry startup investícia Vision Ventures", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Spinbotics investícia Vision Ventures Venture to Future Fund 2024"

Links: [{"title":"sih.sk","url":"https://sih.sk/en/portfolio/spinbotics"},{"title":"Compare Artimus Robotics vs Spinbiotics","url":"https://www.cbinsights.com/compare/artimus-robotics-vs-spinbiotics"},{"title":"Compare Spinbiotics vs ZeroErr Inside","url":"https://www.cbinsights.com/compare/spinbiotics-vs-zeroerr-inside"},{"title":"denmark.dealroom.co","url":"https://denmark.dealroom.co/companies/spinbotics"},{"title":"cednc.dealroom.co","url":"https://cednc.dealroom.co/companies/spinbotics"},{"title":"spin robotics","url":"https://www.cbinsights.com/company/spin-robotics"},{"title":"About Spinbotics","url":"https://crustdata.com/profiles/company/spinbotics"},{"title":"SpinEM Robotics logo","url":"https://www.seedtable.com/startups/spinem-robotics"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/company/spin-robotics"}]

The search confirms the April 2020 investment, but it doesn't mention a "Venture to Future Fund" or any 2024 round.

**The Slovak Investment Holding investment (2020):** The Slovak Investment Holding's portfolio page says that in April 2020, SIH, with the help of the financial intermediary Vision Ventures, used part of the funds it administers under NDF II to invest in Spinbotics. The money came from a financial instrument meant to support businesses in the early stage of their life cycle. The pa
… [skrátené, 2756 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "BiteBerry startup investícia Vision Ventures"

Links: [{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/biteberry"},{"title":"Vision Ventures (Slovakia) Overview","url":"https://pitchbook.com/profiles/investor/436353-58"},{"title":"Compare BiteBerry vs Eatster","url":"https://www.cbinsights.com/compare/biteberry-vs-eatster"},{"title":"Compare BiteBerry vs Choco","url":"https://www.cbinsights.com/compare/biteberry-vs-choco"},{"title":"Back to Vision Ventures","url":"https://seedtable.com/investors/vision-ventures/portfolio"},{"title":"Vision Ventures Investor","url":"https://mindmaps.femtech.health/firms/6969"},{"title":"15111 havel partners advises vision ventures on investment in eatster","url":"https://ceelegalmatters.com/slovakia/15111-havel-partners-advises-vision-ventures-on-investment-in-eatster"},{"title":"new pe firm vision venture partners debuts 20170414574","url":"https://www.thetrustedinsight.com/investment-news/new-pe-firm-vision-venture-partners-debuts-20170414574/"},{"title":"Portfolio Companies","url":"https://seedtable.com/investors/blueberry-ventures"},{"title":"blueberry ventures blueberryventures vc","url":"https://venturecapitalarchive.com/venture-funds/blueberry-ventures-blueberryventures-vc"}]

Vision Ventures is listed as an investor in BiteBerry, but the sources disagree on the round size and date.

- **Investor link:** VCBacked names Vision Ventures as one of BiteBerry's investors. BiteBerry's investors
… [skrátené, 3093 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://sih.sk/en/portfolio/spinbotics 'Vision'; python3 -I $S/page.py grep https://ceelegalmatters.com/slovakia/15111-havel-partners-advises-vision-ventures-on-investment-in-eatster 'Vision|Eatster|20[0-9]{2}' | head -8
```

<details><summary>Výstup nástroja</summary>

```
- Havel & Partners Advises Vision Ventures on Investment in Eatster | CEE Legal Matters
- October 9, 2026
- October 9, 2026
- October 9, 2026
- October 9, 2026
- October 9, 2026
- October 9, 2026
- October 8, 2026
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://ceelegalmatters.com/slovakia/15111-havel-partners-advises-vision-ventures-on-investment-in-eatster 'Eatster' | head -8; python3 -I $S/page.py show https://sih.sk/en/portfolio/spinbotics 3000 | tail -20
```

<details><summary>Výstup nástroja</summary>

```
- Havel & Partners Advises Vision Ventures on Investment in Eatster | CEE Legal Matters
- Havel & Partners Advises Vision Ventures on Investment in Eatster
- Havel & Partners has advised Vision Ventures on its venture capital investment in Slovakian start-up Eatster, which operates an online food order application.
An Error Occurred: Internal Server Error
Oops! An Error Occurred
The server returned a "500 Internal Server Error".
Something is broken. Please let us know what you were doing when this error occurred.
We will fix it as soon as possible. Sorry for any inconvenience caused.
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://ceelegalmatters.com/slovakia/15111-havel-partners-advises-vision-ventures-on-investment-in-eatster | grep -oE '(published_time|datePublished|dateCreated)"?[^,>]{0,50}' | head -3; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://sih.sk/en/portfolio/spinbotics -o /dev/null -w '%{http_code}\n'; curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://www.sih.sk/en/portfolio/spinbotics -o /dev/null -w '%{http_code}\n'
```

<details><summary>Výstup nástroja</summary>

```
published_time" content="2020-11-17T15:25:10+00:00" /
datePublished":"2020-11-17T15:25:10+00:00"
datePublished":"2020-11-17T15:25:10+00:00"
200
200
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" https://sih.sk/en/portfolio/spinbotics | python3 -c "
import sys,re,html
s=sys.stdin.read(); s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>','\n',s))
for l in t.split('\n'):
  l=' '.join(l.split())
  if 'Vision' in l or 'April' in l or 'Error' in l: print('-',l)
"
```

<details><summary>Výstup nástroja</summary>

```
- An Error Occurred: Internal Server Error
- Oops! An Error Occurred
- The server returned a "500 Internal Server Error".
```

</details>

**Nástroj `Bash`**

```bash
for u in https://www.sih.sk/portfolio/spinbotics https://sih.sk/sk/portfolio/spinbotics https://www.sih.sk/en/portfolio/spinbotics-s-r-o; do echo "$u $(curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36' $u | grep -c 'Vision')"; done
```

<details><summary>Výstup nástroja</summary>

```
https://www.sih.sk/portfolio/spinbotics 0
https://sih.sk/sk/portfolio/spinbotics 3
https://www.sih.sk/en/portfolio/spinbotics-s-r-o 0
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://sih.sk/sk/portfolio/spinbotics 'Vision|20[12][0-9]'; curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36' https://sih.sk/sk/portfolio/spinbotics | grep -oE "href=['\"][^'\"]*portfolio[^'\"]*['\"]" | sort -u | head -80 | wc -l
```

<details><summary>Výstup nástroja</summary>

```
ERR <HTTPError 404: 'Not Found'>
0
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36' -w '\nCODE %{http_code} %{url_effective}\n' https://sih.sk/sk/portfolio/spinbotics | python3 -c "
import sys,re,html
s=sys.stdin.read(); print(s[-200:]); s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>','\n',s))
for l in t.split('\n'):
  l=' '.join(l.split())
  if 'Vision' in l: print('-',l[:500])
"
```

<details><summary>Výstup nástroja</summary>

```
             }
         }
     });
    
    $('#c-txt #cc-settings-btn').prependTo($('#c-inr #c-bns'));
});
//]]>
</script>

</body>
</html>
CODE 404 https://www.sih.sk/sk/portfolio/spinbotics

- Slovak Investment Holding je investorom vo fonde spravovanom spoločnosťou Vision Ventures, ktorá nesie plnú zodpovednosť za jeho riadenie a realizáciu investičnej stratégie. Fond bol založený ako časovo ohraničený investičný nástroj s predpokladanou dobou trvania 10 rokov, pričom svoju činnosť začal v roku 2020 a investičné obdobie ukončil v decembri 2023.
- VisionFlow je slovenská technologická spoločnosť vyvíjajúca platformu pre správu dátového životného cyklu v oblasti počítačového videnia. Riešenie pokrýva výber a spracovanie dát, anotáciu, kontrolu kvality, verziovanie datasetov a auditovateľnosť dátových procesov. Platformu je možné nasadiť v privátnom cloude aj priamo v infraštruktúre zákazníka. VisionFlow reaguje na rastúcu potrebu firiem efektívne pripravovať a spravovať kvalitné dáta, ktoré sú základom spoľahlivých AI riešení. Platforma um
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "sih.sk Vision Ventures fond investičné obdobie ukončil v decembri 2023", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "sih.sk Vision Ventures fond investičné obdobie ukončil v decembri 2023"

Links: [{"title":"vision ventures kapitalova investicia","url":"https://sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/vision-ventures-kapitalova-investicia"},{"title":"Fund profile","url":"https://hub.waveup.com/funds/vision-ventures"},{"title":"the vision funds investment pace slows","url":"https://news.crunchbase.com/venture/the-vision-funds-investment-pace-slows"},{"title":"SIH boosts support for Slovak start-up businesses","url":"https://www.sih.sk/en/aktuality/sih-boosts-support-for-slovak-start-up-businesses"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/vision-ventures"},{"title":"Crowdberry, Zero Gravity Ventures, and Vision Ventures to invest state money into Slovak start-ups","url":"https://www.symsite.sk/single-post/2019/10/08/crowdberry-zero-gravity-ventures-and-vision-ventures-to-invest-state-money-into-slovak-st"},{"title":"vision ventures","url":"https://vestbee.com/vc-list/vision-ventures"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/visionvc"},{"title":"vision venture capital","url":"https://startupintros.com/orgs/vision-venture-capital"},{"title":"vision ventures","url":"https://prod.actual.seedtable.com/investors/vision-ventures"}]

Zdroje potvrdzujú plánovaný koniec investičného obdobia v roku 2023, ale nepotvrdzujú, že
… [skrátené, 2898 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py show https://sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/vision-ventures-kapitalova-investicia 20000 | awk 'length($0)>30' | grep -viE 'cookie' | head -60
```

<details><summary>Výstup nástroja</summary>

```
Vision Ventures | Slovak Investment Holding, a. s.
Slovak Investment Holding is an investor in the fund managed by Vision Ventures, which bears sole responsibility for its management and the execution of its investment strategy. The fund was designed as a fixed-term investment vehicle with an anticipated duration of 10 years; it launched operations in 2020 and finalised its investment period in December 2023.
Over the course of the investment period, capital was aimed at supporting early-stage startups, particularly enterprises up to five years post-incorporation, alongside micro and small businesses with strong scaling potential. The deployed investments drove the development of innovative business projects and unlocked new opportunities within the entrepreneurial ecosystem.
The fund is currently its divestment phase, with the manager progressively winding down holdings and returning capital to its investors.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Seerlinq Trnava startup investícia 2023 fond", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://cc.cz/cesko-slovensky-startup-sloneek-nabira-miliony-od-vision-ventures-se-svym-personalnim-systemem-miri-do-evropy/ 'Vision Ventures' | head -5; curl -sL -A "Mozilla/5.0" https://cc.cz/cesko-slovensky-startup-sloneek-nabira-miliony-od-vision-ventures-se-svym-personalnim-systemem-miri-do-evropy/ | grep -oE 'datePublished"?[^,]{0,40}' | head -1
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Seerlinq Trnava startup investícia 2023 fond"

Links: [{"title":"Crowdberry, Zero Gravity Ventures, and Vision Ventures to invest state money into Slovak start-ups","url":"https://www.symsite.sk/single-post/2019/10/08/crowdberry-zero-gravity-ventures-and-vision-ventures-to-invest-state-money-into-slovak-st"},{"title":"venture to future fund a s","url":"https://superscout.co/investor/venture-to-future-fund-a-s"},{"title":"top of page","url":"https://www.symsite.sk/single-post/2019/12/18/the-state-will-seek-start-ups-outside-bratislava"},{"title":"venture capital firms bratislava","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava.md"},{"title":"The state will seek start ups outside Bratislava","url":"https://www.symsite.sk/single-post/2019/12/18/The-state-will-seek-start-ups-outside-Bratislava"},{"title":"Equity financing for innovative startups with growth potential","url":"https://www.podjetniskisklad.si/?p=18859"},{"title":"Na obnovu Linčianskej získala Trnava prvé milióny z ministerstva investícií","url":"https://sita.sk/na-obnovu-lincianskej-ziskala-trnava-prve-miliony-z-ministerstva-investicii/"},{"title":"Interview with Michal Nešpor","url":"https://www.fi-compass.eu/video/interview-michal-nespor?page=1"},{"title":"Subscribe to Our Newsletter","url":"https://techloy.com/zero-one-hundred-fund-to-invest-in-cee-startups"}]

I couldn't find any information about a company called Seerlinq, whether it is based in Trnava, or a
… [skrátené, 2978 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
- Česko-slovenský startup Sloneek nabírá miliony od Vision Ventures. Se svým personálním systémem míří do Evropy - CzechCrunch
- Česko-slovenský startup Sloneek nabírá miliony od Vision Ventures. Se svým personálním systémem míří do Evropy
- Foto: Vision Ventures
- Partneři slovenského VC fondu Vision Ventures Tomáš Bél a Gabriel Horváth
- S novým názvem a teď už jako online systém pro řízení personální agendy zejména v malých a středních podnicích Sloneek získal investici 350 tisíc eur (9,5 milionu korun) od slovenského venture kapitálového fondu Vision Ventures výměnou za dvacetiprocentní podíl ve firmě. Peníze poslouží především pro dokončení technologického přerodu aplikace, startup je ovšem použije i pro vstup na evropský trh.
datePublished":"2020-11-04T12:33:42+01:00"
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Airvolute drony investícia Vision Ventures", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Airvolute drony investícia Vision Ventures"

Links: [{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/baryon-investment-fund-backs-slovak-drone-tech-startup-airvolute-1"},{"title":"top of page","url":"https://www.symsite.sk/single-post/airvolute-makes-components-for-autonomous-drones-and-plans-to-expand"},{"title":"Airvolute logo — AI-powered autonomous unmanned solutions","url":"https://bouncewatch.com/company/airvolute"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/airvolute"},{"title":"Compare Airvolute vs DIY Drones","url":"https://www.cbinsights.com/compare/airvolute-vs-diy-drones"},{"title":"Compare Airvolute vs SOOMVI","url":"https://www.cbinsights.com/compare/airvolute-vs-soomvi"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/airvolute"},{"title":"Compare Airvolute vs AVIDRONE Aerospace","url":"https://www.cbinsights.com/compare/airvolute-vs-avidrone-aerospace"},{"title":"Compare Airvolute vs XTEND","url":"https://www.cbinsights.com/compare/airvolute-vs-xtend"},{"title":"Compare Airvolute vs Cambium","url":"https://www.cbinsights.com/compare/airvolute-vs-cambium-biomaterials"}]

Airvolute je slovenský hĺbkovo-technologický (deep tech) startup z Trnavy, ktorý vyvíja hardvér a softvér pre autonómne drony. Vision Ventures do firmy investoval v niekoľkých kolách, no údaje o sumách sa v zdrojoch líšia.

**Investície Vision Ventures**
- Podľa Symsite z septembra 2024 fond Vision
… [skrátené, 2929 znakov]
```

</details>

**Nástroj `Bash`**

```bash
S=/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools; python3 -I $S/page.py grep https://www.symsite.sk/single-post/airvolute-makes-components-for-autonomous-drones-and-plans-to-expand 'Vision|2024|2023'
```

<details><summary>Výstup nástroja</summary>

```
- Sep 3, 2024
- Airvolute (Lukáš Palkovič and Jozef Rodina) makes components for autonomous drones. It employs 21 developers who are perfecting, for example, control units for drones that allow them to fly without GPS. Major customers include Quantum Systems, Tekever, and the armies of NATO countries. Over three years, it has raised €1.6m from Vision Ventures, a Slovak fund, in the form of equity and debt. It will launch another investment round in the second half of this year.
```

</details>

**Nástroj `Bash`**

```bash
cat > /home/filip/investor-db/research/c012.json <<'EOF'
{
  "candidate_id": "c012",
  "name": "Vision Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://visionventures.vc/",
  "entity_kind": {"value": "investor", "source_url": "https://www.visionventures.vc/", "source_date": null, "quote": "Vision Ventures is a VC investor focused on pre-seed and seed investments in Slovakia, providing investment up to EUR 1.6 million."},
  "investor_type": {"value": "vc", "source_url": "https://www.visionventures.vc/", "source_date": null, "quote": "Vision Ventures is a VC investor focused on pre-seed and seed investments in Slovakia, providing investment up to EUR 1.6 million."},
  "sectors": null,
  "stages": {"value": ["pre-seed", "seed"], "source_url": "https://www.visionventures.vc/", "source_date": null, "quote": "Vision Ventures is a VC investor focused on pre-seed and seed investments in Slovakia, providing investment up to EUR 1.6 million."},
  "ticket_min": {"amount": 100000, "currency": "EUR", "source_url": "https://www.visionventures.vc/", "source_date": null, "quote": "We usually make investments between €100 thousand and €800 thousand, maximum up to €1,6 million."},
  "ticket_max": {"amount": 800000, "currency": "EUR", "source_url": "https://www.visionventures.vc/", "source_date": null, "quote": "We usually make investments between €100 thousand and €800 thousand, maximum up to €1,6 million."},
  "aum": null,
  "f
… [skrátené, 3271 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c012.json
c012.json entity_kind OK
c012.json investor_type OK
c012.json stages OK
c012.json ticket_min OK
c012.json ticket_max OK
c012.json inv:Eatster OK
c012.json inv:Sloneek OK
```

</details>

**Nástroj `Bash`**

```bash
for i in $(seq -w 1 12); do PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c0$i.json; done; python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/r1/tools/verify.py research/c0{01,02,03,04,05,06,07,08,09,10,11,12}.json | grep -vc ' OK$'
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c001.json
OK    research/c002.json
OK    research/c003.json
OK    research/c004.json
OK    research/c005.json
OK    research/c006.json
OK    research/c007.json
OK    research/c008.json
OK    research/c009.json
OK    research/c010.json
OK    research/c011.json
OK    research/c012.json
0
```

</details>

**Nástroj `SendMessage`**

```json
{"to": "team-lead", "summary": "Report c001-c012 hotový", "message": "c001–c012 sú hotové: 12 súborov v /home/filip/investor-db/research/, všetky prešli check-schema OK a všetky citáty som overil proti statickému HTML (0 chýbajúcich).\n\nid | entity_kind | type | #investments | missing fields\nc001 ARX Equity Partners | investor | pe | 3 (2026) | sectors, ticket_min/max, legal_name, reg_no\nc002 CVI | lender | – | 0 | všetky investorské polia (private debt)\nc003 Enterprise Investors | investor | pe | 3 (2026) | aum, legal_name, reg_no\nc004 Eterus Capital | investor | pe | 3 (2023-05 až 2024-08) | sectors, aum, funds\nc005 Fond inovácií a technológií | investor | public_fund | 3 (2014–2015) | aum, funds\nc006 Genesis Capital | investor | pe | 3 (2025-11 až 2026-04) | sectors, stages\nc007 Jet Investment | investor | pe | 3 (2026-09) | stages\nc008 Národný holdingový fond | investor | public_fund | 0 | aum, investments\nc009 Neulogy Ventures | investor | vc | 2 (2024) | funds, legal_name\nc010 Sandberg Capital | investor | pe | 3 (2025-12 až 2026-08) | ticket_min\nc011 Venture to Future Fund | investor | public_fund | 3 (2024-04 až 2025-09) | sectors\nc012 Vision Ventures | investo
… [skrátené, 3092 znakov]
```

<details><summary>Výstup nástroja</summary>

```
{"success":true,"message":"Message sent to team-lead's inbox","msg_id":"cb4940bb-b5bd-4c17-8377-056fcfd3bb4b","routing":{"sender":"research-1","senderColor":"blue","target":"@team-lead","targetColor":"red","summary":"Report c001-c012 hotový","content":"c001–c012 sú hotové: 12 súborov v /home/filip/inv…"}}
```

</details>

## Claude · 2026-10-09 12:36:02 UTC

c001–c012 sú hotové: 12 súborov `/home/filip/investor-db/research/c001.json` až `c012.json`. Všetky prešli `check-schema` (OK). Každý citát som overil proti statickému HTML stránky zo `source_url` a žiadny nechýba. Rovnaký report som poslal team-leadovi.

| id | entity_kind | type | #investments | missing fields |
|---|---|---|---|---|
| c001 ARX Equity Partners | investor | pe | 3 (2026) | sectors, ticket_min/max |
| c002 CVI | lender | – | 0 | všetky investorské polia |
| c003 Enterprise Investors | investor | pe | 3 (2026) | aum |
| c004 Eterus Capital | investor | pe | 3 (2023-05 až 2024-08) | sectors, aum |
| c005 Fond inovácií a technológií | investor | public_fund | 3 (2014–2015) | aum |
| c006 Genesis Capital | investor | pe | 3 (2025-11 až 2026-04) | sectors, stages |
| c007 Jet Investment | investor | pe | 3 (2026-09) | stages |
| c008 Národný holdingový fond | investor | public_fund | 0 | aum, investments |
| c009 Neulogy Ventures | investor | vc | 2 (2024) | funds |
| c010 Sandberg Capital | investor | pe | 3 (2025-12 až 2026-08) | ticket_min |
| c011 Venture to Future Fund | investor | public_fund | 3 (2024-04 až 2025-09) | sectors |
| c012 Vision Ventures | investor | vc | 2 (2020) | sectors, aum |

**V čom som si nebol istý:**
- **c002 CVI** som zaradil ako `lender`. Robí hlavne private debt, ale aj mezanín a výnimočne menšinový podiel vo firme.
- **c005 FIT a c011 VFF** som zaradil ako `public_fund`, nie `vc`. FIT vlastní štát väčšinovo cez SBA. VFF financuje EIB a ministerstvo financií cez SIH.
- **c008 NHF** podľa svojho webu spravuje Eterus (c004) aj FIT (c005). `duplicate_of` som nevyplnil, lebo by sa týkal dvoch kandidátov naraz. Web NHF môže byť zastaraný, Eterus má dnes kontakty na wood.com.
- **Asi už neinvestujú:**
  - c005 je od roku 2025 v post-investičnej fáze.
  - c012 podľa SIH ukončil investičné obdobie v decembri 2023.
  - c008 nemá žiadny datovaný obchod.
  - Pri c010 bol Carrot (august 2026) posledným obchodom fondu SIF II.
- **Výška investície (ticket):**
  - Pri c001 som ju vynechal. SLOVCA uvádza 10–50 mil. EUR ako výšku investície, ale web ARX tak opisuje hodnotu firmy.
  - Pri c010 je len horná hranica 50 mil. EUR z ich webu, SLOVCA uvádza 4–15 mil. EUR.
- **AUM:** pri c006 je to veľkosť najnovšieho fondu GPEF V, nie celej firmy. Pri c007 je to 17 mld. CZK vrátane realitného fondu a ešte nevyčerpaného kapitálu.
- **Slabšie zdroje obchodov:**
  - Pri c004 je obchod z Oaklins a pri c009 z PrivSource a life-sciences-europe.com. Ide o agregátory a weby tretích strán, nie o vlastné tlačové správy fondov.
  - c004 EC Pharmacies a c003 18GYM majú dátum len na úrovni mesiaca.
- **SK v active_in:** pri c003 a c007 je len na základe profilu na SLOVCA, nedávny slovenský obchod som nenašiel. Pri c001 som SK nedal, lebo ARX v zozname investícií nemá žiadnu slovenskú firmu.

Scratchpad zdieľajú všetci research agenti a jeden z nich mi prepísal pomocný skript. Moje nástroje sú preto osobitne v `scratchpad/r1/`.
