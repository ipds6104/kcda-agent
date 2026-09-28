"""
KCDA Typst Document Builder Engine (Orchestrator - A5 Template Resmi BPS).
Assembles frontmatter, chapters 1 to 7, charts, bibliography, and backcover dynamically based on regency configuration.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from .config import (
    REPO_ROOT,
    KCDA_KECAMATAN_CONFIG,
    get_regency_info,
    get_instansi_info,
    get_pimpinan_info,
    get_publikasi_info
)
from .chapters.frontmatter import render_frontmatter
from .chapters.chapter1 import render_chapter1
from .chapters.chapter2 import render_chapter2
from .chapters.chapter3 import render_chapter3
from .chapters.chapter4 import render_chapter4
from .chapters.chapter5 import render_chapter5
from .chapters.chapter6 import render_chapter6
from .chapters.chapter7 import render_chapter7
from .chapters.backcover import render_backcover

def build_kcda_typst(slug: str, out_dir: Any = None) -> str:
    """Menyusun kode dokumen Typst lengkap ukuran A5 sesuai Template Resmi KCDA BPS Pusat."""
    cfg = KCDA_KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak ditemukan di KCDA_KECAMATAN_CONFIG.")

    regency_info = get_regency_info()
    instansi_info = get_instansi_info()
    pub_info = get_publikasi_info()

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())

    tahun_rilis = pub_info.get("tahun_rilis", 2026)
    tahun_data = pub_info.get("tahun_data", 2025)
    nama_kabupaten = regency_info.get("nama_resmi", "Kabupaten")
    nama_kabupaten_singkat = regency_info.get("nama_singkat", "")
    nama_instansi_singkat = instansi_info.get("nama_singkat", "BPS").upper()
    warna_tema = pub_info.get("warna_tema_cmyk", "cmyk(0%, 20%, 90%, 0%)")
    warna_running = pub_info.get("warna_running_cmyk", "cmyk(0%, 35%, 95%, 0%)")

    # Header & Footer Logic Typst untuk A5 (Sesuai Pedoman Publikasi BPS 2023 & Template Resmi KCDA)
    header_logic = f"""
#let in_frontmatter = state("in_frontmatter", true)
#let active_chapter = state("active_chapter", "")
#let active_chapter_en = state("active_chapter_en", "")
#let is_chapter_page = state("is_chapter_page", false)

// Warna Utama & Warna Running Title Resmi BPS (Pedoman KCDA)
#let main_theme_color = {warna_tema}
#let running_title_color = {warna_running}

// Badge pill numbering resmi BPS Pusat (Aturan KCDA: main_theme_color, 49.2pt x 21pt)
#let page_badge(val) = box(
  fill: main_theme_color,
  radius: 10.5pt,
  width: 49.2pt,
  height: 21pt,
)[
  #align(center + horizon)[
    #text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", fill: white)[#val]
  ]
]

#show heading: it => [ #it #metadata("h") <page_marker> ]
#show table: it => [ #it #metadata("t") <page_marker> ]
#show grid: it => [ #it #metadata("g") <page_marker> ]
#show par: it => [ #it #metadata("p") <page_marker> ]
#show figure: it => [ #it #metadata("f") <page_marker> ]
#show image: it => [ #it #metadata("i") <page_marker> ]

#let normal_margins = (
  inside: 2.0cm,
  outside: 1.5cm,
  top: 2.0cm,
  bottom: 2.0cm,
)

#let page_header = context {{
  let p = here().page()
  let has_c = query(selector(<page_marker>)).any(m => {{
    let pos = m.location().position()
    pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
  }})
  if has_c and not in_frontmatter.get() {{
    let page_num = counter(page).get().first()
    let titles = query(selector(<chapter_title>)).filter(m => m.location().page() <= p)
    let chapter_title = if titles.len() > 0 {{ titles.last().value }} else {{ "" }}
    if calc.even(page_num) {{
      // Halaman Genap (Verso/Kiri): Judul Publikasi Bahasa Indonesia
      align(left, text(8pt, font: ("Metropolis", "Liberation Sans"), fill: running_title_color, weight: "bold")[KECAMATAN {nama_singkat.upper()} DALAM ANGKA {tahun_rilis}])
    }} else {{
      // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Indonesia
      let right_text = if chapter_title != "" {{ chapter_title }} else {{ "{nama_instansi_singkat}" }}
      align(right, text(8pt, font: ("Metropolis", "Liberation Sans"), fill: running_title_color, weight: "bold")[#right_text])
    }}
  }}
}}

