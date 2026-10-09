# Subagent agent-aresearch-4-5b2ea734f7ae0813

Zdroj: transkript Claude Code `agent-aresearch-4-5b2ea734f7ae0813.jsonl`

## Používateľ · 2026-10-09 12:20:03 UTC

<teammate-message teammate_id="team-lead" summary="Research candidates c044-c060">
You are a research agent for the project in /home/filip/investor-db. Read /home/filip/investor-db/prompts/research_agent.md first and follow it exactly. Candidate list: /home/filip/investor-db/data/candidates.csv (columns: candidate_id, name, discovery_source, discovery_url).

Your assigned candidates: c044 to c060 (inclusive). They come from public lists of equity funds in Slovakia and from news. Some lists are old, so some funds may be inactive, renamed or duplicates of other candidates (check the whole candidates.csv for duplicates, e.g. a platform vs. its fund, or Slovenský rastový a kapitálový fond vs. other public funds).

Use WebSearch and WebFetch to find sources. Write one JSON file per candidate to /home/filip/investor-db/research/<candidate_id>.json. Do not touch any other files. Validate each file with:
cd /home/filip/investor-db && PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/<id>.json

Remember: quotes must be verbatim from the page text at source_url (a script will check it); missing data is better than wrong data. Finish with the one-line-per-candidate report described in the instructions, plus a short list of anything you were unsure about.
</teammate-message>

**Nástroj `Bash`**

```bash
cat /home/filip/investor-db/prompts/research_agent.md; echo ----; cat /home/filip/investor-db/data/candidates.csv; ls /home/filip/investor-db/research/ | head -50
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
… [skrátené, 14190 znakov]
```

</details>

**Nástroj `Bash`**

```bash
ls research/ src/investordb/ ; PYTHONPATH=src .venv/bin/python -m investordb.cli --help
```

**Nástroj `ToolSearch`**

```json
{"query": "select:WebSearch,WebFetch", "max_results": 2}
```

<details><summary>Výstup nástroja</summary>

```
research/:

src/investordb/:
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
```

</details>

**Nástroj `Bash`**

```bash
cat src/investordb/models.py | head -80; .venv/bin/python -c "import bs4, httpx" ; .venv/bin/pip list 2>/dev/null | head -30; curl -sI https://www.credoventures.com | head -3
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
… [skrátené, 2381 znakov]
```

</details>

**Nástroj `Bash`**

```bash
sed -n 80,200p src/investordb/models.py; ls src/investordb; ls; .venv/bin/python -c "import pydantic; print(pydantic.VERSION)"; python3 -c "import html.parser; print('ok')"
```

<details><summary>Výstup nástroja</summary>

```
    website: HttpUrl | None = None
    entity_kind: KindFact
    investor_type: TypeFact | None = None
    sectors: SectorsFact | None = None
    stages: StagesFact | None = None
    ticket_min: MoneyFact | None = None
    ticket_max: MoneyFact | None = None
    aum: MoneyFact | None = None
    funds: list[str] = Field(default_factory=list)
    investments: list[Investment] = Field(default_factory=list)
    duplicate_of: str | None = Field(default=None, pattern=r"^c\d{3}$")
    notes: str = ""
    researched_at: date

    @field_validator("active_in")
    @classmethod
    def country_codes(cls, value: list[str]) -> list[str]:
        for code in value:
            if len(code) != 2 or not code.isupper():
                raise ValueError(f"invalid country code: {code}")
        return value

    @model_validator(mode="after")
    def investor_needs_type(self) -> "ResearchRecord":
        if self.entity_kind.value == "investor" and self.investor_type is None:
            raise ValueError("entity_kind=investor requires investor_type")
        if self.duplicate_of == self.candidate_id:
            raise ValueError("record cannot be a duplicate of itself")
        return self

    def evidence_items(self) -> list[tuple[str, Evidence]]:
        items: list[tuple[str, Evidence]] = [("entity_kind", self.entity_kind)]
        for field in ("investor_type", "sectors", "stages", "ticket_min", "ticket_max", "aum"):
            fact = getattr(self, field)
            if fact is not None:

… [skrátené, 1893 znakov]
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/pages
cat > /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/fetch.py <<'EOF'
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
    t = re.sub(r"[ \
… [skrátené, 2615 znakov]
```

<details><summary>Výstup nástroja</summary>

```
done
```

</details>

## Claude · 2026-10-09 12:20:33 UTC

