"""Chapter 2: Pemerintahan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter2_charts

def render_chapter2(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter2_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else "\n#v(8pt)\n"

    # --- 2.1.1 RW & RT ---
    rows_211_raw = get_kecamatan_tab_rows("2.1.1", nama_singkat)
    rw_rt_map = {}
    for r in rows_211_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            dusun = clean_cell_value(r[1] if len(r) > 1 else "...")
            rw = clean_cell_value(r[2] if len(r) > 2 else "...")
            rt = clean_cell_value(r[3] if len(r) > 3 else "...")
            rw_rt_map[r[0].strip().lower()] = [dusun, rw, rt]

    t211_rows = []
    for d in desa_list:
        v = rw_rt_map.get(d.lower(), ["...", "...", "..."])
        t211_rows.append([d, v[0], v[1], v[2]])

    t211_markup = render_typst_table(
        table_no="2.1.1",
        title_id=f"Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Number of Hamlets, RW, and RT by Village/Subdistrict in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Jumlah Dusun\nHamlets", "Rukun Warga\n(RW)", "Rukun Tetangga\n(RT)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t211_rows,
        col_widths=["2.2fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 2.1.2 Nama-Nama Camat ---
    rows_212_raw = get_kecamatan_tab_rows("2.1.2", nama_singkat)
    t212_rows = []
    for r in rows_212_raw[3:]:
        if len(r) > 1 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            idx = clean_cell_value(r[0])
            camat = clean_cell_value(r[1])
            periode = clean_cell_value(r[2] if len(r) > 2 else "...")
            t212_rows.append([idx, camat, periode])
    if not t212_rows:
        t212_rows = [["1", "...", "..."]]

    t212_markup = render_typst_table(
        table_no="2.1.2",
        title_id=f"Nama-Nama Camat yang Pernah/Masih Menjabat di {nama_resmi}",
        title_en=f"Names of District Heads of {nama_en}",
        headers=["No", "Nama Camat\nName of District Head", "Periode Menjabat\nPeriod"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t212_rows[:12], # Limit 12 baris agar muat 1 halaman
        col_widths=["0.6fr", "2.8fr", "1.6fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 2.1.3 Nama-Nama Kepala Desa ---
    rows_213_raw = get_kecamatan_tab_rows("2.1.3", nama_singkat)
    kades_map = {}
    for r in rows_213_raw[3:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            d_name = r[1].strip().lower()
            kades_nama = clean_cell_value(r[2])
            kades_map[d_name] = kades_nama

    t213_rows = []
    for idx, d in enumerate(desa_list, 1):
        kades = kades_map.get(d.lower(), "...")
        t213_rows.append([str(idx), d, kades])

    t213_markup = render_typst_table(
        table_no="2.1.3",
        title_id=f"Nama-Nama Kepala Desa/Lurah di {nama_resmi}, 2025",
        title_en=f"Names of Village Heads in {nama_en}, 2025",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Nama Kepala Desa / Lurah\nName of Village Head"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t213_rows,
        col_widths=["0.6fr", "2.2fr", "2.8fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 2.1.5 Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan ---
    rows_215_raw = get_kecamatan_tab_rows("2.1.5", nama_singkat)
    klas_map = {}
    for r in rows_215_raw[2:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            wil_adm = clean_cell_value(r[2] if len(r) > 2 else "Desa")
            klas = clean_cell_value(r[3] if len(r) > 3 else "Perdesaan")
            klas_map[r[1].strip().lower()] = [wil_adm, klas]

    t215_rows = []
    for idx, d in enumerate(desa_list, 1):
        v = klas_map.get(d.lower(), ["Desa", "Perdesaan"])
        t215_rows.append([str(idx), d, v[0], v[1]])

    t215_markup = render_typst_table(
        table_no="2.1.5",
        title_id=f"Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di {nama_resmi}, 2024",
        title_en=f"Urban and Rural Classification of Village/Subdistrict in {nama_en}, 2024",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Wilayah Administratif\nAdministrative Area", "Klasifikasi Desa/Kelurahan\nUrban/Rural Classification"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t215_rows,
        col_widths=["0.6fr", "2.2fr", "1.6fr", "1.6fr"],
        source="Peraturan Kepala BPS No. 120 Tahun 2020 / Chief of BPS Regulation No. 120 of 2020"
    )

    # --- 2.1.6 IDM Desa ---
    rows_216_raw = get_kecamatan_tab_rows("2.1.6", nama_singkat)
    idm_map = {}
    for r in rows_216_raw[2:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            status = clean_cell_value(r[2])
            idm_map[r[1].strip().lower()] = status

    t216_rows = []
    for idx, d in enumerate(desa_list, 1):
        status_idm = idm_map.get(d.lower(), "...")
        t216_rows.append([str(idx), d, status_idm])

    t216_markup = render_typst_table(
        table_no="2.1.6",
        title_id=f"Status Desa Berdasarkan Indeks Desa Membangun (IDM) di {nama_resmi}, 2024",
        title_en=f"Village Status Based on Developing Village Index (IDM) in {nama_en}, 2024",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Status Indeks Desa Membangun\nDeveloping Village Index Status"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t216_rows,
        col_widths=["0.6fr", "2.5fr", "2.5fr"],
        source="Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi / Ministry of Villages, Disadvantaged Regions Development, and Transmigration"
    )

    # --- 2.2.1 PNS menurut Golongan ---
    rows_221_raw = get_kecamatan_tab_rows("2.2.1", nama_singkat)
    t221_rows = []
    gol_list = ["Golongan I", "Golongan II", "Golongan III", "Golongan IV", "Jumlah / Total"]
    for idx, g in enumerate(gol_list, 1):
        t221_rows.append([g, "...", "...", "..."])

    t221_markup = render_typst_table(
        table_no="2.2.1",
        title_id=f"Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Golongan di {nama_resmi}, 2025",
        title_en=f"Number of Civil Servants in {nama_en} Office by Rank/Class, 2025",
        headers=["Golongan\nRank / Class", "Laki-laki\nMale", "Perempuan\nFemale", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t221_rows,
        col_widths=["2.2fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 2.2.2 PNS menurut Pendidikan ---
    pend_list = ["≤ SMP / Junior High", "SMA / Senior High", "Diploma I/II/III", "S1 / D-IV (Bachelor)", "S2 / Master", "Jumlah / Total"]
    t222_rows = [[p, "...", "...", "..."] for p in pend_list]

    t222_markup = render_typst_table(
        table_no="2.2.2",
        title_id=f"Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Tingkat Pendidikan di {nama_resmi}, 2025",
        title_en=f"Number of Civil Servants in {nama_en} Office by Education Level, 2025",
        headers=["Tingkat Pendidikan\nEducation Level", "Laki-laki\nMale", "Perempuan\nFemale", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t222_rows,
        col_widths=["2.2fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    return f"""
// ==========================================
// BAB 2: PEMERINTAHAN (INFOGRAFIS & NARASI)
// ==========================================
{chart_section}
// ==========================================
// ISI BAB 2: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Secara administratif, Kecamatan {nama_singkat} terbagi menjadi {len(desa_list)} desa/kelurahan yang dipimpin oleh kepala desa dan lurah definitif, didukung oleh aparatur pemerintah desa, Badan Permusyawaratan Desa (BPD), serta kelembagaan RT dan RW sebagai garda terdepan pelayanan kemasyarakatan.
]
#v(12pt)

{t211_markup}
#pagebreak()

{t212_markup}
#v(10pt)
{t213_markup}
#pagebreak()

{t215_markup}
#v(10pt)
{t216_markup}
#pagebreak()

{t221_markup}
#v(10pt)
{t222_markup}
"""
