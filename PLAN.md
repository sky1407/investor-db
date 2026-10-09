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
| `public_fund` | Štátny alebo nadnárodný fond, ktorý **priamo** investuje equity do firiem (SIH, NHF) |
| `fund_of_funds` | Investuje len do iných fondov (napr. EIF). Zaraďuje sa, ale s príznakom, lebo do firiem neinvestuje priamo |

### Vyradenie (pole `exclusion_reason`)

| Kód | Kto | Prečo |
|---|---|---|
| `not_investor_service` | Advokáti, audítori, M&A poradcovia, konzultanti (napr. pridružení členovia SLOVCA) | Neinvestujú kapitál, iba poskytujú služby investorom |
| `debt_only` | Banky, lízing, nebankové úvery | Nezískavajú vlastnícky podiel |
| `platform_only` | Crowdfundingové platformy, ktoré len sprostredkúvajú | Investujú tretie strany. Ak má platforma vlastný fond (Crowdberry, CB Investment Management), zaraďuje sa **fond**, nie platforma |
| `grant_only` | Grantové schémy, dotácie | Nezískavajú podiel |
| `public_markets_only` | Hedge fondy, podielové fondy na verejné akcie | Neinvestujú do súkromných firiem |
| `inactive` | Bez doloženej investície alebo nového fondu za 36 mesiacov | Údaje by mohli byť zavádzajúce |
| `no_evidence` | Nenašiel sa žiadny overiteľný verejný dôkaz investície | Nedá sa overiť pravosť |
| `duplicate` | Rovnaký subjekt pod iným názvom (správca vs. fond) | Jeden záznam na investičnú platformu |

### Granularita

Jeden záznam = **investičná platforma (správca)**, nie jednotlivý fond. Napríklad „Neulogy Ventures“ je jeden záznam a jeho fondy sú v poli `funds`. Dôvod: v praxi chce používateľ databázy osloviť správcu a fondy sa každých pár rokov menia.

**Hraničný prípad:** fond, ktorý je samostatnou právnickou osobou s vlastným tímom (Venture to Future Fund), je samostatný záznam.

### Geografia

Krajina záznamu je **sídlo správcu**. Zahraničný fond, ktorý aktívne investuje na Slovensku (Jet Ventures, Credo), dostane `country` podľa sídla a do `active_in` sa pridá `SK`. V pilote vytvárame zoznam „VC aktívne na Slovensku“, ale **presnosť meriame iba na fondoch so sídlom na Slovensku**, aby vzorka bola jednoznačná.

## 2. Polia záznamu a zdroje

Každé fakticky tvrdené pole má vlastný dôkaz `{value, source_url, source_date, retrieved_at, quote}`:

| Pole | Význam |
|---|---|
| `name`, `legal_name`, `ico` / `reg_no`, `country`, `website` | Identita |
| `investor_type` | Viď tabuľka vyššie |
| `sectors` | Sektory, do ktorých investuje (napr. fintech, B2B SaaS, deep tech) |
| `stages` | pre-seed / seed / A / B+ / growth / buyout |
| `ticket_min_eur`, `ticket_max_eur` | Bežná výška jednej investície |
| `aum_eur` | Celkový investičný kapitál (veľkosť fondu alebo fondov) |
| `evidence_investments[]` | Aspoň 1 doložená investícia: firma, dátum, URL |
| `confidence` | `high` / `medium` / `low` |

`quote` je doslovný úryvok zo zdroja. Umožňuje automaticky overiť, že tvrdenie na stránke naozaj je (pozri časť 3).

## 3. Ako overím pravosť a zaradenie

**Pipeline (koncept C, hybrid):**

1. **Kandidáti** (`data/candidates.csv`) z troch typov zdrojov, pri každom je URL, kde sa kandidát našiel:
   - **asociácie:** SLOVCA, Invest Europe, CVCA,
   - **verejné programy:** SIH, NHF, EIF, NRF (Národný rozvojový fond),
   - **deal-first:** tlačové správy a médiá o investičných kolách (Forbes, Startitup, The Recursive, Vestbee).
2. **Rešerš (AI agent):** pre každého kandidáta nájde web, portfólio a aspoň 1 datovaný deal. Do JSON zapíše dôkazy vrátane doslovných citácií.
3. **Automatická kontrola (`verify.py`):**
   - URL odpovedá HTTP 2xx,
   - doslovná `quote` sa nachádza v texte stránky (normalizované medzery a diakritika). Toto chytá **halucinované zdroje**, najčastejšiu chybu LLM,
   - dátum dôkazu je v okne 36 mesiacov,
   - schéma (pydantic): ticket_min ≤ ticket_max, mena prepočítaná na EUR, typy z číselníka.
