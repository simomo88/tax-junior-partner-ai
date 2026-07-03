# Tax Junior Partner AI

## Vision

Tax Junior Partner AI è un assistente fiscale personale progettato per supportare il lavoro di un commercialista senior.

L'obiettivo NON è sostituire il professionista, ma comportarsi come un junior partner estremamente preparato, veloce e sempre disponibile.

---

## Utente

- Commercialista italiano
- Focus su:
  - SRL
  - holding
  - PEX
  - operazioni straordinarie
  - SPV
  - fiscalità internazionale
  - interpelli
  - Agenzia Entrate

---

## Funzionalità v0.1

### 1. Tax News Agent

Ogni giorno deve:

- recuperare nuovi interpelli Agenzia Entrate;
- recuperare nuove circolari;
- recuperare nuove risoluzioni;
- recuperare nuove sentenze tributarie;
- recuperare le principali novità fiscali e commenti della giornata
- classificare gli argomenti;
- produrre un morning briefing.

---

### 2. Knowledge Base

Deve costruire una base di conoscenza locale contenente:

- interpelli;
- circolari;
- risoluzioni;
- sentenze;
- documenti interni dello studio.

---

### 3. Semantic Search

L'utente deve poter chiedere:

- "novità PEX"
- "holding che rifattura costi"
- "operazioni straordinarie"

e ottenere:

- risposta ragionata;
- fonti;
- documenti rilevanti;
- grado di confidenza.

---

### 4. Risk Analysis

Per ogni quesito deve produrre:

- tesi favorevole;
- tesi contraria;
- punti di rischio;
- documenti mancanti;
- checklist.

---

## Architettura desiderata

- Python
- GitHub
- database vettoriale locale
- LLM tramite API
- struttura modulare
- repository facilmente manutenibile

---

## Filosofia

Tax Junior Partner AI deve comportarsi come:

> un praticante molto intelligente,
> molto veloce,
> molto documentato,
> ma che deve sempre essere supervisionato
> dal professionista.
