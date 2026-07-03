# Architecture Documentation - Tax Junior Partner AI

## Mission Clarification

**Objective:** Build a "Tax Junior Partner AI" - not a chatbot, but an intelligent assistant that reasons like a junior tax advisor.

---

## System Design

Tax Junior Partner AI è architettato come un sistema modulare specializzato per il ragionamento fiscale:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        User Interface                                           │
│                   (CLI / Web / Chat API)                                        │
└─────────────────────────────────────┬──────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────▼──────────────────────────────────────────┐
│                    Tax Agent (Orchestrator)                                     │
│              Coordina flusso di ragionamento fiscale                            │
└──────────────────────┬──────────────────┬──────────────────┬───────────────────┘
                       │                  │                  │
      ┌────────────────▼────────┐  ┌─────▼──────────────┐ ┌──▼────────────────┐
      │  Retrieval Layer        │  │  Tax Reasoning     │ │ Studio Memory      │
      │                         │  │                    │ │                    │
      │ - Chunker               │  │ - Pro/Contra       │ │ - Clients          │
      │ - Semantic Search       │  │ - Risk Scoring     │ │ - Cases            │
      │ - Reranker              │  │ - Missing Docs     │ │ - Precedents       │
      │ - Hybrid Search         │  │ - Checklists       │ │ - Notes            │
      └────────────┬────────────┘  └─────┬──────────────┘ └──┬────────────────┘
                   │                      │                   │
      ┌────────────▼──────────────────────▼───────────────────▼────────┐
      │         Knowledge Base            │                           │
      │   (Vector Store + Metadata)       │   Client Impact Analysis  │
      │   - Chroma (Embedded)             │   - Client Mapper         │
      │   - Document Repository           │   - Impact Analyzer       │
      │   - Metadata Index                │                           │
      └────────────┬──────────────────────┴───────────────────────────┘
                   │
      ┌────────────▼──────────────────────────────────┐
      │       Morning Briefing Module                 │
      │                                               │
      │ - Daily Briefing Generator                    │
      │ - Relevance Scoring                           │
      │ - Priority Ranking                            │
      └────────────┬──────────────────────────────────┘
                   │
      ┌────────────▼──────────────────────────────────┐
      │    Data Collection & Normalization            │
      │                                               │
      │  services/scrapers/                           │
      │  ├── agenzia_entrate.py                       │
      │  ├── cassazione.py                            │
      │  ├── normattiva.py                            │
      │  └── sole24ore.py                             │
      └────────────┬──────────────────────────────────┘
                   │
      ┌────────────▼──────────────────────────────────┐
      │      LLM & Services Layer                     │
      │                                               │
      │  - LLM Provider (OpenAI/Anthropic)            │
      │  - Embeddings (OpenAI/HuggingFace)            │
      │  - External APIs                              │
      └───────────────────────────────────────────────┘
```

---

## Core Components

### 1. **TaxAgent (Orchestrator)**

**Responsabilità:**
- Coordina il flusso di ragionamento fiscale
- Mantiene lo stato della conversazione
- Delega ai moduli specializzati
- Gestisce context e memoria del junior partner

**Interfaccia:**
```python
class TaxAgent:
    async def process_query(query: str) -> AgentResponse
    async def analyze_tax_issue(issue: TaxIssue) -> RiskAnalysis
    async def get_daily_briefing() -> DailyBriefing
    async def search_knowledge_base(query: str) -> SearchResults
    async def check_client_impact(issue: TaxIssue) -> ClientImpact
