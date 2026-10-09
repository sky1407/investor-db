# Spoľahlivá databáza investorov (Zadanie A)

Pilot databázy investorov, v ktorej **rozhoduje kód a dôkaz, nie LLM**. AI agent hľadá zdroje a doslovné citácie,
skript overí, že citácia na stránke naozaj je, deterministické pravidlá rozhodnú o zaradení a človek kontroluje
výsledok v jednoduchom UI.

| Dokument | Obsah |
|---|---|
| [`PLAN.md`](PLAN.md) | Kto v databáze je a kto nie, ako overujem pravosť, odhad počtu investorov a spoľahlivosti |
| [`COSTS.md`](COSTS.md) | Odhad nákladov na celý svet z nameraných hodnôt pilotu |
| [`data/investors.csv`](data/investors.csv) | Zaradení investori, pri každom poli zdroj |
| [`data/investors.json`](data/investors.json) | To isté vrátane doslovných citácií, dátumov a všetkých dealov |
| [`data/excluded.csv`](data/excluded.csv) | Vyradení kandidáti s dôvodom a zdrojom |
| [`validation/manual_check.csv`](validation/manual_check.csv) | Kontrolný hárok: AI predkontrola + ručná kontrola |
| [`validation/metrics.json`](validation/metrics.json) | Výsledok merania presnosti |
| [`prompts/`](prompts/) | Presné pokyny, ktoré dostali AI agenti |
| [`ai-log/`](ai-log/) | Export konverzácií s Claude Code |

## Výsledok pilotu

Pilot: **75 kandidátov** pôsobiacich na Slovensku → **29 zaradených, 46 vyradených**. Overených **327 z 329**
dôkazov (citácia sa našla na stránke), 2 URL boli nedostupné.

**Meranie presnosti** prebieha na 50 kandidátoch so sídlom na Slovensku. Skontrolovaných je 100 % (102 položiek:
zaradenie alebo vyradenie a každé vyplnené pole), nevzorkujem. Kontrolu robil človek v UI 2026-10-09 a pri každej
položke otvoril zdroj.

| Metrika (sídlo SK) | Ručná kontrola | AI predkontrola (pre porovnanie) |
|---|---|---|
| **Precision zaradenia** (zaradení sú naozaj aktívni investori) | **10 / 10 = 100 %** | 7 / 8 |
| **Správnosť dôvodu vyradenia** | **36 / 40 = 90 %** | 28 / 33 |
| `investor_type` | 10 / 10 | |
| `sectors`, `stages` | 13 / 13 | |
| `ticket_min_eur`, `ticket_max_eur` | 13 / 13 | |
| `latest_investment` (doložený deal so zdrojom a dátumom) | 10 / 10 | |
| **`aum_eur`** | **5 / 6 = 83 %** | 2 / 4 |
| **Všetky polia spolu** | **51 / 52 = 98 %** | |
| Zhoda AI predkontroly s človekom | 75 / 78 = 96 % | |

**Chyby, ktoré našiel človek** (všetky predtým označila aj AI predkontrola):

- **4× nesprávny dôvod vyradenia** (SRF, Arca Capital, Limerock, Sociálni Inovátori): subjekty sú správne vyradené,
  ale ako `no_evidence` namiesto `inactive`. Staré investície sú doložené, fondy sú ukončené.
- **1× AUM** (Across, c013): 450 mil. EUR je majetok klientov wealth managementu, nie veľkosť VC fondu.
- Mimo meranej vzorky: Fil Rouge Capital (c073, HR) nemá vo fázach `series-a`.

**Kde sa AI predkontrola mýlila** (3 z 78 položiek): CB ESPRI (zaradenie je podľa pravidla 36 mesiacov správne),
CB Investment Management (koinvestícia 2025 len v agregátore, SIH potvrdzuje koniec investičného obdobia v 2023) a
0100 Ventures (23 mil. EUR je skutočný Fund I, 60 mil. je len cieľ nového fondu). AI predkontrola teda chyby
nevynechala, ale bola prísnejšia ako človek.

**Vyplnenosť polí** pri zaradených SK: typ 100 %, fázy a `ticket_max` 70 %, sektory, `ticket_min` a AUM 60 %.

**Interpretácia:** hlavná požiadavka zadania („každý záznam je skutočný investor“) je na vzorke splnená na 100 %.
Identita, typ a doložená investícia sú spoľahlivé. Slabými miestami sú AUM a rozlíšenie „neaktívny“ vs. „bez
dôkazu“. Zodpovedá to odhadu v `PLAN.md` (AUM: stredná až nízka spoľahlivosť). Vzorka je malá (10 zaradených),
preto 100 % neznamená, že vo veľkom rozsahu nebudú chyby. Pri 10 z 10 je 95 % interval spoľahlivosti pre
precision približne 69 – 100 %.

