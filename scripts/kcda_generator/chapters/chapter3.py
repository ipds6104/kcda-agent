"""Chapter 3: Kependudukan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter3_charts
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter3(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_kab_en = regency.get("nama_en", "Mempawah Regency")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    desa_list = cfg.get("desa_list", [])
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter3_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    # --- 3.1 Penduduk ---
    rows_31_raw = get_kecamatan_tab_rows("3.1", nama_singkat)
    t31_p1_map = {}
    t31_p2_map = {}
    tot_lk, tot_pr, tot_all = "–", "–", "–"
    tot_pct, tot_kpd, tot_rasio = "100,00", "–", "–"

    for r in rows_31_raw:
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
    for d, row in t31_p2_map.items():
        try:
            kpd_f = float(row[2].replace('.', '').replace(',', '.'))
            pct_f = float(row[1].replace(',', '.'))
            valid_kpd.append((row[0], kpd_f, row[2], pct_f, row[1]))
        except Exception:
            pass

    if valid_kpd:
        valid_kpd.sort(key=lambda x: x[1])
        lowest_kpd = valid_kpd[0]
        highest_kpd = valid_kpd[-1]
        valid_kpd.sort(key=lambda x: x[3])
        largest_pop = valid_kpd[-1]

        ulasan_kpd_id = (
            f"Penduduk Kecamatan {nama_singkat} pada tahun 2025 berjumlah sekitar {tot_all} jiwa "
            f"dengan kepadatan penduduk sekitar {tot_kpd} jiwa per kilometer persegi.\\\n\\\n"
            f"Penyebaran penduduk di Kecamatan {nama_singkat} tidak merata antar desa yang satu dengan desa lainnya. "
            f"Desa {highest_kpd[0]} merupakan desa dengan tingkat kepadatan penduduk tertinggi yaitu {highest_kpd[2]} jiwa/km². "
            f"Sebaliknya, desa {lowest_kpd[0]} memiliki tingkat kepadatan terendah yaitu sekitar {lowest_kpd[2]} jiwa/km².\\\n\\\n"
            f"{largest_pop[0]} adalah desa dengan persentase penduduk terbesar di Kecamatan {nama_singkat}, "
            f"yaitu sekitar {largest_pop[4]} persen dari total penduduk di Kecamatan {nama_singkat}. "
            f"Rasio jenis kelamin sekitar {tot_rasio}, yang artinya terdapat sekitar {tot_rasio.split(',')[0]} penduduk laki-laki "
            f"untuk setiap 100 penduduk perempuan di Kecamatan {nama_singkat} pada Tahun 2025."
        )

        ulasan_kpd_en = (
            f"The population of {nama_en} District in 2025 totaled about {tot_all} people "
            f"with a population density of about {tot_kpd} people per square kilometer.\\\n\\\n"
            f"The spread of residents in {nama_en} District is not even between villages. "
            f"{highest_kpd[0]} village has the highest population density rate of {highest_kpd[2]} people/sq.km. "
            f"In contrast, {lowest_kpd[0]} village has the lowest density of about {lowest_kpd[2]} people/sq.km.\\\n\\\n"
            f"{largest_pop[0]} is the village with the largest percentage of population in {nama_en} District, "
            f"which is about {largest_pop[4]} percent of the total population. "
            f"The sex ratio is about {tot_rasio}, meaning there are about {tot_rasio.split(',')[0]} male population "
            f"for every 100 female residents in {nama_en} District in 2025."
        )
    else:
        ulasan_kpd_id = f"Penduduk Kecamatan {nama_singkat} pada tahun 2025 berjumlah {tot_all} jiwa dengan kepadatan penduduk {tot_kpd} jiwa/km²."
        ulasan_kpd_en = f"The population of {nama_en} District in 2025 totaled {tot_all} people with a density of {tot_kpd} people/sq.km."

    # Penjelasan Teknis & Ulasan Bab 3
    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Kependudukan] \\
  #v(2pt)
  {ulasan_kpd_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Population] \\
  #v(2pt)
  {ulasan_kpd_en}
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
        v1 = t31_p1_map.get(d.lower(), [d, "–", "–", "–"])
        v2 = t31_p2_map.get(d.lower(), [d, "–", "–", "–"])
        t31_p1_rows.append(v1)
        t31_p2_rows.append(v2)

    t31_p1_rows.append([f"Kecamatan {nama_singkat} / Total", tot_lk, tot_pr, tot_all])
    t31_p2_rows.append([f"Kecamatan {nama_singkat} / Total", "100,00", tot_kpd, tot_rasio])

    source_txt = f"Dinas Kependudukan dan Pencatatan Sipil {nama_kab} (Semester II 2025) / Population and Civil Registration Service of {nama_kab_en} (Semester II 2025)"

    # Halaman 1 dari Tabel 3.1
    t31_p1_markup = render_typst_table(
        table_no="3.1",
        title_id=f"Penduduk Menurut Desa/Kelurahan dan Jenis Kelamin di {nama_resmi}, 2025",
        title_en=f"Population by Villages/Subdistricts and Sex in {nama_en} District, 2025",
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
        table_no="3.1 Lanjutan/Continued",
        title_id=f"Distribusi Persentase Penduduk, Kepadatan Penduduk, dan Rasio Jenis Kelamin Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in {nama_en} District, 2025",
        headers=[
            "Desa/Kelurahan\nVillage/Subdistrict",
            "Persentase Penduduk\nPercentage of Total Population (%)",
            "Kepadatan Penduduk (per km²)\nPopulation Density per sq.km",
            "Rasio Jenis Kelamin Penduduk\nPopulation Sex Ratio"
        ],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t31_p2_rows,
        col_widths=["2.4fr", "1.2fr", "1.2fr", "1.2fr"],
        source=source_txt
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
