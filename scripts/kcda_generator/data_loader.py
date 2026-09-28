"""
Data loader module for KCDA tables with clean caching and fallback handling.
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import REPO_ROOT

_RAW_TABLES_CACHE: Dict[str, Any] = {}

def get_table_data(table_no: str) -> Optional[Dict[str, Any]]:
    """Mencari dan me-load file JSON raw table berdasarkan nomor tabel (misal '1.1.', '2.1.1', '3.1')."""
    if table_no in _RAW_TABLES_CACHE:
        return _RAW_TABLES_CACHE[table_no]

    clean_no = table_no.replace('.', '_').strip('_')
    raw_dir = REPO_ROOT / "data" / "raw_tables"
    pattern = str(raw_dir / f"tabel_{clean_no}_*.json")
    matches = glob.glob(pattern)
    if matches:
        with open(matches[0], encoding='utf-8') as f:
            data = json.load(f)
            _RAW_TABLES_CACHE[table_no] = data
            return data
    return None

def get_kecamatan_tab_rows(table_no: str, nama_kecamatan_singkat: str) -> List[List[str]]:
    """Mengambil baris-baris data dari tab kecamatan tertentu."""
    tbl = get_table_data(table_no)
    if not tbl:
        return []
    tabs = tbl.get("tabs", {})
    target_tab = None
    target_clean = nama_kecamatan_singkat.lower().strip()

    for tname in tabs.keys():
        tname_clean = tname.lower().strip().replace("mampawah", "mempawah")
        if tname_clean == target_clean or target_clean in tname_clean:
            target_tab = tname
            break

    if target_tab and target_tab in tabs:
        return tabs[target_tab].get("rows", [])
    return []

def clean_cell_value(val: Any) -> str:
    """Membersihkan nilai sel untuk Typst markup."""
    if val is None:
        return "..."
    s = str(val).strip()
    if not s or s.lower() == "null":
        return "..."
    if s == "-" or s == "–" or s == "—":
        return "–"
    s = s.replace("#", "\\#").replace("$", "\\$").replace("@", "\\@")
    return s
