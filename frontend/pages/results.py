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


with st.spinner("Analyse en cours..."):
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
    "Un score supérieur à 50 % indique une compatibilité modérée à bonne "
    "avec les métiers du soin."
)


st.subheader("Analyse des compétences")

if block_scores:
    labels = list(block_scores.keys())
    values = list(block_scores.values())

    BLOCK_NAMES = {
        1: "Gestes & Techniques de Soin",
        2: "Relation, Communication & Soutien",
        3: "Organisation & Gestion des Soins",
        4: "Observation Clinique & Analyse",
        5: "Hygiène, Sécurité & Prévention"
    }

    TARGET_PROFILE = {
        1: 0.65,
        2: 0.70,
        3: 0.65,
        4: 0.65,
        5: 0.60
    }

    target_values = [TARGET_PROFILE[int(b)] for b in labels]
    gaps = [target_values[i] - values[i] for i in range(len(values))]

    FIG_SIZE = (5, 4) 

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Écart au profil métier ")

        x = np.arange(len(labels))
        width = 0.35

        fig1, ax1 = plt.subplots(figsize=FIG_SIZE)
        ax1.bar(x - width/2, values, width, label="Votre profil", color="#3b82f6")
        ax1.bar(x + width/2, target_values, width, label="Profil attendu", color="#9ca3af")

        ax1.set_xticks(x)
        ax1.set_xticklabels(
            [BLOCK_NAMES[int(b)] for b in labels],
            rotation=25
        )
        ax1.set_ylim(0, 1)
        ax1.legend()

        for i, v in enumerate(values):
            ax1.text(i - width/2, v + 0.02, f"{round(v*100)}%", ha="center", fontsize=9)

        for i, v in enumerate(target_values):
            ax1.text(i + width/2, v + 0.02, f"{round(v*100)}%", ha="center", fontsize=9)

        fig1.tight_layout()
        st.pyplot(fig1)

    with col2:
        st.markdown("### Priorités de progression")

        fig2, ax2 = plt.subplots(figsize=FIG_SIZE)
        ax2.bar(
            [BLOCK_NAMES[int(b)] for b in labels],
            gaps,
            color="#ef4444"
        )

        ax2.set_ylabel("Écart à combler")
        ax2.set_ylim(0, max(gaps) + 0.05)

        for i, v in enumerate(gaps):
            ax2.text(i, v + 0.01, f"{round(v*100,1)}%", ha="center", fontsize=9)

        plt.xticks(rotation=25)

        fig2.tight_layout()
        st.pyplot(fig2)

else:
    st.info("Graphiques non disponibles.")


st.subheader("Top 3 Métiers Recommandés")

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


st.subheader("Plan de progression personnalisé")

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
    "Cette analyse est une aide à l’orientation et ne remplace pas "
    "un entretien avec un professionnel."
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Refaire le questionnaire"):
    del st.session_state["answers"]
    st.switch_page("app.py")