Začnem s Benson Oak Capital (c044).

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.legalfirm.sk/sk/stranky/clanok/zoznam-equity-fondov "Benson|BHS|Credo|Crowdberry|ARCH|ZAKA|3TS|rozvojov" ; N=4000 python3 -I fetch.py https://www.bensonoak.com/
```

<details><summary>Výstup nástroja</summary>

```
>> Benson Oak Capital – fond investuje do spoločností, ktoré vykazujú významný domáci alebo medzinárodný rastový potenciál, s veľkosťou transakcií zvyčajne medzi 5 až 15 miliónov eur.
>> BHS private equity fund – princípom fondu je dlhodobé zhodnocovanie kapitálu formou investície do slovenských a českých spoločností s cieľom urýchliť ich rast a tým maximalizovať ich hodnotu.
>> Credo Ventures – česká spoločnosť, ktorá podporuje podnikateľov v strednej Európe a investuje do spoločností od 50 000 do 10 miliónov eur.
>> Crowdberry – umožňuje súkromným investorom spoluvlastniť slovenské a české firmy, nad ktorými majú dohľad profesionáli. Pomáhajú im vytvoriť dlhodobú hodnotu a prispievať tak k celkovému rastu domácej ekonomiky. Taktiež podporujú priame lokálne investovanie.
>> Genesis Capital – výber investícií prebieha na základe niekoľkých aspektov. Spoločnosť by mala na trhu pôsobiť niekoľko rokov, má silný rastový potenciál, skúsený manažérsky tím s preukázateľnou schopnosťou úspešnej realizácie rozvojových projektov. Genesis Capital nefinancuje projekty v oblasti nehnuteľnosti, zbrojného priemyslu, hazardných hier, zábavy pre dospelých, tabakových výrobkov a liehovín.
>> J&T ARCH INVESTMENTS – stratégiou fondu je investovanie do príležitostí a projektov, ktoré vytvárajú v skupine J&T sami alebo spoločne s dlhodobými partnermi.
>> ZAKA – investuje do projektov, ktoré ich oslovia svojím inovatívnym nápadom a rastovým potencionálnom. Žiadateľ musí vyplniť registračný formulár
… [skrátené, 2056 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad && curl -sIL --max-time 20 https://www.bensonoak.com/ | grep -iE "^(HTTP|location)"; curl -sIL --max-time 20 https://bensonoak.com/ | grep -iE "^(HTTP|location)"
```

**Nástroj `WebSearch`**

```json
{"query": "Benson Oak Capital investment 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Benson Oak Capital investment 2025"

Links: [{"title":"Benson Oak Capital","url":"https://privateequitylist.com/public/investor/benson-oak-capital"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/benson-oak-capital"},{"title":"Benson Oak Capital","url":"https://privateequitylist.com/investors/benson-oak-capital"},{"title":"CHRISTIAN HENZE A3RAUL","url":"https://sa.marketscreener.com/insider/CHRISTIAN-HENZE-A3RAUL/"},{"title":"CHRISTIAN HENZE A3RAUL","url":"https://it.marketscreener.com/insider/CHRISTIAN-HENZE-A3RAUL/"},{"title":"NOLA.com: Benson Capital Partners, venture fund backed by Gayle Benson, to invest $53M","url":"https://freemannews.tulane.edu/node/3282"},{"title":"TOMAS FENCL A0J1P8","url":"https://se.marketscreener.com/insider/TOMAS-FENCL-A0J1P8/"},{"title":"TOMAS FENCL A0J1P8","url":"https://www.zonebourse.com/insider/TOMAS-FENCL-A0J1P8/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/benson-capital"},{"title":"benson adds usd5 2 million stake in amrize after holcim spinoff","url":"https://www.fool.com/coverage/filings/2025/10/12/benson-adds-usd5-2-million-stake-in-amrize-after-holcim-spinoff"}]

I didn't find any reported Benson Oak Capital investment from 2025. The results describe the firm's focus and past deals, but none are dated 2025.

**What the results say about the firm**
- One investor profile describes it as a venture capital firm founded in 2001 that
… [skrátené, 3210 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.bensonoak.cz/ https://bensonoak.cz/ https://www.bensonoak.com/en https://www.bensonoak.eu; do echo "== $u"; curl -sIL --max-time 15 $u | grep -iE "^(HTTP|location)"; done
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
== https://www.bensonoak.cz/
== https://bensonoak.cz/
== https://www.bensonoak.com/en
== https://www.bensonoak.eu
```

</details>

**Nástroj `Bash`**

```bash
curl -sS -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.bensonoak.com/ ; curl -sS -o /dev/null -w "%{http_code}\n" --max-time 15 https://bensonoak.cz/
```

<details><summary>Výstup nástroja</summary>

```
Exit code 60
curl: (60) SSL: no alternative certificate subject name matches target hostname 'www.bensonoak.com'
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the webpage mentioned above.
000
curl: (60) SSL: no alternative certificate subject name matches target hostname 'bensonoak.cz'
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the webpage mentioned above.
000
```

</details>

**Nástroj `Bash`**

```bash
curl -sL --max-time 15 http://www.bensonoak.com/ | head -c 1500; echo; curl -sL --max-time 15 http://bensonoak.cz/ | head -c 1500
```

<details><summary>Výstup nástroja</summary>

```
<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charSet="utf-8"/><meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width, shrink-to-fit=no"/><meta name="theme-color" content="#3f51b5"/><link href="/static/favicon.ico" rel="shortcut icon" type="image/x-icon"/><link rel="stylesheet" type="text/css" href="/static/css/MyFontsWebfontsKit.css"/><link rel="stylesheet" type="text/css" charSet="UTF-8" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css"/><script src="https://cdn.ravenjs.com/3.26.2/raven.min.js" crossOrigin="anonymous"></script><meta charSet="utf-8" class="next-head"/><link rel="preload" href="/_next/static/_eC0KmaGthoJH3mFtC6qe/pages/index.js" as="script"/><link rel="preload" href="/_next/static/_eC0KmaGthoJH3mFtC6qe/pages/_app.js" as="script"/><link rel="preload" href="/_next/static/runtime/webpack-838b392324e3598684b5.js" as="script"/><link rel="preload" href="/_next/static/chunks/commons.e1c83f8ff158fa8d2e3f.js" as="script"/><link rel="preload" href="/_next/static/runtime/main-205ce9a5de5d463815f0.js" as="script"/><style id="jss-server-side">
.jss1 {}
.jss2 {}
.jss5 {}
.jss6 {}
.jss9 {}
.jss10 {
  align-items: center;
}
@media (min-width:960px) {
  .jss10 {
    display: flex;
  }
}
.jss11 {}
.jss12 {}
.jss13 {}
.jss14 {}
@media (min-width:960px) {
  .jss14 {
    display: flex;
  }
}
.jss15 {}
.jss18 {}
.jss19 {}
.jss20 {
  margin-top: 50px;
}
@media (min-width:960px) {
  .jss20 {
    display: flex;
    ma
… [skrátené, 3001 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=3000 python3 -I fetch.py http://bensonoak.cz/; curl -sL --max-time 15 http://bensonoak.cz/ | grep -oiE 'href="[^"]+"' | sort -u | head -40
```

<details><summary>Výstup nástroja</summary>

```
Benson Oak Capital
Benson Oak
Benson Oak is the exclusive advisor to Benson Oak Capital Cooperatif U.A., a buy-out and growth equity firm investing into leading businesses based in the Czech Republic and Slovakia. We invest in companies which demonstrate significant domestic and/or international growth potential, with transaction sizes typically between €5 and €15 million though our flexible approach allows us to invest more or less; in the end, we target opportunities, not deal size.
With almost 20 years on the Czech and Slovak markets, Benson Oak Capital has a proven track record of creating value for all stakeholders. Our investment into AVG Technologies remains the most successful private equity transaction in the region and highlights our passion for turning promising domestic businesses into international giants. BOC’s professionals are based primarily in Prague, facilitating constant flow of information and rapid decision making, allowing us to react quickly to both opportunities and challenges alike.
Find out more about BOC »
Featured Press Releases
AVG Technologies N.V. Prices Initial Public Offering
February 1, 2012
AMSTERDAM, and NEW YORK, Feb. 1, 2012 /PRNewswire/ -- AVG Technologies N.V. today announced the pricing of its initial public offering of 8.0 million ordinary shares at a price to the public of $16.00 per share. The shares will begin trading on the New York Stock Exchange on February 2, 2012 under the ticker symbol "AVG."
HP TRONIC to buy ETA from Benson
… [skrátené, 3818 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Benson Oak\" Bochemie prodej OR investice", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Benson Oak" Bochemie prodej OR investice"

Links: [{"title":"FORWARD FEATURES CALENDAR","url":"https://www.privateequitywire.co.uk/arx-equity-partners-joins-benson-oak-capital-investor-bochemie/"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/bochemie"},{"title":"www.arxequity.com","url":"https://www.arxequity.com/?p=344"},{"title":"ARX Equity Partners joins Benson Oak Capital as investor in Bochemie","url":"https://www.arxequity.com/2010/11/"},{"title":"EYAL SHANI A3M8HA","url":"https://de.marketscreener.com/insider/EYAL-SHANI-A3M8HA/"},{"title":"Compare Bochemie vs Symbiom","url":"https://www.cbinsights.com/compare/bochemie-vs-symbiom"},{"title":"Compare Bochemie vs Safina","url":"https://www.cbinsights.com/compare/bochemie-vs-safina"},{"title":"Benson Oak Capital","url":"https://privateequitylist.com/public/investor/benson-oak-capital"},{"title":"EYAL SHANI A3M8HA","url":"https://in.marketscreener.com/insider/EYAL-SHANI-A3M8HA/"},{"title":"Benson Oak Capital","url":"https://privateequitylist.com/investors/benson-oak-capital"}]

The search turned up a 2010 minority investment in Bochemie, plus a later ownership change. Results on the investment firm itself are thinner and less clearly tied to Bochemie.

**2010 investment by ARX.** ARX Equity Partners, a Central and Eastern European private equity firm, joined Benson Oak Capital as an investor in Bochemie in November 2010. ARX took a minority stake in the Group. The m
… [skrátené, 2997 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Weinhold Legal Klikpojisteni.cz Benson Oak sale", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Weinhold Legal Klikpojisteni.cz Benson Oak sale"

Links: [{"title":"13616 weinhold legal and wolf theiss advise on sale of klikpojisteni cz","url":"https://ceelegalmatters.com/czech-republic/13616-weinhold-legal-and-wolf-theiss-advise-on-sale-of-klikpojisteni-cz"},{"title":"13616 weinhold legal and wolf theiss advise on sale of klikpojisteni cz","url":"https://www.ceelegalmatters.com/wolf-theiss/13616-weinhold-legal-and-wolf-theiss-advise-on-sale-of-klikpojisteni-cz"},{"title":"Benson Oak Capital Announces Sale of Online Broker Klikpojisteni.cz a.s","url":"https://www.businesswire.com/news/home/20200519005971/en/Benson-Oak-Capital-Announces-Sale-of-Online-Broker-Klikpojisteni.cz-a.s."},{"title":"DEAL MONITOR","url":"https://epravo.cz/top/clanky/deal-monitor-111206.html"},{"title":"deal monitor 111206","url":"https://www.epravo.cz/top/clanky/deal-monitor-111206.html?pdf=1"},{"title":"Travers Smith advises on the acquisition of Klik by TA Associates investee company, Netrisk","url":"https://www.traverssmith.com/knowledge/knowledge-container/travers-smith-advises-on-the-acquisition-of-klik-by-ta-associates-investee-company-netrisk/"},{"title":"benson oak divests entire stake in online insurance broker klik","url":"https://lifeinsuranceinternational.com/news/benson-oak-divests-entire-stake-in-online-insurance-broker-klik"},{"title":"benson oak fully exits eastern european online broker klikpojisteni cz to ta associates and mci euroventures backed ne
… [skrátené, 3766 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.businesswire.com/news/home/20200519005971/en/Benson-Oak-Capital-Announces-Sale-of-Online-Broker-Klikpojisteni.cz-a.s. "Benson|2011|inception" | head; echo ===; python3 -I fetch.py https://www.lupa.cz/aktuality/eichler-prodava-klik-cz-sluzbu-online-pojisteni-ziskavaji-byvali-investori-avg/ "Benson|Eichler|2011|založ" | head -20
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
(eval):1: == not found
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.businesswire.com/news/home/20200519005971/en/Benson-Oak-Capital-Announces-Sale-of-Online-Broker-Klikpojisteni.cz-a.s." "Benson|2011|inception" | head; echo XXX; python3 -I fetch.py "https://www.lupa.cz/aktuality/eichler-prodava-klik-cz-sluzbu-online-pojisteni-ziskavaji-byvali-investori-avg/" "Benson|Eichler|2011|založ" | head -20
```

<details><summary>Výstup nástroja</summary>

```
XXX
>> Eichler prodává Klik.cz, službu online pojištění získávají bývalí investoři AVG - Lupa.cz
>> Eichler prodává Klik.cz, službu online pojištění získávají bývalí investoři AVG
>> Česká společnost Klikpojisteni.cz fungující také pod doménami Klik.cz a Klik.sk mění majitele. Fond Benson Oak Capital, za nímž stojí Gabriel Eichler, který pomohl dovést brněnské AVG na newyorskou burzu, společně s dalšími minoritními investory Klik prodali maďarské firmě Netrisk.
>> Klik funguje od roku 2011 a v Česku a na Slovensku zaměstnává asi 120 lidí. Poslední finanční výsledky jsou v obchodním rejstříku zaznamenány za rok 2017, tehdy Klik vykázal tržby kolem 106 milionů se ziskem 15 milionů.
>> Benson Oak firmu financoval od jejího vzniku. E-commerce projekt se soustředí na prodej několika druhů pojištění online. Spolupracuje s většinou pojišťoven na trhu a má přes půl milionu uzavřených pojistek. Netrisk to samé dělá v Maďarsku, kde drží hlavní pozici. Akvizice má být součástí budování středoevropské skupiny online pojištění.
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.lupa.cz/aktuality/eichler-prodava-klik-cz-sluzbu-online-pojisteni-ziskavaji-byvali-investori-avg/" "2020" | head -5; curl -sL http://bensonoak.cz/company/investment-strategy | python3 -c "import sys,re;t=re.sub(r'<[^>]+>',' ',sys.stdin.read());print(re.sub(r'\s+',' ',t)[:2500])"
```

<details><summary>Výstup nástroja</summary>

```
>> 21. 5. 2020
 Benson Oak Capital Investment Strategy BOC’s approach is centered on maximizing opportunities within the Czech Republic and Slovakia. Given the diversity of industries active in both countries and concentration in terms of company size, BOC is committed to the low/middle market, taking controlling stakes with equity investments of between €5 and 30 million; co-investment on larger transactions is also possible. Rather than limiting ourselves to particular industries, we choose instead to work with companies which demonstrate the capability to be leaders in either domestic or international markets. Domestic The evolution of the Czech and Slovak economies brings with it the opportunity for companies to become domestic leaders in traditionally underserved industries. The last 20 years have played witness to segments of the economy spurred by macro changes, fostering growth to levels found in Western European countries. For businesses competing in these industries, the difference between market leadership and failure is often a well-timed infusion of capital; we seek to identify and fund companies on the cusp of such expansion. International BOC is proud to stand alongside Czech and Slovak champions, businesses with products and services already successfully being sold beyond our borders. Providing these companies with additional strategic vision, capital necessary to expand their sales networks, complete foreign acquisitions and attract additional managerial tale
… [skrátené, 2514 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c044.json`
```
{
  "candidate_id": "c044",
  "name": "Benson Oak Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK"],
  "website": "http://bensonoak.cz/",
  "entity_kind": {
    "value": "investor",
    "source_url": "http://bensonoak.cz/",
    "quote": "Benson Oak is the exclusive advisor to Benson Oak Capital Cooperatif U.A., a buy-out and growth equity firm investing into leading businesses based in the Czech Republic and Slovakia."
  },
  "investor_type": {
    "value": "pe",
    "source_url": "http://bensonoak.cz/",
    "quote": "Benson Oak is the exclusive advisor to Benson Oak Capital Cooperatif U.A., a buy-out and growth equity firm investing into leading businesses based in the Czech Republic and Slovakia."
  },
  "stages": {
    "value": ["growth", "
… [skrátené, 2468 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c044.json (file state is current in your context — no need to Read it back)
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://dev.globalprivatecapital.org/newsroom/benson-oak-fully-exits-eastern-european-online-broker-klikpojisteni-cz-to-ta-associates-and-mci-euroventures-backed-netrisk/" "inception|2011|May" | head; python3 -I fetch.py "https://lifeinsuranceinternational.com/news/benson-oak-divests-entire-stake-in-online-insurance-broker-klik" "inception|2011" | head
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
.venv/bin/python -I - <<'EOF'
import json
p="research/c044.json"; d=json.load(open(p))
d["investments"]=[]
d["notes"]="Website is stale (newest press release 2012) and its HTTPS certificate is invalid, so the http URL is used. Newest found activity is the May 2020 exit from Klikpojisteni.cz (funded since 2011, per lupa.cz 2020-05-21); no new investments found since then, likely inactive. Strategy page states controlling stakes of EUR 5-30 million, homepage EUR 5-15 million."
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c044.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c044.json
```

<details><summary>Výstup nástroja</summary>

```
c044 entity_kind: OK
c044 investor_type: OK
c044 stages: OK
c044 ticket_min: OK
c044 ticket_max: OK
OK    research/c044.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"BHS private equity fund\" OR \"BHS Private Equity\" Slovensko fond investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""BHS private equity fund" OR "BHS Private Equity" Slovensko fond investícia"

Links: [{"title":"bhs fund","url":"https://app.mergerlinks.com/service-providers/bhs-fund"},{"title":"Středa 05. srpna 2026 00:47","url":"https://www.fxstreet.cz/klicova-slova+bhs-private-equity-fund.html"},{"title":"bhs fund","url":"https://app.mergerlinks.com/companies/bhs-fund"},{"title":"dva fondy zabalily unipap","url":"https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/dva-fondy-zabalily-unipap.html"},{"title":"bhs acquires dck holoubkov bohemia","url":"https://www.unquote.com/cee/official-record/3018072/bhs-acquires-dck-holoubkov-bohemia"},{"title":"you are being redirected","url":"https://www.schoenherr.eu/content/czech-republic-schoenherr-advises-bhs-private-equity-fund-on-acquisition-of-alfa-3"},{"title":"9021 jsk and havel partners advises on bhs acquisition of boco pardubice machines","url":"https://www.ceelegalmatters.com/czech-republic/9021-jsk-and-havel-partners-advises-on-bhs-acquisition-of-boco-pardubice-machines"},{"title":"24565 schoenherr and cms advise on bhs private equity fund acquisition of altran","url":"https://mail.ceelegalmatters.com/schoenherr/24565-schoenherr-and-cms-advise-on-bhs-private-equity-fund-acquisition-of-altran"},{"title":"24565 schoenherr and cms advise on bhs private equity fund acquisition of altran","url":"https://ceelegalmatters.com/cms/24565-schoenherr-and-cms-advise-on-bhs-private-equity-fund-acqu
… [skrátené, 3933 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/dva-fondy-zabalily-unipap.html" "BHS|UNIPAP|miliard|2025" | head -20; echo XXX; curl -sIL --max-time 15 https://www.bhs.cz | grep -iE "^(HTTP|location)"; curl -sIL --max-time 15 https://www.bhsfund.cz | grep -iE "^(HTTP|location)"
```

<details><summary>Výstup nástroja</summary>

```
>> Two funds wrapped up UNIPAP | M&A Port | Deloitte Czech Republic
>> 24 Sep 2025
>> Two funds wrapped up UNIPAP
>> Czech private equity funds MAM and BHS have acquired the industrial paper packaging manufacturer.
>> The Belgian group Van de Velde Packaging is selling UNIPAP after three years. The company will be split evenly between BHS Private Equity Fund and MAM Private Equity Fund. The Pardubice-based business employs 140 people and last year generated nearly CZK 550 million in revenue from corrugated cardboard packaging for more than dozen industries with EBITDA amounting to CZK 90 million. The exact transaction price has not been disclosed, and completion is subject to approval by the Office for the Protection of Competition.
>> BHS Private Equity Fund, advised by Versute Investments, manages assets worth CZK 1.5 billion. It focuses on small and medium-sized enterprises in the Czech Republic and Slovakia and holds stakes, among others, in the metallurgical company Gevorkyan and parcel locker manufacturer ALFA 3.
XXX
HTTP/1.1 200 OK
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.bhs.cz https://www.versute.cz https://www.bhsfund.cz https://bhspe.cz; do echo "== $u"; curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" --max-time 15 $u; done; N=3000 python3 -I fetch.py https://www.bhs.cz
```

<details><summary>Výstup nástroja</summary>

```
== https://www.bhs.cz
200 https://www.bhs.cz/
== https://www.versute.cz
200 https://versute.cz/cs_cz/
== https://www.bhsfund.cz
000 https://www.bhsfund.cz/
== https://bhspe.cz
000 https://bhspe.cz/

 Široké portfolio a osobní přístup. | BH Securities
BH Securities
 Akcie
 Fondy
 Zpět
 Nemovitostní fond
 Konzervativní sektor ekonomiky určený pro investory, kteří ocení aktiva, na které si lze sáhnout a preferují investice do prvotřídních komerčních nemovitostí, které generují výnos na základě dlouhodobého nájemného.
 Dynamický fond
 Investiční strategie fondu je zaměřená na taktickou alokaci aktiv v portfoliu, kdy investice směřují zejména do veřejně obchodovaných akcií globálních společností různého zaměření v různých třídách aktiv. Poměry jednotlivých tříd aktiv se dynamicky mění v závislosti na tržním vývoji.
 Dluhopisový fond
 Dluhový fond investuje do rozvoje jiných společností prostřednictvím jejich dluhového financování. Financované společnosti jsou zejména velké stabilní korporace s růstovým potenciálem.
 Fond ikonických automobilů
 Investice s vůní benzínu. Investice do ikonických automobilů představují alternativní možnost investic, kdy zhodnocení vložených prostředků je založeno na dlouhodobé hodnotě unikátních vozů světoznámých značek. Investice do tohoto fondu přináší svým investorům také exkluzivní automobilové zážitky.
 Energetický a bateriový fond
 Fond je svým zaměřením unikátním energetickým fondem na středoevropském trhu, který je otevřený kvalifikovaným inve
… [skrátené, 3198 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=4000 python3 -I fetch.py https://versute.cz/cs_cz/; curl -sL https://versute.cz/cs_cz/ | grep -oE 'href="[^"]+"' | sort -u | head -40
```

<details><summary>Výstup nástroja</summary>

```
 Versute Investments - Investiční a poradenská společnost
Úvod
Reference
Private Equity
Public Equity
Poradenství
Kontakt
English
Úvod
Reference
Private Equity
Public Equity
Poradenství
Kontakt
English
Versute Investments 
 Versute Investments je investiční a poradenská společnost působící jako manažer Private Equity fondů zejména v segmentu malých a středních podniků. 
 Ozvěte se nám 
 jsme 
Private Equity 
 Investujeme do malých a středních podniků prostřednictvím Private Equity fondů. 
 Více informací 
Public Equity 
 Pomáháme společnostem s primární veřejnou nabídkou akcií na burze (IPO) 
 Více informací 
Poradenství 
 Pomáháme společnostem v oblasti podnikových financí. 
 Více informací 
Jsme řádným členem
Jsme oficiálním poradcem na trhu PX START
O nás
Jsme investiční a poradenskou společností působící jako manažer Private Equity fondů investujících zejména do malých a středních podniků. Investujeme rovněž vlastní kapitál formou co-investic a aktivně řídíme portfoliové společnosti fondů.
Působíme i jako poradce pro IPO (vstup na burzu) a pro podnikové finance.
V současné době jsme manažerem (General Partnerem) VERSUTE Funds SICAV a.s..
Hlavní činnosti
Stavíme na třech pilířích
Private Equity
Investujeme do malých a středních podniků prostřednictvím Private Equity fondů. V současné době jsme manažerem (General Partnerem) fondu VERSUTE Private Equity Fund Otevřený.
Více informací
Public Equity
Pomáháme společnostem s primární veřejnou nabídkou akcií na burze (IPO). Jsme o
… [skrátené, 6620 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://versute.cz/cs_cz/sluzby/private-equity/ | sed -n '15,80p'
```

<details><summary>Výstup nástroja</summary>

```
Kontakt
English
PRIVATE EQUITY
Investujeme do malých a středních podniků prostřednictvím Private Equity fondů. V současné době jsme manažerem (General Partnerem) fondu VERSUTE Private Equity Fund Otevřený.
VERSUTE Private Equity Fund Otevřený
Geografická působnost
Zaměření primárně na společnosti v České republice a na Slovensku, které mají potenciál být nebo již jsou přítomny na zahraničních trzích.
Sektor ekonomiky
Fokus na podniky ve všech odvětvích, avšak s primárním zaměřením na odvětví tradiční ekonomiky. Zde má tým společnosti největší zkušenosti.
Velikost podniků
Zaměření na rozvinuté a profitabilní malé a střední podniky s osvědčeným podnikatelským modelem a velkým růstovým a inovačním potenciálem.
Růstový kapitál
Tato forma investice eliminuje odčerpávání finančních prostředků na splácení a obsluhu dluhů a maximum prostředků tak může být investováno do růstových příležitostí.
Odkupy na finanční páku
Versute Investments hledá stabilní, zdravé podniky se silným cash flow, jejichž odkupy lze financovat kombinací vlastního kapitálu a bankovního financování. Splácení akvizičního dluhu ze zdrojů generovaných nakoupeným podnikem je pak jeden z faktorů, kterým se zvyšuje hodnota akcionářských podílů.
Manažerské odkupy
Mnoho vlastníků, kteří založili své podniky v první polovině 90. let, řeší nástupnickou otázku. Investice do manažerských odkupů umožnují stávajícím manažerům získat vlastnický podíl a silně je tak motivovat na dalším rozvoji těchto podniků.
MBIs
V ČR existují
… [skrátené, 2779 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://forbes.cz/doruceno-versute-investments-vstupuje-do-ceskeho-vyrobce-vydejnich-boxu-alfa-3/ "BHS|ALFA 3|Versute|2025" | head -15
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in "https://www.schoenherr.eu/content/czech-republic-schoenherr-advises-bhs-private-equity-fund-on-acquisition-of-alfa-3" "https://ceelegalmatters.com/cms/24565-schoenherr-and-cms-advise-on-bhs-private-equity-fund-acquisition-of-altran"; do echo "== $u"; python3 -I fetch.py "$u" "BHS|ALFA|Altran|20[12][0-9]" | head -12; done
```

<details><summary>Výstup nástroja</summary>

```
== https://www.schoenherr.eu/content/czech-republic-schoenherr-advises-bhs-private-equity-fund-on-acquisition-of-alfa-3
>> Czech Republic: Schoenherr advises BHS Private Equity Fund on acquisition of ALFA 3
>> 26 November 2025
>> Czech Republic: Schoenherr advises BHS Private Equity Fund on acquisition of ALFA 3
>> Schoenherr advised BHS Private Equity Fund and its professional advisor Versute Investments a.s. on the acquisition of a significant minority stake in ALFA 3, s.r.o. ("ALFA 3"), a leading Czech manufacturer of delivery boxes and other industrial metal furniture.
>> "It was our pleasure to assist BHS Private Equity Fund and Versute Investments on this acquisition, which represents another milestone in the expansion of the fund portfolio," said counsel Michal Jendželovský, who led the Schoenherr team. "We are grateful that BHS Private Equity has again put their trust in us – our team is always up for the challenge of delivering on a full-fledged transaction involving multiple parties and a financing provider, such as this one."
>> "We are proud to partner with ALFA 3, a company with a solid foundation and long-term potential in its sector. This investment aligns well with our strategy of supporting resilient, growing SMEs. Our appreciation goes to Schoenherr and Michal Jendželovský for their first-class legal assistance," said Luděk Palata, partner at Versute Investments a.s.
>> BHS Private Equity Fund, whose professional advisor (general partner) is Versute Investme
… [skrátené, 2456 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c045.json`
```
{
  "candidate_id": "c045",
  "name": "BHS private equity fund",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK"],
  "website": "https://versute.cz/cs_cz/sluzby/private-equity/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.schoenherr.eu/content/czech-republic-schoenherr-advises-bhs-private-equity-fund-on-acquisition-of-alfa-3",
    "source_date": "2025-11-26",
    "quote": "BHS Private Equity Fund, whose professional advisor (general partner) is Versute Investments a.s., is a sub-fund of BHS Fund II – Private Equity, an investment fund with variable capital, and focuses on investments in small and medium-sized enterprises in the Czech Republic and Slovakia."
  },
  "investor_type": {
    "value": "pe",
    "source_url": "
… [skrátené, 3382 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c045.json (file state is current in your context — no need to Read it back)
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "UNIPAP BHS Private Equity Fund MAM acquisition 2025 advise", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "UNIPAP BHS Private Equity Fund MAM acquisition 2025 advise"

Links: [{"title":"dva fondy zabalily unipap","url":"https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/dva-fondy-zabalily-unipap.html"},{"title":"Přejít na hlavní obsah","url":"https://kpmg.com/cz/cs/kontakty/k/lukas-kantor.html"},{"title":"latinlawyer.com","url":"https://latinlawyer.com/news?page=612"},{"title":"private equity fund in acquisition of management","url":"https://loeb.com/en/experience/private-equity-fund-in-acquisition-of-management__"},{"title":"private equity fund in acquisition of management","url":"https://www.loeb.com/zh-hans/experience/private-equity-fund-in-acquisition-of-management__"},{"title":"bma advise mpar on the acquisition of shares issued by multiplan","url":"https://thelatinamericanlawyer.com/bma-advise-mpar-on-the-acquisition-of-shares-issued-by-multiplan/"},{"title":"bclp advises mcwin capital partners on the acquisition of a majority stake in the big mamma group","url":"https://bclplaw.com/en-US/events-insights-news/bclp-advises-mcwin-capital-partners-on-the-acquisition-of-a-majority-stake-in-the-big-mamma-group.html"},{"title":"thelatinamericanlawyer.com","url":"https://thelatinamericanlawyer.com/tag/bma/page/5/"},{"title":"skip to main content","url":"https://paulweiss.com/practices/transactional/private-equity/news/apollo-funds-to-acquire-univar-solutions-in-81-billion-deal?id=46272"},{"title":"pp advised camano acquisition
… [skrátené, 2950 znakov]
```

</details>

**Nástroj `Bash`**

```bash
.venv/bin/python -I - <<'EOF'
import json
p="research/c045.json"; d=json.load(open(p))
d["investments"]=d["investments"][:1]
d["notes"]="Fund is advised/managed by Versute Investments a.s. (Prague); per a 2026 notice on versute.cz BHS Fund II was renamed to VERSUTE Funds SICAV. UNIPAP (50% with MAM, Deloitte 2025-09-24) and two 2026 entries on versute.cz (healthcare group, PRP) were not recorded because no single quotable sentence names both the fund and the company."
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c045.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c045.json
```

<details><summary>Výstup nástroja</summary>

```
c045 entity_kind: OK
c045 investor_type: OK
c045 sectors: OK
c045 stages: OK
c045 aum: OK
c045 inv0: OK
OK    research/c045.json
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://www.credoventures.com/; curl -sL https://www.credoventures.com/ | grep -oE 'href="[^"#]+"' | sort -u | head -40
```

<details><summary>Výstup nástroja</summary>

```
 Credo | We back the most ambitious founders from CEE. Pre-everything.
Portfolio
,
Team
,
Manifesto
,
Newsroom
Contact
Portfolio
,
Team
,
Manifesto
,
Newsroom
Contact
We back the most ambitious founders
from Central and Eastern Europe.
Pre-everything.
Pre-seed — Onwards. Leading rounds since ‘09.
Pre-seed — Onwards. Leading rounds since ‘09.
Before consensus.
Before consensus.
Before consensus.
Pre-seed — Onwards
Leading rounds since ‘09
Early × Underrated × Ridiculously ambitious × Built in CEE × Regional → Global × Technical builders × No shortcuts × High conviction × CEE diaspora × Against all odds × Leading pre-seeds × 100+ companies backed × 2 decacorns × 
Intro
(CV.)
Intro
(CV.)
The fund of choice for CEE founders around the world building generational companies. Having believed in the region's talent since 2009, we write the first check — before product, before revenue, often before a deck.
How we operate and invest:
● Backing exceptional people, not thesis-driven.
● Leading Pre-Seed rounds.
● $1M - $5M checks.
● From CEE, for CEE and its global diaspora.
● Working hands-on with no-BS technical founders.
Our manifesto
→
Our manifesto
→
In Numbers
(CV.)
5
5
5
5
Funds
17
17
17
17
Years on the market
100+
100+
100+
100+
Companies backed
2/2 CEE decacorns
2/2 CEE decacorns
2/2 CEE decacorns
2/2 CEE decacorns
First check
Portfolio
(CV.)
Highlights
Piotr & Mati
–01
ElevenLabs
Two best friends from Poland building in voice AI well before it became a category. Competing with 
… [skrátené, 5482 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://www.credoventures.com/newsroom | sed -n '15,120p'
```

<details><summary>Výstup nástroja</summary>

```
Oct
—’26
Spotlight
Vol./C2026
Supernova raises $9.2 million Series A to bring AI efficiency to enterprise product teams
Sep 30, 2025
 · Read ↗ 
Tech.eu
Headline leads Upheal's $10M Series A to help reduce provider burnout
Jan 25, 2025
 · Read ↗ 
Upheal
UK in-home healthcare provider Cera raises $150M to scale its AI platform
Jan 12, 2025
 · Read ↗ 
TechCrunch
Vlayer raises $10 million in pre-seed funding to build Ethereum's 'Solidity 2.0'
Nov 4, 2024
 · Read ↗ 
The Block
Supernova raises $9.2 million Series A to bring AI efficiency to enterprise product teams
Sep 30, 2025
 · Read ↗ 
Tech.eu
Headline leads Upheal's $10M Series A to help reduce provider burnout
Jan 25, 2025
 · Read ↗ 
Upheal
UK in-home healthcare provider Cera raises $150M to scale its AI platform
Jan 12, 2025
 · Read ↗ 
TechCrunch
Replika founder raises $20M pre-seed for Wabi, the 'YouTube of apps'
Nov 5, 2025
 · Read ↗ 
Forbes
Replika founder raises $20M pre-seed for Wabi, the 'YouTube of apps'
Nov 5, 2025
 · Read ↗ 
Forbes
Today, Oct 6
Today, Oct 6
Eastern-like Cloudy
Eastern-like Cloudy
CEE region
Not Real Forecast™
Investing appetite index
Investing appetite index
Trending up
Trending up
CEE region
Led by Credo
Latest
Resistant AI Raises $25M in Series B Funding to Empower AI Agents to Fight Fraud and Fincrime
Oct 14, 2025
 · Read ↗ 
The Recursive
Resistant AI Raises $25M in Series B Funding to Empower AI Agents to Fight Fraud and Fincrime
Oct 14, 2025
 · Read ↗ 
The Recursive
Supernova raises $9.2 million
… [skrátené, 2669 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Credo Ventures\" leads pre-seed 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Credo Ventures" leads pre-seed 2026"

Links: [{"title":"This article was published on March 23, 2026","url":"https://thenextweb.com/news/credo-ventures-88m-fund"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/credo-ventures"},{"title":"Credo Ventures Research","url":"https://f4.fund/firms/credo-ventures"},{"title":"9 Prague seed investors funding Czech tech startups in 2026","url":"https://www.ellty.com/investors/prague-seed-investors"},{"title":"Credo Ventures","url":"https://www.everythingstartups.com/vc-funds/credo-ventures"},{"title":"Credo Ventures lanza fondo de $88M para startups pre-seed en CEE","url":"https://ecosistemastartup.com/credo-ventures-lanza-fondo-de-88m-para-startups-pre-seed-en-cee/"},{"title":"Back to Credo Ventures","url":"https://seedtable.com/investors/credo-ventures/portfolio"},{"title":"Credo Ventures lanza fondo de $88M para startups pre-seed en CEE","url":"https://ecosistemastartup.com/?p=70677"},{"title":"credo ventures","url":"https://www.vcbacked.co/directory/investors/credo-ventures"}]

Credo Ventures closed a new pre-seed fund in March 2026, and one 2026 pre-seed deal shows up in the search results, though I found no complete list of its 2026 leads.

**The fund:** Credo closed an $88 million fund in a single closing, its largest to date, which follows a €75 million fund from 2022. The Prague and Krakow firm is doubling down on pre-seed in Central and Eastern Europe and its g
… [skrátené, 2689 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://thenextweb.com/news/credo-ventures-88m-fund "Credo|\\$|fund|March" | head -30
```

<details><summary>Výstup nástroja</summary>

```
>> Credo Ventures closes $88M fifth fund to stay the first cheque for CEE’s most ambitious founders
>> Investors and funding
>> This article was published on March 23, 2026
>> Investors and funding
>> Credo Ventures closes $88M fifth fund to stay the first cheque for CEE’s most ambitious founders
>> March 23, 2026 - 7:51 pm
>> Credit: Credo Ventures
>> The Prague and Krakow firm, whose earliest bets include UiPath and ElevenLabs, is doubling down on pre-seed in Central and Eastern Europe and its global diaspora, with a six-partner team and a $1–5M typical cheque.
>> Credo Ventures has closed Credo Stage 5, an $88 million fund raised in a single closing, continuing the Prague and Krakow firm’s fifteen-year strategy of writing the first institutional cheque for founders from Central and Eastern Europe and its diaspora.
>> The fund is the firm’s largest to date, stepping up from the €75 million fourth fund closed in 2022.
>> The firm’s founding partners Ondrej Bartos and Jan Habermann launched Credo in 2010 and have backed over 100 companies across four funds.
>> The two headline outcomes, UiPath, the Romanian-founded RPA platform that listed on the NYSE in 2021 at a $35 billion valuation, and ElevenLabs, the AI voice company most recently valued at $11 billion, are the cases Credo leads with, and with good reason: both were pre-seed investments led or co-led by the firm before either company was widely known. Maciek Gnutek, now a partner at Credo, was an early backer of ElevenL
… [skrátené, 3838 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Resistant AI $25M Series B Credo Ventures therecursive", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "SuperPlane pre-seed Credo Ventures 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "SuperPlane pre-seed Credo Ventures 2026"

Links: [{"title":"SuperPlane Raises 2.6M USD in Pre Seed Funding","url":"https://seedtable.com/companies/superplane/funding-rounds/pre-seed-2026-06"},{"title":"Investors Count","url":"https://www.cbinsights.com/company/superplane/financials"},{"title":"Subscribe to Our Newsletter","url":"https://thesaasnews.com/news/superplane-raises-2-28m-pre-seed"},{"title":"Venture-Backed Startups","url":"https://projectstartups.com/pages/pre-seed/"},{"title":"Venture-Backed Startups","url":"https://projectstartups.com/pages/ai-ml-pre-seed/"},{"title":"Founded Year","url":"https://www.cbinsights.com/company/superplane"},{"title":"Back to CredoChangelog and Sources","url":"https://seedtable.com/companies/credo/funding-rounds/seed-2022-03"},{"title":"Credo AI vs Safe Superintelligence","url":"https://neuronfeed.com/compare/credo-ai-vs-safe-superintelligence"},{"title":"series a 2023 02","url":"https://seedtable.com/companies/superplastic/funding-rounds/series-a-2023-02"}]

SuperPlane closed a pre-seed round led by Credo Ventures on June 24, 2026. The sources report the amount differently, and they disagree on where the company is based.

**Round details**
- One source describes a $2.6 million pre-seed round led by Credo Ventures. Another gives the same round as €2.28M in pre-seed funding, which is likely the same raise in a different currency.
- First Momentum Ventures and a group of angel investors also took part, incl
… [skrátené, 2500 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Resistant AI $25M Series B Credo Ventures therecursive"

Links: [{"title":"Aleš Ducháč","url":"https://cz.linkedin.com/in/duchaca"},{"title":"Show options","url":"https://www.legal500.com/firms/13416-weinhold-legal/c-czech-republic/news-and-developments/weinhold-legal-advises-resistant-ai-on-25m-series-b-funding-round-to-accelerate-financial-crime-prevention"},{"title":"ivan nikolajev 95a17891","url":"https://cz.linkedin.com/in/ivan-nikolajev-95a17891"},{"title":"siliconcanals.com","url":"https://siliconcanals.com/?p=70664"},{"title":"Resistant AI: $25 Million Series B Secured For Combating Financial Crimes","url":"https://pulse2.com/resistant-ai-25-million-series-b-secured-for-combating-financial-crimes/amp/"},{"title":"hyper.ai","url":"https://hyper.ai/en/stories/f6e9550dea92b4d90626da102b4ae69c"},{"title":"resistant ai secures 21 5m","url":"https://siliconcanals.com/resistant-ai-secures-21-5m/"},{"title":"Resistant AI raises $25 million","url":"https://coverager.com/resistant-ai-raises-25-million/"},{"title":"credo ventures","url":"https://www.vcbacked.co/directory/investors/credo-ventures"}]

The round was announced in October 2025. Resistant AI, a Prague-based fraud-prevention company, raised $25M in a Series B led by DTCP, and Credo Ventures is among its backers. I found no results for "therecursive," so I can't say what that term refers to.

**Round details**
- The round is reported as a $25 million Series B funding round, dated October 1
… [skrátené, 2713 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://thesaasnews.com/news/superplane-raises-2-28m-pre-seed "Credo|2026|June" | head; echo XX; python3 -I fetch.py https://www.legal500.com/firms/13416-weinhold-legal/c-czech-republic/news-and-developments/weinhold-legal-advises-resistant-ai-on-25m-series-b-funding-round-to-accelerate-financial-crime-prevention "Credo|2025" | head
```

<details><summary>Výstup nástroja</summary>

```
>> SuperPlane raises €2.28M in pre-seed funding led by Credo Ventures to build an open-source control plane for AI agents and production infrastructure.
>> June 24, 2026
>> The funding round was led by Credo Ventures, with participation from First Momentum Ventures. Additional angel investors included Stanislas Polu, CEO of Dust; Mirko Novakovic, CEO of Dash0; Tomas Kratky, Founder of Manta; and Andreas Klinger of Prototype Capital.
>> Funding Date: June 24, 2026
>> Lead Investor: Credo Ventures
>> June 24, 2026
>> October 09, 2026
>> October 09, 2026
>> October 08, 2026
>> October 06, 2026
XX
>> Weinhold Legal is proud to have advised to Resistant AI, a Czech-based fintech firm specializing in AI-powered fraud prevention, in its $25 million Series B funding round. Led by DTCP Growth, with continued support from Experian, Notion Capital, and GV (formerly Google Ventures), this round brings the total capital raised by the company to $53 million. Resistant AI is also supported by the local VC fund, Credo Ventures.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Wabi $20M pre-seed Eugenia Kuyda Credo Ventures", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Wabi $20M pre-seed Eugenia Kuyda Credo Ventures"

Links: [{"title":"- Founders' Daily Briefing","url":"https://founders-daily-briefing.beehiiv.com/p/wabi-raises-20m"},{"title":"Replika founder raises $20M pre-seed for Wabi, the ‘YouTube of apps’","url":"https://finance.yahoo.com/news/replika-founder-raises-20m-pre-170117656.html"},{"title":"Image Credits:Wabi","url":"https://techcrunch.com/2025/11/05/replika-founder-raises-20m-pre-seed-for-wabi-the-youtube-of-apps"},{"title":"Wabi, la ‘YouTube de Apps’, recauda $20M en ronda pre-semilla: un vistazo a su futura transformación","url":"https://ecosistemastartup.com/?p=49325"},{"title":"Fast company logo","url":"https://www.fastcompany.com/91550747/eugenia-kuyda"},{"title":"THE LATEST","url":"https://yespress.io/wabi"},{"title":"wabi raises 20m to become the youtube of apps","url":"https://varenyaz.com/wabi-raises-20m-to-become-the-youtube-of-apps/"},{"title":"Replika founder raises $20M pre-seed for Wabi, the ‘YouTube of apps’","url":"https://coworking.nanabianca.it/?p=754579"},{"title":"Artificial IntelligenceNewswireStartupsTechnology","url":"https://digitrendz.blog/?p=80475"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/wabi"}]

The search confirms the $20 million pre-seed round for Wabi, but none of the results mention Credo Ventures, so I can't verify that firm's involvement.

**The round:** TechCrunch reported that Wabi raised $20 million in pre-seed funding from angel in
… [skrátené, 2855 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Credo Ventures\" slovenský startup investícia 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Credo Ventures" slovenský startup investícia 2025 OR 2026"

Links: [{"title":"Credo ventures","url":"https://www.podnikajte.sk/temy/credo-ventures"},{"title":"server o českém Internetu","url":"https://www.lupa.cz/n/credo-ventures/"},{"title":"Credo Ventures chystají třetí fond. Investují s nimi zakladatelé Avastu i Karel Janeček","url":"https://www.e15.cz/byznys/credo-ventures-chystaji-treti-fond-investuji-s-nimi-zakladatele-avastu-i-karel-janecek-1343424"},{"title":"www.podnikajte.sk","url":"https://www.podnikajte.sk/clanky?page=721"},{"title":"startup a investor","url":"https://www.podnikajte.sk/temy/startup-a-investor?page=5"},{"title":"Další těžká váha na investičním poli. České Credo otevírá svůj třetí fond, ve kterém má pro startupy 2,5 miliardy korun","url":"https://cc.cz/dalsi-tezka-vaha-na-investicnim-poli-ceske-credo-otevira-svuj-treti-fond-ve-kterem-ma-pro-startupy-25-miliardy-korun/"},{"title":"financovanie podnikania","url":"https://www.podnikajte.sk/temy/financovanie-podnikania?page=17"},{"title":"zahajte fazi pet credo ventures maji paty fond za temer dve miliardy prim bude hrat mladi","url":"https://forbes.cz/zahajte-fazi-pet-credo-ventures-maji-paty-fond-za-temer-dve-miliardy-prim-bude-hrat-mladi/"},{"title":"Credo Ventures Research","url":"https://f4.fund/firms/credo-ventures"}]

I found no 2025 or 2026 investment by Credo Ventures in a Slovak startup in these results. The firm is Czech, and most of its recent activity is in C
… [skrátené, 3078 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Supernova $9.2 million Series A Credo Ventures tech.eu", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Supernova $9.2 million Series A Credo Ventures tech.eu"

Links: [{"title":"Get an email the moment Supernova.io Inc raises again","url":"https://seedtable.com/companies/supernovaio-inc/funding-rounds/series-a-2025-10"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/supernova-raises-9-2m-for-portal-platform"},{"title":"Nejdřív to s AI nevyšlo, teď je zde druhý pokus. Tchaj-wan poslal 200 milionů do českého startupu","url":"https://www.lupa.cz/aktuality/nejdriv-to-s-ai-nevyslo-ted-je-zde-druhy-pokus-tchaj-wan-poslal-200-milionu-do-ceskeho-startupu/"},{"title":"How Much Did Supernova.io Raise?","url":"https://www.zoominfo.com/financial/supernovaio-inc/465625016"},{"title":"Supernova: $9.2 Million Series A Closed For Bringing Vibe Coding To Product Teams","url":"https://pulse2.com/supernova-9-2-million-series-a-closed-for-bringing-vibe-coding-to-product-teams"},{"title":"Back to SupernovaChangelog and Sources","url":"https://seedtable.com/companies/supernova/funding-rounds/series-a-2025-10"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/supernova-studios/financials"},{"title":"CEE VC SUMMIT 2026","url":"https://vestbee.com/blog/articles/supernova-raises-9-2-m"},{"title":"Join Vestbee Summer Pitch CEE","url":"https://www.vestbee.com/insights/articles/supernova-raises-9-2-m"}]

The tech.eu article itself didn't come up in these results. The only trace of it is a headline in a SeedTable listing, so the details b
… [skrátené, 3409 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.vestbee.com/insights/articles/supernova-raises-9-2-m "Credo|2025" | head
```

<details><summary>Výstup nástroja</summary>

```
>> October 1, 2025·2 min read
>> The round also saw support from J&T Ventures, Reflex Capital, KAYA VC, Credo Ventures, EQT Ventures, Wing VC, and Y Combinator.
>> Deals#News#Czech RepublicOctober 1, 2025
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c046.json`
```
{
  "candidate_id": "c046",
  "name": "Credo Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "PL", "SK"],
  "website": "https://www.credoventures.com/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://thenextweb.com/news/credo-ventures-88m-fund",
    "source_date": "2026-03-23",
    "quote": "Credo Ventures has closed Credo Stage 5, an $88 million fund raised in a single closing, continuing the Prague and Krakow firm’s fifteen-year strategy of writing the first institutional cheque for founders from Central and Eastern Europe and its diaspora."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://thenextweb.com/news/credo-ventures-88m-fund",
    "source_date": "2026-03-23",
    "quote": "Credo Ventures ha
… [skrátené, 3552 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c046.json (file state is current in your context — no need to Read it back)
```

</details>

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c046.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c046.json
```

<details><summary>Výstup nástroja</summary>

```
c046 entity_kind: OK
c046 investor_type: OK
c046 sectors: OK
c046 stages: OK
c046 ticket_min: OK
c046 ticket_max: OK
c046 aum: OK
c046 inv0: OK
OK    research/c046.json
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://www.crowdberry.eu/ | head -120; curl -sL https://www.crowdberry.eu/ | grep -oE 'href="[^"#]+"' | sort -u | grep -v -E "\.(css|js|png|svg|ico)" | head -40
```

<details><summary>Výstup nástroja</summary>

```
Vercel Security Checkpoint
We're verifying your browser
Website owner? Click here to fix
Vercel Security Checkpoint
|
fra1::1791548721-eLv64E3Iq4JctUgLkgPSpIAbccsDOs0o

href="https://vercel.link/security-checkpoint"
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Crowdberry fond investícia 2025 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Crowdberry fond investícia 2025 2026"

Links: [{"title":"935083 slovaci zarobili na real estate takmer dvojnasobok cez crowdinvesticnu platformu spoluvlastnili komercne nehnutelnosti v trnave a nitre","url":"https://www.noviny.sk/pr-spravy/935083-slovaci-zarobili-na-real-estate-takmer-dvojnasobok-cez-crowdinvesticnu-platformu-spoluvlastnili-komercne-nehnutelnosti-v-trnave-a-nitre"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim","url":"https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/"},{"title":"Crowdberry predstavuje na Slovensku nový fond. Do slovenských a českých nehnuteľností chce investovať 30 miliónov eur","url":"https://www.startitup.sk/crowdberry-predstavuje-na-slovensku-novy-fond-do-slovenskych-a-ceskych-nehnutelnosti-chce-investovat-30-milionov-eur/"},{"title":"Lokální investování je na vzestupu, hlásí Crowdberry. Přes platformu a fondy loni proteklo přes 700 milionů","url":"https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/"},{"title":"Crowdberry predstavuje na Slovensku nový fond. Do slovenských a českých nehnuteľností chce investovať 30 miliónov eur","url":"https://www.startitup.sk/?p=475147"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/crowberry-capital"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim 2","ur
… [skrátené, 4045 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/" "Crowdberry|fond|20[12][0-9]" | head -40
```

<details><summary>Výstup nástroja</summary>

```
>> Přes platformu Crowdberry a fondy loni proteklo přes 700 milionů - CzechCrunch
>> Money Maker 2026
>> Investice – 30. 3. 2023 – 1 min čtení
>> Lokální investování je na vzestupu, hlásí Crowdberry. Přes platformu a fondy loni proteklo přes 700 milionů
>> Původem slovenské Crowdberry spravuje kapitál ve výši 2,4 miliardy korun. Jeho portfolio zahrnuje přes 70 společností a realitních projektů.
>> Foto: Crowdberry
>> Daniel Gašpar, partner investiční platformy Crowdberry
>> Daniel Gašpar, Michal Nešpor, Peter Bečár, Michal Ondrišek a Hynek Bartík. Pětice podnikatelských partnerů si klade za cíl investičně podporovat zejména menší a střední podniky včetně startupů „u sebe doma“, tedy na Slovensku a také v Česku. Jejich aktivity zastřešuje značka Crowdberry, pod kterou spadá investiční platforma a další tři fondy – a během posledních let pomohly k růstu více než sedmdesáti firmám.
>> „Namísto do akcií zahraničních firem chceme naučit Čechy a Slováky investovat do rychle rostoucích společností v našich končinách,“ říká Daniel Gašpar s tím, že přes investiční platformu Crowdberry se tento cíl pomalu daří naplňovat. Počet investorů loni vzrostl o více než tisícovku a celkem jich registruje přes šest tisíc.
>> Kromě investiční platformy Crowdberry provozuje tři dceřiné fondy – startupový CB Investment Management, nemovitostní CB Property Investors a CB ESPRI se zaměřením na organizace s pozitivním společenským dopadem. Poslední jmenovaný vznikl loni v květnu a podpořil jedenáct pro
… [skrátené, 3157 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0" https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/; python3 -I fetch.py https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/ "Crowdberry|miliard" | head
```

<details><summary>Výstup nástroja</summary>

```
200
>> Podíl u miliardáře. Jak se daří firmám, které se otevřely veřejným investicím? | Forbes
>> Daniel Gašpar z Crowdberry, foto Martin Svoboda
>> Podíl u miliardáře. Jak se daří firmám, které se otevřely veřejným investicím?
>> Skoro tři miliardy korun spravuje v českých a slovenských firmách investiční platforma Crowdberry, která během jedenácti let nabídla přímé majetkové podíly ve více než padesáti společnostech. Proč se firmy veřejným investicím otevírají a jak to zpětně hodnotí?
>> Až 37 milionů korun v několika fázích plánuje získat česko-slovenský výrobce ekologické drogerie Tierra Verde přes platformu Crowdberry. Podnik, ve kterém drží více než třetinový podíl i miliardář a majitel Kofoly Jannis Samaras s bývalou manželkou Zuzanou Samara, tak poprvé otvírá kapitál investorům z řad veřejnosti.
>> A to konkrétně přes platformu Crowdberry, jež funguje mezi Prahou a Bratislavou a propojuje veřejnost s firmami nabízejícími přímý majetkový podíl. Umožňuje tak investorům být skutečnými spoluvlastníky, nikoliv jen pasivními přispěvateli.
>> Je libo patro v mrakodrapu? Investiční platforma Crowdberry šlape do nemovitostí
>> Strach Evropanům zatemňuje mysl, říká Daniel Gašpar z platformy Crowdberry
>> Crowdberry zakládá nový nemovitostní fond. Povede ho člen představenstva CPI Sattar
>> „S Crowdberry jsme v kontaktu delší dobu, o jejím vstupu do firmy jsme vedli první rozhovory už před několika lety,“ říká spolumajitel Tierra Verde Tibor Schätzel, který platformu zná z dřívě
… [skrátené, 1559 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/ "202[3-6]" | head -8
```

**Nástroj `WebSearch`**

```json
{"query": "Crowdberry investuje startup 2025 kolo financovania fond CB", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
>> Říjen 2026
>> Říjen 2026
>> Listopad 2025
>> Září 2026
>> Říjen 2026
>> Říjen 2026
>> Říjen 2026
>> Říjen 2026
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Crowdberry investuje startup 2025 kolo financovania fond CB"

Links: [{"title":"Slovákom ukazujú ako investovať inak. Môžu sa stať bankármi","url":"https://www.noviny.sk/pr-spravy/893624-slovakom-ukazuju-ako-investovat-inak-mozu-sa-stat-bankarmi"},{"title":"Slovákom ukazujú ako investovať inak. Môžu sa stať bankármi","url":"https://sita.sk/slovakom-ukazuju-ako-investovat-inak-mozu-sa-stat-bankarmi/"},{"title":"Lokální investování je na vzestupu, hlásí Crowdberry. Přes platformu a fondy loni proteklo přes 700 milionů","url":"https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/"},{"title":"Na slovenské crowdfunding platformě Crowdberry se vybralo za půl roku přes 43 milionů Kč","url":"https://cc.cz/na-slovenske-crowdfunding-platforme-crowdberry-se-vybralo-za-pul-roku-pres-43-milionu-kc/"},{"title":"podil u miliardare jak se dari firmam ktere se otevrely verejnym investicim","url":"https://forbes.cz/podil-u-miliardare-jak-se-dari-firmam-ktere-se-otevrely-verejnym-investicim/"},{"title":"Slovenská sporiteľňa (","url":"https://sk.linkedin.com/in/peter-paska-756a4a8b"},{"title":"Slovákom ukazujú ako investovať inak. Môžu sa stať bankármi","url":"https://www.startitup.sk/slovakom-ukazuju-ako-investovat-inak-mozu-sa-stat-bankarmi/"},{"title":"je libo patro v mrakodrapu investicni platforma crowdberry slape do nemovitosti","url":"https://forbes.cz/je-libo-patro-v-mrakodrapu-investicni-platfor
… [skrátené, 3903 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"CB Investment Management\" Crowdberry startup investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""CB Investment Management" Crowdberry startup investícia"

Links: [{"title":"Lokální investování je na vzestupu, hlásí Crowdberry. Přes platformu a fondy loni proteklo přes 700 milionů","url":"https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/"},{"title":"Přes Crowdberry investoři za šest let poskytli startupům 780 milionů korun, teď samo získává desítky milionů","url":"https://cc.cz/pres-crowdberry-investori-za-sest-let-poskytli-startupum-780-milionu-korun-ted-samo-ziskava-desitky-milionu/"},{"title":"Na Slovensko prichádza nový investičný fond. Jeho objem bude takmer 12 miliónov eur","url":"https://www.startitup.sk/na-slovensko-prichadza-novy-investicny-fond-jeho-objem-bude-takmer-12-milionov-eur/"},{"title":"Description of the company","url":"https://www.profesia.sk/en/work/cb-investment-management/C238924"},{"title":"Crowdberry Overview","url":"https://pitchbook.com/profiles/advisor/175582-36"},{"title":"cb im","url":"https://village.ai/company/cb-im"},{"title":"CB Investment Management 41947","url":"https://contactout.io/company/CB-Investment-Management-41947"},{"title":"Tuzemské nemovitosti si zaslouží pozornost českých investorů","url":"https://www.e15.cz/magazin/tuzemske-nemovitosti-si-zaslouzi-pozornost-ceskych-investoru-1381569"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/cbim"},{"title":"Seco
… [skrátené, 4488 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://cbim.sk https://www.cbim.sk https://cbim.eu; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done; N=5000 python3 -I fetch.py https://www.cbim.sk/ | head -120
```

<details><summary>Výstup nástroja</summary>

```
https://cbim.sk 200 https://www.cbim.sk/
https://www.cbim.sk 200 https://www.cbim.sk/
https://cbim.eu 000 https://cbim.eu/

CB Investment Management — Získajte kapitál a znalosti | Venture Capital
top of page
Crowdberry
CB ESPRI
CB Property Investors
For Founders
Portfolio
Team
More
Use tab to navigate through the menu items.
Login
Innovate. Challenge. Grow.
We help you gain capital and know-how for your success.
Submit your pitch
Want to hear more? Sign up for our newsletter.
What are you looking for?
We believe that thriving startups and SMEs are the backbone of Europe’s future prosperity. Our vision is to become a growth catalyst.
Our goal is your success.
Experience
Capital
Network
Submit your pitch
About us
Since 2015, Crowdberry has been the driving force for investments in startups, SMEs, impact investing and real estate projects in Slovakia and Czechia. Our team has experience in finance management, investment banking and venture capital from all around the world.
​
CB Investment Management Growth One fund was founded in 2019 in order to help seed and pre-seed businesses based in Slovakia.
Meet the team
€23.2M
Fund size
32
Companies
2019
Founded
10
Years lifetime 
+ 3 years extension
Venture Stories
DNA ERA
The Slovak biotechnology company specializes in direct genetic analysis of DNA. Its technology can detect 74 carrier diseases and 34 health risks, as well as predispositions for certain sports and optimal nutrition. In 2021, DNA ERA received investment worth 250,
… [skrátené, 2433 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://www.cbim.sk/ | grep -oE 'href="https://www.cbim.sk[^"]*"' | sort -u; 
```

<details><summary>Výstup nástroja</summary>

```
href="https://www.cbim.sk"
href="https://www.cbim.sk/about"
href="https://www.cbim.sk/cs"
href="https://www.cbim.sk/de"
href="https://www.cbim.sk/_files/ugd/38d23d_742689bfbcc9497e9e23aa092712722a.pdf"
href="https://www.cbim.sk/_files/ugd/c6d8bc_73567defb4b7425b9c4c1d296b9a8c1c.pdf"
href="https://www.cbim.sk/founders"
href="https://www.cbim.sk/login"
href="https://www.cbim.sk/ourportfolio"
href="https://www.cbim.sk/sk"
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=6000 python3 -I fetch.py https://www.cbim.sk/founders | sed -n '10,80p'; echo XXXX; N=6000 python3 -I fetch.py https://www.cbim.sk/ourportfolio | sed -n '10,120p'
```

<details><summary>Výstup nástroja</summary>

```
More
Use tab to navigate through the menu items.
Login
What are you looking for?
Join forces with the largest growth capital investor in Slovakia.
We will help you achieve your goals.
How does it work?
Founder's journey
2
Jump-start a business
Get all the nuts and bolts ready. Verify your idea, design your prototype, and test the MVP. Do the financials. Write a kick-ass pitch deck and update your website.
Negotiate terms
We prepare a detailed overview of your company, valuation, and draft of the contract including terms and a business plans. Sign a contract and finalize formalities.
Enjoy support
Access resources for founders, consult strategy, meet our community and find synergies.
Submit a pitch
Once we receive your pitch, our investment team will get in touch and review your business plan.
Get Investment
Obtain fund tranches for your growth.
Dream bigger
We help you to achieve your financial goals. These may include exit, expansion, but also future rounds of funding.
1
2
3
4
5
4
I am ready
Find out more
What are we looking for?
Outstanding founders of seed and pre-seed businesses with a vision, innovative product, dynamic team, and daring business plan. 
Seed and
pre-seed stage
Up to 3 years of age or
5 years of age in Bratislava
Based in Slovakia
A registered business in Slovakia.
Innovative companies
Cutting-edge products, innovative services, breathtaking USPs, and ambitious business plans.
Submit your pitch
Special Perks for our Companies
Get access to a network of 6,
… [skrátené, 5821 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c047.json`
```
{
  "candidate_id": "c047",
  "name": "Crowdberry",
  "legal_name": "CB Investment Management s. r. o.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ"],
  "website": "https://www.cbim.sk/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.cbim.sk/",
    "quote": "CB Investment Management Growth One fund was founded in 2019 in order to help seed and pre-seed businesses based in Slovakia."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://cc.cz/lokalni-investovani-je-na-vzestupu-hlasi-crowdberry-pres-platformu-a-fondy-loni-proteklo-730-milionu/",
    "source_date": "2023-03-30",
    "quote": "Kromě investiční platformy Crowdberry provozuje tři dceřiné fondy – startupový CB Investment Management, nemovitostní CB Property Invest
… [skrátené, 1929 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c047.json (file state is current in your context — no need to Read it back)
```

</details>

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c047.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c047.json
```

<details><summary>Výstup nástroja</summary>

```
c047 entity_kind: OK
c047 investor_type: OK
c047 stages: OK
c047 inv0: OK
OK    research/c047.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"J&T ARCH INVESTMENTS\" fond investícia 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""J&T ARCH INVESTMENTS" fond investícia 2025"

Links: [{"title":"Buďte správne informovaný! Získajte prémiový účet TU","url":"https://podnikam.sk/?p=128591"},{"title":"Kam zajít, co ochutnat a co stojí za pozornost","url":"https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun"},{"title":"Anna Macaláková: J&T BANKA spravuje majetok klientov v objeme viac ako 5,1 miliardy eur","url":"https://www.startitup.sk/?p=1193716"},{"title":"jt arch investments bude prvym fondom s kontinualnym obchodovanim na prazskej burze 6584","url":"https://www.epravo.sk/top/aktualne/jt-arch-investments-bude-prvym-fondom-s-kontinualnym-obchodovanim-na-prazskej-burze-6584.html"},{"title":"dovera v partnerstvo ktora pretrvava napriec generaciami inzercia","url":"https://www.zakonypreludi.sk/blog/dovera-v-partnerstvo-ktora-pretrvava-napriec-generaciami-inzercia.htm"},{"title":"Buďte správne informovaný! Získajte prémiový účet TU","url":"https://podnikam.sk/?p=129203"},{"title":"investicie do private equity inzercia","url":"https://www.zakonypreludi.sk/blog/investicie-do-private-equity-inzercia.htm"},{"title":"investicie do private equity ponukaju potencial na dosahovanie dvojcifernych vynosov 6229","url":"https://www.epravo.sk/top/aktualne/investicie-do-private-equity-ponukaju-potencial-na-dosahovanie-dvojcifernych-vynosov-6229.html"},{"title":"fond arch sazi na velka jmena sympatie jsou pro investice klicove rika tomis","url":"ht
… [skrátené, 4936 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun" "Arch|miliard|investi|202[56]" | head -30
```

<details><summary>Výstup nástroja</summary>

```
>> J&T Arch dál roste. Majetek fondu přesáhl 200 miliard korun | Newstream
>> Miliardáři
>> J&T Arch dál roste. Majetek fondu přesáhl 200 miliard korun
>> J&T Arch dál roste. Majetek fondu přesáhl 200 miliard korun
>> 27. 3. 2026 15:24
>> Kombinace výnosů a nových investic vynesla fond J&T Arch na rekordní úroveň. Klíčovou roli sehrála energetika i bankovní sektor.
>> Aktiva pod správou fondu kvalifikovaných investorů J&T Arch Investments v roce 2025 stoupla o 81,4 miliardy korun na 202,9 miliardy korun. Akcie fondu v korunách se loni zhodnotily o 15,82 procenta a o 14,4 procenta v eurech. J&T Arch, který je největším investičním fondem v ČR a na Slovensku, to uvedl v tiskové zprávě.
>> Za růstem aktiv stojí kombinace zhodnocení portfolia a silného investorského zájmu v průběhu roku. „Rok 2025 byl pro J&T Arch výjimečný nejen z pohledu výkonnosti, ale i struktury portfolia. Zájem investorů v kombinaci s velmi solidním zhodnocením portfolia vyústil v rekordní meziroční nárůst aktiv,“ uvedl člen investičního výboru J&T Arch Adam Tomis.
>> Fond s ohledem na nastavené podmínky a dlouhodobý závazek zakladatelských rodin J&T držet přibližně polovinu kapitálu fondu přistoupil od 8. prosince 2025 k zavedení kapacitního poplatku, který omezil příliv nových investic. Ve čtvrtém čtvrtletí tak objem primárních úpisů dosáhl pouze 83 milionů korun.
>> Od začátku ledna je J&T Arch Investments jediným fondem na pražské burze, se kterým se obchoduje kontinuálně.
>> J&T Arch v závěru roku usku
… [skrátené, 5553 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "J&T Arch 500 milionů eur preferenční akcie EP Equity Investment", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "J&T Arch 500 milionů eur preferenční akcie EP Equity Investment"

Links: [{"title":"Spojenectví Tkáče, Křetínského i Komárka nese ovoce. Největší český fond už má přes 200 miliard","url":"https://cc.cz/spojenectvi-tkace-kretinskeho-i-komarka-nese-ovoce-nejvetsi-cesky-fond-uz-ma-pres-200-miliard/"},{"title":"Kam zajít, co ochutnat a co stojí za pozornost","url":"https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun"},{"title":"nejvetsi investicni fond u nas dal roste aktiva jt arch loni stoupla o 81 miliard","url":"https://forbes.cz/nejvetsi-investicni-fond-u-nas-dal-roste-aktiva-jt-arch-loni-stoupla-o-81-miliard/"},{"title":"sefove jt presouvaji penize do obriho investicniho fondu uz je v nem pres 45 miliard korun","url":"https://ekonomickydenik.cz/sefove-jt-presouvaji-penize-do-obriho-investicniho-fondu-uz-je-v-nem-pres-45-miliard-korun/"},{"title":"Byznys Tkáčových se opírá o největší fond kvalifikovaných investorů v Česku a na Slovensku","url":"https://www.e15.cz/tema/miliardari/byznys-tkacovych-se-opira-o-nejvetsi-fond-kvalifikovanych-investoru-v-cesku-a-na-slovensku-1427000"},{"title":"Tomáš Janoušek","url":"https://cz.linkedin.com/in/tomas-janousek"},{"title":"j t","url":"https://www.newstream.cz/stitek/j-t"},{"title":"About J&T Arch Investments","url":"https://www.cbinsights.com/company/jt-arch-investments"},{"title":"kkcg prodala jt arch investment minoritni podil v allwyn","url":"https://www.
… [skrátené, 3315 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.deloitte.com/cz-sk/en/mnaport/articles/clanky-transakce/2025-q3/kkcg-prodala-jt-arch-investment-minoritni-podil-v-allwyn.html" "Arch|Allwyn|202[56]" | head -12; echo XX; python3 -I fetch.py "https://cc.cz/spojenectvi-tkace-kretinskeho-i-komarka-nese-ovoce-nejvetsi-cesky-fond-uz-ma-pres-200-miliard/" "EPEI|EP Equity|Allwyn|2026" | head
```

<details><summary>Výstup nástroja</summary>

```
>> KKCG Sold a Minority Stake in Allwyn to J&T Arch Investment | M&A Port | Deloitte Czech Republic
>> 28 Aug 2025
>> KKCG Sold a Minority Stake in Allwyn to J&T Arch Investment
>> The largest Czech investment fund invested half a billion euros in Allwyn.
>> KKCG, an international investment group owned by Karel Komárek, sold a 4.27% stake in Allwyn to the Czech fund J&T Arch Investment for 500 million euros. The minority stake will be held through the newly established JTFG Fund IV SICAV, while the remaining 95% will continue to be owned by KKCG. Allwyn operates lotteries in the United States, the United Kingdom, the Czech Republic, Austria, and Greece. It also participates in the operation of the Italian lottery as part of a consortium.
>> J&T Arch Investment is the largest fund in the Czech Republic and Slovakia. It manages assets worth 5,5 billion euros and is traded on the Prague Stock Exchange. Its most significant asset is a minority stake in J&T Capital, which brings together holdings in joint investment projects, primarily in the energy sector, of J&T (Patrik Tkáč) and EP Group (Daniel Křetínský).
>> KKCG operates in more than 40 countries worldwide. In addition to Allwyn, it also owns the energy group MND, the IT services provider Avenga, and the real estate division KKCG Real Estate Group. The group generates an annual profit of more than 1.4 billion euros.
>> © 2026. See Terms of Use for more information.
XX
>> Money Maker 2026
>> Byznys – 29. 3. 2026 – 2 min čten
… [skrátené, 2694 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c048.json`
```
{
  "candidate_id": "c048",
  "name": "J&T ARCH Investments",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun",
    "source_date": "2026-03-27",
    "quote": "Fond investuje do podniků, projektů a partnerství, které skupina vybudovala v posledních 30 letech."
  },
  "investor_type": {
    "value": "pe",
    "source_url": "https://www.newstream.cz/zpravy-z-firem/j-t-arch-dal-roste-majetek-fondu-presahl-200-miliard-korun",
    "source_date": "2026-03-27",
    "quote": "J&T Arch Investments je hlavní investiční platformou skupiny J&T."
  },
  "aum": {
    "amount": 2029000000
… [skrátené, 2091 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c048.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c048.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c048.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c048 entity_kind: OK
c048 investor_type: OK
c048 aum: OK
c048 inv0: OK
OK    research/c048.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "ZAKA VC Slovakia venture capital investícia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "ZAKA VC Slovakia venture capital investícia"

Links: [{"title":"ZAKA VC Overview","url":"https://pitchbook.com/profiles/investor/493759-63"},{"title":"Get Free Access to The Founder's Handbook","url":"https://www.failory.com/blog/venture-capital-firms-slovakia"},{"title":"venture capital firms bratislava","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava.md"},{"title":"Velké startupové investice zamrzly a propouští se. Je to příležitost, říká Petrus ze Zaka VC","url":"https://www.e15.cz/byznys/technologie-a-media/velke-startupove-investice-zamrzly-a-propousti-se-je-to-prilezitost-rika-petrus-ze-zaka-vc-1396468"},{"title":"Blog9 Trailblazing Venture Capital Firms Powering Bratislava's Startup Surge","url":"https://www.papermark.com/blog/venture-capital-firms-bratislava"},{"title":"Investují jako na běžícím pásu. Česko-slovenský fond Zaka letos podpořil již dvacet startupů","url":"https://cc.cz/investuji-jako-na-bezicim-pasu-cesko-slovensky-fond-zaka-letos-podporil-jiz-dvacet-startupu/"},{"title":"Ján Búza zo ZAKA VC: Slovenský pôvod nie je v Silicon Valley prekážkou","url":"https://www.startitup.sk/?p=1130105"},{"title":"Czech VC single family office opens up to third-party investors","url":"https://familyofficehub.io/blog/czech-vc-single-family-office-opens-up-to-third-party-investors/"},{"title":"czech family office zaka vc news","url":"https://sifted.eu/articles/czech-family-office-zaka-vc-news"}]

ZAKA VC is a venture cap
… [skrátené, 3826 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=4000 python3 -I fetch.py https://www.zaka.vc/ | head -80; echo XXX; python3 -I fetch.py https://sifted.eu/articles/czech-family-office-zaka-vc-news "Zaka|€|fund|seed|2024" | head -20
```

<details><summary>Výstup nástroja</summary>

```
 ZAKA - ZAKA VC
 Skip to content
Home
About
Team
Portfolio
Co-Investors
News
Jobs
Contact
 Submit pitch deck
 Submit pitch deck
Home
About
Team
Portfolio
Co-Investors
News
Jobs
Contact
E-mail is copied
 Founders backed by entrepreneurs 
We are a seed & pre-seed VC fund, investing mainly in the US and Europe. Especially looking for startups in the Health & Biotech and Industrial Tech verticals.
Read our story 
97
Companies invested totally
5
Exits
1
Unicorn
17M
Current fund size
Fund size
Companies
Family office
5M
5M 
invested
34
Fund 1
17M
8M 
invested
46
One of the best Healthcare & Life Sciences portfolios in continental Europe.
 Check it out! 
 Sillicon Valley, London, Prague, Bratislava 
We seek entrepreneurs with global ambition wherever they are and support them by creating a bridge between North America and Europe.
Portfolio
Portfolio
Portfolio
There's already 97 companies across 5 continents that we believe in
 San Francisco, CA
United States 
WonderTx
Extrapolative AI to unlock first-in-class drugs
 Anywhere 
Is this you?
 Ann Arbor, MI
United States 
Aerogen Systems
Modernizing chip manufacturing infrastructure
 London
United Kingdom 
FinalDose
Programmable DNA drug destroying all cancers, unlocking 80% of targets
 San Francisco, CA
United States 
PerfectBit
Correct by construction training data for frontier AI labs
 Mountain View, CA
United States 
Human Archive
Human Archive builds human data archiving platform with comprehensive dataset for training embodied A
… [skrátené, 2727 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://www.zaka.vc/ | grep -oE 'href="https://www.zaka.vc/[^"]*"' | sort -u | head; N=5000 python3 -I fetch.py https://www.zaka.vc/news/ | sed -n '20,90p'
```

<details><summary>Výstup nástroja</summary>

```
Jobs
Contact
E-mail is copied
News
10/08/2026
 Zaka blog 
Read more
mRNA is still made the 1984 way. It was not built for the drugs coming next.
10/06/2026
 Press releases 
Read more
Sensible Biotechnologies raises $47M: why we backed them early, and why it’s personal for us
09/23/2026
 Zaka blog 
Read more
You choose the science. The disease chooses the bill.
09/22/2026
 LinkedIn 
Read more
Our Co-Founder and Managing Partner just landed on the Top 200 VC voices on LinkedIn, worldwide 📢
09/18/2026
 LinkedIn 
Read more
Sutro just got acquired by Lovable 💜
09/14/2026
 LinkedIn 
Read more
📍 Where you build matters almost as much as what you build. Our portfolio company Sygaldry chose to headquarter in Ann Arbor, Michigan – and co-founder Idalia Friedson recently wrote about why.
09/08/2026
 Zaka blog 
Read more
We now design more drugs than we can test
08/31/2026
 LinkedIn 
Read more
⏰ LAST CALL for applicationsBuilding a startup and looking for the right people to help you grow? 🚀 Applications for the next AceON Accelerator batch are open until September 3.
08/24/2026
 Zaka blog 
Read more
Nobody at a frontier lab is working on your disease
08/18/2026
 Press releases 
Read more
PerfectBit: Building the Verified Data Layer for Physical AI
08/11/2026
 Zaka blog 
Read more
The moat decides whether you can play. The asset decides whether you get paid.
08/07/2026
 LinkedIn 
Read more
BUILDING BETTER PRECLINICAL PREDICTIONS 🔬This week, our portfolio company Olio Labs introduced its 
… [skrátené, 2178 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://www.zaka.vc/news/ | grep -oE 'href="[^"]*(sensible|perfectbit)[^"]*"' | sort -u
```

<details><summary>Výstup nástroja</summary>

```
href="https://zaka.vc/perfectbit-building-the-verified-data-layer-for-physical-ai/"
href="https://zaka.vc/sensible-biotechnologies-raises-47m-why-we-backed-them-early-and-why-its-personal-for-us/"
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://zaka.vc/perfectbit-building-the-verified-data-layer-for-physical-ai/ "ZAKA|Zaka|invest|led|round|2026" | head -20; echo XXX; python3 -I fetch.py https://zaka.vc/sensible-biotechnologies-raises-47m-why-we-backed-them-early-and-why-its-personal-for-us/ "ZAKA|Zaka|invest|backed|2026|Slovak" | head -20
```

<details><summary>Výstup nástroja</summary>

```
>> PerfectBit: Building the Verified Data Layer for Physical AI - ZAKA VC
>> Co-Investors
>> Co-Investors
>> For years, the conversation around artificial intelligence revolved around larger models and more compute. Today, a different constraint is becoming increasingly visible: data.
>> PerfectBit, a San Francisco startup that recently graduated from Y Combinator’s Spring 2026 batch, develops verified multimodal datasets and reinforcement learning environments for frontier AI models. Rather than relying on traditional human annotation, the company generates synthetic environments in which every training example can be validated against a known ground truth.
>> Jan Kasper, Managing Partner at ZAKA VC
>> Why we invested
>> The funding round was oversubscribed and included Y Combinator, alongside angel investors from OpenAI, Anthropic, DeepMind and Meta.
>> [email]
>> Co-Investors
>> [email]
XXX
>> Sensible Biotechnologies raises $47M: why we backed them early, and why it's personal for us - ZAKA VC
>> Co-Investors
>> Co-Investors
>> Sensible Biotechnologies raises $47M: why we backed them early, and why it’s personal for us
>> Today, Sensible Biotechnologies announced $47 million in financing to scale its platform for making mRNA in living cells. The financing includes a Series A led by Oxford Science Enterprises and up to $20 million in non-dilutive funding from the Government of Slovakia and the European Union.
>> New institutional investors OTB Ventures and In-Q-Tel
… [skrátené, 4470 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"ZAKA VC\" pre-seed round 2026 raises", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""ZAKA VC" pre-seed round 2026 raises"

Links: [{"title":"ZAKA VC Research","url":"https://f4.fund/firms/zaka-vc"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/zaka"},{"title":"ZAKA VC Activity","url":"https://f4.fund/firms/zaka-vc/activity"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/zaka-ventures"},{"title":"therecursive.com","url":"https://therecursive.com/?p=38085"},{"title":"- The Bridge Club","url":"https://thebridgeclub.beehiiv.com/p/zaka-launches-15m-venture-fund"},{"title":"altss.com","url":"https://altss.com/profile/zaka.md"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/note/zaka-vc-launches-15m-fund"},{"title":"ZAKA unveils €15M 'Fund I'","url":"https://tech.eu/2024/07/19/zaka-unveils-its-fund-i-15m-for-bridging-the-us-with-the-eu-market/"}]

I found no evidence that ZAKA VC raised a pre-seed round in 2026. The results describe ZAKA as an investor, not a company that raised money. Its 2026 activity consists of co-investing in other startups' rounds.

**What ZAKA did in 2026:** Its investment list shows co-investor roles in ParcelBio (May 2026, seed), HexemBio (April 2026, seed), Ateios Systems (March 2026, Series A), Sygaldry Technologies (March 2026, Series A), and Readmio (February 2026, seed). A separate profile notes that ZAKA backed DeepSeq.AI, which uses functional AI for protein drug discovery, 
… [skrátené, 2503 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Readmio investice ZAKA 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Readmio investice ZAKA 2026"

Links: [{"title":"«БЖЗҚ» АҚ 2026 жылдың 1 сәуіріндегі жағдай бойынша зейнетақы жинақтарын инвестициялау есебін ұсынады","url":"https://www.gov.kz/memleket/entities/almobl-ile/press/news/details/1213293"},{"title":"is.cevro.cz","url":"https://is.cevro.cz/publication/55786/en/Jake-investicni-tema-povazujete-pro-rok-2026-za-nejperspektivnejsi-a-proc/Krasnicka"},{"title":"03 rješenje zbi za osnivanje ucits podfonda zb bond 2026 eur iii objava","url":"https://www.hanfa.hr/media/pcwmjpu4/03-rješenje-zbi-za-osnivanje-ucits-podfonda-zb-bond-2026-eur-iii_objava.pdf"},{"title":"best stocks to invest in 2026 d7617","url":"https://sainikschoolrewa.ac.in/economy-desk/best-stocks-to-invest-in-2026-d7617.php"},{"title":"«БЖЗҚ» АҚ 2026 жылдың 1 сәуіріндегі жағдай бойынша зейнетақы жинақтарын инвестициялау есебін ұсынады","url":"https://www.gov.kz/memleket/entities/vko-kurchum/press/news/details/1210075?lang=kk"},{"title":"Buscar Investimentos","url":"https://www.meelion.com/renda-fixa/comparar-investimentos/cra/emissor-zamp/cdi/"},{"title":"Buscar Investimentos","url":"https://www.meelion.com/renda-fixa/comparar-investimentos/emissor-zema-financeira/"},{"title":"4e3b9f66 46c4 4d6d b45f d4ed11d25491","url":"https://www.gov.me/en/documents/4e3b9f66-46c4-4d6d-b45f-d4ed11d25491"},{"title":"«БЖЗҚ» АҚ 2026 жылдың 1 сәуіріндегі жағдай бойынша зейнетақы жинақтарын инвестициялау есебін ұсынады","url":"https://www.gov.kz/memleket/entities/vk
… [skrátené, 2699 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Ateios Systems $7.25M Series A ZAKA", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Ateios Systems $7.25M Series A ZAKA"

Links: [{"title":"ZAKA VC Activity","url":"https://f4.fund/firms/zaka-vc/activity"},{"title":"Atego Systems","url":"https://startups.one.gob.es/companies/atego_systems"},{"title":"Ateios Systems and Ubicept Selected As First-Round Picks in Inaugural TitletownTech Startup Draft","url":"https://innovationcrossroads.ornl.gov/?p=1294"},{"title":"ateios ateios com funding","url":"https://fundediq.co/ateios-ateios-com-funding/"},{"title":"meet siete ateios systems and generation girl hackernoon startups of the week","url":"https://hackernoon.com/lang/sq/meet-siete-ateios-systems-and-generation-girl-hackernoon-startups-of-the-week"},{"title":"zaka vc","url":"https://www.vcbacked.co/directory/investors/zaka-vc"},{"title":"finance.walla.co.il","url":"https://finance.walla.co.il/item/3454058"},{"title":"DiscoverStartupsZaka-Powering ProductSpot & iHeartLocal.Zaka-Powering ProductSpot & iHeartLocal. People","url":"https://wellfound.com/company/zaka-2/people"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/n-technologies/financials"}]

The search confirms the core claim: ZAKA VC took part in a Series A for Ateios, though one source gives a slightly different amount.

- **Round and investor:** F4's ZAKA VC activity page says ZAKA participated in Ateios Systems' $7.25M Series A for flexible battery electrode manufacturing.
- **Amount and date:** FundedIQ lists the latest round as a Series A of $7.3M dat
… [skrátené, 2450 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://tech.eu/2024/07/19/zaka-unveils-its-fund-i-15m-for-bridging-the-us-with-the-eu-market/ "ZAKA|€|ticket|seed|health|B2B" | head -20; echo XXX; python3 -I fetch.py https://cc.cz/investuji-jako-na-bezicim-pasu-cesko-slovensky-fond-zaka-letos-podporil-jiz-dvacet-startupu/ "Zaka|20[12][0-9]" | head -20
```

<details><summary>Výstup nástroja</summary>

```
>> ZAKA unveils €15M 'Fund I' - Tech.eu
>> Healthtech
>> Healthtech
>> Spanish Autentic AI raises €1.5M to accelerate AI-powered market research
>> European startups raise €15.8B in September, nearly five times August's total
>> Funding dips, but fundamentals hold: European tech raises €7.5B in March
>> February funding rebounds to €7.8B as UK startups capture the lion’s share of European capital
>> ZAKA unveils €15M 'Fund I'
>> ZAKA wants to fund CEE-based teams with the ambition to scale to the US. The fund has closed its first round at €10.5M
>> Prague and London-based ZAKA VC has established its first fund sized €15M and ready to support early-stage startups in the US and EU.
>> Founded in 2020 by seasoned entrepreneurs Jan Kasper and Peter Zalesak, ZAKA VC has started as a family office investing purely private money in pre-seed and seed startups. Since then, they have grown into a team of 6 core members, with more than 55 invested companies worldwide in their portfolio and over €11M invested. Previous investments include ExcepGen, Sensible Biotechnologies, Miros.ai, Supliful, Lime Therapeutics and Webel.
>> Originally, ZAKA VC primarily focused on its domestic CEE market but over time, it expanded its presence to the UK and US. Unlike most of CEE based funds, ZAKA’s focus is to explore and fund the European diaspora in US, US-based teams, or CEE-based teams with the ambition to scale to the US.
>> The demand from external investors to co-invest alongside ZAKA led to cre
… [skrátené, 5493 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://zaka.vc/perfectbit-building-the-verified-data-layer-for-physical-ai/ "PerfectBit" ; curl -sL https://www.zaka.vc/news/ | grep -oE 'href="https://zaka.vc/[^"]*"' | sort -u | head -60
```

<details><summary>Výstup nástroja</summary>

```
>> PerfectBit: Building the Verified Data Layer for Physical AI - ZAKA VC
>> PerfectBit: Building the Verified Data Layer for Physical AI
>> This is the problem PerfectBit is solving.
>> PerfectBit, a San Francisco startup that recently graduated from Y Combinator’s Spring 2026 batch, develops verified multimodal datasets and reinforcement learning environments for frontier AI models. Rather than relying on traditional human annotation, the company generates synthetic environments in which every training example can be validated against a known ground truth.
>> The company’s approach is what the founders describe as “correct by construction.” Instead of asking humans to determine whether an answer is correct, PerfectBit creates simulation environments where correctness is built directly into the data generation process. The output includes aligned multimodal signals—including RGB video, depth maps and segmentation data—that are exact in simulation but difficult to obtain consistently from real-world data.
>> Rather than building another foundation model, PerfectBit focuses on a different layer of the AI stack.
>> The company’s datasets and reinforcement learning environments are designed to work independently of a particular model architecture. As new AI architectures emerge, the need for reliable, verifiable training data remains. By focusing on this layer of the stack, PerfectBit is developing infrastructure that can support a wide range of AI systems rather than a single m
… [skrátené, 7058 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://zaka.vc/sygaldry-backed-by-zaka-vc-raises-139m-to-build-quantum-accelerated-ai-infrastructure/ https://zaka.vc/zaka-vc-invests-in-cirrus-therapeutics-to-advance-gene-therapies-for-blinding-eye-diseases/ https://zaka.vc/zaka-vc-invests-in-eigen-therapeutics-accelerating-precision-cancer-treatment-with-vision-and-speed/; do echo "== $u"; python3 -I fetch.py "$u" "ZAKA" "20[22][0-9]" | head -8; done
```

<details><summary>Výstup nástroja</summary>

```
== https://zaka.vc/sygaldry-backed-by-zaka-vc-raises-139m-to-build-quantum-accelerated-ai-infrastructure/
>> Sygaldry, backed by ZAKA VC, raises $139M to build quantum-accelerated AI infrastructure - ZAKA VC
>> Sygaldry, backed by ZAKA VC, raises $139M to build quantum-accelerated AI infrastructure
>> ZAKA VC first invested in Sygaldry through Fund I in June 2025, shortly after the company emerged from the Y Combinator Spring 2025 batch, and also participated in the Series A round announced this month — less than a year after the initial investment, reflecting both strong execution and the urgency of the problem the company is addressing.
>> “The team is focused on a real bottleneck in AI, executing really well, and operating in a massive market. That’s exactly the kind of company we want to back,” said Jan Kasper, Co-Founder and Managing Partner at ZAKA VC.
>> [email]
>> [email]
>> ZAKA VC first invested in Sygaldry through Fund I in June 2025, shortly after the company emerged from the Y Combinator Spring 2025 batch, and also participated in the Series A round announced this month — less than a year after the initial investment, reflecting both strong execution and the urgency of the problem the company is addressing.
== https://zaka.vc/zaka-vc-invests-in-cirrus-therapeutics-to-advance-gene-therapies-for-blinding-eye-diseases/
>> ZAKA VC Invests in Cirrus Therapeutics to Advance Gene Therapies for Blinding Eye Diseases - ZAKA VC
>> ZAKA VC Invests in Cirrus Therapeu
… [skrátené, 3976 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I -c "
import sys; sys.path.insert(0,'.')
from fetch import text_of
t=text_of('https://www.zaka.vc/news/').split('\n')
for i,l in enumerate(t):
    if any(k in l for k in ('Sygaldry','Cirrus','Eigen')): print(t[i-4:i+1])
"; curl -sL https://zaka.vc/sygaldry-backed-by-zaka-vc-raises-139m-to-build-quantum-accelerated-ai-infrastructure/ | grep -oE '"datePublished":"[^"]+"|article:published_time" content="[^"]+"' | head -2; curl -sL https://zaka.vc/zaka-vc-invests-in-cirrus-therapeutics-to-advance-gene-therapies-for-blinding-eye-diseases/ | grep -oE '"datePublished":"[^"]+"|article:published_time" content="[^"]+"' | head -2
```

<details><summary>Výstup nástroja</summary>

```
['Sutro just got acquired by Lovable 💜', '09/14/2026', ' LinkedIn ', 'Read more', '📍 Where you build matters almost as much as what you build. Our portfolio company Sygaldry chose to headquarter in Ann Arbor, Michigan – and co-founder Idalia Friedson recently wrote about why.']
['BUILDING BETTER PRECLINICAL PREDICTIONS 🔬This week, our portfolio company Olio Labs introduced its in vivo platform designed to predict human clinical outcomes earlier in the drug discovery process.', '08/05/2026', ' LinkedIn ', 'Read more', 'Our portfolio company Cirrus Therapeutics has welcomed Coronet Ventures to its investor syndicate. 🤝']
['⏳ 1 WEEK TO GO | On April 28, we’re bringing the Venture Mindset to Bratislava. Free to attend, registration required. Save your spot now', '04/15/2026', ' Press releases ', 'Read more', 'Sygaldry, backed by ZAKA VC, raises $139M to build quantum-accelerated AI infrastructure']
['🚀 What does it really take to get into Y Combinator — and build a venture-backed biotech company from Europe? (conversation with our portfolio founder Miroslav Gasparek, CEO & co-founder of Sensible Biotechnologies)', '02/05/2026', ' Press releases ', 'Read more', 'ZAKA VC Invests in Cirrus Therapeutics to Advance Gene Therapies for Blinding Eye Diseases']
['🌟 Continuing our spotlight on startups from Y Combinator’s Spring 2025 batch that we’re proud to have backed — today we’re featuring Bluejay (YC X25) 🐦', '09/01/2025', ' LinkedIn ', 'Read more', '🚀 While the Demo Day of Y Combina
… [skrátené, 2122 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c049.json`
```
{
  "candidate_id": "c049",
  "name": "ZAKA VC",
  "legal_name": null,
  "reg_no": null,
  "country": "CZ",
  "active_in": ["CZ", "SK", "US", "GB"],
  "website": "https://www.zaka.vc/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.zaka.vc/",
    "quote": "We are a seed & pre-seed VC fund, investing mainly in the US and Europe. Especially looking for startups in the Health & Biotech and Industrial Tech verticals."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://www.zaka.vc/",
    "quote": "We are a seed & pre-seed VC fund, investing mainly in the US and Europe."
  },
  "sectors": {
    "value": ["healthtech", "biotech", "industrial tech"],
    "source_url": "https://www.zaka.vc/",
    "quote": "Especially looking for startups in the Heal
… [skrátené, 2807 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c049.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c049.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c049.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c049 entity_kind: OK
c049 investor_type: OK
c049 sectors: OK
c049 stages: OK
c049 aum: OK
c049 inv0: OK
c049 inv1: OK
OK    research/c049.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "3TS Capital Partners investment 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "3TS Capital Partners investment 2025 OR 2026"

Links: [{"title":"3TS Capital","url":"https://seedtable.com/investors/3ts-capital"},{"title":"3TS Capital Partners","url":"https://www.deutsche-startups.de/tag/3ts-capital-partners/"},{"title":"bet.hu","url":"https://bet.hu/newkibdata/129100281/K%C3%B6zlem%C3%A9ny%20tervezett%20ipar%C3%A1gi%20felv%C3%A1s%C3%A1rl%C3%A1sr%C3%B3l%20%C3%A9s%20potenci%C3%A1lis%20f%C3%BAzi%C3%B3r%C3%B3l.pdf"},{"title":"3TS Leads US$13 Million Series B Investment in Tresorit (CEE and CIS)","url":"https://www.globalprivatecapital.org/newsroom/3ts-leads-us13-million-series-b-investment-in-tresorit-cee-and-cis/"},{"title":"3ts capital partners new 150m fund","url":"https://siliconcanals.com/3ts-capital-partners-new-150m-fund/"},{"title":"3TS Leads US$13 Million Series B Investment in Tresorit (CEE and CIS)","url":"https://www.globalprivatecapital.org/?p=14742"},{"title":"3TS Capital Partners Invests US$7.2 Million in Visual Unity (CEE and CIS)","url":"https://globalprivatecapital.org/?p=4988"},{"title":"3TS Capital Partners","url":"https://dealroom.launchvic.org/companies/3ts_capital"},{"title":"3TS Capital Invests More Than EUR1 Million in Cloud Software Company 123ContactForm (CEE and CIS)","url":"https://globalprivatecapital.org/?p=5539"},{"title":"3ts capital","url":"https://app.dealroom.co/companies/3ts_capital"}]

Links: [{"title":"3TS Capital","url":"https://seedtable.com/investors/3ts-capital"},{"title":"3TS Capital P
… [skrátené, 4684 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=4000 python3 -I fetch.py https://3tscapital.com/ | head -80; echo XXX; python3 -I fetch.py https://www.heuking.de/en/career/latest-news/detail/heuking-advises-3ts-capital-partners-as-lead-investor-in-11-million-euro-financing-round-for-patronus.html "3TS|Patronus|2026" | head
```

<details><summary>Výstup nástroja</summary>

```
3TS Capital Partners - Leading European technology-focused venture growth investment adviser
25 Years of Technology Investment Excellence
Our Funds and Track Record
With over 25 years and multiple fund generations, we know how to navigate market cycles, lead and co-lead growth rounds, execute cross-border expansion across Europe, the US and Asia, and drive value creation from entry to exit. Our multi-vintage funds reflect a consistent strategy: partnering with exceptional founders to scale internationally, drive innovation, and deliver strong returns. The overview below outlines each fund's size, focus, and notable investments.
Key investments from our current portfolio
We focus on exceptional high growth SMEs, which are either proven businesses becoming local leaders or truly innovative global challengers.

XXX
>> HEUKING advises 3TS Capital Partners as Lead Investor in 11 million Euro Financing Round for Patronus
>> IBA Annual Conference Copenhagen 2026
>> 05-04-2026
>> HEUKING advises 3TS Capital Partners as Lead Investor in 11 million Euro Financing Round for Patronus
>> A cross-office team led by Stuttgart-based partners Benedikt Raisch and Alexander Schott provided comprehensive legal advice to investor 3TS Capital Partners on its investment in Berlin-based startup RR Technologies GmbH (Patronus). The financing round led by 3TS Capital totals 11 million Euro. HEUKING's advisory services encompassed legal due diligence as well as the negotiation of all transaction docume
… [skrátené, 2415 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://3tscapital.com/ | grep -oiE '.{0,200}(Fund IV|TCEE|EUR ?[0-9]+ ?m|€ ?[0-9]+).{0,200}' | sed 's/<[^>]*>/ /g' | head -15; python3 -I fetch.py https://siliconcanals.com/3ts-capital-partners-new-150m-fund/ "3TS|€|Fund IV|Slovak|ticket|202" | head -15
```

<details><summary>Výstup nástroja</summary>

```
ugrep: error: error at position 120
[\x80-\xbf]*){0,200}
                    \___exceeds complexity limits


>> 3TS Capital Partners announces first closing of its new €150M fund - Silicon Canals
>> Sep 22, 2021
>> 3TS Capital Partners announces first closing of its new €150M fund
>> 3TS Capital Partners, a European technology-focused growth capital investor, has announced the first closing of its Fund IV with a target size of €150M.
>> Fund IV received commitments from a broad group of premier institutional investors including the European Investment Fund (EIF), Erste Group, Tesi (Finnish Industry Investment), and several family offices and technology entrepreneurs.
>> EIF Chief Executive Alain Godard says, “We are pleased to be supporting this new 3TS Fund IV which will help tech companies across Europe to grow and innovate. 3TS is an established technology growth-stage VC firm in Central Europe and Eastern Europe and will contribute to technological and industrial innovation capital in the region. This new financing opportunity will provide an alternative funding source for companies as they face the economic consequences of the global pandemic.”
>> 3TS Capital Partners: Fund utilisation
>> With Fund IV, 3TS will continue to back rapidly growing technology companies across software, tech-enabled services, and e-commerce sectors, by leading investment rounds of €5-20M.
>> “We are very glad and thankful for the strong backing from existing and new investors in our Fund IV. D
… [skrátené, 2905 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://3tscapital.com/ | grep -oE 'href="https://3tscapital.com/[^"]*"' | sort -u | head -30
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://3tscapital.com/ | grep -oE 'href="[^"]*"' | grep -v -E '\.(css|js|png|svg|ico|woff)' | sort -u | head -40; for p in contact contact-us; do N=3000 python3 -I fetch.py https://3tscapital.com/$p/ | grep -iE "Vienna|Wien|Prague|Praha|Warsaw|Budapest|Helsinki|Bratislava|Austria"; done
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0" https://3tscapital.com/ | wc -c; curl -sL -A "Mozilla/5.0" https://3tscapital.com/ | grep -oiE "(vienna|wien|prague|warsaw|budapest|helsinki|bratislava)[^<]{0,80}" | sort -u | head
```

<details><summary>Výstup nástroja</summary>

```
40731
Vienna"},"contactPoint":{"@type":"ContactPoint","telephone":"+43-1-8901698","email":"i
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c050.json`
```
{
  "candidate_id": "c050",
  "name": "3TS Capital Partners",
  "legal_name": null,
  "reg_no": null,
  "country": "AT",
  "active_in": ["AT", "CZ", "SK", "PL", "HU", "FI", "DE"],
  "website": "https://3tscapital.com/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.heuking.de/en/career/latest-news/detail/heuking-advises-3ts-capital-partners-as-lead-investor-in-11-million-euro-financing-round-for-patronus.html",
    "source_date": "2026-05-04",
    "quote": "3TS Capital Partners is a technology-focused growth equity firm that invests across Europe in sectors such as technology, media, and technology-enabled services."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://siliconcanals.com/3ts-capital-partners-new-150m-fund/",
    "source_date":
… [skrátené, 3960 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c050.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c050.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c050.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c050 entity_kind: OK
c050 investor_type: OK
c050 sectors: OK
c050 stages: OK
c050 ticket_min: OK
c050 ticket_max: OK
c050 aum: OK
c050 inv0: OK
OK    research/c050.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Slovenský rozvojový fond\" investičný fond", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Slovenský rozvojový fond" investičný fond"

Links: [{"title":"Fond Genesis Capital má pre firmy pripravených 80 mil. eur na rast a akvizície","url":"https://www.podnikajte.sk/investor/genesis-80-rast-akvizicie"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"Kolektívne investovanie v Slovenskej republike a možnosti jeho rozvoja – Bc. Vladimír Demčík","url":"https://theses.cz/id/lji62s?lang=en"},{"title":"is.muni.cz","url":"https://is.muni.cz/th/zbhsd/?lang=en"},{"title":"Andrej Kiska (Credo Ventures): Slovenskou startupovou scénu rozjíždí peníze z EU","url":"https://www.lupa.cz/clanky/andrej-kiska-credo-ventures-slovenskou-startupovou-scenu-rozjizdi-penize-z-eu/"},{"title":"Na Slovensko prichádza nový investičný fond. Jeho objem bude takmer 12 miliónov eur","url":"https://www.startitup.sk/na-slovensko-prichadza-novy-investicny-fond-jeho-objem-bude-takmer-12-milionov-eur/"},{"title":"Druhý najvyšší podiel peňazí z fondov smeroval do bánk","url":"https://sita.sk/druhy-najvyssi-podiel-penazi-z-fondov-smeroval-do-bank/"},{"title":"ROZHOVOR: Lucia Lacková o Slovenskej zahraničnej pomoci","url":"https://pravnenoviny.sk/?p=453"},{"title":"slovensky katolicky podfond fond udrzitelnosti rimskokatolicke cirkve investicni fond s promennym zakladnim kapitalem a s 75160901","url":"https://www.topograph.co/companies/cz/slovensky-katolicky-podfond-fond-u
… [skrátené, 3017 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr "rozvojov|Národný holding|QUADRICA|Monogram|LRJ|Pioneer|Arca|rastový|Limerock|2,3|0,5|Aktualizované|20[012][0-9]" | head -60
```

<details><summary>Výstup nástroja</summary>

```
>> Register krátkodobých prenájmov od 1.1.2027
>> Dôležité čísla pre daňové priznanie fyzickej osoby za rok 2026
>> Hypotéky od roku 2027: zvýhodnené prvé bývanie, prísnejšie investičné nákupy
>> 7 najvýznamnejších zmien v zákone o znalcoch, tlmočníkoch a prekladateľoch od 1.7.2018
>> Podnikateľskí anjeli investovali v roku 2015 v rámci Európy viac než 6 miliárd eur
>> 17.2.2016
>> 17.2.2016
>> Nedostatok financií býva jednou z najvýznamnejších prekážok, ktoré obmedzujú podnikateľov v rýchlejšom raste. Existuje viacero možností, odkiaľ je možné získať potrebný kapitál. Jednou z nich je využitie fondov rizikového kapitálu, ktoré sa špecializujú na perspektívne začínajúce, ale aj etablované podniky. Netreba zabúdať, že investorov (fondy private equity a rizikového kapitálu) zaujímajú predovšetkým projekty, ktoré majú vysoký rastový potenciál, teda šancu, že oslovia veľký počet zákazníkov na globálnom trhu.
>> Monogram Ventures
>> Monogram Ventures je zameraná na hi-tech produkty a komercializáciu nových digitálnych trendov. Od roku 2008 táto investičná spoločnosť pomohla rozbehnúť viacero úspešných spin-off projektov (Colosseo, StreamStar) či start-upov (už spomínané Piano Media, Diagnose.me) alebo Websupport.
>> LRJ Capital - investícia sa pohybuje od 100 000 do 2 miliónov eur
>> Pioneers Ventures - počiatočný kapitál až do výšky 125 000 eur
>> Pioneers Ventures sa špecializuje na projekty v počiatočných (zárodočných) štádiách životného cyklu. Začínajúcim podnikom poskytuje ka
… [skrátené, 6951 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Národný holdingový fond Slovenský rastový a kapitálový fond Slovenský rozvojový fond", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Národný holdingový fond Slovenský rastový a kapitálový fond Slovenský rozvojový fond"

Links: [{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"nh fund","url":"https://altss.com/profile/nh-fund.md"},{"title":"n rodn holdingov fond nhfond sk","url":"https://venturecapitalarchive.com/venture-funds/n-rodn-holdingov-fond-nhfond-sk"},{"title":"Fond Genesis Capital má pre firmy pripravených 80 mil. eur na rast a akvizície","url":"https://www.podnikajte.sk/investor/genesis-80-rast-akvizicie"},{"title":"Národní rozvojový fond bude spravovat státní banka, na investice půjde až 35 miliard","url":"https://www.e15.cz/byznys/finance-a-bankovnictvi/narodni-rozvojovy-fond-bude-spravovat-statni-banka-na-investice-pujde-az-35-miliard-1360230"},{"title":"znenie 19930101","url":"https://www.zakonypreludi.sk/print/zz/1993-17/znenie-19930101.htm"},{"title":"znenie 0","url":"https://www.zakonypreludi.sk/print/zz/1993-17/znenie-0.htm"},{"title":"znenie 19930101","url":"https://www.zakonypreludi.sk/print/zz/1991-253/znenie-19930101.htm"},{"title":"znenie 19930101","url":"https://www.zakonypreludi.sk/zz/1993-17/znenie-19930101"}]

The search returned useful information about the Národný holdingový fond (NHF), but little on the other two funds named in your query.

**Národný holdingový fond (NHF)**
- A directory profile describes it as a specialized subsidiary of Slov
… [skrátené, 2583 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.nhfond.sk https://nhfond.sk; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done; N=5000 python3 -I fetch.py https://www.nhfond.sk/ | head -100
```

<details><summary>Výstup nástroja</summary>

```
https://www.nhfond.sk 200 https://www.nhfond.sk/
https://nhfond.sk 200 https://nhfond.sk/

 Domov
 |
 Kontakt
 Podpora MSP
 Mikropôžičky
 Fondy rizikového kapitálu
 Články
 O nás
Kalendár podujatí
Vyberte si z podujatí Slovak Business Agency. Po celý rok organizuje bezplatné semináre, workshopy a prednášky pre podnikateľov a aj tých, ktorí sa len chystajú vstúpiť do vôd biznisu. 
 Zobraziť
Mikropôžičkový program
 Zobraziť
Erasmus
pre mladých podnikateľov je európsky výmenný program pomáhajúci začínajúcim podnikateľom získať skúsenosti a zručnosti prospešné pre úspešný štart alebo rozvoj svojho podnikania v Európe.
 Zobraziť
Eterus Capital
Eterus Capital je partnerom pre financovanie podnikateľa vo fáze rastu.
Cieľom Eterus Capital je identifikácia zaujímavých rastových projektov/spoločností, následná realizácia investície a exit pri požadovanej návratnosti vložených zdrojov.
Fond je svojím kapitálovým vstupom schopný vyriešiť existujúce joint-venture resp. iné vlastnícke spory.
Ideálnym projektom je projekt alebo spoločnosť s výrazným rastovým potenciálom, silným trhovým postavením a motivovaným manažmentom.
 Zobraziť všetko
Fond inovácií a technológií 
Fond inovácií a technológií ponúka partnerstvo (FIT) ponúka výrazné zlepšenie finančnej pozície projektu.
Poslaním FIT je formou poskytovania rizikového kapitálu podporiť podnikateľskú iniciatívu a tak rozvíjať podnikanie, zamestnanosť a hospodárstvo smerom k inovatívnej ekonomike.
Finančné možnosti Fondu poskytuj
… [skrátené, 3082 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Eterus Capital\" \"Slovenský rastový a kapitálový fond\"", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Eterus Capital" "Slovenský rastový a kapitálový fond""

Links: [{"title":"Preskočiť na hlavný obsah","url":"https://kpmg.com/sk/sk/home/insights/2019/10/transakcia-hopin-eteruscapital-kpmg-poradca.html"},{"title":"Go to deals","url":"https://www.oaklins.com/il/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/ie/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/sg/en/deals/110583/"},{"title":"Private Equity","url":"https://altss.com/profile/eterus-capital"},{"title":"Go to deals","url":"https://www.oaklins.com/ma/en/deals/110584/"},{"title":"Gå till Affärer","url":"https://www.oaklins.com/fi/sv/deals/110584"},{"title":"Go to deals","url":"https://www.oaklins.com/se/en/deals/110583/"},{"title":"Go to deals","url":"https://www.oaklins.com/se/en/deals/110584/"},{"title":"Eterus Capital logo","url":"https://www.tryfundable.ai/investor/eterus-capital"}]

The search returned plenty on Eterus Capital but nothing that mentions "Slovenský rastový a kapitálový fond." I can't confirm from these results whether that name refers to Eterus or to a separate entity.

**What the results say about Eterus Capital:**
- It's a Slovak private equity fund that has operated since 2008 and focuses on growth-stage small and medium-sized companies. The fund is managed by WOOD & Company, a Central European investment group. (KPMG Slovakia case study)
- Its investments are mostly minority stakes, which leave management control 
… [skrátené, 2450 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Eterus Capital predtým Slovenský rastový kapitálový fond premenovaný SRKF", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Eterus Capital predtým Slovenský rastový kapitálový fond premenovaný SRKF"

Links: [{"title":"Preskočiť na hlavný obsah","url":"https://kpmg.com/sk/sk/home/insights/2019/10/transakcia-hopin-eteruscapital-kpmg-poradca.html"},{"title":"TILL TRANSAKTIONER","url":"https://www.oaklins.com/se/sv/deals/110583"},{"title":"Private Equity","url":"https://altss.com/profile/eterus-capital"},{"title":"Go to deals","url":"https://www.oaklins.com/il/en/deals/110584/"},{"title":"Zu den Deals","url":"https://www.oaklins.com/at/de/deals/110583/"},{"title":"Gå till Affärer","url":"https://www.oaklins.com/fi/sv/deals/110584"},{"title":"Go to deals","url":"https://www.oaklins.com/ie/en/deals/110584/"},{"title":"Go to deals","url":"https://www.oaklins.com/ma/en/deals/110584/"},{"title":"Ir a las transacciones","url":"https://oaklins.com/co/es/deals/110584"},{"title":"Eterus Capital logo","url":"https://www.tryfundable.ai/investor/eterus-capital"}]

Nenašiel som vo výsledkoch žiadny zdroj, ktorý by spájal Eterus Capital so Slovenským rastovým kapitálovým fondom (SRKF) alebo s tvrdením, že ide o premenovaný fond. Výsledky o SRKF neobsahujú nič, takže túto súvislosť nemôžem potvrdiť ani vyvrátiť.

Z nájdených zdrojov viem o Eterus Capital toto:

- Ide o slovenský private equity fond, ktorý investuje do malých a stredných podnikov vo fáze rastu a na trhu pôsobí od roku 2008.
- Fond spravuje spoločnosť WOOD & Company, podľa iného zdroja ide o skupinu, ktorá má silné posta
… [skrátené, 2255 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.eteruscapital.sk https://eteruscapital.com https://www.eterus.sk; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done; python3 -I fetch.py https://www.eteruscapital.sk/ "rastov|SRKF|2008|Slovensk|kapitálov|WOOD|Národn" | head -20
```

<details><summary>Výstup nástroja</summary>

```
https://www.eteruscapital.sk 000 https://www.eteruscapital.sk/
https://eteruscapital.com 000 https://eteruscapital.com/
https://www.eterus.sk 200 https://eterus.sk/
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=4000 python3 -I fetch.py https://eterus.sk/ | head -60; curl -sL https://eterus.sk/ | grep -oE 'href="https://eterus.sk/[^"]*"' | sort -u | head -20
```

<details><summary>Výstup nástroja</summary>

```
 Eterus Capital – Private equity: Investujeme do vášho rastu
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
Investujeme
 do vášho rastu
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
onsenz
… [skrátené, 4805 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://eterus.sk/en/private-equity-fund/ "growth|Slovak|SRKF|formerly|renam|Holding|NHF|National|2008|WOOD" | head -20
```

<details><summary>Výstup nástroja</summary>

```
>> in your growth
>> Growth capital
>> Eterus is a partner for financing growth-stage companies with capable management and a proven concept.
>> We are an equity fund investing in shares and other equity instruments of companies domiciled in Slovakia. We do not offer debt financing.
>> The fund can also identify potential acquisition targets, negotiate takeover deals, structure the financing of these opportunities, and ensure the company's sustained growth as a market consolidator.
>> Consolidation platform for dental practices in Slovakia.
>> Consolidation platform for pharmacies in Slovakia.
>> The largest cycling e-commerce portal in Slovakia that has been growing steadily since 1998 and serves a community of over 200 thousand users.
>> Developer and operator of the first Slovak ride-hauling app.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Slovenský rozvojový fond, a.s.\" OR \"Slovenský Rozvojový Fond\" Quadrica zánik OR likvidácia OR zlúčenie", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Slovenský rozvojový fond, a.s." OR "Slovenský Rozvojový Fond" Quadrica zánik OR likvidácia OR zlúčenie"

Links: [{"title":"Slovak Guarantee and Development Bank","url":"https://en.wikipedia.org/wiki/Slovak_Guarantee_and_Development_Bank"},{"title":"www.crp.gov.sk","url":"https://www.crp.gov.sk/data/att/55906.pdf"},{"title":"ROZHOVOR: Lucia Lacková o Slovenskej zahraničnej pomoci","url":"https://pravnenoviny.sk/rozhovor-lucia-lackova-o-slovenskej-zahranicnej-pomoci/"},{"title":"ROZHOVOR: Lucia Lacková o Slovenskej zahraničnej pomoci","url":"https://pravnenoviny.sk/?p=453"},{"title":"Original title:","url":"https://invenio.nusl.cz/record/74645?ln=en"},{"title":"Sprava o rozvojovej spolupraci Slovenskej republiky za rok 2022","url":"https://slovakaid.sk/wp-content/uploads/2020/12/Sprava-o-rozvojovej-spolupraci-Slovenskej-republiky-za-rok-2022.pdf"},{"title":"Development assistance and the approach of Slovak Republic to developing countries","url":"https://dspace.cuni.cz/handle/20.500.11956/50185"},{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/slovensko-dohoda-mib-asistencia/194382-clanok.html"},{"title":"vyrocna sprava oda 2016 na web","url":"https://test.slovakaid.sk/wp-content/uploads/2020/12/vyrocna_sprava_oda_2016_na_web.pdf"}]

Links: [{"title":"Slovak Government Allocates New Funds for Development Aid in 2020","url":"https://www.tasr.sk/tasr-clanok/TASR:20200115TBB00187"},{"title"
… [skrátené, 5516 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c051.json`
```
{
  "candidate_id": "c051",
  "name": "Slovenský rozvojový fond",
  "legal_name": "Slovenský Rozvojový Fond, a.s.",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Slovenský Rozvojový Fond (SRF) realizuje investície do zabehnutých alebo začínajúcich spoločností, ktoré potrebujú expanzný kapitál. Investuje formou vkladu do základného imania spoločností a stáva sa spoluvlastníkom na vopred stanovené obdobie."
  },
  "investor_type": {
    "value": "public_fund",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    
… [skrátené, 2023 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c051.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c051.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c051.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c051 entity_kind: OK
c051 investor_type: OK
c051 stages: OK
c051 ticket_max: OK
OK    research/c051.json
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0" https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr | grep -oiE '(datePublished|dateModified|published_time|modified_time)[^,>]{0,60}' | head
```

<details><summary>Výstup nástroja</summary>

```
published_time" content="2016-02-17T23:00:00+01:00" /
modified_time" content="2021-10-04T18:03:40+02:00" /
datePublished": "2016-02-17T23:00:00+01:00"
dateModified": "2021-10-04T18:03:40+02:00"
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c056.json`
```
{
  "candidate_id": "c056",
  "name": "Slovenský rastový a kapitálový fond",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://eterus.sk/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Slovenský rastový a kapitálový fond (SRKF) je partnerom pre financovanie podnikateľa vo fáze rastu."
  },
  "investor_type": {
    "value": "public_fund",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "V rámci verejných fondov u nás pôsobí Národný holdingový fond."
  },
  "stages": {
    "value": ["growth"],
    "source_url": "https://ww
… [skrátené, 2306 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c056.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c056.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c056.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c056 entity_kind: OK
c056 investor_type: OK
c056 stages: OK
c056 ticket_min: OK
c056 ticket_max: OK
OK    research/c056.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Monogram Ventures Bratislava investícia startup", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Monogram Ventures Bratislava investícia startup"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/monogram"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"monogram ventures","url":"https://insights.munich-startup.de/investors/monogram_ventures"},{"title":"Ivan Štefunko: Sľub dodržím a dnes budem súťažiť na Startup Weekend Bratislava","url":"https://www.startitup.sk/?p=10551"},{"title":"Ivan Štefunko: Sľub dodržím a dnes budem súťažiť na Startup Weekend Bratislava","url":"https://www.startitup.sk/ivan-stefunko-slub-dodrzim-a-dnes-budem-sutazit-na-startup-weekend-bratislava/"},{"title":"Monopoly Ventures Overview","url":"https://pitchbook.com/profiles/investor/651787-75"},{"title":"Investori prídu do Bratislavy loviť startupy","url":"https://www.podnikajte.sk/investor/investori-startupy"},{"title":"Investície do startupov","url":"https://www.podnikajte.sk/investor/investicie-startupy"},{"title":"Monogram Capital Closes Debut Fund at $152M | Global AgInvesting","url":"https://globalaginvesting.com/monogram-capital-closes-debut-fund-152m/"},{"title":"Translated by","url":"https://uk.fashionnetwork.com/news/Monogram-raises-nearly-3-million,1509539.html"}]

Monogram Ventures is a Bratislava-based venture investor, and the sources agree on its focus on early-stage 
… [skrátené, 3421 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.monogram.sk https://monogram.sk https://www.monogramventures.com; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done; N=3000 python3 -I fetch.py https://www.monogram.sk | head -50
```

<details><summary>Výstup nástroja</summary>

```
https://www.monogram.sk 200 https://monogram.sk/
https://monogram.sk 200 https://monogram.sk/
https://www.monogramventures.com 200 https://www.monogramventures.com/

MGSK
Zdravie & Životný štýl
Domov & Záhrada
Veda & Technológie
Auto & Moto
Móda & Štýl
Krása
Tipy & Návody
Zdravie & Životný štýl
Domov & Záhrada
Veda & Technológie
Auto & Moto
Móda & Štýl
Krása
Tipy & Návody
 Search
Zdravie & Životný štýl
Domov & Záhrada
Veda & Technológie
Auto & Moto
Móda & Štýl
Krása
Tipy & Návody
 Follow US
Zdravie & Životný štýl
Domov & Záhrada
Veda & Technológie
Auto & Moto
Móda & Štýl
Krása
Tipy & Návody
MGSK © 2025. All Rights Reserved.
Tipy & Návody
 Všetko o varenej strave pre psa: ako ju správne zostaviť a čomu sa vyhnúť
 Simona Kovácová 
Domov & Záhrada
 Z chodby do mačacieho raja: DIY s TEMU
 Simona Kovácová 
Domov & Záhrada
 Záhrada na konci leta nekončí: čo sa oplatí urobiť ešte pred príchodom jesene
August a začiatok septembra môžu pôsobiť ako pomalý koniec záhradnej sezóny. Paradajky dozrievajú, niektoré záhony zostávajú po zbere prázdne a prvé rastliny postupne strácajú svoju…
 Simona Kovácová 
Min. prečítanie 4
Najčítanejšie
na tento mesiac
Zdravie & Životný štýl
 Orechovica: Prírodný dar pre tvoje zdravie – účinky, zloženie a tajomstvá výroby
Zdravie & Životný štýl
 Dusitanová soľ v kuchyni: Riziká a výhody, ktoré by si mal poznať
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=2000 python3 -I fetch.py https://www.monogramventures.com/ | head -30
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
curl -sL -A "Mozilla/5.0" https://www.monogramventures.com/ | head -c 1500
```

<details><summary>Výstup nástroja</summary>

```
<!DOCTYPE html><html><head><script>window.onload=function(){window.location.href="/lander"}</script></head></html>
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.startitup.sk/ivan-stefunko-slub-dodrzim-a-dnes-budem-sutazit-na-startup-weekend-bratislava/ "Monogram" | head
```

<details><summary>Výstup nástroja</summary>

```
>> Je niekoľkonásobným podnikateľom a podnikateľským anjelom so skúsenosťami najmä vo svete online médií a internetových projektov. Založil niekoľko spoločností s regionálnou aj celosvetovou pôsobnosťou, vrátane Monogram Technologies, Pelicantravel.com, Euractiv.sk a wineshop.sk. Pred založením Neulogy Ventures bol aktívny ako investor a investičný poradca pri niekoľkých technologických projektoch ako napríklad Piano Media, GA Drilling (predtým Geothermal Anywhere) a Diagnose.me. Je spoluzakladateľom Neulogy, bratislavskej poradenskej spoločnosti zameranej na manažment vedy, inovácie a začínajúce technologické firmy.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Monogram Ventures\" Piano Media investícia 2011", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Monogram Ventures" Piano Media investícia 2011"

Links: [{"title":"Piano Media","url":"https://en.wikipedia.org/wiki/Piano_Media"},{"title":"Shared Online Paywall Service Piano Media Secures 2 Million Euros From 3TS","url":"https://techcrunch.com/2012/04/17/shared-online-paywall-service-piano-media-secures-euro-2-million-from-3ts"},{"title":"www.eu startups","url":"https://www.eu-startups.com/?p=3200"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/monogram"},{"title":"Founded Year","url":"https://www.cbinsights.com/company/piano-media"},{"title":"www.journalism.co.uk","url":"https://www.journalism.co.uk/news/piano-media-2m-investment-3ts-capital-partners-national-paywall-tomas-bella/s2/a548805/"},{"title":"3ts and aws gr nderfonds back piano media","url":"https://www.unquote.com/dach/official-record/72344/3ts-and-aws-gr-nderfonds-back-piano-media"},{"title":"piano io","url":"https://prod.actual.seedtable.com/startups/piano-io"},{"title":"National paywall firm Piano Media recieves €2m investment","url":"https://www.journalism.co.uk/piano-media-2m-investment-3ts-capital-partners-national-paywall-tomas-bella/"},{"title":"series c 2021 05","url":"https://seedtable.com/companies/piano-company/funding-rounds/series-c-2021-05"}]

The sources agree that Monogram Ventures invested in Piano Media in 2011, but they differ on the date and the round's label.

- **Date and round:** 
… [skrátené, 2830 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://techcrunch.com/2012/04/17/shared-online-paywall-service-piano-media-secures-euro-2-million-from-3ts "MONOGRAM|Monogram" | head; python3 -I fetch.py https://en.wikipedia.org/wiki/Piano_Media "Monogram" | head
```

<details><summary>Výstup nástroja</summary>

```
>> Piano Media, launched in May 2011, enables online publications to offer their readers premium content on a subscription basis. In July 2011 it raised €300,000 from MONOGRAM Ventures, Etarget and NextBig.
>> In September 2011 Piano received Series-A funding from Jan Jenča and Ivan Štefunko at Monogram Ventures. Piano used the money to solidify their Slovak market share and expand their national paywall into several other Central European countries.[14] In January 2012 Piano Media expanded into Slovenia, bringing seven publishers into the common payment system.[15] In April 2012 Piano secured €2 million in a Series B growth capital round from 3TS Capital Partners’ Technology in Central and Eastern Europe Fund S.C.A. SICAR. The funding allowed Piano to accelerate their growth worldwide,[16] by expanding its national paywall into Poland in September 2012.[17] In 2013, the company pivoted away from
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c052.json`
```
{
  "candidate_id": "c052",
  "name": "Monogram Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Monogram Ventures je zameraná na hi-tech produkty a komercializáciu nových digitálnych trendov."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Od roku 2008 táto investičná spoločnosť pomohla rozbehnúť viacero úspešných spin-off projektov (Colosseo, StreamStar) či start-upov (už spomínané Piano Media, Diagnose.me) alebo Websup
… [skrátené, 1876 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c052.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c052.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c052.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c052 entity_kind: OK
c052 investor_type: OK
c052 sectors: OK
c052 inv0: OK
OK    research/c052.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"LRJ Capital\" Slovakia investment", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""LRJ Capital" Slovakia investment"

Links: [{"title":"top of page","url":"https://www.symsite.sk/single-post/2020/01/02/largest-investments-into-slovak-start-ups"},{"title":"Slovenský startup získal investíciu 1,5 milióna eur","url":"https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/"},{"title":"Koľko miliónov eur je dnes dostupných pre slovenské projekty?","url":"https://www.startitup.sk/?p=50283"},{"title":"Koľko miliónov eur je dnes dostupných pre slovenské projekty?","url":"https://www.startitup.sk/kolko-milionov-eur-je-dnes-dostupnych-pre-slovenske-projekty/"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"Second Photo","url":"https://www.tryfundable.ai/investor/lrj-capital"},{"title":"REQUEST A DEMO","url":"https://emis.cn/php/company-profile/SK/Lrj_SRO_en_13250454.html"},{"title":"www.eib.org","url":"https://www.eib.org/de/contacts/office/slovakia"},{"title":"investing in slovakia","url":"https://kpmg.com/sk/en/services/investing-in-slovakia.html"},{"title":"press officer slovakia","url":"https://www.eib.org/de/press/contacts/press-officer-slovakia"}]

LRJ Capital is a Slovak investment holding that has backed several well-known Slovak startups, though most of the results I found are from 2019 to 2020.

- **Exponea:** In 2019, LRJ Capital, with Ivan Chrenko among its partners, was the lead investor in the la
… [skrátené, 3008 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://www.lrjcapital.com https://lrj.sk https://www.growws.com https://growws.sk; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done; N=4000 python3 -I fetch.py https://www.lrjcapital.com | head -80
```

<details><summary>Výstup nástroja</summary>

```
https://www.lrjcapital.com 200 https://www.hugedomains.com/domain_profile.cfm?d=lrjcapital.com
https://lrj.sk 000 https://lrj.sk/
https://www.growws.com 403 https://www.brandbucket.com/names/growws
https://growws.sk 000 https://growws.sk/
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "LRJ Capital Chrenko investícia 2024 OR 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "LRJ Capital Chrenko investícia 2024 OR 2025 OR 2026"

Links: [{"title":"RRJ Capital","url":"https://en.wikipedia.org/wiki/RRJ_Capital"},{"title":"Slovenský startup získal investíciu 1,5 milióna eur","url":"https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/"},{"title":"Koľko miliónov eur je dnes dostupných pre slovenské projekty?","url":"https://www.startitup.sk/?p=50283"},{"title":"Jesteś w trybie podpowiedzi Wyłącz","url":"https://cbonds.pl/company/79755/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/lr-capital"},{"title":"Cargos activos de Jakub Chronek","url":"https://es.marketscreener.com/insider/JAKUB-CHRONEK-A2MB6U/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/l-j"},{"title":"evropsky investicni karibik 10 duvodu proc muze byt z chorvatska hotspot","url":"https://forbes.cz/evropsky-investicni-karibik-10-duvodu-proc-muze-byt-z-chorvatska-hotspot/"},{"title":"Hinweis-Modus ist eingeschaltet Ausschalten","url":"https://cbonds.de/company/79755/"}]

I couldn't find a dated 2024, 2025, or 2026 investment by LRJ Capital involving Chrenko. I ran the search without the "OR" operators, since they aren't supported, and the results were mostly unrelated.

The one relevant result is a Startitup.sk article about Finax, a Slovak fintech. LRJ Capital, through its fund GROWWS SICAV, a.s., invested 1.5 million euros in Finax. GROWWS is a significant shar
… [skrátené, 2285 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/ "LRJ|GROWWS|Finax" | head; curl -sL -A "Mozilla/5.0" https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/ | grep -oE '"datePublished":"[^"]+"|published_time" content="[^"]+"' | head -2; python3 -I fetch.py https://www.symsite.sk/single-post/2020/01/02/largest-investments-into-slovak-start-ups "LRJ" | head
```

<details><summary>Výstup nástroja</summary>

```
>> Spoločnosť Finax poskytla Startitup exkluzívnu informáciu o významnej investícií, ktorú získali. LRJ Capital cez svoj fond GROWWS SICAV, a.s. podporil inovátora v inteligentnom investovaní, Finax investíciou 1,5 milióna eur. Ten využije investíciu na expanziu slovenskej inovácie do sveta a na ďalší technologický rozvoj.
>> archív Finax
>> Finax sa na partnerstve dohodol s GROWWS SICAV, a.s., ktorého významným akcionárom je investičný holding LRJ Capital. GROWWS je profesionálnym venture fondom, ktorého predsedom správnej rady je Peter Irikovský. Peter vybudoval Slevomat Group (nedávno predaný za viac ako €60m) a dnes riadi jeden z najväčších slovenských technologických startupov spoločnosť Exponea.
>> Fond okrem Petra vlastní Ivan Chrenko, ktorý je majiteľom developerskej skupiny HB Reavis. Ďalším partnerom je Michal Pastier, ktorý spoluzaložil Zaraguzu alebo agentúru BigName. Fond GROWWS vstupuje do Finaxu investíciou 1,5 milióna eur, ktorá predstavuje podľa informácii spoločnosti Finax najväčšiu investíciu do fintech startupu v histórii Slovenska. To Finax pre Startitup zdôvodnil takto:
>> zdroj: archív Finax
>> Pýtali sme sa aj na to, čomu podľa vedenia Finax môžu vďačiť za to, že investor do nich vložil tak veľký kapitál. „Tých dôvodov je niekoľko. Žiadna firma ako my na Slovensku nie je, ponúkame unikátny moderný produkt pre 21. storočie, spojenie financií a technológií v pravom slova zmysle. Myslím si, že rolu hral aj náš proklientský a transparentný prístup k biznis
… [skrátené, 3173 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c053.json`
```
{
  "candidate_id": "c053",
  "name": "LRJ Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/",
    "source_date": "2019-03-15",
    "quote": "Finax sa na partnerstve dohodol s GROWWS SICAV, a.s., ktorého významným akcionárom je investičný holding LRJ Capital."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://www.startitup.sk/slovensky-startup-ziskal-investiciu-15-miliona-eur/",
    "source_date": "2019-03-15",
    "quote": "GROWWS je profesionálnym venture fondom, ktorého predsedom správnej rady je Peter Irikovský."
  },
  "ticket_min": {
    "amount": 100000,
    "curr
… [skrátené, 2065 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c053.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c053.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c053.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c053 entity_kind: OK
c053 investor_type: OK
c053 ticket_min: OK
c053 ticket_max: OK
c053 inv0: OK
OK    research/c053.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Pioneers Ventures\" Cloudo investícia Slovensko", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Pioneers Ventures" Cloudo investícia Slovensko"

Links: [{"title":"www.startitup.sk","url":"https://www.startitup.sk/?p=14255"},{"title":"pioneers ventures cloudo becomes first investment","url":"https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/"},{"title":"pioneers.io","url":"https://pioneers.io/?p=1319"},{"title":"office hours pioneers ventures starts 2018 roadshow strong slovenia","url":"https://pioneers.io/office-hours-pioneers-ventures-starts-2018-roadshow-strong-slovenia/"},{"title":"pioneers ventures neuer 8 millionen euro fonds investiert erste 100 000 euro in das start up cloudo","url":"https://www.trendingtopics.eu/pioneers-ventures-neuer-8-millionen-euro-fonds-investiert-erste-100-000-euro-in-das-start-up-cloudo/"},{"title":"pioneers.io","url":"https://pioneers.io/?p=1600"},{"title":"www.thecompanycheck.com","url":"https://www.thecompanycheck.com/company/b/pioneers/mdsw2nond43k32r37"},{"title":"pioneers ventures","url":"https://ecosystem.madrimasd.org/investors/pioneers_ventures"},{"title":"Crowdberry, Zero Gravity Ventures, and Vision Ventures to invest state money into Slovak start-ups","url":"https://www.symsite.sk/single-post/2019/10/08/crowdberry-zero-gravity-ventures-and-vision-ventures-to-invest-state-money-into-slovak-st"}]

The search turned up a 2015 announcement that Pioneers Ventures made its first investment in Cloudo, a Bratislava startup. I found no recent news about the investment, so the status b
… [skrátené, 2956 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/ "Pioneers Ventures|Cloudo|fund|2015|invest" | head -15; curl -sL -A "Mozilla/5.0" https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/ | grep -oE 'published_time" content="[^"]+"' | head -1; python3 -I fetch.py https://www.trendingtopics.eu/pioneers-ventures-neuer-8-millionen-euro-fonds-investiert-erste-100-000-euro-in-das-start-up-cloudo/ "Pioneers Ventures|Cloudo|Millionen|Wien" | head
```

<details><summary>Výstup nástroja</summary>

```
>> Cloudo Gets Pioneers Ventures’ First Investment | Front page
>> Cloudo Gets Pioneers Ventures’ First Investment
>> By PioneersOctober 19, 2015No Comments
>> Pioneers Ventures is our investment vehicle at Pioneers. The fund was officially launched at Pioneers Festival 2015. Today, we are excited to announce the signing of our first investment.
>> Cloudo, the Bratislava based startup enables you to increase your productivity when searching and organizing your stuff online. We are more than proud that Cloudo becomes the first member of the Pioneers Ventures family.
>> From top left: Jakub Kolar (Developer), Tomas Trungel (Developer), Pavel Koci (Developer). From bottom left: Klaus Matzka (Partner PV), Ondrej Prostrednik (Co-founder & CEO Cloudo), Juraj Pelikan (Co-founder & CTO Cloudo), Philipp Stangl (Investment Manager PV), Markus Lang (Investment Manager PV)
>> “New funding is crucial in such an early stage of the company. However, at the end of the day, the decisive factor was that Pioneers Ventures provides far more than money. The decisive factor was that Pioneers Ventures provides far more than money. Access to a large network of experts along with a strong US-connection and support in future fundraising rounds will enable us to build the best possible product,” says Ondrej Prostrednik, founder and CEO at Cloudo.
>> “In Cloudo we found the perfect first partner for our fund. Three things convinced us: first, the ambitious team and their experience in the given field. S
… [skrátené, 5223 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Pioneers Ventures\" Vienna pre-seed fund latest investment 2023 2024", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Pioneers Ventures" Vienna pre-seed fund latest investment 2023 2024"

Links: [{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/pioneers-ventures"},{"title":"Austrian pre-seed fund Pioneers Ventures restructures as Speedinvest takes on its portfolio","url":"https://tech.eu/brief/pioneers-ventures-restructures/"},{"title":"Austrian pre-seed fund Pioneers Ventures restructures as Speedinvest takes on its portfolio","url":"https://tech.eu/2018/08/01/pioneers-ventures-restructures/"},{"title":"pioneers ventures iii neuer startup fonds mit 10 millionen euro geplant","url":"https://www.trendingtopics.eu/pioneers-ventures-iii-neuer-startup-fonds-mit-10-millionen-euro-geplant/"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/startup300"},{"title":"pioneers ventures","url":"https://dealroom.launchvic.org/companies/pioneers_ventures"},{"title":"Pioneers Ventures (investor - Venture Capital)","url":"https://nordic9.com/companies/pioneers-ventures-investor2279292444/"},{"title":"Pioneers Ventures","url":"https://unicorn-nest.com/funds/pioneers-ventures"},{"title":"Pioneers Ventures","url":"https://app.dealroom.co/investors/pioneers_ventures"},{"title":"pioneers ventures","url":"https://startups.one.gob.es/companies/pioneers_ventures"}]

I couldn't find a confirmed Pioneers Ventures investment dated 2023 or 2024. The results point to older deals and one 2025 item.

- **Latest dated deal:**
… [skrátené, 3286 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c054.json`
```
{
  "candidate_id": "c054",
  "name": "Pioneers Ventures",
  "legal_name": null,
  "reg_no": null,
  "country": "AT",
  "active_in": ["AT", "SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/",
    "source_date": "2015-10-19",
    "quote": "Pioneers Ventures is Pioneers’ pre-seed investment vehicle empowering startups with our global network of corporates, industry experts, and entrepreneurs."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://pioneers.io/pioneers-ventures-cloudo-becomes-first-investment/",
    "source_date": "2015-10-19",
    "quote": "Pioneers Ventures is our investment vehicle at Pioneers. The fund was officially launched at Pioneers Festival 
… [skrátené, 3131 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c054.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c054.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c054.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c054 entity_kind: OK
c054 investor_type: OK
c054 sectors: OK
c054 stages: OK
c054 ticket_max: OK
c054 aum: OK
c054 inv0: OK
OK    research/c054.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Arca Capital Slovakia 2025 investícia fond", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Arca Capital Slovakia 2025 investícia fond"

Links: [{"title":"Arca Capital čelí konkurzu po rokoch právnych manévrov. Tržby klesli na 144-tisíc eur, dlhy presiahli miliardu","url":"https://www.startitup.sk/?p=1101306"},{"title":"Arca Investments žiada prerušenie slovenského konkurzného konania. Krúpa: Ide o účelové naťahovanie","url":"https://www.startitup.sk/arca-investments-ziada-prerusenie-slovenskeho-konkurzneho-konania-krupa-ide-o-ucelove-natahovanie/"},{"title":"Spravodajský portál Tlačovej agentúry Slovenskej republiky","url":"https://www.teraz.sk/ekonomika/arca-investments-podala-novy-insolvenc/521892-clanok.html"},{"title":"Arca Investments žiada prerušenie slovenského konkurzného konania. Krúpa: Ide o účelové naťahovanie","url":"https://www.startitup.sk/?p=1144677"},{"title":"arca capital","url":"https://www.newstream.cz/stitek/arca-capital"},{"title":"ekonomickydenik.cz","url":"https://ekonomickydenik.cz/?p=47127"},{"title":"Hlavní obsah","url":"https://www.seznamzpravy.cz/clanek/stiny-arca-investments-sprizneny-fond-redside-prestal-vyplacet-penize-173657"},{"title":"pavol krupa","url":"https://www.newstream.cz/stitek/pavol-krupa"},{"title":"Matovič sa vyjadril ku kauze Arca Capital, tvrdenia označil za útok Fica, Pellegriniho a Haščáka","url":"https://sita.sk/premier-matovic-sa-vyjadri-ku-kauze-arca-capital-na-ktoru-podal-smer-sd-trestne-oznamenie/"}]

Search results show Arca Capital Slovakia in insolvency during 2025, with no sign
… [skrátené, 3370 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.startitup.sk/?p=1101306" "Arca|konkurz|júl|2025" | head -15; curl -sL -A "Mozilla/5.0" "https://www.startitup.sk/?p=1101306" -o /dev/null -w "%{url_effective}\n"
```

<details><summary>Výstup nástroja</summary>

```
>> Z kolosu s majetkom za 800 miliónov na pokraj konkurzu
>> Arca Capital čelí konkurzu po rokoch právnych manévrov. Tržby klesli na 144-tisíc eur, dlhy presiahli miliardu
>> 17. júla 2025 o 12:59
>> Arca Capital Slovakia smeruje do konkurzu, dlhuje viac ako miliardu eur. Veritelia roky čakajú, firma má minimálne tržby a jej strata sa zvyšuje.
>> 17. júla 2025 o 12:59
>> Finančná skupina Arca Capital, kedysi označovaná za „predátora medzi investíciami“, sa po rokoch právnych únikov a reštrukturalizačných manévrov dostáva do ďalšej kľúčovej fázy svojho úpadku.
>> Ako informoval portál SME.sk, Mestský súd Bratislava III začiatkom júla 2025 rozhodol o začatí konkurzného konania voči spoločnosti Arca Capital Slovakia.
>> Návrh na konkurz podala advokátska kancelária Fardous Partners v mene približne 4 500 drobných veriteľov, ktorým firma neuspokojila ich pohľadávky ani v rámci predchádzajúcej reštrukturalizácie.
>> Rozhodnutie o začatí konkurzného konania však ešte neznamená definitívny vstup Arcy do konkurzu. Ako pre SME uviedol právnik Fadi Fardous, Arca má možnosť proces zvrátiť – konkrétne uhradením záväzkov veriteľov, ktorí návrh podali. S ohľadom na rozsah dlhov a dlhodobé problémy so splácaním je však otázne, či je takýto scenár reálny.
>> Podľa analýzy portálu Aktuality.sk ide v prípade skupiny Arca o najväčší firemný krach v novodobej histórii Slovenska i Českej republiky. Celkový dlh skupiny presiahol 770 miliónov eur, a to len na úrovni materskej spoločnosti Arca Inves
… [skrátené, 3340 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c055.json`
```
{
  "candidate_id": "c055",
  "name": "Arca Capital Slovakia",
  "legal_name": "Arca Capital Slovakia",
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Arca Capital je private equity skupina pôsobiaca predovšetkým v regióne strednej a východnej Európy. Investuje svoje vlastné finančné prostriedky, najmä formou vstupu do základného kapitálu."
  },
  "investor_type": {
    "value": "pe",
    "source_url": "https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr",
    "source_date": "2016-02-17",
    "quote": "Arca Capital je private equity skupina pôsobiaca predovšetký
… [skrátené, 1798 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c055.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c055.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c055.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c055 entity_kind: OK
c055 investor_type: OK
c055 stages: OK
OK    research/c055.json
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Limerock Fund Manager\" Slovakia", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Limerock Fund Manager" Slovakia"

Links: [{"title":"Limerock Fund Manager","url":"https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/limerock-fund-manager-kapitalova-investicia"},{"title":"limerock sk","url":"https://superscout.co/investor/limerock-sk"},{"title":"limerock fund manager","url":"https://superscout.co/investor/limerock-fund-manager"},{"title":"Ako to vyzerá s Venture capitalom na Slovensku?","url":"https://www.startitup.sk/limerock-fund-manager/"},{"title":"Buďte správne informovaný! Získajte prémiový účet TU","url":"https://podnikam.sk/?p=77733"},{"title":"Žltý melón získal významnú kapitálovú investíciu","url":"https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/"},{"title":"# Limerock Advisory","url":"https://altss.com/profile/limerock-advisory.md"},{"title":"Become a partner","url":"https://www.itapa.sk/20141-en/masterclassom-sprevadza/"},{"title":"www.crz.gov.sk","url":"https://www.crz.gov.sk//data/att/4853310.pdf"},{"title":"slovakia equity fundmanagers","url":"https://www.eif.org/files/attachments/slovakia-equity-fundmanagers.pdf"}]

The search turned up a few details about Limerock Fund Manager in Slovakia, though the sources don't all agree.

**Fund status:** Slovak Investment Holding (SIH) says it invested in a fund run by Limerock Investment Holding, formerly Limerock Fund Manager. That fund's investment period ran from 2014 to 2016, and it backed small and medium-sized enterprises
… [skrátené, 3342 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/limerock-fund-manager-kapitalova-investicia "Limerock|liquidation|2014|divest|fund|EUR|€" | head -20; echo XXX; python3 -I fetch.py https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/ "Limerock|JEREMIE|melón" | head; curl -sL -A "Mozilla/5.0" https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/ | grep -oE 'published_time" content="[^"]+"' | head -1
```

<details><summary>Výstup nástroja</summary>

```
>> Limerock Fund Manager | Slovak Investment Holding, a. s.
>> Limerock Fund Manager
>> Slovak Investment Holding was an investor in a fund managed by Limerock Investment Holding (formerly Limerock Fund Manager), which was responsible for the fund's management and the implementation of its investment strategy. The fund's investment period ran from 2014 to 2016 and focused on supporting small and medium-sized enterprises (SMEs) through equity investments made alongside private investors on a pari passu basis.
>> The fund has completed its divestment process and is currently undergoing liquidation.
XXX
>> Žltý melón získal významnú kapitálovú investíciu - SITA.sk
>> Žltý melón získal významnú kapitálovú investíciu
>> Foto: Žltý melón
>> BRATISLAVA 17. septembra (WBN/PR) – Na investícii do spoločnosti sa podieľali fond JEREMIE Co-Investment Fund, ktorý spravuje spoločnosť Limerock Fund Manager, investičná spoločnosť FTK Invest a pán Hendrik Bremer, dlhoročný partner pre finančné služby pre región strednej a východnej Európy v konzultačných spoločnostiach PwC a Roland Berger. Pán Bremer zároveň vstúpil do manažmentu spoločnosti a posilnil tak jej existujúci tím.
>> „Po dva a pol ročnom pôsobení spoločnosti na slovenskom trhu sme pred niekoľkými mesiacmi zahájili naše prvé investičné kolo s cieľom získať kapitál na akceleráciu ďalšieho rastu a realizáciu našich strategických plánov, najmä v oblastiach rozvoja produktového portfólia a služieb pre našich klientov a teritoriálnej exp
… [skrátené, 4220 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c057.json`
```
{
  "candidate_id": "c057",
  "name": "Limerock Fund Manager",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": null,
  "entity_kind": {
    "value": "investor",
    "source_url": "https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/",
    "source_date": "2015-09-17",
    "quote": "Spoločnosť Limerock Fund Manager na základe mandátu od Európskeho investičného fondu (www.eif.org) spravuje fond rizikového kapitálu a poskytuje tak start-up ako aj rozvojový kapitál pre investične atraktívne slovenské spoločnosti."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://sita.sk/zlty-melon-ziskal-vyznamnu-kapitalovu-investiciu/",
    "source_date": "2015-09-17",
    "quote": "Spoločnosť Limerock Fund Manager na základe ma
… [skrátené, 3133 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c057.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c057.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c057.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c057 entity_kind: OK
c057 investor_type: OK
c057 stages: OK
c057 ticket_min: OK
c057 ticket_max: OK
c057 aum: OK
OK    research/c057.json
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.forbes.sk/investicny-fond-zero-gravity-capital-hlada-mlade-firmy-rozdelit-ma-12-milionov-eur/ "Zero Gravity|milión|tiket|eur|20[12][0-9]" | head -25
```

<details><summary>Výstup nástroja</summary>

```
>> Investičný fond Zero Gravity Capital hľadá mladé firmy. Rozdeliť má 12 miliónov eur - Forbes Slovensko
>> Najbohatší Slováci 2026
>> október 2026
>> Najbohatší Slováci 2026
>> október 2026
>> Najbohatší Slováci 2026
>> október 2026
>> Najbohatší Slováci 2026
>> október 2026
>> Najbohatší Slováci 2026
>> Október v magazíne Forbes Slovensko už tradične patrí rebríčku Najbohatších Slovákov. A rok 2026 prináša opäť zásadné zmeny v poradí Slovákov s najväčšími majetkami. Tento rebríček je najprestížnejším prehľadom slovenských miliardárov a milionárov – podnikateľov, ktorí formujú slovenský biznis. Rozhovor Forbesu poskytol aj jeden zo stálych členov rebríčka Ivan Kmotrík. Rozhovor síce nevznikal ľahko, ale […]
>> Investičný fond Zero Gravity Capital hľadá mladé firmy. Rozdeliť má 12 miliónov eur
>> Jedným z fondov, ktorý sa spustil v utorok 12. novembra, je fond Zero Gravity Capital. Za úlohu bude mať alokovať 12 miliónov eur do začínajúcich firiem.
>> Štát tento rok odklepol finančnú injekciu 33 miliónov eur pre začínajúce firmy a začínajúcich podnikateľov. Peniaze prerozdeľuje National Development Fund II., ktorý je v správe Slovak Investment Holdingu (dcéra Slovenskej záručnej a rozvojovej banky). Spomínané milióny zverili trom súkromným investičným fondom. Jeden z nich, Zero Gravity Capital, spustil svoj fond v utorok 12. novembra.
>> Kde pôjde 33 miliónov vyčlenených pre startupy?
>> „V rámci nášho investičného fondu Zero Gravity Capital plánujeme alokovať do startupov na
… [skrátené, 2725 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Zero Gravity Capital\" investícia startup 2025 OR 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Zero Gravity Capital" investícia startup 2025 OR 2026"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/zerogravity"},{"title":"Zero Gravity Capital","url":"https://privateequitylist.com/investors/zero-gravity-capital"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/zero-gravity-capital"},{"title":"zero gravity capital","url":"https://superscout.co/investor/zero-gravity-capital"},{"title":"Updated: June 13, 2026","url":"https://incubatorlist.com/zero-gravity-capital"},{"title":"zero gravity capital","url":"https://www.vestbee.com/vc-list/zero-gravity-capital"},{"title":"zero gravity capital zerogravitycap com","url":"https://venturecapitalarchive.com/venture-funds/zero-gravity-capital-zerogravitycap-com"},{"title":"Zero Gravity Capital Overview","url":"https://slimpages.startupim.com/company_page/zero-gravity-capital"},{"title":"IncubatorListincubator listIncubatorList","url":"https://incubatorlist.com/best-venture-capital-firms-in-bratislava"},{"title":"Zero One Hundred · raw details","url":"https://startupim.com/investor/zero-one-hundred/raw"}]

I didn't find any confirmed Zero Gravity Capital investments dated 2025 or 2026. The most recent specific deal in the results is from 2024, though several profile pages were updated in 2026.

**What the firm is**
- Zero Gravity Capital is a Bratislava-based venture fund, founded in 20
… [skrátené, 3271 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://0100.vc https://www.0100.vc https://zerogravitycap.com https://www.zerogravitycap.com https://0100ventures.com; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done
```

<details><summary>Výstup nástroja</summary>

```
https://0100.vc 200 https://www.0100.vc/
https://www.0100.vc 200 https://www.0100.vc/
https://zerogravitycap.com 200 https://zerogravitycap.com/
https://www.zerogravitycap.com 200 https://zerogravitycap.com/
https://0100ventures.com 200 https://www.0100ventures.com/
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://www.0100.vc/ | head -100; echo XXXXX; N=3000 python3 -I fetch.py https://zerogravitycap.com/ | head -50
```

<details><summary>Výstup nástroja</summary>

```
Zero One Hundred | Main page
ABOUT USPORTFOLIOteamtestimonialswork with usCONTACT
A venture capital company founded by builders, with a unique ecosystem, backing the best startups from Emerging Europe and the Middle East.
An entrepreneurial ecosystem which adds value
Future winners require more than mere capital. We love working with founders side by side, helping their visions come to life. We’re also bringing unmatched value through the companies we have built: leading players in the innovation, technology, and investment sectors.
In past 10 years our team
In past
12 years our team
Started
10 companies
Invested
in 34 companies
Exited
4 companies
Organized
70+ international conferences
Welcomed
20,000 entrepreneurs to our events
Brought
10,000 investors to our events
Hosted
4,000 technical talents and operators at our community events
Built
1 unique entrepreneurial ecosystem
Our portfolio
Leading the AI revolution in cardiovascular care
Visit website
Unlocking the full earning power of mobile games
Visit website
Redefining car ownership
Visit website
Tech-driven platform for planning, executing, and financing renovations
Visit website
Smartest partner for personal and business finance
Visit website
AI Real Estate Analysis and Marketing Platform
Visit website
AI behaviour and experimentation layer for enterprises
Visit website
 Platform that simplifies HR, payroll, and attendance for SMEs
Visit website
Revolutionizing medical imaging
Visit website
Portfolio Intelligence Softw
… [skrátené, 5400 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL https://zerogravitycap.com/ | grep -oiE '<a[^>]*href="[^"]*"[^>]*>[^<]{0,40}new website' | head; curl -sL https://zerogravitycap.com/ | grep -oE 'href="https?://[^"]*0100[^"]*"' | sort -u; curl -sL https://www.0100.vc/ | grep -oE 'href="[^"]*"' | grep -vE '\.(css|js|png|svg|ico|woff)' | sort -u | head -30
```

<details><summary>Výstup nástroja</summary>

```
href="https://www.0100conferences.com/"
href="https://www.0100.vc/"
href="https://www.0100ventures.com"
href="/"
href="#arrow-link"
href="#footer"
href="#founders"
href="#history"
href="http://linkedin.com/in/kristína-mončeková-769022171"
href="https://3ipk.com"
href="https://auglio.com"
href="https://augmented-robotics.com"
href="https://biteberry.com/"
href="https://botbot.com/"
href="https://cdn.prod.website-files.com"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/63a1996cd6b229ab7152645e_Dusan-Duffek.webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/63a19a808fe687d23ff6fb74_Martin%20Herma.jpeg"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/6486d640629a3c97710b69bd_Adam%20Durica.webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/6486d67350b15da4c3ae0519_Michal%20Csonga.webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/65083f38c54363b3f1ba9f8b_58b34c6b-bc22-4def-9eb4-7b6a66c001fa%20(1).webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/6508411f2037ee63e0db7ce8_6b3de2c4-1280-46b6-977b-e57b4966ec9b%20(1)%20(1).webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/672b604eab3ac323b5aaa354_001.webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/672b61d1c25b420e8d0b442e_6486d64c55a6b2b46a44f37a_Kristina%20Moncekova%20(1).webp"
href="https://cdn.prod.website-files.com/6391dbf9c8c8ea3b22b83f03/672b61da8039ed280663f63f_6
… [skrátené, 2206 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Zero One Hundred\" fund II investment 2025 OR 2026 startup raises", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Zero One Hundred" fund II investment 2025 OR 2026 startup raises"

Links: [{"title":"Zero One Hundred Launches €25M Fund II","url":"https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-25m-fund-ii"},{"title":"therecursive.com","url":"https://therecursive.com/?p=42210"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/zero-one-hundred-launches-25m-fund-ii"},{"title":"Slovakia's Zero One Hundred targets €60 million fundraise to diversify CEE venture play","url":"https://tech.eu/2022/12/21/slovakias-zero-one-hundred-targets"},{"title":"Zero One Hundred Launches Fund II","url":"https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-fund-ii"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/zero-one-hundred-launches-fund-ii"},{"title":"zero one hundred fund to invest in cee startups","url":"https://www.techloy.com/zero-one-hundred-fund-to-invest-in-cee-startups/"},{"title":"Podpořili největší startupové naděje na Slovensku. S novým fondem mají i pro české firmy 1,5 miliardy","url":"https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/"},{"title":"zero one hundred","url":"https://privateequitylist.com/investors/zero-one-hundred"},{"title":"Zero One Hundred","url":"https://startupim.com/investor/zero-one-hundred"}]

Zero One Hundred launched its second fund in September 2025, and the search turned up no specific 2026 deals.

*
… [skrátené, 2902 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL -A "Mozilla/5.0" "https://therecursive.com/?p=42210" -o /dev/null -w "%{url_effective}\n"; python3 -I fetch.py "https://therecursive.com/?p=42210" "Zero One Hundred|€|Biteberry|Reno|Medannot|Palm|IntellCRE|Zero Gravity|pre-seed|ticket" | head -20
```

<details><summary>Výstup nástroja</summary>

```
https://www.therecursive.com/?p=42210
>> Poland's BGK Launches €114M Vinci Space Tech Fund, the Country's 1st Fund for Space Companies
>> The fund will invest around €2.3–23 million in each of 15 to 20 companies working on satellites, Earth observation, propulsion and space data. ICEYE has joined as a strategic partner.
>> Estonia's Golbriak Space Raises €4M to Scale Laser Communications for Satellites
>> The Tallinn-based spacetech, eight years in the making, raised a €4M seed co-led by Join Capital and PhotonVentures to scale manufacturing of its in-house laser communication terminals for satellites and airborne platforms, already shipping to paying customers.
>> Romanian-founded Siena Raises Over €15M Series A to Build an "Agent of Record" for Consumer Brands
>> Slovak Sensible Biotechnologies Secures €42M for Cell-Based mRNA Platform
>> Ukraine’s Buntar Aerospace Raises €14.3M for Drones Built to Operate Without GPS
>> Ukrainian defence tech company Buntar Aerospace has raised €14.3M ($16M)in a round led by Freedom Fund and an undisclosed international private equity fund. Its total funding is now $30M, and the money will go toward scaling its Buntar-3 reconnaissance drone and Copilot mission software.
>> CEE Startup & Tech Weekly: New €70M+ Fund Backing CEE
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "therecursive Zero One Hundred €25M Fund II Biteberry Reno Home Medannot", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "therecursive Zero One Hundred €25M Fund II Biteberry Reno Home Medannot"

Links: [{"title":"Founded Year","url":"https://www.cbinsights.com/company/intellcre/"},{"title":"Zero One Hundred Launches Fund II","url":"https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-fund-ii"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/zero-one-hundred-launches-fund-ii"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/reno/financials"},{"title":"$420,000 Marks A New Record High For Median Home Prices in Reno","url":"https://www.2news.com/420-000-marks-a-new-record-high-for-median-home-prices-in-reno/image_abe88983-c7d7-529a-b80c-59ee3c4ebb11.html"},{"title":"© All Rights Reserved 2026 | Privacy Policy","url":"https://knpr.org/knpr/2021-01-11/median-reno-existing-home-price-reaches-500k-for-first-time"},{"title":"www.vcbacked.co","url":"https://www.vcbacked.co/company/biteberry"},{"title":"reno.gov","url":"https://reno.gov/home/showpublisheddocument/89203/638028029347170000"},{"title":"Reno Seed Fund","url":"https://privateequitylist.com/investors/reno-seed-fund"}]

The search turned up coverage of Zero One Hundred's second fund, though nothing confirmed the €25M figure in your query.

**Fund II:** Zero One Hundred has launched Fund II and expanded its portfolio, as reported by The Recursive. According to a Polish-language report that cites The Recursive, the fund will put 70% of its capital into pre-seed an
… [skrátené, 2830 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && for u in https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-25m-fund-ii https://finder.techleap.nl/news/feed/zero-one-hundred-launches-25m-fund-ii https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-fund-ii; do echo "== $u"; python3 -I fetch.py "$u" "Zero One Hundred|€|Biteberry|Medannot|2025" | head -10; done
```

<details><summary>Výstup nástroja</summary>

```
== https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-25m-fund-ii
== https://finder.techleap.nl/news/feed/zero-one-hundred-launches-25m-fund-ii
== https://ecosystem.madrimasd.org/news/feed/zero-one-hundred-launches-fund-ii
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Zero One Hundred druhý fond 25 miliónov eur Duriča 2025", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Zero One Hundred druhý fond 25 miliónov eur Duriča 2025"

Links: [{"title":"Podpořili největší startupové naděje na Slovensku. S novým fondem mají i pro české firmy 1,5 miliardy","url":"https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/"},{"title":"zero one hundred","url":"https://www.cbinsights.com/investor/zero-one-hundred"},{"title":"zero one hundred targets eur 15m for new funds first close","url":"https://www.unquote.com/cee/news/3028445/zero-one-hundred-targets-eur-15m-for-new-funds-first-close"},{"title":"60-miliónový balík pre startupy je Slovákom blízko ako nikdy doposiaľ. Prestížna podpora už čaká","url":"https://www.startitup.sk/?p=742627"},{"title":"Zero One Hundred","url":"https://app.dealroom.co/companies/zero_one_hundred"},{"title":"adam durica","url":"https://cc.cz/author/adam-durica/"},{"title":"Financial Transaction:","url":"https://data.kando.tech/company/zyncro-tech-sl/funding/zyncro-tech-sl-funding-round-series-2011-04-01"},{"title":"Startupy zo Slovenska získali kľúč k najbohatším trhom planéty: Miliardové biznisy majú na dosah","url":"https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/"},{"title":"Adam Ďurica","url":"https://sk.linkedin.com/in/adamdurica"}]

I couldn't find any source confirming a 25 million euro figure for Zero One Hundred's second fund, so I can't verify that part of your 
… [skrátené, 3057 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/ "Zero One Hundred|fond|milión|Biteberry|Medannot|IntellCRE|seed" | head -20; curl -sL -A "Mozilla/5.0" https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/ | grep -oE 'published_time" content="[^"]+"' | head -1; echo XX; python3 -I fetch.py https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/ "Zero|23 milion|Gravity|20[12][0-9]" | head -12
```

<details><summary>Výstup nástroja</summary>

```
>> Fond Zero One Hundred a platforma Investopia zo Spojených arabských emirátov spájajú sily. Cieľom je, aby startupy z východnej Európy získali prístup k novým trhom a kapitálu.
>> Tento prelomový krok je výsledkom spolupráce stredoeurópskeho venture kapitálového fondu Zero One Hundred a investičnej platformy Investopia zo Spojených arabských emirátov, ktorá patrí pod vedenie ministra hospodárstva Spojených arabských emirátov, Abdullaha Bin Touqa Ala.
>> Zero One Hundred, známy svojou špecializáciou na early-stage startupy, týmto partnerstvom buduje most medzi rýchlo rastúcou CEE startupovou scénou a Blízkym východom, kde sa hospodárstvo čoraz viac orientuje na inovácie, technológie a znalostnú ekonomiku.
>> „Spojené arabské emiráty sú jednou z najsilnejších ekonomík Blízkeho východu, ktorá sa navyše v súčasnosti naplno transformuje z ropného exportu na znalostnú ekonomiku s dôrazom na súkromné podnikanie, moderné technológie, inovácie a umelú inteligenciu,“ vysvetľuje partner fondu Zero One Hundred Dušan Duffek.
>> zdroj: Zero One Hundred
>> Fond Zero One Hundred, ktorý svoje korene zapustil v Bratislave, dnes funguje ako významný hráč na poli venture kapitálu v CEE regióne. S kanceláriami v Prahe, Bratislave, na Cypre a najnovšie aj v Abú Zabí si kladie za cieľ podporovať technologické startupy v raných fázach ich rastu. Ich silnou stránkou je globálna sieť investorov a schopnosť preniesť úspešné startupy z východnej Európy na svetové trhy.
>> S portfóliom investícií, ako 
… [skrátené, 5065 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Biteberry investícia \"Zero One Hundred\"", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Biteberry investícia "Zero One Hundred""

Links: [{"title":"Zero One Hundred","url":"https://oslo.dealroom.co/companies/zero_one_hundred/team"},{"title":"zero one hundred","url":"https://www.cbinsights.com/investor/zero-one-hundred"},{"title":"Berry, fintech argentina, cierra ronda de US$2M con Coinbase","url":"https://ecosistemastartup.com/berry-fintech-argentina-cierra-ronda-de-us2m-con-coinbase/"},{"title":"app.dealroom.co","url":"https://app.dealroom.co/companies/bite_investments/team"},{"title":"Bite Investments Announces $25M in Funding from NewSpring Growth","url":"https://www.crowdfundinsider.com/2025/10/253521-bite-investments-announces-25m-in-funding-from-newspring-growth/"},{"title":"Bite Investments Announces $25M in Funding from NewSpring Growth","url":"https://www.crowdfundinsider.com/?p=253521"},{"title":"Berry, fintech argentina, cierra ronda de US$2M con Coinbase","url":"https://ecosistemastartup.com/?p=114969"},{"title":"bite investments raises 25m","url":"https://www.finextra.com/newsarticle/46685/bite-investments-raises-25m"},{"title":"Product Avatar Image","url":"https://www.g2.com/sellers/bite-investments"}]

Vo výsledkoch vyhľadávania som nenašiel nič, čo by potvrdzovalo, že Zero One Hundred investovala do spoločnosti Biteberry. Našiel som len informácie o samotnej investorskej spoločnosti a o iných firmách s podobným názvom.

**Zero One Hundred:** Zero One Hundred je venture capital firma, ktorá sa zameriava na investície
… [skrátené, 2476 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Zero One Hundred\" investovala OR investoval OR investment led seed 2026", "mode": "standard", "allowed_domains": ["startitup.sk", "vestbee.com", "therecursive.com", "forbes.sk", "cc.cz", "trend.sk", "eu-startups.com"]}
```

<details><summary>Výstup nástroja</summary>

```
API Error: 400 The following domains are not accessible to our user agent: ['trend.sk']. Read more: https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Zero One Hundred\" startup round 2025 2026", "mode": "standard", "allowed_domains": ["startitup.sk", "vestbee.com", "therecursive.com", "forbes.sk", "cc.cz", "eu-startups.com"]}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Zero One Hundred" startup round 2025 2026"

Links: [{"title":"Zero One Hundred","url":"https://www.eu-startups.com/investor/zero-one-hundred/"},{"title":"Zero One Hundred Launches Fund II and Expands Portfolio - TheRecursive.com","url":"https://www.therecursive.com/zero-one-hundred-0100vc-launches-fund-ii-and-expands-portfolio/"},{"title":"Zero One Hundred Signs Agreement to Connect CEE Startups with UAE Investors","url":"https://therecursive.com/zero-one-hundred-signs-agreement-to-connect-cee-startups-with-uae-investors/"},{"title":"Zero One Hundred","url":"https://www.vestbee.com/vc-list/zero-gravity-capital"},{"title":"TOP CEE Startups That Closed Investment Rounds In June 2023","url":"https://www.vestbee.com/insights/articles/top-cee-funding-rounds-closed-in-june-2023"},{"title":"Top CEE funding rounds closed in November 2024","url":"https://www.vestbee.com/insights/articles/top-cee-funding-rounds-closed-in-november-2024"},{"title":"Zero One Hundred - CzechCrunch","url":"https://cc.cz/tag/zero-one-hundred/"},{"title":"Startupy zo Slovenska získali kľúč k najbohatším trhom planéty: Miliardové biznisy majú na dosah","url":"https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/"},{"title":"Fond Zero One Hundred má 1,5 miliardy pro středoevropské startupy - CzechCrunch","url":"https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-1
… [skrátené, 3191 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.therecursive.com/zero-one-hundred-0100vc-launches-fund-ii-and-expands-portfolio/ "Zero One Hundred|€|Biteberry|Reno|Medannot|Palm|IntellCRE|pre-seed|2025" | head -25; curl -sL -A "Mozilla/5.0" https://www.therecursive.com/zero-one-hundred-0100vc-launches-fund-ii-and-expands-portfolio/ | grep -oE 'published_time" content="[^"]+"' | head -1
```

<details><summary>Výstup nástroja</summary>

```
>> Zero One Hundred Launches Fund II and Expands Portfolio - TheRecursive.com
>> Zero One Hundred Launches Fund II and Expands Portfolio
>> DealsEcosystemInvestorsNewsStartups0100Zero One HundredCEEMENA
>> September 23, 2025 ∙ 1 min read
>> Presto Tech Horizons Steps In as Sole European Backer of Firehawk’s Over €50M Round
>> Estonia's Golbriak Space Raises €4M to Scale Laser Communications for Satellites
>> Romanian-founded Siena Raises Over €15M Series A to Build an "Agent of Record" for Consumer Brands
>> Ukraine’s Buntar Aerospace Raises €14.3M for Drones Built to Operate Without GPS
>> NATO-Trusted Osavul Raises €8.5M to Spot Hybrid Attacks Before They Strike
published_time" content="2025-09-23T15:49:45.000Z"
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I -c "
import sys; sys.path.insert(0,'.')
from fetch import text_of
t=text_of('https://www.therecursive.com/zero-one-hundred-0100vc-launches-fund-ii-and-expands-portfolio/')
i=t.find('1 min read'); print(t[i:i+3500])
"
```

<details><summary>Výstup nástroja</summary>

```
1 min read
 Share
 Written by
Lenka Vranová
Lenka is a curious observer of technology, culture, and shifting human narratives. With a background in linguistics and media, she tries to blend analytical insight with a lyrical voice. Writes about 
 Editor’s Choice
The Silent M&A Wave: When the Next Funding Round Becomes Less Attractive Than a Sale
How Bulgaria Built One of Europe’s Fastest-Growing Battery Markets
Start Up Bulgaria! Crossroads 2026
This post is for subscribers only
Sign up now to read the post and get access to the full library of posts for subscribers only.
 Sign up now
 Already have an account? Sign in
 Newer post
Presto Tech Horizons Steps In as Sole European Backer of Firehawk’s Over €50M Round
 Older post
Fixing Fundraising: The Digital Toolkit Redefining How Startups Raise Capital
 You might also like
CEE Startup & Tech Weekly: Bulgarian-Founded Varda Space Hits $1.6B Valuation After $250M Raise
 by
 The Recursive
Estonia's Golbriak Space Raises €4M to Scale Laser Communications for Satellites
 by
 The Recursive
Romanian-founded Siena Raises Over €15M Series A to Build an "Agent of Record" for Consumer Brands
 by
 Yoana Stanislavova
Ukraine’s Buntar Aerospace Raises €14.3M for Drones Built to Operate Without GPS
 by
 Yoana Stanislavova
NATO-Trusted Osavul Raises €8.5M to Spot Hybrid Attacks Before They Strike
 by
 The Recursive
 Newsletter
Get all the latest posts delivered straight to your inbox.
 Subscribe
 Processing your application
 Please check your i
… [skrátené, 2154 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.vestbee.com/insights/articles/top-cee-funding-rounds-closed-in-november-2024 "Zero One Hundred|SuperScale" | head; echo XX; python3 -I fetch.py https://www.eu-startups.com/investor/zero-one-hundred/ "€|Series|seed|Emerging|Fund II|ticket|invest" | head -12; echo XX; python3 -I fetch.py https://cc.cz/tag/zero-one-hundred/ "Zero One Hundred|20[12][0-9]" | head -20
```

<details><summary>Výstup nástroja</summary>

```
>> SuperScale, €1.14M in Series A
>> Recent funding sources: Across Private Investments, LevelUp Ventures, Zero One Hundred, Venture to Future Fund, Strecko Investments
>> SuperScale provides a growth platform to scale blockchain apps and games profitably. Powered by SuperInsights, its analytics engine predicts strategies for commercial success. The current funding will be spent on the startup’s new SuperPlatform, which unifies data from 40+ sources, offering an AI-driven, all-in-one view of business performance.
XX
>> Get Tickets
>> Investor Database
>> Get Tickets
>> Investor Database
>> Get Tickets
>> Investor Database
>> Zero One Hundred is a venture capital company founded by builders, supported by a unique entrepreneurial ecosystem, backing the best startups from Emerging Europe. With our Fund II, we go all-in in Emerging Europe. 21 countries, a 200M population, local talent in the global spotlight, and untapped opportunities. From the Baltics to Central Europe to the Balkans and Eastern Mediterranean, we support the best startups on their path to success. With our unique strategy of complementary investments combined with state-of-the-art venture capital technology we capture the most lucrative regional returns.
>> Investor Type: VC Firm
>> Investment Areas: Blockchain, E-Commerce, AR/VR, Fintech, Mobile Games, AI, B2B, Healthcare
>> Typical Investment: €100k-€1.5M
>> Funding Stage: Series A/B
XX
>> Zero One Hundred - CzechCrunch
>> Money Maker 2026
>> Zero One Hundred
… [skrátené, 2122 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "\"Zero One Hundred\" Powerful Medical OR Readmio OR Medannot OR SuperScale investment round", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: ""Zero One Hundred" Powerful Medical OR Readmio OR Medannot OR SuperScale investment round"

Links: [{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/company/medannot"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/powerful-medical-secures-multi-million-investment"},{"title":"Powerful Medical","url":"https://www.sih.sk/en/portfolio/powerful-medical"},{"title":"top of page","url":"https://www.symsite.sk/single-post/powerful-medical-landed-6-2m-investment"},{"title":"Slovak startup Powerful Medical raises €6.2M in a seed round","url":"https://en.ain.ua/tag/slovakia/page/7"},{"title":"onemednet expands into 1 5b healthcare data annotation market with medcase","url":"https://www.barchart.com/story/news/35005573/onemednet-expands-into-1-5b-healthcare-data-annotation-market-with-medcase"},{"title":"OneMedNet Expands Into $1.5B Healthcare Data Annotation Market With MedCase","url":"https://www.nasdaq.com/press-release/onemednet-expands-15b-healthcare-data-annotation-market-medcase-2025-09-24"},{"title":"onemednet expands 15b healthcare data annotation market medcase","url":"https://www.santelog.com/actualites-sante-nasdaq/onemednet-expands-15b-healthcare-data-annotation-market-medcase"},{"title":"Meta's Scale AI Acquisition: The Healthcare Opportunity Left Behind","url":"https://www.onhealthcare.tech/p/metas-scale-ai-acquisition-the-healthcare"},{"title":"medinote ai"
… [skrátené, 4952 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "Readmio pohádky aplikace investice únor 2026 kolo", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Readmio pohádky aplikace investice únor 2026 kolo"

Links: [{"title":"Doslova pohádková investice. Aplikace Readmio, která na děti při čtení sama mluví, získala 13 milionů korun","url":"https://cc.cz/doslova-pohadkova-investice-aplikace-readmio-ktera-na-deti-pri-cteni-sama-mluvi-ziskala-13-milionu-korun/"},{"title":"Jejich příběhy zaujaly Brazilce i investory. Pohádkové Readmio získalo další peníze a míří do Indie","url":"https://cc.cz/jejich-pribehy-zaujaly-brazilce-i-investory-pohadkove-readmio-ziskalo-dalsi-penize-a-miri-do-indie/"},{"title":"pohadky nikdy nebyly dojemnejsi aplikace readmio babickam umoznuje predcitat vnoucatum i na dalku","url":"https://forbes.cz/pohadky-nikdy-nebyly-dojemnejsi-aplikace-readmio-babickam-umoznuje-predcitat-vnoucatum-i-na-dalku/"},{"title":"Přeskočit navigaci","url":"https://www.rohlik.cz/tema/readmio-na-rohliku"},{"title":"cc.cz","url":"https://cc.cz/tag/readmio/"},{"title":"czech readmio secures a eur500k investment","url":"https://en.ain.ua/2025/01/22/czech-readmio-secures-a-eur500k-investment"},{"title":"Autor textu MediaGuru","url":"https://www.mediaguru.cz/readmio-diky-investici-25-mil-kc-vstoupi-do-nemecka-a-polska"},{"title":"Back to feed","url":"https://finder.techleap.nl/news/feed/readmio-secures-500k-from-simpact-ventures"},{"title":"CEE VC SUMMIT 2026","url":"https://vestbee.com/insights/articles/readmio-secures-1-m"}]

Ve februáru 2026 získala česká aplikace Readmio nové kolo financování ve výši 1
… [skrátené, 2642 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://vestbee.com/insights/articles/readmio-secures-1-m "Zero One Hundred|ZAKA|Readmio|2026" | head -10; echo XX; python3 -I fetch.py https://cc.cz/jejich-pribehy-zaujaly-brazilce-i-investory-pohadkove-readmio-ziskalo-dalsi-penize-a-miri-do-indie/ "Zero|Zaka|Depo|20[12][0-9]" | head -10
```

<details><summary>Výstup nástroja</summary>

```
>> Czech fairy tale app Readmio secures €1M to drive global expansion | Vestbee
>> February 5, 2026·2 min read
>> Czech fairy tale app Readmio secures €1M to drive global expansion
>> Prague-based Readmio, which develops interactive children’s story apps with sound and learning features, has secured €1 million in new funding from Simpact Ventures, with support from ZAKA VC, Zero One Hundred, and DEPO Ventures, as Vestbee was informed.
>> Founded in 2020 by Slovak entrepreneurs Ilya Novodvorskiy and Jozef Šimko, Readmio is a digital storytelling platform that develops interactive fairy tales and educational content for children. The app’s library contains over 3,277 stories in nine languages, including English, Slovak, Polish, German, Spanish, Portuguese, Italian, Czech, and Hindi.
>> Using an offline voice recognition system, Readmio detects when a parent reads aloud and automatically adds synchronized sound effects and music, from chirping birds to crackling fires, to enhance engagement.
>> The app has been downloaded by over 2 million users in 135 countries, with more than 300,000 monthly active users and 50,000 families holding paid subscriptions. Readmio is available on iOS and Android, allowing children to listen to pre-recorded stories or enjoy interactive reading sessions with their parents, supporting language development, literacy, and cognitive skills.
>> Readmio will use the €1 million investment to accelerate its global expansion into Asia, the US, and Latin Ameri
… [skrátené, 2829 znakov]
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c059.json`
```
{
  "candidate_id": "c059",
  "name": "Zero One Hundred (0100 Ventures)",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK", "CZ", "CY", "AE"],
  "website": "https://www.0100.vc/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.0100.vc/",
    "quote": "A venture capital company founded by builders, with a unique ecosystem, backing the best startups from Emerging Europe and the Middle East."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://www.startitup.sk/startupy-zo-slovenska-ziskali-kluc-k-najbohatsim-trhom-planety-miliardove-biznisy-maju-na-dosah/",
    "source_date": "2024-12-17",
    "quote": "Fond Zero One Hundred, ktorý svoje korene zapustil v Bratislave, dnes funguje ako významný hráč na poli venture k
… [skrátené, 3397 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c059.json (file state is current in your context — no need to Read it back)
```

</details>

## Claude · 2026-10-09 12:38:27 UTC

Teraz c058 ako duplikát a doplním Readmio do c049.

**Nástroj `Write`**

`/home/filip/investor-db/research/c058.json`
```
{
  "candidate_id": "c058",
  "name": "Zero Gravity Capital",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://zerogravitycap.com/",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.forbes.sk/investicny-fond-zero-gravity-capital-hlada-mlade-firmy-rozdelit-ma-12-milionov-eur/",
    "quote": "Jedným z fondov, ktorý sa spustil v utorok 12. novembra, je fond Zero Gravity Capital. Za úlohu bude mať alokovať 12 miliónov eur do začínajúcich firiem."
  },
  "investor_type": {
    "value": "vc",
    "source_url": "https://cc.cz/podporili-nejvetsi-startupove-nadeje-na-slovensku-s-novym-fondem-maji-i-pro-ceske-firmy-15-miliardy/",
    "source_date": "2022-12-20",
    "quote": "Investiční aktivity Zero One Hundred začaly 
… [skrátené, 1898 znakov]
```

**Nástroj `Bash`**

```bash
.venv/bin/python -I - <<'EOF'
import json
p="research/c049.json"; d=json.load(open(p))
d["investments"].insert(0,{
 "company":"Readmio","deal_date":"2026-02-05",
 "source_url":"https://vestbee.com/insights/articles/readmio-secures-1-m","source_date":"2026-02-05",
 "quote":"Prague-based Readmio, which develops interactive children’s story apps with sound and learning features, has secured €1 million in new funding from Simpact Ventures, with support from ZAKA VC, Zero One Hundred, and DEPO Ventures, as Vestbee was informed."})
d["investments"]=sorted(d["investments"],key=lambda x:x["deal_date"],reverse=True)
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
EOF
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c049.json research/c058.json research/c059.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c049.json research/c058.json research/c059.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c058.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c049 entity_kind: OK
c049 investor_type: OK
c049 sectors: OK
c049 stages: OK
c049 aum: OK
c049 inv0: OK
c049 inv1: OK
c049 inv2: OK
c058 entity_kind: OK
c058 investor_type: OK
c058 aum: OK
c059 entity_kind: OK
c059 investor_type: OK
c059 sectors: OK
c059 stages: OK
c059 ticket_min: OK
c059 ticket_max: OK
c059 aum: OK
c059 inv0: OK
OK    research/c049.json
OK    research/c058.json
OK    research/c059.json
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu-webout-ten-ziskava-spolu-165-miliona-eur-a-mieri-do-silicon-valley" "Seed Starter|Webout|eur|fond|investuje|2026|startup" | head -30
```

<details><summary>Výstup nástroja</summary>

```
>> Seed Starter Slovenskej sporiteľne investuje 400-tisíc eur do startupu Webout. Ten získava spolu 1,65 milióna eur a mieri do Silicon Valley
>> Seed Starter Slovenskej sporiteľne investuje 400-tisíc eur do startupu Webout. Ten získava spolu 1,65 milióna eur a mieri do Silicon Valley
>> Seed Starter Slovenskej sporiteľne vedie investičné kolo do českého startupu Webout, ktorý ukazuje, že video nemusí byť len o pozornosti, ale aj o merateľných tržbách. Platforma na hyperpersonalizáciu videa dnes funguje u veľkých značiek aj športových klubov a po piatich rokoch na trhu sa pripravuje na vstup do USA. Ďalšími investormi sú fondy Energy Venture Pals a JIC Ventures.
>> Startup Webout pôsobí na trhu už päť rokov, počas ktorých si vybudoval silné portfólio klientov. Jeho technológiu pre videokampane, ktorá dokáže každému divákovi v reálnom čase ponúknuť obsah prispôsobený na mieru, využívajú značky ako Česká spořitelna, Komerční banka, Allianz, Notino či športové kluby AC Sparta Praha a FC Bruggy. Webout prináša svojim klientom až desaťnásobne vyššiu mieru preklikov a mieru dokončenia sledovania dosahujúcu 95 %. Silu platformy dokazuje aj kampaň pre AC Sparta Praha, ktorá vygenerovala 1,7 milióna pozretí úplne organicky, bez akejkoľvek investície do platenej reklamy. Len v roku 2025 dosiahla dvanásťčlenná firma obrat presahujúci 600-tisíc eur.
>> „Personalizácia video obsahu sa stane štandardom digitálnej komunikácie. Naša platforma firmám ukazuje, že video nie je len o pozornosti,
… [skrátené, 6756 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu-webout-ten-ziskava-spolu-165-miliona-eur-a-mieri-do-silicon-valley" "už investoval do deviatich" | cut -c1-1500
```

**Nástroj `WebSearch`**

```json
{"query": "Seed Starter Slovenskej sporiteľne investuje 2025 startup", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
>> Korporátny venture kapitálový program Seed Starter hľadá podnikateľské plány so silnou víziou a hodnotou pre zákazníkov. Program ponúka nielen investície, ale aj profesionálnu inkubáciu, obsahovú podporu a širokú sieť partnerov a zákazníkov, s ktorými dokáže startupy prepojiť a pomôcť im vstúpiť na reálny trh. Seed Starter sa zameriava na startupy, ktoré by v ideálnom prípade mohli mať synergický efekt s finančnou inštitúciou. Niektoré nádejné startupy tak majú potenciál následne ponúkať svoje produkty aj prostredníctvom rozsiahlej distribučnej siete skupiny Erste. Seed Starter Slovenskej sporiteľne už investoval do deviatich startupov Blockmate, SmartHead, Vestberry, Eatster, Resitech, Inte
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Seed Starter Slovenskej sporiteľne investuje 2025 startup"

Links: [{"title":"Michal a Karel získali 1,65 milióna eur. Teraz s revolučným nápadom mieria do Silicon Valley","url":"https://www.startitup.sk/?p=1207932"},{"title":"Seed Starter Slovenskej sporiteľne hlási prvú investíciu: podporil slovenský startup SmartHead","url":"https://sita.sk/seed-starter-slovenskej-sporitelne-hlasi-prvu-investiciu-podporil-slovensky-startup-smarthead/"},{"title":"Slovensko je čierna diera startupov, zachrániť ho ide táto spoločnosť. Investovať u nás chce 5 miliónov eur","url":"https://www.startitup.sk/?p=664120"},{"title":"slsp infografika 2025","url":"https://cdn0.erstegroup.com/content/dam/sk/slsp/www_slsp_sk/Aktuality/slsp-infografika-2025.pdf"},{"title":"Najlepší startup získal 250 000 eur. Tieto firmy sú budúcnosťou slovenskej ekonomiky","url":"https://www.startitup.sk/najlepsi-startup-ziskal-250-000-eur-tieto-firmy-su-buducnostou-slovenskej-ekonomiky/"},{"title":"Toto je nová generácia slovenských superpodnikateľov. Tieto domáce firmy uvidíš všade","url":"https://www.startitup.sk/?p=698215"},{"title":"Slovenská spořitelna bude investovat do startupů po vzoru České. Připravených má přes 120 milionů","url":"https://cc.cz/ceska-sporitelna-jde-podporovat-startupy-i-na-slovensko-pro-tamni-mlade-firmy-ma-pres-120-milionu/"},{"title":"Šéf Slovenskej sporiteľne: Slovensko by malo skvalitniť školstvo. Naša ekonomika má zásadný problém","url":"https://www.startitu
… [skrátené, 3557 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py "https://cc.cz/ceska-sporitelna-jde-podporovat-startupy-i-na-slovensko-pro-tamni-mlade-firmy-ma-pres-120-milionu/" "Seed Starter|milion|eur|tiket|seed|fintech|202[0-9]" | head -15; echo XX; for u in https://www.seedstarter.sk https://seedstarter.sk; do curl -sL -o /dev/null -w "$u %{http_code} %{url_effective}\n" --max-time 15 $u; done
```

<details><summary>Výstup nástroja</summary>

```
>> Money Maker 2026
>> Startupy – 08. 9. 2022 – 2 min čtení
>> Slovenská spořitelna bude investovat do startupů po vzoru České. Připravených má přes 120 milionů
>> Seed Starter v Česku během posledních dvou let zainvestoval 100 milionů. U sousedů bude fungovat pod hlavičkou Slovenské spořitelny.
>> Foto: Seed Starter
>> Jiří Skopový vede program Seed Starter
>> Pět milionů eur, tedy v přepočtu více než 123 milionů korun, si připravila Slovenská spořitelna na první fázi podpory startupů na Slovensku. Tam se totiž právě rozšiřuje program Seed Starter, projekt, který už přes dva roky běží v Česku. Spustila ho tu Česká spořitelna a zalíbil se její matce, skupině Erste, která v tuzemsku i na Slovensku banky provozuje.
>> „Bylo jen otázkou času, kdy tento ověřený model převedeme do dalších zemí. Jsem rád, že je to právě u našich sousedů na Slovensku, kde dosud CVC a inkubační program zaměřující se na technologické startupy v seed fázi chyběl,“ vysvětluje Jiří Skopový, vedoucí programu Seed Starter.
>> Do fondu podle něj poputují další stovky milionů. „Protože opravdu vidíme přidanou hodnotu pro klienty i Spořitelnu jako takovou, tohle je totiž cesta, jak se může modernizovat a zrychlit. Když zvažujeme, zda do nějaké firmy investujeme, měřítko je, aby služba, kterou startup vyvíjí, buď zlepšila finanční zdraví našich klientů, nebo zlepšila naše vlastní vnitřní procesy,“ vysvětlil motivaci.
>> Na Slovensku se přidává ještě snaha o krok ke změně celé tamní scény. Spořitelna si předsta
… [skrátené, 3203 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && N=5000 python3 -I fetch.py https://www.seedstarter.sk/sk/uvod | head -80
```

<details><summary>Výstup nástroja</summary>

```
Vytvorte niečo, čo pretrvá do budúcnosti | Seed Starter Slovenskej sporiteľne
 Preskočiť navigáciu
 Ísť na Newsletter
Pomáhame startupom
rásť rýchlejšie
Prinášame financie, skúsenosti a príležitosti na spoluprácu s bankou
Chcem investíciuZistiť viac
Ako to robíme?
Ako banka s 200-ročnou tradíciou ponúkame financovanie, expertné know-how aj silné prepojenie na biznisové prostredie. Investujeme tam, kde vidíme víziu, tím a plán, ktoré pretrvajú.
Nie sme klasický VC fond. Okrem investícií aktívne rozvíjame slovenský startupový ekosystém a organizujeme vlastný Startup Bootcamp. Veríme v spoločný dlhodobý rast, nie rýchle výnosy.
 Pozrieť video
Investičná stratégia
Naše investície sú smart money vo svojej najpraktickejšej podobe. Sme oveľa viac hands-on, než by ste od korporácie čakali – a vďaka skupine Erste otvárame dvere aj za hranicami Slovenska.
Pre-seed a seed
investičné kolá
 Veľkosť investície:
 200 000 € – 1 000 000 €
 Menšinový
 akcionár
 Investícia formou
 CLA alebo Equity
Investičný horizont:
 4 – 7 rokov
Slovenskí founderi/slovenské startupy
 Piloty a synergie so Slovenskou sporiteľňou
 Spolufinancovanie
 s VC partnermi
Čo môžete očakávať
Pošlite svoj projekt
Vyplníte krátky formulár a nahráte pitch deck/key podklady.
Prvý kontakt
Investičný manažér s vami prejde vašu víziu, trh a plány.
Prvé hlasovanie
 Investičná komisia vyhodnotí, či má váš projekt potenciál.
Osobné stretnutie
Predstavíte riešenie komisii a preberieme možné smery spolupráce.
Investícia alebo pilot

… [skrátené, 3046 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "TrollWall AI investícia Seed Starter 2026", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "TrollWall AI investícia Seed Starter 2026"

Links: [{"title":"ai proti nenavisti na internete startup trollwall ai ziskal investiciu vo vyske 800 000 eur","url":"https://www.sih.sk/en/aktuality/ai-proti-nenavisti-na-internete-startup-trollwall-ai-ziskal-investiciu-vo-vyske-800-000-eur"},{"title":"AI Against Online Hate: Startup TrollWall AI Secures €800,000 Investment","url":"https://www.sih.sk/en/aktuality/ai-against-online-hate-startup-trollwall-ai-secures-800-000-investment"},{"title":"D99F0E46 732E 4FD3 A384 7A2735E91511","url":"https://funding.tech.eu/companies/D99F0E46-732E-4FD3-A384-7A2735E91511"},{"title":"trollwall ai","url":"https://www.vcbacked.co/company/trollwall-ai"},{"title":"🚀 Slovenský startup","url":"https://sk.linkedin.com/in/tomasgric"},{"title":"300+ investors in your industry, stage, and region Get","url":"https://shizune.co/investors/profile/seed-starter-slovenskej-sporite%C4%BEne"},{"title":"Total Raised","url":"https://www.cbinsights.com/company/trollwall-ai/financials"},{"title":"Recently FundedUSD 933.7KTechnology, Information and Media","url":"https://www.trysignalbase.com/news/funding/trollwall-ai-raises-93"},{"title":"top investors backing ai startups","url":"https://qubit.capital/blog/top-investors-backing-ai-startups"}]

TrollWall AI, a Slovak startup, closed a **€800,000 seed investment on April 9, 2026**. Seed Starter of Slovenská sporiteľňa, Slovak Investment Holding (SIH), and angel investor Miroslav Fedor pro
… [skrátené, 3165 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && python3 -I fetch.py https://www.sih.sk/en/aktuality/ai-against-online-hate-startup-trollwall-ai-secures-800-000-investment "Seed Starter|TrollWall|2026" | head -8
```

<details><summary>Výstup nástroja</summary>

```
(Bash completed with no output)
```

</details>

**Nástroj `Bash`**

```bash
cd /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools && curl -sL -A "Mozilla/5.0" -o /dev/null -w "%{http_code} %{size_download}\n" https://www.sih.sk/en/aktuality/ai-against-online-hate-startup-trollwall-ai-secures-800-000-investment; rm -f ../pages/$(python3 -c "import hashlib;print(hashlib.md5(b'https://www.sih.sk/en/aktuality/ai-against-online-hate-startup-trollwall-ai-secures-800-000-investment').hexdigest()[:12])").txt; python3 -I fetch.py https://www.sih.sk/en/aktuality/ai-against-online-hate-startup-trollwall-ai-secures-800-000-investment "Seed Starter|TrollWall|2026" | head -8
```

<details><summary>Výstup nástroja</summary>

```
466 2541
```

</details>

**Nástroj `Write`**

`/home/filip/investor-db/research/c060.json`
```
{
  "candidate_id": "c060",
  "name": "Seed Starter Slovenskej sporiteľne",
  "legal_name": null,
  "reg_no": null,
  "country": "SK",
  "active_in": ["SK"],
  "website": "https://www.seedstarter.sk/sk/uvod",
  "entity_kind": {
    "value": "investor",
    "source_url": "https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu-webout-ten-ziskava-spolu-165-miliona-eur-a-mieri-do-silicon-valley",
    "source_date": "2026-06-02",
    "quote": "Korporátny venture kapitálový program Seed Starter hľadá podnikateľské plány so silnou víziou a hodnotou pre zákazníkov."
  },
  "investor_type": {
    "value": "cvc",
    "source_url": "https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu
… [skrátené, 3177 znakov]
```

**Nástroj `Bash`**

```bash
python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c060.json; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c060.json
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/research/c060.json (file state is current in your context — no need to Read it back)
```

</details>

<details><summary>Výstup nástroja</summary>

```
c060 entity_kind: OK
c060 investor_type: OK
c060 sectors: OK
c060 stages: OK
c060 ticket_min: OK
c060 ticket_max: OK
c060 aum: OK
c060 inv0: OK
OK    research/c060.json
```

</details>

**Nástroj `Bash`**

```bash
ls research/; PYTHONPATH=src .venv/bin/python -m investordb.cli check-schema research/c04[4-9].json research/c05[0-9].json research/c060.json; python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c04[4-9].json research/c05[0-9].json research/c060.json | grep -c OK; python3 -I /tmp/claude-1000/-home-filip/72997355-d334-4927-aa33-7619dbc7c611/scratchpad/tools/verify.py research/c04[4-9].json research/c05[0-9].json research/c060.json | grep -v ": OK" || echo "all quotes found"
```

<details><summary>Výstup nástroja</summary>

```
c001.json
c002.json
c003.json
c004.json
c005.json
c006.json
c007.json
c008.json
c009.json
c010.json
c011.json
c012.json
c013.json
c014.json
c015.json
c016.json
c017.json
c018.json
c019.json
c020.json
c021.json
c022.json
c023.json
c024.json
c025.json
c026.json
c027.json
c028.json
c029.json
c030.json
c031.json
c032.json
c033.json
c034.json
c035.json
c036.json
c037.json
c038.json
c039.json
c040.json
c041.json
c042.json
c043.json
c044.json
c045.json
c046.json
c047.json
c048.json
c049.json
c050.json
c051.json
c052.json
c053.json
c054.json
c055.json
c056.json
c057.json
c058.json
c059.json
c060.json
c061.json
c062.json
c063.json
c064.json
c065.json
c066.json
c067.json
c068.json
c069.json
c070.json
c071.json
c072.json
c073.json
c074.json
c075.json
OK    research/c044.json
OK    research/c045.json
OK    research/c046.json
OK    research/c047.json
OK    research/c048.json
OK    research/c049.json
OK    research/c050.json
OK    research/c051.json
OK    research/c052.json
OK    research/c053.json
OK    research/c054.json
OK    research/c055.json
OK    research/c056.json
OK    research/c057.json
OK    research/c058.json
OK    research/c059.json
OK    research/c060.json
96
all quotes found
```

</details>

**Nástroj `Bash`**

```bash
python3 -c "
import json
for c in ['c004','c008','c009','c062','c064']:
    d=json.load(open(f'research/{c}.json')); print(c, d['name'], '| dup:', d.get('duplicate_of'), '|', d.get('notes','')[:250])
"
```

<details><summary>Výstup nástroja</summary>

```
c004 Eterus Capital | dup: None | Slovak growth/minority PE fund (contacts on wood.com addresses, i.e. linked to WOOD & Company). Ticket from its own site (EUR 2-2.5m preferred); SLOVCA profile gives a wider 500k-5m range. Only 'invested over EUR 40m' is stated, which is not AUM, so 
c008 Národný holdingový fond | dup: None | State-owned subsidiary of Slovak Business Agency (founded 1994 as Seed Capital Company, later Fond fondov). Its site says it manages two VC funds, Eterus Capital a.s. (c004) and Fond inovácií a technológií, a.s. (c005), plus a microloan fund; not mar
c009 Neulogy Ventures | dup: None | Bratislava-based deeptech VC with Luxembourg (CSSF) regulated funds; invests also outside SK (e.g. StratifAI in Germany). Individual fund names not found. Aggregators mention a 2025 GA Drilling Series D led by Neulogy, but no primary source was found
c062 CB ESPRI | dup: None | Only fund CB ESPRI Impact One (co-financed by SIH from ESF) had its investment period in 2022-2023 and is in post-investment period 2024-2032 per cbespri.sk; Lupa.cz (Jan 2024) says it no longer accepts applications. Instruments are convertible and s
c064 J&T Ventures | dup: None | Prague-based early-stage VC of the J&T group (office in J&T Banka building). Definic (Košice, SK) is a Slovak deal. Website states €120M assets and region CEE & SEE & Baltics, but those are short standalone labels, so AUM was not recorded. Not the sa
```

</details>

## Claude · 2026-10-09 12:40:24 UTC

Všetkých 17 súborov `research/c044.json` až `research/c060.json` je zapísaných. Každý prešiel `check-schema` (OK). Citáty som overil vlastným skriptom: každý stiahne `source_url`, vytiahne z neho text a citát hľadá doslovne. Nájdených bolo všetkých 96, oficiálny skript na overovanie citátov však v repozitári ešte nie je.

`id | entity_kind | type | #investments | missing fields`
```
c044 | investor | pe          | 0 | sectors, aum, investments, legal_name, reg_no
c045 | investor | pe          | 1 | ticket_min, ticket_max, reg_no
c046 | investor | vc          | 1 | legal_name, reg_no
c047 | investor | vc          | 1 | sectors, ticket_min, ticket_max, aum, reg_no
c048 | investor | pe          | 1 | sectors, stages, ticket_min, ticket_max, website, reg_no
c049 | investor | vc          | 3 | ticket_min, ticket_max, legal_name, reg_no
c050 | investor | vc          | 1 | legal_name, reg_no
c051 | investor | public_fund | 0 | sectors, ticket_min, aum, investments, website, reg_no
c052 | investor | vc          | 1 | stages, ticket_min, ticket_max, aum, website
c053 | investor | vc          | 1 | sectors, stages, aum, website
c054 | investor | vc          | 1 | ticket_min, website
c055 | investor | pe          | 0 | sectors, ticket_min, ticket_max, aum, investments, website
c056 | investor | public_fund | 0 | sectors, aum, investments (duplicate_of c004)
c057 | investor | vc          | 0 | sectors, investments, website
c058 | investor | vc          | 0 | sectors, stages, ticket_min, ticket_max, investments (duplicate_of c059)
c059 | investor | vc          | 1 | legal_name, reg_no
c060 | investor | cvc         | 1 | legal_name, reg_no
```

**Duplicity a zmeny názvov:**
- **c058 je duplikát c059.** Zero Gravity Capital bol prvý fond (23 mil. EUR) dnešného Zero One Hundred, čo výslovne uvádza CzechCrunch (2022). Investície som zapísal pod c059.
- **c056 je duplikát c004 (Eterus Capital), ale je to len môj záver.** Výslovnú zmienku o premenovaní som nenašiel. Dôvody:
  - nhfond.sk dnes opisuje Eterus rovnakými slovami, akými podnikajte.sk v roku 2016 opisoval SRKF;
  - oba fondy majú v portfóliu Sygic;
  - veľkosť investícií sa zhoduje.
- **c051 (Slovenský rozvojový fond)** bol samostatný fond pod Národným holdingovým fondom (c008). Ako duplikát som ho neoznačil. Dnes už na nhfond.sk nie je a je takmer určite neaktívny.
- **c047 Crowdberry** je sama osebe crowdinvestingová platforma. Podľa inštrukcií som preto spracoval jej vlastný startupový fond CB IM Growth One. Fond CB ESPRI je samostatný kandidát c062.
- **c048 J&T ARCH** nie je to isté ako J&T Ventures (c064). Je to holdingový fond skupiny J&T, ktorý investuje do veľkých podielov, napríklad Allwyn a EPH, nie do startupov.

**Pravdepodobne neaktívne:**
- **c044 Benson Oak:** posledná aktivita je odchod z Kliku v roku 2020.
- **c052 Monogram Ventures:** doména je dnes iný web, posledný obchod je z roku 2011.
- **c053 LRJ Capital:** doména je na predaj, posledný obchod je z roku 2019.
- **c054 Pioneers Ventures:** portfólio v roku 2018 prevzal Speedinvest.
- **c055 Arca Capital Slovakia:** súd v júli 2025 začal konkurzné konanie.
- **c057 Limerock:** podľa SIH je fond v likvidácii.
- **c051:** pozri vyššie.

**V čom si nie som istý:**
- **Zdroje bez dátumu:** c058 (Forbes 2019) a c059 (profil na EU-Startups) nemajú pri citátoch `source_date`.
- **Krátke citáty:** v c059 a c060 sú niektoré citáty len krátke štítky z webu (napr. „Typical Investment: €100k-€1.5M“, „Pre-seed a seed“, „200 000 € – 1 000 000 €“). Ak oficiálny skript spracuje text stránky inak ako môj, nemusí ich nájsť. Pri c047 (web na Wix) a c046 (Framer) stránky dopĺňa JavaScript, citáty som však našiel v ich statickom HTML.
- **c044:** HTTPS certifikát bensonoak.cz je neplatný, preto je `source_url` cez `http://`.
- **AUM často zodpovedá len jednému fondu:** c046 (Stage 5, 88 mil. USD), c049 (Fund I, 15 mil. EUR), c050 (cieľová veľkosť Fund IV, 150 mil. EUR), c059 (Fund I, 23 mil. EUR), c060 (počiatočných 5 mil. EUR). Pri c048 ide o celkové aktíva fondu (202,9 mld. CZK). Vždy je to vysvetlené v `notes`.
- **Vynechané obchody:** UNIPAP (c045), Supernova (c046), TrollWall AI (c060) a Žltý melón (c057) som nezapísal. Buď žiadna jedna veta nespomína investora aj firmu naraz, alebo zdroj blokuje automatické sťahovanie.
- **`active_in`:** pri c046 a c050 je `SK` odvodené z mandátu pre strednú a východnú Európu, konkrétny slovenský obchod v sledovanom období som nenašiel.
