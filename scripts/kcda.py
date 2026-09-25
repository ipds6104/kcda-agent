#!/usr/bin/env python3
"""
KCDA Agent Unified Command-Line Interface (CLI).
Alat bantu kompilasi, validasi, dan sinkronisasi naskah Kecamatan Dalam Angka (KCDA).
"""

import sys
import argparse
from pathlib import Path

# Tambahkan repo root ke sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.kcda_generator.config import (
    REPO_ROOT,
    CONFIG_FILE,
    IS_TEMPLATE_DEFAULT,
    KCDA_KECAMATAN_CONFIG,
    get_regency_info,
    get_instansi_info,
    get_publikasi_info,
    get_tables_schema
)
from scripts.kcda_generator.validator import KCDAValidator, print_validation_report
from scripts.kcda_generator.compiler import compile_kecamatan, compile_all
from scripts.kcda_generator.sync_engine import run_sync
from scripts.kcda_generator.data_loader import get_kecamatan_tab_rows


def cmd_status(args):
    """Menampilkan status konfigurasi, placeholder guard, dan ketersediaan data."""
    regency = get_regency_info()
    instansi = get_instansi_info()
    pub = get_publikasi_info()

    print("=" * 70)
    print("📍 STATUS KCDA AGENT")
    print("=" * 70)
    print(f"Instansi     : {instansi.get('nama_resmi', '-')}")
    print(f"Wilayah      : {regency.get('nama_resmi', '-')} ({regency.get('nama_en', '-')})")
    print(f"Ibukota Kab. : {regency.get('ibukota_kabupaten', '-')}")
    print(f"Publikasi    : KCDA {pub.get('tahun_rilis', 2026)} (Data Tahun {pub.get('tahun_data', 2025)})")
    print(f"Config File  : {'✅ ' + str(CONFIG_FILE.name) if CONFIG_FILE.exists() else '⚠️ Fallback ke regency.example.yaml'}")

    if IS_TEMPLATE_DEFAULT or "Mempawah" in regency.get("nama_resmi", ""):
        print("\n🚨 PERINGATAN PLACEHOLDER TEMPLATE:")
        print("   Status: AKTIF (Repositori masih memakai profil contoh Kabupaten Mempawah).")
        print("   -> Edit `config/regency.yaml` atau panggil coding agent Anda untuk onboarding.")
    else:
        print("\n✅ Profil Kabupaten kustom telah terkonfigurasi.")

    print(f"\nDaftar Kecamatan Terdaftar ({len(KCDA_KECAMATAN_CONFIG)} wilayah):")
    covers_dir = REPO_ROOT / "assets" / "covers"
    out_dir = REPO_ROOT / "outputs"

    for i, (slug, kcfg) in enumerate(KCDA_KECAMATAN_CONFIG.items(), 1):
        cover_path = REPO_ROOT / kcfg.get("cover_depan", "")
        has_cover = cover_path.exists()
        cover_mark = "🖼️ Cover [OK]" if has_cover else "⚠️ Cover [MISSING]"

        # Cek apakah ada data raw untuk kecamatan ini
        sample_rows = get_kecamatan_tab_rows("1.1", kcfg["nama_singkat"])
        raw_mark = "📄 Raw Data [OK]" if sample_rows else "❌ Raw Data [EMPTY]"

        has_pdf = (out_dir / slug / f"kcda-{slug}.pdf").exists()
        pdf_mark = "📕 PDF [READY]" if has_pdf else "⚪ PDF [NOT COMPILED]"

        print(f"  {i}. {kcfg['nama_resmi']:<26} | {cover_mark} | {raw_mark} | {pdf_mark}")

    print("=" * 70)


def cmd_validate(args):
    """Menjalankan audit diagnostik data dan placeholder guard."""
    ok = print_validation_report()
    if not ok:
        sys.exit(1)


def cmd_sync(args):
    """Menyinkronkan data dari Google Sheets ke penyimpanan lokal."""
    table_no = getattr(args, "tabel", None)
    run_sync(table_no=table_no)


