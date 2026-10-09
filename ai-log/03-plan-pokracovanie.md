# 03 Plán: pokračovanie

Zdroj: transkript Claude Code `3eee6771-8363-4c8a-b492-ab597a507ea3.jsonl`

## Používateľ · 2026-10-09 11:25:54 UTC

Pracovať môžete v Claude Code alebo v podobnom nástroji. Ak nestihnete všetko, uprednostnite podstatné časti a uveďte, čo v riešení chýba. V README prosím popíšte, ako ste s AI pracovali (aké pokyny dostali agenti, ako ste kontrolovali ich výstup a kde sa pomýlili). Ak Vám v zadaní niečo nebude jasné, rozhodnite podľa seba a v README zdôvodnite, prečo ste sa tak rozhodli. S otázkami sa na mňa môžete kedykoľvek obrátiť aj odpoveďou na tento e-mail.

<pasted_content id="7cfb">
ZADANIE B: Konverzná landing page

Cieľom je landing page s porovnaním ETF obchodovaných na NYSE pre českého drobného investora, ktorý prichádza z reklamy na mobile a stránke venuje len niekoľko sekúnd. Stránka má fungovať ako lead magnet: ponúknuť návštevníkovi hodnotu a výmenou za ňu získať jeho kontakt. Pekný dizajn nestačí, stránka musí byť optimalizovaná na prínos kontaktov. Zároveň nesmie pôsobiť ako základný výstup od Claude. Dizajn aj texty majú byť premyslené pre túto cieľovú skupinu. Pri hodnotení sa budem riadiť hlavne otázkou, či by sme na ňu mohli zajtra spustiť reklamu.

Určte cieľovú skupinu, čo návštevník dostane výmenou za kontakt a v ktorom momente oň požiadate. Hodnota by mala byť zrejmá ešte pred vyplnením formulára. Navrhnite aj dve verzie reklamy. Prvá obrazovka stránky by mala nadväzovať na prísľub reklamy a okamžite komunikovať, čo návštevník získa.

Výber interaktívnych prvkov, napríklad porovnania fondov, kalkulačky poplatkov alebo skladania portfólia, nechávam na Vás. Každý z nich by mal viesť ku kontaktu. Formulár by mal mať čo najmenej polí. Premyslite aj to, čo návštevník dostane po jeho odoslaní.

Použite skutočné dáta s uvedením zdroja a merajte celú cestu od príchodu po odoslanie formulára. V README zdôvodnite poradie sekcií, uveďte očakávanú konverziu a tri hypotézy na A/B test zoradené podľa očakávaného dopadu. Stránku nasaďte na bezplatný hosting, napríklad Vercel.
</pasted_content id="7cfb">

**Nástroj `Bash`**

[vynechané: súkromné poznámky alebo súbory mimo projektu]

[vynechané: súkromné poznámky alebo súbory mimo projektu]

**Nástroj `AskUserQuestion`**

```json
{"questions": [{"question": "Ktorý hlavný interaktívny koncept (lead magnet) zvolíme?", "header": "Koncept", "multiSelect": false, "options": [{"label": "Kalkulačka + UCITS dvojča (Recommended)", "description": "Vyberieš NYSE ETF (VOO/SPY/QQQ/VTI/SCHD…) + mesačnú sumu → hneď vidíš TER, výnos, rozdiel v Kč za 20 rokov a UCITS alternatívu kúpiteľnú v ČR. Plus: hodnota okamžite viditeľná, 1 interakcia, silný háčik. Mínus: trochu viac textu o regulácii."}, {"label": "Čisté porovnanie fondov", "description": "Tabuľka/karty NYSE ETF s filtrom (poplatok, výnos, dividenda), plná verzia za e-mail. Plus: najjednoduchšie, priamo podľa zadania. Mínus: slabšia hodnota, na mobile tabuľky nefungujú, typický 'gated content'."}, {"label": "Kvíz → portfólio", "description": "3 otázky (horizont, riziko, suma) → navrhnuté portfólio z ETF, detail za e-mail. Plus: vysoká angažovanosť, osobný výsledok. Mínus: hraničí s investičným poradenstvom (regulačné riziko pre firmu), pomalšie na pár sekúnd pozornosti."}]}, {"question": "Kam ukladať leady a čo pošleme po odoslaní?", "header": "Leady", "multiSelect": false, "options": [{"label": "Resend + Vercel funkcia (Recommended)", "description": "Serverless endp
… [skrátené, 2646 znakov]
```

