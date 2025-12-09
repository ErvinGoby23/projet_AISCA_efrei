import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AISCA – Questionnaire", page_icon="🩺")

st.title("🩺 AISCA – Questionnaire de Compétences Santé")
st.write("Veuillez répondre aux questions suivantes de manière honnête et détaillée.")

# -----------------------------
# QUESTIONS OUVERTES
# -----------------------------
q1 = st.text_area("1️⃣ Décrivez une situation où vous avez aidé quelqu’un.")
q2 = st.text_area("2️⃣ Qu’est-ce qui vous attire dans le fait d’aider ou accompagner une personne ?")
q3 = st.text_area("3️⃣ Racontez un moment où vous avez dû gérer une situation stressante.")
q4 = st.text_area("4️⃣ Décrivez une situation où vous avez dû être très rigoureux(se) ou organisé(e).")
q5 = st.text_area("5️⃣ Comment réagiriez-vous si une personne ne se sent pas bien ?")
q6 = st.text_area("6️⃣ Quelles qualités vous représentent le mieux dans un contexte de soin ?")
q7 = st.text_area("7️⃣ Quelles tâches ou situations vous mettraient le plus en difficulté dans un métier de la santé ?")
q10 = st.text_area("8️⃣ Quels types de métiers vous attirent le moins, et pourquoi ?")

# -----------------------------
# QUESTION CHOIX MULTIPLE
# -----------------------------
q9 = st.multiselect(
    "9️⃣ Quelle activité dans le domaine de la santé vous attire le plus ?",
    [
        "Assister dans des soins",
        "Observer et surveiller un patient",
        "Soutenir moralement et communiquer",
        "Organiser un service ou des dossiers",
        "Assurer hygiène et propreté",
        "Je ne sais pas"
    ]
)

# -----------------------------
# BOUTON ENVOI
# -----------------------------
if st.button("📤 Envoyer mes réponses"):

    # Construire l'objet JSON
    answers = {
        "q1_help": q1,
        "q2_motivation": q2,
        "q3_stress": q3,
        "q4_rigueur": q4,
        "q5_patient_state": q5,
        "q6_qualities": q6,
        "q7_difficulty": q7,
        "q10_rejection_text": q10,
        "q9_interest": q9
    }

    # Vérifier que toutes les réponses sont remplies
    if any(value == "" for key, value in answers.items() if key != "q9_interest"):
        st.error("⚠️ Merci de répondre à toutes les questions avant de continuer.")
        st.stop()

    # Sauvegarde dans le backend FastAPI
    res = requests.post(f"{API}/save-responses/", json=answers)

    if res.status_code == 200 or res.status_code == 201:

        # 🔥 Stocker les réponses dans la session Streamlit
        st.session_state["answers"] = answers

        # 🔥 Redirection automatique vers la page des résultats
        st.switch_page("pages/results.py")

    else:
        st.error("❌ Erreur lors de l’enregistrement des réponses.")
        st.write("Détails :", res.text)
