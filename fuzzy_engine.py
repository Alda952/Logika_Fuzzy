"""
fuzzy_engine.py
Core Engine sistem fuzzy Mamdani (Max-Min) + defuzzifikasi Centroid.
Kasus: Penentuan Skor Akhir Seleksi Penerimaan Mahasiswa Baru.
Modul ini TIDAK bergantung pada UI (Streamlit) sehingga mudah diuji dan dipanggil ulang.
"""
import numpy as np

_trapz = getattr(np, "trapezoid", None) or np.trapz  # kompatibel NumPy 1.x dan 2.x

# ---------- Semesta pembicaraan ----------
UNIVERSE = {
    "tes": (0, 100),     # Nilai Tes Seleksi
    "rapor": (0, 100),   # Rata-rata Nilai Rapor
    "skor": (0, 100),    # Skor Akhir Seleksi (output)
}

# ---------- Fungsi keanggotaan ----------
def trimf(x, a, b, c):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        left = np.where(b != a, (x - a) / (b - a), (x >= b).astype(float))
        right = np.where(c != b, (c - x) / (c - b), (x <= b).astype(float))
    return np.clip(np.minimum(left, right), 0.0, 1.0)

def trapmf(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        left = np.where(b != a, (x - a) / (b - a), (x >= b).astype(float))
        right = np.where(d != c, (d - x) / (d - c), (x <= c).astype(float))
    return np.clip(np.minimum(np.minimum(left, 1.0), right), 0.0, 1.0)

INPUT_MF = {
    "Rendah": lambda x: trapmf(x, 0, 0, 40, 60),
    "Sedang": lambda x: trimf(x, 40, 60, 80),
    "Tinggi": lambda x: trapmf(x, 60, 80, 100, 100),
}
OUTPUT_MF = {
    "Rendah": lambda x: trapmf(x, 0, 0, 25, 50),
    "Sedang": lambda x: trimf(x, 25, 50, 75),
    "Tinggi": lambda x: trapmf(x, 50, 75, 100, 100),
}

# ---------- Basis aturan (Tes, Rapor) -> Skor ----------
RULES = [
    ("Rendah", "Rendah", "Rendah"),
    ("Rendah", "Sedang", "Rendah"),
    ("Rendah", "Tinggi", "Sedang"),
    ("Sedang", "Rendah", "Rendah"),
    ("Sedang", "Sedang", "Sedang"),
    ("Sedang", "Tinggi", "Tinggi"),
    ("Tinggi", "Rendah", "Sedang"),
    ("Tinggi", "Sedang", "Tinggi"),
    ("Tinggi", "Tinggi", "Tinggi"),
]

def validate(tes, rapor):
    for nama, v in (("Nilai Tes", tes), ("Nilai Rapor", rapor)):
        if v is None or not isinstance(v, (int, float, np.number)) or np.isnan(v):
            raise ValueError(f"{nama} harus berupa angka.")
        if not 0 <= v <= 100:
            raise ValueError(f"{nama} harus berada pada rentang 0-100 (diterima: {v}).")

def fuzzify(tes, rapor):
    return (
        {k: float(f(tes)) for k, f in INPUT_MF.items()},
        {k: float(f(rapor)) for k, f in INPUT_MF.items()},
    )

def evaluate_rules(mu_tes, mu_rapor):
    """Operator AND = min. Mengembalikan daftar (aturan, firing strength)."""
    return [((t, r, o), min(mu_tes[t], mu_rapor[r])) for t, r, o in RULES]

def aggregate(fired, z):
    """Implikasi Min (clipping) + agregasi Max."""
    agg = np.zeros_like(z, dtype=float)
    for (_, _, out), alpha in fired:
        agg = np.maximum(agg, np.minimum(alpha, OUTPUT_MF[out](z)))
    return agg

def defuzzify_centroid(z, agg):
    area = _trapz(agg, z)
    if area == 0:
        return 0.0
    return float(_trapz(agg * z, z) / area)

def kategori(skor):
    if skor >= 70:
        return "Layak Diterima"
    if skor >= 50:
        return "Dipertimbangkan"
    return "Belum Layak"

def infer(tes, rapor, resolution=1001):
    """Pipeline lengkap. Mengembalikan dict hasil + data untuk visualisasi."""
    validate(tes, rapor)
    mu_tes, mu_rapor = fuzzify(tes, rapor)
    fired = evaluate_rules(mu_tes, mu_rapor)
    z = np.linspace(*UNIVERSE["skor"], resolution)
    agg = aggregate(fired, z)
    skor = defuzzify_centroid(z, agg)
    return {
        "mu_tes": mu_tes,
        "mu_rapor": mu_rapor,
        "firing": [(f"IF Tes={t} AND Rapor={r} THEN Skor={o}", a) for (t, r, o), a in fired],
        "z": z,
        "agregasi": agg,
        "skor": skor,
        "kategori": kategori(skor),
    }

def interpret(hasil):
    aktif = [(r, a) for r, a in hasil["firing"] if a > 0]
    teks = [f"Skor akhir seleksi = {hasil['skor']:.2f} -> {hasil['kategori']}.",
            f"{len(aktif)} aturan aktif:"]
    teks += [f"- {r} (alpha={a:.2f})" for r, a in aktif]
    return "\n".join(teks)

if __name__ == "__main__":
    h = infer(75, 82)
    print(interpret(h))
