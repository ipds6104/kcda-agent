"""
Chapter-specific Chart Extractors for KCDA 2026.
Mengekstrak data dari Google Sheets / tabel lokal dan menghasilkan markup gambar Typst.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from ..data_loader import get_kecamatan_tab_rows
from ..table_renderer import format_bilingual_source
from ..config import get_regency_info
from .svg_engine import (
    parse_number,
    format_figure_header,
    generate_horizontal_bar_chart,
    generate_grouped_horizontal_bar_chart
)

def get_chapter1_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path], fig_no: int = 2) -> str:
    """
    Menghasilkan visualisasi Bab 1 (Geografi & Iklim):
    Gambar {fig_no}: Jarak dari Desa/Kelurahan ke Ibukota Kecamatan (km) [Tabel 1.2 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_1_2 = get_kecamatan_tab_rows("1.2.", nama_singkat)
    labels = []
    values = []
    for r in rows_1_2[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            num = parse_number(r[1])
            if num is not None and num > 0:
                labels.append(r[0].strip())
                values.append(num)

    if len(values) >= 2:
        svg_code = generate_horizontal_bar_chart(labels, values, unit="km", color="#F5A623", sort_descending=True)
        chart_path = charts_dir / f"gambar_{fig_no}.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
        fig_header = format_figure_header(
            str(fig_no),
            f"Jarak ke Ibukota Kecamatan Menurut Desa/Kelurahan di Kecamatan {nama_singkat} (km), 2025",
            f"Distance to District Capital by Village/Subdistrict in {nama_en} District (km), 2025"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_{fig_no}.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        return fig_typst

    return ""

def get_chapter2_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path], fig_no: int = 3) -> str:
    """
    Menghasilkan visualisasi Bab 2 (Pemerintahan):
    Gambar {fig_no}: Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan [Tabel 2.1.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_2_1_1 = get_kecamatan_tab_rows("2.1.1", nama_singkat)
    labels = []
    values = []
    for r in rows_2_1_1[3:]:
        if len(r) > 3 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            num = parse_number(r[3])
            if num is not None and num > 0:
                labels.append(r[0].strip())
                values.append(num)

    if len(values) < 2:
        return ""

    svg_code = generate_horizontal_bar_chart(labels, values, unit="RT", color="#0284C7", sort_descending=True)
    chart_path = charts_dir / f"gambar_{fig_no}.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
    fig_header = format_figure_header(
        str(fig_no),
        f"Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025",
        f"Number of RT by Village/Subdistrict in {nama_en} District, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_{fig_no}.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst

def get_chapter3_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path], fig_no: int = 4) -> str:
    """
    Menghasilkan visualisasi Bab 3 (Kependudukan):
    Gambar {fig_no}: Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan [Tabel 3.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_3_1 = get_kecamatan_tab_rows("3.1", nama_singkat)
    labels = []
    male_vals = []
    female_vals = []

    for r in rows_3_1[3:]:
        if len(r) > 2 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            if any(r[0].strip().lower() == l.lower() for l in labels):
                break
            m = parse_number(r[1])
            f = parse_number(r[2])
            if m is not None and f is not None and (m > 0 or f > 0):
                labels.append(r[0].strip())
                male_vals.append(m)
                female_vals.append(f)

    if len(labels) < 2:
        return ""

    series = [
        {"name": "Laki-laki / Male", "color": "#0284C7", "values": male_vals},
        {"name": "Perempuan / Female", "color": "#F5A623", "values": female_vals}
    ]

    svg_code = generate_grouped_horizontal_bar_chart(labels, series, sort_descending=True)
    chart_path = charts_dir / f"gambar_{fig_no}.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    reg = get_regency_info()
    nama_kab = reg.get("nama_resmi", "Kabupaten")
    src_fmt = format_bilingual_source(f"Dinas Kependudukan dan Pencatatan Sipil {nama_kab} (Semester II 2025)")
    fig_header = format_figure_header(
        str(fig_no),
        f"Jumlah Penduduk Menurut Jenis Kelamin dan Desa/Kelurahan di Kecamatan {nama_singkat}, 2025",
        f"Population by Sex and Village/Subdistrict in {nama_en} District, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_{fig_no}.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst

def get_chapter4_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path], fig_no: int = 5) -> str:
    """
    Menghasilkan visualisasi Bab 4 (Sosial & Pendidikan):
    Gambar {fig_no}: Perkembangan Jumlah Sekolah Dasar (SD) 2022–2025.
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_4_1_1 = get_kecamatan_tab_rows("4.1.1", nama_singkat)
    for r in rows_4_1_1:
        if len(r) > 4 and "sekolah dasar" in r[0].lower():
            vals = [parse_number(x) for x in r[1:5]]
            valid_vals = [v for v in vals if v is not None and v > 0]
            if len(valid_vals) >= 2:
                years = ["2022", "2023", "2024", "2025"]
                filtered_years = []
                filtered_nums = []
                for y, v in zip(years, vals):
                    if v is not None:
                        filtered_years.append(y)
                        filtered_nums.append(v)

                svg_code = generate_horizontal_bar_chart(filtered_years, filtered_nums, unit="Unit", color="#10B981", sort_descending=False)
                chart_path = charts_dir / f"gambar_{fig_no}.svg"
                chart_path.write_text(svg_code, encoding="utf-8")

                src_fmt = format_bilingual_source("BPS, Pendataan Potensi Desa (Podes) 2025")
                fig_header = format_figure_header(
                    str(fig_no),
                    f"Perkembangan Jumlah Sekolah Dasar (SD) di Kecamatan {nama_singkat}, 2022–2025",
                    f"Number of Primary Schools (SD) in {nama_en} District, 2022–2025"
                )
                fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_{fig_no}.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
                return fig_typst

    return ""

def get_chapter5_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path], fig_no: int = 5) -> str:
    """
    Menghasilkan visualisasi Bab 5 (Pertanian):
    Gambar {fig_no}: Produksi Tanaman Sayuran / Buah-buahan.
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_5_7 = get_kecamatan_tab_rows("5.7", nama_singkat)
    labels = []
    values = []
    for r in rows_5_7[3:]:
        if len(r) > 4 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "buah"]):
            num = parse_number(r[4])
            if num is not None and num > 0:
                name = r[0].split("/")[0].strip()
                labels.append(name)
                values.append(num)

    if len(values) >= 2:
        svg_code = generate_horizontal_bar_chart(labels[:8], values[:8], unit="Kuintal", color="#F5A623", sort_descending=True)
        chart_path = charts_dir / f"gambar_{fig_no}.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source("BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)")
        fig_header = format_figure_header(
            str(fig_no),
            f"Produksi Buah-buahan Utama di Kecamatan {nama_singkat}, 2025 (Kuintal)",
            f"Production of Major Fruits in {nama_en} District, 2025 (Quintal)"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_{fig_no}.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        return fig_typst

    return ""


def get_subdistrict_figures(slug: str, nama_singkat: str, nama_en: str) -> List[Dict[str, Any]]:
    """
    Mendeteksi seluruh Gambar (Peta dan Grafik) yang benar-benar aktif untuk suatu kecamatan,
    dan memberikan penomoran berurutan 1, 2, 3, dst. secara kontinu.
    """
    figs = []
    # 1. Gambar 1: Peta Wilayah Kecamatan
    figs.append({
        "num": 1,
        "title_id": f"Peta Wilayah Kecamatan {nama_singkat}, 2025",
        "title_en": f"Map of {nama_en} District, 2025",
        "label": "fig_1",
        "chapter": 1
    })

    # 2. Bab 1: Jarak ke Ibukota Kecamatan (Tabel 1.2)
    r12 = get_kecamatan_tab_rows("1.2.", nama_singkat)
    v12 = [r for r in r12[3:] if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]) and parse_number(r[1]) and parse_number(r[1]) > 0]
    if len(v12) >= 2:
        num = len(figs) + 1
        figs.append({
            "num": num,
            "title_id": f"Jarak ke Ibukota Kecamatan Menurut Desa/Kelurahan di Kecamatan {nama_singkat} (km), 2025",
            "title_en": f"Distance to District Capital by Village/Subdistrict in {nama_en} District (km), 2025",
            "label": f"fig_{num}",
            "chapter": 1
        })

    # 3. Bab 2: Jumlah RT (Tabel 2.1.1)
    r211 = get_kecamatan_tab_rows("2.1.1", nama_singkat)
    v211 = [r for r in r211[3:] if len(r) > 3 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]) and parse_number(r[3]) and parse_number(r[3]) > 0]
    if len(v211) >= 2:
        num = len(figs) + 1
        figs.append({
            "num": num,
            "title_id": f"Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025",
            "title_en": f"Number of RT by Village in {nama_en} District, 2025",
            "label": f"fig_{num}",
            "chapter": 2
        })

    # 4. Bab 3: Jumlah Penduduk menurut Jenis Kelamin (Tabel 3.1)
    r31 = get_kecamatan_tab_rows("3.1", nama_singkat)
    v31 = [r for r in r31[3:] if len(r) > 2 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]) and (parse_number(r[1]) or parse_number(r[2]))]
    if len(v31) >= 2:
        num = len(figs) + 1
        figs.append({
            "num": num,
            "title_id": f"Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan {nama_singkat}, 2025",
            "title_en": f"Population by Sex in {nama_en} District, 2025",
            "label": f"fig_{num}",
            "chapter": 3
        })

    # 5. Bab 5: Produksi Buah-buahan Utama (Tabel 5.7)
    r57 = get_kecamatan_tab_rows("5.7", nama_singkat)
    v57 = [r for r in r57[3:] if len(r) > 4 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "buah"]) and parse_number(r[4]) and parse_number(r[4]) > 0]
    if len(v57) >= 2:
        num = len(figs) + 1
        figs.append({
            "num": num,
            "title_id": f"Produksi Tanaman Hortikultura Unggulan di Kecamatan {nama_singkat}, 2025",
            "title_en": f"Production of Leading Horticulture Crops in {nama_en} District, 2025",
            "label": f"fig_{num}",
            "chapter": 5
        })

    return figs
