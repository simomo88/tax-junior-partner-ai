# Architecture Documentation

## System Design

Tax Junior Partner AI è architettato come un sistema modulare con separazione chiara delle responsabilità.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                   (CLI / Web / Chat API)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Tax Agent (Orchestrator)                 │
│              Coordina tutti i componenti                     │
└──────────────────┬──────────────────┬──────────────────────┘
                   │                  │
      ┌────────────▼────────┐   ┌─────▼──────────────┐
      │  News Aggregator   │   │  Risk Analyzer     │
      │  & Scraper         │   │  & Tesis Generator │
      │  - Agenzia Entrate │   │  - Pro & Contra    │
      │  - Circolari       │   │  - Risk Points     │
      │  - Sentenze        │   │  - Checklist       │
      └────────────┬────────┘   └─────┬──────────────┘
                   │                  │
      ┌────────────▼──────────────────▼────────────┐
      │         Knowledge Base & Storage           │
      │  - Vector Store (Chroma / Weaviate)       │
      │  - Document Repository                     │
      │  - Metadata Index                          │
      └────────────┬──────────────────────────────┘
                   │
      ┌────────────▼──────────────────────────────┐
      │         LLM & Services Layer              │
      │  - LLM Provider (OpenAI / Anthropic)     │
      │  - Embeddings (OpenAI / HuggingFace)     │
      │  - External APIs (Agenzia Entrate)      │
      └───────────────────────────────────────────┘
```

## Core Components

### 1. **TaxAgent (Orchestrator)**

**Responsabilità:**
- Coordina il flusso di esecuzione
- Mantiene lo stato della conversazione
- Delega ai moduli specializzati
- Gestisce context e memoria

**Interfaccia:**
```python
class TaxAgent:
    async def process_query(query: str) -> AgentResponse
    async def analyze_tax_issue(issue: TaxIssue) -> RiskAnalysis
    async def get_daily_briefing() -> DailyBriefing
    async def search_knowledge_base(query: str) -> SearchResults
```

### 2. **NewsAggregator**

**Responsabilità:**
- Scraping fonti ufficiali
- Classificazione automatica
- Deduplicazione
- Memorizzazione KB

**Fonti (MVP):**
- Agenzia Entrate (Interpelli, Circolari)
- Gazzetta Ufficiale
- Riviste specializzate (API)

**Output:** DailyBriefing con items classificati per tema

### 3. **RiskAnalyzer**

**Responsabilità:**
- Generazione tesi favorevole
- Generazione tesi contraria
- Identificazione punti di rischio
- Creazione checklist compliance
- Citazione fonti

**Prompt Chain:**
1. Understanding → Analizza il quesito
2. Research → Cerca nel KB
3. Tesis Generation → Genera pro/contro
4. Risk Identification → Identifica rischi
5. Checklist → Crea checklist

### 4. **VectorStore Interface**

**Responsabilità:**
- Astrazione db vettoriale
- CRUD operazioni
- Semantic search
- Metadata filtering

**Implementazioni supportate:**
- Chroma (local-first, embedded)
- Weaviate (scalable, self-hosted)
- Future: Pinecone, Supabase

### 5. **LLM Provider**

**Responsabilità:**
- Interfaccia unificata LLM
- Token counting
- Rate limiting
- Fallback handling
- Cost tracking

**Implementazioni:**
- OpenAI GPT-4 / GPT-3.5
- Anthropic Claude
- Future: Local models (Ollama)

### 6. **News Scraper**

**Responsabilità:**
- Web scraping
- Parsing documenti
- Estrarre metadata (data, numero, URL)
- Normalizzazione formato

**Tecnologie:**
- BeautifulSoup4 per parsing HTML
- Requests per HTTP
- Selenium per JS-heavy sites
- AsyncIO per parallelizzazione

## Data Models

### TaxDocument
```python
class TaxDocument(BaseModel):
    id: str  # UUID
    title: str
    content: str
    source: str  # "agenzia-entrate", "circolare", etc
    document_type: str  # "interpello", "risoluzione", etc
    publication_date: datetime
    url: str
    tags: List[str]
    extracted_topics: List[str]
    relevance_score: float
    metadata: Dict[str, Any]
```

### SearchResult
```python
class SearchResult(BaseModel):
    document: TaxDocument
    similarity_score: float
    reasoning: str
    confidence: float
```

### RiskAnalysis
```python
class RiskAnalysis(BaseModel):
    query: str
    pro_thesis: str
    contra_thesis: str
    risk_points: List[RiskPoint]
    confidence: float
    source_documents: List[TaxDocument]
    checklist: List[ChecklistItem]
    recommendations: List[str]
```

## Development Phases

### Phase 1: Foundation (Weekend 1)
- Setup progetto e struttura
- Core configuration management
- LLM provider interface (mock + real)
- Vector store interface (mock + Chroma)
- Base data models
- Logging infrastructure

### Phase 2: MVP Features (Weekend 2)
- News scraper (Agenzia Entrate)
- Knowledge base CRUD
- Semantic search (basic)
- Risk analyzer (core logic)
- End-to-end integration
- CLI interface basic

### Phase 3: Production Ready
- Production embeddings
- Advanced scraping
- Caching & optimization
- Error handling & resilience
- Monitoring & alerting
- API server (FastAPI)
- Web UI

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

## Security Considerations

- Environment variables per secrets (no hardcoding)
- API key rotation support
- Rate limiting per LLM provider
- Input validation & sanitization
- Document access control (future)
- Audit logging per analisi

## Future Extensions

- **Multi-language** → Italian + English
- **RAG Advanced** → Hybrid search (BM25 + semantic)
- **Document Upload** → Internal docs indexing
- **Collaborative Features** → Team annotations
- **Reporting** → PDF/Word export
- **Integration** → Slack, Teams, Email
- **Mobile** → App version