<details><summary>Výstup nástroja</summary>

```
Your questions have been answered: "Ktorý hlavný interaktívny koncept (lead magnet) zvolíme?"="Kalkulačka + UCITS dvojča (Recommended)", "Kam ukladať leady a čo pošleme po odoslaní?"="Resend + Vercel funkcia (Recommended)", "Čím merať celý funnel (príchod → odoslanie)?"="PostHog (Recommended)", "V akom jazyku má byť README (stránka bude po česky)?"="Slovensky". You can now continue with these answers in mind.
```

</details>

## Claude · 2026-10-09 11:27:24 UTC

Zvolené: kalkulačka s UCITS dvojčatami, Resend + Vercel, PostHog, README po slovensky. Teraz zbieram skutočné dáta o fondoch.

**Nástroj `ToolSearch`**

```json
{"query": "select:WebFetch,WebSearch", "max_results": 2}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/voo/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/spy/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/qqq/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/vti/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/schd/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/vt/", "prompt": "Extract exactly: expense ratio, assets under management (AUM), dividend yield, inception date, exchange, price, and any total return figures (1Y, 5Y, 10Y annualized/CAGR) shown. Also the data date if shown."}
```

<details><summary>Výstup nástroja</summary>

```
- **Expense ratio:** 0.06%
- **AUM:** $83.26B
- **Dividend yield:** 1.52% (trailing twelve months)
- **Inception date:** June 24, 2008
- **Exchange:** NYSE Arca (ticker NYSEARCA: VT)
- **Price:** $158.73 at close, October 8, 2026 (4:00 PM EDT). Pre-market was $159.30 on October 9, 2026.
- **Total returns:**
  - 1-year: 16.33%, including dividends
  - Since inception: 8.79% average annual return
  - 5-year and 10-year figures are not shown.
- **Data date:** Price data is as of October 8, 2026 close. The page was last checked October 9, 2026.
```

</details>

<details><summary>Výstup nástroja</summary>