```

---

## 1. Retrieval Layer

**Posizione:** `src/retrieval/`

**Componenti:**

#### `chunker.py`
- Intelligente document chunking
- Preservation di contesto legale
- Metadata propagation
- Support per molteplici tipi di documento

#### `semantic_search.py`
- Query embedding
- Similarity scoring
- Top-K retrieval
- Confidence scoring

#### `reranker.py`
- Cross-encoder reranking
- Tax-specific relevance signals
- Source credibility scoring
- Temporal relevance weighting

#### `hybrid_search.py`
- Combined BM25 + semantic search
- Weighted fusion
- Query expansion
- Boolean logic support

**Purpose:**
- Efficiente document retrieval
- Ranking di fonti per credibilità
- Minimizzare hallucinations
- Fondazione per citazioni accurate

---

## 2. Studio Memory

**Posizione:** `src/studio_memory/`

**Componenti:**

#### `clients.py`
- Profilo cliente (settore, dimensione, complessità)
- Storico questioni
- Preferenze di comunicazione
- Risk profile

#### `cases.py`
- Questioni fiscali risolte
- Outcome e risultati
- Lessons learned
- Pattern recognition

#### `precedents.py`
- Internal precedents (interpelli, circolari)
- Giurisprudenza rilevante
- Administrative rulings
- Posizioni consolidate dello studio

#### `notes.py`
- Annotazioni junior partner
- Research findings
- Tag e categorizzazione
- Linked references

**Purpose:**
- Ricordare casi precedenti
- Evitare di ripetere errori
- Build institutional knowledge
- Personalize analysis per client

---

## 3. Morning Briefing

**Posizione:** `src/briefing/`

**Componenti:**

#### `morning_brief.py`
- Aggregazione notizie overnight
- Personalized per tema/area
- Classificazione per urgenza
- Auto-categorization

#### `relevance_scorer.py`
- Score rilevanza per studio
- Score rilevanza per singoli client
- Trend detection
- Impact estimation

**Purpose:**
- Keep updated su sviluppi
- Prioritize important tax news
- Identify client impacts early
- Enable proactive advising

---

## 4. Tax Reasoning

**Posizione:** `src/reasoning/`

**Componenti:**

#### `favorable_position.py`
- Generazione tesi favorevole
- Pro arguments with citations
- Supporting evidence gathering
- Caveat identification

#### `contrary_position.py`
- Generazione tesi contraria
- Counter-arguments
- Challenging evidence
- Revenue authority perspective

#### `risk_score.py`
- Risk quantification (0-100)
- Confidence interval
- Exposure estimation
- Probability assessment

#### `missing_documents.py`
- Identify documentation gaps
- Suggest documentation strategy
- Evidence collection plan
- Protection recommendations

#### `checklist_generator.py`
- Compliance checklist
- Documentation requirements
- Timeline & deadlines
- Escalation triggers

**Purpose:**
- Reason come un junior tax advisor
- Balance pro/contro perspectives
- Structured risk analysis
- Actionable recommendations

---

## 5. Client Impact Analysis

**Posizione:** `src/client_impact/`

**Componenti:**

#### `client_mapper.py`
- Map tax development → affected clients
- Sector/activity matching
- Threshold identification
- Priority ranking

#### `impact_analyzer.py`
- Quantify potential impact
- Financial exposure
- Compliance implications
- Recommended actions

**Purpose:**
- Identify relevant clients per news
- Proactive client notifications
- Enable targeted consultations
- Build advisory partnerships

---

## 6. Data Collection & Normalization

**Posizione:** `services/scrapers/`

**Componenti:**

#### `agenzia_entrate.py`
- Agenzia Entrate interpelli
- Circolari e risoluzioni
- Press releases
- Normative updates

#### `cassazione.py`
- Corte di Cassazione rulings
- Regional court decisions
- Administrative case law
- Judicial precedents

#### `normattiva.py`
- Italian legislation
- Decree updates
- Regulatory changes
- Legislative history

#### `sole24ore.py`
- Tax news & analysis
- Industry publications
- Expert commentary
- Market insights

**Technology Stack (MVP):**
- **HTTP Client:** `requests` (no Selenium)
- **HTML Parsing:** `BeautifulSoup4`
- **Async I/O:** `asyncio`
- **Rate Limiting:** Built-in
- **Caching:** Local disk cache

**MVP Simplification:**
- ✅ **KEEP:** Chroma, Requests, BeautifulSoup
- ❌ **REMOVE:** Weaviate (use Chroma locally)
- ❌ **REMOVE:** Selenium (static parsing only)

---

## Data Models

### TaxDocument
```python
class TaxDocument(BaseModel):
    id: str  # UUID
    title: str
    content: str
    source: str  # "agenzia-entrate", "cassazione", etc
    document_type: str  # "interpello", "sentenza", etc
    publication_date: datetime
    url: str
    tags: List[str]
    extracted_topics: List[str]
    relevance_score: float
    metadata: Dict[str, Any]
    credibility_score: float  # Source trustworthiness
```

### SearchResult
```python
class SearchResult(BaseModel):
    document: TaxDocument
    similarity_score: float
    reasoning: str
    confidence: float
    rank: int  # After reranking
