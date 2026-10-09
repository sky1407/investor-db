# 02 Plán a koncepty

Zdroj: transkript Claude Code `cd73308a-76ca-42a3-b248-5dfd47186b91.jsonl`

## Používateľ · 2026-10-09 11:23:15 UTC

<pasted_content id="f230">
Pracovať môžete v Claude Code alebo v podobnom nástroji. Ak nestihnete všetko, uprednostnite podstatné časti a uveďte, čo v riešení chýba. V README prosím popíšte, ako ste s AI pracovali (aké pokyny dostali agenti, ako ste kontrolovali ich výstup a kde sa pomýlili). Ak Vám v zadaní niečo nebude jasné, rozhodnite podľa seba a v README zdôvodnite, prečo ste sa tak rozhodli. S otázkami sa na mňa môžete kedykoľvek obrátiť aj odpoveďou na tento e-mail.


ZADANIE A: Spoľahlivá databáza investorov

Úloha sa týka databázy investorov do firiem: VC fondov, private equity, family office, angel investorov a veľkých súkromných investorov. Kľúčová je spoľahlivosť dát: každý záznam musí byť skutočný investor, nie náhodná firma. Pri každom investorovi musí byť uvedené, v akom sektore pôsobí, do čoho bežne investuje a v akej výške, aký má celkový investičný kapitál a odkiaľ tieto informácie pochádzajú.

Začnite plánom. Z neho musí byť jasné, kto v databáze bude a kto nie, teda podľa akých pravidiel subjekt zaradíte alebo vyradíte. Popíšte tiež, ako overíte pravosť a správne zaradenie záznamov. Odhadnite, aký okruh investorov je možné z verejných zdrojov získať, približne koľko ich bude a aká bude spoľahlivosť dát. Uveďte, z čoho odhad vychádza.

Plán následne overte na menšej vzorke, napríklad na VC fondoch v jednej krajine. Pri každom zázname uveďte zdroj a dátum, ktoré dokladajú, že subjekt skutočne investuje. Na ručne overenej vzorke zmerajte presnosť. Na záver odhadnite náklady na rozšírenie na celý svet.

Používajte výhradne verejne dostupné dáta.
</pasted_content id="f230">

## Claude · 2026-10-09 11:23:54 UTC

# Zadanie A: návrh postupu pred začiatkom práce

Podľa tvojich pravidiel najprv navrhujem postup a koncepty. Kód začnem písať, až keď vyberieš smer.

## 1. Kto v databáze bude a kto nie (návrh pravidiel)

**Zaradíme** subjekt, ktorý **pravidelne vkladá vlastný alebo spravovaný kapitál do súkromných firiem výmenou za podiel** a aspoň jedna jeho investícia je verejne doložená za posledných 36 mesiacov:
- VC fondy, PE fondy, family office, korporátne VC, ktoré majú samostatnú investičnú jednotku,
- angel investorov s aspoň 2 verejne doloženými investíciami,
- veľkých súkromných investorov, teda investičné holdingy.

**Vyradíme:**
- banky a nebankové subjekty, ktoré iba požičiavajú,
- crowdfundingové platformy, ktoré len sprostredkúvajú, nie sú investormi,
- M&A poradcov a konzultantov,
- akcelerátory bez podielu vo firmách,
- hedge fondy, ktoré investujú iba do verejných trhov,
- neaktívne fondy, ktoré nemajú žiadny deal za viac ako 36 mesiacov,
- štátne grantové schémy,
- firmy, ktoré urobili jednu akvizíciu, ale nemajú investičnú stratégiu.

**Hraničné prípady** (štátne fondy fondov, napríklad SIH alebo NRB, a hybridné akcelerátory) dostanú príznak `status: borderline` a zdôvodnenie v README.

## 2. Ako overím pravosť záznamov

Každý záznam musí prejsť **dvomi nezávislými zdrojmi**:
1. **Zdroj identity:** regulačný register (NBS, ČNB, SEC Form ADV), člen asociácie (SLOVCA, CVCA, Invest Europe), portfólio EIF alebo obchodný register.
2. **Dôkaz aktivity:** URL a dátum konkrétneho dealu (tlačová správa, portfólio na webe fondu, správa v médiách).

Každý údaj (sektor, typický ticket, AUM) bude mať vlastný `source_url`, `source_date` a `confidence`. Presnosť zmeriam na ručne overenej vzorke: vypočítam precision pre otázku „je to skutočný investor“ a presnosť jednotlivých polí. Všetky miesta, kde sa AI pomýlila, zapíšem do README.

## 3. Koncepty postupu

| | Koncept | Plusy | Mínusy |
|---|---|---|---|
| **A** | **Najprv registre:** kandidátov beriem z registrov a asociácií, potom ich doplním z webov fondov (LLM extrakcia) | Vysoká presnosť, postup sa dá zopakovať a dá sa z neho odhadnúť cena za záznam | Neodhalí angel investorov ani tichých investorov, ktorí nie sú v žiadnom zozname |
| **B** | **Najprv dealy:** zbieram ohlásené investičné kolá z médií a investorov odvodzujem od nich | Dôkaz o investovaní je v dátach od začiatku, zachytí aj angel investorov | Veľa šumu (rovnaký investor pod rôznymi menami, nepresné články), PE a FO zverejňujú dealy málo |
| **C** | **Hybrid (odporúčam):** kandidátov beriem z A, overujem ich cez B a nové mená z B pridávam ako kandidátov | Najlepšie pokrytie a overenie, presne zodpovedá požiadavke na zdroj a dátum | Najviac práce, mapovanie rovnakých subjektov (entity resolution) je náročnejšie |

**Výstup vo všetkých troch prípadoch:**
- dokument s plánom a odhadmi (počty, spoľahlivosť, náklady na rozšírenie na celý svet),
- skripty,
- `investors.csv` / `.json` so zdrojmi,
- súbor s ručnou validáciou a meraním presnosti,
- README s popisom práce s AI.

**Hrubý odhad dostupnosti z verejných zdrojov:**
- VC: približne 10 až 15 tisíc aktívnych fondov,
- PE: približne 8 až 12 tisíc,
- single family office: približne 8 až 10 tisíc, verejne identifikovateľných je však iba zlomok,
- angel investori: verejne doložiteľných sú desaťtisíce.

Tieto čísla pred použitím v pláne overím a ku každému uvediem zdroj.

Najprv potrebujem od teba štyri rozhodnutia:

**Nástroj `AskUserQuestion`**

