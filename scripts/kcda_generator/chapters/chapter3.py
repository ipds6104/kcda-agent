"""Chapter 3: Kependudukan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value, match_village_row
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter3_charts
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter3(cfg: Dict[str, Any], out_dir: Optional[Any] = None, fig_no: int = 4) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_kab_en = regency.get("nama_en", "Mempawah Regency")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    desa_list = cfg.get("desa_list", [])
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter3_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None, fig_no=fig_no)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    # --- 3.1 Penduduk ---
    rows_31_raw = get_kecamatan_tab_rows("3.1", nama_singkat)
    t31_p1_map = {}
    t31_p2_map = {}
    tot_lk, tot_pr, tot_all = "–", "–", "–"
    tot_pct, tot_kpd, tot_rasio = "100,00", "–", "–"

    for r in rows_31_raw:
        if any("2024" in str(c) for c in r):
            break
        if len(r) > 3 and r[0].strip():
            first_cell = r[0].strip()
            if any(first_cell.lower().startswith(x) for x in ['desa', 'tabel', 'sumber', 'catatan', '2025', 'no']):
                continue
            if any(first_cell.lower().startswith(x) for x in ['jumlah', 'total', 'kecamatan']):
                tot_lk = clean_cell_value(r[1])
                tot_pr = clean_cell_value(r[2])
                tot_all = clean_cell_value(r[3])
                if len(r) > 5:
                    tot_kpd = clean_cell_value(r[5])
                if len(r) > 6:
                    tot_rasio = clean_cell_value(r[6])
                continue

            d_name = first_cell
            lk = clean_cell_value(r[1])
            pr = clean_cell_value(r[2])
            tot = clean_cell_value(r[3])
            pct = clean_cell_value(r[4] if len(r) > 4 else "–")
            kpd = clean_cell_value(r[5] if len(r) > 5 else "–")
            rasio = clean_cell_value(r[6] if len(r) > 6 else "–")

            t31_p1_map[d_name.lower()] = [d_name, lk, pr, tot]
            t31_p2_map[d_name.lower()] = [d_name, pct, kpd, rasio]

    valid_kpd = []
    for d in desa_list:
        row = match_village_row(t31_p2_map, d)
        if row:
            try:
                kpd_f = float(row[2].replace('.', '').replace(',', '.'))
                pct_f = float(row[1].replace(',', '.'))
                valid_kpd.append((d, kpd_f, row[2], pct_f, row[1]))
            except Exception:
                pass

    if valid_kpd:
        valid_kpd.sort(key=lambda x: x[1])
        lowest_kpd = valid_kpd[0]
        highest_kpd = valid_kpd[-1]
        valid_kpd.sort(key=lambda x: x[3])
        smallest_pop = valid_kpd[0]
        largest_pop = valid_kpd[-1]

        teks_jml_id = (
            f"Penduduk Kecamatan {nama_singkat} pada tahun 2025 tercatat sebanyak {tot_all} jiwa, "
            f"terdiri atas {tot_lk} jiwa laki-laki dan {tot_pr} jiwa perempuan. "
            f"Komposisi ini menghasilkan rasio jenis kelamin sebesar {tot_rasio}, "
            f"yang mengindikasikan terdapat sekitar {tot_rasio.split(',')[0]} penduduk laki-laki "
            f"untuk setiap 100 penduduk perempuan di wilayah ini."
        )
        teks_jml_en = (
            f"The population of {nama_en} District in 2025 was recorded at {tot_all} people, "
            f"comprising {tot_lk} males and {tot_pr} females. "
            f"This composition yields a sex ratio of {tot_rasio}, "
            f"indicating approximately {tot_rasio.split(',')[0]} males for every 100 females in this district."
        )

        teks_kpd_id = (
            f"Kepadatan penduduk di Kecamatan {nama_singkat} mencapai rata-rata sekitar {tot_kpd} jiwa per kilometer persegi. "
            f"Penyebaran penduduk belum merata antardesa, di mana Desa {highest_kpd[0]} memiliki kepadatan tertinggi mencapai {highest_kpd[2]} jiwa/km², "
            f"sedangkan Desa {lowest_kpd[0]} mencatat kepadatan terendah sebesar {lowest_kpd[2]} jiwa/km².\\\n\\\n"
            f"Dari sisi konsentrasi penduduk, {largest_pop[0]} merupakan desa dengan proporsi penduduk terbesar ({largest_pop[4]} persen), "
            f"sementara proporsi penduduk terkecil berada di {smallest_pop[0]} ({smallest_pop[4]} persen)."
        )
        teks_kpd_en = (
            f"The average population density in {nama_en} District reaches approximately {tot_kpd} people per square kilometer. "
            f"Population distribution is not evenly distributed across villages; {highest_kpd[0]} village has the highest density at {highest_kpd[2]} people/sq.km, "
            f"while {lowest_kpd[0]} village records the lowest at {lowest_kpd[2]} people/sq.km.\\\n\\\n"
            f"In terms of population concentration, {largest_pop[0]} has the largest share ({largest_pop[4]} percent), "
            f"whereas the smallest share is found in {smallest_pop[0]} ({smallest_pop[4]} percent)."
        )

        ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Perkembangan Penduduk dan Rasio Jenis Kelamin] \\
  #v(2pt)
  {teks_jml_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Distribusi dan Kepadatan Penduduk] \\
  #v(2pt)
  {teks_kpd_id}
]"""

        ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Population Growth and Sex Ratio] \\
  #v(2pt)
  {teks_jml_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Population Distribution and Density] \\
  #v(2pt)
  {teks_kpd_en}
]"""
    else:
        ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Kependudukan] \\
  #v(2pt)
  Penduduk Kecamatan {nama_singkat} pada tahun 2025 berjumlah {tot_all} jiwa dengan kepadatan penduduk {tot_kpd} jiwa/km².
]"""
        ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Population] \\
  #v(2pt)
  The population of {nama_en} District in 2025 totaled {tot_all} people with a density of {tot_kpd} people/sq.km.
]"""

    technical_notes_bab3 = [
        (
            "Kepadatan penduduk adalah angka yang menyatakan banyaknya penduduk per kilometer persegi, dihitung dengan perbandingan antara banyaknya penduduk terhadap luas wilayah.",
            "The population density is a figure that states the number of residents per square kilometer, calculated by comparison between the population of the area."
        ),
        (
            "Rasio jenis kelamin adalah perbandingan antara jumlah penduduk laki-laki dan jumlah penduduk perempuan pada suatu daerah dan waktu tertentu, yang biasanya dinyatakan dalam banyaknya penduduk laki-laki perseratus penduduk perempuan.",
            "Sex ratio is a comparison between the number of male population and the number of female population at a given area and time, which is usually expressed in the number of male population per hundred female population."
        )
    ]

    bab3_intro = render_chapter_intro(
        chapter_num=3,
        title_id="PENDUDUK",
        title_en="POPULATION",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab3
    )

    t31_p1_rows = []
    t31_p2_rows = []
    for d in desa_list:
        row1 = match_village_row(t31_p1_map, d)
        row2 = match_village_row(t31_p2_map, d)
        v1 = [d, row1[1], row1[2], row1[3]] if row1 else [d, "–", "–", "–"]
        v2 = [d, row2[1], row2[2], row2[3]] if row2 else [d, "–", "–", "–"]
        t31_p1_rows.append(v1)
        t31_p2_rows.append(v2)

    t31_p1_rows.append([f"Kecamatan {nama_singkat}", tot_lk, tot_pr, tot_all])
    t31_p2_rows.append([f"Kecamatan {nama_singkat}", "100,00", tot_kpd, tot_rasio])

    source_txt = f"Dinas Kependudukan dan Pencatatan Sipil {nama_kab}/Population and Civil Registration Service of {nama_kab_en}"

    # Halaman 1 dari Tabel 3.1
    t31_p1_markup = render_typst_table(
        table_no="3.1",
        title_id=f"Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Population, Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in {nama_en} District, 2025",
        headers=[
            "Desa/Kelurahan\nVillage/Subdistrict",
            "Laki-laki\nMale",
            "Perempuan\nFemale",
            "Jumlah\nTotal"
        ],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t31_p1_rows,
        col_widths=["2.6fr", "1.1fr", "1.1fr", "1.2fr"],
        source=source_txt
    )

    # Halaman 2 dari Tabel 3.1 (Lanjutan)
    t31_p2_markup = render_typst_table(
        table_no="3.1 Lanjutan",
        title_id="",
        title_en="",
        headers=[
            "Desa/Kelurahan\nVillage/Subdistrict",
            "Distribusi Penduduk\nPopulation Distribution (%)",
            "Kepadatan Penduduk (per km²)\nPopulation Density per sq.km",
            "Rasio Jenis Kelamin Penduduk\nPopulation Sex Ratio"
        ],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t31_p2_rows,
        col_widths=["2.4fr", "1.2fr", "1.2fr", "1.2fr"],
        source=source_txt,
        is_continued=True
    )

    return f"""
// ==========================================
// BAB 3: PENDUDUK (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================
{bab3_intro}
{chart_section}
// ==========================================
// TABEL DATA BAB 3 (FORMAT 2 HALAMAN)
// ==========================================
{t31_p1_markup}
#pagebreak()

{t31_p2_markup}
"""