4. **Pravidlá zaradenia (`build.py`):** deterministicky z overených dôkazov priradí `included` alebo `exclusion_reason`. Rozhoduje kód, nie LLM.
5. **Ručná kontrola:** človek otvorí zdroj a pre každý záznam vyplní `validation/manual_check.csv`.
   - Pre každý zaradený záznam: je to skutočný aktívny investor? Sedí typ?
   - Pre každé pole: zhoduje sa so zdrojom?
   - Pre vyradené záznamy: je dôvod vyradenia správny?

**Metriky (`metrics.py`):**
- **Precision zaradenia** = správne zaradené / všetky zaradené. Toto je hlavná požiadavka zadania („každý záznam je skutočný investor“).
- **Správnosť vyradenia** = správne vyradené / všetky vyradené.
- **Presnosť polí** = správne hodnoty / vyplnené hodnoty pre `investor_type`, `sectors`, ticket a AUM zvlášť.
- **Vyplnenosť polí** = podiel záznamov, kde pole nie je prázdne.
- **Recall** sa nedá zmerať presne, lebo neexistuje úplný zoznam. Odhadujem ho cez **capture-recapture**: koľko fondov z deal-first zdroja už bolo v asociačných zdrojoch.

## 4. Odhad: koľko investorov sa dá získať z verejných zdrojov

| Typ | Odhad počtu aktívnych vo svete | Zdroj odhadu | Verejne overiteľné (môj odhad) | Očakávaná spoľahlivosť |
|---|---|---|---|---|
| VC | 4 000 – 7 000 | Decile Group, „guesstimate“ z panelových dát | 80 – 90 % (fondy zverejňujú portfólio) | vysoká |
| PE | ~ 7 000 (z toho ~ 6 000 v USA) | American Investment Council cez Vault; Preqin 2009: 4 270 až 6 000 | 70 – 85 % (deal PR, v USA SEC Form ADV) | vysoká |
| CVC | 2 300 – 3 100 | Global Corporate Venturing 2024/2025 | 70 – 80 % | vysoká |
| Single family office | ~ 8 000 (2024) | Deloitte, Defining the Family Office Landscape | **10 – 25 %** (FO zámerne nezverejňujú) | stredná |
| Angel | ~ 445 000 aktívnych iba v USA (2024) | UNH Center for Venture Research | **1 – 5 %** (verejne doložené ≥2 investície) | nízka až stredná |

**Realistický rozsah databázy:** približne 15 – 20 tisíc inštitucionálnych investorov (VC, PE, CVC, FO), k tomu 5 – 20 tisíc angel investorov s verejnou stopou.

**Obmedzenia odhadov:** čísla pochádzajú z rôznych rokov a definícií a čiastočne sa prekrývajú (VC aj PE). Ide o rádový odhad, nie o súpis.

**Očakávaná spoľahlivosť podľa poľa:**
- identita a aktivita: vysoká, lebo je doložená URL a dátumom,
- sektor a fáza: vysoká, lebo ich fondy samy deklarujú,
- ticket: stredná, často chýba alebo je zastaraný,
- AUM: stredná až nízka, lebo PE a FO ho často neuvádzajú.

**Vyplnenosť:**
- ticket očakávam pri 50 – 70 % VC,
- AUM pri 60 – 80 % VC (veľkosť fondu býva v tlačovej správe),
- pri FO a angel investoroch AUM takmer vôbec nebude.

## 5. Pilot (Slovensko, VC)

**Odhad veľkosti:** 15 – 30 aktívnych VC so sídlom na Slovensku a 20 – 40 zahraničných, ktoré investujú na Slovensku.

**Podklady:**
- 12 riadnych členov SLOVCA, z ktorých časť je PE a časť sídli v CZ alebo PL,
- Invest Europe: na Slovensko išlo v roku 2025 iba 7 mil. EUR VC.

**Postup:**
1. Zber kandidátov z SLOVCA, verejných programov a deal-first zdrojov.
2. Rešerš a `verify.py` na **všetkých** kandidátoch.
3. Ručná kontrola **100 %** zaradených aj vyradených slovenských záznamov. Vzorka je malá, preto nevzorkujem.
4. Výsledné metriky, zoznam chýb AI a ich príčin.

## 6. Odhad nákladov na celý svet

Dopočíta sa z nameraných hodnôt pilotu:
- tokeny a čas na jeden záznam,
- podiel záznamov, ktoré potrebujú ručný zásah,
- čas ručnej kontroly na jeden záznam.

Model nákladov:

`náklad = N_kandidátov × (LLM rešerš + vyhľadávacie API) + N_zaradených × podiel ručnej kontroly × čas × hodinová sadzba + údržba (opakovaná kontrola aktivity každých 6 – 12 mesiacov)`

Konkrétne čísla sú v `COSTS.md`.