def cmd_generate(args):
    """Mengompilasi naskah Typst menjadi PDF resmi."""
    validator = KCDAValidator()
    if validator.check_placeholder_status():
        print(validator.warnings[0])
        print("--------------------------------------------------------------------------------\n")

    if args.kecamatan:
        print(f"🚀 Mengompilasi naskah KCDA untuk: {args.kecamatan}...")
        try:
            res = compile_kecamatan(args.kecamatan)
            print(f"🎉 SUKSES!")
            print(f"   • Wilayah      : {res['nama_resmi']}")
            print(f"   • Berkas PDF   : {res['pdf_path']}")
            print(f"   • Ukuran       : {res['file_size_kb']} KB")
            print(f"   • Halaman      : {res.get('pages', 'N/A')} hal")
            print(f"   • Waktu Build  : {res['duration_sec']} detik")
        except Exception as e:
            print(f"❌ Gagal kompilasi: {e}")
            sys.exit(1)
    else:
        print("🚀 Mengompilasi naskah KCDA untuk seluruh kecamatan terdaftar...")
        results = compile_all()
        print(f"\n🎉 Selesai mengompilasi {len(results)} buku KCDA.")
        for r in results:
            print(f"   • {r['nama_resmi']:<25} -> {r['pdf_path']} ({r['file_size_kb']} KB, {r['pages']} hal)")


def cmd_init(args):
    """Inisialisasi konfigurasi kabupaten baru dari template."""
    dest = CONFIG_FILE
    src = REPO_ROOT / "config" / "regency.example.yaml"
    if dest.exists() and not args.force:
        print(f"⚠️  Berkas {dest} sudah ada.")
        print("   Gunakan flag `--force` jika ingin menimpa dengan berkas template kosong.")
        return

    import shutil
    shutil.copyfile(src, dest)
    print(f"✅ Berkas konfigurasi baru telah dibuat di: {dest}")
    print("   Langkah berikutnya:")
    print("   1. Edit `config/regency.yaml` dengan nama kabupaten, kode wilayah, dan daftar kecamatan Anda.")
    print("   2. Panggil coding agent (AGY / Antigravity) untuk memandu onboarding via perintah:")
    print("      `agy \"Bantu saya isi config/regency.yaml untuk BPS Kabupaten saya\"`")


def main():
    parser = argparse.ArgumentParser(
        description="KCDA Agent CLI - Generator Publikasi Kecamatan Dalam Angka Resmi BPS",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia")

    # Command: status
    parser_status = subparsers.add_parser("status", help="Tampilkan status konfigurasi dan ketersediaan berkas")
    parser_status.set_defaults(func=cmd_status)

    # Command: validate
    parser_val = subparsers.add_parser("validate", help="Jalankan audit diagnostik data & placeholder guard")
    parser_val.set_defaults(func=cmd_validate)

    # Command: sync
    parser_sync = subparsers.add_parser("sync", help="Sinkronkan data dari Google Sheets")
    parser_sync.add_argument("--tabel", "-t", type=str, help="Nomor tabel spesifik (misal: 1.1)")
    parser_sync.set_defaults(func=cmd_sync)

    # Command: generate
    parser_gen = subparsers.add_parser("generate", help="Kompilasi naskah Typst menjadi PDF resmi BPS")
    parser_gen.add_argument("--kecamatan", "-k", type=str, help="Slug kecamatan yang ingin dikompilasi")
    parser_gen.add_argument("--all", "-a", action="store_true", help="Kompilasi seluruh kecamatan")
    parser_gen.set_defaults(func=cmd_generate)

    # Command: init
    parser_init = subparsers.add_parser("init", help="Inisialisasi config/regency.yaml baru")
    parser_init.add_argument("--force", "-f", action="store_true", help="Paksa timpa file konfigurasi yang sudah ada")
    parser_init.set_defaults(func=cmd_init)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
