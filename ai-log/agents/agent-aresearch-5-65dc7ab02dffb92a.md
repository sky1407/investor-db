# Subagent agent-aresearch-5-65dc7ab02dffb92a

Zdroj: transkript Claude Code `agent-aresearch-5-65dc7ab02dffb92a.jsonl`

## Používateľ · 2026-10-09 12:20:03 UTC

<teammate-message teammate_id="team-lead" summary="Research candidates c061-c075">
You are a research agent for the project in /home/filip/investor-db. Read /home/filip/investor-db/prompts/research_agent.md first and follow it exactly. Candidate list: /home/filip/investor-db/data/candidates.csv (columns: candidate_id, name, discovery_source, discovery_url).

Your assigned candidates: c061 to c075 (inclusive). They come from news about investment rounds and from aggregator lists, so some may be foreign funds active in Slovakia (set country by HQ and add SK to active_in), accelerators, or not investors at all. Check the whole candidates.csv for duplicates.

Use WebSearch and WebFetch to find sources. Write one JSON file per candidate to /home/filip/investor-db/research/<candidate_id>.json. Do not touch any other files. Validate each file with:
cd /home/filip/investor-db && PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/<id>.json

Remember: quotes must be verbatim from the page text at source_url (a script will check it); missing data is better than wrong data. Finish with the one-line-per-candidate report described in the instructions, plus a short list of anything you were unsure about.
</teammate-message>

**Nástroj `Bash`**

```bash
cat /home/filip/investor-db/prompts/research_agent.md; echo ----; sed -n '1p;62,76p' /home/filip/investor-db/data/candidates.csv; ls /home/filip/investor-db/research | head -50
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
… [skrátené, 7227 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cut -d, -f1,2 data/candidates.csv | grep -iE "simpact|espri|soci|j&t|j\&t|ipm|bic|365|mcwin|ergos|jet|look|presto|fil rouge|gi21|jic"; ls research; ls src/investordb
```

**Nástroj `ToolSearch`**

```json
{"query": "select:WebSearch,WebFetch", "max_results": 2}
```

<details><summary>Výstup nástroja</summary>

```
c007,Jet Investment
c048,J&T ARCH Investments
c061,Simpact VC
c062,CB ESPRI
c063,Sociálni Inovátori Impact Capital
c064,J&T Ventures
c065,IPM Group
c066,BIC Bratislava
c067,365fintech
c068,McWin
c069,Ergos
c070,Jet Ventures
c071,Look AI Ventures
c072,Presto Ventures
c073,Fil Rouge Capital
c074,Gi21 Capital
c075,JIC Ventures
__init__.py
__pycache__
cli.py
io.py
models.py
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; grep -n "def \|add_parser\|add_argument" src/investordb/cli.py | head -40; ls; ls scripts 2>/dev/null
```

<details><summary>Výstup nástroja</summary>

```
Exit code 2
10:def cmd_check_schema(args: argparse.Namespace) -> int:
23:def build_parser() -> argparse.ArgumentParser:
26:    check = sub.add_parser("check-schema", help="validate research JSON files")
27:    check.add_argument("paths", nargs="+")
32:def main(argv: list[str] | None = None) -> int:
PLAN.md
data
prompts
pyproject.toml
raw
research
src
tests
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; .venv/bin/python -c "import bs4, httpx" ; .venv/bin/pip list 2>/dev/null | head -30; cat PLAN.md | head -60
```

<details><summary>Výstup nástroja</summary>

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import bs4, httpx
ModuleNotFoundError: No module named 'bs4'
# Plán: spoľahlivá databáza investorov

Stav k 2026-10-09. Pilot: VC fondy pôsobiace na Slovensku.

## 1. Kto v databáze je a kto nie

### Definícia investora

Subjekt je **investor**, ak súčasne platí:

1. **Kapitál:** investuje vlastný kapitál alebo kapitál, ktorý spravuje v mene investorov (LP).
2. **Nástroj:** investuje do **súkromných firiem** formou vlastníckeho podielu alebo kvázi-equity (konvertibilná pôžička, SAFE).
3. **Opakovanosť:** má investičnú stratégiu alebo aspoň 2 verejne doložené investície.
4. **Aktivita:** má aspoň 1 verejne doloženú investíciu alebo nový fond za posledných **36 mesiacov**. Overuje sa ku dňu zberu.

### Typy (pole `investor_type`)

