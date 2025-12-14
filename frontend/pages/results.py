# ====================================
# 📦 IMPORTS
# ====================================
# import streamlit as st
# import requests
# import numpy as np
# import matplotlib.pyplot as plt

# def load_css():
#     with open("assets/style.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css()


# API = "http://127.0.0.1:8000/api/analyze/"


# -----------------------------------
# 👉 Vérifier que les réponses existent
# -----------------------------------
# if "answers" not in st.session_state:
#     st.error("Veuillez remplir le questionnaire d'abord.")
#     st.stop()

# answers = st.session_state["answers"]

# st.title("📊 Résultats AISCA – Analyse de Compétences Santé")
# st.write("Voici votre profil analysé grâce à SBERT et à l'IA générative.")


# -----------------------------------
# 👉 Appel à FastAPI
# -----------------------------------
# with st.spinner("Analyse en cours..."):
#     res = requests.post(API, json=answers).json()

# block_scores = res["block_scores"]
# global_score = res["global_score"]
# top3 = res["top3"]
# progression = res["progression"]
# bio = res["bio"]


# -----------------------------------
# 👉 Score Global
# -----------------------------------
# st.subheader("🎯 Score Global AISCA")

# color = (
#     "green" if global_score >= 0.6
#     else "orange" if global_score >= 0.4
#     else "red"
# )

# st.markdown(
#     f"<h2 style='color:{color}; font-size:40px;'>{round(global_score*100,1)}%</h2>",
#     unsafe_allow_html=True
# )


# -----------------------------------
# 👉 Radar Chart
# -----------------------------------
# st.subheader("🧭 Radar des Blocs de Compétences")

# labels = list(block_scores.keys())
# values = list(block_scores.values())

# angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
# values += values[:1]
# angles += angles[:1]

# fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
# ax.plot(angles, values, linewidth=2, color="blue")
# ax.fill(angles, values, alpha=0.25, color="skyblue")
# ax.set_xticks(angles[:-1])
# ax.set_xticklabels(labels, fontsize=12)

# st.pyplot(fig)



# -----------------------------------
# 👉 TOP 3 METIERS
# -----------------------------------
# st.subheader("🏥 Top 3 Métiers Recommandés")

# for job in top3:
#     st.markdown(f"### {job['title']} – **{round(job['score']*100,1)}%**")
#     st.write(job["description"])
#     st.write("---")



# -----------------------------------
# 👉 Plan de progression
# -----------------------------------
# st.subheader("📘 Plan de progression personnalisé")
# st.write(progression)



# -----------------------------------
# 👉 Résumé automatique
# -----------------------------------
# st.subheader("🧬 Résumé automatique (BIO)")
# st.info(bio)



# -----------------------------------
# 👉 Retour au questionnaire
# -----------------------------------
# if st.button("↩️ Refaire le questionnaire"):
#     del st.session_state["answers"]
#     st.switch_page("app.py")
import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CHARGEMENT DU CSS
# =========================
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

API = "http://127.0.0.1:8000/api/analyze/"

# =========================
# VÉRIFICATION SESSION
# =========================
if "answers" not in st.session_state:
    st.error("Veuillez remplir le questionnaire d'abord.")
    st.stop()

answers = st.session_state["answers"]

# =========================
# TITRE
# =========================
st.title("📊 Résultats AISCA – Analyse de Compétences Santé")
st.write("Voici votre profil analysé grâce à SBERT et à l’IA générative.")

# =========================
# APPEL BACKEND
# =========================
with st.spinner("Analyse en cours..."):
    res = requests.post(API, json=answers).json()

block_scores = res["block_scores"]
global_score = res["global_score"]
top3 = res["top3"]
progression = res["progression"]
bio = res["bio"]

# =========================
# SCORE GLOBAL
# =========================
st.subheader("🎯 Score Global AISCA")

color = (
    "green" if global_score >= 0.6
    else "orange" if global_score >= 0.4
    else "red"
)

st.markdown(
    f"""
    <div class="card">
        <div class="score" style="color:{color}">
            {round(global_score * 100, 1)}%
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# RADAR CHART
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧭 Radar des Blocs de Compétences")

labels = list(block_scores.keys())
values = list(block_scores.values())

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=12)

st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TOP 3 MÉTIERS
# =========================
st.subheader("🏥 Top 3 Métiers Recommandés")

for job in top3:
    st.markdown(
        f"""
        <div class="job">
            <h3>{job['title']} – {round(job['score'] * 100, 1)}%</h3>
            <p>{job['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# PLAN DE PROGRESSION
# =========================
st.markdown(
    f"""
    <div class="card">
        <h3>📘 Plan de progression personnalisé</h3>
        <p>{progression}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# RÉSUMÉ AUTOMATIQUE
# =========================
st.markdown(
    f"""
    <div class="card">
        <h3>🧬 Résumé automatique</h3>
        <p>{bio}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# RETOUR
# =========================
if st.button("↩️ Refaire le questionnaire"):
    del st.session_state["answers"]
    st.switch_page("app.py")
