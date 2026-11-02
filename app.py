"""
app.py - Antarmuka Streamlit (kerangka untuk Pertemuan 13).
Jalankan: streamlit run src/app.py
"""
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from fuzzy_engine import infer, interpret, INPUT_MF, OUTPUT_MF

st.set_page_config(page_title="Fuzzy Seleksi Mahasiswa Baru", layout="wide")
st.title("SPK Fuzzy: Skor Akhir Seleksi Penerimaan Mahasiswa Baru")

col1, col2 = st.columns(2)
tes = col1.slider("Nilai Tes Seleksi (0-100)", 0, 100, 70)
rapor = col2.slider("Rata-rata Nilai Rapor (0-100)", 0, 100, 75)

if st.button("Hitung"):
    try:
        h = infer(tes, rapor)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    st.metric("Skor Akhir", f"{h['skor']:.2f}", h["kategori"])
    st.text(interpret(h))

    x = np.linspace(0, 100, 501)
    fig, ax = plt.subplots(figsize=(7, 3))
    for nama, f in OUTPUT_MF.items():
        ax.plot(x, f(x), "--", label=nama)
    ax.fill_between(h["z"], h["agregasi"], alpha=0.4, color="orange", label="Agregasi")
    ax.axvline(h["skor"], color="red", label=f"Centroid={h['skor']:.1f}")
    ax.legend(); ax.set_xlabel("Skor"); ax.set_ylabel("Derajat keanggotaan")
    st.pyplot(fig)