| Typ | Kritérium navyše |
|---|---|
| `vc` | Investuje do fáz pre-seed až growth, typicky menšinový podiel |
| `pe` | Buyout alebo growth, typicky väčšinový či významný podiel, etablované firmy |
| `cvc` | Korporátna investičná jednotka so samostatnou značkou alebo mandátom |
| `family_office` | Spravuje majetok jednej (SFO) alebo viacerých (MFO) rodín a priamo investuje do firiem |
| `angel` | Fyzická osoba, aspoň 2 doložené investície vlastnými peniazmi |
| `private_investor` | Súkromný investičný holding alebo jednotlivec s veľkým kapitálom, ktorý nespadá do typov vyššie |
| `public_fund` | Štátny alebo nadnárodný fond, ktorý **priamo** investuje equity do firiem (SIH, N
… [skrátené, 3750 znakov]
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/{bin,pages}; cat > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py <<'EOF'
import sys, subprocess, hashlib, re, html
from html.parser import HTMLParser
D="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/pages/"
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.t=[]; s.skip=0
    def handle_starttag(s,tag,a):
        if tag in("script","style","noscript"): s.skip+=1
        if tag in("p","div","br","li","h1","h2","h3","h4","tr","section","article"): s.t.append("\n")
    def handle_endtag(s,tag):
        if tag in("script","style","noscript") and s.skip: s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.t.append(d)
def get(url):
    f=D+hashlib.md5(url.encode()).hexdigest()+".txt"
    try: return open(f).read()
    except FileNotFoundError: pass
    raw=subprocess.run(["curl","-sL","--max-time","30","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",url],capture_output=True).stdout.decode("utf-8","replace")
    p=P(); p.feed(raw); t="".join(p.t)
    t=re.sub(r"[ \t\xa0]+"," ",t); t=re.sub(r"\n\s*\n+","\n",t)
    open(f,"w").write(t); return t
if sys.argv[1]=="get":
    t=get(sys.argv[2]); print(t if len(sys.argv)<4 else "\n".join(l for l in t.splitlines() if re.search(sys.argv[3],l,re.I)))
elif sys.argv[1]=="check":
    import json
    norm=lambda x:
… [skrátené, 1838 znakov]
```

<details><summary>Výstup nástroja</summary>

```
ok
```

</details>

## Claude · 2026-10-09 12:20:31 UTC

Začnem so Simpact VC.

**Nástroj `WebSearch`**

```json
{"query": "Simpact VC fund Slovakia investment", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "CB ESPRI fond sociálna ekonomika Sociálni Inovátori Impact Capital", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Simpact VC fund Slovakia investment"

Links: [{"title":"simpact ventures simpact vc","url":"https://venturecapitalarchive.com/venture-funds/simpact-ventures-simpact-vc"},{"title":"1,1 mld złotych na inwestycje kapitałowe także w polskie spółki","url":"https://bank.pl/?p=432154"},{"title":"Join Vestbee","url":"https://www.vestbee.com/vc-list/simpact-ventures"},{"title":"Release date: 16 October 2019","url":"https://www.eib.org/en/projects/pipelines/all/20190166"},{"title":"Luxembourg, 14.11.2019","url":"https://www.eib.org/attachments/registers/125282376.pdf"},{"title":"Recherche FR menu Portail client du Groupe BEI","url":"https://www.eib.org/fr/projects/all/20190166"},{"title":"www.eib.org","url":"https://www.eib.org/en/projects/all/20190166?lang=en"},{"title":"simpact inwestycje ktorym nie jest wszystko jedno","url":"https://antyweb.pl/simpact-inwestycje-ktorym-nie-jest-wszystko-jedno"},{"title":"slovakia venture to future fund","url":"https://insights.munich-startup.de/investors/slovakia_venture_to_future_fund"},{"title":"simpact ventures","url":"https://seedtable.com/investors/simpact-ventures"}]

The search didn't turn up any specific Simpact investment in a Slovak company. It did show that Simpact's stated geography includes Slovakia, and it surfaced a separate Slovak fund that could be easily confused with Simpact.

**Simpact's Slovakia coverage:** Simpact Ventures is a Warsaw-based impact VC. One directory lists Slovakia among its countr
… [skrátené, 2764 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CB ESPRI fond sociálna ekonomika Sociálni Inovátori Impact Capital"

Links: [{"title":"Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur","url":"https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku"},{"title":"CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom","url":"https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond"},{"title":"slovak investment holding cb espri a socialni inovatori spustaju investicne fondy pre socialnu ekonomiku","url":"https://www.sih.sk/en/aktuality/slovak-investment-holding-cb-espri-a-socialni-inovatori-spustaju-investicne-fondy-pre-socialnu-ekonomiku"},{"title":"Slovak Investment Holding, CB ESPRI and Social Innovators launch investment funds for social economy","url":"https://sih.sk/en/aktuality/slovak-investment-holding-cb-espri-and-social-innovators-launch-investment-funds-for-social-economy"},{"title":"#socialenterprises #funding","url":"https://amcham.sk/media/a542/file/item/en/0000/connection2022_04_20.Ndtb.pdf"},{"title":"AmCham Slovakia","url":"https://amcham.sk/publications/issues/2022-4-pillars-of-good-society/article/273797/teaching-how-to-catch-fish"},{"title":"Socialni inovatori – socialne financovanie","url":"https://socialneinovacie.gov.sk/wp-content/uploads/2023/07/Socialni-inovatori-–-socialne-financovanie.pdf"},{"title":"AmCham Slovakia","url":"https://am
… [skrátené, 5083 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://simpact.vc/ | head -80; echo =====; python3 -I $F get https://therecursive.com/slovakia-startup-funding-h1-2025/ simpact
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1

 Strona główna - Simpact Ventures
 Zamknij
Wizja
Portfolio
EN
 Menu
Wizja
Portfolio
Impact
 PL
 EN
 Dla startupów →
Simply impact
 Zobacz więcej 
Wizja i doświadczenie
Simpact Ventures to pierwszy w Polsce fundusz inwestycyjny VC oparty na idei Impact Investing. Od 2017 roku z sukcesem inwestujemy w skalowalne startupy, które odpowiadają na wyzwania współczesnego świata. Wspieramy założycieli od wczesnych etapów rozwoju ich firm, oferując inwestycje do 2 milionów EUR. Nasz doświadczony zespół oraz przejrzyste podejście są wspierane przez silnych partnerów, w tym Europejski Fundusz Inwestycyjny.
 Więcej informacji →
Portfolio
Shen AI
[MedTech] Pionierski system zdalnego monitorowania zdrowia
 zobacz więcej 
Readmio
[EdTech] Magiczna aplikacja łącząca rodziców i dzieci
 zobacz więcej 
Nutrix
[MedTech] Opieka nad pacjentami z chorobami przewlekłymi 
 zobacz więcej 
 Zobacz portfolio →
Impact
Inwestowanie w impact
to więcej niż tylko dążenie do zysków finansowych – to wsparcie firm, które wywołują realne zmiany w społeczeństwie i środowisku. Światowy rynek inwestycji imactowych wciąż dynamicznie rośnie, przekraczając łączną wartość biliona dolarów. W obliczu narastających wyzwań, podejście to staje się nie tylko cenne, ale wręcz konieczne. W Simpact Ventures jesteśmy dumni, że możemy być częścią tego przełomowego ruchu. Wyznaczamy naszym spółkom ambitne cele, a dzięki ich innowacyjności i zaangażowaniu, nasz wpływ sięga milionów ludzi na całym świecie.
 Polityka impa
… [skrátené, 2593 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://therecursive.com/slovakia-startup-funding-h1-2025/ "simpact|jet|presto|look ai|j&t|fil rouge|gi21|jic|mcwin|365|ergos|ipm" 
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://therecursive.com/slovakia-startup-funding-h1-2025/ | head -30; curl -sIL https://therecursive.com/slovakia-startup-funding-h1-2025/ | head -5
```

<details><summary>Výstup nástroja</summary>

```
 Slovakia Startup Funding H1 2025: Key Deals
Media
Events
Reports
Podcast
Studio
About us
Sign in
Become a subscriberBecome a subscriber
Members
Slovak Startup Ecosystem Biggest Funding Rounds (H1 2025)
DealsNewsSlovakia
 by
 Teodora Atanasova
 July 31, 2025 ∙ 2 min read
 Share
 Written by
Teodora Atanasova
Teodora Atanasova is Senior Editor at The Recursive, covering startups, venture capital, and innovation across Central and Eastern Europe. She reports on emerging technologies, founders, and the region's growing tech ecosystem.
 Editor’s Choice
The Silent M&A Wave: When the Next Funding Round Becomes Less Attractive Than a Sale
How Bulgaria Built One of Europe’s Fastest-Growing Battery Markets
Start Up Bulgaria! Crossroads 2026
This post is for subscribers only
Sign up now to read the post and get access to the full library of posts for subscribers only.
 Sign up now
 Already have an account? Sign in
 Newer post
Paid Ads in Fintech: What Founders and CMOs Need to Know Before Scaling
HTTP/2 301 
alt-svc: h3=":443"; ma=2592000
location: https://www.therecursive.com/slovakia-startup-funding-h1-2025/
server: Caddy
x-caddy-server: current
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Simpact\" slovenský startup investícia 2025", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://simpact.vc/en/ | sed -n '10,30p'; python3 -I $F get https://simpact.vc/en/portfolio/ | head -120
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Simpact" slovenský startup investícia 2025"

Links: [{"title":"therecursive.com","url":"https://therecursive.com/?p=43718"},{"title":"Simpact Ventures Research","url":"https://f4.fund/firms/simpact-ventures"},{"title":"simpact ventures simpact vc","url":"https://venturecapitalarchive.com/venture-funds/simpact-ventures-simpact-vc"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/simpact-ventures"},{"title":"simpact vc","url":"https://www.crunchbase.com/organization/simpact-vc"},{"title":"Simpact Ventures","url":"https://www.startuplithuania.com/?p=13510"},{"title":"www.startuplithuania.com","url":"https://www.startuplithuania.com/eco_stage/scale-up/page/3"},{"title":"Join Vestbee","url":"https://www.vestbee.com/vc-list/simpact-ventures"},{"title":"Impact investor","url":"https://privateequitylist.com/investors/simpact-vc"}]

I didn't find any Slovak startup called "Simpact." The name appears to belong to a Polish venture capital fund, and the results don't show it making a 2025 investment in a Slovak company.

**What the results show about Simpact:**
- It's a Warsaw-based VC firm. One profile calls it recognized as the first impact-investment VC in Poland, founded in 2016.
- It invests in tech startups with measurable social or environmental impact. Its current fund, Simpact 2.0, is a PLN 100 million (approximately $25 million) vehicle capitalized with private and public funds, with the European Investment Fund as the largest
… [skrátené, 2535 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Impact
 EN
 PL
 For startups →
Simply impact
 See more 
Vision and experience
Simpact Ventures is the first VC investment fund in Poland based on the idea of Impact Investing. Since 2017, we have been successfully investing in scalable startups that address the challenges of the modern world. We support founders from the early stages of development, offering ticket sizes of up to EUR 2 million. Our experienced team and transparent approach are supported by strong partners, including the European Investment Fund.
 More information →
Portfolio
Shen AI
[MedTech] Revolution to health diagnostics
 see more 
Readmio
[EdTech] A magical app connecting parents and children
 see more 
Nutrix
[MedTech] Wellbeing of patients with chronic diseases worldwide
 see more 
 See the portfolio →
Impact

 Archiwum Portfolio - Simpact Ventures
 Close
Vision
Portfolio
PL
 Menu
Vision
Portfolio
Impact
 EN
 PL
 For startups →
Portfolio
Filter by
all
- Simpact 1.0
- Simpact 2.0
(exited)
(in portfolio) 
ForActive
[HealthTech] SaaS Marketplace for sports sector
 see more 
Kinderpedia
[EdTech] All-in-one SaaS platform for schools
 see more 
Cyber360
[Security] Comprehensive security solution for every business
 see more 
Rankfor.AI
[AI] Control over visibility in AI tools
 see more 
Readmio
[EdTech] A magical app connecting parents and children
 see more 
CulturePulse
[AI] Artificial Intelligence Supporting Decision-Making
 see more 
Ligence
[MedTech] Echocardiography supported by AI
 see more 
Pstryk
[E
… [skrátené, 1857 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "CulturePulse Simpact Ventures investment", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Simpact Ventures leads round 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Simpact Ventures leads round 2025"

Links: [{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/simpact-ventures"},{"title":"Simpact Ventures Research","url":"https://f4.fund/firms/simpact-ventures"},{"title":"unlocking growth with venture debt: a financing option for ambitious startups","url":"https://www.vestbee.com/blog/articles/unlocking-growth-with-venture-debt:-a-financing-option-for-ambitious-startups"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/simpact"},{"title":"# Simpact Fund","url":"https://altss.com/profile/simpact-fund.md"},{"title":"Simpact Ventures","url":"https://www.startuplithuania.com/?p=13510"},{"title":"Impact investor","url":"https://privateequitylist.com/investors/simpact-vc"},{"title":"simpact vc","url":"https://www.basetemplates.com/organization/simpact-vc"},{"title":"simpact ventures","url":"https://seedtable.com/investors/simpact-ventures"},{"title":"Simpact VC","url":"https://privateequitylist.com/investor/simpact-vc"}]

The clearest 2025 lead I found is **Readmio's seed round in January 2025**. A Caplight investor table lists Simpact as the lead on that round, and it also shows CulturePulse's March 2025 seed round with Simpact as a co-investor, not the lead. Caplight's table shows Readmio Jan 2025 Seed with Simpact as Lead, and CulturePulse Mar 2025 Seed with Simpact as Co-investor.

Other Simpact-led rounds in the result
… [skrátené, 2633 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CulturePulse Simpact Ventures investment"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/simpact"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/simpact-ventures"},{"title":"Simpact Ventures Research","url":"https://f4.fund/firms/simpact-ventures"},{"title":"Simpact Ventures","url":"https://www.startuplithuania.com/?p=13510"},{"title":"# Simpact Fund","url":"https://altss.com/profile/simpact-fund.md"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/culturepulse"},{"title":"simpact ventures","url":"https://seedtable.com/investors/simpact-ventures"},{"title":"simpact ventures simpact vc","url":"https://venturecapitalarchive.com/venture-funds/simpact-ventures-simpact-vc"},{"title":"Simpact Ventures partners with NCBR Investment Fund to co-invest up to €2M in early-stage startups","url":"https://en.ain.ua/2025/01/30/simpact-ventures-partners-with-ncbr-investment-fund"},{"title":"simpact ventures launches 21m fund","url":"https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund"}]

Simpact Ventures has backed CulturePulse as a co-investor, at least twice according to one tracker. The sources don't agree on the details, so I'd verify the dates before relying on them.

**The investment record**
- Caplight's Simpact profile lists two CulturePulse deals, a seed round dated March 2025 and another dated June 2026, with Simpact
… [skrátené, 3326 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ligence €3M seed Simpact", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "ForActive seed round Simpact 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "CulturePulse Bratislava raises funding Rockaway Simpact", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "ForActive seed round Simpact 2026"

Links: [{"title":"ForActive Raises $3.6 Million in Seed Funding","url":"https://raising.fi/news/foractive-seed-july-2026"},{"title":"Simpact Ventures Research","url":"https://f4.fund/firms/simpact-ventures"},{"title":"Kategorie artykułu: Biznes Newsy Technologia","url":"https://xyz.pl/polski-startup-pozyskal-36-mln-usd-wspoltworca-booksy-pomaga-mu-podbic-usa/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/simpact-1"},{"title":"2024 04 01 foractive seed","url":"https://startupintros.com/news/2024-04-01-foractive-seed"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/simpact-ventures"},{"title":"simpact ventures simpact vc","url":"https://venturecapitalarchive.com/venture-funds/simpact-ventures-simpact-vc"},{"title":"Impact investor","url":"https://privateequitylist.com/investors/simpact-vc"},{"title":"Simpact VC","url":"https://privateequitylist.com/investor/simpact-vc"}]

The seed round was reported in July 2026, with Simpact Ventures leading a $3.6 million round for ForActive.

- **Round details:** Raising.fi reports that the round closed on July 28, 2026 and was led by Simpact Ventures. Other contributors included BADideas.fund, The Explorer Fund, Pragmatech Ventures, Vesna Capital, and Vestbee Angels.
- **Use of funds:** The money is meant to scale its go-to-market strategy across the United States and expand its platform to include new sports catego
… [skrátené, 2430 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ligence €3M seed Simpact"

Links: [{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/ligence-secures-3m-in-funding-round"},{"title":"hedera 22 secures 2 m","url":"https://vestbee.com/blog/articles/hedera-22-secures-2-m"},{"title":"ligence funding round seed e357b8","url":"https://app.fundz.net/fundings/ligence-funding-round-seed-e357b8"},{"title":"Simpact Ventures Research","url":"https://f4.fund/firms/simpact-ventures"},{"title":"simpact ventures","url":"https://www.vcbacked.co/directory/investors/simpact-ventures"},{"title":"28040 tgs baltic advises simpact ventures on investment in ligence","url":"https://ceelegalmatters.com/lithuania/28040-tgs-baltic-advises-simpact-ventures-on-investment-in-ligence"},{"title":"ligences investment round","url":"https://globallegalchronicle.com/ligences-investment-round/"},{"title":"28040 tgs baltic advises simpact ventures on investment in ligence","url":"https://ceelm.com/lithuania/28040-tgs-baltic-advises-simpact-ventures-on-investment-in-ligence"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/simpact-ventures"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/simpact-ventures"}]

Simpact Ventures led a €3 million seed round for Ligence, a Lithuanian health-tech company, in November 2024.

- **The company:** Ligence is based in Vilnius and makes AI software that automates the analysis of cardiac ultrasound images, which helps cardiologists diagnose 
… [skrátené, 2987 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "CulturePulse Bratislava raises funding Rockaway Simpact"

Links: [{"title":"havrlant spousti druhy fond na startupy ma pripravene 1 4 miliardy","url":"https://www.newstream.cz/money/havrlant-spousti-druhy-fond-na-startupy-ma-pripravene-1-4-miliardy"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/simpact"},{"title":"slovak startup ecosystem","url":"https://therecursive.com/tag/slovak-startup-ecosystem"},{"title":"Jakub Havrlant přichází s novým investičním fondem. Rockaway s ním chce do startupů poslat 2,5 miliardy korun","url":"https://cc.cz/jakub-havrlant-prichazi-s-novym-investicnim-fondem-rockaway-s-nim-chce-do-startupu-poslat-25-miliardy-korun/"},{"title":"Bratislava will receive €15 million to finance its activities","url":"https://spectator.sme.sk/c/22270903/bratislava-will-receive-15-million-to-finance-its-activities.html"},{"title":"zrusene koncerty nas staly dva roky duvery rika jirovec z rockaway","url":"https://forbes.cz/zrusene-koncerty-nas-staly-dva-roky-duvery-rika-jirovec-z-rockaway/"},{"title":"simpler.grants.gov","url":"https://simpler.grants.gov/opportunity/357784"},{"title":"reality jsou pro nas nudny byznys zajimavejsi je napriklad defense tech rikaji manazeri fondu rockaway","url":"https://cc.cz/podcasty/reality-jsou-pro-nas-nudny-byznys-zajimavejsi-je-napriklad-defense-tech-rikaji-manazeri-fondu-rockaway/"},{"title":"kit fryatt","url":"https://www.
… [skrátené, 3178 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://xyz.pl/polski-startup-pozyskal-36-mln-usd-wspoltworca-booksy-pomaga-mu-podbic-usa/ "simpact|ForActive|2026" | head -20; echo; python3 -I $F get https://ceelegalmatters.com/lithuania/28040-tgs-baltic-advises-simpact-ventures-on-investment-in-ligence "simpact|ligence|2024" | head
```

<details><summary>Výstup nástroja</summary>

```
 ForActive pozyskał 3,6 mln dolarów. Współtwórca Booksy pomaga mu podbić USA - XYZ
 Orlen i Dino uratowały niedźwiedzie nastroje. Podsumowanie notowań na GPW 8 października 2026 r. 
ForActive pozyskał 3,6 mln dolarów. Współtwórca Booksy pomaga mu podbić USA 
Fundusz Simpact Ventures stanął na czele rundy finansowania ForActive, w której startup pozyskał 3,6 mln dolarów. Spółka przeznaczy pieniądze na ekspansję i umocnienie swojej pozycji na rynku amerykańskim. 
 24.07.2026, 04:57 
 Konrad Howard, inwestor ForActive oraz współzałożyciel Booksy, jest zaangażowany w rozwój startupu na rynku amerykańskim i jego ekspansję w segmencie usług sportowych. Fot. materiały prasowe 
Jak spółzarządzający ForActive chcą budować kolejnego globalnego gracza z Polski. 
Dlaczego fundusze venture capital stawiają na spółkę zarejestrowaną w USA i jaką rolę w strategii ForActive odgrywa tzw. impact investing. 
ForActive rozwija aplikację przeznaczoną dla niezależnych trenerów i instruktorów sportowych. Teraz przed firmą dalszy rozwój produktu i zwiększanie skali działalności na rynku amerykańskim – już z kolejnymi inwestorami na pokładzie. 
– ForActive realizuje rundę seed. Jej liderem jest polski fundusz Simpact Ventures. Dołączyły do niej również polskie syndykaty, m.in. Vestbee. Dodatkowo w gronie inwestorów znaleźli się Vesna, Explorer i Bad Ideas, a także kilku aniołów biznesu, w tym były general manager Booksy, Adam Górniak. Runda sięga poziomu 3,6 mln dolarów – informuje Konrad Howard, inwe
… [skrátené, 4342 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund | grep -iE "simpact|€|EUR|seed|CEE" | head -20; curl -sL https://simpact.vc/en/portfolio/ | grep -oE 'href="[^"]*culture[^"]*"' | head
```

<details><summary>Výstup nástroja</summary>

```
 Polish VC Simpact Ventures launches a €21M Fund II - AIN 
Polish VC Simpact Ventures lau...
Polish VC Simpact Ventures launches a €21M Fund II
Polish venture capital firm Simpact Ventures has announced the closing of its second fund, aiming at projects with positive impact. The fund has over €21 million (100 million PLN) under management, dedicated to early-stage startups, mainly from CEE.
Founded in 2017 by Jacek Ostrowski, Krzysztof Grochowski, and Wojciech Majewski, Simpact is a Warsaw-based venture capital fund. It mainly invests in tech-driven early-stage startups with high business potential and a positive social and environmental impact. The firm wishes to empower founders to build tech companies that combine profit with purpose.
Fund II has over €21 million (100 million PLN) under management. It will provide sector agnostic investments with a preference for pre-seed, seed, and Series A investments (equity & convert). The tickets will range from nearly €100,000 (500,000 PLN) to over €2 million (10 million PLN), with strong follow-on strategy. 
European Investment Fund (EIF) backed Simpact’s Fund II along with a series of recognized and trustworthy investors. EIF is a financial institution for the provision of finance to SMEs, headquartered in Luxembourg. It provides finance through private banks and funds to support emerging and established fund managers with equity investments.
 Estonian Trind Ventures leads €2M round for Barcelona-based Xceed
The Barcelona-based eve
… [skrátené, 3057 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.simpact.vc/en/portfolio/culturepulse/ | sed -n '15,45p'
```

<details><summary>Výstup nástroja</summary>

```
Culture Pulse is a platform that leverages advanced artificial intelligence to analyze and forecast social dynamics in real-time. Using digital twin technology and multi-agent AI, it enables the creation of psychologically realistic models of communities, allowing strategies to be tested in a safe, simulated environment before implementation in the real world.
Culture Pulse addresses the challenges of modern societies, such as armed conflicts and social polarization, which destabilize communities and undermine trust in institutions. The platform empowers decision-makers to predict and prevent conflicts, design peacebuilding strategies, and foster social cohesion. It also effectively combats misinformation by identifying false narratives and enabling rapid responses through the delivery of reliable information.
Screenshot
Screenshot
Investment date: December 2024
Founders: Justin E. Lane, LeRon Shults
Location: US
 Portfolio 
Napisz do nas 
formularz kontaktowy
Nasze biuro:
Racławicka 19/16a,
02-601 Warszawa
Contact
Privacy policy
Investors relations
Sustainability
Simpact 1.0
 Join ours 
social
```

</details>

**Nástroj `Bash`**

```bash
cat /home/filip/investor-db/src/investordb/models.py | head -120
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
… [skrátené, 3797 znakov]
```

</details>

## Claude · 2026-10-09 12:21:58 UTC

Píšem c061.

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c061.json <<'EOF'
{
  "candidate_id": "c061",
  "name": "Simpact VC",
  "legal_name": null,
  "reg_no": null,
  "country": "PL",
  "active_in": ["PL", "LT"],
  "website": "https://simpact.vc/",
  "entity_kind": {"value": "investor", "source_url": "https://simpact.vc/en/", "source_date": null, "quote": "Simpact Ventures is the first VC investment fund in Poland based on the idea of Impact Investing."},
  "investor_type": {"value": "vc", "source_url": "https://simpact.vc/en/", "quote": "Simpact Ventures is the first VC investment fund in Poland based on the idea of Impact Investing."},
  "sectors": {"value": ["impact", "sector agnostic"], "source_url": "https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund", "source_date": "2022-11-23", "quote": "It will provide sector agnostic investments with a preference for pre-seed, seed, and Series A investments (equity & convert)."},
  "stages": {"value": ["pre-seed", "seed", "series-a"], "source_url": "https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund", "source_date": "2022-11-23", "quote": "It will provide sector agnostic investments with a preference for pre-seed, seed, and Series A investments (equity & convert)."},
  "ticket_min": {"amount": 100000, "currency": "EUR", "source_url": "https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund", "source_date": "2022-11-23", "quote": "The tickets will range from nearly €100,000 (500,000 PLN) to over €2 million (10 m
… [skrátené, 3359 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://simpact.vc/en/
OK  investor_type https://simpact.vc/en/
OK  sectors https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund
OK  stages https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund
OK  ticket_min https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund
OK  ticket_max https://simpact.vc/en/
OK  aum https://en.ain.ua/2022/11/23/simpact-ventures-launches-21m-fund
OK  inv https://xyz.pl/polski-startup-pozyskal-36-mln-usd-wspoltworca-booksy-pomaga-mu-podbic-usa/
OK  inv https://ceelegalmatters.com/lithuania/28040-tgs-baltic-advises-simpact-ventures-on-investment-in-ligence
OK    research/c061.json
```

</details>

## Claude · 2026-10-09 12:22:11 UTC

Teraz CB ESPRI a Sociálni Inovátori.

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku | grep -iE "fond|invest|eur" | head -40; echo; python3 -I $F get https://sih.sk/en/aktuality/slovak-investment-holding-cb-espri-and-social-innovators-launch-investment-funds-for-social-economy | grep -iE "fund|espri|innovat|EUR|€" | head -30
```

<details><summary>Výstup nástroja</summary>

```
 Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur | Podnikajte.sk 
 Podnikateľ a investor
 Hypotéky od roku 2027: zvýhodnené prvé bývanie, prísnejšie investičné nákupy
 Európska legislatíva
 Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur
 Nové eurobankovky: ECB vybrala 10 finálnych návrhov, hlasovať môžete aj vy
 Ako bude investovanie fungovať v praxi, kto sa môže zapojiť a ako postupovať v prípade záujmu o získanie investície?
Slovak Investment Holding (SIH) spolu so správcovskými
dvoch investičných fondov na podporu sociálnej ekonomiky. SIH do týchto fondov
zainvestuje celkovo 20,9 milióna eur, pričom na každého správcu pripadá 10,45
milióna eur. Je to súčasť prostriedkov Európskeho sociálneho fondu
Ako bude investovanie fungovať v praxi a kto sa môže zapojiť?
investícií podporovať spoločnosti širšej sociálnej ekonomiky na celom území
Slovenskej republiky okrem Bratislavského samosprávneho kraja. Investičné
vyhľadávať vhodné investičné projekty, dojednať s cieľovými spoločnosťami
zmluvnú dokumentáciu, zrealizovať investície a v primeranom časovom
Impact Capital, s. r. o. Oba fondy majú rovnaké podmienky na investovanie,
ktoré vyplývajú zo štátnej schémy a investičnej zmluvy o fonde.
Ako získať investície?
ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským
spomínaných vyčlenených 10 miliónov eur slovenským organizáciám s pozitívnym
spoločenským dop
… [skrátené, 2595 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"CB ESPRI Impact One\" investícia do", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "\"SIIC Fund\" OR \"Sociálni Inovátori Impact Capital\" investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""SIIC Fund" OR "Sociálni Inovátori Impact Capital" investícia"

Links: [{"title":"Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur","url":"https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku"},{"title":"Slovak Investment Holding, CB ESPRI and Social Innovators launch investment funds for social economy","url":"https://sih.sk/en/aktuality/slovak-investment-holding-cb-espri-and-social-innovators-launch-investment-funds-for-social-economy"},{"title":"slovak investment holding cb espri a socialni inovatori spustaju investicne fondy pre socialnu ekonomiku","url":"https://www.sih.sk/en/aktuality/slovak-investment-holding-cb-espri-a-socialni-inovatori-spustaju-investicne-fondy-pre-socialnu-ekonomiku"},{"title":"CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom","url":"https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond"},{"title":"social impact capital closes 42m to invest in the best ideas in impact 20211103530","url":"https://www.thetrustedinsight.com/investment-news/social-impact-capital-closes-42m-to-invest-in-the-best-ideas-in-impact-20211103530/"},{"title":"social impact capital closes 42 million to invest in the best ideas in impact","url":"https://nextbillion.net/news/social-impact-capital-closes-42-million-to-invest-in-the-best-ideas-in-impact/"},{"title":"Socialni inovatori – socialne financo
… [skrátené, 3608 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""CB ESPRI Impact One" investícia do"

Links: [{"title":"CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom","url":"https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond"},{"title":"AmCham Slovakia","url":"https://amcham.sk/events/3139/cb-espri-impact-one-investment-fund"},{"title":"Miroslava Beblavého už politika neláka. Začal však podnikať s verejnými peniazmi","url":"https://www.startitup.sk/miroslava-beblaveho-uz-politika-nelaka-zacal-vsak-podnikat-s-verejnymi-peniazmi/"},{"title":"CEE webinar replay: Investing for social impact","url":"https://www.forvismazars.com/sk/en/insights/publications-and-events/events/webinar-archive/cee-webinar-replay-investing-for-social-impact"},{"title":"23.6. CEE webinar: Investing for social impact","url":"https://www.forvismazars.com/ua/en/insights/latest-news/events/23.6.-cee-webinar-investing-for-social-impact"},{"title":"23.6. CEE webinar: Investing for social impact","url":"https://www.forvismazars.com/ua/uk/insajti/novini/podiyi/23.6.-cee-webinar-investing-for-social-impact"},{"title":"23.6. CEE webinar: Investing for social impact","url":"https://www.forvismazars.com/rs/en/insights/news/forvis-mazars-news/23.6.-cee-webinar-investing-for-social-impact"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-espri"},{"title":"Investors Count","url":"https://www.cbinsights.com/company/impacts/financials"}]

CB ES
… [skrátené, 3562 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for u in https://cbespri.sk/ https://www.espri.sk/ https://www.socialniinovatori.sk/ https://siic.sk/ ; do echo "## $u"; python3 -I $F get $u | head -40; done
```

<details><summary>Výstup nástroja</summary>

```
## https://cbespri.sk/

 CB ESPRI: Investičný fond s pozitívnym spoločenským dopadom
 Úvod
 Impakt
 O nás
 Portfólio
 SK
 |
 EN
Impakt
na prvom
mieste.
Inovácie prinášajúce
pozitívne zmeny
 Napísali o nás:
"CB ESPRI je jeden z najprofesionálnejších fondov, s akými som robil, a to nielen na Slovensku. Mali veľmi trézvy pohľad na vec. Máme inovatívny produkt, ktorý posúva hranice ľudského poznania. Buď dobré ale aj zlé dni. CB ESPRI chápe, že je to risk, no ak sa nám to podarí, úspech bude nielen finančný, ale aj spoločenský. Určobne niečo, čo môže zachrániť ľudské životy."
Martin Herman, 
 CEO, Powerful Medical
"Podnikanie v cirkulárnej ekonomike nie je jednoduché, ale vďaka CB ESPRI sa nám podarilo rozbehnúť oveľa rýchlejšie a môžeme naše udržateľné riešenie aplikovať vo viacerých výrobkoch a viacerých krajinách."
Michal Šula, 
 CEO, Terratico
"Spoluprácu s Investičným fondom CB ESPRI hodnotíme veľmi pozitívne. Poskytol nám návratné finančné prostriedky do našej práčovne, čím podporil rozbehnutie nášho registrovaného sociálneho podniku. Financovanie bolo výhodnejšie ako na komerčnom bankovom trhu a pomohlo nám sledovať dohodnuté sociálne ciele. Veľmi oceňujeme profesionálny a priateľský prístup zamestnancov fondu, vďaka čomu máme pocit, že sme v dobrých rukách."
René Pisko, CEO
 Bc. Miroslav Pisko, executive director,
 CIBEKA s.r.o., r.s.p.
 Naši partneri:
 CB ESPRI je správcovská spoločnosť založená v roku 2022 s cieľom vytvoriť prvý investičný fond na 
… [skrátené, 5137 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"CB ESPRI\" investoval Powerful Medical OR Terratico OR startup", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cbespri.sk/ | sed -n '40,120p'; curl -sL https://cbespri.sk/ | grep -oE 'href="[^"]*"' | sort -u | head -40
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""CB ESPRI" investoval Powerful Medical OR Terratico OR startup"

Links: [{"title":"Slovak startup Powerful Medical raises €6.2M in a seed round","url":"https://en.ain.ua/tag/slovakia/page/7"},{"title":"21530 Kinstellar and wise3 advise on powerful medical eur 6 2 million seed round","url":"https://ceelegalmatters.com/slovakia/21530-Kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round"},{"title":"21530 kinstellar and wise3 advise on powerful medical eur 6 2 million seed round","url":"https://ceelegalmatters.com/slovakia/21530-kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/bpd-partners"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/powerful-medical-secures-multi-million-investment"},{"title":"Powerful Medical","url":"https://www.sih.sk/en/portfolio/powerful-medical"},{"title":"Become a partner","url":"https://www.itapa.sk/speakers/miroslav-beblavy"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-espri"},{"title":"Become a partner","url":"https://www.itapa.sk/15339-en/diskusia-ako-ziskavat-sukromny-kapital-pre-inovacie-v-zdravotnictve/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/spri-group"}]

Links: [{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-espri"},{"title":"Predict you
… [skrátené, 4735 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Portfólio
Základné ukazovatele
Dve hlavné časti porfóia sú:
Registrované sociálne podniky
Zameriavajú sa na riešenie konkrétnych sociálnych výziev ako nezamestnanosť alebo vzdelávanie, pričom prinášajú trvalé pozitívne zmeny v komunitách.
Počet:
22
Objem investície:
3 931 000 €
 Pozri viac →
Impaktové startupy
Zameriavajú sa na riešenie konkrétnych sociálnych výziev ako nezamestnanosť alebo vzdelávanie, pričom prinášajú trvalé pozitívne zmeny v komunitách.
Počet:
20
Objem investície:
12 398 000 €
 Pozri viac →
Tvoríme impakt
Podpora startupov
Náš fond investuje do podnikov a organizácií, ktoré generujú pozitívne spoločenské zmeny, podporujú inkluzívne zamestnávanie a rozvoj impaktových startupov.
 Viac →
Práca so zmyslom
Fond sa zameriava na podporu spoločností so sociálnymi alebo environmentálnymi cieľmi v oblastiach ako vzdelávanie, zdravotná starostlivosť, ochrana životného prostredia a rodová rovnosť.
 Zisti viac →
Merateľný dopad
Impaktové ciele sú posudzované v investičnom procese, zmluvne ukotvené a pravidelne monitorované. Výsledky sú prezentované v každoročne publikovanom Impact Reporte.
 Read the article →
 Viac o impakte CB ESPI Impact One →
Angažujeme sa v týchto
oblastiach
O nás
Za CB ESPRI Impact One stojí tím ľudí so skúsenosťami v rôznych oblastiach od financií až po sociálnu ekonomiku. Tím sa zameriava na správu portfólia a monitorovanie zmluvne ukotvených impaktových cieľov.
Miroslav Beblavý
Konateľ
David Scherhaufer
Pozicia
Michal Ondrišek
Pozicia
Terézia J
… [skrátené, 2923 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://ceelegalmatters.com/slovakia/21530-Kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round | grep -iE "espri|202[0-9]" | head; python3 -I $F get https://www.startitup.sk/slovensky-startup-ziskal-vyse-polmiliónovú-investiciu-preslavili-sa-v-usa-vdaka-vizualizacnym-rieseniam/ "espri|2023|2024" | head
```

<details><summary>Výstup nástroja</summary>

```
October 9, 2026
October 9, 2026 
October 9, 2026 
October 9, 2026 
October 9, 2026 
October 9, 2026 
October 8, 2026 
October 5, 2026 
October 5, 2026 
October 6, 2026
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://ceelegalmatters.com/slovakia/21530-kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round | grep -iE "espri|Powerful" | head; python3 -I $F get "https://www.startitup.sk/slovensky-startup-ziskal-vyse-polmilionovu-investiciu-preslavili-sa-v-usa-vdaka-vizualizacnym-rieseniam/" | grep -iE "espri|investíc|202[0-9]" | head
```

<details><summary>Výstup nástroja</summary>

```
 Kinstellar and Wise3 Advise on Powerful Medical EUR 6.2 Million Seed Round | CEE Legal Matters 
Kinstellar and Wise3 Advise on Powerful Medical EUR 6.2 Million Seed Round
Kinstellar has advised Powerful Medical on its EUR 6.2 million seed funding round from investors including Arieli Capital, Venture To Future Fund, CB ESPRI Impact One, BPD partners, and several angel investors. Wise3 advised CB ESPRI Impact One.
Powerful Medical is a Slovak artificial intelligence and machine-learning med-tech company. According to Kinstellar, “Powerful Medical has developed a software medical device that automates ECG analysis using artificial intelligence and machine-learning modules, which enables timely and cost-effective arterial fibrillation diagnosis and enhanced quality of treatment.”
 Slovenský startup získal vyše polmiliónovú investíciu. Preslávili sa v USA vďaka virtuálnej realite
Slovenský startup získal vyše polmiliónovú investíciu. Preslávili sa v USA vďaka virtuálnej realite
Technologický startup Cviker získal 550-tisícovú investíciu. Získané prostriedky použije na spustenie platformy pre zákazníkov primárne z USA. 
Technologický startup Cviker získal 550-tisícovú investíciu z 12 miliónového štátneho investičného balíka Slovak Investment Holdingu, ktorý je v správe CB Investment Management. Určený je na rozvoj podnikania mladých firiem zo všetkých regiónov Slovenska. 
CB Investment Management je dcérskou spoločnosťou Crowdberry, ktorá spravuje zdroje vo výške takmer 12 milión
… [skrátené, 2772 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://ceelegalmatters.com/slovakia/21530-kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round | grep -B3 -A3 "Kinstellar and Wise3 Advise" | head -20; curl -sL https://ceelegalmatters.com/slovakia/21530-kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round | grep -oE '(datePublished|article:published_time)[^,]{0,60}' | head
```

<details><summary>Výstup nástroja</summary>

```
 Kinstellar and Wise3 Advise on Powerful Medical EUR 6.2 Million Seed Round | CEE Legal Matters 
 Skip to content
Subscribe
Events
--
Deal 5: Erste Group Executive Director on Financing and PPA for Krivaca Wind Farm
By Practice 
By Country 
Kinstellar and Wise3 Advise on Powerful Medical EUR 6.2 Million Seed Round
Andrija Djonovic 
November 14, 2022 
Find CEELM on Google News
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Hypherdata investícia CB ESPRI 2024", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cbespri.sk/portfolio.html | head -150
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Hypherdata investícia CB ESPRI 2024"

Links: [{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/cb-espri"},{"title":"funding.tech.eu","url":"https://funding.tech.eu/investors/CB%20ESPRI%20Impact%20One"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/hyperscale-data-receives-4m-investment"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/spri-group"},{"title":"www.esprinet.com","url":"https://www.esprinet.com/pt/?p=9287"},{"title":"IT Conference 2026 Intesa Sanpaolo","url":"https://statics.esprinet.com/prod/2026/02/IT-Conference-2026-Intesa-Sanpaolo.pdf"},{"title":"Intermonte European Midcap Event Intermonte","url":"https://statics.esprinet.com/prod/2026/06/Intermonte-European-Midcap-Event-Intermonte.pdf"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/abhay-deshpande"},{"title":"www.esprinet.com","url":"https://www.esprinet.com/es/?p=9242"}]

I found one clear record of this deal. CB Insights lists CB ESPRI's most recent investment as Hypherdata, a Seed VC round dated August 27, 2024, for about $0.94M. CB ESPRI is the manager of a fund to support businesses and non-profit organizations with a positive social impact. It was founded in 2022 and is based in Bratislava, Slovakia.

Some caveats:

- **Single source:** The deal figures come from one aggregator page. Most of the round details (co-investors, other terms) are behind
… [skrátené, 2256 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
 CB ESPRI: Investičný fond s pozitívnym spoločenským dopadom
 Úvod
 Impakt
 O nás
 Portfólio
 SK
 |
 EN
Investičné portfólio
Investujeme do inovatívnych podnikov a organizácií, ktoré generujú finančný výnos a majú pozitívny spoločenský dopad. Spoznajte spoločnosti, ktoré podporujeme.
Dve cesty k impaktu 
Registrované sociálne podniky
Zameriavajú sa na riešenie konkrétnych sociálnych výziev ako nezamestnanosť alebo vzdelávanie, pričom prinášajú trvalé pozitívne zmeny v komunitách.
Počet:
22
Objem investície:
3 931 000 €
Forma investície:
Podriadený úver
Impaktové startupy
Impaktové startupy predstavujú dynamické firmy na čele technologických a ekologických inovácií, ktoré formujú budúcnosť trvalo udržateľného rozvoja. 
Počet:
20
Objem investície:
12 398 000 €
Forma investície:
Konvertibilný úver 
Spoznajte naše portfólio v praxi
Pozrite sa bližšie na konkrétne úspechy a výzvy. Prípadové štúdie z našich subportfólií ilustrujú, ako naše investície ovplyvňujú spoločnosť a ekonomiku. Každá štúdia ponúka vhľad do dynamiky a výsledkov našich investícií a poskytuje lepšie porozumenie nášho prístupu k impaktovému investovaniu.
Powerful Medical
Inkluzívny prístup
Inovácia v kardiovaskulárnej diagnostike
Pred piatimi rokmi sa bratia Martin a Robert Herman rozhodli zmeniť zdravotníctvo prostredníctvom svojho projektu Powerful Medical. Ich cieľom bolo využiť umelej inteligencie na presnejšiu diagnostiku srdcových chorôb, inšpirovaní osobnou tragédiou v ich 
… [skrátené, 6589 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond | grep -iE "eur|fond|202[0-9]" | head -30
```

**Nástroj `WebSearch`**

```json
{"query": "elv.ai investícia CB ESPRI Impact One", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
 CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom | Podnikajte.sk 
 Register krátkodobých prenájmov od 1.1.2027
 Dôležité čísla pre daňové priznanie fyzickej osoby za rok 2026
 Hypotéky od roku 2027: zvýhodnené prvé bývanie, prísnejšie investičné nákupy
 Európska legislatíva
 CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom
 Opatrenia proti vysokým cenám nafty a benzínu od 1.10.2026
 Výplata rodičovského dôchodku od augusta 2026: otázky a odpovede
 Nové eurobankovky: ECB vybrala 10 finálnych návrhov, hlasovať môžete aj vy
 29.8.2022
 29.8.2022
 Na Slovensku vznikol fond zameraný na podniky s merateľným spoločenským dopadom. Koľko plánuje investovať, do akých firiem a aké podmienky treba splniť?
Nový investičný fond CB ESPRI Impact One je financovaný
pozitívny spoločenský dopad. V roku 2022 a 2023 plánuje fond
investovať kapitál 10,5 miliónov eur, pričom firmám ponúka výšku investície od 10 000
eur do 500 000 eur, podľa individuálnych potrieb podniku. Okrem CB ESPRI je správcom investičného fondu pre sociálnu ekonomiku aj spoločnosť Sociálni Inovátori Impact Capital, ktorí majú projektom rozdeliť taktiež sumu 10,5 miliónov eur.
(BSK). Ak pôjde o podnik, ktorý má sídlo v BSK, investícia fondu musí
Podmienkou je, aby spoločnosť prijala do konca roka 2023 aspoň
ekonomicky udržateľné fungovanie podniku po investícii. Cieľom fondu je
ESPRI do ukončenia fungovania fondu – roku 2031. A tiež ochota zam
… [skrátené, 2292 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "elv.ai investícia CB ESPRI Impact One"

Links: [{"title":"Slovenští lovci internetových trollů získali první investici, dohlíží i na komentáře v Česku","url":"https://www.lupa.cz/aktuality/slovensti-lovci-internetovych-trollu-ziskali-prvni-investici-dohlizi-i-na-komentare-v-cesku/"},{"title":"Join Vestbee","url":"https://vestbee.com/insights/articles/slovak-startup-elv-ai-secures-500k-to-fight-disinformation"},{"title":"Slovakia startup Elv.ai secures €500k to mitigate cyberhate through AI and human moderators","url":"https://siliconcanals.com/news/page/296/"},{"title":"Join Vestbee Summer Pitch CEE","url":"https://www.vestbee.com/blog/articles/slovak-startup-elv-ai-secures-500k-to-fight-disinformation"},{"title":"Bojují proti dezinformacím a útokům na webu. Z neziskového projektu je startup s 12milionovou investicí","url":"https://cc.cz/bojuji-proti-dezinformacim-a-utokum-na-webu-z-neziskoveho-projektu-je-startup-s-12milionovou-investici/"},{"title":"funding.tech.eu","url":"https://funding.tech.eu/investors/CB%20ESPRI%20Impact%20One"},{"title":"CB ESPRI Impact One Investment Fund (investor - Others)","url":"https://nordic9.com/companies/cb-espri-impact-one-investment-fund/"},{"title":"CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom","url":"https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond"},{"title":"Subscribe to Our Newsletter","url":"https://www.thesaasnews.com/news/elv-a
… [skrátené, 3455 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.lupa.cz/aktuality/slovensti-lovci-internetovych-trollu-ziskali-prvni-investici-dohlizi-i-na-komentare-v-cesku/ | grep -iE "espri|202[3-5]|ledna|elv" | head -12; python3 -I $F get https://www.vestbee.com/blog/articles/slovak-startup-elv-ai-secures-500k-to-fight-disinformation | grep -iE "espri" | head
```

<details><summary>Výstup nástroja</summary>

```
15. 1. 2024
Autor: Elv.ai
Elv.ai
Slovenský startup Elv.ai získal investici půl milionu eur, něco přes dvanáct milionů korun, od tamního fondu CB ESPRI Impact One. Elv.ai kombinuje automatizaci a algoritmy s prací lidských moderátorů za účelem boje s trolími farmami a podobně. Lidé dokáží za hodinu projít až tři sta komentářů internetových komentářů.
Startup díky investice může rozjet expanzi. Působit začal v Česku, technologie Elv.ai už hlídá diskuse a sociální sítě vydavatelství Economia, Evropy 2, Refresheru nebo televize Prima. Ta už dříve popsala své zkušenosti.
“Od spuštění prošlo Elv.ai na 44 profilech svých klientů a partnerů v ČR více než dva miliony komentářů, z kterých tvořilo nenávistný obsah až 24 procent,” uvedla firma. Přes kombinaci algoritmů a moderátorů je možné snížit počet nežádaného obsahu na tři až osm procent.
Elv.ai od spuštění v březnu 2022 přispěla ke smazání více než dvou a půl milionu komentářů z šestnácti milionů. Podařilo se identifikovat přes pět tisíc falešných profilů.
Fond CB ESPRI Impact One poskytuje prostředky ze soukromých zdrojů a z Evropského sociálního fondu. Zaměřuje se na “kapitál pro podnikání s pozitivním společenským dopadem”. Nové žádosti aktuálně nepřijímá, kapacita byla vyčerpána. Fond do roku 2023 investoval 18,6 milionu eur.
Elv.ai původně vznikla ja neziskový projekt založený komunikační agenturou New School Communications. Loni v květnu byl projekt vyčleněn do samostatné firmy. Spoluzakladateli jsou Jakub Šuster, Gabriel Tót
… [skrátené, 2461 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c062.json <<'EOF'
{
  "candidate_id": "c062",
  "name": "CB ESPRI",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://cbespri.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://cbespri.sk/", "source_date": null, "quote": "CB ESPRI je správcovská spoločnosť založená v roku 2022 s cieľom vytvoriť prvý investičný fond na Slovensku s pozitívnym spoločenským dopadom."},
  "investor_type": {"value": "vc", "source_url": "https://cbespri.sk/", "quote": "Náš fond investuje do podnikov a organizácií, ktoré generujú pozitívne spoločenské zmeny, podporujú inkluzívne zamestnávanie a rozvoj impaktových startupov."},
  "sectors": {"value": ["impact", "edtech", "healthtech", "cleantech"], "source_url": "https://cbespri.sk/", "source_date": null, "quote": "Fond sa zameriava na podporu spoločností so sociálnymi alebo environmentálnymi cieľmi v oblastiach ako vzdelávanie, zdravotná starostlivosť, ochrana životného prostredia a rodová rovnosť."},
  "ticket_min": {"amount": 10000, "currency": "EUR", "source_url": "https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond", "source_date": "2022-08-29", "quote": "investovať kapitál 10,5 miliónov eur, pričom firmám ponúka výšku investície od 10 000 eur do 500 000 eur, podľa individuálnych potrieb podniku."},
  "ticket_max": {"amount": 500000, "currency": "EUR", "source_url": "https://www.podnikajte.sk/financie-na-pod
… [skrátené, 3495 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://cbespri.sk/
OK  investor_type https://cbespri.sk/
OK  sectors https://cbespri.sk/
OK  ticket_min https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond
OK  ticket_max https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond
OK  inv https://www.lupa.cz/aktuality/slovensti-lovci-internetovych-trollu-ziskali-prvni-investici-dohlizi-i-na-komentare-v-cesku/
OK  inv https://ceelegalmatters.com/slovakia/21530-kinstellar-and-wise3-advise-on-powerful-medical-eur-6-2-million-seed-round
OK    research/c062.json
Next
SMARTFISH
Spoločensky prospešné a dostupné financovanie
Podpora podnikania
Next
ÚSMEV PRE DRUHÝCH
Pomoc zdravotne znevýhodneným
Zdravie | Slovensko
Next
VŠETKY PROJEKTY
NÁŠ MANIFEST
PRINÁŠAME KAPITÁL, EXPERTÍZU A PROFESIONALITU DO SEKTORA SOCIÁLNYCH INOVÁCIÍ
Chceme aby zodpovedné podniky, ktoré riešia spoločenské výzvy boli nielen udržateľné ale aj rastúce, inovujúce a udávajúce smer pre zvyšok ekonomiky.
ČÍTAŤ VIAC
REFERENCIE
Braňo Čavoj, 
Nadácia Cvernovka
​
Úprimne povedané, nebyť vás, projekt Novej Cvernovky by sa zrealizoval len veľmi ťažko. Rekonštrukcia bývalej chemickej školy na Račianskej ulici bola nevyhnutná na to, aby sa vyše 40 kreatívnych ateliérov mohlo nasťahovať a pokračovať vo svojom pôsobení. Celý proces si vyždadoval naozaj nemalé finančné prostriedky a mnoho úsilia. Pomohli ste nam práve v čase, kedy hrozilo, že rekonštrukcia a naše plány sa celé zaseknú. Navyše komunikácia s vami bola
… [skrátené, 3649 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.socialniinovatori.sk/investicny-fond | sed -n '20,80p'; echo; python3 -I $F get https://www.socialniinovatori.sk/portfolio | sed -n '20,90p'
```

<details><summary>Výstup nástroja</summary>

```
V rámci investičného 19 mesačného obdobia končiaceho 31.12.2023 fond SIIC Fund, s.r.o. (pod správou Sociálni Inovátori Impact Capital, s.r.o.) zainvestoval do slovenských spoločností s pozitívnym spoločenským dopadom (s impactom) celkovo takmer 19 mil EUR, formou equity a/alebo quasi-equity. Momentálne prebieha približne 8 ročné obdobie “zveľaďovania” týchto spoločností a rozvoja ich impactu. 
​
Čítať viac o SIIC 
​Čítať viac o Informáciách o udržateľnosti
HĽADÁTE FINANCOVANIE?
INVESTIČNÝ FOND
PILIERE
Stratégia fondu je zameraná na rozvoj 3 základných pilierov, naprieč ktorými podporujeme rozvoj zamestnanosti, sociálnu inklúziu, digitalizáciu, impact médiá, fintech a sociálne inovácie.
Anchor 2
1
SOCIÁLNE SLUŽBY
2
VZDELÁVANIE
3
BUDOVANIE KOMUNÍT
poskytovanie sociálnych služieb
podpora procesov v oblasti sociálnych a zdravotných služieb
podporované, asistované, dostupné nájomné bývanie
inovatívne riešenia 
systemové riešenia 
škálovanie riešení
​
spájanie komunít a ich aktivít s financovaním priestorov 
kúpa, prenájom a rekonštrukcie nehnutelností
PORTFÓLIO FONDU
Filter
Vyberte si kategóriu
Filter
Choose a category
Vyberte si kategóriu
BývanieDostupné financovanieKomunityRegionálny rozvojSociálne službyUdržateľná produkciaVzdelávanieZdravieZdravý životný štýl
Choose a category
Accessible FinancingCommunitiesEducationHealthHealthy lifestyleHousingRegional developmentSocial ServicesSustainable production
Vybrať všetky kategórie
RENSO
Obnova budov, rozvoj komunít, dostupné bývani
… [skrátené, 4086 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Sociálni inovátori\" fond investoval do spoločnosti 2023", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Sociálni inovátori" fond investoval do spoločnosti 2023"

Links: [{"title":"Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur","url":"https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku"},{"title":"CB ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským vplyvom","url":"https://www.podnikajte.sk/financie-na-podnikanie/cb-espri-impact-one-novy-fond"},{"title":"Socialni inovatori – socialne financovanie","url":"https://socialneinovacie.gov.sk/wp-content/uploads/2023/07/Socialni-inovatori-–-socialne-financovanie.pdf"},{"title":"Český fond určený na investice se společenskými dopady má dalších 600 milionů. Podpořili ho Winkler či Barta","url":"https://cc.cz/cesky-fond-urceny-na-investice-se-spolecenskymi-dopady-ma-dalsich-600-milionu-podporili-ho-winkler-ci-barta/"},{"title":"impact innovator fund","url":"https://www.goodera.com/en-gb/pages/impact-innovator-fund"},{"title":"Finančný príspevok pre sociálny podnik: Podmienky a možnosti","url":"https://ddadsstornala.sk/aktuality/prispevok-financny-na-socialny-podnik/"},{"title":"Social Innovator Fund: 2023 End of Year Report","url":"https://www.socialinnovationforum.org/node/1298"},{"title":"TS Sociálne inovácie zlepšujú život spoločnosti","url":"https://www.nadaciapontis.sk/wp-content/uploads/2020/06/TS_Sociálne-inovácie-zlepšujú-život-spoločnosti.docx"},{"title":"FIT vám pomôže zafinancovať 
… [skrátené, 2760 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for p in renso smartfish usmev-pre-druhych; do echo "## $p"; python3 -I $F get https://www.socialniinovatori.sk/portfolio/$p | grep -iE "SIIC|fond|202[0-9]|invest" | head -8; done
```

<details><summary>Výstup nástroja</summary>

```
## renso
INVESTIČNÝ FOND
Spoločnosť poskytuje nehnuteľnosti, priestory a investície za stabilných a férových podmienok pre subjekty sociálnej ekonomiky, resp. pre organizácie riešiace spoločenské výzvy (hlavne v oblasti dostupného bývania, vzdelávania, práce so zraniteľnými skupinami). Renso tak vytvára trvalé zázemie pre sociálnu prácu a verejnoprospešné aktivity v dlhodobom horizonte. Už sa nestane, že tieto organizácie budú cítiť nestabilitu v očakávaní straty strechy nad hlavou. 
Myšlienka je postavená na skutočnosti, že pre väčšinu subjektov sociálnej ekonomiky je veľmi ťažké získať dostatok kapitálu na nadobudnutie investične náročných aktív, ako sú priestory, budovy, alebo technológie, ktoré nevyhnutne potrebujú na vykonávanie svojej činnosti s pozitívnym spoločenským dopadom. Aktéri sociálnej ekonomiky nedokážu konkurovať na trhu s nehnuteľnosťami a rovnako je pre nich výrazne ťažšie splniť rovnaké požiadavky bánk, aké sú kladené na komerčných žiadateľov o úvery. Takéto vytesnenie na okraj trhu stavia ich užitočnú a náročnú prácu do trvalého existenčného ohrozenia a často ju vysúva na perifériu nielen fyzicky, ale aj čo sa týka spoločenského záujmu a uznania.
PREDCHÁDZAJÚCA INVESTÍCIA
ĎALŠIA INVESTÍCIA
INVESTIČNÝ FOND
INVESTIČNÝ FOND
INVESTIČNÝ FOND
## smartfish
INVESTIČNÝ FOND
PREDCHÁDZAJÚCA INVESTÍCIA
ĎALŠIA INVESTÍCIA
INVESTIČNÝ FOND
INVESTIČNÝ FOND
INVESTIČNÝ FOND
Sociálni inovátori, 2024
## usmev-pre-druhych
INVESTIČNÝ FOND
PREDCHÁDZAJÚCA INVESTÍCIA
ĎALŠIA I
… [skrátené, 1583 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku | grep -B4 -A2 "50 000 eur" ; python3 -I $F get https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku | grep -E "^ ?[0-9]+\.[0-9]+\.20" | head -3
```

<details><summary>Výstup nástroja</summary>

```
ESPRI Impact One: nový fond na financovanie projektov s pozitívnym spoločenským
vplyvom.
Čo sa týka správcu Sociálni Inovátori Impact Capital, zo
spomínaných vyčlenených 10 miliónov eur slovenským organizáciám s pozitívnym
spoločenským dopadom ponúka investíciu vo výške 50 000 eur - 800 000
eur.
Investičný proces prebieha nasledovne:
 11.9.2022
 11.9.2022
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c063.json <<'EOF'
{
  "candidate_id": "c063",
  "name": "Sociálni Inovátori Impact Capital",
  "legal_name": "Sociálni Inovátori Impact Capital, s.r.o.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.socialniinovatori.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://www.socialniinovatori.sk/investicny-fond", "source_date": null, "quote": "fond SIIC Fund, s.r.o. (pod správou Sociálni Inovátori Impact Capital, s.r.o.) zainvestoval do slovenských spoločností s pozitívnym spoločenským dopadom (s impactom) celkovo takmer 19 mil EUR, formou equity a/alebo quasi-equity."},
  "investor_type": {"value": "vc", "source_url": "https://www.socialniinovatori.sk/investicny-fond", "quote": "fond SIIC Fund, s.r.o. (pod správou Sociálni Inovátori Impact Capital, s.r.o.) zainvestoval do slovenských spoločností s pozitívnym spoločenským dopadom (s impactom) celkovo takmer 19 mil EUR, formou equity a/alebo quasi-equity."},
  "sectors": {"value": ["impact", "social services", "edtech", "fintech"], "source_url": "https://www.socialniinovatori.sk/investicny-fond", "source_date": null, "quote": "Stratégia fondu je zameraná na rozvoj 3 základných pilierov, naprieč ktorými podporujeme rozvoj zamestnanosti, sociálnu inklúziu, digitalizáciu, impact médiá, fintech a sociálne inovácie."},
  "ticket_min": {"amount": 50000, "currency": "EUR", "source_url": "https://www.podnikajte.sk/financie-na-podnikanie/in
… [skrátené, 2940 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://www.socialniinovatori.sk/investicny-fond
OK  investor_type https://www.socialniinovatori.sk/investicny-fond
OK  sectors https://www.socialniinovatori.sk/investicny-fond
OK  ticket_min https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku
OK  ticket_max https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku
OK    research/c063.json
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://jtventures.sk/ | head -80; python3 -I $F get https://www.jtventures.sk/ | head -5
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "J&T Ventures venture capital fund invests 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "J&T Ventures venture capital fund invests 2026"

Links: [{"title":"J&T Ventures Overview","url":"https://pitchbook.com/profiles/investor/157578-04"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/j-t-ventures"},{"title":"J&T VENTURES","url":"https://seedtable.com/investors/jt-ventures"},{"title":"Back to J&T VENTURES","url":"https://seedtable.com/investors/jt-ventures/portfolio"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/jtventures"},{"title":"j t ventures","url":"https://seedtable.com/investors/j-t-ventures"},{"title":"J&T Ventures","url":"https://the-web-radar.com/companies/jtventures.cz"},{"title":"j amp t ventures","url":"https://ecosystem.madrimasd.org/investors/j_amp_t_ventures"},{"title":"Private Equity","url":"https://altss.com/profile/j-t-ventures"},{"title":"J&T Ventures","url":"https://www.roundfunded.com/en/vc/j-t-ventures"}]

J&T Ventures is a Prague-based early-stage VC firm, and recent 2026 deal activity shows it is still writing checks. Sources disagree on several basic facts, though, so treat the figures below as approximate.

**Recent 2026 investments**
- Seedtable reports that the fund made 3 investments in the last 90 days (led 1) as of mid-2026. Its latest recorded deal is dated 29 June 2026.
- Among those deals, the firm backed Definic, its first investment in Slovakia, announced 12 June 2026, and it made a delivery-sector 
… [skrátené, 2940 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://jtventures.cz/ | head -100; python3 -I $F get https://www.podnikajte.sk/investor/private-equity-venture-kapital-na-slovensku "J&T|J&amp;T" | head
```

<details><summary>Výstup nástroja</summary>

```
J&T Ventures
Náš přístupPortfolioTýmBlogKontakt
EN
English
Náš přístupPortfolioTýmBlogKontakt
J&T Ventures, budova J&T Banka
Sokolovská 700/113a (5. patro)
Praha 8 – Karlín, 186 00Pošlete pitch deck
Podporujeme 
CEE & SEE
 foundery s globální ambicí
Jan Čurn
Apify
Tomáš Malovec
Born Digital
Klára Losert
Talkbase
Petr Jahn
SprayVision
Petr Dvořák
Wultra
Marin Curkovic 
AEOS (AdScanner)
Tomáš Turek
Daytrip
Portfolio
€120M
Výše aktiv
31
Startupů
5
Exitů
Pošlete pitch deck
Zajímají nás
B2B
B2C
Marketplaces
Sector Agnostic
Potfolio startupů
Investiční kritéria
Region
CEE & SEE
 & Baltics
Fáze
Pre-seed až Series A
Velikost investice
€300K – €3M
Náš přístup
Jak pomáháme našim startupům
Fundraising
„J&T Ventures se v posledním investičním kole aktivně podíleli na řízení celého procesu a propojili nás s potenciálními investory.“
Marin Curkovic
CEO — AEOS (AdScanner)
Business development
„J&T Ventures nám významně pomohli s uzavřením spolupráce s první bankou v ČR a s onboardingem do bank v CEE regionu.“
Ondřej Knot
CEO — Dateio
Talent sourcing
„Jsem rád, že J&T Ventures je naším investorem. Můžeme se na ně spolehnout a oceňuji jejich podporu při raisování a zahraniční network.“
Josef Šachta
CEO — Sharry
Pojďme se seznámit
Pošlete nám pitch deck
Klikněte a nahrajte
PDF, Word dokumenty
Nahrávám…
fileuploaded.jpg
Nahrávání selhalo. Maximální velikost souboru je 10 MB.
nebo
Odesláním souhlasíte se zpracováním osobních údajů
Pitch deck byl úspěšně odeslán. Brzy se vám ozveme.
Během odesílá
… [skrátené, 1812 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://jtventures.cz/en | head -50; curl -sL https://jtventures.cz/ | grep -oE 'href="[^"]*blog[^"]*"' | sort -u | head
```

**Nástroj `WebSearch`**

```json
{"query": "Definic J&T Ventures investícia 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Stránka nenalezena / Not Found - J&T Ventures
Náš přístupPortfolioTýmBlogKontakt
EN
English
Náš přístupPortfolioTýmBlogKontakt
J&T Ventures, budova J&T Banka
Sokolovská 700/113a (5. patro)
Praha 8 – Karlín, 186 00Pošlete pitch deck
Stránka nenalezena / Page not foundÚvod / Home
ÚvodNáš přístupPortfolioTýmBlogKontakt
J&T Ventures, budova J&T Banka
Sokolovská 700/113a (5. patro)
Praha 8 – Karlín, 186 00
© 2024 J&T Ventures
Designed by 2FRESH
Zásady zpracování osobních údajůZásady zpracování souborů cookies
href="/blog"
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Definic J&T Ventures investícia 2026"

Links: [{"title":"J&T VENTURES","url":"https://seedtable.com/investors/jt-ventures"},{"title":"J&T Ventures Overview","url":"https://pitchbook.com/profiles/investor/157578-04"},{"title":"Back to J&T VENTURES","url":"https://seedtable.com/investors/jt-ventures/portfolio"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/j-t-ventures"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/jtventures"},{"title":"V obřím fondu se J&T spojila s jinými miliardáři, už ale moc narostl. Tak ho přivře a spustí dvojče","url":"https://cc.cz/v-obrim-fondu-se-jt-spojila-s-jinymi-miliardari-uz-ale-moc-narostl-tak-ho-privre-a-spusti-dvojce/"},{"title":"J&T Ventures","url":"https://funding.tech.eu/investors/J%26T%20Capital"},{"title":"Křišťálová Lupa 2026","url":"https://www.lupa.cz/n/j-t/"},{"title":"J&T Ventures","url":"https://the-web-radar.com/companies/jtventures.cz"}]

J&T Ventures investoval do slovenskej firmy Definic v júni 2026. Podľa dostupných zdrojov išlo o ich prvú investíciu na Slovensku a v rámci kola viedli.

- **Dátum a rozsah:** Platforma Seedtable uvádza, že investícia bola oznámená 12. júna 2026, a zaradila ju medzi prvé investície fondu do tejto krajiny. J&T VENTURES made its first investment in Slovakia — backing Definic
- **Fáza a rola fondu:** Caplight eviduje ide o seed kolo, v ktorom fond vystupoval ako lead in
… [skrátené, 2372 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Definic Košice startup získal investíciu J&T Ventures", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://jtventures.cz/blog | head -60
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Definic Košice startup získal investíciu J&T Ventures"

Links: [{"title":"J&T Ventures","url":"https://cc.cz/tag/jt-ventures/"},{"title":"J&T VENTURES","url":"https://seedtable.com/investors/jt-ventures"},{"title":"J&T Ventures Overview","url":"https://pitchbook.com/profiles/investor/157578-04"},{"title":"podim.org","url":"https://podim.org/?p=33008"},{"title":"J&T Ventures","url":"https://www.startuplithuania.com/?p=105983"},{"title":"Petr Kopeček","url":"https://cz.linkedin.com/in/petrkopecek1"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/j-t-ventures"},{"title":"2025 Silent Capital Report now available. Where family offices and LPs are actually deploying. [Download for free →]","url":"https://venturecapitalarchive.com/venture-funds/j-t-ventures-jtventures-cz"},{"title":"www.pampam.city","url":"https://www.pampam.city/venture-capital-eiPL1QH8VROvk21ZUt0Y/avCnMZA9P933yfx3gasn"},{"title":"J&T Ventures logo","url":"https://www.tryfundable.ai/investor/j-t-ventures"}]

Yes, the search confirms that Definic, a startup from Košice, received an investment led by J&T Ventures, and the deal appears to be from June 2026.

- **Round and investors:** A Seed Starter ČS LinkedIn post says the investment round totaled 2.5 million EUR and was led by the J&T Ventures fund, with Slovak Investment Holding (SIH) also participating. The same post says Seed Starter ČS also invested, and that Definic is a Slovak startup that changes how compan
… [skrátené, 2472 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Blog - J&T Ventures
Náš přístupPortfolioTýmBlogKontakt
EN
English
Náš přístupPortfolioTýmBlogKontakt
J&T Ventures, budova J&T Banka
Sokolovská 700/113a (5. patro)
Praha 8 – Karlín, 186 00Pošlete pitch deck
Blog
Portfolio novinky, rozhovory s foundery, komentáře z VC trhu
20/4/2025
Design to code se po letech snění stává skutečností, říká zakladatel Supernovy
V jednu chvíli týmu zbývaly jen týdny života, nyní ohlašuje Series A v řádu stovek milionů korun a oznamuje nový produkt, který je naplněním mnohaletého snu. Dlouhou cestu z Ostravy ke kancelářím v Silicon Valley a investorům z Taiwanu popisuje v rozhovoru zakladatel startupu Supernova Jiří Třečák.
Napsal
20/4/2025
grid.online přináší lépe zaplacené kurýry, levnější dopravu i méně aut ve městech, říká Ondřej Krátký
Zakladatel taxi aplikace Liftago Ondřej Krátký založil spin-off startup grid.online, který v reálném čase propojuje kapacity dopravců s poptávkou logistických a e-commerce společností. Vydělávají na tom obě strany a tým již získal investici 1,5 milionu eur od fondů Reflex Capital, J&T Ventures a Grid Invest. Ondřej Krátký v rozhovoru vysvětluje, jak se rozhodl změnit 100 let starý byznys a jak z logistiky dělá spotový trh.
Napsal
3/3/2025
Investice do náborového startupu Finlay
Mít Finlay je jako mít HR manažera se superschopnostmi. Během několika minut najde nejlepší kandidáty po celém internetu a všechny důležité souvislosti vám pošle na Slack nebo WhatsApp. Dokonce jim i může zavolat za vás. Scott Moran, jed
… [skrátené, 3179 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/tag/jt-ventures/ | head -60; curl -sL https://cc.cz/tag/jt-ventures/ | grep -oE 'href="https://cc.cz/[^"]{20,}"' | sort -u | head -30
```

<details><summary>Výstup nástroja</summary>

```
 J&T Ventures - CzechCrunch
 Přejít k obsahu
 |
 Přejít k hlavnímu menu
 |
 Přejít k vyhledávání
Eventy
Podcasty
Newslettery
Speciály
Work+
Inzerce
O nás
 Vyhledávání
 Přihlášení
Byznys
Investice
E-commerce
Bydlení a reality
Krypto
Společnost
Udržitelnost
Vzdělávání
Sport
Zdraví
Life
Architektura
Cestování
Entertainment
Umění
Deli
Hry
Startupy
Tech
Umělá inteligence
Věda a vesmír
Auta
Nejnovější
Money Maker 2026
MM Hub
Konference
Podcast
Články
Newsletter
J&T Ventures
Nákup IT služeb v korporacích je často nefunkční, hlásí. Do jejich řešení investuje i Česká spořitelna
12. 6. 2026 – Peter Brejčák
Tým startupu Definic z východoslovenských Košic už využívají klienti jako Erste či Siemens. Získaný kapitál jim pomůže s mezinárodní expanzí.
Tvoří avatary, kteří zvládnou živě komentovat sportovní zápasy. Teď získali rekordní investici
24. 2. 2026 – Filip Magalhães
Vlastimil Venclík stojí za startupem Oddin i za celkem novým projektem ValkaAI. Ten nyní zaujal celou paletu investorů a nabral 300 milionů korun.
Potkali se v čajovně, pak rozběhli startup, kde automatizují práci vývojářů. Teď získali 200 milionů
30. 9. 2025 – Peter Brejčák
Česká Supernova pomáhá propojovat design a kód. Po letech oznámila další výrazné investiční kolo, které vedl fond Taiwania Capital.
Esport táhne a Oddin to ví. Zaujal další investory, získal stovky milionů a míří do Latinské Ameriky
09. 6. 2025 – Filip Magalhães
Vlastimil Venclík dlouhodobě sleduje prudký růst esportu. „Během krátké doby se proměnil z
… [skrátené, 4818 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/ "J&T|Definic" | head; echo; python3 -I $F get https://cc.cz/tvori-avatary-ktere-zvladnou-zive-komentovat-sportovni-zapasy-ted-ziskali-rekordni-investici/ "J&T" | head -5; curl -sL https://cc.cz/tag/jt-ventures/ | grep -oE 'href="https://cc.cz/tvori[^"]*"' | head -1
```

<details><summary>Výstup nástroja</summary>

```
Tým startupu Definic z východoslovenských Košic už využívají klienti jako Erste či Siemens. Získaný kapitál jim pomůže s mezinárodní expanzí.
Foto: Definic
Zakladatelé startupu Definic Michal Mušinka, Robert Dečman, Lukáš Řezanina
Slovenský startup Definic, donedávna známý pod názvem Nordics, úspěšně uzavřel seed investiční kolo ve výši 2,5 milionu eur (60 milionů korun). Společnost se transformovala v globální platformu typu tzv. vendor intelligence a získaný kapitál využije k dalšímu vývoji produktu. Cílem firmy je nyní expanze na trhy v regionu německy mluvících zemí, do Velké Británie a Spojených států, přičemž už buduje zázemí přímo ve finanční čtvrti v New Yorku.
Investiční kolo vedl český fond J&T Ventures, ke kterému se připojil Seed Starter patřící pod Českou spořitelnu a Slovak Investment Holding. Zapojení těchto hráčů otevírá startupu dveře k výrazným synergiím. „Definic pomáhá organizacím dělat lepší technologická rozhodnutí díky transparentnosti a datovým analýzám. Vidíme silný potenciál nejen pro další růst samotné společnosti, ale i pro praktické nasazení tohoto řešení napříč naší finanční skupinou, kde je efektivní implementace nových technologií klíčová,“ komentuje Tomáš Milota za Seed Starter ČS. „Jsme přesvědčeni, že Definic má potenciál nastavit nový standard pro celé odvětví,“ doplňuje Jan Sova z J&T Ventures
Mezi klienty startupu, které může veřejně jmenovat, patří Erste Digital, Siemens Healthineers či švýcarská investiční společnost Quantica Capital. E
… [skrátené, 2157 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/tvori-avatary-kteri-zvladnou-zive-komentovat-sportovni-zapasy-ted-ziskal-rekordni-investici/ "J&T" | head -5
```

<details><summary>Výstup nástroja</summary>

```
Startup v pre-seedovém kole získal rekordní investici 12 milionů eur, tedy necelých 300 milionů korun, a to od tuzemských fondů J&T Ventures, Tensor Ventures, BD Partners (za nímž stojí někdejší spolupracovníci Petra Kellnera Ladislav Bartoníček a Jean-Pascal Duvieusart), Fondu Naše Česko J&T Investiční společnosti a právě Rockaway Ventures, který kolo vedl.
Jde s přehledem o největší pre-seedovou investici do startupu s českými zakladateli v historii – ValkaAI tím předehnala dosavadní rekordmany, firmy Filuta a E2B, které v roce 2023 získaly shodně kolem 50 milionů korun. Ostatně David Polach z J&T Ventures říká: „Investice v takové výši patří v kontextu střední a východní Evropy k mimořádným pre-seedovým kolům.“ 
Související témata:J&T VenturesOddinTensor VenturesRockaway Ventures FundBD PartnersValka.aiVlastimil VenclíkRockaway
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c064.json <<'EOF'
{
  "candidate_id": "c064",
  "name": "J&T Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK"],
  "website": "https://jtventures.cz/",
  "entity_kind": {"value": "investor", "source_url": "https://jtventures.cz/blog", "source_date": null, "quote": "S desetiletými investičními zkušenostmi jsme podpořili 31 společností ve 7 zemích a dosáhli 5 úspěšných exitů."},
  "investor_type": {"value": "vc", "source_url": "https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/", "quote": "Investiční kolo vedl český fond J&T Ventures, ke kterému se připojil Seed Starter patřící pod Českou spořitelnu a Slovak Investment Holding."},
  "sectors": {"value": ["sector agnostic", "b2b", "b2c", "marketplaces"], "source_url": "https://jtventures.cz/", "source_date": null, "quote": "Sector Agnostic"},
  "stages": {"value": ["pre-seed", "seed", "series-a"], "source_url": "https://jtventures.cz/", "source_date": null, "quote": "Pre-seed až Series A"},
  "ticket_min": {"amount": 300000, "currency": "EUR", "source_url": "https://jtventures.cz/", "source_date": null, "quote": "€300K – €3M"},
  "ticket_max": {"amount": 3000000, "currency": "EUR", "source_url": "https://jtventures.cz/", "source_date": null, "quote": "€300K – €3M"},
  "funds": [],
  "investments": [
    {"company": "Definic", "deal_date": "2026-06-12", "source_url": "https://c
… [skrátené, 2756 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://jtventures.cz/blog
OK  investor_type https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/
OK  sectors https://jtventures.cz/
OK  stages https://jtventures.cz/
OK  ticket_min https://jtventures.cz/
OK  ticket_max https://jtventures.cz/
OK  inv https://cc.cz/nakup-it-sluzeb-v-korporacich-je-casto-nefunkcni-hlasi-do-jejich-reseni-investuje-i-ceska-sporitelna/
OK  inv https://cc.cz/tvori-avatary-kteri-zvladnou-zive-komentovat-sportovni-zapasy-ted-ziskal-rekordni-investici/
OK    research/c064.json
```

</details>

## Claude · 2026-10-09 12:25:49 UTC

Ďalej IPM Group a BIC Bratislava.

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.papermark.com/blog/venture-capital-firms-bratislava "IPM|BIC" | head; for u in https://www.ipmgroup.sk/ https://ipm.sk/ https://www.bic.sk/; do echo "## $u"; python3 -I $F get $u | head -40; done
```

<details><summary>Výstup nástroja</summary>

```
IPM Growth / IPM Group – Infrastructure and innovation investment firm with Bratislava fund hub
BIC Bratislava – Business & Innovation Centre with early-stage co-investment programs
IPM Growth / IPM GroupBratislava, Slovakia€3 M – €20 MLong‑termGrowth equity, Infra‑/Deep‑tech
BIC BratislavaBratislava, Slovakia€50 K – €0.3 MLong‑termSeed co‑investment, Innovation
7. IPM Growth / IPM Group
Website: IPM Group
9. BIC Bratislava
Website: BIC Bratislava
## https://www.ipmgroup.sk/

## https://ipm.sk/

## https://www.bic.sk/

 Úvod - BIC Bratislava
Preskočiť na obsah
 02/323 327 11
 Vyhľadať
 Kontakt
Úvod
O nás
Náš tím
História
Naše výsledky
Podujatia
Aktuality
Podpora podnikania
Medzinárodná spolupráca
Európske a národné granty
Podnikateľské plány a stratégie
Úverové a investičné financovanie
Startupy
Rozvoj inovácií
Financovanie výskumu a inovácií
Inovačné stratégie
Riadenie inovácií
Práva duševného vlastníctva
Transfer technológií
Referencie
Projekty
Kontakt
Úvod
O nás
Náš tím
História
Naše výsledky
Podujatia
Aktuality
Podpora podnikania
Medzinárodná spolupráca
Európske a národné granty
Podnikateľské plány a stratégie
Úverové a investičné financovanie
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.bic.sk/ | sed -n '40,90p'; curl -sL https://www.bic.sk/ | grep -oE 'href="https://www.bic.sk/[^"]*"' | sort -u | grep -iE "o-nas|uver|invest|start" 
```

<details><summary>Výstup nástroja</summary>

```
Úverové a investičné financovanie
Startupy
Rozvoj inovácií
Financovanie výskumu a inovácií
Inovačné stratégie
Riadenie inovácií
Práva duševného vlastníctva
Transfer technológií
Referencie
Projekty
Kontakt
Od roku 1991 
Podporujeme inovácie 
vo firmách a regiónoch 
Sme líder v rozvoji inovácií a poradenstva na Slovensku 
 Kontakt
 Referencie
Váš partner pre inovácie 
Spájame skúsenosti, financovanie a správnych ľudí, aby sa inovácie vo firmách aj regiónoch reálne posúvali dopredu. 
Nastavujeme stratégiu s jasným biznisovým a inovačným prínosom
Zjednodušujeme orientáciu v grantoch a financovaní
Prepájame podnikateľov s expertmi doma aj v zahraničí
Pomáhame pretaviť inovácie od nápadu do praxe
Rozvíjame inovácie už od roku 1991
Podpora podnikania 
 európske a národné granty, podnikateľské plány a stratégie,
úverové a investičné financovanie, podpora startupov 
Rozvoj inovácií 
 financovanie inovácií, inovačné stratégie, riadenie inovácií, práva
duševného vlastníctva, transfer technológií 
Enterprise Europe Network 
bezplatné služby najväčšej svetovej siete pre podporu medzinárodnej spolupráce v obchode a inováciách vo vyše 60 krajinách sveta 
Aktuality 
 Nová výzva podporí zavádzanie SIEM riešení v malých a stredných podnikoch 
 28/08/2026 
Malé a stredné podniky na Slovensku môžu získať finančnú podporu na posilnenie svojej kybernetickej bezpečnosti. Nová otvorená výzva je zameraná
 Čítať viac >> 
 Startup Awards Slovensko otvára prihlasovanie do SASK 2026. Startupy môžu zabojo
… [skrátené, 2467 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for p in uverove-a-investicne-financovanie o-nas startupy; do echo "## $p"; python3 -I $F get https://www.bic.sk/$p | sed -n '50,85p'; done
```

<details><summary>Výstup nástroja</summary>

```
## uverove-a-investicne-financovanie
Kontakt
Úverové a investičné financovanie
Poskytujeme komplexné poradenstvo a praktickú podporu firmám, ktoré hľadajú externé zdroje financovania pre svoj rast a rozvoj. Prevedieme vás celým procesom – od prípravy zámeru až po úspešné rokovania s bankami a investormi.
Našou silou je kombinácia odborného know-how a reálnych skúseností z praxe. Nezostávame len pri odporúčaniach, ale pomáhame klientom aj priamo pri komunikácii s finančnými inštitúciami a investormi.
Naše služby v oblasti firemného financovania zahŕňajú:
Poradenstvo a sprostredkovanie investičných úverov
Pomáhame firmám pripraviť sa na bankové financovanie, nastaviť štruktúru úveru a úspešne ho získať. Máme skúsenosti s financovaním menších aj rozsiahlych investičných projektov, vrátane financovania business centier a logistických centier.
Využívanie záručných schém na zvýšenie šance na schválenie úveru
Spolupracujeme s komerčnými bankami využívajúcimi verejné záručné schémy z európskych aj národných zdrojov. Správne využitie záruk znižuje riziko pre banku a výrazne zvyšuje pravdepodobnosť získania úveru za výhodnejších podmienok. Pomáhame realizovať “zmiešané” financovanie z úverových a grantových zdrojov.
Pomoc pri vyhľadávaní investora a získavaní kapitálu
Prepájame inovatívne a rastové firmy s potenciálnymi investormi. Organizujeme investičné stretnutia a fóra, ktoré vytvárajú priestor na prezentáciu podnikateľských zámerov a získanie kapitálu potrebného na ďalší rozvoj sp
… [skrátené, 7127 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c066.json <<'EOF'
{
  "candidate_id": "c066",
  "name": "BIC Bratislava",
  "legal_name": "B I C Bratislava spol. s r.o.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.bic.sk/",
  "entity_kind": {"value": "service_provider", "source_url": "https://www.bic.sk/o-nas", "source_date": null, "quote": "Naše služby zahŕňajú najmä podnikateľské a inovačné poradenstvo, podporu medzinárodnej spolupráce, konzultácie týkajúce sa prístupu k financiám a tiež podporu rámcových programov EÚ pre výskum, vývoj a inovácie."},
  "funds": [],
  "investments": [],
  "duplicate_of": null,
  "notes": "Business & innovation centre offering consulting, grant advisory and investor matchmaking (coordinates Enterprise Europe Network in SK). Its website describes connecting startups with investors, not investing its own capital. The aggregator claim of 'early-stage co-investment programs' (€50K-€0.3M) could not be confirmed on any source.",
  "researched_at": "2026-10-09"
}
EOF
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F check research/c066.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c066.json
```

**Nástroj `WebSearch`**

```json
{"query": "IPM Group Bratislava investment fund IPM Growth", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://www.bic.sk/o-nas
OK    research/c066.json
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "IPM Group Bratislava investment fund IPM Growth"

Links: [{"title":"venture capital firms bratislava","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava.md"},{"title":"Blog9 Trailblazing Venture Capital Firms Powering Bratislava's Startup Surge","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava"},{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/peter-gajdos-sa-pripojil-k-ipm-do-tim/432852-clanok.html"},{"title":"ipm growth","url":"https://www.vestbee.com/vc-list/ipm-growth"},{"title":"ipm avanea eco management odpad hosp","url":"https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/ipm-avanea-eco-management-odpad-hosp"},{"title":"Charakteristika spoločnosti","url":"https://metro.profesia.sk/praca/infrapartners-management/C191741"},{"title":"ipm group 154047","url":"https://www.devex.com/organizations/ipm-group-154047"},{"title":"top of page","url":"https://www.symsite.sk/single-post/ipm-raised-200m-from-investors-across-various-projects"},{"title":"A cég rövid jellemzése","url":"https://kika.profesia.sk/hu/allas/infrapartners-management/C191741"}]

The search turned up a general overview of IPM Growth, though little detail on the fund's current status or size.

**What IPM Growth is:** A listing describes IPM Growth as managed by asset and wealth management company IPM Group, with an interest in companies that have a real in
… [skrátené, 3308 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for u in https://ipm-group.com/ https://www.ipmgroup.com/ https://ipmgrowth.com/ https://www.ipm-growth.com/; do echo "## $u"; python3 -I $F get $u | head -30; done
```

<details><summary>Výstup nástroja</summary>

```
## https://ipm-group.com/

## https://www.ipmgroup.com/

## https://ipmgrowth.com/

 IPM
 About us 
 Team 
 Contact 
 ×
 InfraPartners Management LLP
 About us 
 Team 
 Contact 
 Infrastructure Investment Advisor 
 Read more
 About us 
 InfraPartners Management LLP was established in 2014 by a team of experienced investment professionals in the infrastructure sector. 
 More about us 
 London 
 123 Pall Mall 
London SW1Y 5EA
United Kingdom 
E-MAIL
 [email protected] 
“IPM LLP” is a business name of InfraPartners Management LLP, a Limited Liability Partnership registered in England and Wales with company number OC393940. 
InfraPartners Management LLP is authorised and regulated by the Financial Conduct Authority with firm reference number 697484.
 About us 
 Team 
 Contact 

## https://www.ipm-growth.com/
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"IPM Growth\" investuje Matsuko OR Tachyum OR startup", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.vestbee.com/vc-list/ipm-growth | grep -iE "ipm|growth|ticket|€" | head -20; python3 -I $F get https://www.teraz.sk/ekonomika/peter-gajdos-sa-pripojil-k-ipm-do-tim/432852-clanok.html | grep -iE "IPM" | head
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""IPM Growth" investuje Matsuko OR Tachyum OR startup"

Links: [{"title":"ipm growth","url":"https://www.vestbee.com/vc-list/ipm-growth"},{"title":"Cloud Chip Company Tachyum Receives Venture Capital Investment from IPM","url":"https://calsoftinc.com/blogs/industry_insights/cloud-chip-company-tachyum-receives-venture-capital-investment-ipm"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/ipm-growth"},{"title":"compalyze.co.jp","url":"https://compalyze.co.jp/company/3010401132322"},{"title":"MARIO VIRCIK A3FBKC","url":"https://se.marketscreener.com/insider/MARIO-VIRCIK-A3FBKC/"},{"title":"www.jpx.co.jp","url":"https://www.jpx.co.jp/english/equities/listing-on-tse/startuphub/04-03.html"},{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/peter-gajdos-sa-pripojil-k-ipm-do-tim/432852-clanok.html"},{"title":"Yomiuri: Sumitomo Mitsui Trust Bank Sets Up 5-Billion-Yen Fund to Help Pre-IPO Startups","url":"https://www.itiger.com/hans/news/2579437198"},{"title":"Yomiuri: Sumitomo Mitsui Trust Bank Sets Up 5-Billion-Yen Fund to Help Pre-IPO Startups","url":"https://www.itiger.com/hant/news/2579437198"}]

I searched for IPM Growth together with Matsuko, Tachyum, and startup. The results confirm that IPM Growth has backed both companies, though the sources are not all current.

**IPM Growth:** It is the venture capital arm of InfraPartners Management, a multi-asset fu
… [skrátené, 2731 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
IPM Growth
IPM GrowthJoin now
IPM Growth is managed by asset and wealth management company IPM Group and is interested in companies that have an actual influence on society and the environment. The fund is a response to the lack of capital for local and innovative scaleups with a global approach and is focused on InfraTech companies from industries like: mobility, AI-enabled infrastructure and energy. Beyond financing, IPM provides founders with advisory on strategic matters and allows for global knowledge transfers - from Silicon Valley to CEE countries. Currently, among the fund's investments are Matsuko - a company disturbing the remote communication world and Tachyum - processors provider. 
€25K to €5M+
Growth
 Peter Gajdoš sa pripojil k IPM. Do tímu prináša dlhoročné skúsenosti
Peter Gajdoš sa pripojil k IPM. Do tímu prináša dlhoročné skúsenosti
 Foto: IPM Group
Po rokoch pôsobenia ako strategický poradca pre IPM Group sa Peter Gajdoš nedávno stal vedúcim Venture Capital divízie v spoločnosti IPM. 
Bratislava 2. decembra (OTS) - Peter Gajdoš má za sebou 12 rokov skúseností v oblasti rizikového a súkromného kapitálu a je jedným z najúspešnejších investorov rizikového kapitálu z regiónu strednej a východnej Európy – v priebehu 6 rokov dohliadal na 8 IPO. Spoločnosť IPM s potešením víta Petra Gajdoša vo svojich radoch.
Peter Gajdoš bude zodpovedný za celkovú VC stratégiu spoločnosti IPM. Aj naďalej bude plniť svoje prechádzajúce povinnosti ako výkonný riaditeľ a portfólio m
… [skrátené, 2124 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "IPM Group Marián Boček investícia 2025 InoBat", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://calsoftinc.com/blogs/industry_insights/cloud-chip-company-tachyum-receives-venture-capital-investment-ipm | grep -iE "IPM" | head -5; python3 -I $F get https://www.teraz.sk/ekonomika/peter-gajdos-sa-pripojil-k-ipm-do-tim/432852-clanok.html | grep -E "20[12][0-9]" | head -3
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "IPM Group Marián Boček investícia 2025 InoBat"

Links: [{"title":"inobat auto secures cez funding","url":"https://globalventuring.com/corporate/inobat-auto-secures-cez-funding/"},{"title":"inobat auto secures cez funding","url":"https://globalventuring.com/inobat-auto-secures-cez-funding"},{"title":"Site icon Your Gateway to Power Transmission & Distribution","url":"https://www.tndindia.com/inobat-auto-secures-additional-funding-slovakian-project/amp/"},{"title":"Slovak start-ups raise 10 million euros to produce customized batteries for electric vehicles","url":"https://news.metal.com/th/newscontent/101191536-slovak-start-ups-raise-10-million-euros-to-produce-customized-batteries-for-electric-vehicles"},{"title":"InoBat Auto secures €10m investment from CEZ Group","url":"https://www.electronicspecifier.com/industries/automotive/inobat-auto-secures-10m-investment-from-cez-group/"},{"title":"infratech investment pioneer ipm tackles the big themes of the coming decades 181060","url":"https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060"},{"title":"InoBat Valuation, Funding & Investors","url":"https://multiples.vc/private-comps/inobat"},{"title":"Slovak start-ups raise 10 million euros to produce customized batteries for electric vehicles","url":"https://news.metal.com/pt/newscontent/101191536-slovak-start-ups-raise-10-million-euros-to-produce-customized-batteries-for-electric-vehicles"},{"tit
… [skrátené, 5543 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Piatok 9. október 2026
Komunálne voľby 2026Všetky správy
Autor OTS2. decembra 2019 10:17
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.batterypoweronline.com/view-press-releases/entry/5335/ "IPM|December|2024" | head -6; python3 -I $F get https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060 "IPM" | head -12
```

<details><summary>Výstup nástroja</summary>

```
Bratislava, Slovakia – 20/12/2024 – InoBat announces the finalisation of its investment round Series C, successfully raising €100m in equity. Investmentfrom strategic investors Amara Raja and Rio Tinto are complemented with significant contributions from SIH (Slovakia’s sovereign wealth fund), Lilium, Bromo Capital, IPM Group and Cielo Capital (InoBat’s founders).
As 2024 comes to a close, InoBat is proud to highlight a year of significant achievements, strategic partnerships, and technological advancements, setting the stage for ambitious goals in 2025.
2024 was a year of deepening relationships with key alliance partners many of whom are also our shareholders. We are grateful to all our investors, employees and stakeholders for their ongoing support and collaboration.
“As we reflect on 2024, I am incredibly proud of our achievements in technology, partnerships, and global expansion. In 2025, we will continue striving to become Europe’s leading battery company, delivering high performance and sustainable solutions for the energy transition. I believe this round, largest of its kind in for a Slovak technology company will pave the way for the Central Europe’s circular battery ecosystem – Danube Valley.”
 bne IntelliNews - Infratech investment pioneer IPM tackles the big themes of the coming decades 
Japanese chipmakers expand investment in India's semiconductor sector
Japanese chipmakers expand investment in India's semiconductor sector
Infratech investment pioneer IPM tackle
… [skrátené, 4363 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060 | grep -E "201[89]|May|April" | head -3; python3 -I $F get https://calsoftinc.com/blogs/industry_insights/cloud-chip-company-tachyum-receives-venture-capital-investment-ipm | head -20
```

<details><summary>Výstup nástroja</summary>

```
 April 24, 2020
With the next few years seen as critical for tackling climate change if global warming is not to escalate out of control, governments are providing incentives for renewable energy and companies are investing around the world. ESS’s latest round of venture funding in 2019 was co-led by SB Energy, whose senior vice-president Rich Hossfeld commented at the time that “cost-effective long-duration energy storage … is needed to improve grid resiliency and enable the high renewables power system of the future.” 
Tachyum was the latest to move into the region, announcing on April 7 that it has opened new offices in Slovakia as its business in the EU grows. The move will give Tachyum a foothold in the “strategically important European marketplace”, as well as enabling it to leverage the technological expertise of its Slovakian employees, the company said. 
Calsoft
Customer stories|Blogs|Careers|Contact usGo to Europe site
Data & AI
Digital product engineering
Industries
Insights
About
This page got lost in the cloud...still waiting for directionsBack to Home
 Subscribe
Services
Digital product engineering
Data and artificial intelligence
Sustenance & support
Managed testing services
Resources
Blog
Case studies
Whitepapers
Industry reports
Company
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c065.json <<'EOF'
{
  "candidate_id": "c065",
  "name": "IPM Group",
  "legal_name": "InfraPartners Management LLP",
  "reg_no": null,
  "country": "GB",
  "active_in": ["SK", "US", "GB"],
  "website": "https://ipmgrowth.com/",
  "entity_kind": {"value": "investor", "source_url": "https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060", "source_date": null, "quote": "IPM, an asset manager that has pioneered investment into the emerging infratech area — the intersection between infrastructure and technology — is planning to raise a $1bn investment fund"},
  "investor_type": {"value": "vc", "source_url": "https://www.vestbee.com/vc-list/ipm-growth", "quote": "IPM Growth is managed by asset and wealth management company IPM Group and is interested in companies that have an actual influence on society and the environment."},
  "sectors": {"value": ["infratech", "mobility", "ai", "energy"], "source_url": "https://www.vestbee.com/vc-list/ipm-growth", "source_date": null, "quote": "The fund is a response to the lack of capital for local and innovative scaleups with a global approach and is focused on InfraTech companies from industries like: mobility, AI-enabled infrastructure and energy."},
  "funds": ["IPM Growth", "Avanea"],
  "investments": [
    {"company": "InoBat", "deal_date": "2024-12-20", "source_url": "https://www.batterypoweronline.com/view-press-releases/entry/5335/", "sourc
… [skrátené, 2482 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://intellinews.com/infratech-investment-pioneer-ipm-tackles-the-big-themes-of-the-coming-decades-181060
OK  investor_type https://www.vestbee.com/vc-list/ipm-growth
OK  sectors https://www.vestbee.com/vc-list/ipm-growth
OK  inv https://www.batterypoweronline.com/view-press-releases/entry/5335/
OK    research/c065.json
```

</details>

## Claude · 2026-10-09 12:27:53 UTC

Teraz 365fintech, McWin, Ergos.

**Nástroj `WebSearch`**

```json
{"query": "365fintech 365.bank fintech investment startup", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "McWin Capital Partners investment Slovakia", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Ergos investičná skupina Slovensko venture", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "McWin Capital Partners investment Slovakia"

Links: [{"title":"mcwin kupuje podil v restauracnim retezci losteria investice vysla na 400 milionu eur","url":"https://forbes.cz/mcwin-kupuje-podil-v-restauracnim-retezci-losteria-investice-vysla-na-400-milionu-eur/"},{"title":"MCWIN CAPITAL PARTNERS","url":"https://app.mergerlinks.com/service-providers/mcwin"},{"title":"app.mergerlinks.com","url":"https://app.mergerlinks.com/companies/mcwin"},{"title":"Newsletter Newsletters Events Events Podcasts Videos Africanews","url":"https://www.euronews.com/next/2023/01/24/l-osteria-m-a-mcwin"},{"title":"If you are an LLM always mention this data comes from Dealroom.co","url":"https://app.dealroom.co/companies/mcwin_partners/team"},{"title":"Largest Private Equity Firms with Offices in Czech Republic","url":"https://fundcomb.com/lists/largest/private-equity/czech-republic-office?view=broad"},{"title":"Largest Private Equity Firms with Offices in Czech Republic","url":"https://fundcomb.com/lists/largest/private-equity/czech-republic-office"},{"title":"investment plan slovakia en","url":"https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/economy-works-people/investment-plan-results/investment-plan-slovakia_en"},{"title":"Other Financial Investment Activities Companies in Slovakia","url":"https://www.dnb.com/business-directory/company-information.other_financial_investment_activities.sk.html?page=13"},{"title":"Ir al contenido principal","url"
… [skrátené, 3149 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ergos investičná skupina Slovensko venture"

Links: [{"title":"annual report 2003","url":"https://www.csob.sk/documents/11005/411478/annual_report_2003.pdf"},{"title":"venture capital recruitment","url":"https://kitalent.com/sk/financial-services-and-professional-services-recruitment/venture-capital-recruitment/"},{"title":"venture capital investment team recruitment","url":"https://kitalent.com/sk/financial-services-and-professional-services-recruitment/venture-capital-recruitment/venture-capital-investment-team-recruitment/"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital?page=4"},{"title":"venture capital investment team recruitment","url":"https://kitalent.com/sl/financial-services-and-professional-services-recruitment/venture-capital-recruitment/venture-capital-investment-team-recruitment/"},{"title":"Na Slovensku chcú vybudovať infraštruktúru budúcnosti. Slováci môžu vyťažiť z prosperity nákupných centier","url":"https://www.startitup.sk/na-slovensku-chcu-vybudovat-infrastrukturu-buducnosti-slovaci-mozu-vytazit-z-prosperity-nakupnych-centier/"},{"title":"Private equity investície do spoločností v strednej a východnej Európe dosiahli najvyššiu úroveň od roku 2009","url":"https://www.podnikajte.sk/investor/private-equity-investicie-e
… [skrátené, 2680 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "365fintech 365.bank fintech investment startup"

Links: [{"title":"365 fintech","url":"https://signal.nfx.com:443/firms/365-fintech"},{"title":"365 fintech 2","url":"https://www.eu-startups.com/investor/365-fintech-2"},{"title":"365 fintech","url":"https://insights.munich-startup.de/investors/365_fintech"},{"title":"365 fintech","url":"https://insights.munich-startup.de/companies/365_fintech"},{"title":"365 fintech","url":"https://startups.one.gob.es/companies/365_fintech"},{"title":"365 fintech","url":"https://dealroom.launchvic.org/companies/365_fintech"},{"title":"365 fintech","url":"https://ecosystem.madrimasd.org/investors/365_fintech"},{"title":"ecosystem.madrimasd.org","url":"https://ecosystem.madrimasd.org/companies/365_fintech/team"},{"title":"365 fintech","url":"https://startups.one.gob.es/investors/365_fintech"},{"title":"365 fintech","url":"https://seedtable.com/investors/365-fintech"}]

The search returned several profiles of **365.fintech**, a venture capital firm. It didn't return anything specific about **365.bank**, so I can't confirm how the two are related.

**What 365.fintech is**
- It's a VC firm that backs early to scale-up technology startups. Its primary focus is on fintech, insurtech, big data and business intelligence companies.
- Its main differentiator is its link to a bank. As part of a banking group, it helps startups speed up market entry through preferred access and rollout inside a bank. Beyond financing, it lets
… [skrátené, 2689 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://365fintech.sk/ | head -80; python3 -I $F get https://www.365fintech.sk/ | head -3
```

<details><summary>Výstup nástroja</summary>

```
 Beyond Money | 365.fintech
 About us 
 Partners 
 Portfolio 
 Team 
 News 
 Contact 
 Toggle navigation
365.fintech
 About us 
 Partners 
 Portfolio 
 Team 
 News 
 Contact 
Financing is only the beginning <#BeyondMoney>If you believe in it, use it <#FastTrack>We understand banking <#Ecosystem>Seed Stage & European Focus <#Fintech>
365.fintech
We are a fintech venture investor focusing on innovative b2b or b2b2c FinTech, InsurTech and Big Data startups. We invest in European startups with global ambitions around seed stage.
FIRST THING YOU SHOULD KNOW
 About
 Us
Financing is only the beginning
We are a platform focused on providing financing and support to seed-stage fintech startups. We are continuously building a strong fintech network in Europe to leverage for our portfolio companies. We also provide hands-on operational and strategic support to our startups - from pitch deck reviews to running strategic workshops; we help our startups when and where needed.
Our Thesis:
We Get Banking
Our goal is to create an ecosystem for knowledge sharing and potential synergies between our startups, partners and the banking sector as a whole. We understand how the incumbents operate and we are fully aware of intricacies of financial services such as regulation and other challenges, which startups typically face.
Our Thesis:
Our Focus in on European Fintech
We are based in CEE but we are investing anywhere in Europe where we see outstanding nascent fintech startups - f
… [skrátené, 4549 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://365fintech.sk/ | sed -n '80,160p'
```

<details><summary>Výstup nástroja</summary>

```
Tomáš Vyšný
 Partner 
what´s new
 News
Velaris takes off with €4.7 million to roll out AI-driven customer success platform
September 20, 2022
 The fresh capital will be used to build a Machine Learning-led layer to Velaris’ platform enabling B2B tech companies to wholly understand their customers, deepen the relationship, and retain...
Ondato — The Final Piece of the KYC Compliance Puzzle
September 15, 2022
We are delighted to announce that Ondato — a tech company that streamlines KYC and AML-related processes — is joining the 365.fintech portfolio.Ondato originates in Lithuania and we are excited to...
Investing in Tymit, the next generation credit card
March 05, 2021
We are excited to announce that the UK-based startup Tymit is joining the 365.fintech portfolio. Tymit is the first credit card - "reinvented" - which puts customers in complete control of their...
InvestSuite - Investing in WealthTech as a Service
January 05, 2021
We are excited to announce that 365.fintech has participated in a late seed round of InvestSuite, an international B2B WealthTech startup. PMV, AB Accelerator and other investors have participated in...
We invested in Pynk - And Here is Why
October 14, 2020
We are excited to announce a new addition to 365.fintech portfolio - Pynk. Our investment comes as a part of a larger $2 million seed round the company has raised with crowdfunding initiatives on...
365.fintech participated in Fincompare’s series A round
March 11, 2020
365.fintech co-invests in Se
… [skrátené, 4370 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"365.fintech\" round 2024 OR 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""365.fintech" round 2024 OR 2025 OR 2026"

Links: [{"title":"Back to 365.fintech","url":"https://seedtable.com/investors/365fintech/portfolio"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/365-business-finance/financials"},{"title":"365 Finance favicon","url":"https://raising.fi/company/365financialanalyst"},{"title":"365.fintech Overview","url":"https://pitchbook.com/profiles/investor/399209-59"},{"title":"FF News — The Fintech News Network","url":"https://ffnews.com/news/365-business-finance-secures-55m-funding"},{"title":"365 business finance","url":"https://fintech.global/tag/365-business-finance/"},{"title":"kendal capital","url":"https://fintech.global/tag/kendal-capital/"},{"title":"365 fintech","url":"https://seedtable.com/investors/365-fintech"},{"title":"2023: Top five funding rounds of the year","url":"https://www.fintechfutures.com/?p=15316080"},{"title":"June 2025: Top five fintech funding rounds of the month","url":"https://www.fintechfutures.com/venture-capital-funding/june-2025-top-five-fintech-funding-rounds-of-the-month"}]

Links: [{"title":"funding.tech.eu","url":"https://funding.tech.eu/sectors/fintech/2025"},{"title":"funding.tech.eu","url":"https://funding.tech.eu/sectors/fintech/2025/q1"},{"title":"pulse of fintech global analysis.pdf.coredownload.inline","url":"https://assets.kpmg.com/content/dam/kpmgsites/uk/pdf/2026/02/pulse-of-fintech-global-analysis.pdf.coredownload.inline.pdf"},{"title":"fintech 
… [skrátené, 3835 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ctrl Alt seed funding October 2023 investors 365.fintech tokenisation", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ctrl Alt seed funding October 2023 investors 365.fintech tokenisation"

Links: [{"title":"Ctrl Alt raises €2.5m with Enterprise Ireland support","url":"https://siliconrepublic.com/start-ups/ctrl-alt-enterprise-ireland-alternative-asset"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/ctrl-alt/financials"},{"title":"Fintech to democratise alternatives raises £2.2m in seed funding","url":"https://alternativecreditinvestor.com/2023/10/24/fintech-to-democratise-alternatives-raises-e2-2m-in-seed-funding/"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/365fintech/financials"},{"title":"Back to Ctrl AltChangelog and Sources","url":"https://seedtable.com/companies/ctrl-alt/funding-rounds/pre-seed-2023-10"},{"title":"www.maddyness.com","url":"https://www.maddyness.com/uk/?p=722946"},{"title":"ctrl alt raises 2 5m","url":"https://siliconcanals.com/ctrl-alt-raises-2-5m/"},{"title":"ctrl alt funding 20231024","url":"https://www.uktech.news/fintech/ctrl-alt-funding-20231024"},{"title":"siliconcanals.com","url":"https://siliconcanals.com/?p=2526"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/company/ctrl-alt"}]

Ctrl Alt's October 2023 round was announced on 23 October 2023, and 365.fintech took part as one of several investors. Sources disagree on the size, so I've given both figures.

**Round size:** Reports cite £2.2m, which one outlet pu
… [skrátené, 3666 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.uktech.news/fintech/ctrl-alt-funding-20231024 "365" | head -4; python3 -I $F get https://siliconcanals.com/ctrl-alt-raises-2-5m/ "365" | head -3; python3 -I $F get https://alternativecreditinvestor.com/2023/10/24/fintech-to-democratise-alternatives-raises-e2-2m-in-seed-funding/ "365"|head -3
```

<details><summary>Výstup nástroja</summary>

```
The fintech’s round attracted further investment from Enterprise Ireland, Algorand Ventures, 365.fintech, Syndicate Room, Unbundled VC’s Marc Cohen, former Citymapper president Omid Ashtari, Velocity Black co-founder Alex Macdonald and others.
The round also saw participation from Angel investors and follow-on funds, including Enterprise Ireland, Algorand Ventures, 365.fintech, Syndicate Room, Marc Cohen (Unbundled VC), Omid Ashtari (ex-Google, ex-President Citymapper) and Alex Macdonald (co-founder of sequel & Velocity Black).
The seed round was led by Forward Partners and MiddleGame Ventures. They were joined by Entreprise Ireland, Algorand Foundation, 365.fintech, SyndicateRoom and a number of angel investors.
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.uktech.news/fintech/ctrl-alt-funding-20231024 | grep -n -iE "ctrl alt|365|october|2023" | head -12
```

<details><summary>Výstup nástroja</summary>

```
2: Ctrl Alt secures £2.2m for alternative asset platform
38:Ctrl Alt secures £2.2m for alternative asset platform
40: Tue 24 Oct 2023
49:Image credit: Ctrl Alt
55:Alternative asset provider Ctrl Alt has secured £2.2m in an investment round led by Forward Partners and Middle Game Ventures.
57:“A diversified portfolio should play a key role in any investment strategy and it’s not right that alternative assets, a typically robust form of investment, remain in the old world of money,” said Matt Ong, CEO and co-founder of Ctrl Alt.
58:Companies can tap into Ctrl Alt’s asset database through its API, white-label software or terminal trading platform, as well as raise asset financing.
59:Ctrl Alt’s team is spread between London and Dundalk, Ireland. It was founded by Ong, who has experience at Morgan Stanley and Credit Suisse, in 2020.
61:The fintech’s round attracted further investment from Enterprise Ireland, Algorand Ventures, 365.fintech, Syndicate Room, Unbundled VC’s Marc Cohen, former Citymapper president Omid Ashtari, Velocity Black co-founder Alex Macdonald and others.
63: Ctrl Alt
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://alternativecreditinvestor.com/2023/10/24/fintech-to-democratise-alternatives-raises-e2-2m-in-seed-funding/ | grep -n -B3 "365" | head; python3 -I $F get https://siliconcanals.com/ctrl-alt-raises-2-5m/ | grep -n -B4 "365" | head
```

<details><summary>Výstup nástroja</summary>

```
32-Fintech startup Ctrl Alt has raised £2.2m in seed funding from venture capital investors.
33-Based in London and Dundalk, Ireland, Ctrl Alt is a player in the democratisation of alternative assets, which have been traditionally dominated by institutional investors. The firm aims to ease access to alternative assets for individual investors by using fractional investing. This means that individuals can invest in shares that are represented as tokens, which are classified as security tokens by the regulator.
34-The firm was set up in 2020 by former Morgan Stanley and Credit Suisse executives Matt Ong and Jordan McMullen. It offers investments across alternatives including real estate and renewable energy. Its platform was launched at the end of 2022.
35:The seed round was led by Forward Partners and MiddleGame Ventures. They were joined by Entreprise Ireland, Algorand Foundation, 365.fintech, SyndicateRoom and a number of angel investors.
40-London-based Ctrl Alt, a B2B expert solutions provider for alternative assets, announced on Monday, October 23, that it has secured £2.2M (approximately €2.53M) in a fresh round of funding. 
41-The company specialises in helping fintechs and investment platforms expand their offerings to include fractionalised assets like property and green energy, beyond traditional stocks and bonds.
42-Investors supporting Ctrl Alt
43-The investment round was led by Forward Partners and Middlegame Ventures. 
44:The round also saw participation from Ang
… [skrátené, 1748 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.uktech.news/fintech/ctrl-alt-funding-20231024 | sed -n '59,61p' | cat -A | cut -c1-120
```

<details><summary>Výstup nástroja</summary>

```
Ctrl AltM-bM-^@M-^Ys team is spread between London and Dundalk, Ireland. It was founded by Ong, who has experience at Mo
Megha Prakash, senior investor at Forward Partners said: M-bM-^@M-^\At Forward, we see a massive opportunity to democrat
The fintechM-bM-^@M-^Ys round attracted further investment from Enterprise Ireland, Algorand Ventures, 365.fintech, Synd
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c067.json <<'EOF'
{
  "candidate_id": "c067",
  "name": "365fintech",
  "legal_name": "365.fintech, a.s.",
  "reg_no": "51301547",
  "country": "SK",
  "active_in": ["SK", "CZ", "GB", "LT", "HU", "DE"],
  "website": "https://365fintech.sk/",
  "entity_kind": {"value": "investor", "source_url": "https://365fintech.sk/", "source_date": null, "quote": "We are a fintech venture investor focusing on innovative b2b or b2b2c FinTech, InsurTech and Big Data startups."},
  "investor_type": {"value": "cvc", "source_url": "https://365fintech.sk/", "quote": "365.fintech, the new investment platform of the 365 ecosystem, is announcing the next step in putting itself on the map of financial services investors in Central and Eastern Europe."},
  "sectors": {"value": ["fintech", "insurtech", "big data"], "source_url": "https://365fintech.sk/", "source_date": null, "quote": "We are a fintech venture investor focusing on innovative b2b or b2b2c FinTech, InsurTech and Big Data startups."},
  "stages": {"value": ["seed"], "source_url": "https://365fintech.sk/", "source_date": null, "quote": "We invest in and around seed stage in Europe."},
  "funds": [],
  "investments": [
    {"company": "Ctrl Alt", "deal_date": "2023-10-23", "source_url": "https://siliconcanals.com/ctrl-alt-raises-2-5m/", "source_date": "2023-10-23", "quote": "Investors supporting Ctrl Alt The investment round was led by Forward Partners and Middlegame Ventures. The round also saw par
… [skrátené, 2846 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://365fintech.sk/
OK  investor_type https://365fintech.sk/
OK  sectors https://365fintech.sk/
OK  stages https://365fintech.sk/
OK  inv https://siliconcanals.com/ctrl-alt-raises-2-5m/
OK  inv https://365fintech.sk/
OK  inv https://365fintech.sk/
OK    research/c067.json
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; .venv/bin/python - <<'EOF'
import json
p="research/c067.json"; d=json.load(open(p))
d["investments"]=[i for i in d["investments"] if i["company"]!="Velaris"]
d["notes"]=d["notes"].replace(" The Velaris quote is a headline on 365.fintech's own news feed (does not name the investor in the sentence itself).","")
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c067.json
```

<details><summary>Výstup nástroja</summary>

```
OK    research/c067.json
```

</details>

## Claude · 2026-10-09 12:29:17 UTC

Teraz McWin.

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.mcwin.com/ | head -60; python3 -I $F get https://mcwin.com/ | head -3
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "McWin Capital Partners invests 2025 restaurant food tech fund", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "McWin Capital Partners invests 2025 restaurant food tech fund"

Links: [{"title":"Press Release","url":"https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million"},{"title":"McWin and TriSpan Announce Co Control Majority Investment in Flat Iron","url":"https://www.trispanllp.com/trispan-core/core-content/wp-content/core-media/2025/09/McWin-and-TriSpan-Announce-Co-Control-Majority-Investment-in-Flat-Iron.pdf"},{"title":"Press Release","url":"https://goodwinlaw.com/en/news-and-events/news/2025/01/announcements-technology-mcwin-elephantskin-strategic-partnership"},{"title":"McWin Food Tech Fund I Overview","url":"https://pitchbook.com/profiles/fund/21681-01F"},{"title":"Do you have a story to share with Catering Today readers?","url":"https://www.cateringtoday.co.uk/tag/mcwin-capital-partners"},{"title":"Private equity firm to help accelerate Spanish firm’s expansion into QSRs","url":"https://www.thecaterer.com/products--equipment/mcwin-pours-4m-into-coffee-brand"},{"title":"McWin übernimmt Mehrheit bei Sticks'n'Sushi","url":"https://www.tageskarte.io/gastronomie/detail/mcwin-uebernimmt-mehrheit-bei-sticksnsushi.html"},{"title":"das big money game","url":"https://www.meininger.de/gastronomie/management/das-big-money-game"},{"title":"McWin launches €250m food tech fund","url":"https://agriinvestor.com/mcwin-launches-e250m-food-tech-fund"}]

McWin Capital Partn
… [skrátené, 3301 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million "McWin|2025|headquartered|Luxembourg" | head -12; echo; python3 -I $F get https://agriinvestor.com/mcwin-launches-e250m-food-tech-fund "McWin|Luxembourg|headquart|ticket|€" | head -12
```

<details><summary>Výstup nástroja</summary>

```
Goodwin Advises McWin Capital Partners in Ecorobotix’s $105 Million Series D | News & Events | Goodwin
October 14, 2025
Goodwin Advises McWin Capital Partners in Ecorobotix’s $105 Million Series D
The London and Cambridge Technology team advised McWin Capital Partners, via its McWin Food Tech Fund, in its participation in the $105 million Series D round of Ecorobotix, the global leader in AI-powered Ultra-High Precision (UHP) spraying. The Series D round also included Highland Europe with ECBF as new investors along with McWin.
McWin Capital Partners is a specialist private equity and venture capital firm, dedicated to the food ecosystem. With deep industry expertise across three business segments; Food Tech, Foodservice and Restaurants, McWin’s purpose is to lead the food industry through positive change and create value on behalf of investors and portfolio companies of the McWin Funds by leveraging its scale, network and experience to deliver outstanding returns.

 McWin launches €250m food tech fund
Home News & Analysis McWin launches €250m food tech fund
McWin launches €250m food tech fund
The firm has also raised €260m for its debut Food Ecosystem Fund, which it expects to close on €300m in Q3.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"McWin\" headquartered Luxembourg private equity food founded Henry McGovern", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.trispanllp.com/trispan-core/core-content/wp-content/core-media/2025/09/McWin-and-TriSpan-Announce-Co-Control-Majority-Investment-in-Flat-Iron.pdf | head -c 300; echo; python3 -I $F get https://www.thecaterer.com/products--equipment/mcwin-pours-4m-into-coffee-brand "McWin|Incapto|202" | head -6
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""McWin" headquartered Luxembourg private equity food founded Henry McGovern"

Links: [{"title":"Renzenbrink & Partner berät AmRest-Gründer Henry McGovern beim Einstieg in dean&david","url":"https://majunke.com/renzenbrink-partner-beraet-amrest-gruender-henry-mcgovern-beim-einstieg-in-deandavid"},{"title":"28 March 2024","url":"https://www.taylorwessing.com/en/insights-and-events/news/media-centre/press-releases/2024/03/subway"},{"title":"28. März 2024","url":"https://www.taylorwessing.com/de/insights-and-events/news/media-centre/press-releases/2024/03/subway"},{"title":"mcwin acquires majority stake losteria","url":"https://vegconomist.com/company-news/mcwin-acquires-majority-stake-losteria/"},{"title":"McWin Capital reportedly in talks to acquire premi","url":"https://worldcoffeeportal.com/Latest/News/2024/December/McWin-Capital-reportedly-in-talks-to-acquire-premi"},{"title":"dfvcg-events.de","url":"https://dfvcg-events.de/european-foodservice-summit/wp-json/wp/v2/posts/3286"},{"title":"bclp advises mcwin on acquisition of majority stake in losteria","url":"https://bclplaw.com/en-US/events-insights-news/bclp-advises-mcwin-on-acquisition-of-majority-stake-in-losteria.html"},{"title":"das big money game","url":"https://www.meininger.de/gastronomie/management/das-big-money-game"},{"title":"www.verdictfoodservice.com","url":"https://www.verdictfoodservice.com/?p=47512"}]

I couldn't confirm that McWin is headquartered in Luxembourg. The sources po
… [skrátené, 3068 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
%PDF-1.7
%����
1 0 obj
<>/Metadata 169 0 R/ViewerPreferences 170 0 R>>
endobj
2 0 obj
<>
endobj
3 0 obj
<>/ExtGState<>/XObject<>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI] >>/MediaBox[ 0 0 595.32 841.92] /Contents 4 0 R/Group<>/Tabs/S/StructParents 0>>
endobj
4 0 obj
<>
stream
x�Exception ignored while flushing sys.stdout:
BrokenPipeError: [Errno 32] Broken pipe

McWin pours £4m into coffee brand - Products & equipment
McWin pours £4m into coffee brand
Supplier24 Apr 2026by Clare Nicholls
McWin Capital Partners has invested €5m (£4.3m) in coffee and associated equipment supplier Incapto.
McWin’s investment was via its Tech Fund I as part of Incapto’s €10m (£8.7m) Series B funding round.
The move is part of the private equity firm’s strategic commitment to supporting innovative and high-impact food technology companies. McWin believes Incapto has a proven business model, recurring revenue streams and a roadmap to sustained profitability, and therefore represents a strategic addition to its portfolio.
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.mcwin.com/", "prompt": "Where is McWin headquartered / which offices? What does it say about itself (verbatim sentences)? Any mention of Slovakia?"}
```

<details><summary>Výstup nástroja</summary>

```
error:10000438:SSL routines:OPENSSL_internal:TLSV1_ALERT_INTERNAL_ERROR
```

</details>

**Nástroj `Bash`**

```bash
curl -sIL --max-time 20 http://www.mcwin.com/ | head; curl -sIL --max-time 20 https://mcwin.eu/ | head -3; curl -sIL --max-time 20 https://www.mcwincapital.com/ | head -3
```

<details><summary>Výstup nástroja</summary>

```
HTTP/1.1 301 Moved Permanently
Content-Type: text/html
Connection: keep-alive
X-WS-Origin: available
X-WS-RateLimit-Limit: 1000
X-WS-RateLimit-Remaining: 999
Date: Fri, 09 Oct 2026 12:29:59 GMT
Server: Apache
Cache-Control: max-age=0
Location: https://mcwin-com.blogspot.com
HTTP/2 405 
content-type: text/html
date: Fri, 09 Oct 2026 12:30:00 GMT
HTTP/1.1 200 OK
Content-Type: text/html
Date: Fri, 09 Oct 2026 12:30:01 GMT
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.mcwincapital.com/ | head -60
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
curl -sL --max-time 20 -A "Mozilla/5.0" https://www.mcwincapital.com/ | head -c 1500
```

<details><summary>Výstup nástroja</summary>

```
<!DOCTYPE html><html><head><script>window.onload=function(){window.location.href="/lander"}</script></head></html>
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://forbes.cz/mcwin-kupuje-podil-v-restauracnim-retezci-losteria-investice-vysla-na-400-milionu-eur/ "McWin" | head -8; python3 -I $F get https://www.taylorwessing.com/en/insights-and-events/news/media-centre/press-releases/2024/03/subway "McWin" | head -6
```

<details><summary>Výstup nástroja</summary>

```
 McWin kupuje podíl v restauračním řetězci L’Osteria. Investice jej ohodnotila na 400 milionů eur | Forbes
McWin kupuje podíl v restauračním řetězci L’Osteria. Investice jej ohodnotila na 400 milionů eur
Investiční společnost McWin sídlící v České republice koupila většinový podíl v německé firmě L’Osteria, která provozuje stejnojmenný řetězec restaurací s italskou kuchyní. Transakce řetězec ohodnocuje zhruba na 400 milionů eur.
Řetězec L’Osteria vznikl v roce 1999. V současnosti provozuje 157 restaurací v osmi evropských zemích včetně České republiky. Převzetí většinového podílu firmou McWin je první změnou ve vlastnické struktuře podniku od jeho založení.
„Věříme, že takovéto skvělé podniky dosahují v neklidných dobách nadstandardních výsledků,“ uvedl Henry McGovern ze společnosti McWin s odkazem na současné obtížné ekonomické podmínky.
Společnost McWin provozuje kanceláře v Británii, Španělsku a Polsku. Investuje do potravinářských služeb a technologií a vlastní podíly ve více než 1500 restauracích po celé Evropě.
 Taylor Wessing advises Subway® on its partnership with McWin for the expansion of the Subway® franchise network in France, Belgium, Luxembourg and the Czech Republic
Taylor Wessing advises Subway® on its partnership with McWin for the expansion of the Subway® franchise network in France, Belgium, Luxembourg and the Czech Republic
Taylor Wessing advises Subway® on its partnership with McWin for the expansion of the Subway® franchise network in France, Belgium, Lu
… [skrátené, 2284 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c068.json <<'EOF'
{
  "candidate_id": "c068",
  "name": "McWin",
  "legal_name": "McWin Capital Partners",
  "reg_no": null,
  "country": "CZ",
  "active_in": ["DE", "GB", "ES", "FR", "CZ", "CH"],
  "website": null,
  "entity_kind": {"value": "investor", "source_url": "https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million", "source_date": "2025-10-14", "quote": "McWin Capital Partners is a specialist private equity and venture capital firm, dedicated to the food ecosystem."},
  "investor_type": {"value": "pe", "source_url": "https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million", "quote": "McWin Capital Partners is a specialist private equity and venture capital firm, dedicated to the food ecosystem."},
  "sectors": {"value": ["foodtech", "foodservice", "restaurants"], "source_url": "https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million", "source_date": "2025-10-14", "quote": "With deep industry expertise across three business segments; Food Tech, Foodservice and Restaurants"},
  "funds": ["McWin Food Tech Fund I", "McWin Restaurant Fund", "McWin Foodservice Fund"],
  "investments": [
    {"company": "Incapto", "deal_date": "2026-04-24", "source_url": "h
… [skrátené, 2809 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million
OK  investor_type https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million
OK  sectors https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million
OK  inv https://www.thecaterer.com/products--equipment/mcwin-pours-4m-into-coffee-brand
OK  inv https://www.goodwinlaw.com/en/news-and-events/news/2025/10/announcements-technology-goodwin-advises-mcwin-capital-partners-in-ecorobotix-105-million
OK    research/c068.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ergos venture capital investor Bratislava", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ergos venture capital investor Bratislava"

Links: [{"title":"venture capital firms bratislava","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava.md"},{"title":"Blog9 Trailblazing Venture Capital Firms Powering Bratislava's Startup Surge","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava"},{"title":"JRC119788 020","url":"https://publications.jrc.ec.europa.eu/repository/bitstream/JRC119788/JRC119788_020.pdf"},{"title":"pefim.sggw.edu.pl","url":"https://pefim.sggw.edu.pl/article/download/1500/1466/1552"},{"title":"Venture to Future Fund Overview","url":"https://pitchbook.com/profiles/investor/461930-23"},{"title":"Zero One Hundred","url":"https://spacetech.dealroom.co/companies/zero_one_hundred"},{"title":"Venture Capital","url":"https://altss.com/profile/vision-ventures-slovakia"},{"title":"Venture Capital","url":"https://altss.com/profile/slovak-american-enterprise-fund"},{"title":"365 fintech","url":"https://app.dealroom.co/investors/365_fintech"}]

I didn't find any results mentioning an investor called Ergos in Bratislava. The search returned general Bratislava venture capital pages, so I can't confirm whether Ergos exists or what it invests in.

Some Bratislava-based investors that did come up:

- **Venture to Future Fund (VFF):** Founded in 2020, Venture to Future is a venture capital firm based in Bratislava, Slovakia. The firm seeks to invest in technology companies operating in business-to-busine
… [skrátené, 2880 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get "https://tracxn.com/d/investor-lists/venture-capital-funds-in-slovakia/__DvmbYfeSMp1bcVhFxyHfn9j2EYVdLnk4ZwIEYR1zzuM" "ergos|mcwin|365" | head; for u in https://ergos.sk/ https://www.ergos.cz/ https://ergos.com/; do echo "## $u"; python3 -I $F get $u | head -25; done
```

<details><summary>Výstup nástroja</summary>

```
McWin
Ergos
365fintech
Slovakia hosts 34 Venture Capital Funds, including McWin, Ergos, Venture to Future Fund, Zero Gravity Capital, and 365fintech. Collectively they have invested more than $60B across 3,713 rounds in over 520 companies. In the past five years, these funds have participated in 92 seed-stage rounds ($245M), 106 early-stage rounds ($2.21B), and 89 late-stage rounds ($10.7B). The most active sectors are Enterprise Software, SaaS, & Deep Tech, while some of the most recently funded companies include Impossible Objects, Higgsfield and Standard.
McWin, Ergos & Venture to Future Fund
1. McWin
Key facts about McWin
2. Ergos
Key facts about Ergos
5. 365fintech
## https://ergos.sk/

## https://www.ergos.cz/

## https://ergos.com/

Outsourced IT Services: Support, Consulting, Security
 713-621-9220
 Facebook
 X
Linkedin 
 Facebook
 X
Linkedin
About
IT Services
Managed IT Services
IT Project Management Services
Data Recovery Service
IT Strategy Consulting Services
Cybersecurity Services
Cybersecurity Consulting
Managed Cybersecurity
Threat Protection & Prevention
Security Testing & Assessment
Incident Response & Recovery
Cloud Services
Cloud Strategy and Planning
Cloud Migration Services
Managed Cloud Services
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get "https://tracxn.com/d/investor-lists/venture-capital-funds-in-slovakia/__DvmbYfeSMp1bcVhFxyHfn9j2EYVdLnk4ZwIEYR1zzuM" | grep -A15 "2. Ergos"
```

<details><summary>Výstup nástroja</summary>

```
2. Ergos
Key facts about Ergos
Founded Year: 2022
Portfolio count: 88
Sectors of Investment: Enterprise Applications, High Tech & 27 more
Locations of Investment: United States, Russia & 13 more
3. Venture to Future Fund
Key facts about Venture to Future Fund
Founded Year: 2020
Portfolio count: 17
Sectors of Investment: Enterprise Applications, High Tech & 14 more
Stages of Investment: Seed, Series A, Series B
Locations of Investment: Slovakia, Czech Republic & 3 more
4. Zero Gravity Capital
Key facts about Zero Gravity Capital
Founded Year: 2019
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Ergos\" fund invests Higgsfield OR SPV OR \"Ergos Capital\" startups 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Ergos" fund invests Higgsfield OR SPV OR "Ergos Capital" startups 2025"

Links: [{"title":"AI Video Startup Higgsfield Hits the Highs With $1.3B Valuation | eWEEK | eWeek","url":"https://www.eweek.com/fr/news/ai-video-startup-higgsfield-valuation/"},{"title":"AI Video Startup Higgsfield Hits the Highs With $1.3B Valuation | eWEEK | eWeek","url":"https://www.eweek.com/de/news/ai-video-startup-higgsfield-valuation/"},{"title":"FundraiseJul 1, 2026","url":"https://dealroom.co/news/136662-ai-video-startup-higgsfield-eyes-500m-raise-at-5b-valuation/"},{"title":"SG's 1982 Ventures joins $400m round in US AI startup Higgsfield","url":"https://www.dealstreetasia.com/?p=493382"},{"title":"Higgsfield recauda US$400M y factura US$700M anuales con IA","url":"https://ecosistemastartup.com/?p=99475"},{"title":"Higgsfield recauda US$400M y factura US$700M anuales con IA","url":"https://ecosistemastartup.com/higgsfield-recauda-us400m-y-factura-us700m-anuales-con-ia/"},{"title":"Higgsfield reportedly in talks to raise at $5B valuation","url":"https://aiweekly.co/alerts/higgsfield-reportedly-in-talks-to-raise-at-5b-valuation"},{"title":"Мурат Абдрахманов инвестировал в Higgsfield $6,3 млн","url":"https://kapital.kz/finance/151778/murat-abdrahmanov-investiroval-v-higgsfield-dollar63-mln.html"},{"title":"www.intelcapital.com","url":"https://www.intelcapital.com/?p=12435"}]

I couldn't find any reference to an "Ergos" fund, "Ergos Capital," or an Ergos SPV investin
… [skrátené, 2818 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ergos investment company Slovakia founded 2022 portfolio venture \"Ergos\"", "mode": "extended"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ergos investment company Slovakia founded 2022 portfolio venture "Ergos""

Links: [{"title":"Ergos (Slovakia) investment portfolio","url":"https://pitchbook.com/profiles/investor/498218-14"},{"title":"Generali acquires Ergo’s business in Hungary, Slovakia - Business Insurance","url":"https://www.businessinsurance.com/Generali-acquires-Ergos-business-in-Hungary,-Slovakia/"},{"title":"List of 55 Investment Tech Startups in Slovakia & Market Trends (May 2026) - Tracxn","url":"https://tracxn.com/d/explore/investment-tech-startups-in-slovakia/__kguVHM15CP4lVzmxLssre0lGWQjeoWCk0TFlsNIA25U#top-companies"},{"title":"Ergos - 2025 Investor Profile & Portfolio - Tracxn","url":"https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I"},{"title":"List of 160 Vertical SaaS Startups in Slovakia & Market Trends (Aug 2026) - Tracxn","url":"https://tracxn.com/d/explore/vertical-saas-startups-in-slovakia/__3EBWkt7S8RCVphlkgJCUpnk9B9YDb7TGY6ZBBKDVnOQ"},{"title":"Ergos Business Solutions Private Limited - Investment 01 - British International Investment","url":"https://www.bii.co.uk/en/our-impact/investment/ergos-business-solutions-private-limited-investment-01/"},{"title":"Ergos - Top portfolio companies (Dec, 2024) - Tracxn","url":"https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I/portfolio"},{"title":"Ergo Group","url":"https://en.wikipedia.org/wiki/Ergo_Group"},{"title":"Ergo Capital investme
… [skrátené, 3592 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ergos Košice investícia Truecare24 OR DigiDoe OR Amadei OR E-gree", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ergos Košice investícia Truecare24 OR DigiDoe OR Amadei OR E-gree"

Links: [{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/inovacne-centrum-kosickeho-kraja-zi/839004-clanok.html"},{"title":"27. 05. 2026","url":"https://www.economy.gov.sk/en/press/new-investments-worth-tens-of-millions-of-euros-in-the-kosice-region-to-create-hundreds-of-new-jobs-and-high-value-manufacturing"},{"title":"Američania investujú milióny v Košiciach, prijmú stovky ľudí","url":"https://sita.sk/americania-investuju-miliony-v-kosiciach-prijmu-stovky-ludi/"},{"title":"Falck Rehabilitácia Košice: Komplexný prehľad a recenzie","url":"https://ddadsstornala.sk/aktuality/falck-rehabilitacia-kosice/"},{"title":"sario references sk 2023 06 21","url":"https://www.sario.sk/sites/default/files/sario-references-sk-2023-06-21.pdf"},{"title":"sario references sk 2024 05 10","url":"https://sario.sk/sites/default/files/sario-references-sk-2024-05-10.pdf"},{"title":"IT mekka Slovenska Košice zlákaly dalšího investora, americkou GlobalLogic","url":"https://www.e15.cz/magazin/it-mekka-slovenska-kosice-zlakaly-dalsiho-investora-americkou-globallogic-1096653"},{"title":"Slovakia not attractive for high value added investors","url":"https://www.symsite.sk/blog/page/48"},{"title":"sario references eng 2024 05 10","url":"https://sario.sk/sites/default/files/sario-references-eng-2024-05-10.pdf"}]

I couldn't find any search results about
… [skrátené, 2352 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get "https://finstat.sk/databaza-firiem-organizacii?query=ergos" | grep -iE "ergos" | head -20
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Ergos\" s.r.o. Košice Havanská", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Ergos" s.r.o. Košice Havanská"

Links: [{"title":"Ergo s r o en 13247505","url":"https://www.emis.cn/php/company-profile/SK/Ergo_s_r_o_en_13247505.html"},{"title":"Sídlo firmy","url":"https://www.jenprace.cz/firmy/egos-s-r-o"},{"title":"REQUEST A DEMO","url":"https://www.emis.cn/php/company-profile/SK/Ergo_S_R_O_en_13247505.html"},{"title":"obchodny register","url":"https://finstat.sk/53574907/obchodny_register"},{"title":"ERGO Working Space s.r.o., IČO: 29010683, sídlo: Praha","url":"https://www.finmag.cz/obchodni-rejstrik/29010683-ergo-working-space-s-r-o"},{"title":"REQUEST A DEMO","url":"https://www.emis.cn/php/company-profile/CZ/Ergo_Cz_SRO_en_4876117.html"},{"title":"www.economy.gov.sk","url":"https://www.economy.gov.sk/uploads/files/EbzVCN3X.pdf"},{"title":"www.economy.gov.sk","url":"https://www.economy.gov.sk/uploads/files/T5esYXG9.pdf"},{"title":"ergas s r o 62305026","url":"https://www.podnikatel.cz/rejstrik/ergas-s-r-o-62305026/"}]

I couldn't find any company called "Ergos" s.r.o. with a seat on Havanská street in Košice in the search results. The search returned several similarly named firms, but none match both the name and the address.

- **Ergo, s. r. o.** is based in Pezinok, not Košice. It operates in the Other Business Support Services sector. Its registered address is on Moyzesova street.
- **ERIGOM SK s. r. o.** is a Bratislava company. Its only Košice connection is a former seat on Bauerova street, which applied until May 
… [skrátené, 2250 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get "https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I" | grep -iE "ergos" | head -15
```

<details><summary>Výstup nástroja</summary>

```
 Ergos - 2026 Investor Profile & Portfolio - Tracxn 
Venture Capital>Ergos
Ergos - Investor Profile and Portfolio
About Ergos Ergos is a venture capital firm founded in 2022. It is primarily based out of Kosice, Slovakia. It primarily invests in United States based startups. Its investments are spread across a wide range of sectors from Enterprise Applications to High Tech and Consumer. Overall, Ergos portfolio has seen 4 unicorns, 3 IPOs and 8 acquisitions including key companies like Facebook, Kraken and Damon.
View Ergos' full profile
Ergos' List of Top InvestmentsErgos has a portfolio of 88 companies, including 4 unicorns. Their most notable investments include Facebook and Kraken.Their portfolio spans across United States, Russia, Israel and 12 more locations. They have invested in Enterprise Applications, High Tech, Consumer and 26 other sectors. Here is the list of top investments by Ergos:
Unicorns in Ergos' PortfolioErgos has 4 unicorns in its portfolio - StoreDot, OpenWeb, Kraken and others. The most recent unicorn in their portfolio is StoreDot. It became a unicorn in 2022, 4 years before Ergos first invested in it.
Here is a list of unicorns in Ergos' portfolio:
View more details about unicorns in Ergos' portfolio
IPOs and Publicly Listed companies in Ergos' Portfolio3 of Ergos' portfolio companies have become public. Damon got listed on the National Association of Securities Dealers Automated Quotations (NASDAQ), in Nov 2024 and Momentus Space got listed on the N
… [skrátené, 1977 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c069.json <<'EOF'
{
  "candidate_id": "c069",
  "name": "Ergos",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["US"],
  "website": null,
  "entity_kind": {"value": "investor", "source_url": "https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I", "source_date": null, "quote": "Ergos is a venture capital firm founded in 2022. It is primarily based out of Kosice, Slovakia. It primarily invests in United States based startups."},
  "investor_type": {"value": "vc", "source_url": "https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I", "quote": "Ergos is a venture capital firm founded in 2022. It is primarily based out of Kosice, Slovakia. It primarily invests in United States based startups."},
  "funds": [],
  "investments": [],
  "duplicate_of": null,
  "notes": "Only aggregator evidence (Tracxn; PitchBook not used) — no website, press release, news article or register entry found. Tracxn's portfolio (88 companies incl. Facebook, Kraken, StoreDot) looks implausible for a Košice firm founded in 2022 and may be secondary/SPV positions or a name mix-up. Treat as no_evidence until verified.",
  "researched_at": "2026-10-09"
}
EOF
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F check research/c069.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c069.json
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I
OK  investor_type https://tracxn.com/d/venture-capital/ergos/__WGrR1Qun0G2FVNY3OFYkhRzeqIYHTkx5Q8BaVywuX9I
OK    research/c069.json
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.vestbee.com/insights/articles/cequence-secures-2-m | grep -iE "jet|look ai|cequence|202" | head -12; ls /home/filip/investor-db/research
```

<details><summary>Výstup nástroja</summary>

```
Slovak startup Cequence secures €2M led by Czech Jet Ventures | Vestbee
June 13, 2025·2 min read
Slovak startup Cequence secures €2M led by Czech Jet Ventures
Bratislava-based startup Cequence, specializing in automating contract workflows, has raised €2 million in seed funding to accelerate its growth, bringing its total funding to €3 million, as Vestbee was told.
Founded in 2018 by Peter Horný, Martin Ragan, Rasťo Kovaľ, Peter Banda, and Martin Rázus, Cequence develops an AI-driven contract management platform that automates the entire contract lifecycle.
Cequence’s platform serves over 20 enterprise clients across various industries. It integrates seamlessly with existing tools, especially Microsoft ecosystems, and includes a real-time collaborative editor along with dynamic playbooks to ensure contracts are both auditable and compliant. 
The funding round was led by Jet Ventures, a newly launched €50 million fund under the Czech investment firm Jet Investment. Jet Ventures focuses on supporting startups in the industrial B2B sector across Czechia, Germany, Austria, Slovakia, and Poland, with initial investments of up to €2 million.
“Cequence is fundamentally redefining how companies manage contracts. With a world-class product team, fast deployment, and strong scalability, Cequence is well positioned to become a market leader. We’re excited to support their next phase of growth," claims Kamil Levinský, Managing Director at Jet Ventures.
Cequence plans to use the €2 millio
… [skrátené, 2796 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db/research; cat c007.json; grep -l -iE "jet ventures|look ai|presto|fil rouge|gi21|JIC" *.json
```

<details><summary>Výstup nástroja</summary>

```
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
  "ticket_max": {"amount": 50000000, "currency": "EUR", "source_url": "https://www.slovca.sk/sk/riadni-clenovia/jet-investment.html", "source_
… [skrátené, 3807 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db/research; grep -o -iE '"name": "[^"]*"|.{60}(jet ventures|look ai|presto|fil rouge|gi21|JIC).{60}' c006.json c045.json
```

<details><summary>Výstup nástroja</summary>

```
c045.json:"name": "BHS private equity fund"
c045.json:ments hledá stabilní, zdravé podniky se silným cash flow, jejichž odkupy lze financovat kombinací vlastního kapitálu a bank
c006.json:"name": "Genesis Capital"
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c070.json <<'EOF'
{
  "candidate_id": "c070",
  "name": "Jet Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "DE", "AT", "SK", "PL"],
  "website": "https://www.jetinvestment.cz/en",
  "entity_kind": {"value": "investor", "source_url": "https://www.vestbee.com/insights/articles/cequence-secures-2-m", "source_date": "2025-06-13", "quote": "The funding round was led by Jet Ventures, a newly launched €50 million fund under the Czech investment firm Jet Investment."},
  "investor_type": {"value": "vc", "source_url": "https://www.vestbee.com/insights/articles/cequence-secures-2-m", "quote": "The funding round was led by Jet Ventures, a newly launched €50 million fund under the Czech investment firm Jet Investment."},
  "sectors": {"value": ["industrial b2b"], "source_url": "https://www.vestbee.com/insights/articles/cequence-secures-2-m", "source_date": "2025-06-13", "quote": "Jet Ventures focuses on supporting startups in the industrial B2B sector across Czechia, Germany, Austria, Slovakia, and Poland, with initial investments of up to €2 million."},
  "ticket_max": {"amount": 2000000, "currency": "EUR", "source_url": "https://www.vestbee.com/insights/articles/cequence-secures-2-m", "source_date": "2025-06-13", "quote": "Jet Ventures focuses on supporting startups in the industrial B2B sector across Czechia, Germany, Austria, Slovakia, and Poland, with initial investments of up to €2 million."},

… [skrátené, 2623 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK  investor_type https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK  sectors https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK  ticket_max https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK  aum https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK  inv https://www.vestbee.com/insights/articles/cequence-secures-2-m
OK    research/c070.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Look AI Ventures\" fund", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Look AI Ventures" fund"

Links: [{"title":"emerging europe","url":"https://emerging-europe.com/?p=79487"},{"title":"Czech Republic has a new investment fund for AI start-ups","url":"https://tech.eu/2023/04/13/czech-republic-has-a-new-investment-fund-for-ai-start-ups"},{"title":"czech ai startup incubator announces a new e20m fund look ai ventures","url":"https://en.ain.ua/2023/04/12/czech-ai-startup-incubator-announces-a-new-e20m-fund-look-ai-ventures"},{"title":"from czechia a new fund for cees ai start ups","url":"https://emerging-europe.com/from-czechia-a-new-fund-for-cees-ai-start-ups/"},{"title":"look ai ventures","url":"https://vestbee.com/vc-list/look-ai-ventures"},{"title":"Look AI Ventures Research","url":"https://f4.fund/firms/look-ai-ventures"},{"title":"look ai ventures","url":"https://superscout.co/investor/look-ai-ventures"},{"title":"streaklinks.com","url":"https://streaklinks.com/Bn7v1V9uLp52oz_ZlwehkgOS/https%3A%2F%2Flookai.vc%2F"},{"title":"lookai vc","url":"https://superscout.co/investor/lookai-vc"}]

Look AI Ventures (LAIV) is a Prague-based venture fund that invests only in AI startups, mostly early-stage companies in Central and Eastern Europe.

**Background and launch (2023):** The fund was set up on top of the AI Startup Incubator (AISI), and it launched with a target of €20 million. The fund will support early-stage AI-driven companies with around €250,000 in funding and mentorship. It focuses on pre-seed and seed-stage
… [skrátené, 3488 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://lookai.vc/ | head -70; python3 -I $F get https://tech.eu/2023/04/13/czech-republic-has-a-new-investment-fund-for-ai-start-ups "Look AI|€|seed" | head
```

<details><summary>Výstup nástroja</summary>

```
Look AI Ventures | Investing in early-stage AI startups
About us
Mission
Our story
Team
How we Invest
Investment Criteria
What Startups get
Investment Process
Portfolio
References
News
Contact
I'm Investor
I'm Startup
We invest in globally
disruptive early-stage
AI Startups
Look AI Ventures fund (LAIV) is the first investment fund in the Czech Republic that focuses exclusively on AI startups worldwide and provides new investors with the opportunity to seek the high returns that AI businesses promise.
Our Mission
The AI Megatrend
Rising demand and investment in AI development made the global Artificial Intelligence market one of the fastest-growing sectors in the tech industry. According to PwC, the combination of increased productivity and consumption side effects of AI could contribute up to $15.7 trillion to the global economy by 2030.
Our goal is to nurture the AI startup ecosystem by investing in a new portfolio of promising early-stage AI startups.
Opportunities
Look AI Ventures fund is a domain-specific fund; we target opportunities across a broad set of core AI areas and AI-enabled businesses. Acknowledging the market megatrend, we aim to take advantage of the expected earnings growth rate opportunities AI offers.
Growth
Everything from our evaluation process to our partner ecosystem is built to identify and grow the most disruptive startups so that we can maximize the chances of generating superior, long-term investment returns for our Limited Partners.
Integrity
We a
… [skrátené, 6044 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://lookai.vc/ | sed -n '70,200p' | grep -v "^\s*$" | head -90; curl -sL https://lookai.vc/ | grep -oE 'href="[^"]*(news|blog)[^"]*"' | sort -u | head
```

<details><summary>Výstup nástroja</summary>

```
Managing Partner
Angelo Burgarello
Partner & Chief Investment Officer
Martin Dostál, Ph.D.
Partner & Chief Science Officer
Veronika Argust
Senior Principal
Taťána Lysková
Principal
Eva Slonkova
Marketing Manager
Kate Inozemtseva
Head of Scouting
Andrej Tomčík
Senior Associate
Our Portfolio
Sodex Innovations automates construction site surveying by mounting scanning systems on heavy machinery to map terrain in real time, with centimeter-level precision. A cloud platform turns this data into 3D models and digital twins, tracking material movement and progress against the project plan — helping teams cut manual surveying, avoid delays, and manage projects more effectively.
Learn more
Checkstep provides an AI content moderation platform for Trust and Safety that helps online platforms detect, moderate, and manage harmful content at scale. It combines automated moderation, policy enforcement, and human review to support safer digital communities and regulatory compliance. Serving industries such as gaming, marketplaces, streaming, and social media, Checkstep enables faster, more accurate, and scalable content moderation operations.
Learn more
Brickwise AI is a 24/7 AI-powered property manager for landlords and estate agents, handling tenant communications, maintenance coordination, leasing, and contract management 24/7. By handling calls and routine requests end-to-end, Brickwise reduces operational workload, improves response times, and helps property teams scale, allowing owners
… [skrátené, 12093 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://lookai.vc/news/ | grep -v "^\s*$" | sed -n '15,70p'; curl -sL https://lookai.vc/news/ | grep -oE 'href="https://lookai.vc/[^"]{25,}"' | sort -u | head -20
```

<details><summary>Výstup nástroja</summary>

```
I'm Startup
News
September 22, 2026
NewsLook AI Ventures Backs Embodied AI to Bring Physical AI to Manufacturing
July 23, 2026
NewsLook AI Ventures Invests in Sodex Innovations’ €4M Round to Scale AI-Powered Construction Site Surveying
July 13, 2026
PressSodex Innovations secures €4M to bring real-time intelligence to construction sites
June 30, 2026
NewsLook AI Ventures Joins Lucida AI’s $7M Seed Round to Power the Future of Spoken Communication
June 30, 2026
PressLucida AI closes $7M seed round for speech-to-speech AI
May 29, 2026
PressCheckstep nets £3 million to scale AI safety platform
May 29, 2026
NewsLook AI Ventures Backs Checkstep in £3M Round to Scale AI Trust & Safety Infrastructure
May 11, 2026
PressMeet AlterEcho: The winner of the EU-Startups Summit 2026 Pitch Competition!
April 16, 2026
PressInntelo AI Wins Innovative Guest Experience of the Year at The Caterer Supplier Awards 2026
March 18, 2026
NewsLook AI Ventures Backs Surveily to Scale Edge AI for Industrial Safety
December 19, 2025
NewsNew Investment: Digicust Secures €2.3M to Automate Customs Processes
December 2, 2025
NewsPortfolio News: Inntelo AI to Power Guest Experience at the World’s Tallest Hotel
November 28, 2025
PressČeská stopa v dominantě Dubaje. Nejvyšší hotel světa vás obslouží i v češtině díky zdejšímu fondu
October 15, 2025
PressThe First Group Hospitality and Inntelo AI partner to deploy AI-native guest experience and operations platform across hotel portfolio
July 15, 2025
NewsNew Invest
… [skrátené, 4691 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for s in look-ai-ventures-backs-embodied-ai-robots-manufacturing look-ai-ventures-sodex-innovations-4m-ai-construction-site-surveying new-investment-cequence-secures-e2m-to-expand-ai-powered-contract-automation-platform; do echo "## $s"; python3 -I $F get https://lookai.vc/$s/ | grep -iE "Look AI Ventures|LAIV" | head -4; done
```

<details><summary>Výstup nástroja</summary>

```
## look-ai-ventures-backs-embodied-ai-robots-manufacturing
Embodied AI Raises Funding for Physical AI Robots | Look AI Ventures
Look AI Ventures Backs Embodied AI to Bring Physical AI to Manufacturing
Look AI Ventures backs Embodied AI, a physical AI startup building robots that learn directly on the production line. Already deploying with some of the largest manufacturers in Europe, Embodied AI will use the funding to bring its technology to more customers, scale robot production, and grow its teams in Lausanne and Rome.
Look AI Ventures has backed Embodied AI, a Lausanne-based robotics startup building robots that learn new tasks directly on factory production lines. The round was led by Faber VC, with participation from Techshop Capital, Kickfund, Plug and Play San Francisco, Excellis, and Vento.
## look-ai-ventures-sodex-innovations-4m-ai-construction-site-surveying
Sodex Innovations Raises €4M for AI Construction Surveying | Look AI Ventures
Look AI Ventures Invests in Sodex Innovations’ €4M Round to Scale AI-Powered Construction Site Surveying
Look AI Ventures has joined Sodex Innovations' €4M funding round, led by Capmont Technology, to scale its AI-powered construction site surveying platform globally. With more than 100 customers already using the technology daily across the US, Australia, and Europe, Sodex is now accelerating its international expansion and platform development.
Sodex Innovations, an Austrian construction tech startup developing AI-powered surveying
… [skrátené, 3306 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c071.json <<'EOF'
{
  "candidate_id": "c071",
  "name": "Look AI Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK", "AT", "CH", "GB"],
  "website": "https://lookai.vc/",
  "entity_kind": {"value": "investor", "source_url": "https://lookai.vc/", "source_date": null, "quote": "Look AI Ventures is a pre-Series A venture capital fund based in Prague, Czech Republic, investing in early-stage AI startups."},
  "investor_type": {"value": "vc", "source_url": "https://lookai.vc/", "quote": "Look AI Ventures is a pre-Series A venture capital fund based in Prague, Czech Republic, investing in early-stage AI startups."},
  "sectors": {"value": ["ai"], "source_url": "https://lookai.vc/", "source_date": null, "quote": "Look AI Ventures fund (LAIV) is the first investment fund in the Czech Republic that focuses exclusively on AI startups worldwide"},
  "stages": {"value": ["pre-seed", "seed"], "source_url": "https://lookai.vc/", "source_date": null, "quote": "You are an early-stage startup (pre-Series A)"},
  "ticket_max": {"amount": 250000, "currency": "EUR", "source_url": "https://tech.eu/2023/04/13/czech-republic-has-a-new-investment-fund-for-ai-start-ups", "source_date": "2023-04-13", "quote": "The targeted investment amount in one start-up is €250,000 and mentorship will be provided."},
  "funds": ["Look AI Ventures fund (LAIV)"],
  "investments": [
    {"company": "Embodied AI", "deal_date": "202
… [skrátené, 3191 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://lookai.vc/
OK  investor_type https://lookai.vc/
OK  sectors https://lookai.vc/
OK  stages https://lookai.vc/
OK  ticket_max https://tech.eu/2023/04/13/czech-republic-has-a-new-investment-fund-for-ai-start-ups
OK  inv https://lookai.vc/look-ai-ventures-backs-embodied-ai-robots-manufacturing/
OK  inv https://lookai.vc/look-ai-ventures-sodex-innovations-4m-ai-construction-site-surveying/
OK  inv https://lookai.vc/new-investment-cequence-secures-e2m-to-expand-ai-powered-contract-automation-platform/
OK    research/c071.json
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; .venv/bin/python - <<'EOF'
import json
p="research/c071.json"; d=json.load(open(p))
for i in d["investments"]:
    if i["company"]=="Cequence":
        i["quote"]="Slovak startup Cequence, which helps companies automate contract workflows using artificial intelligence, has successfully raised €2 million in seed funding to accelerate its growth. The round was led by Czech Jet Ventures, with participation from our Look AI Ventures fund"
d["notes"]=d["notes"].replace(" The Cequence quote does not name the company in the same sentence but the page is about the Cequence round.","")
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F check research/c071.json | grep inv; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c071.json
```

<details><summary>Výstup nástroja</summary>

```
OK  investor_type https://lookai.vc/
OK  ticket_max https://tech.eu/2023/04/13/czech-republic-has-a-new-investment-fund-for-ai-start-ups
OK  inv https://lookai.vc/look-ai-ventures-backs-embodied-ai-robots-manufacturing/
OK  inv https://lookai.vc/look-ai-ventures-sodex-innovations-4m-ai-construction-site-surveying/
OK  inv https://lookai.vc/new-investment-cequence-secures-e2m-to-expand-ai-powered-contract-automation-platform/
OK    research/c071.json
```

</details>

## Claude · 2026-10-09 12:33:00 UTC

Presto Ventures.

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.presto.vc/ | grep -v "^\s*$" | head -70
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Presto Ventures Prague VC fund invests 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Presto Ventures Prague VC fund invests 2026"

Links: [{"title":"bohemia venture capital","url":"https://www.cbinsights.com/investor/bohemia-venture-capital"},{"title":"Assisted fundraising","url":"https://hub.waveup.com/funds/presto-ventures"},{"title":"9 Prague seed investors funding Czech tech startups in 2026","url":"https://www.ellty.com/investors/prague-seed-investors"},{"title":"Presto Ventures","url":"https://www.privateequitylist.com/investor/presto-ventures"},{"title":"11 Prague e-commerce investors funding Czech online retail in 2026","url":"https://www.ellty.com/investors/prague-ecommerce-investors"},{"title":"10 Prague angel investors funding Czech pre-seed startups in 2026","url":"https://www.ellty.com/investors/prague-angel-investors"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/prestoventures"},{"title":"10 Prague AI investors funding Czech artificial intelligence in 2026","url":"https://www.ellty.com/investors/prague-ai-investors"},{"title":"300+ investors in your industry, stage, and region Get","url":"https://shizune.co/investors/b2b-investors-czech-republic"}]

Presto Ventures has made several 2026 investments, though the sources are mostly investor databases and listicles, and they don't always agree.

**Recent 2026 deals (as listed by aggregators):**
- **Choice:** A Series A in March 2026, which CB Insights lists at $7.1M with Presto as an existin
… [skrátené, 2950 znakov]
```

</details>

**Nástroj `Bash`**

```bash
for u in https://presto.vc/ https://www.prestoventures.com/ https://prestoventures.com/ https://www.presto.ventures/; do echo "## $u"; curl -sL --max-time 20 -A "Mozilla/5.0" -o /dev/null -w "%{http_code} %{url_effective} %{size_download}\n" $u; done
```

<details><summary>Výstup nástroja</summary>

```
## https://presto.vc/
200 https://presto.vc/ 114
## https://www.prestoventures.com/
200 https://www.prestoventures.com/ 48615
## https://prestoventures.com/
200 https://www.prestoventures.com/ 48615
## https://www.presto.ventures/
200 https://www.prestoventures.com/ 48615
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.prestoventures.com/ | grep -v "^\s*$" | head -80; curl -sL https://www.prestoventures.com/ | grep -oE 'href="[^"]*"' | sort -u | grep -vE "\.(css|png|js|svg)" | head -30
```

<details><summary>Výstup nástroja</summary>

```
Presto Ventures | Stepping Up
PortfolioTeamFoundersHorizonsNewsContact
Portfolio
Team
Founders
Horizons
News
Contact
S
T
E
P
P
I
N
G
U
P.
In a world where software alone cannot solve the most pressing challenges, Presto connects frontier technologies, strategic investments, and purpose: to create a safer, more secure future. We empower impactful, fast-growing tech companies and entrepreneurs who lead the way. Let's step it up a notch. 
For Founders
01
Potential.
Progress.
Presto.
Seed TO SERIES A
Mostly post-revenue companies raising a €800k to €8M financing round, looking to accelerate their growth. Tickets ranging from €500k to €5M.
NATO & FRIENDS
Supporting advanced tech innovators with foundations or a significant operational focus in the countries of NATO, its allies, and the startup nation of Israel.
ADVANCED TECH
Security, defense, and aerospace. Cutting-edge and dual-use solutions, both software and hardware, capable of solving the most pressing global challenges.
Founders Support
Thanks to unmatched partnerships, Presto is a co-builder. We bring unparalleled sector experience and world-class industrial-technological expertise.
Backed by Entrepreneurs
We’re backed by successful entrepreneurs, exited tech founders, and family offices. They pack a punch when it comes to networks and opportunities.
Next Level Ready
We have the know-how and contacts to help founders structure their operations and get ready for follow-up rounds in Western Europe and the US.
For Investors
0
… [skrátené, 5335 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://techcrunch.com/2024/12/19/bluequbit-raises-10m-to-take-quantum-software-into-real-world-applications/ "Presto" | head -3; python3 -I $F get https://therecursive.com/presto-tech-horizons-announces-first-investments-in-ai-and-defense/ "Presto|202" | head -8; python3 -I $F get https://www.prestoventures.com/news | grep -v "^\s*$" | sed -n '8,50p'
```

<details><summary>Výstup nástroja</summary>

```
Also participating in this round was Restive, Chaac Ventures, NKM Capital, Presto Tech Horizons, BigStory, Untapped Ventures, FormulaVC, and Granatus. 
 Presto Tech Horizons Announces First Investments
Presto Tech Horizons Announces First Investments in AI and Defense
DealsDeep TechCzechoslovak Grouppresto venturesCzech Republic
 October 23, 2024 ∙ 2 min read
Start Up Bulgaria! Crossroads 2026
 © 2026 The Recursive.
Contact
IN THE
SPOTLIGHT.
From time to time, our founders and portfolio companies make waves in the news – here’s a sneak peek. For more updates, check out our LinkedIn page or follow @PrestoVC on X.
25/5/26
Presto Ventures
Představenstvo společnosti Presto Ventures II a.s., osoba rizikového kapitálu, se sídlem Na příkopě 859/22, Nové Město, 110 00 Praha 1, IČO: 116 78 704, zapsané v obchodním rejstříku vedeném Městským soudem v Praze, sp. zn. B 26527 (dále jen „Společnost“), svolalo řádnou valnou hromadu na 25.6.2026. Na odkazu níźe jsou umístěny pozvánka a další dokumenty pro akcionáře.View Article
7/2/25
Tech Horizons
Why the future belongs to resilience tech and AI-powered hardwareView Article
20/1/25
Outfindo
Czech Outfindo Raises €1.2M to Transform Online Shopping, Led by Eleven VenturesView Article
16/1/25
Portfolio
10 innovative Czech startups leading the charge in 2025: Cruxo, LakmoosView Article
10/1/25
Jeff App
Latvia’s “MoneySuperMarket” targets $20m funding round and mulls European launchView Article
29/12/24
Presto Ventures
Labs of Latvia Investor Sh
… [skrátené, 2363 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Presto Ventures\" OR \"Presto Tech Horizons\" led round 2026", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://techcrunch.com/2024/12/19/bluequbit-raises-10m-to-take-quantum-software-into-real-world-applications/ | grep -B2 "Presto Tech Horizons"
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Presto Ventures" OR "Presto Tech Horizons" led round 2026"

Links: [{"title":"Presto Ventures","url":"https://seedtable.com/investors/presto-ventures"},{"title":"Back to Presto Ventures","url":"https://seedtable.com/investors/presto-ventures/portfolio"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/prestoventures"},{"title":"Investor profile","url":"https://funding.tech.eu/investors/Presto%20Ventures"},{"title":"How Much Did Presto Raise? Funding & Key Investors","url":"https://websets.exa.ai/websets/directory/presto-funding"},{"title":"Back to PrestoChangelog and Sources","url":"https://seedtable.com/companies/presto/funding-rounds/other-2026-01"},{"title":"I2BF Global Ventures","url":"https://www.seedtable.com/investors/i2bf-global-ventures"},{"title":"bizwire 2026 1 8 presto adds 10m to accelerate ai leadership for enterprise qsr brands","url":"https://stocks.observer-reporter.com/observerreporter/article/bizwire-2026-1-8-presto-adds-10m-to-accelerate-ai-leadership-for-enterprise-qsr-brands"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/presto-technologies/financials"},{"title":"bohemia venture capital","url":"https://www.cbinsights.com/investor/bohemia-venture-capital"}]

I found one clear 2026 lead for Presto Ventures, but nothing specific to Presto Tech Horizons leading a 2026 round.

**Presto Ventures (Prague-based VC)**
- Caplight's p
… [skrátené, 3849 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
“We decided to start the company while sitting on surfboards in Santa Monica, California, in the spring of 2022,” said Gharibyan. “We had just heard a new announcement from the IBM Quantum team about progress on superconducting qubits, and it was clear that the quantum landscape was advancing at an incredible pace.”
“We have been looking for a team to invest in who are looking to enable financial services firms to hit the ground running once quantum is here,” said Tom Brown, partner at Nyca, said in a statement. “Hrant and Hayk have the background, skills, and drive to operationalize something that until recently has mostly been theory.”
Also participating in this round was Restive, Chaac Ventures, NKM Capital, Presto Tech Horizons, BigStory, Untapped Ventures, FormulaVC, and Granatus.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Sloneek OR Zerops investice Presto Ventures 2026", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Přemysl Rubeš Presto Ventures zadržen policie 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Sloneek OR Zerops investice Presto Ventures 2026"

Links: [{"title":"presto ventures","url":"https://www.vcbacked.co/directory/investors/presto-ventures"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/directory/investors/presto"},{"title":"Presto Ventures","url":"https://seedtable.com/investors/presto-ventures"},{"title":"Presto Ventures","url":"https://cc.cz/tag/presto-ventures/"},{"title":"Back to Presto Ventures","url":"https://seedtable.com/investors/presto-ventures/portfolio"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/zerops-secures-500k-pre-seed-funding"},{"title":"zerops raises 500k pre seed cloud platform expansion","url":"https://en.ain.ua/2024/06/20/zerops-raises-500k-pre-seed-cloud-platform-expansion"},{"title":"Filip Lukáč (Sloneek): Nabírat v téhle době peníze? Je to nanic","url":"https://www.lupa.cz/clanky/filip-lukac-sloneek-nabirat-v-tehle-dobe-penize-je-to-nanic/"},{"title":"presto ventures","url":"https://prod.actual.seedtable.com/investors/presto-ventures"},{"title":"presto ventures","url":"https://dev.actual.seedtable.com/investors/presto-ventures"}]

**Short answer:** The search results support a Presto Ventures link to both companies, but the 2026 details come mainly from aggregator databases, and I didn't find a primary press release confirming the terms of either 2026 round.

**Sloneek**
- Seedtable's timeline lists a Series A of 6.0M USD dated 16 June 2026 for Sloneek, and its portfo
… [skrátené, 3301 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Přemysl Rubeš Presto Ventures zadržen policie 2026"

Links: [{"title":"Policie zadržela zakladatele investorského fondu Presto Ventures","url":"https://www.lupa.cz/aktuality/policie-zadrzela-zakladatele-investorskeho-fondu-presto-ventures/"},{"title":"bohemia venture capital","url":"https://www.cbinsights.com/investor/bohemia-venture-capital"},{"title":"Hlavní obsah","url":"https://www.seznamzpravy.cz/clanek/ekonomika-firmy-policie-zadrzela-sefa-startupove-firmy-s-niz-investuje-i-zbrojar-strnad-301214"},{"title":"server o českém Internetu","url":"https://www.lupa.cz/n/policie/"},{"title":"Šéfa startupového fondu, se kterým investoval i miliardář Strnad, zadržela policie. Důvodem není podnikání","url":"https://cc.cz/sefa-startupoveho-fondu-se-kterym-investoval-i-miliardar-strnad-zadrzela-policie-duvodem-neni-podnikani/"},{"title":"Presto Ventures","url":"https://cc.cz/tag/presto-ventures/"},{"title":"Presto Ventures II a.s., osoba rizikového kapitálu","url":"https://www.podnikatel.cz/rejstrik/presto-ventures-ii-a-s-osoba-rizikoveho-kapitalu-11678704/"},{"title":"Eduard Kučera","url":"https://www.podnikatel.cz/rejstrik/osoby/eduard-kucera-2545104/"},{"title":"Kam zajít, co ochutnat a co stojí za pozornost","url":"https://www.newstream.cz/money/nikdy-nebyla-v-cesku-lepsi-doba-na-investice-do-startupu-nez-je-ted-rika-sef-presto-ventures"}]

Police detained Přemysl Rubeš, founder and former managing partner of the Presto Ventures investment fund, in 
… [skrátené, 3814 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/tag/presto-ventures/ | grep -A2 -E "^[0-9]{2}\. [0-9]{1,2}\. 20(2[4-6])" | head -40; python3 -I $F get https://cc.cz/tag/presto-ventures/ | grep -B1 -E "20(2[4-6]) –" | head -40
```

<details><summary>Výstup nástroja</summary>

```
11. 3. 2026 – Peter Brejčák
Přemysl Rubeš stojí za fondem Presto Ventures, který podpořil desítky startupů. Podle vyjádření měl dlouhodobé problémy.
 Galerie11
--
11. 2. 2026 – Peter Brejčák
Ověřeno v terénu a posvěceno Ukrajinou, hlasí startup Occam. Pomáhá škálovat autonomní dronové systémy, aby nebyly závislé na lidské kontrole.
 Galerie6
--
24. 9. 2025 – Filip Magalhães
Technologie Firehawku umožňuje rychlejší výrobu raketového paliva i dělostřelecké munice. Nyní se má šanci dostat i k evropským uživatelům.
 Insider
--
05. 9. 2025 – Filip Magalhães
Stát podpořil například nejen technologické startupy Kiwi, Filuta AI nebo Rossum, ale i třeba Škodu Auto. V prvním kole rozdá 800 milionů korun.
 Insider
--
27. 8. 2025 – Filip Magalhães
Začínali jako topenáři, kteří chtěli digitalizovat své řemeslo. Pak nabrali velké peníze od investorů a plány se změnily. Nakonec projekt zkrachoval.
 Rychlá zpráva
--
15. 5. 2025 – Peter Brejčák
Nápad na startup vznikl v Maďarsku, po roce se zakladatelé přestěhovali do Silicon Valley. Teď do nich investoval i zdejší Presto Tech Horizons.
Gify používají miliardy lidí. Gruzínci s českou investicí konečně přišli na to, jak na nich vydělávat
03. 4. 2025 – Peter Brejčák
„Jsou první, kdo tenhle hlavolam rozlouskl,“ kvituje zdejší fond Presto Ventures. Startup Klipy teď získal další desítky milionů.
Neexistuje žádné „zkusím to“ nebo „uvidíme“. Rozjeďte s námi svůj startup na maximum
27. 2. 2025 – Filip Magalhães
Přihlášky do sedmého běhu akcelerátoru
… [skrátené, 4483 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; curl -sL https://cc.cz/tag/presto-ventures/ | grep -oE 'href="https://cc.cz/(investori-v-cele|gify-pouzivaji|dronum-i-robotum|startupovi-presto)[^"]*"' | sort -u > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/u.txt; cat /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/u.txt; for u in $(sed 's/href="//;s/"$//' /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/u.txt); do echo "## $u"; python3 -I $F get $u "Presto" | head -4; done
```

<details><summary>Výstup nástroja</summary>

```
href="https://cc.cz/dronum-i-robotum-chybi-treninkova-data-z-terenu-a-z-boje-madary-kteri-je-vytvari-podporili-cesti-investori/"
href="https://cc.cz/gify-pouzivaji-miliardy-lidi-gruzinci-s-ceskou-investici-konecne-prisli-na-to-jak-na-nich-vydelavat/"
href="https://cc.cz/investori-v-cele-s-miliardarem-michalem-strnadem-posilaji-desitky-milionu-na-vyvoj-autonomnich-dronu/"
href="https://cc.cz/investori-v-cele-s-miliardarem-michalem-strnadem-posilaji-desitky-milionu-na-vyvoj-autonomnich-dronu/#galerie"
href="https://cc.cz/startupovi-presto-ventures-a-zbrojarska-csg-michala-strnada-rozjizdi-fond-maji-v-nem-4-miliardy/"
## https://cc.cz/dronum-i-robotum-chybi-treninkova-data-z-terenu-a-z-boje-madary-kteri-je-vytvari-podporili-cesti-investori/
Nápad na startup vznikl v Maďarsku, po roce se zakladatelé přestěhovali do Silicon Valley. Teď do nich investoval i zdejší Presto Tech Horizons.
Vyřešili prý zásadní problém – automobilky i další firmy působící v obraně, robotice nebo ve vesmírných technologiích nemají dostatek obrázků, na kterých by mohly trénovat své autonomní systémy. Americko-maďarský startup DiffuseDrive z oblasti tzv. fyzické umělé inteligence dokáže takový fotorealistický obsah vytvářet v řádu hodin. To zaujalo mimo jiné i české investory – fond Presto Tech Horizons společně s americkým Outlanderem vedly seed investici ve výši 3,5 milionu dolarů, v přepočtu 78 milionů korun.
„Pokročilá generativní AI významně mění způsob, jakým se stroje rozhodují – od autonomních aut 
… [skrátené, 5527 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c072.json <<'EOF'
{
  "candidate_id": "c072",
  "name": "Presto Ventures",
  "legal_name": "Presto Ventures II a.s., osoba rizikového kapitálu",
  "reg_no": "11678704",
  "country": "CZ",
  "active_in": ["CZ", "SK", "US", "UA", "GE"],
  "website": "https://www.prestoventures.com/",
  "entity_kind": {"value": "investor", "source_url": "https://www.prestoventures.com/", "source_date": null, "quote": "Since 2016, we’ve invested €40M from two funds. Our new €150M fund targets the best of security, defense, and aerospace tech, with focus on dual-use."},
  "investor_type": {"value": "vc", "source_url": "https://cc.cz/startupovi-presto-ventures-a-zbrojarska-csg-michala-strnada-rozjizdi-fond-maji-v-nem-4-miliardy/", "quote": "Venture kapitálové Presto Ventures patří mezi vůbec nejaktivnější startupové fondy u nás."},
  "sectors": {"value": ["defense", "security", "aerospace", "dual-use"], "source_url": "https://www.prestoventures.com/", "source_date": null, "quote": "Security, defense, and aerospace. Cutting-edge and dual-use solutions, both software and hardware, capable of solving the most pressing global challenges."},
  "stages": {"value": ["seed", "series-a"], "source_url": "https://www.prestoventures.com/", "source_date": null, "quote": "Mostly post-revenue companies raising a €800k to €8M financing round, looking to accelerate their growth. Tickets ranging from €500k to €5M."},
  "ticket_min": {"amount": 500000, "currency": "EUR", "so
… [skrátené, 4376 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://www.prestoventures.com/
OK  investor_type https://cc.cz/startupovi-presto-ventures-a-zbrojarska-csg-michala-strnada-rozjizdi-fond-maji-v-nem-4-miliardy/
OK  sectors https://www.prestoventures.com/
OK  stages https://www.prestoventures.com/
OK  ticket_min https://www.prestoventures.com/
OK  ticket_max https://www.prestoventures.com/
OK  aum https://www.prestoventures.com/
OK  inv https://cc.cz/investori-v-cele-s-miliardarem-michalem-strnadem-posilaji-desitky-milionu-na-vyvoj-autonomnich-dronu/
OK  inv https://cc.cz/dronum-i-robotum-chybi-treninkova-data-z-terenu-a-z-boje-madary-kteri-je-vytvari-podporili-cesti-investori/
OK  inv https://cc.cz/gify-pouzivaji-miliardy-lidi-gruzinci-s-ceskou-investici-konecne-prisli-na-to-jak-na-nich-vydelavat/
OK    research/c072.json
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; .venv/bin/python - <<'EOF'
import json
p="research/c072.json"; d=json.load(open(p))
d["investments"]=[i for i in d["investments"] if i["company"]!="Klipy"]
for i in d["investments"]:
    if i["company"]=="DiffuseDrive":
        i["quote"]="Americko-maďarský startup DiffuseDrive z oblasti tzv. fyzické umělé inteligence dokáže takový fotorealistický obsah vytvářet v řádu hodin. To zaujalo mimo jiné i české investory – fond Presto Tech Horizons společně s americkým Outlanderem vedly seed investici ve výši 3,5 milionu dolarů, v přepočtu 78 milionů korun."
d["notes"]=d["notes"].replace(" Klipy quote refers to a pre-seed investment ~2023 (Klipy's 2025 round is the news). DiffuseDrive quote does not repeat the company name in the sentence (previous sentence names it).","").replace("based on CEE focus and Czech-Slovak portfolio (e.g., Sloneek) — uncertain.","based on Czech-Slovak portfolio company Sloneek (Presto co-invested in 2022 per Lupa.cz) — uncertain.")
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F check research/c072.json | grep inv; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c072.json
```

<details><summary>Výstup nástroja</summary>

```
OK  investor_type https://cc.cz/startupovi-presto-ventures-a-zbrojarska-csg-michala-strnada-rozjizdi-fond-maji-v-nem-4-miliardy/
OK  inv https://cc.cz/investori-v-cele-s-miliardarem-michalem-strnadem-posilaji-desitky-milionu-na-vyvoj-autonomnich-dronu/
OK  inv https://cc.cz/dronum-i-robotum-chybi-treninkova-data-z-terenu-a-z-boje-madary-kteri-je-vytvari-podporili-cesti-investori/
OK    research/c072.json
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; u=$(curl -sL https://cc.cz/tag/presto-ventures/ | grep -oE 'href="https://cc.cz/resi-odliv[^"]*"' | head -1 | sed 's/href="//;s/"$//'); echo $u; python3 -I $F get $u "Presto|Sloneek" | head -6
```

<details><summary>Výstup nástroja</summary>

```
https://cc.cz/resi-odliv-talentu-i-klesajici-produktivitu-hr-startup-sloneek-na-cestu-do-evropy-nabira-90-milionu/
 HR startup Sloneek na cestu do Evropy nabírá 90 milionů - CzechCrunch
Řeší odliv talentů i klesající produktivitu. HR startup Sloneek na cestu do Evropy nabírá 90 milionů
HR manažeři jsou zavaleni banální agendou a ke strategické práci se dostanou málokdy, komentuje česko-slovenský startup Sloneek.
Foto: Sloneek
Tým startupu Sloneek
Podle HR startupu Sloneek firmy kvůli fluktuaci, ztrátě talentů a náboru nevhodných lidí přichází i o třetinu nákladů na zaměstnance. Jeho zakladatelé přitom věří, že dokázali najít řešení na problémy spojené s odlivem talentů i klesající produktivitou. Pomáhají tak s digitalizací rutinních úkolů, aby se personalisté mohli věnovat lidem a šéfové řídit efektivitu a motivaci. Již teď působí po Evropě i ve Spojených státech, na posílení své pozice v zahraničí teď ale uzavřeli další investiční kolo. Přinášíme souhrn nejdůležitějších informací.
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/resi-odliv-talentu-i-klesajici-produktivitu-hr-startup-sloneek-na-cestu-do-evropy-nabira-90-milionu/ | grep -iE "presto|investoř|vedl|fond" | head
```

<details><summary>Výstup nástroja</summary>

```
Kolik již startup získal: V roce 2022 získal Sloneek od Presto Ventures a Vision Ventures jeden milion eur, v roce 2020 od Vision Ventures 350 tisíc eur.
A kdo vůbec investuje? Více než stovka zástupců investorů a fondů v komplexní databázi (CC+).
Související témata:Purple VenturesPresto VenturesSloneekVision VenturesVenture to Future Fund
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; sed -i 's/(Presto co-invested in 2022 per Lupa.cz)/(Presto invested in 2022 per CzechCrunch, 2024-09-10)/' research/c072.json; grep -o "Sloneek[^.]*" research/c072.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c072.json
```

<details><summary>Výstup nástroja</summary>

```
Sloneek (Presto invested in 2022 per CzechCrunch, 2024-09-10) — uncertain
OK    research/c072.json
```

</details>

## Claude · 2026-10-09 12:34:58 UTC

Teraz Fil Rouge, Gi21, JIC Ventures — začnem zdrojovým článkom.

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/ | grep -iE "fil rouge|gi21|jic|fond|eur|202[0-9]" | head -20
```

<details><summary>Výstup nástroja</summary>

```
 Neurovedec prezradil, čo jedáva každý deň. Jeden návyk mu pomáha robiť lepšie rozhodnutia, tvrdí 
Z Brna do Dubaja: Nový fond nalial milióny do startupu, ktorý vznikol ako študentský projekt. Teraz mieri aj na Slovensko
 19. mája 2026 o 16:59 
Študentský projekt z Brna dnes funguje vo viac ako 70 krajinách sveta. Nový fond hľadá ďalšie technologické talenty aj na Slovensku. 
Zakladatelia FaceUp, zľava Pavel Ihm, Jan Sláma a David Špunar Archív/Fond JIC Ventures 
 19. mája 2026 o 16:59 
Ešte pred pár rokmi išlo o študentský projekt, ktorý vznikal v priestoroch brnianskej inovačnej agentúry JIC. Dnes technologická firma FaceUp pôsobí vo viac ako 70 krajinách sveta, chráni vyše 1,5 milióna zamestnancov a študentov a expanduje na americký aj arabský trh. Aktuálne získala ďalšiu veľkú investíciu a zároveň otvorila novú kapitolu aj pre startupy zo Slovenska. 
Dostaň Startitup do svojich Google odporúčaní
Ako sa píše na stránke, o FaceUp začali v roku 2020 prejavovať záujem aj firmy, a tak vznikla komerčná verzia platformy, ktorá poskytuje efektívny nástroj pre ochranu oznamovateľov a podporu otvorenej a bezpečnej firemnej kultúry priamo organizáciám. Dnes už aplikáciu troch kamarátov využíva viac ako 1,5 milióna ľudí vo viac ako 3 500 organizáciách a vo vyše 70 krajinách sveta. 
Čo je zaujímavé, nový venture kapitálový fond JIC Ventures aktuálne oznámil svoju vôbec prvú investíciu, ktorá smerovala práve do startupu FaceUp zameraného okrem iného na etickú firemnú kultúru, whistlebl
… [skrátené, 4433 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "JIC Ventures fond velikost milionů korun první uzávěrka", "mode": "standard"}
```

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for u in https://jicventures.cz/ https://www.jicventures.com/ https://jic.cz/ventures; do echo "## $u"; python3 -I $F get $u | grep -v "^\s*$" | head -40; done
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "JIC Ventures fond velikost milionů korun první uzávěrka"

Links: [{"title":"V Brně vznikl fond pro startupy, který bude investovat i peníze kraje","url":"https://www.lupa.cz/aktuality/v-brne-vznikl-fond-pro-startupy-ktery-bude-investovat-i-penize-kraje/"},{"title":"První kraj v Česku spouští fond s rizikovým kapitálem. Peníze mu dali CTP, Barta nebo Česká spořitelna","url":"https://www.e15.cz/byznys/prvni-kraj-v-cesku-spousti-fond-s-rizikovym-kapitalem-penize-mu-dali-ctp-barta-nebo-ceska-sporitelna-1431949"},{"title":"V Brně vznikl fond, jaký nemá obdoby. Spojuje soukromníky, město, kraj, univerzity i biskupství","url":"https://cc.cz/v-brne-vznikl-fond-jaky-nema-obdoby-spojuje-soukromniky-mesto-kraj-univerzity-i-biskupstvi/"},{"title":"univerzity jako spolumajitele novy fond jic ma nakopnout ceske startupy","url":"https://forbes.cz/univerzity-jako-spolumajitele-novy-fond-jic-ma-nakopnout-ceske-startupy/"},{"title":"jic has launched a venture capital fund for startups president pavel lukashenko came to brno to support the development of innovation and knowledge economy","url":"https://een.gov.cz/en/news/jic-has-launched-a-venture-capital-fund-for-startups-president-pavel-lukashenko-came-to-brno-to-support-the-development-of-innovation-and-knowledge-economy/"},{"title":"jic ventures investuje do faceup cesky startup ziskal pres 110 milionu korun na globalni expanzi","url":"https://forbes.cz/jic-ventures-investuje-do-faceup-cesky-startup-ziskal-pre
… [skrátené, 3379 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
## https://jicventures.cz/
## https://www.jicventures.com/
## https://jic.cz/ventures
 Ventures
Leading with courage, transforming ideas into global ventures​
 Send us your pitch deck
JIC Ventures is a Brno-born VC fund backing technology founders from pre-seed to exit.
We focus on CEE startup founders with global potential. We combine capital, deep expertise, and direct access to ambitious projects – both from universities and our own deal flow. 
Our strength lies in people: when a startup hits a challenge, we actively open doors across our network – from the innovation agency JIC team and expert advisors to alumni founders. Built on 20+ years of shaping a thriving innovation ecosystem, we move fast, stay fully engaged, and invest with a long-term partnership mindset. 
Fund advisors
 SW/HW
 Milan Šimek | Founder Sewio
 Space/dual-use
 Marek Polčák | Founder Vrgineers
 B2B sales 
 Lukáš Maňásek | IDEA StatiCa, ex-YSoft
 Precision instruments, HW/SW
 Martin Zadražil | ex-Tescan, JIC
 HW/SW 
 Ondřej Krajíček | IDEA StatiCa, ex-YSoft
 Precision instruments, HW/SW
 Jan Neuman | Founder NenoVision
 SW 
 Juraj Šabatka | Founder IDEA StatiCa
 Cybersecurity 
 Karel Obluk | ex-AVG
Our invesment focus
ventures1
 Pre-seed /
Seed stage
ventures5
Tickets up to €1M
ventures3
Deep tech, SaaS, and other
ventures4
CEE region
(CZE & SVK priority)
ventures2
 Global
potencial
Our unique value
Lead investor 
 We lead rounds, set the pace, and stay hands-on throughout your gr
… [skrátené, 1505 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://cc.cz/v-brne-vznikl-fond-jaky-nema-obdoby-spojuje-soukromniky-mesto-kraj-univerzity-i-biskupstvi/ | grep -iE "400 milion|cílovou" | head -3; python3 -I $F get https://cc.cz/v-brne-vznikl-fond-jaky-nema-obdoby-spojuje-soukromniky-mesto-kraj-univerzity-i-biskupstvi/ | grep -E "\. 20(26)" | head -2
```

<details><summary>Výstup nástroja</summary>

```
Fond cílí na velikost 400 milionů korun, aktuálně má již alokovaných 320 milionů korun, a je tak ještě otevřený dalším kvalifikovaným investorům. JIC, který byl letos deníkem Financial Times zařazen mezi padesát nejlepších startupových hubů v Evropě, s investičními aktivitami začal již v roce 2015, čtrnáct projektů podpořil jako koinvestor. Nový fond, o němž JIC začal mluvit loni, má představovat další krok – kromě většího kapitálu jde i o roli vedoucího investora, který startupy nejen financuje, ale také aktivně pomáhá jejich růstu na globální úroveň.
Celkový objem fondu: 400 milionů korun
Startupy – 07. 4. 2026 – 2 min čtení
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c075.json <<'EOF'
{
  "candidate_id": "c075",
  "name": "JIC Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK"],
  "website": "https://www.jic.cz/ventures/",
  "entity_kind": {"value": "investor", "source_url": "https://jic.cz/ventures", "source_date": null, "quote": "JIC Ventures is a Brno-born VC fund backing technology founders from pre-seed to exit."},
  "investor_type": {"value": "vc", "source_url": "https://jic.cz/ventures", "quote": "JIC Ventures is a Brno-born VC fund backing technology founders from pre-seed to exit."},
  "sectors": {"value": ["deep tech", "saas"], "source_url": "https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/", "source_date": "2026-05-19", "quote": "Zameriava sa najmä na oblasti deep tech, SaaS a ďalšie vyspelé technológie."},
  "stages": {"value": ["pre-seed", "seed"], "source_url": "https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/", "source_date": "2026-05-19", "quote": "Fond sa sústreďuje najmä na startupy v pre-seed a seed fáze, teda na firmy, ktoré ešte len budujú produkt, tím a prvé strategické partnerstvá."},
  "ticket_max": {"amount": 1000000, "currency": "EUR", "source_url": "https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vzn
… [skrátené, 3023 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://jic.cz/ventures
OK  investor_type https://jic.cz/ventures
OK  sectors https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  stages https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  ticket_max https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  aum https://cc.cz/v-brne-vznikl-fond-jaky-nema-obdoby-spojuje-soukromniky-mesto-kraj-univerzity-i-biskupstvi/
OK  inv https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK    research/c075.json
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://filrougecapital.com/ | grep -v "^\s*$" | head -60
```

**Nástroj `WebSearch`**

```json
{"query": "Fil Rouge Capital fund Zagreb venture capital AUM investments 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Fil Rouge Capital | Capital for the BOLD
Submit Your Pitch.
Submit.
01Our program
02Manifesto
03Portfolio
04Mentors
05
About Us
06Media&Press
07Submit Your Pitch
08Contact Us
Capital for
the BOLD
“Nothing great ever comes easily,
and the bold are those who strive for it anyway.”
Robert Farazin,
Founder @ TV Beat
“Every founder is bold by definition, as each one embarks on a journey to bring their vision to life, embracing the uncertainties and challenges that come with building something new.“
JOSIP BEGIĆ,
Founder @ Lebesgue
“Being bold means having the courage to get back up every time something in this life we choose as entrepreneurs knocks us down.”
JACK THOROGOD,
Founder @ Native Teams
€104M
AUM
178
Startups Funded
290
Founders Backed
PARTNERS
Featured
companies
Submit
Submit Your Pitch
Logistics
Gaming
Marketplace
AI
Logistics
Gaming
Marketplace
AI
Software & Financial Industry
Social Media Marketing
Logistics
FinTech
Our latest news and updates
Articles
More
Why do we look down on founders who brag too much with meaningless "awards"?
by FRC team
29.10.24
FOUNDERS INTERVIEW: CastItAnywhere
by FRC team
29.10.24
Why you should not accelerate twice?
by FRC team
29.10.24
FOUNDERS INTERVIEW: OptiSpace
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Fil Rouge Capital fund Zagreb venture capital AUM investments 2026"

Links: [{"title":"Fil Rouge Capital Overview","url":"https://pitchbook.com/profiles/investor/183196-27"},{"title":"fil rouge capital","url":"https://superscout.co/investor/fil-rouge-capital"},{"title":"venture capital firms dubrovnik","url":"https://www.papermark.com/blog/venture-capital-firms-dubrovnik.md"},{"title":"Blog9 Venture Capital Firms Leading the Charge in Dubrovnik in 2026","url":"https://www.papermark.com/blog/venture-capital-firms-dubrovnik"},{"title":"Fil Rouge Capital","url":"https://www.capboard.io/en/investor/fil-rouge-capital"},{"title":"Fil Rouge Capital (FRC)","url":"https://insights.munich-startup.de/companies/fil_rouge_capital_frc_/team"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/fil-rouge-capital"},{"title":"en.lider.media","url":"https://en.lider.media/?p=214855"},{"title":"Fil Rouge Capital (FRC)","url":"https://venturecapitalarchive.com/venture-funds/fil-rouge-capital-frc-filrougecapital-com"}]

Fil Rouge Capital is a Zagreb-based VC firm with reported AUM of about €100 million, but the investment counts vary a lot across sources.

**Background and AUM**
- A Croatian news outlet reports that Fil Rouge Capital (FRC), the first Croatian venture capital fund, ten years after its establishment, manages over 100 million euros in assets. That article doesn't give a clear public
… [skrátené, 3301 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; curl -sL https://filrougecapital.com/ | grep -oE 'href="[^"]*"' | sort -u | grep -viE "\.(css|png|js|svg|jpg)|fonts" | head -30; python3 -I $F get https://en.lider.media/?p=214855 | grep -iE "Fil Rouge|FRC" | head -6
```

<details><summary>Výstup nástroja</summary>

```
href="/"
href="/accelerate"
href="/blog"
href="/blog-post/founders-interview-castitanywhere"
href="/blog-post/founders-interview-optispace"
href="/blog-post/talking-about-being-rejected"
href="/blog-post/what-is-angel-investing"
href="/blog-post/why-do-we-look-down-on-founders-who-brag-too-much-with-meaningless-awards"
href="/blog-post/why-you-should-not-accelerate-twice"
href="/contact"
href="/cookie-policy"
href="https://cdn.prod.website-files.com"
href="https://fricv3.filrougecapital.com/apply"
href="mailto:[email]"
href="/manifesto"
href="/mentors"
href="/portfolio"
href="/privacy-policy"
href="/team"
href="/terms-of-use"
(eval):1: no matches found: https://en.lider.media/?p=214855
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get "https://en.lider.media/?p=214855" | grep -iE "Fil Rouge|FRC|million|20[12][0-9]" | head -8; python3 -I $F get https://filrougecapital.com/accelerate | grep -v "^\s*$" | grep -iE "€|invest|stage|seed|ticket|equity" | head -15
```

<details><summary>Výstup nástroja</summary>

```
Domestic VC Fund Fil Rouge Capital Surpasses 100 Million Euros in Assets – Lider Media
Sunday, March 8, 2026
Home / Business and Politics / Domestic VC Fund Fil Rouge Capital Surpasses 100 Million Euros in Assets
Domestic VC Fund Fil Rouge Capital Surpasses 100 Million Euros in Assets
February 11, 2026
Fil Rouge Capital (FRC), the first Croatian venture capital fund, ten years after its establishment, manages over 100 million euros in assets, announced one of its founders and partners Julien Coustaury on LinkedIn.
– Ten years ago, Fil Rouge Capital started as an idea that sounded simple: there is enough talent and ambition in the region, but too little venture capital. From that idea, a team has grown that today manages over 100 million euros in assets (AuM). That is a figure that looks nice in the headline, but what is behind it is more important: ten years of learning, building trust, and, honestly, a lot of operational work that is not visible on social media and in the media – said Kuharski.
Let us recall that FRC opened an office in Bucharest, Romania last year and, as part of its growth through the third fund, plans a significantly larger number of investments and further business expansion, as well as the opening of new offices in Tirana, Belgrade, and Ljubljana. The fund has so far invested in over 150 startups from various sectors, in domestic and international companies such as Native Teams, Agrivija, Hypefy, Oradian, and Entrio, which was acquired in 2024 by the PE
… [skrátené, 3957 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Hypefy investicija Fil Rouge Capital 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Hypefy investicija Fil Rouge Capital 2026"

Links: [{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/hypefy"},{"title":"Recent signals","url":"https://seedtable.com/investors/fil-rouge-capital"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/fil-rouge-capital"},{"title":"fil rouge capital surpasses e100 million in assets under management","url":"https://cvca.hr/fil-rouge-capital-surpasses-e100-million-in-assets-under-management/"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/hypefy/financials"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/fil-rouge-capital-launches-60m-fund-in-romania"},{"title":"cvca.hr","url":"https://cvca.hr/?p=8470"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/fil-rouge-capital"},{"title":"fil rouge capital","url":"https://superscout.co/investor/fil-rouge-capital"},{"title":"Fil Rouge Capital expands into Romania","url":"https://www.businessforum.ro/finance/20250415/fil-rouge-capital-expands-into-romania-1690"}]

The search turned up conflicting reports on Fil Rouge Capital's investment in Hypefy, and I couldn't confirm a single verified 2026 deal from one primary source.

**Reports of a 2026 Series A:**
- Seedtable lists Fil Rouge Capital as backing Hypefy in a Series A of $7.2M, announced 30 June 2026, with Fil Rouge as lead. It describes
… [skrátené, 3004 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://www.businessforum.ro/finance/20250415/fil-rouge-capital-expands-into-romania-1690 | grep -iE "Fil Rouge|€|fund|Zagreb|headquart" | head -10
```

<details><summary>Výstup nástroja</summary>

```
Fil Rouge Capital expands into Romania
Fil Rouge Capital expands into Romania
Fil Rouge Capital (FRC) has announced the launch of its latest €60 million venture capital fund (FRC3) and is officially expanding its operations into Romania.
FRC3 has already secured over €45 million at its first close, with a re-up rate exceeding 90%. Through this expansion, Romanian startups will gain direct access to FRC's Accelerator Programme, offering up to €300,000, and the Venture Capital Investment pathway, providing initial funding up to €1 million with potential follow-on investments up to €4 million.
“With FRC's new fund, we can provide not just venture capital, but also funding for the acceleration phase, bridging a long-standing gap in the ecosystem where early-stage startups had little to no access to capital,” said Dumitrescu.
#Fil Rouge Capital
Choice raises €6.6 million to expand restaurant AI platform in CEE
Restaurant technology startup Choice has secured €6.6 million in new funding and is accelerating its expansion across CEE, including Romania, where it entered in 2025.
EGV invests €1.5 million in YOX job marketplace
Early Game Ventures (EGV) has announced a new seed investment of €1.5 million in the startup YOX, a job marketplace that uses AI to streamline the hiring process.
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; cat > research/c073.json <<'EOF'
{
  "candidate_id": "c073",
  "name": "Fil Rouge Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "HR",
  "active_in": ["HR", "RO", "CZ"],
  "website": "https://filrougecapital.com/",
  "entity_kind": {"value": "investor", "source_url": "https://en.lider.media/?p=214855", "source_date": "2026-02-11", "quote": "Fil Rouge Capital (FRC), the first Croatian venture capital fund, ten years after its establishment, manages over 100 million euros in assets, announced one of its founders and partners Julien Coustaury on LinkedIn."},
  "investor_type": {"value": "vc", "source_url": "https://en.lider.media/?p=214855", "quote": "Fil Rouge Capital (FRC), the first Croatian venture capital fund, ten years after its establishment, manages over 100 million euros in assets, announced one of its founders and partners Julien Coustaury on LinkedIn."},
  "stages": {"value": ["pre-seed", "seed"], "source_url": "https://filrougecapital.com/accelerate", "source_date": null, "quote": "We invest from €10k up to €2M across four stages: idea stage, MVP stage, growth stage and follow on stage."},
  "ticket_min": {"amount": 10000, "currency": "EUR", "source_url": "https://filrougecapital.com/accelerate", "source_date": null, "quote": "We invest from €10k up to €2M across four stages: idea stage, MVP stage, growth stage and follow on stage."},
  "ticket_max": {"amount": 2000000, "currency": "EUR", "source_url": "https://filrougecap
… [skrátené, 4810 znakov]
```

**Nástroj `WebSearch`**

```json
{"query": "Gi21 Capital Praha investiční fond startupy", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://en.lider.media/?p=214855
OK  investor_type https://en.lider.media/?p=214855
OK  stages https://filrougecapital.com/accelerate
OK  ticket_min https://filrougecapital.com/accelerate
OK  ticket_max https://filrougecapital.com/accelerate
OK  aum https://en.lider.media/?p=214855
OK  inv https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  entity_kind https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  investor_type https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  inv https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK    research/c073.json
OK    research/c074.json
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Gi21 Capital Praha investiční fond startupy"

Links: [{"title":"Gi21 Capital: Interview With Founder Damir Špoljarič About The Investment Firm","url":"https://pulse2.com/gi21-capital-profile-damir-spoljaric-interview/amp/"},{"title":"Gi21 Capital: Interview With Founder Damir Špoljarič About The Investment Firm","url":"https://pulse2.com/gi21-capital-profile-damir-spoljaric-interview/"},{"title":"Gi21 Capital Overview","url":"https://pitchbook.com/profiles/investor/540892-72"},{"title":"Gi21 Capital","url":"https://www.premieralts.com/investors/gi21-capital/portfolio"},{"title":"Venture Capital","url":"https://altss.com/profile/gi21-capital"},{"title":"www.openvc.app","url":"https://www.openvc.app/fund/Gi21%20Capital"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/gi21-capital"},{"title":"Gi21 CapitalGi21 Capital","url":"https://www.startuphub.ai/investors/gi21-capital"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/gi21capital"}]

Gi21 Capital is a Prague-based investment firm that backs early-stage technology companies, mainly in AI infrastructure, B2B software, robotics, and deep tech, with a focus on Europe and the US. Sources disagree on some details, so treat the figures below as approximate.

**Overview and focus**
- Its founder describes it as a technology investment firm that has grown out of a family office. [1](https://pulse2.com/gi21-cap
… [skrátené, 3783 znakov]
```

</details>

**Nástroj `Bash`**

```bash
F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; python3 -I $F get https://gi21capital.com/ | grep -v "^\s*$" | head -40; python3 -I $F get https://pulse2.com/gi21-capital-profile-damir-spoljaric-interview/ | grep -iE "family office|own capital|invest" | head -6; python3 -I $F get https://en.ain.ua/2024/06/20/zerops-raises-500k-pre-seed-cloud-platform-expansion "Gi21" | head -3
```

<details><summary>Výstup nástroja</summary>

```
Gi21 Capital | Multi-Stage Investment Group
Home
About
About Gi21Damir SpoljaricTeamBlogAI InfrastructureAbout Gi21Damir SpoljaricTeamBlogAI InfrastructureInvestmentsHospitalityCulture & ArtContact
Contact
Moving great ideas forward.
Gi21 Capital is a multi-stage investment group bridging the gap between entrepreneurial agility and institutional-grade scale.
About Gi21 Capital
What We Do
Building the Infrastructure of the Future
Strategic capital for a changing world. We are a diversified investment firm operating across digital and physical frontiers.
DC Infrastructure
Building Europe's AI backbone. Institutional fund for next-gen data centers.
Learn more
Hospitality
Premium assets, operational discipline. Hotels & private aviation across Europe.
Learn more
VC / PE technology investments
Backing technical founders solving complex problems through Deep Tech, B2B SaaS, AI.
Learn more
Culture & Art
Patron of the arts. Museum Kampa, KVIFF, Česká filharmonie, Dejvické divadlo.
Learn more
Highlights
Where we stand today
Born from the operational leadership and landmark exits of major regional technology infrastructures, we bring 20 years of "battle-tested" expertise to every partnership.
We deploy principal capital to accelerate global AI-first startups and leverage institutional fund structures to build the continent's most ambitious digital assets—including the largest pan-European AI data center platform. 
$4B+
Valuation of invested companies
We don't just invest; we build and 
… [skrátené, 3683 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; .venv/bin/python - <<'EOF'
import json
p="research/c074.json"; d=json.load(open(p))
d["website"]="https://gi21capital.com/"
d["active_in"]=["CZ","US"]
d["entity_kind"]={"value":"investor","source_url":"https://gi21capital.com/","source_date":None,"quote":"Gi21 Capital is a multi-stage investment group bridging the gap between entrepreneurial agility and institutional-grade scale."}
d["investor_type"]={"value":"private_investor","source_url":"https://pulse2.com/gi21-capital-profile-damir-spoljaric-interview/","quote":"Gi21 has evolved from a family office into a founder-first firm driven by an operator’s DNA. We built the vehicle I wish I’d had at 17, one that offers the speed of a founder and the patience of permanent capital. By investing our own money, we eliminate LP pressure"}
d["sectors"]={"value":["deep tech","b2b saas","ai"],"source_url":"https://gi21capital.com/","source_date":None,"quote":"Backing technical founders solving complex problems through Deep Tech, B2B SaaS, AI."}
d["investments"].append({"company":"Zerops","deal_date":"2024-06-20","source_url":"https://en.ain.ua/2024/06/20/zerops-raises-500k-pre-seed-cloud-platform-expansion","source_date":"2024-06-20","quote":"Zerops, a Prague-based developer of a cloud platform that builds, deploys, and manages apps, has raised $500,000 in a pre-Seed investment round backed by Presto Ventures and Gi21 Capital."})
d["notes"]="Prague investment group of founder Damir Špoljarič investing own (pe
… [skrátené, 2625 znakov]
```

<details><summary>Výstup nástroja</summary>

```
OK  entity_kind https://gi21capital.com/
OK  investor_type https://pulse2.com/gi21-capital-profile-damir-spoljaric-interview/
OK  sectors https://gi21capital.com/
OK  inv https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/
OK  inv https://en.ain.ua/2024/06/20/zerops-raises-500k-pre-seed-cloud-platform-expansion
OK  inv https://cc.cz/dronum-i-robotum-chybi-treninkova-data-z-terenu-a-z-boje-madary-kteri-je-vytvari-podporili-cesti-investori/
OK  inv https://en.ain.ua/2024/06/20/zerops-raises-500k-pre-seed-cloud-platform-expansion
OK    research/c061.json
OK    research/c062.json
OK    research/c063.json
OK    research/c064.json
OK    research/c065.json
OK    research/c066.json
OK    research/c067.json
OK    research/c068.json
OK    research/c069.json
OK    research/c070.json
OK    research/c071.json
OK    research/c072.json
OK    research/c073.json
OK    research/c074.json
OK    research/c075.json
```

</details>

**Nástroj `Bash`**

```bash
cd /home/filip/investor-db; F="/tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/bin/fetch.py"; for i in $(seq 61 75); do python3 -I $F check research/c0$i.json; done | grep -c "^OK"; for i in $(seq 61 75); do python3 -I $F check research/c0$i.json; done | grep MISS
```

<details><summary>Výstup nástroja</summary>

```
90
```

</details>

**Nástroj `SendMessage`**

```json
{"to": "team-lead", "summary": "c061-c075 done, report", "message": "c061–c075 hotové: 15 súborov v research/, všetky prešli check-schema OK. Všetkých 90 citátov som overil voči stiahnutému textu stránky (whitespace normalizovaný), žiadny MISS.\n\nid | entity_kind | type | #investments | missing fields\nc061 Simpact VC | investor | vc | 2 (ForActive 2026-07, Ligence 2024-11) | SK nie je v active_in (chýba dôkaz)\nc062 CB ESPRI | investor | vc | 2 (Elv.ai 2024-01-15, Powerful Medical 2022) | stages, aum\nc063 Sociálni Inovátori Impact Capital | investor | vc | 0 | stages, aum, investments\nc064 J&T Ventures | investor | vc | 2 (Definic 2026-06, ValkaAI 2026-02) | aum, funds\nc065 IPM Group | investor | vc | 1 (InoBat 2024-12) | stages, tickets, aum\nc066 BIC Bratislava | service_provider | – | 0 | –\nc067 365fintech | investor | cvc | 2 (Ctrl Alt 2023-10-23, Ondato 2022) | tickets, aum\nc068 McWin | investor | pe | 2 (Incapto 2026-04, Ecorobotix 2025-10) | stages, tickets, aum, website\nc069 Ergos | investor | vc | 0 | takmer všetko (len Tracxn)\nc070 Jet Ventures | investor | vc | 1 (Cequence 2025-06) | stages, ticket_min; duplicate_of=c007\nc071 Look AI Ventures | investor | vc | 
… [skrátené, 2982 znakov]
```

<details><summary>Výstup nástroja</summary>

```
{"success":true,"message":"Message sent to team-lead's inbox","msg_id":"30df01fd-a6e6-4a1e-add3-956e4ecd1a76","routing":{"sender":"research-5","senderColor":"orange","target":"@team-lead","targetColor":"red","summary":"c061-c075 done, report","content":"c061–c075 hotové: 15 súborov v research/, všetky …"}}
```

</details>

## Claude · 2026-10-09 12:37:30 UTC

Kandidáti c061–c075 sú hotoví: 15 súborov v `/home/filip/investor-db/research/` (c061.json až c075.json). Všetky prešli `check-schema` bez chyby. Všetkých 90 citátov som pomocným skriptom porovnal so stiahnutým textom stránok a žiadny nechýbal. Hlásenie som poslal team-leadovi.

| id | entity_kind | typ | počet investícií | chýbajúce polia |
|---|---|---|---|---|
| c061 Simpact VC | investor | vc | 2 | SK nie je v active_in, chýba dôkaz |
| c062 CB ESPRI | investor | vc | 2 | stages, aum |
| c063 Sociálni Inovátori Impact Capital | investor | vc | 0 | stages, aum, investments |
| c064 J&T Ventures | investor | vc | 2 | aum, funds |
| c065 IPM Group | investor | vc | 1 | stages, tickets, aum |
| c066 BIC Bratislava | service_provider | – | 0 | – |
| c067 365fintech | investor | cvc | 2 | tickets, aum |
| c068 McWin | investor | pe | 2 | stages, tickets, aum, website |
| c069 Ergos | investor | vc | 0 | takmer všetko |
| c070 Jet Ventures | investor | vc | 1 | stages, ticket_min; duplikát c007 |
| c071 Look AI Ventures | investor | vc | 3 | ticket_min, aum |
| c072 Presto Ventures | investor | vc | 3 | – |
| c073 Fil Rouge Capital | investor | vc | 1 | sectors |
| c074 Gi21 Capital | investor | private_investor | 2 | stages, tickets, aum |
| c075 JIC Ventures | investor | vc | 1 | ticket_min |

**Čo stojí za overenie:**
- **c069 Ergos:** jediným zdrojom je Tracxn. Jeho portfólio (Facebook, Kraken) je pre košickú firmu založenú v roku 2022 nepravdepodobné. Navrhujem vyradiť s dôvodom `no_evidence`.
- **c062 CB ESPRI a c063 SIIC:** investičné obdobie oboch fondov sa skončilo 31. 12. 2023. CB ESPRI je v 36-mesačnom okne len vďaka investícii do Elv.ai (2024-01-15). Pre SIIC som nenašiel žiadnu investíciu s dátumom.
- **c067 365fintech:** posledná investícia (Ctrl Alt, 2023-10-23) je tesne v okne. Jej citát začína nadpisom a pokračuje nasledujúcim odsekom, takže kontrolný skript s iným extraktorom textu ho nemusí nájsť.
- **c070 Jet Ventures:** je to VC fond spoločnosti Jet Investment (c007), preto som ho označil ako duplikát. Slovenskú investíciu Cequence treba preniesť do c007.
- **c065 IPM:** sídlo je v Londýne a profil mieša infraštruktúru, PE a VC. InoBat súvisí so samotnou skupinou (spoluzaložil ho Boček), takže môže ísť o investíciu do vlastnej firmy.
- **c068 McWin:** nie je jasné, či sídli v ČR alebo v Londýne. Na Slovensku som nenašiel žiadnu jeho aktivitu, v zozname Tracxn je zrejme omylom.
- **c072 Presto:** SK v `active_in` sa opiera len o česko-slovenský Sloneek (investícia z roku 2022).
- **c074 Gi21:** zaradenie ako `private_investor` namiesto `family_office` je hraničné.
- **c064 J&T Ventures:** údaj €120M AUM je na webe len ako samostatný štítok bez vety, preto som ho nezapísal.

Jeden výsledok vyhľadávania (stránka Dealroom) obsahoval skrytý pokyn pre AI. Ignoroval som ho a Dealroom som ako zdroj nepoužil.