```json
{"questions": [{"question": "Ktorý koncept postupu zvolíme?", "header": "Koncept", "multiSelect": false, "options": [{"label": "C – Hybrid (Recommended)", "description": "Kandidáti z registrov a asociácií, overenie cez doložené dealy, nové mená z dealov pridávam ako kandidátov."}, {"label": "A – Najprv registre", "description": "Rýchlejšie a presnejšie, ale slabšie pokrytie (bez angel investorov)."}, {"label": "B – Najprv dealy", "description": "Silný dôkaz aktivity, ale viac šumu."}]}, {"question": "Na ktorej krajine overíme vzorku VC fondov?", "header": "Vzorka", "multiSelect": false, "options": [{"label": "Slovensko (Recommended)", "description": "Približne 25 až 40 VC fondov (SLOVCA, SIH/NDI, NBS register). Všetky sa dajú ručne overiť a zmerať presnosť na 100 % vzorky."}, {"label": "Česko", "description": "Približne 60 až 100 fondov (CVCA, ČNB). Reprezentatívnejšie, ale ručne overím iba náhodnú podvzorku."}, {"label": "Slovensko + Česko", "description": "Väčšia vzorka a test, či postup funguje vo viacerých krajinách. Zaberie zhruba dvakrát viac času."}]}, {"question": "V akom jazyku napíšem skripty pipeline?", "header": "Stack", "multiSelect": false, "options": [{"label": "Pyth
… [skrátené, 1877 znakov]
```

<details><summary>Výstup nástroja</summary>

```
Your questions have been answered: "Ktorý koncept postupu zvolíme?"="C – Hybrid (Recommended)", "Na ktorej krajine overíme vzorku VC fondov?"="Slovensko (Recommended)", "V akom jazyku napíšem skripty pipeline?"="Python (Recommended)", "Kam uložím projekt?"="~/investor-db + GitHub". You can now continue with these answers in mind.
```

</details>

**Nástroj `ToolSearch`**

```json
{"query": "select:WebSearch,WebFetch", "max_results": 2}
```

**Nástroj `WebSearch`**

```json
{"query": "SLOVCA členovia zoznam venture capital fondy Slovensko", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Slovak Investment Holding venture capital fondy portfólio správcovia", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "number of active venture capital firms worldwide 2025 estimate", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "number of active venture capital firms worldwide 2025 estimate"

Links: [{"title":"Accepted Answer","url":"https://decilehub.com/base/1-general_questions/9758-how-many-vc-firms-are-in-the-united-states-how-to-approach-counting-the-number-of-vc-firms-how-much-capital-was-deployed-in-2024"},{"title":"100 Top Venture Capital Firms (2025)","url":"https://eqvista.com/?p=4632"},{"title":"many firms united states approach counting number firms much capital deployed 2024","url":"https://decilegroup.com/posts/many-firms-united-states-approach-counting-number-firms-much-capital-deployed-2024"},{"title":"Venture Capital Private Equity Firms Guide 2025 Comprehensive Database of 3000 of the Most Active VC and Private Equity Firms Operating Domestically and Internationally   ResearchAndMarkets","url":"https://www.businesswire.com/news/home/20250723336119/en/Venture-Capital-Private-Equity-Firms-Guide-2025-Comprehensive-Database-of-3000-of-the-Most-Active-VC-and-Private-Equity-Firms-Operating-Domestically-and-Internationally---ResearchAndMarkets.com"},{"title":"www.businesswire.com","url":"https://www.businesswire.com/news/home/20250723336119/en"},{"title":"data 2025 vs 2021 funding hottest companies ai","url":"https://news.crunchbase.com/venture/data-2025-vs-2021-funding-hottest-companies-ai/"},{"title":"news.crunchbase.com","url":"https://news.crunchbase.com/?p=93153"},{"title":"PipelineRoad Research","url":"https://pipelineroad.com/research/venture-capital-g
… [skrátené, 3648 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "SLOVCA členovia zoznam venture capital fondy Slovensko"

Links: [{"title":"Popularita private equity a venture kapitálu na Slovensku","url":"https://www.podnikajte.sk/investor/private-equity-venture-kapital-na-slovensku"},{"title":"www.podnikajte.sk","url":"https://www.podnikajte.sk/financie?page=36"},{"title":"startup a investor","url":"https://www.podnikajte.sk/temy/startup-a-investor?page=6"},{"title":"Tlačová správa","url":"https://www.podnikajte.sk/autori/tlacova-sprava?page=58"},{"title":"www.cbinsights.com","url":"https://www.cbinsights.com/company/slovca/financials"},{"title":"Compare HVCA vs SLOVCA","url":"https://www.cbinsights.com/compare/hvca-vs-slovca"},{"title":"Compare EstVCA vs SLOVCA","url":"https://www.cbinsights.com/compare/estvca-vs-slovca"},{"title":"Compare Genesis Capital vs SLOVCA","url":"https://www.cbinsights.com/compare/genesis-capital-sro-vs-slovca"},{"title":"Radoslav Tausinger","url":"https://cz.linkedin.com/in/tausinger"}]

Priamy zoznam členov SLOVCA sa vo výsledkoch vyhľadávania nenašiel. Našiel som však niekoľko informácií o združení a o fondoch, ktoré s ním súvisia.

**Čo je SLOVCA:** Podľa jedného profilu ide o združenie zamerané na venture capital a private equity, ktoré zastupuje záujmy svojich členov a spolupracuje s vládou na zlepšení investičného prostredia (SLOVCA is an association that focuses on venture capital and private equity within the financial services industry. The organization represents the i
… [skrátené, 3473 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Slovak Investment Holding venture capital fondy portfólio správcovia"

Links: [{"title":"Investičný fond pre sociálnu ekonomiku: Sociálni Inovátori do projektov investujú 10 miliónov eur","url":"https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku"},{"title":"www.eib.org","url":"https://www.eib.org/en/projects/all/20190166?lang=en"},{"title":"Recherche FR menu Portail client du Groupe BEI","url":"https://www.eib.org/fr/projects/all/20190166"},{"title":"investicie zo slovak investment holding vyhrali celoeuropsku sutaz","url":"https://www.sih.sk/en/aktuality/investicie-zo-slovak-investment-holding-vyhrali-celoeuropsku-sutaz"},{"title":"Slovenské startupy už nemusia odchádzať do zahraničia. Vznikol jedinečný fond na ich podporu","url":"https://www.startitup.sk/slovenske-startupy-uz-nemusia-odchadzat-do-zahranicia-vznikol-jedinecny-fond-na-ich-podporu/"},{"title":"Luxembourg, 14.11.2019","url":"https://www.eib.org/attachments/registers/125282376.pdf"},{"title":"Slovenské startupy už nemusia odchádzať do zahraničia. Vznikol jedinečný fond na ich podporu","url":"https://www.startitup.sk/?p=358673"},{"title":"www.crz.gov.sk","url":"https://www.crz.gov.sk//data/att/4853310.pdf"},{"title":"Release date: 16 October 2019","url":"https://www.eib.org/en/projects/pipelines/all/20190166"},{"title":"vs sih 2019 en final 351","url":"https://www.sih.sk/data/files/vs_sih_2019_en_final-351.pdf"}]

Slovak Investment Holding (SIH) 
… [skrátené, 3527 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.slovca.sk/", "prompt": "List all member organizations (full and associate members) with URLs if present. Also note any link to a members page."}
```

