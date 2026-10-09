# Export konverzácií s Claude Code

Transkripty všetkých relácií, v ktorých vznikalo riešenie (2026-10-09), v chronologickom poradí. Vygenerované
z lokálnych transkriptov Claude Code (`~/.claude/projects/…/*.jsonl`) do Markdownu, obsahovo zodpovedajú `/export`.

| Súbor | Obsah |
|---|---|
| `01-zadanie-a-uvod.md` | Vloženie zadania |
| `02-plan-a-koncepty.md` | Koncepty riešenia (čisté LLM / scrapovanie / hybrid), výber hybridu |
| `03-plan-pokracovanie.md` | Dopracovanie plánu |
| `04-implementacia-a-reserse.md` | Pipeline, testy, rešerš 5 paralelnými agentmi, AI predkontrola c001–c050, náklady |
| `05-dokoncenie-a-rucna-kontrola.md` | AI predkontrola c051–c075, README, úpravy UI, ručná kontrola, nezhody človek vs. AI |
| `06-export-tejto-relacie.txt` | Doslovný výstup príkazu `/export` relácie 05 (vrátane opráv v2) |
| `agents/agent-aresearch-*.md` | Rešeršní agenti (pokyny: `prompts/research_agent.md`) |
| `agents/agent-areview-*.md`, `agents/agent-ab984fec*.md` | Kontrolní agenti (pokyny: `prompts/review_agent.md`) |

Úpravy oproti surovému transkriptu:

- dlhé výstupy nástrojov sú skrátené (označené „skrátené“),
- e-mailové adresy sú nahradené `[email]`,
- v súbore `06` je jeden blok (diff exportu so súkromnými údajmi) nahradený značkou „vynechané“ a názov iného
  projektu je nahradený výrazom „iný projekt“,
- výstupy so súkromnými poznámkami používateľa o iných projektoch (pamäť Claude Code, výpis domovského
  priečinka) sú vynechané a označené „vynechané“. Správy používateľa ani odpovede Claude sa nevynechávali.
