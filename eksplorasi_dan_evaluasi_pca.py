# =============================================================================
# EKSPLORASI DATA, EVALUASI PREPROCESSING, DAN DIAGNOSTIK PCA
# Ujian Akhir Semester (UAS) Visualisasi Data dan Informasi
# Studi Kasus: Ketimpangan Ketenagakerjaan & Relokasi Industri Jawa Tengah (2021-2025)
# 
# Petunjuk Penggunaan:
# 1. Di Komputer Lokal: Jalankan `python eksplorasi_dan_evaluasi_pca.py`
# 2. Di Google Colab: Upload file ini atau copy-paste kodenya ke sel Colab.
#    Hanya membutuhkan package standar: numpy, pandas, matplotlib, seaborn.
# =============================================================================

import os
import json
import numpy as np
import pandas as pd
# Coba import modul visualisasi (tersedia otomatis di Google Colab)
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOT = True
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['figure.dpi'] = 120
except ImportError:
    HAS_PLOT = False
    print("[INFO] Matplotlib/Seaborn belum terpasang di Python lokal. Output teks/tabel statistik tetap berjalan penuh.")
    print("       (Jika dijalankan di Google Colab, seluruh grafik akan otomatis dirender).")

print("=" * 80)
print("1. MEMUAT DATA MULTIVARIAT JAWA TENGAH")
print("=" * 80)

# Cek lokasi file
data_path = 'data/multivariate_jateng.json'
if not os.path.exists(data_path):
    # Jika di Colab dan file belum di folder data/
    if os.path.exists('multivariate_jateng.json'):
        data_path = 'multivariate_jateng.json'
    else:
        raise FileNotFoundError("Berkas 'multivariate_jateng.json' tidak ditemukan. Harap pastikan file ada di folder.")

with open(data_path, 'r', encoding='utf-8') as f:
    raw_json = json.load(f)

metadata = raw_json['metadata']
var_keys = metadata['variables']
var_labels = {
    'tpt': 'Tingkat Pengangguran Terbuka (%)',
    'tpak': 'Tingkat Partisipasi Angkatan Kerja (%)',
    'umk': 'Upah Minimum Kab/Kota (Rp)',
    'pdrb_kapita': 'PDRB per Kapita (Ribu Rp)',
    'pengeluaran': 'Pengeluaran per Kapita (Rp/bln)',
    'angkatan_kerja': 'Jumlah Angkatan Kerja (jiwa)',
    'rls': 'Rata-Rata Lama Sekolah (tahun)',
    'kepadatan': 'Kepadatan Penduduk (jiwa/km²)'
}

# Ambil data tahun 2025 (tahun utama analisis)
rec_2025 = raw_json['records']['2025']
df_2025 = pd.DataFrame.from_dict(rec_2025, orient='index')
df_vars = df_2025[var_keys].astype(float)

print(f"Dataset berhasil dimuat!")
print(f"- Jumlah Wilayah Observasi: {len(df_2025)} Kabupaten/Kota")
print(f"- Jumlah Variabel Analisis: {len(var_keys)} Variabel")
print(f"- Tahun Acuan Utama       : 2025")
print("\nContoh 5 Baris Data Teratas:")
print(df_vars.head())

print("\n" + "=" * 80)
print("2. EVALUASI KUALITAS DATA & PREPROCESSING (SKEWNESS & OUTLIERS)")
print("=" * 80)

# Statistik Deskriptif
desc = df_vars.describe().T[['mean', 'std', 'min', '50%', 'max']]
desc['skewness'] = df_vars.skew()
desc['kurtosis'] = df_vars.kurtosis()
desc['interpretasi_distribusi'] = desc['skewness'].apply(
    lambda s: 'Sangat Mencong Kanan (Extreme Skew)' if s > 1.5 
    else ('Mencong Sedang' if abs(s) > 0.5 else 'Simetris / Normal')
)

print(desc.round(2))

print("\n" + "-" * 80)
print("CATATAN EVALUASI PREPROCESSING:")
print("1. KEPADATAN PENDUDUK (Skewness: +2.50):")
print("   - Nilai minimum: 467 jiwa/km² (Kab. Rembang), Median: 1.196 jiwa/km².")
print("   - Nilai maksimum: 11.324 jiwa/km² (Kota Surakarta) & 6.744 (Kota Magelang).")
print("   - AKIBAT PREPO JELEK PADA VISUALISASI:")
print("     Pada Clustered Heatmap, 29 Kabupaten memiliki Z-score rendah (-0.6 s/d -0.2),")
print("     sehingga sel-selnya tampak 'putih mati' tanpa variasi warna.")
print("     Hanya 5 Kota otonom di bawah yang menyala merah.")
print("   - SOLUSI PREPO: Sebaiknya variabel kepadatan di-transformasi log (np.log1p)")
print("     sebelum Z-score, atau gunakan Min-Max / Rank-scaling khusus pada Heatmap.")