```
- **Expense ratio:** 0.03%
- **AUM:** $696.15B
- **Dividend yield:** 1.04% (dividend TTM: $3.95)
- **Inception date:** May 24, 2001
- **Exchange:** NYSE Arca (ticker NYSEARCA: VTI)
- **Price:** 379.56 USD at close, Oct 8, 2026, 4:00 PM EDT (-1.47, -0.39%)
- **Total return:**
  - 1Y: 16.47%. The page says, "VTI had a total return of 16.47% in the past year, including dividends."
  - Since inception: 9.65% average annual return. The page doesn't label this as CAGR.
  - 5Y and 10Y figures: not shown.
- **Data date:** Price as of Oct 8, 2026 close. The page was last checked Oct 9, 2026.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**SPY (State Street SPDR S&P 500 ETF) from the page:**

- **Expense ratio:** 0.09%
- **AUM:** $815.33B
- **Dividend yield:** 0.98% (TTM dividend $7.58)
- **Inception date:** Jan 22, 1993
- **Exchange:** NYSE Arca (ticker shown as NYSEARCA: SPY)
- **Price:** $773.93, down $3.29 (-0.42%) at close on Oct 8, 2026, 4:00 PM EDT
  - Pre-market: $776.99 (+0.40%) on Oct 9, 2026, 7:21 AM EDT
- **Total return:**
  - 1Y: 16.91%, including dividends
  - Since inception: 10.85% average annual return
  - 5Y and 10Y figures are not shown.
- **Data date:** Last checked Oct 9, 2026. The price data is from the Oct 8, 2026 close.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**QQQ (Invesco QQQ Trust Series I): Extracted Data**

- **Expense ratio:** 0.18%
- **Assets under management:** $505.19B (listed as "Assets")
- **Dividend yield:** 0.41%
- **Inception date:** Mar 10, 1999
- **Exchange:** NASDAQ
- **Price:** $747.58 at close (-$10.15, -1.34%)
- **Total return:**
  - 1-year: 24.25% total return, including dividends
  - Since inception: 10.91% average annual return
  - 5-year and 10-year figures are not shown.
- **Data dates:** Price is as of the Oct 8, 2026 close (4:00 PM EDT). The page was last checked Oct 9, 2026. A pre-market price of $753.67 is listed for Oct 9, 2026, 7:26 AM EDT.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**VOO (Vanguard S&P 500 ETF) data from the page:**

- **Expense ratio:** 0.03%
- **AUM:** $1.05T (listed as "Assets")
- **Dividend yield:** 1.04% (dividend ttm $7.43)
- **Inception date:** September 7, 2010
- **Exchange:** NYSE Arca (ticker shown as NYSEARCA: VOO)
- **Price:** $711.28, down $3.06 (-0.43%) at close on October 8, 2026, 4:00 PM EDT. The page also shows a pre-market price of $714.30 on October 9, 2026, 7:26 AM EDT.
- **Total return:** 16.95% over the past year, including dividends. Since inception, the average annual return is 14.87%. The page shows no 5Y or 10Y annualized/CAGR figures.
- **Data date:** Last checked October 9, 2026. Closing price is as of October 8, 2026.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**SCHD (Schwab U.S. Dividend Equity ETF)**

- **Expense ratio:** 0.06%
- **Assets under management:** $108.67B
- **Dividend yield:** 3.18%
- **Inception date:** Oct 20, 2011
- **Exchange:** NYSE Arca (ticker NYSEARCA: SCHD)
- **Price:** $33.15, up $0.50 (+1.53%) at close on Oct 8, 2026, 4:00 PM EDT. Pre-market on Oct 9, 2026 was $33.11.
- **Total return figures:**
  - 1-year: 25.78%, including dividends
  - Since inception: 13.20% average annual return
  - 5-year and 10-year figures are not shown on the page.
- **Data date:** Last checked Oct 9, 2026. The closing price is as of Oct 8, 2026.
```

</details>

## Claude · 2026-10-09 11:27:56 UTC

QQQ sa obchoduje na Nasdaqu, nie na NYSE, takže ho vyraďujem a nahrádzam IVV (NYSE Arca). Teraz overím UCITS dvojčatá na justETF.

**Nástroj `WebFetch`**

```json
{"url": "https://stockanalysis.com/etf/ivv/", "prompt": "Extract exactly: expense ratio, AUM, dividend yield, inception date, exchange, price, 1Y total return, since-inception average annual return, data date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=IE00BFMXXD54", "prompt": "Extract: fund name, ISIN, ticker(s), TER, fund size, distribution policy (acc/dist), replication, fund domicile, inception date, and which exchanges/tickers (esp. Xetra, LSE, Prague if any). Data date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=IE00B5BMR087", "prompt": "Extract: fund name, ISIN, ticker(s), TER, fund size, distribution policy (acc/dist), fund domicile, inception date, exchanges/tickers. Data date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=IE00BK5BQT80", "prompt": "Extract: fund name, ISIN, ticker(s), TER, fund size, distribution policy (acc/dist), fund domicile, inception date, exchanges/tickers. Data date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=IE000XZSV718", "prompt": "Extract: fund name, ISIN, ticker(s), TER, fund size, distribution policy (acc/dist), fund domicile, inception date, exchanges/tickers. Data date."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=IE00BJ0KDR00", "prompt": "Extract: fund name, ISIN, ticker(s), TER, fund size, distribution policy (acc/dist), fund domicile, inception date, exchanges/tickers. Data date."}
```

