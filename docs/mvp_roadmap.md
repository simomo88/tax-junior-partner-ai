# MVP Roadmap: Tax Junior Partner AI - 1-2 Weekends Implementation

## Obiettivo MVP

Un sistema minimale funzionante che dimostra:
1. Aggregazione notizie fiscali da 4 fonti
2. Knowledge base con semantic search (Chroma + embeddings mock)
3. Tax reasoning che genera tesi pro/contro + risk scoring
4. Studio Memory base (clients & cases)
5. CLI interface per testing
6. Simplified stack: NO Weaviate, NO Selenium

---

## MVP Scope Changes

### ✅ KEEP
- Chroma (embedded vector store)
- Requests (HTTP client)
- BeautifulSoup4 (HTML parsing)
- Async processing

### ❌ REMOVE from MVP
- Weaviate (use Chroma locally instead)
- Selenium (use BeautifulSoup only, static sites)

### ✨ NEW in MVP
- Retrieval Layer (chunker, semantic_search, reranker structure)
- Tax Reasoning modules (favorable_position, contrary_position, risk_score, checklist_generator)
- Studio Memory (basic clients.py, cases.py)
- Client Impact Analysis (mapper + analyzer)
- 4 specialized scrapers (agenzia_entrate, cassazione, normattiva, sole24ore)

---

## Timeline Dettagliato

### 🎯 Weekend 1: Foundation & Setup

#### Venerdì 2h
- ✅ Repository setup completato
- ✅ Folder structure creata (with new modules)
- ✅ Git workflows e contributing guidelines
- ✅ CI/CD baseline (GitHub Actions stubs)

#### Sabato Mattina 3h
- ✅ Setup Python environment e requirements
- ✅ Configuration system (pydantic + env variables)
- ✅ Logging infrastructure
- ✅ Base error handling e custom exceptions
- **Output:** `src/utils/config.py`, `src/utils/logger.py`, `config/settings.py`

#### Sabato Pomeriggio 4h
- ✅ LLM Provider interface (abstract base)
- ✅ OpenAI provider implementation
- ✅ Mock provider per testing
- ✅ Token counting utility
- **Output:** `src/services/llm_provider.py` + tests
- **Testing:** Unit tests per LLM calls

#### Domenica Mattina 4h
- ✅ Vector Store interface (abstract base)
- ✅ Chroma provider implementation
- ✅ CRUD operations (create, read, update, search)
- ✅ Metadata filtering
- **Output:** `src/data/vector_store.py` + tests
- **Testing:** Integration tests con Chroma

#### Domenica Pomeriggio 3h
- ✅ Data models (TaxDocument, SearchResult, RiskAnalysis, ClientImpact)
- ✅ Pydantic validators
- ✅ Serialization/deserialization
- ✅ Mock data fixtures
- **Output:** `src/data/models.py` + test fixtures
- **Testing:** Model validation tests

#### Domenica Sera 2h
- ✅ TaxAgent orchestrator skeleton
- ✅ Basic state management
- ✅ Query routing logic
- ✅ README e documentazione base
- **Output:** `src/core/tax_agent.py` skeleton
- **PR:** Aprire PR con struttura + documentazione

**Weekend 1 Total:** ~16-18 ore → Struttura solida + infrast. pronta

---

### 🎯 Weekend 2: MVP Features & Integration

#### Sabato Mattina 4h
- ✅ Retrieval Layer (basic semantic_search.py)
- ✅ Chunker interface (basic implementation)
- ✅ Query embedding pipeline
- ✅ Mock embeddings for MVP
- **Output:** `src/retrieval/` modules
- **Testing:** Unit tests per retrieval

#### Sabato Pomeriggio 4h
- ✅ 4 Specialized Scrapers
  - AgenziaEntrate (interpelli, circolari)
  - Cassazione (court rulings)
  - Normattiva (legislation)
  - Sole24Ore (tax news)
- ✅ Mock scrapers (test data)
- ✅ Document extraction logic
- **Output:** `src/services/scrapers/` - 4 files
- **Testing:** Unit tests per parsing
- **Deliverable:** Scraper che estrae ≥5 items per fonte

