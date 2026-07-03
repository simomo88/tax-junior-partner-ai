import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Tax Junior Partner AI",
    layout="wide"
)

st.title("⚖️ Tax Junior Partner AI")
from datetime import datetime

def classify(doc):

    text = doc.get("title", "").lower()

    if "iva" in text:
        return "IVA"

    if "partecipazione" in text or "holding" in text:
        return "HOLDING"

    if "direttiva" in text or "francia" in text:
        return "FISCALITÀ INTERNAZIONALE"

    if "fusione" in text:
        return "OPERAZIONI STRAORDINARIE"

    if "trust" in text:
        return "TRUST"

    return "ALTRO"

folder = Path("data/raw/agenzia_entrate/interpello")

# carica i documenti prima di usarli nelle metriche
documents = []
if folder.exists():
    for f in folder.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                documents.append(json.load(fp))
        except Exception:
            pass

col1, col2, col3 = st.columns(3)

col1.metric("Interpelli", len(documents))
col2.metric("Circolari", 0)
col3.metric("Risoluzioni", 0)

if documents:
    st.caption(
        f"Ultimo aggiornamento: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

st.metric("Interpelli scaricati", len(documents))

st.divider()
st.subheader("📅 Morning Briefing")

for doc in documents[:3]:
    st.write(
        f"• Risposta {doc.get('number')} — "
        f"{doc.get('title','')[:120]}..."
    )

st.divider()

# ===== NUOVA SEZIONE =====

st.subheader("🧠 Analisi fiscale")

question = st.text_area(
    "Inserisci un quesito",
    placeholder="Es. holding che rifattura costi alle SPV"
)

if st.button("Analizza"):
    query = question.lower()

    relevant = []

    for doc in documents:

        score = 0

        title = doc.get("title", "").lower()

        for word in query.split():

            if word in title:
                score += 1

        if score > 0:
            relevant.append((score, doc))

    relevant.sort(reverse=True, key=lambda x: x[0])

    st.markdown("## Analisi preliminare")

    if relevant:

        st.success(
            f"Trovati {len(relevant)} documenti rilevanti"
        )

        st.markdown("### Documenti rilevanti")

        for score, doc in relevant[:5]:

            st.write(
                f"**Risposta {doc['number']} "
                f"({doc['publication_date']})**"
            )

            st.write(doc["title"])

            st.link_button(
                "Apri documento",
                doc["url"],
                key=doc["number"]
            )

    else:

        st.warning(
            "Nessun documento trovato"
        )

    st.markdown("### Tesi favorevole")

    st.write(
        "La posizione potrebbe essere sostenibile "
        "previa verifica della documentazione."
    )

    st.markdown("### Tesi contraria")

    st.write(
        "Occorre verificare rischi di contestazione "
        "e supporto documentale."
    )

    st.markdown("### Livello di rischio")

    st.warning("MEDIO")

st.divider()

# ===== SEZIONE ESISTENTE =====


st.divider()

# ===== SEZIONE ESISTENTE =====

search = st.text_input("Cerca")

for doc in sorted(
    documents,
    key=lambda x: x.get("publication_date", ""),
    reverse=True,
):
    text = (
        doc.get("title", "")
        + " "
        + doc.get("number", "")
    ).lower()

    if search and search.lower() not in text:
        continue

    title = doc.get("title", "Titolo non disponibile")
    number = doc.get("number", "N/A")
    publication_date = doc.get("publication_date", "N/A")
    url = doc.get("url")

    category = classify(doc)
    with st.expander(f"Risposta {number} - {publication_date}"):    
        st.write(title)
        st.json(doc)
        if url:
            st.link_button("Apri PDF", url)
        else:
            st.info("URL non disponibile")