<details><summary>Výstup nástroja</summary>

```
| Field | Value |
|---|---|
| Expense ratio | 0.03% |
| AUM (Assets) | $888.29B |
| Dividend yield | 1.08% |
| Inception date | May 15, 2000 |
| Exchange | NYSE Arca (ticker NYSEARCA: IVV) |
| Price | $777.27 (-3.31, -0.42%), at close Oct 8, 2026 |
| 1-year total return | 16.96% (including dividends) |
| Since-inception average annual return | 8.55% |
| Data date | Oct 9, 2026 (last checked) |
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Vanguard S&P 500 UCITS ETF (USD) Accumulating**

- **ISIN:** IE00BFMXXD54
- **WKN:** A2PFN2
- **Primary ticker:** VUAA
- **TER:** 0.07% p.a.
- **Fund size:** EUR 33,371 m
- **Distribution policy:** Accumulating (acc)
- **Replication:** Physical, full replication
- **Fund domicile:** Ireland
- **Inception date:** 14 May 2019
- **Index:** S&P 500®
- **Fund currency:** USD (currency unhedged)

**Listings and tickers**

| Exchange | Trade currency | Ticker |
|---|---|---|
| Xetra | EUR | VUAA (Reuters: VUA1.DE) |
| gettex | EUR | VUAA |
| Borsa Italiana | EUR | VUAA |
| Frankfurt Stock Exchange | EUR | no ticker listed |
| London Stock Exchange | USD | VUAA |
| London Stock Exchange | GBP | VUAG |
| Bolsa Mexicana de Valores | MXN | VUAAN |
| Bolsa Mexicana de Valores | USD | no ticker listed |

Prague is not listed on this page.

**Data date:** The page does not give one overall date. Holdings are as of 31/08/2026, savings plan and order fee data as of 10/2026, and the factsheet filename is dated 2026-07-31. Performance and risk figures are undated.
```

</details>

<details><summary>Výstup nástroja</summary>

