# AISCA – Agent Intelligent Sémantique et Génératif pour la Cartographie des Compétences

Projet réalisé dans le cadre de la formation  
**Mastère Data Engineering & IA – EFREI Paris**

AISCA est une application d’aide à l’orientation professionnelle dans les métiers de la santé.  
Elle analyse des réponses en langage naturel à l’aide de modèles NLP (SBERT + IA générative) afin de :
- évaluer des compétences,
- calculer un score global,
- recommander des métiers,
- proposer un plan de progression personnalisé,
- générer un résumé automatique du profil.

---

##  Fonctionnalités principales

- Analyse sémantique des réponses utilisateur (SBERT)
- Scoring par blocs de compétences
- Score global de compatibilité
- Recommandation du **Top 3 métiers**
- Génération d’un **plan de progression**
- Génération d’un **résumé automatique (bio IA)**
- Interface utilisateur interactive avec **Streamlit**
- API backend en **FastAPI**

--

# Aller dans le frontend
cd frontend

# Lancer l'application Streamlit
streamlit run app.py

# Aller dans le backend
cd backend

# Lancer l'API FastAPI
uvicorn main:app --reload
