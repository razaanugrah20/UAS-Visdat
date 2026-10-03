# Eksplorasi Ketimpangan Ketenagakerjaan dan Fenomena Relokasi Industri Jawa Tengah (2021–2025)

Proyek Akhir / Ujian Akhir Semester (UAS) Mata Kuliah **Visualisasi Data dan Informasi** (K203407)  
Program Studi Komputasi Statistik, Politeknik Statistika STIS — Semester Genap TA 2025/2026  
**Dosen Pengampu:** Siti Mariyah, Ph.D. & Farid Ridho, M.T.

---

## 📌 Ringkasan Eksekutif & Tema Riset

* **Tema Utama:** Ketimpangan Ketenagakerjaan dan Pengupahan Kabupaten/Kota.
* **Lokus Penelitian:** Nasional (±500 Kab/Kota) dan Fokus Utama Provinsi **Jawa Tengah (35 Kabupaten/Kota)**.
* **Narasi Substantif:**
  Dalam periode 2022–2025, terjadi gelombang relokasi industri padat karya (khususnya tekstil, garmen, dan alas kaki) dari kawasan industri berupah tinggi di Jabodetabek dan Jawa Barat (UMK > Rp5 Juta) menuju koridor pantai utara Jawa Tengah (Kendal, Batang, Brebes) dengan UMK berkisar Rp2,1 – 2,6 Juta. Dasbor ini memvisualisasikan bagaimana transformasi spasial dan multivariat ini terjadi serta implikasinya terhadap struktur serapan tenaga kerja sektoral.

---

## 📊 Pemenuhan Kriteria Soal & 3 Topik Visualisasi (Lampiran A)

Aplikasi mengintegrasikan **3 topik visualisasi data** yang saling terpadu:

### 1. Data Geospasial (Nasional, 507 Kabupaten/Kota)
* **Kepatuhan Kriteria:** Mencakup 507 unit kabupaten/kota se-Indonesia (> 500 unit).
* **Dua Representasi Peta Berbeda:**
  1. *Choropleth Map:* Mengkodekan **Tingkat Pengangguran Terbuka (TPT, %)** dengan klasifikasi bertingkat dan palet warna *Viridis* (ramah buta warna/colorblind-safe). Menggunakan rasio intensif (bukan angka absolut pengangguran) sesuai kaidah kartografi.
  2. *Proportional Symbol Map:* Mengkodekan besaran absolut **Jumlah Penduduk Bekerja (jiwa)** melalui ukuran radius lingkaran.
  3. *Combined Bivariate Layer:* Menampilkan kedua indikator secara simultan.
* **Interaktivitas:** Zoom, pan, filter pulau (Jawa, Sumatera, Kalimantan, Sulawesi, dsb.), dan tooltip kartu profil daerah komparatif.

### 2. Data Berdimensi Tinggi / Multivariat (35 Kab/Kota Jateng, 2021–2025)
* **Kepatuhan Kriteria:** 8 variabel numerik, 35 unit observasi (> 34 unit), deret waktu 5 tahun.
* **8 Variabel Terpilih:**
  1. `tpt`: Tingkat Pengangguran Terbuka (%)
  2. `tpak`: Tingkat Partisipasi Angkatan Kerja (%)
  3. `umk`: Upah Minimum Kabupaten/Kota (Rupiah)
  4. `pdrb_kapita`: PDRB per Kapita ADHB (Ribu Rupiah)
  5. `pengeluaran`: Rata-Rata Pengeluaran per Kapita sebulan (Rupiah)
  6. `angkatan_kerja`: Jumlah Angkatan Kerja (jiwa)
  7. `rls`: Rata-Rata Lama Sekolah (tahun)
  8. `kepadatan`: Kepadatan Penduduk (jiwa/km²)
* **Teknik Reduksi Dimensi:**
  * **PCA Biplot:** Mereduksi 8 variabel ke dalam 2 komponen utama (PC1 & PC2) yang merangkum **68.82% total varians** (PC1: 46.66%, PC2: 22.16%). Menampilkan vektor loading 8 arah variabel dan proyeksi skor 35 daerah.
* **Dua Teknik Visualisasi Tambahan:**
  * **Parallel Coordinates Plot (PCP):** 8 sumbu dimensi vertikal dengan fitur **Interactive Brushing**.
  * **Clustered Heatmap:** Matriks 35 kab/kota × 8 variabel (Z-score standardized) diurutkan berdasarkan skor PC1.
* **Brushing & Linking Antar Tampilan:** Menyorot (*hover*) atau memilih (*brush*) daerah pada salah satu grafik secara instan menyorot entitas yang sama pada kedua grafik lainnya.
* **Slider Waktu & Animasi:** Memutar trayektori perubahan dari tahun 2021 hingga 2025.

### 3. Data Berhierarki / Berjenjang (Jawa Tengah)
* **Kepatuhan Kriteria:** Struktur 3 level administratif & sektoral:
  $$\text{Provinsi Jawa Tengah} \longrightarrow \text{Eks-Karesidenan (6)} \longrightarrow \text{Kabupaten/Kota (35)} \longrightarrow \text{Sektor Lapangan Usaha (3)}$$
* **Dua Representasi Berbeda:**
  1. *Zoomable Squarified Treemap*
  2. *Concentric Sunburst Diagram*