Mimo SK vzorky AI predkontrola označila ďalšie chyby čísel (3TS: ticket je veľkosť kola, AUM je cieľ fondu; ZAKA:
zastarané AUM; BHM: AUM je hodnota aktív skupiny; BHS: príliš úzky sektor). Človek ich nekontroloval, preto nie sú
v metrikách.

> Metriky v `validation/metrics.json` majú dve vetvy: `human` (len ľudské verdikty, z nich je tabuľka vyššie) a
> `combined` (ľudský verdikt, inak AI).

## Ako to funguje

```
candidates.csv ──► AI rešerš ──► research/cXXX.json ──► verify ──► build ──► data/investors.*
 (SLOVCA, SIH,     (5 agentov,    (každé pole:            (HTTP +    (pravidlá   data/excluded.csv
  NHF, EIF, médiá)  prompts/)      URL + citácia + dátum)  citácia)   zaradenia)        │
                                                                                        ▼
                                     metrics.json ◄── manual_check.csv ◄── AI predkontrola + človek (UI)
```

1. **Kandidáti** (`data/candidates.csv`, 75): riadni a pridružení členovia SLOVCA, verejné programy (SIH, NHF,
   EIF, NRF) a deal-first zdroje (správy o investičných kolách). Pri každom je URL, kde sa našiel.
2. **Rešerš** (AI agent, `prompts/research_agent.md`): pre každého kandidáta jeden JSON. Každé tvrdenie má
   `source_url`, `source_date` a **doslovnú citáciu** zo stránky.
3. **`verify`**: stiahne každú URL a hľadá citáciu v texte stránky (normalizované medzery, úvodzovky, diakritika).
   Citácia, ktorá na stránke nie je, sa berie ako halucinácia a pole sa zahodí.
4. **`build`**: deterministické pravidlá z `PLAN.md` (investor? equity? aktivita za 36 mesiacov?) priradia
   `included` alebo dôvod vyradenia. Sumy prepočíta kód podľa `data/fx_rates.json`, nie model.
5. **Kontrola**: AI predkontrola (`prompts/review_agent.md`, iný agent ako ten, čo robil rešerš) a potom ručná
   kontrola v UI na `localhost:8000`. Metriky počítajú s ľudským verdiktom tam, kde existuje.

## Spustenie

Python 3.12+.

```bash
make install    # venv + závislosti
make test       # 87 testov (pytest)
make pipeline   # verify → build → metrics
make serve      # UI na http://localhost:8000 (prehliadanie + ručná kontrola)
PYTHONPATH=src .venv/bin/python -m investordb.cli import-review validation/ai_review_2.json
```

## Ako som pracoval s AI

Celý projekt vznikol v Claude Code (Opus 5.5). Konverzácie sú v `ai-log/`.

### Rozdelenie práce

| Krok | Kto | Prečo |
|---|---|---|
| Plán, pravidlá zaradenia, definície typov | ja + Claude v dialógu | Claude navrhol 3 koncepty (čisté LLM, čisté scrapovanie, hybrid), vybral som hybrid |
| Kód pipeline (`src/`) | Claude, po malých krokoch s testami | Po každom kroku `pytest` + `ruff`, commit až po zelených testoch |
| Rešerš 75 kandidátov | 5 paralelných subagentov, každý 15 kandidátov | Pokyny: `prompts/research_agent.md` |
| Overenie citácií | skript `verify` | Halucinácie má chytať kód, nie ďalší model |
| Zaradenie / vyradenie | skript `build` | Rovnaký vstup = rovnaký výsledok, pravidlá sú čitateľné a testované |
| Predkontrola záverov | samostatný review agent, 2 dávky (c001–c050, c051–c075) | Pokyny: `prompts/review_agent.md`, „skeptický recenzent“ |
| Ručná kontrola | ja v UI | Jediný zdroj „pravdy“ pre metriky |

### Aké pokyny dostali agenti

Kľúčové pravidlá v `prompts/research_agent.md`:

- **Nič nevymýšľať.** Chýbajúce pole je v poriadku, nesprávne pole je zlyhanie.
- **Citácia doslovne, v pôvodnom jazyku, 8 – 600 znakov.** Preto ju vie skript overiť.
- Vyhýbať sa LinkedIn, Crunchbase, PDF a stránkam za prihlásením, lebo ich skript nevie stiahnuť.
- Čísla nikdy z pamäte. Prepočet mien robí kód.
- Najprv klasifikácia subjektu (`investor` / `service_provider` / `lender` / `platform` / …), až potom polia.