#let page_footer = context {{
  let p = here().page()
  let has_c = query(selector(<page_marker>)).any(m => {{
    let pos = m.location().position()
    pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
  }})
  if not has_c {{
    none
  }} else if in_frontmatter.get() {{
    let page_num = counter(page).get().first()
    if page_num >= 5 {{
      let display_val = counter(page).display("i")
      if calc.even(page_num) {{
        align(left + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
      }} else {{
        align(right + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
      }}
    }}
  }} else {{
    let page_num = counter(page).get().first()
    let display_val = counter(page).display("1")
    let titles_en = query(selector(<chapter_title_en>)).filter(m => m.location().page() <= p)
    let chapter_en = if titles_en.len() > 0 {{ titles_en.last().value }} else {{ "" }}
    if calc.even(page_num) {{
      grid(
        columns: (auto, auto),
        align: horizon,
        column-gutter: 8pt,
        page_badge(display_val),
        text(8pt, font: ("Metropolis", "Liberation Sans"), style: "italic", fill: running_title_color)[{nama_en.upper()} DISTRICT IN FIGURES {tahun_rilis}]
      )
    }} else {{
      let right_en_text = if chapter_en != "" {{ upper(chapter_en) }} else {{ "{nama_en.upper()} DISTRICT IN FIGURES {tahun_rilis}" }}
      grid(
        columns: (1fr, auto),
        align: horizon,
        column-gutter: 8pt,
        align(right, text(8pt, font: ("Metropolis", "Liberation Sans"), style: "italic", fill: running_title_color)[#right_en_text]),
        page_badge(display_val)
      )
    }}
  }}
}}

#set page(
  paper: "a5",
  margin: normal_margins,
  header-ascent: 40%,
  footer-descent: 20%,
  header: page_header,
  footer: page_footer,
)

#set text(font: ("Myriad Pro", "Liberation Sans"), size: 7.5pt, lang: "id")
#set par(justify: true, leading: 0.5em)

#show table.cell: set par(justify: false)
#show figure.where(kind: image): set figure(supplement: none)
#show figure.where(kind: image): set figure.caption(separator: none)
"""

    daftar_pustaka_markup = f"""
// ==========================================
// DAFTAR PUSTAKA (BIBLIOGRAPHY)
// ==========================================
#pagebreak()
#metadata("DAFTAR PUSTAKA") <chapter_title>
#metadata("BIBLIOGRAPHY") <chapter_title_en>
#metadata("daftar_pustaka") <daftar_pustaka>
#v(0.5cm)
#block[
  #text(12pt, weight: "bold")[DAFTAR PUSTAKA] \\
  #text(9pt, style: "italic", fill: rgb("#4B5563"))[BIBLIOGRAPHY]
]
#v(10pt)

#text(8pt)[
  {instansi_info.get("nama_resmi", "Badan Pusat Statistik")}. {tahun_data}. _{nama_kabupaten} Dalam Angka {tahun_data}_. {nama_kabupaten_singkat}: {instansi_info.get("nama_singkat", "BPS")}.

  #v(8pt)
  Badan Pusat Statistik. 2024. _Indikator Pertanian 2023/2024_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Badan Pusat Statistik. 2023. _Statistik Indonesia 2023_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Badan Pusat Statistik. 2022. _Buku 3: Konsep dan Definisi Podes 2022_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Direktorat Statistik Ketahanan Sosial. 2024. _Buku 3: Pedoman Konsep dan Definisi Podes 2024_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Kementerian Pertanian & Badan Pusat Statistik. 2023. _Pedoman Statistik Pertanian Hortikultura (SPH)_. Jakarta: Kementerian Pertanian.
]
#metadata("akhir_buku") <akhir_buku>
"""

    # Assemble Document
    parts = [
        header_logic,
        render_frontmatter(cfg),
        """
#metadata("transisi_isi") <transisi_isi>
""",
        render_chapter1(cfg, out_dir=out_dir),
        render_chapter2(cfg, out_dir=out_dir),
        render_chapter3(cfg, out_dir=out_dir),
        render_chapter4(cfg, out_dir=out_dir),
        render_chapter5(cfg, out_dir=out_dir),
        render_chapter6(cfg, out_dir=out_dir),
        render_chapter7(cfg, out_dir=out_dir),
        daftar_pustaka_markup,
        render_backcover(cfg)
    ]

    return "\n".join(parts)