#### Domenica Mattina 4h
- ✅ Knowledge Base CRUD layer
- ✅ Document ingestion pipeline
- ✅ Deduplication logic
- ✅ Batch indexing
- **Output:** `src/data/knowledge_base.py`
- **Testing:** Integration tests end-to-end
- **Deliverable:** Carica ≥20 documenti test in Chroma

#### Domenica Pomeriggio 4h
- ✅ Tax Reasoning modules
  - favorable_position.py (pro thesis generation)
  - contrary_position.py (contra thesis generation)
  - risk_score.py (quantified risk assessment)
  - checklist_generator.py
- ✅ Pro/Contra thesis generation via LLM
- ✅ Risk point extraction
- **Output:** `src/reasoning/` - 4 files
- **Testing:** Unit tests per logic
- **Deliverable:** Analizza case study fiscale → output strutturato

#### Domenica Sera 3h
- ✅ Studio Memory (basic)
  - clients.py (client profiles)
  - cases.py (stored cases)
  - precedents.py (reference collection)
- ✅ Client Impact Analysis (mapper + analyzer)
- ✅ CLI interface (click)
- ✅ Commands: search, analyze, briefing, clients
- ✅ Output formatting (table + JSON)
- ✅ Integration tests end-to-end
- **Output:** `main.py` con CLI commands
- **Testing:** E2E tests per CLI
- **Deliverable:** CLI funzionante e testata

#### Lunedì (Opzionale) 2h
- ✅ Documentation completata
- ✅ Setup guide
- ✅ Example queries
- **PR finale:** Merge MVP in main

**Weekend 2 Total:** ~19-21 ore → MVP completato e funzionante

---

## MVP Acceptance Criteria

### ✅ Core Features

- [ ] **4 Data Scrapers**
  - Agenzia Entrate: Scrape interpelli
  - Cassazione: Scrape court rulings
  - Normattiva: Scrape legislation
  - Sole24Ore: Scrape tax news
  - Estrae: titolo, data, numero, contenuto
  - Salva in vector store
  - Rate limiting rispettato

- [ ] **Retrieval Layer**
  - Chunker implemented (basic)
  - Semantic search working
  - Reranker interface defined (not implemented)
  - Hybrid search interface defined (not implemented)

- [ ] **Knowledge Base**
  - CRUD operations funzionanti
  - ≥20 test documents indicizzati
  - Metadata searchable
  - Deduplicazione attiva

- [ ] **Tax Reasoning**
  - Pro thesis generato via LLM
  - Contra thesis generato via LLM
  - Risk score (0-100) generated
  - Risk points identificati
  - Checklist generata
  - Output strutturato (JSON)

- [ ] **Studio Memory**
  - Client profiles storage
  - Cases/precedents storage
  - Notes capability

- [ ] **Client Impact Analysis**
  - Identify affected clients
  - Impact severity assessment

- [ ] **CLI Interface**
  - `python main.py search --query "..."`
  - `python main.py analyze --issue "..."`
  - `python main.py briefing`
  - `python main.py clients list`
  - Help documentation

### ✅ Quality Standards

- [ ] Code coverage ≥70%
- [ ] Type hints su 100% public API
- [ ] Docstrings per tutti i moduli
- [ ] README completato
- [ ] Architecture docs completate
- [ ] Setup guide funzionante
- [ ] No hardcoded secrets
- [ ] Logging su tutti i componenti
- [ ] NO Weaviate dependency
- [ ] NO Selenium dependency

### ✅ Repository

- [ ] Branch structure clean
- [ ] CI/CD passing
- [ ] .gitignore completo
- [ ] .env.example fornito
- [ ] requirements.txt aggiornato (Chroma, Requests, BeautifulSoup only)
- [ ] LICENSE aggiunto

---

## MVP Demo Script

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# [Edit .env with API keys]

# Demo 1: Search in Knowledge Base
python main.py search --query "novità PEX 2024"
# → Mostra 5 documenti più rilevanti con score