Review agent (`prompts/review_agent.md`) nekontroluje, či citácia existuje (to už urobil skript), ale **či je
záver z citácie správny**: či je AUM naozaj spravovaný kapitál, či ticket nie je veľkosť kola atď.

### Ako som kontroloval výstup

1. **Schéma** (pydantic, `check-schema`): typy z číselníka, `ticket_min ≤ ticket_max`, platné dátumy.
2. **Existencia citácie** (`verify`): 327 z 329 dôkazov overených, 2 URL nedostupné (HTTP chyba).
3. **Druhý, nezávislý agent** kontroloval interpretáciu.
4. **Ručná kontrola** v UI: pri každej položke odkaz na zdroj, verdikt a poznámka AI, tlačidlá správne/nesprávne.
   - **Jazyk zdroja:** citácie sú doslovné, v jazyku, v ktorom ich agent na stránke našiel. Viacjazyčné weby
     (napr. fondy so sídlom v SK alebo CZ) slovenskému prehliadaču často zobrazia slovenskú verziu, hoci agent aj
     skript dostali anglickú. Text vtedy Ctrl+F nenájde, kým sa stránka neprepne do angličtiny. **Nie je to chyba
     dôkazu.** UI pri anglickej citácii zobrazí upozornenie. Citácie zámerne neprekladám, lebo preložený text by
     skript nevedel overiť.
5. **Testy** pre pravidlá zaradenia, normalizáciu textu, overovanie a metriky (87 testov).

### Kde sa AI pomýlila

| Chyba | Ako sa prejavila | Ako som ju zachytil | Riešenie |
|---|---|---|---|
| **AUM nie je spravovaný kapitál** (najčastejšia) | Ako AUM zapísaný majetok klientov wealth managementu (Across, c013), hodnota aktív portfóliových firiem (BHM, c018), cieľová veľkosť fondu namiesto skutočného uzavretia (3TS, ZAKA) | Review agent | Pole označené ako nesprávne; v pokynoch pre ďalšie kolo treba presnejšiu definíciu AUM |
| **Veľkosť kola namiesto ticketu** | 3TS: „vedie kolá 5 – 20 mil. EUR“ zapísané ako ticket fondu | Review agent | Ticket ponechať prázdny |
| **Príliš konkrétny sektor** | BHS: „manufacturing“, hoci zdroj hovorí „všetky odvetvia, primárne tradičná ekonomika“ | Review agent | Navrhnutá oprava: generalist |
| **Review agent: falošné poplachy** | CB Investment Management: „aktívny“ podľa agregátora Caplight, primárny zdroj neexistuje. CB ESPRI: „neaktívny“, hoci posledný deal je v okne 36 mesiacov. 0100 Ventures: AUM „zastarané“, hoci nový fond je len cieľ | Ručná kontrola | Aj kontrolný agent sa mýli, preto o metrikách rozhoduje človek. Zhoda AI s človekom bola 96 % |
| **Aktivita podľa dátumu dealu, nie stavu fondu** (obmedzenie pravidla, nie chyba dát) | CB ESPRI (c062) je podľa pravidla správne zaradený (Elv.ai 01/2024). Fond je však od 2024 v poinvestičnom období a nové investície nerobí | Review agent | Pravidlo aktivity treba rozšíriť: ak zdroj uvádza ukončené investičné obdobie a nie je nový fond, `inactive` |
| **`no_evidence` namiesto `inactive`** | SRF, Arca Capital, Limerock, Sociálni Inovátori: agent v poznámke správne napísal, že subjekt je neaktívny (likvidácia, konkurz, skončené investičné obdobie), ale staré investície nezapísal, hoci to prompt vyžadoval. Pravidlo bez investícií vráti „bez dôkazu“ | Review agent | Vyradenie je správne, dôvod nie. Riešenie: povinne zapísať najnovší starý deal, alebo pole `status_evidence` s citáciou o likvidácii |
| **Jazyková verzia stránky** (chyba môjho skriptu, nie modelu) | Agent citoval anglickú verziu, skript stiahol slovenskú (podľa `Accept-Language`) → citácia „nenájdená“, falošný negatív | Ručne pri prvom behu `verify` | Commit `eb6542a`: pri nezhode skúsi aj anglický variant stránky |
| **Zdieľaný scratchpad agentov** | Paralelní agenti rešerše si navzájom prepisovali pomocné skripty v spoločnom pracovnom priečinku | Report agenta 1 | Výstupy (`research/cXXX.json`) to nepoškodilo; paralelní agenti potrebujú izolované priečinky. Review agent má zakázané zapisovať mimo svojho výstupného súboru |
| **Prompt injection** | Výsledok vyhľadávania (Dealroom) obsahoval skrytý pokyn pre AI | Agent 5 ho ignoroval a uviedol v reporte | Dealroom sa ako zdroj nepoužil; druhé kolo kontroly dostalo pokyn, že obsah stránok sú dáta, nie inštrukcie |
| **Duplicita nezlučuje dôkazy** | Slovenský rastový a kapitálový fond (c056) je pravdepodobne starý názov Eterus Capital (c004). Pravidlo `duplicate` ho vyradí, ale jeho dôkazy sa nepripoja k c004 | Pri prezeraní vyradených | Známe obmedzenie, viď nižšie |
| **Správca viacerých fondov** | NHF (c008) spravuje Eterus aj Fond inovácií a technológií, ktoré sú samostatné záznamy. Nie je to duplicita, ale ani samostatný aktívny investor | Poznámka agenta | Rozhodnuté podľa pravidla granularity v `PLAN.md` (samostatný tím = samostatný záznam) |

