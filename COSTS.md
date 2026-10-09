# Odhad nákladov na rozšírenie na celý svet

Stav k 2026-10-09. Odhad vychádza z **nameraných** hodnôt pilotu (75 kandidátov, Slovensko), nie z odhadu od oka.

## 1. Namerané v pilote

Spotrebu tokenov som vytiahol z transkriptov subagentov v Claude Code. Odpovede sú deduplikované podľa ID správy, lebo jedna odpoveď sa v logu zapisuje do viacerých riadkov. Ceny sú cenníkové ceny Claude API pre `claude-opus-5-5` (stav 2026-10-06):

| Cena | Hodnota |
|---|---|
| Vstup | $4 / 1M tokenov |
| Výstup | $20 / 1M tokenov |
| Čítanie z cache | $0,20 / 1M tokenov |
| Zápis do cache (1 h) | $8 / 1M tokenov |
| Web search | $10 / 1 000 vyhľadávaní |

Pilot bežal v rámci predplatného Claude Code. Uvedené sumy sú teda **ekvivalent v cenách API**, nie skutočne zaplatená suma.

| Fáza | Agenti | Čas (wall clock) | Čítanie z cache | Zápis do cache | Výstup* | Vyhľadávania | Náklad |
|---|---|---|---|---|---|---|---|
| Rešerš 75 kandidátov | 5 paralelne | 6 – 20 min na agenta | 66,1 M | 1,03 M | 23 k | 142 | **≈ $23,3** |
| Predkontrola (AI) c001–c050 | 1 | 8 min | 4,7 M | 0,18 M | 2 k | 15 (+61 fetch) | **≈ $2,6** |
| `verify.py` (329 dôkazov, 260 URL) | – | < 1 min | – | – | – | – | $0 |

\* Výstupné tokeny v logu sú podhodnotené (pravdepodobne sa zapisujú pri začiatku streamu). Berte ich ako dolnú hranicu. Ani 10-násobok by však celkovú sumu nezmenil o viac ako $5.

**Jednotkové náklady:**
- rešerš: **≈ $0,31 na kandidáta**,
- predkontrola: **≈ $0,05 na kandidáta**,
- spolu **≈ $0,36 na kandidáta**.

Približne 95 % nákladov tvorí čítanie a zápis cache, teda opakované čítanie kontextu v cykle agenta. Výstup a vyhľadávanie sú zanedbateľné.

## 2. Koľko kandidátov treba spracovať

Podľa `PLAN.md` vychádza databáza na približne **15 – 20 tis. inštitucionálnych investorov** (VC, PE, CVC, FO) a **5 – 20 tis. angel investorov** s verejnou stopou.

V pilote prešlo zaradením **29 zo 75 kandidátov (39 %)**. Toto číslo je však skreslené: 31 kandidátov boli pridružení členovia SLOVCA, teda prevažne advokáti a audítori. Bez nich je výťažnosť 29 zo 44, teda **66 %**.

Pri celosvetovom zbere (asociácie, verejné programy, deal-first zdroje) rátam s výťažnosťou **40 – 60 %**. To znamená **50 – 90 tis. kandidátov**, z toho 30 – 40 tis. investorov.

## 3. Scenáre

### A. Naivné škálovanie súčasného postupu

Postup ostáva rovnaký: Opus 5.5, agent na každého kandidáta, AI predkontrola každého záznamu.

| Položka | Výpočet | Náklad |
|---|---|---|
| Rešerš | 50 – 90 tis. × $0,31 | $15 – 28 tis. |
| Predkontrola | 30 – 40 tis. zaradených × $0,05 × 1,5 (viac polí) | $2 – 3 tis. |
| **LLM spolu** | | **$17 – 31 tis.** |

### B. Optimalizovaný postup (odporúčaný)

1. **Deterministický predfilter.** Členov asociácií, ktorí sú advokáti, audítori či banky, vyradí pravidlo podľa kľúčových slov a registrov (NACE kód, typ licencie). V pilote by to odbremenilo 31 zo 75 kandidátov.
2. **Krátky kontext namiesto dlhého cyklu agenta.** Stiahnutie stránok rieši kód a model dostane iba text kandidátových stránok. Odhadom to dá 5 – 10× menej tokenov z cache.
3. **Model podľa úlohy.** Extrakciu robí Claude Sonnet 5.5 ($2 / $10) a predkontrolu iba vzorka plus položky, ktoré skript označí. Opus 5.5 ostáva len pre hraničné prípady.
4. **Batch API** (-50 %) pre všetko, čo nie je interaktívne.

| Položka | Náklad |
|---|---|
| LLM (extrakcia + cielená predkontrola) | **$3 – 6 tis.** |
| Vyhľadávanie (2 – 3 dotazy na kandidáta) | $1 – 3 tis. |

### Ľudská kontrola (v oboch scenároch)

V pilote kontrolujem 100 % záznamov. Pri celosvetovom rozsahu sa robí **stratifikovaná vzorka** podľa typu a regiónu: 5 typov × 6 regiónov × 60 záznamov, spolu **≈ 1 800 záznamov**. Pri precision okolo 95 % dáva vzorka 60 záznamov interval spoľahlivosti ±5,5 p. b. na jednu bunku a vzorka 1 800 záznamov ±1 p. b. celkovo.

K tomu treba ručne vyriešiť položky, ktoré AI predkontrola označila ako nesprávne. V pilote to bolo 8 zo 117 položiek, teda **≈ 7 %**.

| Položka | Výpočet | Hodiny | Náklad pri 25 €/h |
|---|---|---|---|
| Kontrola vzorky | 1 800 záznamov × ~4 položky × 0,5 min | ≈ 60 h | ≈ 1 500 € |
| Riešenie označených | 35 tis. × 4 položky × 7 % × 3 min | ≈ 490 h | ≈ 12 000 € |
| **Spolu** | | **≈ 550 h** | **≈ 13 – 14 tis. €** |

Ľudská práca je teda **najdrahšia položka**, nie LLM. Najväčšia úspora preto leží v lepšom zadaní pre AI. Najčastejšia chyba AI (AUM, ktoré nie je spravovaný kapitál) sa dá z veľkej časti odstrániť presnejšou definíciou v pokynoch pre agentov.

## 4. Údržba

- **Kontrola aktivity každých 6 mesiacov.** `verify.py` je iba HTTP, takže stojí takmer nič. Nové dealy sa sledujú cez deal-first zdroje (RSS, tlačové správy), čo je ≈ $0,02 – 0,05 na investora a rok, spolu **≈ $1 – 2 tis. ročne**.
- **Zastarané odkazy:** v pilote boli nedostupné 2 z 329 dôkazov (0,6 %). Rátam s 5 – 10 % ročne, ktoré treba obnoviť.

## 5. Zhrnutie

| | Jednorazovo | Ročne |
|---|---|---|
| LLM + vyhľadávanie (scenár B) | $4 – 9 tis. | $1 – 2 tis. |
| Ľudská kontrola | ≈ 13 – 14 tis. € | ≈ 3 – 5 tis. € |
| **Spolu** | **≈ 17 – 23 tis. €** | **≈ 4 – 7 tis. €** |

**Neistoty:**
- výťažnosť mimo Slovenska,
- podiel stránok blokovaných proti botom (v pilote 1 z 260 URL, v USA a UK bude vyšší),
- angel investori, ktorých verejná stopa je slabá: odhad 1 – 5 % aktívnych, viď `PLAN.md`.
