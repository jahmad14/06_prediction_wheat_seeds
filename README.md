# Déploiement — Segmentation des graines de blé (Wheat Seeds)

Application interactive développée avec **Streamlit** pour classifier une nouvelle observation de graine de blé dans l'un des 2 groupes morphologiques identifiés par la **Classification Ascendante Hiérarchique (CAH)**.

---

## 1. Modèle & Méthodologie

- **Modèle retenu :** `AgglomerativeClustering(n_clusters=2, linkage='average')` (`modele_cah.joblib`), sélectionné selon la Formulation B (classification exhaustive à 100 %, sans rejet, avec un score de silhouette de **0.506**).
- **Affectation de nouvelles observations :**
  - La CAH ne disposant pas d'une méthode `.predict()` native, les centroïdes des 2 groupes ont été calculés sur l'ensemble d'apprentissage.
  - Toute nouvelle graine est affectée au cluster dont le centroïde est le plus proche au sens de la distance euclidienne.
- **Variables explicatives (7 dimensions) :** `['area A', 'perimeter', 'compactness', 'length of kernel', 'width of kernel', 'asymmetry coefficient', 'length of kernel groove']`.

---

## 2. Structure du dossier

```text
Deployment/
├── app.py              # Interface utilisateur Streamlit
├── modele_cah.joblib   # Modèle CAH, centroïdes et labels d'apprentissage
├── requirements.txt    # Dépendances exactes (sans xgboost)
├── test_app.py         # Tests unitaires automatisés avec AppTest
└── README.md           # Documentation du projet
```

---

## 3. Installation et exécution

```bash
pip install -r requirements.txt
streamlit run app.py
```