```
| Field | Value |
|---|---|
| Fund name | Xtrackers MSCI USA UCITS ETF 1C |
| ISIN | IE00BJ0KDR00 |
| WKN | A1XB5V |
| Primary ticker | XD9U |
| TER | 0.03% p.a. |
| Fund size | EUR 12,329 m |
| Distribution policy | Accumulating (acc) |
| Fund domicile | Ireland |
| Inception date | 9 May 2014 |

**Listings (exchange: trade currency, ticker):**
- gettex: EUR, XD9U
- Stuttgart Stock Exchange: EUR, XD9U
- Borsa Italiana: EUR, XD9U
- London Stock Exchange: GBX, XDUS
- London Stock Exchange: USD, XD9U
- SIX Swiss Exchange: CHF, XD9U
- SIX Swiss Exchange: USD, XD9U
- XETRA: EUR, XD9U

**Data date:** The page has no single date. Holdings are as of 31/08/2026, broker and savings plan data are as of October 2026, and the fund size and returns are undated.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**State Street SPDR S&P 500 UCITS ETF USD Unhedged (Acc)**

- **ISIN:** IE000XZSV718
- **WKN:** A3EUC1
- **Primary ticker:** SPYL
- **TER:** 0.03% p.a.
- **Fund size:** EUR 17,596 m
- **Distribution policy:** Accumulating (Acc)
- **Fund domicile:** Ireland
- **Inception date:** 31 October 2023
- **Fund currency:** USD (currency unhedged)
- **Replication:** Physical (full replication)

**Listings and tickers**

| Exchange | Trade currency | Ticker |
|---|---|---|
| gettex | EUR | SPYL |
| Borsa Italiana | EUR | SP5A |
| Euronext Amsterdam | EUR | SPYL |
| London Stock Exchange | USD | SPYL |
| London Stock Exchange | GBP | SPXL |
| SIX Swiss Exchange | USD | SPYL |
| XETRA | EUR | SPYL |
| Bolsa Mexicana de Valores | MXN / USD | listed, ticker not shown ("-") |

**Data dates**

- Holdings: as of 31/08/2026
- Factsheet: dated 2026-08-31
- Savings plan and order fee data: as of 10/2026
- The page does not give a single overall data date. Performance and fund size figures are not dated.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**iShares Core S&P 500 UCITS ETF USD (Acc)**

- **ISIN:** IE00B5BMR087
- **WKN:** A0YEDG
- **Primary ticker:** SXR8
- **TER:** 0.07% p.a.
- **Fund size:** EUR 141,385 m
- **Distribution policy:** Accumulating (no distributions)
- **Fund domicile:** Ireland
- **Inception date:** 19 May 2010

**Listings (exchange: trade currency, ticker)**
- gettex: EUR, SXR8
- Stuttgart: EUR, SXR8
- XETRA: EUR, SXR8
- Borsa Italiana: EUR, CSSPX
- Euronext Amsterdam: EUR, CSPX
- London Stock Exchange: USD, CSPX; GBX, CSP1
- SIX Swiss Exchange: USD, CSSPX
- Bolsa Mexicana de Valores: MXN, CSPX MM

**Data date:** The page does not give one date for the whole profile. Holdings are as of 31/08/2026, and the broker and savings plan data is as of 10/2026. The factsheet is dated 2026-09-30. The TER, fund size, and listing details have no stated date.
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Vanguard FTSE All-World UCITS ETF (USD) Accumulating**

- **ISIN:** IE00BK5BQT80
- **WKN:** A2PKXG
- **Primary ticker:** VWCE
- **TER:** 0.14% p.a.
- **Fund size:** EUR 55,102 m
- **Distribution policy:** Accumulating
- **Fund domicile:** Ireland
- **Inception date:** 23 July 2019
- **Fund currency:** USD

**Listings**

| Exchange | Trade currency | Ticker |
|---|---|---|
| gettex | EUR | VWCE |
| Stuttgart | EUR | VWCE |
| Borsa Italiana | EUR | VWCE |
| Frankfurt | EUR | - |
| Euronext Amsterdam | EUR | VWCE |
| London Stock Exchange | USD | VWRA |
| London Stock Exchange | GBP | VWRP |
| SIX Swiss Exchange | CHF | VWRA |
| XETRA | EUR | VWCE |

**Data date:** The page has no single date for all fields. Holdings are as of 31/08/2026, the factsheet is dated 31/07/2026, and the broker and fee data is as of 10/2026.
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "justETF dividend UCITS ETF similar SCHD Dow Jones US Dividend 100 UCITS TER", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "PRIIPs KID americké ETF nelze koupit český investor VOO XTB Trading 212", "mode": "standard"}
```

**Nástroj `WebSearch`**

