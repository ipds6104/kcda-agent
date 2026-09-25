"""
Google Sheets Sync Engine for KCDA Agent.
Synchronizes tables from Google Sheets directly to data/raw_tables/ as structured JSON.
"""

import os
import re
import json
import time
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

from .config import REPO_ROOT, KCDA_KECAMATAN_CONFIG, get_tables_schema
from .validator import KCDAValidator

def get_auth_token() -> Optional[str]:
    """Mengambil OAuth token Google Drive jika tersedia."""
    # 1. Cek token dari gdrive_tool
    try:
        sys.path.insert(0, '/root/.gemini/config/skills/gdrive/scripts')
        import gdrive_tool
        return gdrive_tool.get_valid_access_token()
    except Exception:
        pass

    # 2. Cek token file di /app/data/google_token.json
    token_file = Path("/app/data/google_token.json")
    if token_file.exists():
        try:
            with open(token_file, "r") as f:
                data = json.load(f)
                return data.get("access_token") or data.get("token")
        except Exception:
            pass
    return None

def normalize_tab_name(name: str) -> str:
    """Menyelaraskan nama tab sheet dengan nama singkat kecamatan."""
    clean = re.sub(r'[^a-zA-Z\s]', '', name).strip().lower()
    for slug, kcfg in KCDA_KECAMATAN_CONFIG.items():
        k_clean = kcfg["nama_singkat"].lower()
        if k_clean in clean:
            return kcfg["nama_singkat"]
    return name.strip()

def sync_table_from_sheet(sheet_id: str, table_info: Dict[str, Any], token: Optional[str]) -> Optional[Dict[str, Any]]:
    """Mengunduh satu spreadsheet Google Sheets dan menyusunnya menjadi format JSON KCDA."""
    if not token:
        # Fallback ke public view / export jika tanpa token
        return None

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?includeGridData=true"

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code != 200:
            print(f"   ⚠️ HTTP {resp.status_code} saat mengunduh Sheet ID {sheet_id}")
            return None
        data = resp.json()
    except Exception as e:
        print(f"   ❌ Gagal menghubungi Google Sheets API: {e}")
        return None

    tabs_result = {}
    for sheet in data.get("sheets", []):
        props = sheet.get("properties", {})
        title = props.get("title", "")
        norm_title = normalize_tab_name(title)

        data_rows = []
        grid_data = sheet.get("data", [])
        if grid_data:
            row_data = grid_data[0].get("rowData", [])
            for r in row_data:
                cells = []
                for c in r.get("values", []):
                    val = c.get("formattedValue", "")
                    cells.append(str(val) if val is not None else "")
                data_rows.append(cells)

        tabs_result[norm_title] = {
            "title": title,
            "rows": data_rows
        }

    return {
        "no": table_info.get("no", ""),
        "nama": table_info.get("nama", ""),
        "sumber": table_info.get("sumber", ""),
        "tahun": table_info.get("tahun", ""),
        "sheet_id": sheet_id,
        "tabs": tabs_result
    }

def run_sync(table_no: Optional[str] = None):
    """Menjalankan sinkronisasi seluruh tabel dari Google Sheets."""
    print("================================================================================")
    print("🔄 SINKRONISASI DATA GOOGLE SHEETS KCDA AGENT")
    print("================================================================================")

    # 1. Peringatan placeholder
    validator = KCDAValidator()
    if validator.check_placeholder_status():
        print(validator.warnings[0])
        print("--------------------------------------------------------------------------------")

    token = get_auth_token()
    if not token:
        print("⚠️ Catatan: Google OAuth token tidak ditemukan di environment.")
        print("   -> Sinkronisasi membutuhkan otorisasi Google API.")
        print("   -> Menggunakan cache data lokal yang ada di data/raw_tables/.")
        return False

    tables = get_tables_schema()
    target_tables = [t for t in tables if not table_no or t.get("no") == table_no]

    out_dir = REPO_ROOT / "data" / "raw_tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    total = len(target_tables)
    print(f"🚀 Memulai unduh {total} tabel Google Sheets...")

    for idx, t in enumerate(target_tables, 1):
        sid = t.get("sheet_id")
        tno = t.get("no", "")
        tname = t.get("nama", "")

        if not sid:
            print(f"[{idx:>2}/{total}] ⏭️  Tabel {tno}: Sheet ID belum diset.")
            continue

        clean_slug = re.sub(r'[^a-zA-Z0-9]', '_', tname.lower())[:30].strip('_')
        clean_no = tno.replace('.', '_').strip('_')
        out_file = out_dir / f"tabel_{clean_no}_{clean_slug}.json"

        print(f"[{idx:>2}/{total}] 📥 Mengunduh Tabel {tno} ({tname[:40]}...)...")
        res = sync_table_from_sheet(sid, t, token)
        if res:
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)
            success_count += 1
            print(f"         ✅ Berhasil disimpan ke {out_file.name}")
        else:
            print(f"         ⚠️ Melewati tabel {tno}.")
        time.sleep(0.3)

    print(f"\n🎉 Selesai! Berhasil menyinkronkan {success_count}/{total} tabel.")
    return True