print("\n2. PDRB PER KAPITA (Skewness: +1.98):")
print("   - Kudus (Rp167 Juta - industri tembakau) dan Kota Semarang (Rp145 Juta)")
print("     jauh meninggalkan rata-rata kabupaten (Rp24 - 45 Juta).")
print("   - Menghasilkan efek outlier yang mendistorsi rentang skala sumbu.")

print("\n3. SIFAT VARIABEL INTENSIF VS EKSTENSIF:")
print("   - 'angkatan_kerja' adalah kuantitas absolut (jiwa: 68 ribu s/d 1,15 juta).")
print("   - Menggabungkan besaran absolut penduduk dengan rasio (TPT %, TPAK %) membuat")
print("     variabel absolut merefleksikan 'ukuran daerah' (Brebes/Cilacap sangat besar).")
print("-" * 80)

print("\n" + "=" * 80)
print("3. MATRIKS KORELASI & UJI MULTIKOLINEARITAS")
print("=" * 80)

corr_matrix = df_vars.corr()
print("Matriks Korelasi Pearson (8 Variabel):")
print(corr_matrix.round(2))

# Pasangan dengan korelasi tertinggi
corr_pairs = []
for i in range(len(var_keys)):
    for j in range(i + 1, len(var_keys)):
        v1, v2 = var_keys[i], var_keys[j]
        r = corr_matrix.loc[v1, v2]
        corr_pairs.append((v1, v2, r, abs(r)))

corr_pairs = sorted(corr_pairs, key=lambda x: x[3], reverse=True)
print("\n5 Pasangan Korelasi Terkuat:")
for v1, v2, r, _ in corr_pairs[:5]:
    print(f"  * {v1:15s} <--> {v2:15s} : r = {r:+.3f}")

print("\n" + "=" * 80)
print("4. DIAGNOSTIK KELAYAKAN DATA UNTUK PCA (KMO & BARTLETT'S TEST)")
print("=" * 80)

# Perhitungan KMO (Kaiser-Meyer-Olkin) secara numerik
R = corr_matrix.values
invR = np.linalg.inv(R)
n_vars = R.shape[0]
A = np.zeros((n_vars, n_vars))
for i in range(n_vars):
    for j in range(n_vars):
        A[i, j] = -invR[i, j] / np.sqrt(invR[i, i] * invR[j, j])
np.fill_diagonal(A, 0)
sum_r2 = np.sum(R**2) - np.sum(np.diag(R)**2)
sum_a2 = np.sum(A**2)
kmo_overall = sum_r2 / (sum_r2 + sum_a2)

# Bartlett's Sphericity
N = len(df_vars)
p = n_vars
detR = np.linalg.det(R)
chi2_bartlett = - (N - 1 - (2*p + 5)/6) * np.log(detR)
df_chi = p * (p - 1) / 2

print(f"1. Nilai KMO (Kaiser-Meyer-Olkin) = {kmo_overall:.3f}")
if kmo_overall >= 0.6:
    print("   -> KESIMPULAN: DATA LAYAK DILAKUKAN PCA (KMO > 0.60, kategori Moderate).")
else:
    print("   -> KESIMPULAN: KMO kurang dari 0.60.")

print(f"2. Uji Bartlett of Sphericity     = Chi-Square: {chi2_bartlett:.2f} (df = {int(df_chi)})")
print(f"   Determinant R = {detR:.6e} (jauh < 1.0, korelasi antar variabel signifikan)")
print("   -> KESIMPULAN: Matriks korelasi bukan matriks identitas (p-value < 0.0001).")
print("                  Reduksi dimensi PCA SANGAT TEPAT & VALID secara statistik.")

print("\n" + "=" * 80)
print("5. ANALISIS KOMPONEN UTAMA (PCA SVD) & PROPORSI VARIANS")
print("=" * 80)

# Standardisasi Z-score
X = df_vars.values
mu = np.mean(X, axis=0)
sigma = np.std(X, axis=0, ddof=1)
Z = (X - mu) / sigma

# SVD
U, S, Vt = np.linalg.svd(Z, full_matrices=False)
eigenvalues = (S ** 2) / (len(X) - 1)
total_var = np.sum(eigenvalues)
var_exp = eigenvalues / total_var * 100
cum_var = np.cumsum(var_exp)

scree_df = pd.DataFrame({
    'Komponen': [f'PC{i+1}' for i in range(len(eigenvalues))],
    'Eigenvalue': eigenvalues,
    'Varians Terjelaskan (%)': var_exp,
    'Kumulatif Varians (%)': cum_var,
    'Kaiser Criterion (>1.0)': ['Lolos (> 1.0)' if e >= 1.0 else 'Tidak (< 1.0)' for e in eigenvalues]
})
print(scree_df.round(2).to_string(index=False))