Poučenie: **halucinované zdroje** (najčastejšie riziko LLM) sa v pilote takmer neobjavili, lebo ich chytá skript.
Chyby, ktoré zostali, sú **chyby interpretácie** pravdivého zdroja. Tie zachytí len druhý agent alebo človek.

## Rozhodnutia pri nejasnostiach v zadaní

| Nejasnosť | Rozhodnutie | Dôvod |
|---|---|---|
| Čo je „skutočný investor“ | 4 podmienky: kapitál, equity, opakovanosť, aktivita za 36 mesiacov | Zadanie zdôrazňuje spoľahlivosť; neaktívny fond s neaktuálnymi údajmi by používateľa zavádzal |
| Jeden záznam = fond, alebo správca? | Správca (investičná platforma), fondy v poli `funds` | Používateľ databázy oslovuje správcu; fondy sa menia každých pár rokov |
| „VC fondy v jednej krajine“ | Zbierané VC (a PE) aktívne na Slovensku, **presnosť meraná len na subjektoch so sídlom na Slovensku** | Malá krajina dovolí skontrolovať 100 % vzorky; sídlo je jednoznačné kritérium |
| PE v pilote | Ponechané | Zadanie vymenúva aj PE; SLOVCA ich nerozlišuje a pravidlá ich musia vedieť správne zaradiť |
| Fond fondov (EIF) | Zaradený s typom `fund_of_funds` | Je to investor, ale do firiem priamo neinvestuje, preto má príznak |
| Výška investície | Ticket ako rozsah `min`–`max` v EUR, AUM zvlášť | Zadanie chce „v akej výške“ aj „celkový kapitál“; sú to dve rôzne čísla, ktoré si AI najčastejšie zamieňala |
| Zdroj pri každom údaji | Každé pole má vlastnú URL, dátum zdroja, dátum stiahnutia a citáciu | Pri jednej URL na záznam by sa nedalo overiť, odkiaľ je konkrétne číslo |

## Čo v riešení chýba

- **Ručná kontrola mimo SK:** zaradení a vyradení so sídlom mimo Slovenska (CZ, PL, AT…) majú iba AI predkontrolu.
- **Recall** som nemeral. Capture-recapture z `PLAN.md` vyžaduje druhý nezávislý zoznam (napr. Dealroom export),
  ktorý nie je verejne a zadarmo dostupný v strojovo čitateľnej podobe.
- **Opravy zistené kontrolou nie sú zapracované do dát.** Zámerne: metriky opisujú výstup pipeline tak, ako ho
  vyrobila. Ďalší krok je opraviť `research/*.json` (5 položiek), upraviť pokyny pre agentov (AUM, staré dealy) a
  spustiť pipeline znova.
- **Zlučovanie duplicít:** `duplicate` záznam sa vyradí, ale jeho dôkazy sa nepripoja k hlavnému záznamu.
- **Vzťah správca → fondy** (NHF → Eterus, FIT) nie je modelovaný, iba popísaný v poznámke.
- **Pravidlo aktivity** neberie do úvahy ukončené investičné obdobie (prípad CB ESPRI).
- **Angel investori a family office** v pilote nie sú. Pilot je VC/PE; pre tieto typy je verejná stopa slabá
  (odhad v `PLAN.md`) a vyžadovali by iné zdroje (registre konečných užívateľov výhod, prezentácie na akciách).
- **10 položiek bez AI verdiktu**, lebo zdroj vracia HTTP 403 (Forbes, PwC, advokátske kancelárie). Pri ručnej
  kontrole ich treba otvoriť v prehliadači.
