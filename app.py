import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# KONFIGURASI DASHBOARD
# ===============================
st.set_page_config(
    page_title="Dashboard Computational Thinking",
    layout="wide"
)

st.title("🧠 Dashboard Computational Thinking Berbasis Data Iklim & DSS")
st.markdown("---")

# ===============================
# LOAD DATA
# ===============================
uploaded_file = st.file_uploader(
    "Unggah data skor CT (Excel / CSV)",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data berhasil dimuat!")

    # ===============================
    # METRIK UTAMA
    # ===============================
    mean_ct = df.mean().mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Jumlah Responden", df.shape[0])
    col2.metric("🧠 Dimensi CT", df.shape[1])
    col3.metric("📊 Skala", "1 – 5")
    col4.metric("⭐ Mean CT", f"{mean_ct:.2f}")

    st.markdown("---")

    # ===============================
    # SECTION 1: MEAN CT TOTAL
    # ===============================
    st.subheader("📊 Skor Rata-rata Computational Thinking")

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["Mean CT"], [mean_ct])
    ax.set_ylim(1, 5)
    ax.set_ylabel("Skor")
    ax.set_title("Rata-rata CT Keseluruhan")
    st.pyplot(fig)

    st.markdown(
        "📌 **Interpretasi:** Kemampuan berpikir komputasi responden berada pada kategori baik hingga sangat baik."
    )

    st.markdown("---")

    # ===============================
    # SECTION 2: PER DIMENSI
    # ===============================
    st.subheader("📌 Perbandingan Antar Dimensi CT")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df.columns, df.mean())
    ax.set_ylim(1, 5)
    ax.set_ylabel("Skor Rata-rata")
    ax.set_title("Rata-rata Skor per Dimensi CT")
    plt.xticks(rotation=30)
    st.pyplot(fig)

    st.markdown("---")

    # ===============================
    # SECTION 3: HEATMAP
    # ===============================
    st.subheader("🟥 Distribusi Skor Responden (Heatmap)")

    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.imshow(
        df.values,
        cmap="RdYlGn",
        aspect="auto",
        vmin=1,
        vmax=5
    )

    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=30)
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels([f"R{i+1}" for i in range(len(df))])

    plt.colorbar(heatmap, ax=ax, label="Skor (1–5)")
    ax.set_title("Heatmap Skor Responden")
    st.pyplot(fig)

    st.markdown("---")

    # ===============================
    # SECTION 4: KORELASI
    # ===============================
    st.subheader("🟦 Korelasi Antar Dimensi CT")

    corr = df.corr()

    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=30)
    ax.set_yticklabels(corr.index)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center")

    plt.colorbar(cax, ax=ax, label="Korelasi")
    ax.set_title("Matriks Korelasi CT")
    st.pyplot(fig)

    st.markdown("---")

    # ===============================
    # SECTION 5: PROFIL INDIVIDU
    # ===============================
    st.subheader("🟩 Profil Individu Responden (Radar Chart)")

    idx = st.slider(
        "Pilih Responden",
        1,
        len(df),
        1
    ) - 1

    values = df.iloc[idx].values
    labels = df.columns.tolist()

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    values = np.concatenate([values, [values[0]]])
    angles = np.concatenate([angles, [angles[0]]])

    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_thetagrids(angles[:-1]*180/np.pi, labels)
    ax.set_ylim(1, 5)
    ax.set_title(f"Profil CT Responden {idx+1}", pad=20)

    st.pyplot(fig)

    st.markdown("---")

    # ===============================
    # SECTION 6: RINGKASAN DASHBOARD
    # ===============================
    st.subheader("🟪 Ringkasan Visual Hasil")

    fig, axs = plt.subplots(1, 3, figsize=(14, 4))

    axs[0].bar(["Mean CT"], [mean_ct])
    axs[0].set_ylim(1, 5)
    axs[0].set_title("CT Total")

    axs[1].bar(df.columns, df.mean())
    axs[1].set_ylim(1, 5)
    axs[1].set_title("Per Dimensi")
    axs[1].tick_params(axis='x', rotation=30)

    axs[2].boxplot(df.values, labels=df.columns)
    axs[2].set_ylim(1, 5)
    axs[2].set_title("Sebaran Skor")
    axs[2].tick_params(axis='x', rotation=30)

    st.pyplot(fig)

else:
    st.info("Silakan unggah file data untuk memulai dashboard.")
