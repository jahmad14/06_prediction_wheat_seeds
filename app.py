"""
Application Streamlit — Segmentation de graines de blé (Clustering Doc 1 - Wheat Seeds)
Modèle retenu : Classification Ascendante Hiérarchique (CAH, linkage='average', k=2)
Lancement en local : streamlit run app.py
"""

import os
import joblib
import numpy as np
import streamlit as st

# ----------------------------------------------------------------------
# Configuration de la page
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Wheat Seeds Clustering",
    page_icon="🌾",
    layout="centered",
)

DESCRIPTION = (
    "Cette application permet d'affecter une graine de blé à l'un des 2 groupes morphologiques "
    "identifiés par la Classification Ascendante Hiérarchique (CAH, liaison moyenne, k=2) à partir "
    "de ses 7 caractéristiques géométriques.\n\n"
    "**Note méthodologique** : La CAH (`AgglomerativeClustering`) ne disposant pas de méthode "
    "`predict()` native pour de nouvelles données, l'affectation est réalisée en calculant la distance "
    "euclidienne aux centroïdes des 2 clusters appris sur le jeu de données d'origine."
)

# ----------------------------------------------------------------------
# Chargement des artefacts (mis en cache)
# ----------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    base_dir = os.path.dirname(__file__)
    artefacts = joblib.load(os.path.join(base_dir, "modele_cah.joblib"))
    return artefacts


artefacts = load_artifacts()
centroids = artefacts["centroids"]
feature_names = artefacts["colonnes"]
noms_clusters = artefacts["noms_clusters"]

# ----------------------------------------------------------------------
# Fonction de prédiction (affectation au centroïde le plus proche)
# ----------------------------------------------------------------------
def predict_seed_cluster(area, perimeter, compactness, length_k, width_k, asym, groove):
    raw_vector = np.array([area, perimeter, compactness, length_k, width_k, asym, groove])
    
    # Distance euclidienne à chaque centroïde
    dist_c0 = float(np.linalg.norm(raw_vector - centroids[0]))
    dist_c1 = float(np.linalg.norm(raw_vector - centroids[1]))
    
    assigned_cluster = 0 if dist_c0 < dist_c1 else 1
    return assigned_cluster, dist_c0, dist_c1


# ----------------------------------------------------------------------
# Interface utilisateur
# ----------------------------------------------------------------------
st.title("🌾 Wheat Seeds Clustering (CAH)")
st.write(DESCRIPTION)

with st.form("form_seeds_clustering"):
    st.subheader("Caractéristiques géométriques de la graine")

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Surface de la graine (Area A)", min_value=9.0, max_value=25.0, value=14.86, step=0.1, format="%.2f")
        perimeter = st.number_input("Périmètre (Perimeter P)", min_value=11.0, max_value=20.0, value=14.57, step=0.1, format="%.2f")
        compactness = st.number_input("Compacité (Compactness C = 4*pi*A/P^2)", min_value=0.70, max_value=0.98, value=0.871, step=0.005, format="%.3f")
        length_k = st.number_input("Longueur du grain (Length of kernel)", min_value=3.5, max_value=7.5, value=5.63, step=0.05, format="%.2f")

    with col2:
        width_k = st.number_input("Largeur du grain (Width of kernel)", min_value=2.0, max_value=5.0, value=3.26, step=0.05, format="%.2f")
        asym = st.number_input("Coefficient d'asymétrie (Asymmetry coefficient)", min_value=0.5, max_value=10.0, value=2.71, step=0.1, format="%.2f")
        groove = st.number_input("Longueur du sillon (Length of kernel groove)", min_value=3.5, max_value=7.5, value=5.13, step=0.05, format="%.2f")

    submit_btn = st.form_submit_button("Classifier la graine", type="primary")

if submit_btn:
    try:
        cluster_id, d0, d1 = predict_seed_cluster(area, perimeter, compactness, length_k, width_k, asym, groove)
        cluster_desc = noms_clusters[cluster_id]

        if cluster_id == 0:
            st.info(f"🌾 **Cluster attribué : {cluster_desc}**")
        else:
            st.success(f"🌾 **Cluster attribué : {cluster_desc}**")

        st.write("### Proximité géométrique avec les centroïdes CAH :")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.metric(label="Distance au Centroïde 0 (Petit gabarit)", value=f"{d0:.2f}")
        with col_d2:
            st.metric(label="Distance au Centroïde 1 (Grand gabarit)", value=f"{d1:.2f}")
    except Exception as e:
        st.error(f"Erreur lors de l'affectation : {e}")
