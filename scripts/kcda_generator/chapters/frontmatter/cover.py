"""
Frontmatter: Cover & Title Page for KCDA.
Menangani Kover Depan dan Halaman Judul Utama (Halaman i).
"""

import os
from pathlib import Path
from typing import Dict, Any

def render_cover_and_title_page(cfg: Dict[str, Any]) -> str:
    slug = cfg.get("slug", "")
    
    # 1. Prioritas dari konfigurasi kecamatan
    cover_depan = cfg.get("cover_depan", f"assets/covers/depan/{slug.title()}1.jpg")
    cover_dalam = cfg.get("cover_dalam", f"assets/covers/depan/{slug.title()}2.jpg")

    # Format path untuk Typst (relatif terhadap repo root /)
    if not cover_depan.startswith("/"):
        cover_depan = "/" + cover_depan
    if not cover_dalam.startswith("/"):
        cover_dalam = "/" + cover_dalam

    return f"""// ==========================================
// 1. KOVER DEPAN (FRONT COVER) - DESAIN RESMI TERBARU
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("{cover_depan}", width: 100%, height: 100%)
]

// ==========================================
// HALAMAN KOSONG DI BALIK KOVER DEPAN (INSIDE COVER / FLYLEAF)
// Sesuai Pedoman Pembuatan Publikasi BPS 2023 Subbab 4.1.2 Poin 6 (Hal. 45) & Terbitan Statistik Indonesia BPS RI.
// Halaman setelah kover depan tidak dihitung sebagai halaman dan tidak diberi nomor halaman.
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[ ]

// ==========================================
// 2. HALAMAN JUDUL UTAMA / TITLE PAGE (HALAMAN i)
// Terletak pada halaman ganjil (rekto/kanan) sesuai Pedoman Publikasi BPS 2023 Subbab 4.3.1 (Hal. 75).
// Perhitungan angka romawi resmi dimulai pada Halaman Judul Utama (halaman i).
// ==========================================
#counter(page).update(1)

#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("{cover_dalam}", width: 100%, height: 100%)
]
"""
