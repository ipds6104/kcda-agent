"""
Chapter-specific Chart Extractors for KCDA 2026.
Mengekstrak data dari Google Sheets / tabel lokal dan menghasilkan markup gambar Typst.
"""

from pathlib import Path
from typing import Optional
from ..data_loader import get_kecamatan_tab_rows
from ..table_renderer import format_bilingual_source
from ..config import get_regency_info
from .svg_engine import (
    parse_number,
    format_figure_header,
    generate_horizontal_bar_chart,
    generate_grouped_horizontal_bar_chart
)

def get_chapter1_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 1 (Geografi & Iklim):
    Gambar 1.1: Jarak dari Desa/Kelurahan ke Ibukota Kecamatan (km) [Tabel 1.2 - Terurut Menurun]
    Gambar 1.2: Luas Wilayah menurut Desa/Kelurahan (km²) [Tabel 1.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    figures = []

    # 1. Gambar 1.1: Jarak ke Ibukota Kecamatan (Tabel 1.2) - Terurut Menurun
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
        chart_path = charts_dir / "gambar_1_1.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
        fig_header = format_figure_header(
            "1.1",
            f"Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di {nama_singkat}, 2025 (km)",
            f"Distance from Village/Subdistrict to District Capital in {nama_en}, 2025 (km)"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_1_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        figures.append(fig_typst)

    # 2. Gambar 1.2: Luas Wilayah (Tabel 1.1) - Terurut Menurun & Tanpa Baris Total
    rows_1_1 = get_kecamatan_tab_rows("1.1.", nama_singkat)
    luas_labels = []
    luas_values = []
    for r in rows_1_1[3:]:
        if len(r) > 7 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            if any(r[0].strip().lower() == l.lower() for l in luas_labels):
                break
            num = parse_number(r[7])
            if num is not None and num > 0:
                luas_labels.append(r[0].strip())
                luas_values.append(num)

    if len(luas_values) >= 2:
        svg_code_luas = generate_horizontal_bar_chart(luas_labels, luas_values, unit="km²", color="#0284C7", sort_descending=True)
        chart_path_luas = charts_dir / "gambar_1_2.svg"
        chart_path_luas.write_text(svg_code_luas, encoding="utf-8")

        reg = get_regency_info()
        nama_kab = reg.get("nama_resmi", "Kabupaten")
        src_fmt_luas = format_bilingual_source(f"Dinas Kependudukan dan Pencatatan Sipil / BAPEDDA {nama_kab}")
        fig_header_luas = format_figure_header(
            "1.2",
            f"Luas Wilayah menurut Desa/Kelurahan di {nama_singkat}, 2025 (km²)",
            f"Total Area by Village/Subdistrict in {nama_en}, 2025 (sq.km)"
        )
        fig_luas = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_1_2.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt_luas}]
#v(4pt)
{fig_header_luas}
#v(10pt)
"""
        figures.append(fig_luas)

    return "\n".join(figures)

def get_chapter2_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 2 (Pemerintahan):
    Gambar 2.1: Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan [Tabel 2.1.1 - Terurut Menurun]
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
    chart_path = charts_dir / "gambar_2_1.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
    fig_header = format_figure_header(
        "2.1",
        f"Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan di {nama_singkat}, 2025",
        f"Number of Neighborhood Units (RT) by Village/Subdistrict in {nama_en}, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_2_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst

def get_chapter3_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 3 (Kependudukan):
    Gambar 3.1: Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan [Tabel 3.1 - Terurut Menurun]
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
    chart_path = charts_dir / "gambar_3_1.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    reg = get_regency_info()
    nama_kab = reg.get("nama_resmi", "Kabupaten")
    src_fmt = format_bilingual_source(f"Dinas Kependudukan dan Pencatatan Sipil {nama_kab} (Semester II 2025)")
    fig_header = format_figure_header(
        "3.1",
        f"Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan di {nama_singkat}, 2025",
        f"Population by Sex and Village/Subdistrict in {nama_en}, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_3_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst

def get_chapter4_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 4 (Sosial & Pendidikan):
    Gambar 4.1: Perkembangan Jumlah Sekolah Dasar (SD) 2022–2025.
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
                chart_path = charts_dir / "gambar_4_1.svg"
                chart_path.write_text(svg_code, encoding="utf-8")

                src_fmt = format_bilingual_source("BPS, Pendataan Potensi Desa (Podes) 2025")
                fig_header = format_figure_header(
                    "4.1",
                    f"Perkembangan Jumlah Sekolah Dasar (SD) di {nama_singkat}, 2022–2025",
                    f"Number of Primary Schools (SD) in {nama_en}, 2022–2025"
                )
                fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_4_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
                return fig_typst

    return ""

def get_chapter5_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 5 (Pertanian):
    Gambar 5.1: Produksi Tanaman Sayuran / Buah-buahan.
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
        chart_path = charts_dir / "gambar_5_1.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source("BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)")
        fig_header = format_figure_header(
            "5.1",
            f"Produksi Buah-buahan Utama di {nama_singkat}, 2025 (Kuintal)",
            f"Production of Major Fruits in {nama_en}, 2025 (Quintal)"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_5_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        return fig_typst

    return ""
