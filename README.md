# Tax Junior Partner AI

> Un assistente fiscale personale intelligente, veloce, documentato e sempre supervisionato dal professionista.

## 📋 Vision

Tax Junior Partner AI è un assistente fiscale progettato per supportare il lavoro di un commercialista senior, **non per sostituirlo**, ma per comportarsi come un junior partner estremamente preparato.

**Target User:** Commercialista italiano specializzato in:
- SRL
- Holding
- PEX
- Operazioni straordinarie
- SPV
- Fiscalità internazionale
- Interpelli Agenzia Entrate

## 🚀 Features (v0.1 MVP)

### 1. **Tax News Agent**
Recupera e classifica giornalmente:
- Interpelli Agenzia Entrate
- Circolari e risoluzioni
- Sentenze tributarie
- Novità fiscali e commenti
- Genera morning briefing personalizzato

### 2. **Knowledge Base Locale**
- Interpelli
- Circolari e risoluzioni
- Sentenze tributarie
- Documenti interni dello studio
- Indicizzazione vettoriale semantica

### 3. **Semantic Search**
Consenti ricerche naturali come:
- "novità PEX"
- "holding che rifattura costi"
- "operazioni straordinarie"

Risultati con:
- Risposta ragionata
- Fonti citate
- Documenti rilevanti
- Grado di confidenza

### 4. **Risk Analysis**
Per ogni quesito genera:
- Tesi favorevole
- Tesi contraria
- Punti di rischio
- Documenti mancanti
- Checklist di compliance

## 🏗️ Architecture

```
tax-junior-partner-ai/
├── src/
│   ├── core/                      # Business logic centrale
│   │   ├── __init__.py
│   │   ├── tax_agent.py          # Orchestratore principale
│   │   ├── news_aggregator.py    # Aggregazione notizie fiscali
│   │   └── risk_analyzer.py      # Analisi rischi e tesi
│   │
│   ├── data/                      # Gestione dati e KB
│   │   ├── __init__.py
│   │   ├── vector_store.py       # Interfaccia vector database
│   │   ├── knowledge_base.py     # Gestione KB locale
│   │   └── models/               # Modelli di dati
│   │       └── __init__.py
│   │
│   ├── services/                  # Integrazioni esterne
│   │   ├── __init__.py
│   │   ├── news_scraper.py       # Scraping Agenzia Entrate
│   │   ├── llm_provider.py       # Interfaccia LLM
│   │   └── embeddings.py         # Generazione embeddings
│   │
│   ├── utils/                     # Utilities
│   │   ├── __init__.py
│   │   ├── config.py             # Configurazione centralizzata
│   │   ├── logger.py             # Logging
│   │   └── validators.py         # Validatori
│   │
│   └── __init__.py
│
├── docs/
│   ├── architecture.md           # Architettura tecnica dettagliata
│   ├── mvp_roadmap.md           # Piano MVP
│   ├── api.md                    # API specification
│   └── deployment.md             # Guide deploy
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── config/
│   ├── __init__.py
│   ├── settings.py               # Configurazione app
│   ├── logging.conf              # Logging config
│   └── prompts/                  # Template prompts LLM
│       └── __init__.py
│
├── .env.example                  # Template variabili ambiente
├── .gitignore
├── requirements.txt              # Dipendenze Python
├── setup.py                      # Package setup
├── main.py                       # Entry point
└── VISION.md                     # Vision document
```

## 📦 Tech Stack

- **Language:** Python 3.11+
- **Vector DB:** Chroma / Weaviate (local-first)
- **LLM API:** OpenAI / Anthropic (via API)
- **Web Scraping:** BeautifulSoup4, Requests, Selenium (se needed)
- **Data Processing:** Pandas, NumPy
- **Embeddings:** OpenAI Embeddings / HuggingFace
- **Async:** AsyncIO, HTTPX
- **Testing:** Pytest, Pytest-asyncio
- **Code Quality:** Ruff, Black, MyPy

## 🚦 Quick Start

```bash
# Clone repository
git clone https://github.com/simomo88/tax-junior-partner-ai.git
cd tax-junior-partner-ai

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys and settings

# Run
python main.py
```

## 📚 Documentation

- **[Architecture](docs/architecture.md)** - Design tecnico e componenti
- **[MVP Roadmap](docs/mvp_roadmap.md)** - Piano per prime 1-2 weekend
- **[API Reference](docs/api.md)** - Specifiche API interne
- **[Deployment](docs/deployment.md)** - Guide per deploy

## 🎯 MVP Timeline (1-2 weekends)

**Weekend 1:**
- Setup repository e struttura base
- Configurazione logging e config management
- Interfaccia LLM provider (test con mock)
- Basic vector store interface
- Schema modelli dati

**Weekend 2:**
- Implementazione primo news scraper (Agenzia Entrate)
- Knowledge base CRUD operations
- Semantic search basic (mock embeddings)
- Risk analyzer core logic
- Integration test end-to-end

**Post-MVP:**
- Production embeddings
- Real vector database
- Multi-source scraping
- Morning briefing generation
- Web UI / API server

## 🔄 Development Workflow

```bash
# Create feature branch
git checkout -b feat/your-feature

# Make changes and test
pytest tests/

# Format and lint
black src/ tests/
ruff check src/ tests/

# Commit and push
git commit -m "feat: description"
git push origin feat/your-feature

# Open PR
```

## 📝 Code Standards

- **Style:** Black + Ruff
- **Type Hints:** MyPy strict mode
- **Docstrings:** Google style
- **Testing:** >80% coverage target
- **Commits:** Conventional commits

## ⚖️ License

Private project.

---

**Philosophy:** Un praticante molto intelligente, molto veloce, molto documentato, ma che deve sempre essere supervisionato dal professionista.
