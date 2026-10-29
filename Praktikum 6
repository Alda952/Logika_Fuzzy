class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator='AND'):
        self.rule_id = rule_id          
        self.antecedent = antecedent    
        self.consequent = consequent   
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        """Hitung alpha: gabungan derajat keanggotaan semua syarat IF."""
        nilai_derajat = []
        for var_nama, label_nama in self.antecedent.items():
            deg = derajat_fuzzifikasi[var_nama].get(label_nama, 0.0)
            nilai_derajat.append(deg)

        if not nilai_derajat:
            return 0.0

        if self.operator == 'AND':
            return min(nilai_derajat)
        elif self.operator == 'OR':
            return max(nilai_derajat)
        else:
            raise ValueError(f"Operator {self.operator} tidak dikenali.")

    def __str__(self):
        syarat = f" {self.operator} ".join(
            [f"{var} is {lbl}" for var, lbl in self.antecedent.items()])
        hasil = ", ".join(
            [f"{var} is {lbl}" for var, lbl in self.consequent.items()])
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"

rule_base = [
    FuzzyRule("R1", {"rapor": "Rendah", "tes_tulis": "Rendah"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R2", {"rapor": "Rendah", "tes_tulis": "Sedang"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R3", {"rapor": "Rendah", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R4", {"rapor": "Sedang", "tes_tulis": "Rendah"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R5", {"rapor": "Sedang", "tes_tulis": "Sedang"}, {"nilai_akhir": "Sedang"}),
    FuzzyRule("R6", {"rapor": "Sedang", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Tinggi"}),
    FuzzyRule("R7", {"rapor": "Tinggi", "tes_tulis": "Rendah"}, {"nilai_akhir": "Sedang"}),
    FuzzyRule("R8", {"rapor": "Tinggi", "tes_tulis": "Sedang"}, {"nilai_akhir": "Tinggi"}),
    FuzzyRule("R9", {"rapor": "Tinggi", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Tinggi"}),
]

def mu(tipe, p, x):
    if tipe == "L":
        b, c = p
        return 1.0 if x <= b else 0.0 if x >= c else (c - x) / (c - b)
    if tipe == "T":
        a, b, c = p
        if x <= a or x >= c: return 0.0
        return (x - a) / (b - a) if x <= b else (c - x) / (c - b)
    if tipe == "R":
        a, b = p
        return 0.0 if x <= a else 1.0 if x >= b else (x - a) / (b - a)


himpunan_input = {   
    "rapor": {"Rendah": ("L", (55, 65)),
              "Sedang": ("T", (60, 72, 85)),
              "Tinggi": ("R", (75, 88))},
    "tes_tulis": {"Rendah": ("L", (50, 60)),
                  "Sedang": ("T", (55, 75, 85)),
                  "Tinggi": ("R", (75, 88))},
}


def nilai_ke_derajat(rapor, tes_tulis):
    crisp = {"rapor": rapor, "tes_tulis": tes_tulis}
    return {var: {lbl: round(mu(tp, pr, crisp[var]), 4)
                  for lbl, (tp, pr) in himpunan_input[var].items()}
            for var in crisp}

def evaluasi_aturan(derajat_input, judul="HASIL EVALUASI BASIS ATURAN FUZZY"):
    print("=" * 86)
    print(judul)
    print("=" * 86)

    aturan_aktif = []
    for rule in rule_base:
        alpha = rule.hitung_firing_strength(derajat_input)
        out_var = list(rule.consequent.keys())[0]
        out_lbl = rule.consequent[out_var]
        status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
        print(f"{rule} --> {status}")
        if alpha > 0:
            aturan_aktif.append((rule.rule_id, out_lbl, alpha))

    print("\n" + "=" * 86)
    print("RINGKASAN ATURAN YANG TERPICU (FIRING RULES):")
    print("=" * 86)
    for r_id, konklusi, alpha in aturan_aktif:
        print(f" - {r_id:<4}: Nilai Akhir = {konklusi:<8} dengan alpha = {alpha:.2f}")
    if not aturan_aktif:
        print(" Tidak ada aturan yang terpicu. Periksa kelengkapan rule base "
              "dan fungsi keanggotaan.")
    return aturan_aktif

if __name__ == "__main__":
    derajat_praktikum = {
        "rapor":     {"Rendah": 0.0, "Sedang": 0.5,  "Tinggi": 0.5},
        "tes_tulis": {"Rendah": 0.0, "Sedang": 0.75, "Tinggi": 0.25},
    }
    evaluasi_aturan(derajat_praktikum, "HASIL EVALUASI BASIS ATURAN FUZZY - NILAI AKHIR SELEKSI MAHASISWA BARU")

    # Cara 2: nilai asli pelamar (data jurnal 071-0003)
    print()
    derajat_nyata = nilai_ke_derajat(rapor=79.52, tes_tulis=80)
    evaluasi_aturan(derajat_nyata, "HASIL EVALUASI BASIS ATURAN FUZZY - DATA NYATA (rapor 79.52, tes tulis 80)")
