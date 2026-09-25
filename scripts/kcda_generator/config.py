"""
KCDA Dynamic Configuration Module.
Loads regency and kecamatan configuration from config/regency.yaml or config/regency.example.yaml.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = REPO_ROOT / "config" / "regency.yaml"
EXAMPLE_CONFIG_FILE = REPO_ROOT / "config" / "regency.example.yaml"
TABLES_SCHEMA_FILE = REPO_ROOT / "config" / "tables_schema.json"

def _load_raw_config() -> Dict[str, Any]:
    target = CONFIG_FILE if CONFIG_FILE.exists() else EXAMPLE_CONFIG_FILE
    if not target.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_FILE} or {EXAMPLE_CONFIG_FILE}")
    with open(target, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

REGENCY_RAW_CONFIG = _load_raw_config()
IS_TEMPLATE_DEFAULT = REGENCY_RAW_CONFIG.get("is_template_default", True)

# Build KCDA_KECAMATAN_CONFIG dictionary for backwards compatibility & fast lookup
KCDA_KECAMATAN_CONFIG: Dict[str, Dict[str, Any]] = {}
for kec in REGENCY_RAW_CONFIG.get("kecamatan", []):
    slug = kec.get("slug")
    if slug:
        KCDA_KECAMATAN_CONFIG[slug] = {
            "slug": slug,
            "nama_resmi": kec.get("nama_resmi", f"Kecamatan {slug.replace('-', ' ').title()}"),
            "nama_singkat": kec.get("nama_singkat", slug.replace('-', ' ').title()),
            "nama_en": kec.get("nama_en", f"{slug.replace('-', ' ').title()} Subdistrict"),
            "kode_wilayah": str(kec.get("kode_wilayah", "")),
            "no_katalog": str(kec.get("no_katalog", "")),
            "no_publikasi": str(kec.get("no_publikasi", "")),
            "pic_nama": kec.get("pic_nama", "Staf BPS"),
            "pic_nama_polos": kec.get("pic_nama", "Staf BPS").split(",")[0].strip(),
            "ibukota_kecamatan": kec.get("ibukota", ""),
            "desa_list": kec.get("desa_list", []),
            "cover_depan": kec.get("cover_depan", f"assets/covers/depan/{slug.title()}1.jpg"),
            "cover_dalam": kec.get("cover_dalam", f"assets/covers/depan/{slug.title()}2.jpg"),
            "gsheet_id": kec.get("gsheet_id", "")
        }

def get_regency_info() -> Dict[str, Any]:
    """Mengembalikan informasi profil kabupaten/kota."""
    return REGENCY_RAW_CONFIG.get("kabupaten", {})

def get_instansi_info() -> Dict[str, Any]:
    """Mengembalikan informasi instansi BPS."""
    return REGENCY_RAW_CONFIG.get("instansi", {})

def get_publikasi_info() -> Dict[str, Any]:
    """Mengembalikan konfigurasi publikasi."""
    return REGENCY_RAW_CONFIG.get("publikasi", {})

def get_pimpinan_info() -> Dict[str, Any]:
    """Mengembalikan profil pimpinan BPS."""
    return REGENCY_RAW_CONFIG.get("pimpinan", {})

def get_tables_schema() -> List[Dict[str, Any]]:
    """Mengembalikan skema daftar tabel (wajib & opsional)."""
    if TABLES_SCHEMA_FILE.exists():
        with open(TABLES_SCHEMA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
