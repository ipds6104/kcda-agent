"""
Compiler module for KCDA Typst documents.
Executes typst CLI with proper repo root and font paths.
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from .config import REPO_ROOT, KCDA_KECAMATAN_CONFIG
from .builder import build_kcda_typst
from .validator import KCDAValidator

def get_page_count(pdf_path: str) -> Optional[int]:
    """Mendapatkan jumlah halaman PDF menggunakan pdfinfo jika tersedia."""
    try:
        res = subprocess.run(["pdfinfo", pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        for line in res.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
    except Exception:
        pass
    return None

def compile_kecamatan(slug: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Mengompilasi naskah Typst untuk satu kecamatan."""
    cfg = KCDA_KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak ditemukan di konfigurasi.")

    out_base = Path(output_dir) if output_dir else (REPO_ROOT / "outputs" / slug)
    out_base.mkdir(parents=True, exist_ok=True)

    typ_path = out_base / f"kcda-{slug}.typ"
    pdf_path = out_base / f"kcda-{slug}.pdf"

    t0 = time.time()

    # 1. Build Typst Code
    typst_code = build_kcda_typst(slug, out_dir=out_base)
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(typst_code)

    # 2. Compile via Typst CLI
    fonts_dir = REPO_ROOT / "assets" / "fonts"
    cmd = ["typst", "compile", "--root", str(REPO_ROOT), "--font-path", str(fonts_dir), str(typ_path), str(pdf_path)]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Typst compilation failed for {slug}:\n{res.stderr}")

    duration = round(time.time() - t0, 2)
    file_size_kb = round(os.path.getsize(pdf_path) / 1024, 1)
    pages = get_page_count(str(pdf_path))

    return {
        "slug": slug,
        "nama_resmi": cfg["nama_resmi"],
        "no_publikasi": cfg.get("no_publikasi", "-"),
        "typ_path": str(typ_path),
        "pdf_path": str(pdf_path),
        "file_size_kb": file_size_kb,
        "pages": pages,
        "duration_sec": duration,
        "status": "SUCCESS"
    }

def compile_all_kcda(output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """Mengompilasi seluruh kecamatan yang terdaftar secara batch."""
    validator = KCDAValidator()
    if validator.check_placeholder_status():
        print(validator.warnings[0])
        print("--------------------------------------------------------------------------------")

    results = []
    total = len(KCDA_KECAMATAN_CONFIG)
    print(f"🚀 Memulai kompilasi KCDA untuk {total} kecamatan...")

    for idx, slug in enumerate(KCDA_KECAMATAN_CONFIG.keys(), 1):
        kname = KCDA_KECAMATAN_CONFIG[slug]["nama_resmi"]
        print(f"[{idx:>2}/{total}] ⚙️  Mengompilasi: {kname} ({slug})...")
        try:
            res = compile_kecamatan(slug, output_dir=output_dir)
            results.append(res)
            print(f"         ✅ Berhasil! {res['pages']} halaman, {res['file_size_kb']} KB ({res['duration_sec']}s)")
        except Exception as e:
            print(f"         ❌ Gagal: {e}")
            results.append({
                "slug": slug,
                "nama_resmi": kname,
                "status": "FAILED",
                "error": str(e)
            })

    return results

compile_all = compile_all_kcda
