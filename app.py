import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="Dashboard Clustering Kasus Kekerasan Perempuan Dewasa (1)",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

@st.cache_data
def load_data():
    return pd.read_csv("dataset/hasil_clustering.csv")
    #return X
df = load_data()

# ======================
# SIDEBAR
# ======================

st.sidebar.title("Filter Data")

tahun = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["Tahun"].unique()),
    default=sorted(df["Tahun"].unique())
)

cluster = st.sidebar.multiselect(
    "Pilih Cluster",
    options=sorted(df["Cluster_Label"].unique()),
    default=sorted(df["Cluster_Label"].unique())
)

filtered_df = df[
    (df["Tahun"].isin(tahun)) &
    (df["Cluster_Label"].isin(cluster))
]

# ======================
# HEADER
# ======================

st.title("📊 Dashboard Clustering Kasus Kekerasan Anak (1)")

st.markdown("""
Dashboard ini menampilkan hasil analisis clustering kasus kekerasan anak berdasarkan beberapa kategori kasus.
""")

# ======================
# KPI
# ======================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Jumlah Data",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Jumlah Provinsi",
        filtered_df["Provinsi"].nunique()
    )

with col3:
    st.metric(
        "Jumlah Tahun",
        filtered_df["Tahun"].nunique()
    )

with col4:
    st.metric(
        "Jumlah Cluster",
        filtered_df["Cluster"].nunique()
    )

st.divider()

# ======================
# DISTRIBUSI CLUSTER
# ======================

st.subheader("Distribusi Cluster")

cluster_count = (
    filtered_df.groupby("Cluster_Label")
    .size()
    .reset_index(name="Jumlah")
)

fig_cluster = px.bar(
    cluster_count,
    x="Cluster_Label",
    y="Jumlah",
    text="Jumlah",
    title="Jumlah Data pada Setiap Cluster"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

# ======================
# TOTAL KASUS
# ======================

st.subheader("Total Kasus per Provinsi")

filtered_df["Total_Kasus"] = (
    filtered_df["Fisik"] +
    filtered_df["Psikis"] +
    filtered_df["Seksual"] +
    filtered_df["Eksploitasi"] +
    filtered_df["TPPO"] +
    filtered_df["Penelantaran"]
)

provinsi_total = (
    filtered_df.groupby("Provinsi")["Total_Kasus"]
    .sum()
    .reset_index()
)

fig_prov = px.bar(
    provinsi_total,
    x="Provinsi",
    y="Total_Kasus",
    title="Total Kasus per Provinsi"
)

st.plotly_chart(
    fig_prov,
    use_container_width=True
)

# ======================
# PROFIL CLUSTER
# ======================

st.subheader("Profil Cluster")

cluster_profile = (
    filtered_df.groupby("Cluster_Label")[
        [
            "Fisik",
            "Psikis",
            "Seksual",
            "Eksploitasi",
            "TPPO",
            "Penelantaran"
        ]
    ]
    .mean()
    .reset_index()
)

st.dataframe(
    cluster_profile,
    use_container_width=True
)

# ======================
# HEATMAP
# ======================

st.subheader("Heatmap Karakteristik Cluster")

heatmap_data = cluster_profile.set_index("Cluster_Label")

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Rata-rata Karakteristik Tiap Cluster"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ======================
# DATASET
# ======================

st.subheader("Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)