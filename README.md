# Eksplorasi Ketimpangan Ketenagakerjaan & Relokasi Industri

Aplikasi web visualisasi data interaktif (scrollytelling) tentang disparitas ketenagakerjaan di Indonesia, dengan fokus analisis pada Jawa Tengah tahun 2025. Data bersumber dari BPS, dibuat dalam konteks mata kuliah Visualisasi Data STIS.

## Isi Halaman

Halaman dibagi menjadi beberapa bagian yang dibaca berurutan sambil di-scroll:

1. **Pendahuluan (Hero)**: pengantar topik ketimpangan ketenagakerjaan.
2. **Lanskap Ketenagakerjaan Nasional 2025** (`#geospatial`): peta interaktif Leaflet per wilayah, dengan pewarnaan berdasarkan kelas TPT, mode peta yang bisa diganti, filter per pulau, panel detail wilayah, dan tombol reset zoom.
3. **Dinamika Multivariat 35 Kabupaten/Kota Jawa Tengah** (`#multivariate`): tiga visual yang saling terhubung:
   - PCA biplot
   - Parallel coordinates dengan brushing
   - Clustered heatmap (skala bisa diganti)
   Dilengkapi pemilih tahun, filter cluster, highlight kabupaten/kota (hover maupun permanen), dan story tour.
4. **Struktur Hierarki Tenaga Kerja Jawa Tengah** (`#hierarchy`): treemap dan sunburst D3.
5. **Kesimpulan** (`#kesimpulan`).

Navigasi tersedia lewat top nav dan dot navigation di samping yang otomatis mengikuti posisi scroll.

## Struktur Folder

```
.
├── index.html          # Struktur halaman dan seluruh JavaScript
├── style.css           # Seluruh styling (dipisah dari index.html)
├── README.md
└── data_json/          # WAJIB ada, tidak termasuk di file ini
    ├── geospatial_national.js
    ├── multivariate_jateng.js
    └── hierarchy_jateng.js
```

File di `data_json/` dimuat sebagai `<script>` biasa (bukan `fetch`), jadi datanya berupa variabel JavaScript global. Tanpa folder ini, semua visualisasi akan kosong.

## Teknologi

| Library | Kegunaan | Sumber |
|---|---|---|
| D3.js v7 | PCA biplot, parallel coordinates, heatmap, treemap, sunburst | d3js.org |
| Leaflet 1.9.4 | Peta geospasial | unpkg |
| Lucide | Ikon | unpkg (`@latest`) |
| Google Fonts | Public Sans, Roboto Mono | fonts.googleapis.com |

Tidak ada build step, framework, atau dependensi npm.

## Cara Menjalankan

Karena data dimuat lewat tag `<script>`, halaman bisa dibuka langsung dengan klik dua kali `index.html`. Tetap disarankan memakai server lokal agar perilakunya sama dengan saat di-hosting:

```bash
# Python
python -m http.server 8000

# atau Node
npx serve .
```

Lalu buka `http://localhost:8000`. Koneksi internet diperlukan untuk memuat library dari CDN.

## Gambaran Kode JavaScript

Semua logika ada di satu blok `<script>` di akhir `index.html`, dikelompokkan per bagian:

- **Data**: `getGeoData`, `getMvData`, `getHierarchyData` mengambil data dari variabel global.
- **Navigasi & scroll**: `initScrollyTelling`, `initDotNav`, `initTopNavObserver`.
- **Tooltip**: `showTooltip`, `hideTooltip`.
- **Peta**: `initGeospatialMap`, `renderGeoLayers`, `getTptClassColor`, `getFeatureStyle`, `displayRegionDetail`, `setGeoMapMode`, `filterMapIsland`, `resetMapZoom`.
- **Multivariat**: `initMultivariateVisualizations`, `renderPcaBiplot`, `renderParallelCoordinates`, `onPcpBrush`, `renderClusteredHeatmap`, `setHeatmapScaleMode`, `setMvYear`, `filterMvCluster`, serta fungsi highlight (`highlightKabKota`, `togglePermanentHighlight`, `applyCurrentHighlightState`, `resetMvHighlight`) dan story tour (`setTourCids`, `resetStoryTour`).
- **Hierarki**: `initHierarchyVisualizations`, `renderTreemap`, `renderSunburst`, `getHierarchyColor`.

## Catatan Teknis

- Masih ada sekitar 100 atribut `style="..."` inline di HTML. Ini sengaja tidak dipindah ke `style.css` agar tampilan tidak berubah; bisa dirapikan bertahap menjadi class.
- Lucide dimuat dengan versi `@latest`. Sebaiknya dikunci ke versi tertentu supaya tampilan tidak berubah tiba-tiba saat ada rilis baru.
- JavaScript masih menyatu di `index.html` (sekitar 1.300 baris). Jika ingin konsisten, bisa dipisah juga ke `script.js`.

## Kredit

Kode dibuat oleh [Muhammad Raza Anugrah]. Data: Badan Pusat Statistik (BPS).
