"""
KCDA Validator & Placeholder Guard Module.
Audits configuration, checks for unedited template defaults, and validates table readiness.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from .config import (
    REPO_ROOT,
    CONFIG_FILE,
    IS_TEMPLATE_DEFAULT,
    REGENCY_RAW_CONFIG,
    KCDA_KECAMATAN_CONFIG,
    get_tables_schema
)
from .data_loader import get_table_data, get_kecamatan_tab_rows

class KCDAValidator:
    def __init__(self):
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.info: List[str] = []

    def check_placeholder_status(self) -> bool:
        """Mengecek apakah repositori masih memakai template contoh Mempawah."""
        is_default = IS_TEMPLATE_DEFAULT
        kab = REGENCY_RAW_CONFIG.get("kabupaten", {})
        nama_kab = kab.get("nama_resmi", "")

        if is_default or "Mempawah" in nama_kab:
            self.warnings.append(
                "🚨 PERINGATAN PLACEHOLDER TEMPLATE:\n"
                "   Repositori ini saat ini masih menggunakan konfigurasi contoh (Kabupaten Mempawah).\n"
                "   Data dan naskah yang digenerate adalah sampel template.\n"
                "   -> Untuk BPS Kabupaten/Kota lain: Harap sesuaikan `config/regency.yaml` "
                "dengan data kabupaten Anda sebelum publikasi final!"
            )
            return True
        return False

    def check_kecamatan_completeness(self) -> Dict[str, Any]:
        """Mengecek kelengkapan data per kecamatan."""
        kec_summary = {}
        tables = get_tables_schema()
        mandatory_tables = [t for t in tables if t.get("wajib")]

        for slug, kcfg in KCDA_KECAMATAN_CONFIG.items():
            nama_singkat = kcfg["nama_singkat"]
            filled_tables = 0
            empty_tables = 0

            for t in mandatory_tables:
                tno = t.get("no", "")
                rows = get_kecamatan_tab_rows(tno, nama_singkat)
                if rows and len(rows) > 0:
                    filled_tables += 1
                else:
                    empty_tables += 1

            total_mandatory = len(mandatory_tables)
            completeness_pct = round((filled_tables / total_mandatory * 100), 1) if total_mandatory > 0 else 0
            kec_summary[slug] = {
                "nama_resmi": kcfg["nama_resmi"],
                "total_mandatory": total_mandatory,
                "filled_tables": filled_tables,
                "empty_tables": empty_tables,
                "completeness_pct": completeness_pct
            }

        return kec_summary

    def run_full_audit(self) -> Dict[str, Any]:
        """Menjalankan audit lengkap dan mengembalikan laporan diagnostik."""
        self.warnings.clear()
        self.errors.clear()
        self.info.clear()

        # 1. Cek status placeholder
        is_placeholder = self.check_placeholder_status()

        # 2. Cek file config
        if not CONFIG_FILE.exists():
            self.warnings.append(f"Berkas config/regency.yaml belum dibuat, saat ini membaca fallback dari regency.example.yaml.")

        # 3. Cek daftar kecamatan
        total_kec = len(KCDA_KECAMATAN_CONFIG)
        if total_kec == 0:
            self.errors.append("Tidak ada kecamatan yang terdaftar di konfigurasi.")
        else:
            self.info.append(f"Terdaftar {total_kec} kecamatan di konfigurasi.")

        # 4. Cek audit tabel
        kec_audit = self.check_kecamatan_completeness()

        return {
            "is_placeholder": is_placeholder,
            "warnings": self.warnings,
            "errors": self.errors,
            "info": self.info,
            "kecamatan_summary": kec_audit
        }

def print_validation_report():
    validator = KCDAValidator()
    report = validator.run_full_audit()

    print("================================================================================")
    print("🔍 LAPORAN VALIDASI & KESIAPAN DATA KCDA AGENT")
    print("================================================================================")

    if report["is_placeholder"]:
        for w in report["warnings"]:
            print(f"\n{w}")
        print("--------------------------------------------------------------------------------")

    for inf in report["info"]:
        print(f"ℹ️  {inf}")

    if report["errors"]:
        print("\n❌ KESALAHAN KRITIS:")
        for err in report["errors"]:
            print(f"   • {err}")

    print("\n📊 KESIAPAN TABEL WAJIB PER KECAMATAN:")
    for slug, summary in report["kecamatan_summary"].items():
        bar_len = int(summary["completeness_pct"] / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        print(f"   • {summary['nama_resmi']:<30} [{bar}] {summary['completeness_pct']:>5}% "
              f"({summary['filled_tables']}/{summary['total_mandatory']} tabel wajib)")

    print("================================================================================")
    return len(report["errors"]) == 0
