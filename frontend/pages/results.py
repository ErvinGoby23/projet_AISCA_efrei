import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

API = "http://127.0.0.1:8000/api/analyze/"


if "answers" not in st.session_state:
    st.error("Veuillez remplir le questionnaire d'abord.")
    st.stop()

answers = st.session_state["answers"]


st.markdown("""
<h1>Analyse AISCA – Compétences Santé</h1>
<p style="text-align:center; font-size:18px;">
Votre profil a été analysé grâce au modèle <b>SBERT</b> et à l’IA générative.
</p>
""", unsafe_allow_html=True)


with st.spinner(" Analyse en cours..."):
    res = requests.post(API, json=answers).json()

block_scores = res.get("block_scores", {})
global_score = res.get("global_score", 0)
top3 = res.get("top3", [])
progression = res.get("progression", "")
bio_raw = res.get("bio", "")


st.subheader("Score Global AISCA")

score_color = (
    "#22c55e" if global_score >= 0.6
    else "#f59e0b" if global_score >= 0.4
    else "#ef4444"
)

st.markdown(
    f"<div class='card'><div class='score' style='color:{score_color}'>"
    f"{round(global_score * 100, 1)}%</div></div>",
    unsafe_allow_html=True
)

st.caption(
    "💡 Un score supérieur à 50 % indique une compatibilité modérée à bonne "
    "avec les métiers du soin."
)

st.subheader("Analyse des compétences")

if block_scores:
    labels = list(block_scores.keys())
    values = list(block_scores.values())

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Scores par bloc")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(labels, values, color="#3b82f6")
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=30)
        for i, v in enumerate(values):
            ax.text(i, v + 0.03, f"{round(v * 100)}%", ha="center")
        st.pyplot(fig)

    with col2:
        st.markdown("### 🧭 Radar des compétences")
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values_radar = values + values[:1]
        angles += angles[:1]

        fig2, ax2 = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax2.plot(angles, values_radar, color="#60a5fa", linewidth=2)
        ax2.fill(angles, values_radar, color="#3b82f6", alpha=0.3)
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(labels, fontsize=10)
        st.pyplot(fig2)

else:
    st.info("Graphiques non disponibles.")


st.subheader("🏥 Top 3 Métiers Recommandés")

cols = st.columns(3)

for i, job in enumerate(top3):
    with cols[i]:
        st.markdown(f"""
        <div class="job">
            <h3>{job['title']}</h3>
            <span>{round(job['score'] * 100, 1)}%</span>
            <p>{job['description']}</p>
        </div>
        """, unsafe_allow_html=True)


st.subheader("📘 Plan de progression personnalisé")

st.markdown(f"""
<div class="card">
    <p>{progression}</p>
</div>
""", unsafe_allow_html=True)


st.subheader("Résumé automatique")

if bio_raw:
    st.markdown(f"""
    <div class="card">
        <p>{bio_raw}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Résumé non disponible.")

st.caption(
    "⚠️ Cette analyse est une aide à l’orientation et ne remplace pas "
    "un entretien avec un professionnel."
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("↩️ Refaire le questionnaire"):
    del st.session_state["answers"]
    st.switch_page("app.py")
