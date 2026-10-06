"""Chapter 1: Geografi dan Iklim Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value, match_village_row
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter1_charts
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter1(cfg: Dict[str, Any], out_dir: Optional[Any] = None, fig_no: int = 2) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_kab_en = regency.get("nama_en", "Mempawah Regency")
    ibukota_kab = regency.get("ibukota_kabupaten", "Mempawah")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    ibukota = cfg.get("ibukota_kecamatan", "")
    desa_list = cfg.get("desa_list", [])
    slug = cfg.get("slug", "")

    peta_path = f"/assets/maps/{slug}.jpg"

    # --- Gambar 1: Peta Wilayah Kecamatan ---
    peta_section = f"""
#metadata("fig_1") <fig_1>
#metadata("fig_peta") <fig_peta>
#v(0.5cm)
#align(center)[
  #text(8.5pt, weight: "bold")[Gambar 1/]#text(8.5pt, weight: "bold", style: "italic")[Figure 1] \\
  #v(2pt)
  #text(9pt, weight: "bold")[Peta Wilayah Kecamatan {nama_singkat}, 2025] \\
  #text(8pt, style: "italic")[Map of {nama_en} District, 2025] \\
  #v(8pt)
  #box(width: 95%, stroke: 0.5pt + rgb("#CBD5E1"), radius: 4pt)[
    #image("{peta_path}", width: 100%)
  ] \\
  #v(4pt)
  #text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] : Badan Pusat Statistik/#text(style: "italic")[BPS-Statistics Indonesia]]
]
#pagebreak()
"""

    # --- Gambar 2 dst: Grafik ---
    charts_markup = get_chapter1_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None, fig_no=fig_no)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    # --- 1.1 Luas Daerah ---
    rows_1_1_raw = get_kecamatan_tab_rows("1.1.", nama_singkat)
    luas_map = {}
    total_luas = "–"
    for r in rows_1_1_raw:
        if len(r) > 1 and r[0].strip():
            nama_d = r[0].strip()
            if nama_d.isdigit() or nama_d.startswith('202') or any(nama_d.lower().startswith(x) for x in ['desa/kelurahan', 'kelurahan/desa', 'tabel']):
                continue
            if any(nama_d.lower().startswith(x) for x in ['jumlah', 'total', 'kecamatan']):
                if len(r) > 7 and r[7].strip() and total_luas == "–":
                    total_luas = clean_cell_value(r[7])
                continue
            if any(nama_d.lower().startswith(x) for x in ['sumber', 'catatan']):
                continue

            if nama_d.lower() not in luas_map:
                luas_val = clean_cell_value(r[7] if len(r) > 7 else r[1])
                pct_val = clean_cell_value(r[8] if len(r) > 8 else "–")
                status_val = clean_cell_value(r[9] if (len(r) > 9 and r[9].strip()) else "Indikatif")
                luas_map[nama_d.lower()] = [luas_val, pct_val, status_val]

    t1_1_rows = []
    for d in desa_list:
        v = match_village_row(luas_map, d, ["–", "–", "Indikatif"])
        t1_1_rows.append([d, v[0], v[1], v[2]])

    t1_1_rows.append([f"Kecamatan {nama_singkat}", total_luas, "100,00", ""])

    t1_1_markup = render_typst_table(
        table_no="1.1",
        title_id=f"Luas Daerah Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Area by Village/Subdistrict in {nama_en} District, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Luas Daerah\nArea (km²)", "Persentase terhadap Luas Kecamatan\nPercentage to District Area", "Status Batas\nBoundary Status"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t1_1_rows,
        col_widths=["1.9fr", "1.1fr", "1.8fr", "1.2fr"],
        source="Badan Perencanaan Pembangunan, Riset dan Inovasi Daerah Kabupaten Mempawah/Regional Development, Research and Innovation Agency of Mempawah Regency",
        note="Untuk desa/kelurahan dengan status Indikatif masih perlu dilakukan pelacakan ke lapangan dan kesepakatan batas antarwilayah yang berbatasan. / For villages/subdistricts with Indicative status, field tracking and boundary agreements between adjacent areas are still required."
    )

    # --- 1.2 Jarak ke Ibukota Kecamatan & Kabupaten ---
    rows_1_2_raw = get_kecamatan_tab_rows("1.2.", nama_singkat)
    jarak_map = {}
    for r in rows_1_2_raw:
        if len(r) > 1 and r[0].strip():
            nama_d = r[0].strip()
            if nama_d.isdigit() or nama_d.startswith('202') or any(nama_d.lower().startswith(x) for x in ['desa', 'kelurahan', 'tabel', 'jumlah', 'total', 'sumber', 'catatan', '(1)']):
                continue
            j_kec = clean_cell_value(r[1] if len(r) > 1 else "–")
            j_kab = clean_cell_value(r[2] if len(r) > 2 else "–")
            if nama_d.lower() not in jarak_map:
                jarak_map[nama_d.lower()] = [j_kec, j_kab]

    t1_2_rows = []
    for d in desa_list:
        v = match_village_row(jarak_map, d, ["–", "–"])
        t1_2_rows.append([d, v[0], v[1]])

    t1_2_markup = render_typst_table(
        table_no="1.2",
        title_id=f"Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten/Kota Menurut Desa/Kelurahan di {nama_resmi} (km), 2025",
        title_en=f"Distance to District Capital and Regency Capital by Village in {nama_en} District (km), 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Jarak ke Ibukota Kecamatan\nDistance to District Capital", "Jarak ke Ibukota Kabupaten/Kota\nDistance to Regency/Municipal Capital"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_2_rows,
        col_widths=["1.8fr", "1.7fr", "1.9fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
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
            ["1", "Utara/North", "–"],
            ["2", "Selatan/South", "–"],
            ["3", "Barat/West", "–"],
            ["4", "Timur/East", "–"]
        ]

    t1_3_markup = render_typst_table(
        table_no="1.3",
        title_id=f"Batas Administrasi {nama_resmi} Menurut Arah Mata Angin, 2025",
        title_en=f"Administrative Borders of {nama_en} District by Cardinal Direction, 2025",
        headers=["No", "Arah Mata Angin\nWind Direction", "Berbatasan Dengan\nBordering With"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_3_rows,
        col_widths=["0.6fr", "1.8fr", "3.0fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    # --- 1.4 Jarak Kantor Camat ke Tempat Penting ---
    rows_1_4_raw = get_kecamatan_tab_rows("1.4.", nama_singkat)
    t1_4_rows = []
    idx_no = 1
    for r in rows_1_4_raw[3:]:
        if len(r) > 1 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            tempat = clean_cell_value(r[1])
            if "makam juang mandor" in tempat.lower() and slug in ["toho", "jongkat"]:
                continue
            jarak = clean_cell_value(r[2] if len(r) > 2 else "–")
            t1_4_rows.append([str(idx_no), tempat, jarak])
            idx_no += 1
    if not t1_4_rows:
        t1_4_rows = [
            ["1", "Ibukota Provinsi / Provincial Capital", "–"],
            ["2", f"Ibukota Kabupaten ({ibukota_kab}) / Regency Capital", "–"],
            ["3", "Bandara Terdekat / Nearest Airport", "–"],
            ["4", "Pelabuhan Terdekat / Nearest Seaport", "–"]
        ]

    t1_4_markup = render_typst_table(
        table_no="1.4",
        title_id=f"Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025",
        title_en=f"Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025",
        headers=["No", "Nama Kota dan Tempat Penting\nOther Important Places", "Jarak\nDistance (km)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_4_rows,
        col_widths=["0.6fr", "3.2fr", "1.2fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    valid_desas = []
    for d in desa_list:
        v = match_village_row(luas_map, d)
        if v:
            try:
                val_f = float(v[0].replace(',', '.'))
                pct_f = float(v[1].replace(',', '.'))
                valid_desas.append((d, val_f, v[0], pct_f, v[1]))
            except Exception:
                pass

    if valid_desas:
        valid_desas.sort(key=lambda x: x[1])
        smallest_desa = valid_desas[0]
        largest_desa = valid_desas[-1]
        teks_luas_id = (
            f"Luas wilayah Kecamatan {nama_singkat} mencapai {total_luas} km². "
            f"Kecamatan {nama_singkat} terdiri dari {len(desa_list)} desa/kelurahan. "
            f"{largest_desa[0]} menjadi desa terluas di Kecamatan {nama_singkat} dengan luas mencapai {largest_desa[2]} km² atau sekitar {largest_desa[4]} persen dari luas Kecamatan {nama_singkat}. "
            f"Sementara, {smallest_desa[0]} menjadi desa dengan luas terkecil yaitu {smallest_desa[2]} km² atau sekitar {smallest_desa[4]} persen dari luas Kecamatan {nama_singkat}."
        )
        teks_luas_en = (
            f"The area of {nama_en} District reaches {total_luas} sq.km. "
            f"{nama_en} District consists of {len(desa_list)} villages. "
            f"{largest_desa[0]} became the largest village in {nama_en} District with an area of {largest_desa[2]} sq.km or about {largest_desa[4]} percent of the area of {nama_en} District. "
            f"Meanwhile, {smallest_desa[0]} became the smallest village with the smallest area of {smallest_desa[2]} sq.km or about {smallest_desa[4]} percent of the area of {nama_en} District."
        )
    else:
        teks_luas_id = f"Luas wilayah Kecamatan {nama_singkat} mencapai {total_luas} km² yang terbagi atas {len(desa_list)} desa/kelurahan."
        teks_luas_en = f"The area of {nama_en} District reaches {total_luas} sq.km, which is divided into {len(desa_list)} villages."

    batas_map = {}
    for r in t1_3_rows:
        if len(r) > 2:
            arah_raw = r[1].lower()
            if 'utara' in arah_raw:
                batas_map['utara'] = r[2]
            elif 'selatan' in arah_raw:
                batas_map['selatan'] = r[2]
            elif 'barat' in arah_raw:
                batas_map['barat'] = r[2]
            elif 'timur' in arah_raw:
                batas_map['timur'] = r[2]

    teks_letak_id = (
        f"Kecamatan {nama_singkat} adalah salah satu kecamatan di {nama_kab}. "
        f"Secara administratif, batas wilayah Kecamatan {nama_singkat} adalah:\\\n"
        f"Utara : {batas_map.get('utara', '–')}\\\n"
        f"Selatan : {batas_map.get('selatan', '–')}\\\n"
        f"Barat : {batas_map.get('barat', '–')}\\\n"
        f"Timur : {batas_map.get('timur', '–')}"
    )
    teks_letak_en = (
        f"{nama_en} District is one of the districts in {nama_kab_en}. "
        f"Administratively, the boundaries of {nama_en} District are:\\\n"
        f"North : {batas_map.get('utara', '–')}\\\n"
        f"South : {batas_map.get('selatan', '–')}\\\n"
        f"West : {batas_map.get('barat', '–')}\\\n"
        f"East : {batas_map.get('timur', '–')}"
    )

    valid_distances = []
    for r in t1_2_rows:
        if len(r) > 1 and r[1] not in ["–", "...", ""]:
            try:
                d_val = float(r[1].replace(',', '.'))
                valid_distances.append((r[0], d_val, r[1]))
            except Exception:
                pass

    jarak_kab = "–"
    for r in t1_4_rows:
        if len(r) > 2 and ("ibukota kabupaten" in r[1].lower() or "regency" in r[1].lower()):
            jarak_kab = r[2]
            break

    if valid_distances:
        valid_distances.sort(key=lambda x: x[1])
        nearest_desa = valid_distances[0]
        farthest_desa = valid_distances[-1]
        teks_jarak_id = (
            f"Aksesibilitas antarwilayah desa ke pusat pemerintahan kecamatan cukup bervariasi. "
            f"Desa dengan jarak terjauh ke ibukota kecamatan adalah {farthest_desa[0]} dengan jarak sekitar {farthest_desa[2]} km, "
            f"sedangkan desa terdekat adalah {nearest_desa[0]} ({nearest_desa[2]} km). "
            + (f"Jarak dari kantor camat ke ibukota kabupaten ({ibukota_kab}) adalah sekitar {jarak_kab} km." if jarak_kab != "–" else "")
        )
        teks_jarak_en = (
            f"Accessibility between villages and the district capital varies. "
            f"The village with the farthest distance to the district capital is {farthest_desa[0]} ({farthest_desa[2]} km), "
            f"while the nearest village is {nearest_desa[0]} ({nearest_desa[2]} km). "
            + (f"The distance from the district office to the regency capital ({ibukota_kab}) is approximately {jarak_kab} km." if jarak_kab != "–" else "")
        )
    else:
        teks_jarak_id = f"Jarak dari kantor camat ke ibukota kabupaten ({ibukota_kab}) adalah sekitar {jarak_kab} km." if jarak_kab != "–" else "Seluruh desa di kecamatan ini terhubung melalui jalur transportasi menuju ibukota kecamatan."
        teks_jarak_en = f"The distance from the district office to the regency capital ({ibukota_kab}) is approximately {jarak_kab} km." if jarak_kab != "–" else "All villages in this district are connected via transportation routes to the district capital."

    # Penjelasan Teknis & Ulasan Bab 1 (2 Kolom Resmi Sesuai Gambar 1 & Gambar 2)
    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Letak Wilayah] \\
  #v(2pt)
  {teks_letak_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Luas Wilayah] \\
  #v(2pt)
  {teks_luas_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Aksesibilitas Wilayah] \\
  #v(2pt)
  {teks_jarak_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Area Location] \\
  #v(2pt)
  {teks_letak_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Total Area] \\
  #v(2pt)
  {teks_luas_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Regional Accessibility] \\
  #v(2pt)
  {teks_jarak_en}
]"""

    technical_notes_bab1 = [
        (
            "Luas wilayah merujuk pada batas geografis suatu daerah yang mencakup daratan, perairan, dan ruang udara di atasnya. Luas wilayah merupakan ukuran area geografis yang mencakup semua aspek yang menjadi bagian dari suatu entitas administratif, dan penting dalam pengelolaan sumber daya serta perencanaan pembangunan di suatu daerah.",
            "The area of the area refers to the geographical boundaries of an area that includes land, waters, and airspace on it. The area is a size of the geographical area that covers all aspects of an administrative entity, and is important in the management of resources and development planning in an area"
        ),
        (
            "Ibu kota merujuk pada kota yang menjadi pusat pemerintahan suatu negara atau daerah, di mana terdapat kantor pemerintahan, lembaga legislatif, dan institusi penting lainnya. Ibu kota berfungsi sebagai simbol kedaulatan dan identitas suatu daerah, serta pusat administrasi dan pengambilan keputusan.",
            "The capital refers to the city that is the center of government of a country or region, where there are government offices, legislative institutions, and other important institutions. The capital serves as a symbol of the sovereignty and identity of an area, as well as the administrative and decision–making centers."
        ),
        (
            "Batas administrasi merujuk pada garis atau daerah yang menentukan wilayah administratif suatu entitas, seperti desa, kecamatan, kabupaten, atau provinsi. Batas administrasi adalah batas wilayah yang memisahkan satu daerah otonom dengan daerah otonom lainnya.",
            "Administration Limits refer to the lines or areas that determine the administrative territory of an entity, such as villages, sub– districts, districts, or provinces. The administrative limit is the boundary of the region that separates one autonomous region from another autonomous region"
        )
    ]

    bab1_intro = render_chapter_intro(
        chapter_num=1,
        title_id="GEOGRAFI",
        title_en="GEOGRAPHY",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab1
    )

    return f"""
// ==========================================
// BAB 1: GEOGRAFI (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================
{bab1_intro}
{peta_section}
{chart_section}
// ==========================================
// TABEL DATA BAB 1 (1 HALAMAN 1 TABEL)
// ==========================================
{t1_1_markup}
#pagebreak()

{t1_2_markup}
#pagebreak()

{t1_3_markup}
#pagebreak()

{t1_4_markup}
"""