```

### RiskAnalysis
```python
class RiskAnalysis(BaseModel):
    query: str
    pro_thesis: str
    contra_thesis: str
    risk_points: List[RiskPoint]
    risk_score: float  # 0-100
    confidence: float
    source_documents: List[TaxDocument]
    missing_documents: List[str]
    checklist: List[ChecklistItem]
    recommendations: List[str]
```

### ClientImpact
```python
class ClientImpact(BaseModel):
    tax_development: TaxDocument
    affected_clients: List[str]
    impact_severity: str  # "high", "medium", "low"
    recommended_action: str
    financial_exposure: Optional[float]
    timeline: str
```

---

## Development Phases

### Phase 1: Foundation (Weekend 1)
- Setup progetto e struttura
- Core configuration management
- LLM provider interface (mock + real)
- Vector store interface (mock + Chroma)
- Base data models
- Logging infrastructure

### Phase 2: MVP Features (Weekend 2)
- Retrieval Layer (basic implementation)
- News scrapers (4 sources)
- Knowledge base CRUD
- Tax Reasoning (pro/contra + risk scoring)
- Studio Memory (basic clients & cases)
- CLI interface
- End-to-end integration

### Phase 3: Advanced (Week 3+)
- Reranking + Hybrid Search
- Morning Briefing + Client Impact
- Advanced precedent matching
- Production embeddings
- Web API (FastAPI)
- Web UI

---

## Repository Structure

```
tax-junior-partner-ai/
├── src/
│   ├── core/
│   │   └── tax_agent.py          # Orchestrator
│   ├── retrieval/
│   │   ├── chunker.py
│   │   ├── semantic_search.py
│   │   ├── reranker.py
│   │   └── hybrid_search.py
│   ├── reasoning/
│   │   ├── favorable_position.py
│   │   ├── contrary_position.py
│   │   ├── risk_score.py
│   │   ├── missing_documents.py
│   │   └── checklist_generator.py
│   ├── studio_memory/
│   │   ├── clients.py
│   │   ├── cases.py
│   │   ├── precedents.py
│   │   └── notes.py
│   ├── briefing/
│   │   ├── morning_brief.py
│   │   └── relevance_scorer.py
│   ├── client_impact/
│   │   ├── client_mapper.py
│   │   └── impact_analyzer.py
│   ├── data/
│   │   ├── vector_store.py
│   │   ├── models.py
│   │   └── knowledge_base.py
│   ├── services/
│   │   ├── llm_provider.py
│   │   └── scrapers/
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
│   ├── architecture.md
│   └── mvp_roadmap.md
├── config/
│   └── settings.py
├── requirements.txt
├── .env.example
├── main.py
└── README.md
```

---

## Error Handling Strategy

**Livelli di errore:**

1. **Critical** → Ferma esecuzione, alert
   - LLM API failure
   - Vector store crash
   - Data corruption

2. **High** → Fallback con degradazione
   - Scraper timeout → usa cache
   - Embedding API down → usa mock
   - Partial search → best effort

3. **Medium** → Log & continue
   - Formatting errors
   - Partial data extraction
   - Rate limiting

4. **Low** → Log silently
   - Missing optional fields
   - Cache misses
   - Metadata extraction failures

---

## Performance Considerations

### Scalability
- Async/await per I/O operations
- Batch processing per embeddings
- Connection pooling per DB
- Caching multi-layer (memory + disk)

### Optimization
- Lazy loading documents
- Incremental indexing
- Smart batching per LLM calls
- Vector cache per semantic searches

### Monitoring
- Token usage tracking
- API latency metrics
- Cache hit rates
- Error rates per component

---

## Security Considerations

- Environment variables per secrets (no hardcoding)
- API key rotation support
- Rate limiting per LLM provider
- Input validation & sanitization
- Document access control (future)
- Audit logging per analisi

---

## Future Extensions

- **Multi-language** → Italian + English
- **RAG Advanced** → More sophisticated fusion strategies
- **Document Upload** → Internal docs indexing
- **Collaborative Features** → Team annotations
- **Reporting** → PDF/Word export with citations
- **Integration** → Slack, Teams, Email
- **Mobile** → App version
- **Advanced Reasoning** → Full logical argumentation
- **Precedent Discovery** → Automated pattern matching