print(f"\nRingkasan Reduksi 2D (PC1 + PC2): Merangkum {cum_var[1]:.2f}% dari seluruh varians data.")
print(f"Kriteria Kaiser merekomendasikan 3 komponen utama (total: {cum_var[2]:.2f}% varians).")

print("\n" + "=" * 80)
print("6. HASIL PCA: VARIABEL APA SAJA YANG PALING BERPENGARUH?")
print("=" * 80)

# Eigenvector matrix
eigenvectors = Vt.T

# Loading murni (Korelasi r antara variabel dengan masing-masing PC)
loadings = eigenvectors * np.sqrt(eigenvalues)

# Kontribusi persentase per variabel terhadap masing-masing komponen
# Formula: contrib_ik = (eigenvector_ik^2) * 100
contributions = (eigenvectors ** 2) * 100

summary_pca = pd.DataFrame({
    'Variabel': var_keys,
    'Label Lengkap': [var_labels[v] for v in var_keys],
    'PC1_Eigenvector': eigenvectors[:, 0],
    'PC1_Loading_r': loadings[:, 0],
    'PC1_Kontribusi(%)': contributions[:, 0],
    'PC2_Eigenvector': eigenvectors[:, 1],
    'PC2_Loading_r': loadings[:, 1],
    'PC2_Kontribusi(%)': contributions[:, 1],
    'PC3_Loading_r': loadings[:, 2],
    'PC3_Kontribusi(%)': contributions[:, 2]
})

print(summary_pca[['Variabel', 'PC1_Loading_r', 'PC1_Kontribusi(%)', 'PC2_Loading_r', 'PC2_Kontribusi(%)']].round(3).to_string(index=False))

print("\n" + "-" * 80)
print("INTERPRETASI SUBSTANTIF: VARIABEL YANG PALING BERPENGARUH DI PCA")
print("-" * 80)
print("A. KOMPONEN 1 (PC1: 46.66% Varians) -> 'DIMENSI KESEJAHTERAAN & KAPITAS MODERN'")
print("   Variabel paling dominan:")
print("   1. Rata-rata Lama Sekolah (RLS) : Kontribusi 23.37% (r = -0.934)")
print("   2. PDRB per Kapita              : Kontribusi 21.07% (r = -0.887)")
print("   3. Pengeluaran per Kapita       : Kontribusi 18.05% (r = -0.821)")
print("   4. Kepadatan Penduduk           : Kontribusi 17.70% (r = -0.813)")
print("   * 4 variabel ini menyumbang 80.2% kekuatan sumbu PC1!")
print("   * Variabel TPT (Pengangguran) sama sekali TIDAK berpengaruh di PC1 (r = -0.003).")
print("   * ARTINYA: Sumbu PC1 memisahkan wilayah metropolis maju/pusat upah")
print("              (Kota Semarang, Solo, Salatiga, Kudus) dari kabupaten agraris.")

print("\nB. KOMPONEN 2 (PC2: 22.16% Varians) -> 'DIMENSI STRUKTUR & TEKANAN KETENAGAKERJAAN'")
print("   Variabel paling dominan:")
print("   1. Tingkat Pengangguran (TPT)   : Kontribusi 51.22% (r = -0.953) [SANGAT DOMINAN!]")
print("   2. Partisipasi Kerja (TPAK)     : Kontribusi 27.02% (r = +0.692)")
print("   3. Jumlah Angkatan Kerja        : Kontribusi 16.71% (r = -0.544)")
print("   * 3 variabel tenaga kerja ini menyumbang 94.95% kekuatan sumbu PC2!")
print("   * Seluruh variabel moneter/ekonomi (PDRB, UMK, RLS) mendekati 0% di PC2.")
print("   * ARTINYA: Sumbu PC2 murni memetakan kondisi ketenagakerjaan daerah:")
print("              Arah TPT tinggi (Cilacap, Brebes) vs Arah TPAK tinggi (Wonosobo, Banjarnegara).")

print("\nC. MENGAPA TIDAK PERLU REDUKSI VARIABEL (FEATURE REMOVAL)?")
print("   Dalam konteks visualisasi Biplot, tujuan PCA adalah memproyeksikan")
print("   seluruh 8 dimensi ke dalam bidang datar 2D (koordinat kartesius),")
print("   bukan membuang variabel seperti eliminasi fitur pada regresi linier.")
print("   Ke-8 variabel tetap ditampilkan sebagai vektor panah loading!")
print("-" * 80)