```json
{"query": "časový test cenné papíry 3 roky osvobození limit 100 000 Kč 40 milionů 2025 zákon o daních z příjmů", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "justETF dividend UCITS ETF similar SCHD Dow Jones US Dividend 100 UCITS TER"

Links: [{"title":"Top STOXX Global Select Dividend 100 ETFs","url":"https://justetf.com/en/how-to/stoxx-global-select-dividend-100-etfs.html"},{"title":"www.etfstream.com","url":"https://www.etfstream.com/de/etf-screener/DJDVPEX"},{"title":"Top STOXX Global Select Dividend 100 ETFs","url":"https://www.justetf.com/uk/how-to/stoxx-global-select-dividend-100-etfs.html"},{"title":"ishares dow jones u s select dividend ucits etf de dis usd","url":"https://www.analizy.pl/etf/DE000A0D8Q49/ishares-dow-jones-u-s-select-dividend-ucits-etf-de-dis-usd"},{"title":"iShares Dow Jones U.S. Select Dividend UCITS ETF (DE)","url":"https://extraetf.com/es/etf-profile/DE000A0D8Q49"},{"title":"etfstream.com","url":"https://etfstream.com/etf-screener/DJDVPEX"},{"title":"top 50 equity etfs with the highest dividend yield in eur","url":"https://justetf.com/en/market-overview/top-50-equity-etfs-with-the-highest-dividend-yield-in-eur.html"},{"title":"iShares Dow Jones U.S. Select Dividend UCITS ETF (DE)","url":"https://extraetf.com/ch/etf-profile/DE000A0D8Q49"},{"title":"Performance in Euro","url":"https://www.brokerexperte.de/etf/de000a0d8q49/"}]

I didn't find a UCITS ETF that tracks the Dow Jones U.S. Dividend 100 index (SCHD's index) on justETF. The closest match in the results is an iShares fund, which tracks a related but different index.

**Closest UCITS match: iShares Dow Jones U.S. Sele
… [skrátené, 3378 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "časový test cenné papíry 3 roky osvobození limit 100 000 Kč 40 milionů 2025 zákon o daních z příjmů"

Links: [{"title":"zmena u investic","url":"https://www.crowe.com/cz/cs-cz/news/zmena-v-limitech-pro-osvobozeni-u-investic"},{"title":"Problematika cenných papírů u fyzických osob","url":"https://www.dauc.cz/clanky/10579/problematika-cennych-papiru-u-fyzickych-osob"},{"title":"casovy test osvobozen","url":"https://rulecalc.com/de/steuern/casovy-test-osvobozen"},{"title":"casovy test osvobozen","url":"https://rulecalc.com/cs/dan/casovy-test-osvobozen"},{"title":"dan z prodeje cp","url":"https://rulecalc.com/de/dan/dan-z-prodeje-cp"},{"title":"dan z prodeje cp","url":"https://rulecalc.com/cs/dan/dan-z-prodeje-cp"},{"title":"neosvobozeni prijmu fyzickych osob z prodeju cennych papiru a podilu v obchodnich korporacich 118792","url":"https://www.epravo.cz/top/clanky/neosvobozeni-prijmu-fyzickych-osob-z-prodeju-cennych-papiru-a-podilu-v-obchodnich-korporacich-118792.html"},{"title":"Prodej cenných papírů v roce 2023 a daň z příjmu","url":"https://www.finance.cz/clanky/549833-dan-z-prijmu-prodej-cennych-papiru/"},{"title":"vycházející slunce na poli","url":"https://www.ey.com/cs_cz/insights/tax/danove-a-pravni-zpravy-listopad-2024"}]

Podle dostupných zdrojů platí pro cenné papíry v roce 2025 tato pravidla:

**1. Časový test (3 roky):** Příjem z prodeje cenných papírů bývá osvobozen, pokud od nabytí uplynuly alespoň tři roky (§ 4 odst. 1 písm. w) ZDP). 
… [skrátené, 4456 znakov]
```

</details>

<details><summary>Výstup nástroja</summary>

```
Web search results for query: "PRIIPs KID americké ETF nelze koupit český investor VOO XTB Trading 212"

Links: [{"title":"application priips regulation what happens us packaged products subscribed regulation came force","url":"https://www.amf-france.org/en/amf-ombudsman/ombudsman-online-diary/latest/application-priips-regulation-what-happens-us-packaged-products-subscribed-regulation-came-force"},{"title":"ETF Insight: European investors set to be impacted by KID requirements","url":"https://www.etfstream.com/articles/etf-insight-european-investors-set-to-be-impacted-by-kid-requirements"},{"title":"starting 1 january 2023 retail investors can no longer purchase investment fund units and etfs if","url":"https://seb.ee/en/starting-1-january-2023-retail-investors-can-no-longer-purchase-investment-fund-units-and-etfs-if"},{"title":"hargreaves lansdown removes trusts for failing to produce kids information","url":"https://www.investmentweek.co.uk/investment-week/news/3023610/hargreaves-lansdown-removes-trusts-for-failing-to-produce-kids-information"},{"title":"Application of the PRIIPs Regulation what happens to US packaged products subscribed before the regulation came into force","url":"https://www.amf-france.org/sites/institutionnel/files/pdf/70135/en/Application_of_the_PRIIPs_Regulation_what_happens_to_US_packaged_products_subscribed_before_the_regulation_came_into_force_.pdf?1713518203"},{"title":"US-domiciled ETFs: why they are no longer available from many online brokers",
… [skrátené, 5960 znakov]
```

