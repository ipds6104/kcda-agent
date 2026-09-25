"""Chapter 1: Geografi dan Iklim Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter1_charts
from ..config import get_regency_info

def render_chapter1(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten")
    nama_kab_en = regency.get("nama_en", "Regency")
    ibukota_kab = regency.get("ibukota_kabupaten", "Ibukota Kabupaten")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    ibukota = cfg["ibukota_kecamatan"]
    desa_list = cfg["desa_list"]
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter1_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else "\n#v(8pt)\n"

    # --- 1.1 Luas Daerah ---
    rows_1_1_raw = get_kecamatan_tab_rows("1.1.", nama_singkat)
    luas_map = {}
    total_luas = "..."
    for r in rows_1_1_raw[3:]:
        if len(r) > 1 and r[0].strip():
            nama_d = r[0].strip()
            if nama_d.isdigit() or any(nama_d.lower().startswith(x) for x in ['desa/kelurahan', 'kelurahan/desa', 'tabel']):
                continue
            if any(nama_d.lower().startswith(x) for x in ['jumlah', 'total', 'kecamatan']):
                if len(r) > 7 and r[7].strip() and total_luas == "...":
                    total_luas = clean_cell_value(r[7])
                continue
            if any(nama_d.lower().startswith(x) for x in ['sumber', 'catatan']):
                continue

            if nama_d.lower() not in luas_map:
                luas_val = clean_cell_value(r[7] if len(r) > 7 else r[1])
                pct_val = clean_cell_value(r[8] if len(r) > 8 else "...")
                status_val = clean_cell_value(r[9] if len(r) > 9 else "Indikatif")
                luas_map[nama_d.lower()] = [luas_val, pct_val, status_val]

    t1_1_rows = []
    for d in desa_list:
        v = luas_map.get(d.lower(), ["...", "...", "Indikatif"])
        t1_1_rows.append([d, v[0], v[1], v[2]])

    t1_1_rows.append([f"Kecamatan {nama_singkat} / Total", total_luas, "100,00", ""])

    t1_1_markup = render_typst_table(
        table_no="1.1",
        title_id=f"Luas Daerah Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Total Area by Village/Subdistrict in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Luas Daerah\nTotal Area (km²)", "Persentase\nPercentage (%)", "Status Batas\nBoundary Status"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t1_1_rows,
        col_widths=["2.2fr", "1.1fr", "1.0fr", "1.3fr"],
        source=f"BAPEDDA/Dinas Terkait {nama_kab} / Regional Development Planning Agency of {nama_kab_en}",
        note="Untuk desa/kelurahan dengan status Indikatif masih perlu dilakukan pelacakan ke lapangan dan kesepakatan batas antarwilayah yang berbatasan. / For villages/subdistricts with Indicative status, field tracking and boundary agreements between adjacent areas are still required."
    )

    # --- 1.2 Jarak ke Ibukota Kecamatan & Kabupaten ---
    rows_1_2_raw = get_kecamatan_tab_rows("1.2.", nama_singkat)
    jarak_map = {}
    for r in rows_1_2_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            j_kec = clean_cell_value(r[1] if len(r) > 1 else "...")
            j_kab = clean_cell_value(r[2] if len(r) > 2 else "...")
            jarak_map[r[0].strip().lower()] = [j_kec, j_kab]

    t1_2_rows = []
    for d in desa_list:
        v = jarak_map.get(d.lower(), ["...", "..."])
        t1_2_rows.append([d, v[0], v[1]])

    t1_2_markup = render_typst_table(
        table_no="1.2",
        title_id=f"Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Distance to Subdistrict and Regency Capital by Village in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Ke Ibukota Kec.\nTo District Capital (km)", "Ke Ibukota Kab.\nTo Regency Capital (km)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_2_rows,
        col_widths=["2.5fr", "1.3fr", "1.3fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 1.3 Batas Administrasi ---
    rows_1_3_raw = get_kecamatan_tab_rows("1.3.", nama_singkat)
    t1_3_rows = []
    for r in rows_1_3_raw[3:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            arah = clean_cell_value(r[1])
            batas = clean_cell_value(r[2])
            no_idx = clean_cell_value(r[0])
            t1_3_rows.append([no_idx, arah, batas])
    if not t1_3_rows:
        t1_3_rows = [
            ["1", "Utara/North", "..."],
            ["2", "Selatan/South", "..."],
            ["3", "Barat/West", "..."],
            ["4", "Timur/East", "..."]
        ]

    t1_3_markup = render_typst_table(
        table_no="1.3",
        title_id=f"Batas Administrasi {nama_resmi} Menurut Arah Mata Angin, 2025",
        title_en=f"Administrative Borders of {nama_en} by Cardinal Direction, 2025",
        headers=["No", "Arah Mata Angin\nWind Direction", "Berbatasan Dengan\nBordering With"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_3_rows,
        col_widths=["0.6fr", "1.8fr", "3.0fr"],
        source=f"Kantor Camat {nama_singkat} / Bagian Tata Pemerintahan Setda {regency.get('nama_singkat', '')}"
    )

    # --- 1.4 Jarak Kantor Camat ke Tempat Penting ---
    rows_1_4_raw = get_kecamatan_tab_rows("1.4.", nama_singkat)
    t1_4_rows = []
    for r in rows_1_4_raw[3:]:
        if len(r) > 1 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            tempat = clean_cell_value(r[1])
            jarak = clean_cell_value(r[2] if len(r) > 2 else "...")
            no_idx = clean_cell_value(r[0])
            t1_4_rows.append([no_idx, tempat, jarak])
    if not t1_4_rows:
        t1_4_rows = [
            ["1", "Ibukota Provinsi", "..."],
            ["2", f"Ibukota Kabupaten ({ibukota_kab})", "..."],
            ["3", "Bandara Terdekat", "..."],
            ["4", "Pelabuhan Terdekat", "..."]
        ]

    t1_4_markup = render_typst_table(
        table_no="1.4",
        title_id=f"Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025",
        title_en=f"Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025",
        headers=["No", "Nama Kota dan Tempat Penting\nOther Important Places", "Jarak\nDistance (km)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_4_rows,
        col_widths=["0.6fr", "3.2fr", "1.2fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # Infografis Halaman Bab 1
    infografis_markup = f"\n{charts_markup}\n" if charts_markup.strip() else """
#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS GEOGRAFI & IKLIM]\
      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan """ + nama_singkat + """]
    ]
  ]
]
"""

    return f"""
// ==========================================
// BAB 1: GEOGRAFI DAN IKLIM (INFOGRAFIS & NARASI)
// ==========================================
{chart_section}
// ==========================================
// ISI BAB 1: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Kecamatan {nama_singkat} secara geografis dan administratif berada di wilayah {nama_kab} dengan ibukota kecamatan berkedudukan di {ibukota}. Wilayah ini terbagi ke dalam {len(desa_list)} desa/kelurahan dengan akses perhubungan yang menghubungkan pusat-pusat kegiatan masyarakat dengan ibukota kabupaten.
]
#v(12pt)

{t1_1_markup}
#pagebreak()

{t1_2_markup}
#v(10pt)
{t1_3_markup}
#pagebreak()

{t1_4_markup}
"""
