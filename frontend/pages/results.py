import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

API = "http://127.0.0.1:8000/api/analyze/"

# -----------------------------------
# Vérifier que les réponses existent
# -----------------------------------
if "answers" not in st.session_state:
    st.error("Veuillez remplir le questionnaire d'abord.")
    st.stop()

answers = st.session_state["answers"]

# -----------------------------------
# TITRE PRINCIPAL
# -----------------------------------
st.markdown("""
<h1 style="text-align:center; color:#2A8BF2;">
📊 Analyse AISCA – Compétences Santé
</h1>
<p style="text-align:center; font-size:18px;">
Votre profil a été analysé grâce au modèle SBERT et à l’IA générative.
</p>
""", unsafe_allow_html=True)

# -----------------------------------
# Appel à FastAPI
# -----------------------------------
with st.spinner("⏳ Analyse en cours..."):
    res = requests.post(API, json=answers).json()

block_scores = res["block_scores"]
global_score = res["global_score"]
top3 = res["top3"]
progression = res["progression"]
bio = res["bio"]

# -----------------------------------
# SCORE GLOBAL
# -----------------------------------
st.subheader("🎯 Score Global AISCA")

color = (
    "green" if global_score >= 0.6
    else "orange" if global_score >= 0.4
    else "red"
)

st.markdown(
    f"<h2 style='color:{color}; font-size:50px; text-align:center;'>{round(global_score*100,1)}%</h2>",
    unsafe_allow_html=True
)


# ============================================================
# 📊 NOUVEAU : Bar Chart des Scores par Bloc
# ============================================================
st.subheader("📌 Scores par Bloc de Compétences (Bar Chart)")

fig, ax = plt.subplots(figsize=(7,4))
labels = list(block_scores.keys())
values = list(block_scores.values())

ax.bar(labels, values, color="cornflowerblue", edgecolor="black")
ax.set_ylabel("Score", fontsize=12)
ax.set_title("Scores par Bloc", fontsize=14)
ax.set_ylim(0, 1)

for i, v in enumerate(values):
    ax.text(i, v + 0.02, f"{round(v*100)}%", ha="center", fontsize=12)

st.pyplot(fig)


# ============================================================
# 🧭 Radar Chart
# ============================================================
st.subheader("🧭 Radar des Blocs de Compétences")

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values_radar = values + values[:1]
angles += angles[:1]

fig2, ax2 = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax2.plot(angles, values_radar, linewidth=2, color="blue")
ax2.fill(angles, values_radar, alpha=0.25, color="skyblue")
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(labels, fontsize=12)

st.pyplot(fig2)



# ============================================================
# 🏥 TOP 3 MÉTIERS
# ============================================================
st.subheader("🏥 Top 3 Métiers Recommandés")

for job in top3:
    st.markdown(f"""
    <div style='padding:15px; border-radius:10px; background:#F4F9FF; margin-bottom:10px;'>
        <h3 style='margin:0;'>{job['title']} — <span style='color:#2A8BF2;'>{round(job['score']*100,1)}%</span></h3>
        <p>{job['description']}</p>
    </div>
    """, unsafe_allow_html=True)



# ============================================================
# 📘 Plan de progression IA
# ============================================================
st.subheader("📘 Plan de progression personnalisé")
st.info(progression)



# ============================================================
# 🧬 Résumé automatique
# ============================================================
st.subheader("🧬 Résumé automatique (BIO)")
st.success(bio)



# ============================================================
# Retour bouton
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("↩️ Refaire le questionnaire"):
    del st.session_state["answers"]
    st.switch_page("app.py")
