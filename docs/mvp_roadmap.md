# MVP Roadmap: 1-2 Weekends Implementation Plan

## Obiettivo MVP

Un sistema minimale funzionante che dimostra:
1. Aggregazione notizie fiscali (mock + base reale)
2. Knowledge base con semantic search (Chroma + embeddings mock)
3. Risk analyzer che genera tesi pro/contro
4. CLI interface per testing

## Timeline Dettagliato

### 🎯 Weekend 1: Foundation & Setup

#### Venerdì 2h
- ✅ Repository setup completato
- ✅ Folder structure creata
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
- ✅ Data models (TaxDocument, SearchResult, RiskAnalysis)
- ✅ Pydantic validators
- ✅ Serialization/deserialization
- ✅ Mock data fixtures
- **Output:** `src/data/models/` + test fixtures
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
- ✅ News Scraper interface
- ✅ AgenziaEntrate scraper (HTML parser)
- ✅ Mock news scraper (test data)
- ✅ Document extraction logic
- **Output:** `src/services/news_scraper.py`
- **Testing:** Unit tests per parsing
- **Deliverable:** Scraper che estrae ≥5 items da Agenzia Entrate

#### Sabato Pomeriggio 4h
- ✅ Knowledge Base CRUD layer
- ✅ Document ingestion pipeline
- ✅ Deduplication logic
- ✅ Batch indexing
- **Output:** `src/data/knowledge_base.py`
- **Testing:** Integration tests end-to-end
- **Deliverable:** Carica ≥20 documenti test in Chroma

#### Domenica Mattina 4h
- ✅ Semantic search implementation
- ✅ Query embedding (mock embeddings per MVP)
- ✅ Similarity scoring
- ✅ Result ranking e filtering
- **Output:** Search endpoint in TaxAgent
- **Testing:** Search accuracy tests
- **Deliverable:** Ricerca semantica query "novità PEX" → risultati ordinati

#### Domenica Pomeriggio 4h
- ✅ Risk Analyzer core logic
- ✅ Pro/Contra thesis generation via LLM
- ✅ Risk point extraction
- ✅ Checklist generation
- **Output:** `src/core/risk_analyzer.py`
- **Testing:** Unit tests per logic
- **Deliverable:** Analizza case study fiscale → output strutturato

#### Domenica Sera 3h
- ✅ CLI interface (click)
- ✅ Commands: search, analyze, daily-briefing
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

- [ ] **News Scraper**
  - Scrape Agenzia Entrate interpelli
  - Estrae: titolo, data, numero, contenuto
  - Salva in vector store
  - Rate limiting rispettato

- [ ] **Knowledge Base**
  - CRUD operations funzionanti
  - ≥20 test documents indicizzati
  - Metadata searchable
  - Deduplicazione attiva

- [ ] **Semantic Search**
  - Query naturali supportate
  - Top-5 results returned
  - Similarity scores visibili
  - Confidence scoring

- [ ] **Risk Analyzer**
  - Pro thesis generato via LLM
  - Contra thesis generato via LLM
  - Risk points identificati
  - Checklist generata
  - Output strutturato (JSON)

- [ ] **CLI Interface**
  - `python main.py search --query "..."`
  - `python main.py analyze --issue "..."`
  - `python main.py briefing`
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

### ✅ Repository

- [ ] Branch structure clean
- [ ] CI/CD passing
- [ ] .gitignore completo
- [ ] .env.example fornito
- [ ] requirements.txt aggiornato
- [ ] LICENSE aggiunto

---

## MVP Demo Script

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# [Edit .env with API keys]

# Demo 1: Search
python main.py search --query "novità PEX 2024"
# → Mostra 5 documenti più rilevanti con score

# Demo 2: Analyze
python main.py analyze --issue "holding che rifattura costi: è deducibile?"
# → Mostra:
#    - Pro thesis
#    - Contra thesis  
#    - Risk points
#    - Checklist

# Demo 3: Briefing
python main.py briefing
# → Mostra notizie ultimo giorno classificate per tema
```

---

## Post-MVP Priorities (Next)

### Phase 3a: Production Ready (Week 3)
1. Real embeddings (OpenAI / HuggingFace)
2. Production vector DB setup
3. Scraper multi-source
4. Caching layer
5. Error handling resilience
6. Monitoring & logging

### Phase 3b: UX & Scale (Week 4)
1. Web API (FastAPI)
2. Web UI (React / Vue)
3. Email briefing delivery
4. Slack integration
5. Document upload
6. User preferences

### Phase 4: Advanced Features
1. RAG advanced (BM25 hybrid)
2. Multi-language
3. Document annotations
4. Team collaboration
5. Report generation
6. Integration ecosystems

---

## Success Metrics

**For MVP Success:**
- ✅ All 5 features working
- ✅ Code quality passing
- ✅ Zero showstopper bugs
- ✅ Setup guide confirmed working
- ✅ Demo script completo

**For Product Success:**
- User can find relevant tax docs in <2 sec
- Risk analysis takes <5 sec
- Daily briefing generated <10 sec
- Confidence scores ≥0.75 for relevant results
- False positive rate <10%

---

## Resource Requirements

### Compute
- Local machine sufficient (8GB RAM min)
- Chroma local embedding
- LLM via API (no GPU needed)

### APIs
- OpenAI API key (for LLM)
- Optional: HuggingFace API (for embeddings)

### Time Commitment
- ~35-40 hours total
- ~18 hours weekend 1
- ~20 hours weekend 2
- Flexible scheduling (can split across more weekends)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | Fixed feature set, aggressive MVP scope |
| API rate limits | Built-in rate limiting, mock providers |
| Integration issues | Heavy use of mocks and fixtures initially |
| Time overruns | Clear hour allocations, daily check-ins |
| Data quality | Test fixtures with known good data |

---

## Branch Strategy for MVP

```
main
├── feat/initial-project-structure  (PR #1)
├── feat/foundation-setup           (PR #2)
├── feat/llm-provider               (PR #3)
├── feat/vector-store               (PR #4)
├── feat/data-models                (PR #5)
├── feat/news-scraper               (PR #6)
├── feat/knowledge-base             (PR #7)
├── feat/semantic-search            (PR #8)
├── feat/risk-analyzer              (PR #9)
└── feat/cli-interface              (PR #10)

↓ Merge all into main

main (v0.1 MVP)
```

---

## Notes & Considerations

- **Start small:** Mock providers permettono testing senza API calls
- **Test-driven:** Scrivere tests mentre sviluppi
- **Documentation:** Aggiorna docs mentre avanzano le features
- **Commits:** Frequent, small, meaningful commits
- **Review:** Self-review prima di PR
- **Flexibility:** Adjust timeline if needed, ma mantieni feature set

---

**Target completion:** Week of July 7-8, 2026

**Status tracking:** Use GitHub Issues + Projects for tracking