* **Visual Encoding Ganda:**
  * **Ukuran (Size / Luas / Sudut):** Mengkodekan kuantitas absolut *Jumlah Penduduk Bekerja (jiwa)*.
  * **Warna (Color Ramp):** Mengkodekan indikator moneter *Upah Minimum (UMK)* atau *Pengeluaran per Kapita*.
* **Interaktivitas:** Fitur *Drill-down* interaktif dengan *Breadcrumb Navigation* penunjuk posisi hierarki.

---

## 🗂️ Struktur Direktori Repositori

```text
├── WebStory.html                    # Berkas Utama Laman Web Visualisasi Data (Single Page App)
├── README.md                        # Dokumentasi Lengkap Proyek & Metodologi
├── [LapakGIS.com] Batas Wilayah Kabupaten 2024/ # Shapefile Resmi Batas Administrasi Kab/Kota 2024 (456 MB)
├── scripts/
│   ├── process_lapakgis_shapefile.py # Ekstraksi & Kompresi Topologi SHP LapakGIS -> GeoJSON 3.5 MB
│   ├── build_full_datasets.py       # Skrip Master Pipeline Ekstraksi, Normalisasi & Kalkulasi PCA SVD
│   └── test_process.py              # Skrip Pengujian Pemetaan BPS Code
├── data/
│   ├── geospatial_national.json     # 515 Kab/Kota Terpetakan Nasional Teranotasi TPT & Penduduk Bekerja
│   ├── geospatial_national.js       # Wrapper JavaScript (Kompatibel Offline & Online)
│   ├── multivariate_jateng.json     # Data 8 Variabel 35 Kab/Kota Jateng 2021-2025 + PCA
│   ├── multivariate_jateng.js       # Wrapper JavaScript
│   ├── hierarchy_jateng.json        # Data Pohon Hierarki 3 Level (JSON)
│   └── hierarchy_jateng.js          # Wrapper JavaScript
└── [Folder Sumber Data BPS Excel]   # Berkas Mentah Asli dari BPS Jateng & BPS RI (2021-2025)
```

---

## 🚀 Cara Menjalankan Aplikasi

Aplikasi dirancang agar dapat dibuka tanpa ketergantungan server backend:

### Opsi 1: Membuka Langsung (Offline / Local)
Cukup buka berkas `WebStory.html` langsung di peramban web modern (Google Chrome, Microsoft Edge, Mozilla Firefox). Karena seluruh dataset telah dibundel ke dalam direktori `data/`, aplikasi dapat langsung beroperasi tanpa kendala CORS.

### Opsi 2: Menjalankan via Local Web Server
```bash
# Menggunakan Python 3:
python -m http.server 8080

# Buka pada browser:
http://localhost:8080/WebStory.html
```

### Opsi 3: Akses Publik (GitHub Pages)
Aplikasi siap di-deploy secara instan ke **GitHub Pages**:
1. Push repositori ini ke akun GitHub publik Anda.
2. Buka menu **Settings** > **Pages**.
3. Pilih branch `main` dan folder `/ (root)`.
4. Aplikasi akan aktif pada alamat: `https://[username].github.io/[repo-name]/WebStory.html`.

---

## 📚 Sumber Data Resmi & Atribusi BPS

1. **BPS RI:**
   * *Tingkat Pengangguran Terbuka Menurut Kabupaten/Kota (2025)* — Sakernas BPS RI.
   * *Penduduk Berumur 15 Tahun Keatas yang Bekerja Menurut Kabupaten/Kota dan Lapangan Usaha (2025)* — BPS RI.
   * *Jumlah Penduduk Menurut Kabupaten/Kota (2025)* — BPS RI.
2. **BPS Provinsi Jawa Tengah (2021–2025):**
   * *Tingkat Pengangguran Terbuka (TPT) dan Tingkat Partisipasi Angkatan Kerja (TPAK) Menurut Kabupaten/Kota di Jawa Tengah (Keadaan Agustus 2021–2025)*.
   * *Upah Minimum Kabupaten/Kota (UMK) Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.
   * *Produk Domestik Regional Bruto (PDRB) per Kapita Atas Dasar Harga Berlaku Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.
   * *Rata-Rata Pengeluaran per Kapita Sebulan Makanan dan Bukan Makanan di Daerah Perkotaan Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.
   * *Jumlah Angkatan Kerja Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.
   * *Rata-Rata Lama Sekolah (RLS) Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.
   * *Kepadatan Penduduk Menurut Kabupaten/Kota di Provinsi Jawa Tengah (2021–2025)*.

---

## ⚖️ Deklarasi Integritas Akademik (Sesuai Soal Poin 7)

Pekerjaan ini orisinal dan dikerjakan secara mandiri. Penggunaan alat bantu kecerdasan buatan (*AI assistant*) sebatas alat bantu asistensi teknis (penyusunan struktur sintaks skrip ekstraksi data tabular Python, implementasi aljabar linear SVD untuk PCA menggunakan NumPy, serta tata letak CSS/D3.js). Seluruh sintesis narasi, pemilihan tema penelitian, validasi data statistik, dan penarikan kesimpulan dilakukan secara independen oleh mahasiswa.
"# UAS-Visdat" 