**Nástroj `WebSearch`**

```json
{"query": "number of single family offices worldwide 2024 2025 Deloitte estimate", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "number of private equity firms worldwide estimate active", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Slovensko startupy investície 2025 report venture capital fondy zoznam investorov Dealroom", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
The page doesn't name any full or associate member organizations, so I can't list them or give their individual URLs.

It does link to separate pages for each membership category:

- **Full members (Riadni členovia):** https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html
- **Associate members (Pridružení členovia):** https://www.slovca.sk/sk/clenstvo/pridruzeni-clenovia.html
- **Members page:** https://www.slovca.sk/sk/stranky/clenstvo

The domain comes from the page's own links; I added `https://www.slovca.sk` to the relative paths. The page also links to Partnerskí členovia (partner members) and Partneri (partners), which you didn't ask about.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "number of single family offices worldwide 2024 2025 Deloitte estimate"

Links: [{"title":"deloitte number of family offices to grow 75 by 2030","url":"https://www.dakota.com/fundraising-news/deloitte-number-of-family-offices-to-grow-75-by-2030"},{"title":"Weiter zum Inhalt","url":"https://www.ig.com/ch/prime/einblicke/artikel/no-end-in-sight-for-the-family-office-boom-250718"},{"title":"global edition explores the rapid expansion family offices and ffers vision of the future landscape","url":"https://www.deloitte.com/global/en/about/press-room/global-edition-explores-the-rapid-expansion-family-offices-and-ffers-vision-of-the-future-landscape.html"},{"title":"global edition explores the rapid expansion family offices and ffers vision of the future landscape","url":"https://www.deloitte.com/in/en/about/press-room/global-edition-explores-the-rapid-expansion-family-offices-and-ffers-vision-of-the-future-landscape.html"},{"title":"global family office wealth to hit 9 5tr by 2030 report","url":"https://arabianbusiness.com/culture-society/global-family-office-wealth-to-hit-9-5tr-by-2030-report"},{"title":"no end in sight for the family office boom 250718","url":"https://www.ig.com/za/prime/insights/articles/no-end-in-sight-for-the-family-office-boom-250718"},{"title":"no end in sight for the family office boom 250718","url":"https://www.ig.com/uk/prime/insights/articles/no-end-in-sight-for-the-family-office-boom-250718"},{"title":"no end in sight for t
… [skrátené, 3553 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "number of private equity firms worldwide estimate active"

Links: [{"title":"Print this article","url":"https://www.wealthbriefing.com/html/printarticle.php?id=26481"},{"title":"Tue, Jul 21, 2026","url":"https://www.opalesque.com/672699/250000_people_worldwide_working_in_the_private_equity269.html"},{"title":"Key insights","url":"https://www.statista.com/topics/12166/private-equity-in-the-us"},{"title":"the industry today","url":"https://legacy.vault.com/industries-professions/industries/private-equity/the-industry-today"},{"title":"Print this article","url":"https://www.wealthbriefing.com/html/printarticle.php?id=26850"},{"title":"Private equity worldwide","url":"https://statista.com/study/14775/private-equity-statista-dossier"},{"title":"The Global Accounting Profession, Now Featuring 1,000+ PE-Backed Firms","url":"https://www.goingconcern.com/the-global-accounting-profession-now-featuring-1000-pe-backed-firms/"},{"title":"Key insights","url":"https://www.statista.com/topics/1454/online-gaming"},{"title":"Key insights","url":"https://www.statista.com/topics/1454/vinyl-records"},{"title":"Private equity worldwide","url":"https://www-statista-com.ezproxy.canberra.edu.au/study/14775/private-equity-statista-dossier"}]

Estimates range from about 4,000 to 7,000 firms, depending on the source, the year, and how "private equity firm" is defined.

The most recent figure I found is roughly 7,000. According to the American Investment Council, there are 
… [skrátené, 2930 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Slovensko startupy investície 2025 report venture capital fondy zoznam investorov Dealroom"

Links: [{"title":"Slovenské startupy silnejú v IT. Rast brzdí nedostatok investícií","url":"https://pravnenoviny.sk/?p=17472"},{"title":"Slovenské startupy silnejú v IT. Rast brzdí nedostatok investícií","url":"https://pravnenoviny.sk/slovenske-startupy-silneju-v-it-rast-brzdi-nedostatok-investicii/"},{"title":"Slovensko sa ocitlo na chvoste Európy, v rozvoji startupov zaostávame za najlepšími","url":"https://sita.sk/slovensko-sa-ocitlo-na-chvoste-europy-v-rozvoji-startupov-zaostavame-za-najlepsimi/"},{"title":"Štvrtina Slovenských startupov chce z našej krajiny odísť. Dve tretiny zarobili pod 100-tisíc eur (STARTUP REPORT 2025)","url":"https://www.startitup.sk/?p=1120488"},{"title":"slowakei.ahk.de","url":"https://slowakei.ahk.de/sk/content/download/397336/6252205?version=1"},{"title":"Slovenská spořitelna bude investovat do startupů po vzoru České. Připravených má přes 120 milionů","url":"https://cc.cz/ceska-sporitelna-jde-podporovat-startupy-i-na-slovensko-pro-tamni-mlade-firmy-ma-pres-120-milionu/"},{"title":"top of page","url":"https://www.symsite.sk/single-post/low-venture-capital-investments-in-slovakia"},{"title":"top of page","url":"https://www.symsite.sk/single-post/lovakia-attracted-only-7m-in-venture-capital-in-2025"},{"title":"top of page","url":"https://www.symsite.sk/single-post/quarter-of-startups-considering-leaving-slovakia"}]

I found 
… [skrátené, 3835 znakov]
```

</details>

**Nástroj `Bash`**

```bash
ls ~/investor-db 2>&1; python3 --version; which uv pip3; gh auth status 2>&1 | head -3
```

<details><summary>Výstup nástroja</summary>

```
ls: cannot access '/home/filip/investor-db': No such file or directory
Python 3.14.4
uv not found
/home/filip/.local/bin/pip3
github.com
  ✓ Logged in to github.com account sky1407 (/home/filip/.config/gh/hosts.yml)
  - Active account: true
```

</details>

**Nástroj `Bash`**

```bash
mkdir -p ~/investor-db/raw && cd ~/investor-db && git init -q && for p in riadni-clenovia pridruzeni-clenovia; do curl -sL "https://www.slovca.sk/sk/clenstvo/$p.html" -o raw/slovca-$p.html; done; ls -la raw; python3 -c "import httpx, pydantic, bs4; print('ok')"
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
total 64
drwxr-xr-x 2 filip filip  4096 Oct  9 13:25 .
drwxr-xr-x 4 filip filip  4096 Oct  9 13:25 ..
-rw-r--r-- 1 filip filip 30585 Oct  9 13:25 slovca-pridruzeni-clenovia.html
-rw-r--r-- 1 filip filip 21817 Oct  9 13:25 slovca-riadni-clenovia.html
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import httpx, pydantic, bs4; print('ok')
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'httpx'
```

</details>

## Claude · 2026-10-09 11:25:46 UTC

Projekt `~/investor-db` je založený a stiahol som zoznamy členov SLOVCA. Teraz ich spracujem do zoznamu slovenských kandidátov.

**Nástroj `Bash`**

```bash
cd ~/investor-db && python3 -m venv .venv && .venv/bin/pip install -q httpx pydantic beautifulsoup4 && .venv/bin/python -I -c "
from bs4 import BeautifulSoup
for f in ['raw/slovca-riadni-clenovia.html','raw/slovca-pridruzeni-clenovia.html']:
    s=BeautifulSoup(open(f,encoding='utf-8'),'html.parser')
    m=s.find('main') or s.body
    print('==',f); print(' '.join(m.get_text(' ',strip=True).split())[:4000])
    print([a['href'] for a in m.find_all('a',href=True) if 'slovca' not in a['href']][:80])
"
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.14-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /home/filip/investor-db/.venv/bin/python3
```

</details>

**Nástroj `Bash`**

```bash
cd ~/investor-db && rm -rf .venv && pip3 install --user -q --break-system-packages httpx pydantic beautifulsoup4 2>&1 | tail -2; python3 -I -c "
from bs4 import BeautifulSoup
for f in ['raw/slovca-riadni-clenovia.html','raw/slovca-pridruzeni-clenovia.html']:
    s=BeautifulSoup(open(f,encoding='utf-8'),'html.parser')
    m=s.find('main') or s.body
    print('==',f); print(' '.join(m.get_text(' ',strip=True).split())[:4000])
    print([a['href'] for a in m.find_all('a',href=True) if 'slovca' not in a['href']][:80])
"
```

<details><summary>Výstup nástroja</summary>

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 2, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
```

</details>

**Nástroj `Bash`**

```bash
cd ~/investor-db && python3 -P -c "
from bs4 import BeautifulSoup
for f in ['raw/slovca-riadni-clenovia.html','raw/slovca-pridruzeni-clenovia.html']:
    s=BeautifulSoup(open(f,encoding='utf-8'),'html.parser')
    m=s.find('main') or s.body
    print('==',f); print(' '.join(m.get_text(' ',strip=True).split())[:4000])
    print([a['href'] for a in m.find_all('a',href=True) if 'slovca' not in a['href']][:80])
"
```

<details><summary>Výstup nástroja</summary>

```
== raw/slovca-riadni-clenovia.html
Riadni členovia ARX Equity Partners CVI Enterprise Investors Eterus Capital Fond inovácií a technológií Genesis Capital Jet Investment Národný holdingový fond s.r.o. Neulogy Ventures Sandberg Capital Venture to Future Fund Vision Ventures Členstvo Riadni členovia Pridružení členovia Partnerskí členovia Partneri Etický kódex Prihláška Čerstvé správy! Prihláste sa na odber noviniek SLOVCA a získajte informácie o private equity trhu v EU a na Slovensku ako aj najnovšie štatistiky o investovanom rozvojovom kapitáli. Registrovať
['/sk/riadni-clenovia/arx-equity-partners.html', '/sk/riadni-clenovia/arx-equity-partners.html', '/sk/riadni-clenovia/cvi.html', '/sk/riadni-clenovia/cvi.html', '/sk/riadni-clenovia/enterprise-investors.html', '/sk/riadni-clenovia/enterprise-investors.html', '/sk/riadni-clenovia/eterus-capital.html', '/sk/riadni-clenovia/eterus-capital.html', '/sk/riadni-clenovia/fond-inovacii-a-technologii.html', '/sk/riadni-clenovia/fond-inovacii-a-technologii.html', '/sk/riadni-clenovia/genesis-capital.html', '/sk/riadni-clenovia/genesis-capital.html', '/sk/riadni-clenovia/jet-investment.html', '/sk/riadni-clenovia/jet-investment.html', '/sk/riadni-clenovia/narodny-holdingovy-fond-s-r-o.html', '/sk/riadni-clenovia/narodny-holdingovy-fond-s-r-o.html', '/sk/riadni-clenovia/neulogy-ventures.html', '/sk/riadni-clenovia/neulogy-ventures.html', '/sk/riadni-clenovia/sandberg-capital.html', '/sk/riadni-clenovia/sandberg-capital.html', '/sk/ria
… [skrátené, 5630 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "zoznam slovenských venture capital fondov 2025 Zero Gravity Capital Limerock Crowdberry Neulogy Lighthouse Ventures", "mode": "extended"}
```

**Nástroj `WebSearch`**

```json
{"query": "Fond inovácií a technológií FIT investoval do fondov rizikového kapitálu zoznam správcov", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "Národný holdingový fond investície do VC fondov Slovensko 2024 2025 správca", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Fond inovácií a technológií FIT investoval do fondov rizikového kapitálu zoznam správcov"

Links: [{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"FIT vám pomôže zafinancovať inovatívne podnikateľské nápady","url":"https://www.podnikajte.sk/investor/fit-fond-financovanie"},{"title":"private equity a venture kapital","url":"https://www.podnikajte.sk/temy/private-equity-a-venture-kapital?page=7"},{"title":"Osobitná správa","url":"https://op.europa.eu/webpub/eca/special-reports/venture-capital-17-2019/sk/"},{"title":"eif icf and grow venture partners sign agreement to set up fondo de inversion en tecnologia avanzada fita","url":"https://eif.org/what_we_do/equity/news/2024/eif-icf-and-grow-venture-partners-sign-agreement-to-set-up-fondo-de-inversion-en-tecnologia-avanzada-fita.htm"},{"title":"Osobitná správa","url":"https://op.europa.eu/webpub/eca/special-reports/venture-capital-17-2019/sk/index.html"},{"title":"Podnikateľ a investor","url":"https://www.podnikajte.sk/investor?page=5"},{"title":"Predict your next investment","url":"https://www.cbinsights.com/investor/fond-fit"},{"title":"Private Equity","url":"https://altss.com/profile/fond-fit"}]

I couldn't find a list of venture capital fund managers that FIT has invested in. The results describe FIT as a direct investor in companies, not as a limited partner in other funds.

- **What FIT does
… [skrátené, 2800 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Národný holdingový fond investície do VC fondov Slovensko 2024 2025 správca"

Links: [{"title":"První investiční VC fond z Národního plánu obnovy ČR bude spravovat Tensor Ventures","url":"https://www.businessinfo.cz/clanky/prvni-investicni-vc-fond-z-narodniho-planu-obnovy-cr-bude-spravovat-tensor-ventures/"},{"title":"NEWCaplight raises a $16M Series A, led by BlackRock and Fin Capital →","url":"https://www.caplight.com/investor/nhfond"},{"title":"n rodn holdingov fond nhfond sk","url":"https://venturecapitalarchive.com/venture-funds/n-rodn-holdingov-fond-nhfond-sk"},{"title":"NRI dokončila výběr venture kapitálového fondu pro program Fond Ukrajina","url":"https://www.businessinfo.cz/clanky/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/"},{"title":"nh fund","url":"https://altss.com/profile/nh-fund.md"},{"title":"Vietnam sets up national VC fund; looks to raise $78m in first five years","url":"https://www.dealstreetasia.com/?p=460176"},{"title":"Vietnam sets up national VC fund with $20m in initial state capital","url":"https://media.dealstreetasia.com/stories/vietnam-national-vc-fund-460176"},{"title":"National Capital Fund (KFK)","url":"https://pfrventures.pl/en/program-dla-vc/national-capital-fund-kfk"},{"title":"Publications Office of the EU","url":"https://op.europa.eu/en/web/public-procurement/procurement-details/-/procurement/1e8eb477-a5c6-4cbd-b736-e5fae75c130e"}]

I found only a few relevant results, and they a
… [skrátené, 3663 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "zoznam slovenských venture capital fondov 2025 Zero Gravity Capital Limerock Crowdberry Neulogy Lighthouse Ventures"

Links: [{"title":"Financovanie start-upov v roku 2025 - Legalion: Advokátska kancelária","url":"https://www.legalion.sk/2025/04/09/financovanie-start-upov-v-roku-2025/"},{"title":"Zoznam equity fondov","url":"https://www.legalfirm.sk/sk/stranky/clanok/zoznam-equity-fondov"},{"title":"Slovenské startupy dostanú významnú pomoc. Investičné fondy sa spájajú a pomôžu bezplatným mentoringom","url":"https://www.startitup.sk/slovenske-startupy-dostanu-vyznamnu-pomoc-investicne-fondy-sa-spajaju-a-pomozu-bezplatnym-mentoringom/"},{"title":"Private equity a venture kapitálové fondy pôsobiace v SR","url":"https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr"},{"title":"Venture to Future Fund","url":"https://vff.sk/"},{"title":"Zoznam equity fondov na Slovensku - BALTEUS","url":"https://balteus.sk/en/blog/a-list-of-equity-funds-in-slovakia/"},{"title":"Nhfond","url":"http://www.nhfond.sk/o-nas/slovca/"},{"title":"Fond inovácií a technológií / Slovak Venture Capital & Private Equity Association SLOVCA","url":"https://www.slovca.sk/sk/riadni-clenovia/fond-inovacii-a-technologii.html"},{"title":"Index Ventures","url":"https://en.wikipedia.org/wiki/Index_Ventures"}]

Links: [{"title":"Investičný fond Zero Gravity Capital hľadá mladé firmy. Rozdeliť má 12 miliónov eur - Forbes Slovensko","url":"https://www.forbes.sk/investicny-fond-z
… [skrátené, 5244 znakov]
```

</details>

**Nástroj `Bash`**

```bash
cd ~/investor-db && curl -sL -A "Mozilla/5.0" https://balteus.sk/en/blog/a-list-of-equity-funds-in-slovakia/ -o raw/balteus.html; curl -sL -A "Mozilla/5.0" https://www.legalfirm.sk/sk/stranky/clanok/zoznam-equity-fondov -o raw/legalfirm.html; curl -sL -A "Mozilla/5.0" https://www.podnikajte.sk/investor/private-equity-venture-fondy-sr -o raw/podnikajte.html; ls -la raw; python3 -P -c "
from bs4 import BeautifulSoup
import sys
for f in ['raw/balteus.html','raw/legalfirm.html','raw/podnikajte.html']:
    s=BeautifulSoup(open(f,encoding='utf-8',errors='ignore'),'html.parser')
    m=s.find('article') or s.find('main') or s.body
    hs=[h.get_text(' ',strip=True) for h in m.find_all(['h2','h3','h4','strong'])]
    print('==',f, s.title.get_text(strip=True) if s.title else '')
    print(hs[:120])
"
```

<details><summary>Výstup nástroja</summary>

```
total 228
drwxr-xr-x 2 filip filip   4096 Oct  9 13:26 .
drwxr-xr-x 4 filip filip   4096 Oct  9 13:25 ..
-rw-r--r-- 1 filip filip   2541 Oct  9 13:26 balteus.html
-rw-r--r-- 1 filip filip  52746 Oct  9 13:26 legalfirm.html
-rw-r--r-- 1 filip filip 108251 Oct  9 13:26 podnikajte.html
-rw-r--r-- 1 filip filip  30585 Oct  9 13:25 slovca-pridruzeni-clenovia.html
-rw-r--r-- 1 filip filip  21817 Oct  9 13:25 slovca-riadni-clenovia.html
== raw/balteus.html Access Forbidden
['Access Denied']
== raw/legalfirm.html Zoznam equity fondov | Hronček & Partners
['Zoznam equity fondov', 'z privátnych spoločností (private equity)', 'z\xa0verejných fondov', 'Zoznam private equity fondov', 'Benson Oak Capital', 'BHS private equity fund', 'Credo Ventures', 'Crowdberry', 'Enterprise Investors', 'Eterus Capital', 'Fond kvalifikovaných investorů', 'Genesis Capital', 'Jet Investment', 'J&T ARCH INVESTMENTS', 'Neulogy Ventures', 'Sandberg', 'ZAKA', '3TS Capital Partners', 'Verejné fondy', 'Fond inovácií a technológií', 'Národný holdingový fond', 'Slovenský rozvojový fond', 'Hronček & Partners', 'Odborné právne poradenstvo, ktoré Vám pomôže progresívne rásť']
== raw/podnikajte.html Private equity a venture kapitálové fondy pôsobiace v SR | Podnikajte.sk
['Veterinárna klinika ako podnikanie: čo môže veterinár delegovať na iných?', 'Ako prebieha pracovný pohovor s AI? Rozhovor môže viesť chatbot aj 3D avatar', 'Firma na Google mapách: Ako získať dopyty z okolia bez rozpočtu na reklamu?', 'Inšpirácia', '
… [skrátené, 4389 znakov]
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "slovenský startup získal investíciu 2026 fond viedol kolo", "mode": "extended"}
```

**Nástroj `WebSearch`**

```json
{"query": "Slovak startup raises seed round 2025 led by venture fund Bratislava", "mode": "extended"}
```

**Nástroj `WebSearch`**

```json
{"query": "NBS zoznam správcovských spoločností alternatívnych investičných fondov register subjektov finančného trhu", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "NBS zoznam správcovských spoločností alternatívnych investičných fondov register subjektov finančného trhu"

Links: [{"title":"ciastka27V 2013","url":"https://nbs.sk/_img/Documents/_Legislativa/_Vestnik/ciastka27V-2013.pdf"},{"title":"nbs.sk","url":"https://nbs.sk/dokument/bd086d02-541e-481d-b28b-37c1999a569f/stiahnut/?force=true"},{"title":"ciastka2V 2015","url":"https://nbs.sk/_img/Documents/_Legislativa/_Vestnik/ciastka2V-2015.pdf"},{"title":"ciastka2v 2015","url":"https://nbs.sk/_img/documents/_legislativa/_vestnik/ciastka2v-2015.pdf"},{"title":"nbs.sk","url":"https://nbs.sk/dokument/c4ee7eff-532a-422a-8aed-51d6ac379a37/stiahnut/?force=true"},{"title":"nbs.sk","url":"https://nbs.sk/dokument/6484c550-9cb5-4df7-8388-b22be39ffe0b/stiahnut/?force=true"},{"title":"ciaska 3 2012","url":"https://nbs.sk/_img/documents/_legislativa/_vestnik/ciaska-3-2012.pdf"},{"title":"nbs.sk","url":"https://nbs.sk/dokument/4dfca3c2-3daf-45c0-a770-6e1a37a4175d/stiahnut/?force=true"},{"title":"nbs.sk","url":"https://nbs.sk/dokument/d918e99a-6c2f-4524-96d6-ffb239440b69/stiahnut/?force=true"}]

I couldn't find a direct NBS list of alternative investment fund managers in these results, so I can't confirm where that list is published. The results do explain how the register relates to the regulation.

The most relevant item is an NBS measure on reporting by AIF managers. It covers three groups, including a person who manages AIFs after being entered in the register of AI
… [skrátené, 2622 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Slovak startup raises seed round 2025 led by venture fund Bratislava"

Links: [{"title":"Top Funding Rounds Raised by Slovak Startups in 2025","url":"https://therecursive.com/top-funding-rounds-raised-by-slovak-startups-in-2025/"},{"title":"Slovak startup Cequence secures €2M led by Czech Jet Ventures","url":"https://www.vestbee.com/insights/articles/cequence-secures-2-m"},{"title":"Slovak Startup Ecosystem Biggest Funding Rounds (H1 2025)","url":"https://therecursive.com/slovakia-startup-funding-h1-2025/"},{"title":"Slovak Cequence Raises €2M Seed Round","url":"https://lookai.vc/new-investment-cequence-secures-e2m-to-expand-ai-powered-contract-automation-platform/"},{"title":"Venture to Future Fund - Crunchbase Company Profile & Funding","url":"https://www.crunchbase.com/organization/venture-to-future-fund"},{"title":"Startups in Slovakia - 2026 Latest Funding Rounds, Trends and News - Tracxn","url":"https://tracxn.com/d/geographies/slovakia/__MqqTYQpms3Zdt99rMUzg_DtPUg8Uhg9VCov-EX2e7jg"},{"title":"37 VC-Backed Startups in Bratislava, Slovakia Slovak Republic (2026)","url":"https://www.vcbacked.co/directory/cities/slovakia-slovak-republic/bratislava"},{"title":"Slovak AI Startup Cequence Raises €2M Seed Funding to Scale Contract Management Platform - Startup Reporter","url":"https://www.startupreporter.eu/slovak-ai-startup-cequence/"},{"title":"Vision Ventures (Slovakia)","url":"https://altss.com/profile/vision-ventures-slovakia"}]

The closest
… [skrátené, 3671 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "slovenský startup získal investíciu 2026 fond viedol kolo"

Links: [{"title":"Z Brna do Dubaja: Nový fond nalial milióny do startupu, ktorý vznikol ako študentský projekt. Teraz mieri aj na Slovensko","url":"https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/"},{"title":"Slováci pomáhajú rásť svetovým herným štúdiám. Investori do nich naliali päť miliónov - Forbes Slovensko","url":"https://www.forbes.sk/slovaci-pomahaju-rast-svetovym-hernym-studiam-investori-do-nich-naliali-pat-milionov/"},{"title":"Seed Starter Slovenskej sporiteľne investuje 400-tisíc eur do startupu Webout. Ten získava spolu 1,65 milióna eur a mieri do Silicon Valley","url":"https://www.slsp.sk/sk/aktuality/2026/6/2/seed-starter-slovenskej-sporitelne-investuje-400-tisic-eur-do-startupu-webout-ten-ziskava-spolu-165-miliona-eur-a-mieri-do-silicon-valley"},{"title":"Česko-slovenský startup získava miliónovú investíciu. Dokonale vyplnil dieru na trhu","url":"https://www.startitup.sk/cesko-slovensky-startup-ziskava-milionovu-investiciu-dokonale-vyplnil-dieru-na-trhu/"},{"title":"Investícia 300-tisíc eur: Tri Slovenky vybudovali startup, ktorý zaujal nielen súkromný kapitál, ale aj štátny fond","url":"https://www.startitup.sk/investicia-300-tisic-eur-tri-slovenky-vybudovali-startup-ktory-zaujal-nielen-sukromny-kapital-ale-aj-statny-fond/"},{"title":"Slovenský biotechnologický startup Sensib
… [skrátené, 3994 znakov]
```

</details>

## Claude · 2026-10-09 11:26:59 UTC

Mám prvých slovenských kandidátov zo SLOVCA, zo zoznamov fondov a zo správ o investičných kolách. Teraz dohľadávam zvyšné čísla pre globálny odhad a potom napíšem `PLAN.md`.

**Nástroj `WebSearch`**

```json
{"query": "Center for Venture Research angel investor market active angels number 2023 2024", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "number of active corporate venture capital units worldwide 2024 2025", "mode": "standard"}
```

**Nástroj `WebFetch`**

```json
{"url": "https://therecursive.com/top-funding-rounds-raised-by-slovak-startups-in-2025/", "prompt": "List every funding round: startup, amount, date, and all named investors. Include the article publication date."}
```

<details><summary>Výstup nástroja</summary>

```
The page doesn't include the funding rounds. The article body is behind a subscriber paywall, and the visible text only says "This post is for subscribers only" and asks readers to sign up.

The only details I can confirm are:

- **Title:** Top Funding Rounds Raised by Slovak Startups in 2025
- **Author:** Teodora Atanasova
- **Publication date:** January 20, 2026

The related article links on the page cover other companies and regions, so I haven't counted them as Slovak rounds. To get the startups, amounts, dates, and investors, you'll need to sign in or subscribe to The Recursive, or find the article through another source.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Center for Venture Research angel investor market active angels number 2023 2024"

Links: [{"title":"paulcollege.unh.edu","url":"https://paulcollege.unh.edu/sites/default/files/media/2025-12/FY%202024%20Analysis%20Report%20Final.pdf"},{"title":"- July 3, 2024","url":"https://eban.org/?p=40179"},{"title":"eban.org","url":"https://eban.org/center-for-venture-research-the-angel-market-in-2023-an-inflection-point-for-women-angels/amp"},{"title":"UNH Center for Venture Research: U.S. Angel Investor Market in 2014 Made a Market Correction in Deal Size","url":"https://unh.edu/unhtoday/node/7026"},{"title":"center for venture research the angel market in 2023 an inflection point for women angels","url":"https://www.eban.org/industry-reports/center-for-venture-research-the-angel-market-in-2023-an-inflection-point-for-women-angels/"},{"title":"fy 2022 analysis report final","url":"https://paulcollege.unh.edu/sites/default/files/resource/files/fy_2022_analysis_report_final.pdf"},{"title":"center for venture research the angel market in 2023 an inflection point for women angels","url":"https://eban.org/center-for-venture-research-the-angel-market-in-2023-an-inflection-point-for-women-angels"},{"title":"axis intelligence","url":"https://axis-intelligence.com/?p=40436"},{"title":"www.unh.edu","url":"https://www.unh.edu/unhtoday/node/11005"},{"title":"The Angel Market in 2021: Metrics Indicate Strong Market – By Center for Venture Research","url":"https://www.
… [skrátené, 3216 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "number of active corporate venture capital units worldwide 2024 2025"

Links: [{"title":"Where Global Innovation","url":"https://globalventuring.com/intelligence/?p=958"},{"title":"Where Global Innovation","url":"https://globalventuring.com/intelligence/2026-wocv-3-leadership-society-welcome"},{"title":"Where Global Innovation","url":"https://globalventuring.com/intelligence/2026-wocv-1-contents"},{"title":"Where Global Innovation","url":"https://globalventuring.com/intelligence/?p=1227"},{"title":"# More than 50 corporate investment funds created in 2025","url":"https://globalventuring.com/corporate/asia/50-corporate-investment-funds-2025/?format=md"},{"title":"# Startup funding rounds involving corporate investors rise 20% by value","url":"https://globalventuring.com/corporate-investors-trends-2025/?format=md"},{"title":"# CVC takes a larger role in corporate innovation spend","url":"https://globalventuring.com/corporate/cvc-proportion-corporate-innovation-spend/?format=md"},{"title":"50 corporate investment funds 2025","url":"https://globalventuring.com/corporate/asia/50-corporate-investment-funds-2025/"},{"title":"# Here&#8217;s what a typical CVC unit looks like","url":"https://globalventuring.com/corporate/cvc-directory-trends/?format=md"}]

Global Corporate Venturing (GCV) is the main source here, and its figures for 2024 and 2025 don't fully agree with each other.

**Active corporate investors**
- For 2025, the GCV survey puts the number
… [skrátené, 3468 znakov]
```

</details>

## Claude · 2026-10-09 11:27:11 UTC

Mám dosť podkladov a píšem `PLAN.md` (pravidlá, overovanie, odhady s citovanými zdrojmi).

**Nástroj `Write`**

`/home/filip/investor-db/PLAN.md`
```
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
| `pe` | Buy
… [skrátené, 8593 znakov]
```

<details><summary>Výstup nástroja</summary>

```
File created successfully at: /home/filip/investor-db/PLAN.md (file state is current in your context — no need to Read it back)
```

</details>

## Claude · 2026-10-09 11:28:11 UTC

`PLAN.md` je hotový. Teraz zbieram slovenských kandidátov z ďalších zdrojov (štátne programy a správy o investičných kolách).

**Nástroj `WebFetch`**

```json
{"url": "https://therecursive.com/slovakia-startup-funding-h1-2025/", "prompt": "List every funding round: startup, amount, month, and every named investor. Include publication date."}
```

**Nástroj `WebSearch`**

```json
{"query": "Slovak Investment Holding venture capital nástroje 2025 2026 investície do startupov správca fondu", "mode": "extended"}
```

**Nástroj `WebSearch`**

```json
{"query": "nový slovenský venture fond 2025 OR 2026 spúšťa fond miliónov eur startupy Slovensko", "mode": "extended"}
```

<details><summary>Výstup nástroja</summary>

```
The page doesn't include the funding rounds. The article is behind a subscriber paywall, and the text shows only the teaser: "This post is for subscribers only."

What the page does show:

- **Title:** "Slovak Startup Ecosystem Biggest Funding Rounds (H1 2025)"
- **Publication date:** July 31, 2025
- **Author:** Teodora Atanasova, The Recursive
- **Listed rounds, startups, amounts, months, and investors:** none

The other headlines on the page, such as EnduroSat, ElevenLabs, and Varda, are separate articles and don't provide Slovak H1 2025 round details.

To get the full list, you could subscribe to The Recursive or paste the article text here, and I'll extract the startups, amounts, months, and named investors.
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "Slovak Investment Holding venture capital nástroje 2025 2026 investície do startupov správca fondu"

Links: [{"title":"Domov","url":"https://www.sih.sk/en/"},{"title":"Slovak Investment Holding - 2026 Investor Profile, Portfolio, Team & Investment Trends - Tracxn","url":"https://tracxn.com/d/venture-capital/slovak-investment-holding/__tjVxlFXqLGRs2qT_DSyshq5mSj3rkiqhhq4iSORfe08"},{"title":"Nový impulz pre podnikanie: Slovak Investment Holding spúšťa atraktívne financovanie pre firmy a inovácie - euBrief","url":"https://eubrief.sme.sk/ekonomika-a-euro/c/novy-impulz-pre-podnikanie-slovak-investment-holding-spusta-atraktivne-financovanie-pre-firmy-a-inovacie"},{"title":"Venture to Future Fund navyšuje kapitál o 15,3 milióna EUR na podporu slovenských startupov","url":"https://www.sih.sk/aktuality/venture-to-future-fund-increases-capital-by-eur-15-3-million-to-support-slovak-startups"},{"title":"Startups in Slovakia - 2026 Latest Funding Rounds, Trends and News - Tracxn","url":"https://tracxn.com/d/geographies/slovakia/__MqqTYQpms3Zdt99rMUzg_DtPUg8Uhg9VCov-EX2e7jg"},{"title":"Novinky","url":"https://www.sih.sk/aktuality"},{"title":"Top Venture Capital Fund in Slovakia (Oct, 2025) - Tracxn","url":"https://tracxn.com/d/investor-lists/venture-capital-funds-in-slovakia/__DvmbYfeSMp1bcVhFxyHfn9j2EYVdLnk4ZwIEYR1zzuM"},{"title":"9 Trailblazing Venture Capital Firms Powering Bratislava's Startup Surge","url":"https://www.papermark.com/blog/venture-capital-f
… [skrátené, 5557 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "nový slovenský venture fond 2025 OR 2026 spúšťa fond miliónov eur startupy Slovensko"

Links: [{"title":"Štát spúšťa nové fondy pre startupy: SIH hľadá správcov 90 miliónov eur","url":"https://openiazoch.zoznam.sk/financie/stat-spusta-nove-fondy-pre-startupy-sih-hlada-spravcov-90-milionov-eur/"},{"title":"Venture to Future Fund navyšuje kapitál na podporu slovenských startupov o 15,3 mil. eur - SITA Financie","url":"https://sita.sk/vofinanciach/venture-to-future-fund-navysuje-kapital-na-podporu-slovenskych-startupov-o-153-mil-eur/"},{"title":"Venture to Future Fund navyšuje kapitál o 15,3 milióna EUR na podporu slovenských startupov","url":"https://www.sih.sk/aktuality/venture-to-future-fund-increases-capital-by-eur-15-3-million-to-support-slovak-startups"},{"title":"Startup Archives - grantUP","url":"https://grantup.sk/tag/startup/"},{"title":"Venture to Future Fund navyšuje kapitál o 15,3 milióna EUR na podporu slovenských startupov","url":"https://slord.sk/aktualita/venture-to-future-fund-navysuje-kapital-o-153-miliona-eur-na-podporu-slovenskych-startupov/"},{"title":"Z Brna do Dubaja: Nový fond nalial milióny do startupu, ktorý vznikol ako študentský projekt. Teraz mieri aj na Slovensko","url":"https://www.startitup.sk/z-brna-do-dubaja-novy-fond-nalial-miliony-do-startupu-ktory-vznikol-ako-studentsky-projekt-teraz-mieri-aj-na-slovensko/"},{"title":"Slovenské startupy už nemusia odchádzať do zahraničia. Vznikol jedinečný fond na ich podporu",
… [skrátené, 4757 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.papermark.com/blog/venture-capital-firms-bratislava", "prompt": "List every firm named, with any claimed details (focus, ticket, website). Give the article date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://tracxn.com/d/investor-lists/venture-capital-funds-in-slovakia/__DvmbYfeSMp1bcVhFxyHfn9j2EYVdLnk4ZwIEYR1zzuM", "prompt": "List every investor name visible on the page, in order."}
```

<details><summary>Výstup nástroja</summary>

```
The page names 10 investors, in this order:

1. McWin
2. Ergos
3. Venture to Future Fund
4. Zero Gravity Capital
5. 365fintech
6. Neulogy Ventures
7. Slovak Investment Holding
8. Eterus Capital
9. Vision Ventures
10. Zero One Hundred

The first five have full profiles on the page. The last five appear only in the "Top Investors" table of contents, where they're marked with a lock icon, so their profiles are not shown.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Article date:** Published January 15, 2025; last updated February 28, 2026.

The article names nine firms. Details are as the article states them, and I haven't verified them.

| Firm | Focus | Investment (per article) | Website |
|---|---|---|---|
| Neulogy Ventures | Deep-tech, software, AI | €0.25M–€2M, seed/Series A | neulogy.vc |
| Zero Gravity Capital | B2B and B2C software, platform tech | €0.1M–€1M, seed | 0100.vc (linked under this name) |
| Vision Ventures | SaaS, digital platforms, web apps | €0.1M–€0.5M initial tickets | visionventures.vc |
| Venture to Future Fund (VFF) | Growth capital, industrial tech, digitisation | €1M–€10M, Series A–C | vff.sk/en |
| Crowdberry a.s. | Retail and institutional co-investment, SMEs, real estate | €0.1M–€3M per deal | crowdberry.eu/en |
| ZAKA Ventures | Health-tech, life science, deep-tech | €0.2M–€1.5M, seed | zaka.vc |
| IPM Growth / IPM Group | Infrastructure tech, energy, deep-tech scale-ups | €3M–€20M, growth rounds | ipmllp.com |
| Slovak Investment Holding (SIH) | Growth capital, innovation financing | €1M–€20M, various instruments | sih.sk/en |
| BIC Bratislava | Seed co-investment, EU innovation projects | €50K–€300K co-investments | bic.sk |

The article is inconsistent in places. Its quick list and table describe some firms differently from the detailed profiles. For example, it calls Crowdberry a crowd-based platform and lists BIC Bratislava and the others as "accelerators" in the table.
```

</details>

## Claude · 2026-10-09 11:28:51 UTC

Mám dosť kandidátov. Zapíšem ich do `data/candidates.csv`, pričom pri každom uvediem, odkiaľ pochádza.

**Nástroj `Bash`**

```bash
mkdir -p ~/investor-db/data && cat > ~/investor-db/data/candidates.csv <<'EOF'
candidate_id,name,discovery_source,discovery_url,retrieved_at
c001,ARX Equity Partners,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c002,CVI,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c003,Enterprise Investors,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c004,Eterus Capital,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c005,Fond inovácií a technológií,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c006,Genesis Capital,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c007,Jet Investment,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c008,Národný holdingový fond,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c009,Neulogy Ventures,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c010,Sandberg Capital,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c011,Venture to Future Fund,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c012,Vision Ventures,slovca_full_member,https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html,2026-10-09
c013,Across Private Investments,slovca_associate_member,https:/
… [skrátené, 9202 znakov]
```

<details><summary>Výstup nástroja</summary>

```
76 /home/filip/investor-db/data/candidates.csv
```

</details>

## Claude · 2026-10-09 11:29:25 UTC

Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access

## Používateľ · 2026-10-09 11:32:23 UTC

co to znamena ako to vyriesim

## Claude · 2026-10-09 11:32:23 UTC

Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access

## Používateľ · 2026-10-09 11:32:40 UTC

pokracuj

## Claude · 2026-10-09 11:32:41 UTC

Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