</details>

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/etf-profile.html?isin=DE000A0D8Q49", "prompt": "Extract: fund name, ISIN, ticker, TER, fund size, distribution policy, domicile, inception, index, listings/tickers."}
```

**Nástroj `WebFetch`**

```json
{"url": "https://www.justetf.com/en/news/etf/us-domiciled-etfs.html", "prompt": "Summarize the key claims about why US-domiciled ETFs are not available to EU retail investors (PRIIPs/KID), including any exceptions (professional clients, options), and the article's publication/update date. Quote 1-2 key sentences verbatim."}
```

**Nástroj `Bash`**

```bash
curl -s "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt" | head -2; curl -s "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt" | grep -E "USD|EUR"
```

<details><summary>Výstup nástroja</summary>

```
**iShares Dow Jones US Select Dividend UCITS ETF (DE)**

- **Fund name:** iShares Dow Jones US Select Dividend UCITS ETF (DE)
- **ISIN:** DE000A0D8Q49
- **WKN:** A0D8Q4
- **Ticker:** EXX5
- **TER:** 0.31% p.a.
- **Fund size:** EUR 398 m
- **Distribution policy:** Distributing (at least annually)
- **Domicile:** Germany
- **Inception:** 28 September 2005
- **Index:** Dow Jones US Select Dividend

**Listings (all in EUR):**

| Exchange | Ticker | Bloomberg | Reuters |
|---|---|---|---|
| gettex | EXX5 | – | – |
| Stuttgart Stock Exchange | EXX5 | – | – |
| Borsa Italiana | EXX5 | DJDVPEX IM | DJDVPEX.MI |
| XETRA | EXX5 | DJDVPEX GY | DJDVPEX.DE |
```

</details>

<details><summary>Výstup nástroja</summary>

```
**Key claims:**

- **Cause:** The article attributes the restriction to PRIIPs, EU rules requiring a Key Information Document (KID). EU-domiciled UCITS ETFs had compliant KIDs when the rules took effect in early 2018. US-domiciled ETFs did not, and the author argues their providers had little incentive to produce EU-compliant documents because they mainly serve the US market.
- **Effect:** Existing holders can keep or sell. New purchases are blocked until a PRIIPs-compliant KID exists. As the article puts it: "you won't be able to buy more until a PRIIPs compatible KID becomes available."
- **Sophisticated investor exception:** Some platforms may let professional or highly qualified investors buy these funds, if the broker accepts them under the UK definition of a sophisticated investor. The article mentions a possible £500,000+ portfolio requirement and notes that many popular brokers don't offer this route.
- **Other possible routes:** Some EU-based brokers may apply a looser national interpretation of PRIIPs. Some US funds with large European institutional investor bases might produce compliant KIDs, though sophisticated investors are not subject to PRIIPs anyway.
- **Options:** The article does not discuss options.

**Publication date:** 28 March 2018, by Dominique Riedl. The page shows no update date. The "2011-2026" in the footer is a site-wide copyright notice, not an article date.
```

</details>

<details><summary>Výstup nástroja</summary>

```
08.10.2026 #194
země|měna|množství|kód|kurz
EMU|euro|1|EUR|24,400
USA|dolar|1|USD|21,811
```

</details>

**Nástroj `WebSearch`**

```json
{"query": "průměrná nákladovost TER akciových podílových fondů banky Česko 2025 analýza poplatky vs ETF", "mode": "standard"}
```

<details><summary>Výstup nástroja</summary>

```
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

</details>

## Claude · 2026-10-09 11:29:14 UTC

Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