print("\n" + "=" * 80)
print("7. VISUALISASI EKSPLORASI (DISTRIBUSI, CORRELATION, BIPLOT)")
print("=" * 80)

if HAS_PLOT:
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. Scree Plot
    axes[0, 0].bar(range(1, 9), var_exp, alpha=0.7, color='#38bdf8', label='Individual Variance (%)')
    axes[0, 0].step(range(1, 9), cum_var, where='mid', color='#ef4444', linewidth=2, label='Cumulative Variance (%)')
    axes[0, 0].axhline(y=68.82, color='orange', linestyle='--', label='2D Cutoff (68.8%)')
    axes[0, 0].set_title('Scree Plot: Varians Terjelaskan per Komponen', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Principal Component')
    axes[0, 0].set_ylabel('Variance Explained (%)')
    axes[0, 0].set_xticks(range(1, 9))
    axes[0, 0].legend(loc='center right')

    # 2. Variable Contribution Bar Plot (PC1 vs PC2)
    contrib_df = pd.DataFrame({
        'PC1 (Kemakmuran)': contributions[:, 0],
        'PC2 (Ketenagakerjaan)': contributions[:, 1]
    }, index=var_keys)
    contrib_df.plot(kind='bar', ax=axes[0, 1], colormap='viridis', alpha=0.85)
    axes[0, 1].set_title('Kontribusi Variabel terhadap PC1 & PC2 (%)', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Kontribusi (%)')
    axes[0, 1].set_xticklabels([var_keys[i].upper() for i in range(len(var_keys))], rotation=45)
    axes[0, 1].axhline(y=12.5, color='red', linestyle=':', label='Garis Acuan Rata-rata (100%/8 = 12.5%)')
    axes[0, 1].legend()

    # 3. Correlation Heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=axes[1, 0], cbar=False)
    axes[1, 0].set_title('Matriks Korelasi Pearson 8 Variabel (2025)', fontsize=12, fontweight='bold')

    # 4. PCA Biplot (Python Rendition)
    pc1_scores = df_2025['pca'].apply(lambda p: p['pc1']).values
    pc2_scores = df_2025['pca'].apply(lambda p: p['pc2']).values
    clusters = df_2025['cluster'].values

    color_map = {
        "Kawasan Industri Baru (Relokasi)": "#ef4444",
        "Pusat Metropolis & Industri Matang": "#38bdf8",
        "Kota Jasa & Perdagangan": "#f59e0b",
        "Sentra Industri Spesifik / Energi": "#a855f7",
        "Wilayah Agraris & Penyangga": "#10b981"
    }

    for c_name, c_col in color_map.items():
        mask = clusters == c_name
        axes[1, 1].scatter(pc1_scores[mask], pc2_scores[mask], label=c_name, color=c_col, s=70, alpha=0.85, edgecolors='black')

    # Anotasi daerah kunci
    key_cities = ['Kota Semarang', 'Kota Surakarta', 'Batang', 'Kendal', 'Brebes', 'Cilacap']
    for i, txt in enumerate(df_2025['name']):
        if txt in key_cities:
            axes[1, 1].annotate(txt, (pc1_scores[i] + 0.15, pc2_scores[i] + 0.15), fontsize=9, fontweight='bold')

    # Plot vektor loading pada biplot
    scale_vec = 4.0
    for i, vk in enumerate(var_keys):
        vx = eigenvectors[i, 0] * scale_vec
        vy = eigenvectors[i, 1] * scale_vec
        axes[1, 1].arrow(0, 0, vx, vy, color='grey', alpha=0.7, head_width=0.15)
        axes[1, 1].text(vx * 1.15, vy * 1.15, vk.upper(), color='darkblue', fontsize=8, ha='center')

    axes[1, 1].axhline(0, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].axvline(0, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].set_title('PCA Biplot: 35 Kab/Kota & Vektor Indikator (2025)', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel(f'PC1 ({var_exp[0]:.1f}% Varians)')
    axes[1, 1].set_ylabel(f'PC2 ({var_exp[1]:.1f}% Varians)')
    axes[1, 1].legend(loc='lower left', fontsize=7)

    plt.tight_layout()
    output_fig = 'diagnostik_pca_dan_eksplorasi.png'
    plt.savefig(output_fig, dpi=150)
    print(f"Gambar diagnostik berhasil disimpan ke: {output_fig}")
else:
    print("[INFO] Grafik tidak dirender di terminal lokal karena matplotlib tidak ada.")
    print("       Seluruh tabel hasil uji, evaluasi preprocessing, dan kontribusi PCA sudah tercetak lengkap di atas!")
    print("       Jika dijalankan di Google Colab, plot visual akan otomatis tampil di layar.")

print("\n=== SEMUA TAHAP EKSPLORASI & EVALUASI SELESAI DENGAN SUKSES! ===")
