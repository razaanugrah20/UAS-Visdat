import os
import re
import json
import glob
import openpyxl
import numpy as np

# 1. Definisi 35 Kabupaten/Kota di Jawa Tengah dan Pemetaannya ke Eks-Karesidenan
JATENG_KABKOT = [
    {"id": "3301", "name": "Cilacap", "type": "Kabupaten", "karesidenan": "Banyumas"},
    {"id": "3302", "name": "Banyumas", "type": "Kabupaten", "karesidenan": "Banyumas"},
    {"id": "3303", "name": "Purbalingga", "type": "Kabupaten", "karesidenan": "Banyumas"},
    {"id": "3304", "name": "Banjarnegara", "type": "Kabupaten", "karesidenan": "Banyumas"},
    {"id": "3305", "name": "Kebumen", "type": "Kabupaten", "karesidenan": "Kedu"},
    {"id": "3306", "name": "Purworejo", "type": "Kabupaten", "karesidenan": "Kedu"},
    {"id": "3307", "name": "Wonosobo", "type": "Kabupaten", "karesidenan": "Kedu"},
    {"id": "3308", "name": "Magelang", "type": "Kabupaten", "karesidenan": "Kedu"},
    {"id": "3309", "name": "Boyolali", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3310", "name": "Klaten", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3311", "name": "Sukoharjo", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3312", "name": "Wonogiri", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3313", "name": "Karanganyar", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3314", "name": "Sragen", "type": "Kabupaten", "karesidenan": "Surakarta"},
    {"id": "3315", "name": "Grobogan", "type": "Kabupaten", "karesidenan": "Semarang"},
    {"id": "3316", "name": "Blora", "type": "Kabupaten", "karesidenan": "Pati"},
    {"id": "3317", "name": "Rembang", "type": "Kabupaten", "karesidenan": "Pati"},
    {"id": "3318", "name": "Pati", "type": "Kabupaten", "karesidenan": "Pati"},
    {"id": "3319", "name": "Kudus", "type": "Kabupaten", "karesidenan": "Pati"},
    {"id": "3320", "name": "Jepara", "type": "Kabupaten", "karesidenan": "Pati"},
    {"id": "3321", "name": "Demak", "type": "Kabupaten", "karesidenan": "Semarang"},
    {"id": "3322", "name": "Semarang", "type": "Kabupaten", "karesidenan": "Semarang"},
    {"id": "3323", "name": "Temanggung", "type": "Kabupaten", "karesidenan": "Kedu"},
    {"id": "3324", "name": "Kendal", "type": "Kabupaten", "karesidenan": "Semarang"},
    {"id": "3325", "name": "Batang", "type": "Kabupaten", "karesidenan": "Pekalongan"},
    {"id": "3326", "name": "Pekalongan", "type": "Kabupaten", "karesidenan": "Pekalongan"},
    {"id": "3327", "name": "Pemalang", "type": "Kabupaten", "karesidenan": "Pekalongan"},
    {"id": "3328", "name": "Tegal", "type": "Kabupaten", "karesidenan": "Pekalongan"},
    {"id": "3329", "name": "Brebes", "type": "Kabupaten", "karesidenan": "Pekalongan"},
    {"id": "3371", "name": "Kota Magelang", "type": "Kota", "karesidenan": "Kedu"},
    {"id": "3372", "name": "Kota Surakarta", "type": "Kota", "karesidenan": "Surakarta"},
    {"id": "3373", "name": "Kota Salatiga", "type": "Kota", "karesidenan": "Semarang"},
    {"id": "3374", "name": "Kota Semarang", "type": "Kota", "karesidenan": "Semarang"},
    {"id": "3375", "name": "Kota Pekalongan", "type": "Kota", "karesidenan": "Pekalongan"},
    {"id": "3376", "name": "Kota Tegal", "type": "Kota", "karesidenan": "Pekalongan"}
]

NAME_TO_ID = {k["name"].lower(): k["id"] for k in JATENG_KABKOT}
# also map alternate forms
for k in JATENG_KABKOT:
    NAME_TO_ID[k["name"].lower().replace("kota ", "")] = k["id"]
    NAME_TO_ID["kabupaten " + k["name"].lower()] = k["id"]
    NAME_TO_ID["kab. " + k["name"].lower()] = k["id"]

def normalize_name(text):
    if not text:
        return ""
    text = str(text).strip()
    # remove leading digits if any
    text = re.sub(r'^\d+\s*', '', text)
    # clean extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_float(val):
    if val is None:
        return None
    val_str = str(val).strip().replace(',', '.')
    # check for '-' or '...'
    if val_str in ['-', '...', 'null', 'None', '']:
        return None
    try:
        return float(val_str)
    except:
        return None

print("Setup mapping complete. 35 Kab/Kota Jateng.")
