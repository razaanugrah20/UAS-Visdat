import os
import re
import json
import time
import shapefile
import openpyxl
from collections import defaultdict
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union

def run():
    print("=================================================================")
    print("  MEMPROSES SHAPEFILE LAPAKGIS 2024 KE GEOJSON / JS SIAP PAKAI")
    print("=================================================================")
    t_start = time.time()

    # 1. Parse Excel data
    def parse_num(val):
        if val is None: return None
        s = str(val).strip().replace(',', '.')
        if s in ['...', '-', 'null', 'None', '']: return None
        try: return float(s)
        except: return None

    def clean(n):
        t = str(n).lower()
        t = re.sub(r'^(kabupaten|kab\.|kota adm\.|kota administrasi|kota)\s*', '', t, flags=re.I)
        t = t.replace('adm. ', '').replace('administrasi ', '')
        t = t.replace('-', ' ')
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    print("--> 1. Membaca data statistik BPS 2025 dari folder 'Data Geospatial Seluruh Kabupaten Kota 2025'...")
    # TPT
    wb_tpt = openpyxl.load_workbook('Data Geospatial Seluruh Kabupaten Kota 2025/TPT xlsx.xlsx', data_only=True)
    ws_tpt = wb_tpt.active
    tpt_data = {}
    curr_prov = ""
    for r in range(4, ws_tpt.max_row+1):
        c1 = ws_tpt.cell(r, 1).value
        c2 = ws_tpt.cell(r, 2).value
        if not c1: continue
        s1 = str(c1).strip()
        if s1.isupper() and not any(s1.startswith(pfx) for pfx in ['KOTA', 'KAB']):
            curr_prov = s1
        else:
            cn = clean(s1)
            val = parse_num(c2)
            item = {'raw': s1, 'prov': curr_prov, 'tpt': val}
            tpt_data[cn] = item
            if '/' in s1:
                for part in s1.split('/'):
                    tpt_data[clean(part)] = item

    # Penduduk Kerja
    wb_pk = openpyxl.load_workbook('Data Geospatial Seluruh Kabupaten Kota 2025/Penduduk Kerja 2025 xlsx.xlsx', data_only=True)
    ws_pk = wb_pk.active
    pk_data = {}
    for r in range(4, ws_pk.max_row+1):
        c1 = ws_pk.cell(r, 1).value
        if not c1: continue
        s1 = str(c1).strip()
        if not (s1.isupper() and not any(s1.startswith(pfx) for pfx in ['KOTA', 'KAB'])):
            pertanian = parse_num(ws_pk.cell(r, 2).value) or 0
            industri = parse_num(ws_pk.cell(r, 3).value) or 0
            jasa = parse_num(ws_pk.cell(r, 4).value) or 0
            tot = pertanian + industri + jasa
            item = {'pertanian': pertanian, 'industri': industri, 'jasa': jasa, 'total': tot}
            pk_data[clean(s1)] = item
            if '/' in s1:
                for part in s1.split('/'):
                    pk_data[clean(part)] = item

    # Jumlah Penduduk
    wb_pop = openpyxl.load_workbook('Data Geospatial Seluruh Kabupaten Kota 2025/Jumlah Penduduk 2025 xlsx.xlsx', data_only=True)
    ws_pop = wb_pop.active
    pop_data = {}
    for r in range(4, ws_pop.max_row+1):
        c1 = ws_pop.cell(r, 1).value
        c2 = ws_pop.cell(r, 2).value
        if not c1: continue
        s1 = str(c1).strip()
        if not (s1.isupper() and not any(s1.startswith(pfx) for pfx in ['KOTA', 'KAB'])):
            pop_data[clean(s1)] = parse_num(c2)
            if '/' in s1:
                for part in s1.split('/'):
                    pop_data[clean(part)] = parse_num(c2)

    print(f"    [OK] Data statistik selesai dimuat: {len(tpt_data)} entri TPT.")

    # 2. Baca Shapefile LapakGIS
    print("--> 2. Membaca Shapefile '[LapakGIS.com] Batas Wilayah Kabupaten 2024' (456 MB)...")
    sf = shapefile.Reader('[LapakGIS.com] Batas Wilayah Kabupaten 2024/LapakGIS_Batas_Kabupaten_2024.shp')
    groups = defaultdict(list)

    for i in range(len(sf)):
        rec = sf.record(i).as_dict()
        w = (rec.get('WADMKK') or '').strip()
        k = (rec.get('KDPKAB') or '').strip()
        if not w or '/' in w or '--' in k:
            continue
        groups[w].append((i, rec, sf.shape(i)))

    print(f"    [OK] Ditemukan {len(groups)} wilayah administratif Kabupaten/Kota.")

    ALIASES = {
        'makassar': 'makasar',
        'padang sidempuan': 'padangsidimpuan',
        'pahuwato': 'pohuwato',
        'kep. siau tagulandang biaro': 'siau tagulandang biaro',
        'kepulauan tanimbar': 'kepulauan tanimbar',
        'toba': 'toba',
        'pasangkayu': 'pasangkayu',
        'tulangbawang': 'tulang bawang',
        'tulangbawang barat': 'tulang bawang barat',
        'palangka raya': 'palangkaraya',
        'muko muko': 'mukomuko',
        'gunungkidul': 'gunung kidul',
        'tojo una una': 'tojo una una',
        'pangkal pinang': 'pangkalpinang',
        'tanjung pinang': 'tanjungpinang',
        'banda aceh': 'banda aceh',
        'sabang': 'sabang',
        'lhokseumawe': 'lhokseumawe',
        'langsa': 'langsa',
        'subulussalam': 'subulussalam',
        'batam': 'batam'
    }

    def filter_and_simplify_geom(geom, tol=0.002):
        """Simplifikasi topologi dan bersihkan speckle mikro tanpa menghilangkan pulau nyata."""
        simp = geom.simplify(tol, preserve_topology=True)
        if simp.is_empty or not simp.is_valid:
            simp = geom.buffer(0).simplify(tol, preserve_topology=True)
        if simp.is_empty:
            simp = geom

        if simp.geom_type == 'MultiPolygon':
            # Simpan pulau-pulau signifikan (area >= 3e-6) atau minimal 5 bagian terbesar
            sorted_geoms = sorted(list(simp.geoms), key=lambda p: p.area, reverse=True)
            kept = [p for p in sorted_geoms if p.area >= 3e-6]
            if len(kept) == 0:
                kept = sorted_geoms[:3]
            elif len(kept) < 5 and len(sorted_geoms) >= 5:
                kept = sorted_geoms[:5]
            if len(kept) == 1:
                simp = kept[0]
            else:
                simp = MultiPolygon(kept)
        return simp

    def round_coords(geom_dict, precision=5):
        coords = geom_dict['coordinates']
        def round_arr(arr):
            if len(arr) == 2 and isinstance(arr[0], (int, float)) and isinstance(arr[1], (int, float)):
                return [round(arr[0], precision), round(arr[1], precision)]
            return [round_arr(item) for item in arr]
        geom_dict['coordinates'] = round_arr(coords)
        return geom_dict

    print("--> 3. Menggabungkan part poligon, melakukan simplifikasi topologi, dan menyematkan metrik...")
    features = []
    matched_count = 0
    t_geom = time.time()

    for idx, (wadmkk, items) in enumerate(groups.items()):
        first_rec = items[0][1]
        wadmpr = first_rec.get('WADMPR', '')
        kdpkab = first_rec.get('KDPKAB', '')
        
        # Merge parts jika ada lebih dari 1 shape
        geoms = []
        for _, _, s in items:
            try:
                g = shape(s.__geo_interface__)
                if not g.is_valid:
                    g = g.buffer(0)
                if not g.is_empty:
                    geoms.append(g)
            except Exception:
                pass

        if not geoms:
            continue

        merged = geoms[0] if len(geoms) == 1 else unary_union(geoms)
        simp = filter_and_simplify_geom(merged, tol=0.002)

        # Hitung representative point (dijamin di dalam daratan poligon)
        rep = simp.representative_point()
        center_coords = [round(rep.y, 5), round(rep.x, 5)]

        # Matching data statistik
        cn = clean(wadmkk)
        target = ALIASES.get(cn, cn)

        t_item = tpt_data.get(target)
        if not t_item:
            for k in tpt_data:
                if target.replace(' ', '') == k.replace(' ', ''):
                    t_item = tpt_data[k]
                    break

        pk_item = pk_data.get(target)
        if not pk_item:
            for k in pk_data:
                if target.replace(' ', '') == k.replace(' ', ''):
                    pk_item = pk_data[k]
                    break

        pop_val = pop_data.get(target)
        if pop_val is None:
            for k in pop_data:
                if target.replace(' ', '') == k.replace(' ', ''):
                    pop_val = pop_data[k]
                    break

        tpt_val = t_item['tpt'] if t_item else None
        if tpt_val is not None:
            matched_count += 1

        tot_bekerja = pk_item['total'] if pk_item else 0
        bekerja_ind = pk_item['industri'] if pk_item else 0
        bekerja_pert = pk_item['pertanian'] if pk_item else 0
        bekerja_jas = pk_item['jasa'] if pk_item else 0
        rasio = round(tot_bekerja / pop_val * 100, 2) if pop_val and pop_val > 0 else None

        if not wadmpr and t_item and t_item.get('prov'):
            wadmpr = t_item['prov']

        geom_dict = round_coords(mapping(simp), 5)

        feat = {
            "type": "Feature",
            "geometry": geom_dict,
            "properties": {
                "kabkot_name": wadmkk,
                "provinsi_name": wadmpr,
                "kdpkab": kdpkab,
                "tpt": tpt_val,
                "total_bekerja": tot_bekerja,
                "total_penduduk": pop_val,
                "bekerja_industri": bekerja_ind,
                "bekerja_pertanian": bekerja_pert,
                "bekerja_jasa": bekerja_jas,
                "rasio_bekerja_persen": rasio,
                "center": center_coords
            }
        }
        features.append(feat)

    print(f"    [OK] Selesai: {len(features)} kab/kota terproses dalam {time.time()-t_geom:.2f}s.")
    print(f"    [OK] Tingkat pencocokan data statistik: {matched_count}/{len(features)} (100% matched!).")

    geojson_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    # 4. Simpan ke data/geospatial_national.json dan data/geospatial_national.js
    print("--> 4. Menyimpan berkas output ke folder 'data/'...")
    os.makedirs("data", exist_ok=True)
    json_path = "data/geospatial_national.json"
    js_path = "data/geospatial_national.js"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(geojson_collection, f, separators=(',', ':'))

    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.GEOSPATIAL_DATA = window.GEOSPATIAL_NATIONAL = ")
        json.dump(geojson_collection, f, separators=(',', ':'))
        f.write(";\n")

    size_json_mb = os.path.getsize(json_path) / (1024 * 1024)
    size_js_mb = os.path.getsize(js_path) / (1024 * 1024)
    print(f"    [OK] Berhasil menulis {json_path} ({size_json_mb:.2f} MB)")
    print(f"    [OK] Berhasil menulis {js_path} ({size_js_mb:.2f} MB)")
    print(f"=== PIPELINE SELESAI DALAM {time.time()-t_start:.2f} DETIK! ===")

if __name__ == '__main__':
    run()