# Demo 2: Analyze Tax Issue
python main.py analyze --issue "holding che rifattura costi: è deducibile?"
# → Mostra:
#    - Pro thesis
#    - Contra thesis
#    - Risk score (0-100)
#    - Risk points
#    - Checklist
#    - Source citations

# Demo 3: Daily Briefing
python main.py briefing
# → Mostra notizie ultimo giorno classificate per tema

# Demo 4: Client Management
python main.py clients list
python main.py clients add --name "Acme Corp" --sector "Manufacturing"

# Demo 5: Check Client Impact
python main.py analyze --issue "PEX changes" --check-clients
# → Mostra affected clients
```

---

## Post-MVP Priorities (Next)

### Phase 3a: Enhanced Retrieval (Week 3)
1. Reranker implementation (cross-encoder)
2. Hybrid search (BM25 + semantic)
3. Query expansion
4. Advanced chunking strategies
5. Source credibility scoring

### Phase 3b: Advanced Reasoning (Week 3-4)
1. Real embeddings (OpenAI / HuggingFace)
2. Production vector DB setup
3. Scraper multi-source expansion
4. Advanced risk assessment
5. Precedent pattern matching

### Phase 3c: Studio Features (Week 4)
1. Full precedents database
2. Team collaboration features
3. Annotation system
4. Email notifications
5. Slack integration

### Phase 4: UX & Scale
1. Web API (FastAPI)
2. Web UI (React / Vue)
3. Daily briefing delivery
4. Document upload
5. User preferences
6. Advanced reporting

---

## Success Metrics

**For MVP Success:**
- ✅ All 5 scrapers working (≥5 items each)
- ✅ Retrieval layer working
- ✅ Tax reasoning generating pro/contra/risk
- ✅ Studio memory storing clients & cases
- ✅ Client impact analysis identifying affected parties
- ✅ Code quality passing
- ✅ Zero showstopper bugs
- ✅ Setup guide confirmed working
- ✅ Demo script completo

**For Product Success (Post-MVP):**
- User can find relevant tax docs in <2 sec
- Risk analysis takes <5 sec
- Daily briefing generated <10 sec
- Confidence scores ≥0.75 for relevant results
- False positive rate <10%
- User can track client impacts

---

## Resource Requirements

### Compute
- Local machine sufficient (8GB RAM min)
- Chroma local embedding
- LLM via API (no GPU needed)
- No infrastructure needed for MVP

### APIs
- OpenAI API key (for LLM)
- Optional: HuggingFace API (for embeddings)

### Dependencies (MVP Stack)
- `chroma-db` (vector store)
- `requests` (HTTP client)
- `beautifulsoup4` (HTML parsing)
- `openai` (LLM provider)
- `pydantic` (data validation)
- `click` (CLI)
- `python-dotenv` (configuration)

### Time Commitment
- ~35-40 hours total
- ~18 hours weekend 1
- ~20 hours weekend 2
- Flexible scheduling (can split across more weekends)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | Fixed feature set, MVP-only for 2 weeks |
| Scraper fragility | Mock scrapers + BeautifulSoup only (no JS) |
| API rate limits | Built-in rate limiting, mock providers |
| Integration issues | Heavy use of mocks and fixtures initially |
| Time overruns | Clear hour allocations, daily check-ins |
| Data quality | Test fixtures with known good data |
| Complexity | Simplified architecture, no external DBs |

---

## Branch Strategy for MVP

```
main
├── feat/architecture-revision        (PR #1) ← You are here
├── feat/foundation-setup             (PR #2)
├── feat/llm-provider                 (PR #3)
├── feat/vector-store                 (PR #4)
├── feat/data-models                  (PR #5)
├── feat/retrieval-layer              (PR #6)
├── feat/specialized-scrapers         (PR #7)
├── feat/knowledge-base               (PR #8)
├── feat/tax-reasoning                (PR #9)
├── feat/studio-memory                (PR #10)
├── feat/client-impact                (PR #11)
└── feat/cli-interface                (PR #12)

↓ Merge all into main

main (v0.1 MVP)
```

---

## Repository Structure (Updated)

```
tax-junior-partner-ai/
├── src/
│   ├── core/
│   │   └── tax_agent.py
│   ├── retrieval/               ← NEW
│   │   ├── chunker.py
│   │   ├── semantic_search.py
│   │   ├── reranker.py
│   │   └── hybrid_search.py
│   ├── reasoning/               ← NEW
│   │   ├── favorable_position.py
│   │   ├── contrary_position.py
│   │   ├── risk_score.py
│   │   ├── missing_documents.py
│   │   └── checklist_generator.py
│   ├── studio_memory/           ← NEW
│   │   ├── clients.py
│   │   ├── cases.py
│   │   ├── precedents.py
│   │   └── notes.py
│   ├── briefing/                ← NEW
│   │   ├── morning_brief.py
│   │   └── relevance_scorer.py
│   ├── client_impact/           ← NEW
│   │   ├── client_mapper.py
│   │   └── impact_analyzer.py
│   ├── data/
│   │   ├── vector_store.py
│   │   ├── models.py
│   │   └── knowledge_base.py
│   ├── services/
│   │   ├── llm_provider.py
│   │   └── scrapers/            ← UPDATED (4 files instead of 1)
│   │       ├── agenzia_entrate.py
│   │       ├── cassazione.py
│   │       ├── normattiva.py
│   │       └── sole24ore.py
│   └── utils/
│       ├── config.py
│       ├── logger.py
│       └── exceptions.py
├── tests/
├── docs/
│   ├── architecture.md          ← UPDATED
│   └── mvp_roadmap.md           ← UPDATED
├── config/
│   └── settings.py
├── requirements.txt              ← NO Weaviate, NO Selenium
├── .env.example
├── main.py
└── README.md
```

---

## Requirements.txt (MVP)

```
# Core
python-dotenv>=0.19.0
pydantic>=1.9.0
click>=8.0.0

# LLM & Embeddings
openai>=0.27.0

# Vector Store
chroma-db>=0.3.0  # No Weaviate

# Web & Parsing
requests>=2.27.0
beautifulsoup4>=4.10.0  # No Selenium
lxml>=4.9.0

# Async
aiohttp>=3.8.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.18.0
pytest-cov>=3.0.0

# Dev
black>=22.0.0
mypy>=0.930
flake8>=4.0.0
isort>=5.10.0
```

---

## Notes & Considerations

- **Start small:** Mock providers permettono testing senza API calls
- **Scrapers:** Use only BeautifulSoup for static HTML (no JS rendering)
- **Test-driven:** Scrivere tests mentre sviluppi
- **Documentation:** Aggiorna docs mentre avanzano le features
- **Commits:** Frequent, small, meaningful commits
- **Review:** Self-review prima di PR
- **Flexibility:** Adjust timeline if needed, ma mantieni feature set
- **No External Infra:** Everything local for MVP (Chroma embedded)

---

## Decision Log

### Architecture Decisions

1. **Removed Weaviate from MVP**
   - Reason: Chroma sufficient for local development
   - Future: Can add Weaviate post-MVP for scaling
   - Impact: Simpler setup, faster iteration

2. **Removed Selenium from MVP**
   - Reason: Main sources (Agenzia, Cassazione) serve static HTML
   - Approach: BeautifulSoup + Requests only
   - Future: Add Selenium if JavaScript-heavy sources needed
   - Impact: No browser automation overhead

3. **Added Specialized Scrapers**
   - Reason: Better code organization and maintainability
   - Approach: 4 separate modules, shared extraction logic
   - Impact: Easy to add new sources, cleaner imports

4. **New Modules Added**
   - Retrieval Layer: Foundation for advanced search
   - Tax Reasoning: Core differentiator vs generic chatbot
   - Studio Memory: Personalization & learning
   - Client Impact: Proactive advisory capability

---

**Target completion:** Week of July 7-8, 2026

**Status tracking:** Use GitHub Issues + Projects for tracking
