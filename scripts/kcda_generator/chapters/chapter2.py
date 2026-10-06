"""Chapter 2: Pemerintahan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value, match_village_row, normalize_village_name
from ..table_renderer import render_typst_table, render_subchapter_heading
from ..chart_generator import get_chapter2_charts
from .narrative_helper import render_chapter_intro

def render_chapter2(cfg: Dict[str, Any], out_dir: Optional[Any] = None, fig_no: int = 3) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    desa_list = cfg.get("desa_list", [])
    slug = cfg.get("slug", "")

    year_212 = "2026" if slug == "toho" else "2025"
    year_213 = "2025" if slug == "toho" else "2026"
    has_214 = slug not in ["mempawah-hilir", "sungai-pinyuh"]

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter2_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None, fig_no=fig_no)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    
    # --- 2.1.1 Dusun, RW & RT ---
    rows_211_raw = get_kecamatan_tab_rows("2.1.1", nama_singkat)
    rw_rt_map = {}
    tot_dusun = None
    tot_rw = None
    tot_rt = None

    for r in rows_211_raw[3:]:
        if len(r) > 1 and r[0].strip():
            row_label = r[0].strip().lower()
            if any(row_label.startswith(x) for x in ['jumlah', 'total', 'kecamatan']):
                if tot_dusun is None:
                    tot_dusun = clean_cell_value(r[1] if len(r) > 1 else "–")
                    tot_rw = clean_cell_value(r[2] if len(r) > 2 else "–")
                    tot_rt = clean_cell_value(r[3] if len(r) > 3 else "–")
                continue
            if row_label.startswith('sumber') or row_label.startswith('catatan'):
                continue
            dusun = clean_cell_value(r[1] if len(r) > 1 else "–")
            rw = clean_cell_value(r[2] if len(r) > 2 else "–")
            rt = clean_cell_value(r[3] if len(r) > 3 else "–")
            rw_rt_map[row_label] = [dusun, rw, rt]

    t211_rows = []
    for d in desa_list:
        v = match_village_row(rw_rt_map, d, ["–", "–", "–"])
        t211_rows.append([d, v[0], v[1], v[2]])

    if tot_dusun is None or tot_dusun in ["–", "...", ""]:
        try:
            d_sum = sum(int(r[1]) for r in t211_rows if str(r[1]).isdigit())
            rw_sum = sum(int(r[2]) for r in t211_rows if str(r[2]).isdigit())
            rt_sum = sum(int(r[3]) for r in t211_rows if str(r[3]).isdigit())
            tot_dusun = str(d_sum)
            tot_rw = str(rw_sum)
            tot_rt = str(rt_sum)
        except Exception:
            tot_dusun, tot_rw, tot_rt = "–", "–", "–"

    t211_rows.append([f"Kecamatan {nama_singkat}", tot_dusun, tot_rw, tot_rt])

    t211_markup = render_typst_table(
        table_no="2.1.1",
        title_id=f"Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Number of Hamlets, Rukun Warga and Rukun Tetangga by Villages/Subdistricts in {nama_en} District, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Dusun\nHamlet", "Rukun Warga\n(RW)", "Rukun Tetangga\n(RT)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t211_rows,
        col_widths=["2.2fr", "0.9fr", "1.0fr", "1.0fr"],
        source="Master SLS Badan Pusat Statistik / Master SLS BPS-Statistics Indonesia"
    )

    # --- 2.1.2 Nama-Nama Camat ---
    rows_212_raw = get_kecamatan_tab_rows("2.1.2", nama_singkat)
    t212_rows = []
    for r in rows_212_raw[3:]:
        if len(r) > 1 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            idx = clean_cell_value(r[0])
            camat = clean_cell_value(r[1])
            periode = clean_cell_value(r[2] if len(r) > 2 else "–")
            t212_rows.append([idx, camat, periode])
    if not t212_rows:
        t212_rows = [["1", "–", "–"]]
    elif slug == "toho":
        t212_rows[-1][2] = "Oktober 2025 - saat ini"

    t212_markup = render_typst_table(
        table_no="2.1.2",
        title_id=f"Nama-Nama Camat yang Pernah/Masih Menjabat di {nama_resmi}, {year_212}",
        title_en=f"Names of Last and Current Who Have/Still Served in {nama_en} District, {year_212}",
        headers=["No", "Nama Camat\nName of District Head", "Periode Menjabat\nPeriod"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t212_rows,
        col_widths=["0.6fr", "2.8fr", "1.6fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    # --- 2.1.3 Nama-Nama Kepala Desa ---
    rows_213_raw = get_kecamatan_tab_rows("2.1.3", nama_singkat)
    kades_map = {}
    for r in rows_213_raw[2:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan', 'tabel', 'no', 'desa', '(']):
            d_name = r[1].strip().lower()
            kades_nama = clean_cell_value(r[2])
            kades_map[d_name] = kades_nama

    t213_rows = []
    for idx, d in enumerate(desa_list, 1):
        kades = "..." if slug == "toho" else match_village_row(kades_map, d, "–")
        t213_rows.append([str(idx), d, kades])

    t213_markup = render_typst_table(
        table_no="2.1.3",
        title_id=f"Nama-Nama Kepala Desa/Lurah di {nama_resmi}, {year_213}",
        title_en=f"Names of Village Heads in {nama_en} District, {year_213}",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Nama Kepala Desa / Lurah\nName of Village Head"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t213_rows,
        col_widths=["0.6fr", "2.2fr", "2.8fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    # --- 2.1.4 Nama-Nama Kepala Dusun (Hanya 7 Kecamatan) ---
    t214_markup = ""
    if has_214:
        rows_214_raw = get_kecamatan_tab_rows("2.1.4", nama_singkat)
        t214_rows = []
        for r in rows_214_raw[2:]:
            if len(r) > 3 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan', 'tabel', 'no', 'desa', '(']):
                no_d = clean_cell_value(r[0])
                desa_d = clean_cell_value(r[1])
                dusun_d = clean_cell_value(r[2])
                nama_d = "..." if slug == "toho" else clean_cell_value(r[3])
                if desa_d:
                    t214_rows.append([no_d, desa_d, dusun_d, nama_d])
        if not t214_rows:
            t214_rows = [["1", "–", "–", "..." if slug == "toho" else "–"]]

        t214_markup = render_typst_table(
            table_no="2.1.4",
            title_id=f"Nama-Nama Kepala Dusun di {nama_resmi}, 2025",
            title_en=f"Names of Hamlet Heads in {nama_en} District, 2025",
            headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Nama Dusun\nName of Hamlet", "Nama Kepala Dusun\nName of Hamlet Head"],
            col_numbers=["(1)", "(2)", "(3)", "(4)"],
            rows=t214_rows,
            col_widths=["0.6fr", "1.8fr", "1.6fr", "2.0fr"],
            source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
        )

    # --- 2.1.5 / 2.1.4 Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan ---
    tno_klas = "2.1.5" if has_214 else "2.1.4"
    tno_idm = "2.1.6" if has_214 else "2.1.5"

    rows_215_raw = get_kecamatan_tab_rows("2.1.5", nama_singkat)
    klas_map = {}
    for r in rows_215_raw[2:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['jumlah', 'total', 'sumber', 'catatan', 'no', 'desa', '(']):
            wil_adm = clean_cell_value(r[2] if len(r) > 2 else "Desa")
            klas = clean_cell_value(r[3] if len(r) > 3 else "Perdesaan")
            klas_map[r[1].strip().lower()] = [wil_adm, klas]

    t215_rows = []
    for idx, d in enumerate(desa_list, 1):
        v = match_village_row(klas_map, d, ["Desa", "Perdesaan"])
        t215_rows.append([str(idx), d, v[0], v[1]])

    t215_markup = render_typst_table(
        table_no=tno_klas,
        title_id=f"Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di {nama_resmi}, 2024",
        title_en=f"Urban and Rural Classification of Village/Subdistrict in {nama_en} District, 2024",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Wilayah Administratif\nAdministrative Area", "Klasifikasi Desa/Kelurahan\nUrban/Rural Classification"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t215_rows,
        col_widths=["0.6fr", "2.2fr", "1.6fr", "1.6fr"],
        source="Peraturan Kepala Badan Pusat Statistik Nomor 120 Tahun 2020 Tentang Klasifikasi Desa Perkotaan dan Perdesaan di Indonesia Tahun 2020/ Regulation of the Chief Statistician Number 120 of 2020 Concerning the Classification of Urban and Rural Villages in Indonesia in 2020"
    )

    # --- 2.1.6 / 2.1.5 IDM Desa ---
    rows_216_raw = get_kecamatan_tab_rows("2.1.6", nama_singkat)
    idm_map = {}
    for r in rows_216_raw[2:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['jumlah', 'total', 'sumber', 'catatan', 'no', 'desa', '(']):
            status = clean_cell_value(r[2])
            idm_map[r[1].strip().lower()] = status

    t216_rows = []
    for idx, d in enumerate(desa_list, 1):
        status_idm = match_village_row(idm_map, d, "–")
        t216_rows.append([str(idx), d, status_idm])

    t216_markup = render_typst_table(
        table_no=tno_idm,
        title_id=f"Status Desa berdasarkan Indeks Desa Membangun di {nama_resmi}, 2024",
        title_en=f"Village Status Based on Developing Village Index in {nama_en} District, 2024",
        headers=["No", "Desa/Kelurahan\nVillage/Subdistrict", "Status Indeks Desa Membangun\nDeveloping Village Index Status"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t216_rows,
        col_widths=["0.6fr", "2.5fr", "2.5fr"],
        source="Indeks Desa Membangun (IDM) Tahun 2024 per Desa, Kementerian Desa, PDT dan Transmigrasi/ Index of Developing Village 2024 for each Village, Ministry of Villages, Development of Disadvantaged Regions, and Transmigration"
    )

    # --- 2.2.1 PNS menurut Pemerintah Daerah ---
    rows_221_raw = get_kecamatan_tab_rows("2.2.1", nama_singkat)
    t221_rows = []
    if len(rows_221_raw) > 2:
        for r in rows_221_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan', 'pemerintah daerah\n', '(']):
                pem = clean_cell_value(r[0])
                if slug == "toho":
                    lk, pr, tot = "...", "...", "..."
                else:
                    lk = clean_cell_value(r[1] if len(r) > 1 else "–")
                    pr = clean_cell_value(r[2] if len(r) > 2 else "–")
                    tot = clean_cell_value(r[3] if len(r) > 3 else "–")
                t221_rows.append([pem, lk, pr, tot])
    if not t221_rows:
        t221_rows = [
            [f"Pemerintah Daerah Kecamatan {nama_singkat}\n{nama_en} District Government", "..." if slug == "toho" else "–", "..." if slug == "toho" else "–", "..." if slug == "toho" else "–"]
        ]

    t221_markup = render_typst_table(
        table_no="2.2.1",
        title_id=f"Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin di {nama_resmi}, 2025",
        title_en=f"Number of Government Employee by Local Government and Sex in {nama_en} District, 2025",
        headers=["Pemerintah Daerah\nLocal Government", "Laki-laki\nMale", "Perempuan\nFemale", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t221_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    # --- 2.2.2 PNS menurut Pendidikan ---
    rows_222_raw = get_kecamatan_tab_rows("2.2.2", nama_singkat)
    t222_rows = []
    if len(rows_222_raw) > 2:
        for r in rows_222_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan', 'tingkat pendidikan', '(']):
                pend = clean_cell_value(r[0])
                if slug == "toho":
                    lk, pr, tot = "...", "...", "..."
                else:
                    lk = clean_cell_value(r[1] if len(r) > 1 else "–")
                    pr = clean_cell_value(r[2] if len(r) > 2 else "–")
                    tot = clean_cell_value(r[3] if len(r) > 3 else "–")
                t222_rows.append([pend, lk, pr, tot])
    if not t222_rows:
        pend_list = [
            "Sekolah Dasar (SD)\nPrimary School",
            "SMP/Sederajat\nJunior High School",
            "SMA/Sederajat\nSenior High School",
            "Diploma I/II/III\nDiploma I/II/III",
            "Diploma IV/S1\nBachelor Degree",
            "S2 / Master",
            "Jumlah / Total"
        ]
        t222_rows = [[p, "..." if slug == "toho" else "–", "..." if slug == "toho" else "–", "..." if slug == "toho" else "–"] for p in pend_list]

    t222_markup = render_typst_table(
        table_no="2.2.2",
        title_id=f"Jumlah Pegawai Negeri Sipil Pemerintah Daerah {nama_resmi} Menurut Tingkat Pendidikan dan Jenis Kelamin, 2025",
        title_en=f"Number of Government Employee of {nama_en} District Local Government by Educational Level and Sex, 2025",
        headers=["Tingkat Pendidikan\nEducational Level", "Laki-laki\nMale", "Perempuan\nFemale", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t222_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr"],
        source=f"Kantor Camat {nama_singkat}/ {nama_singkat} District Office"
    )

    # --- Ulasan dan Penjelasan Teknis Bab 2 Sesuai Publikasi BPS ---
    tot_rw = 0
    tot_rt = 0
    tot_dusun = 0
    for d in desa_list:
        v = match_village_row(rw_rt_map, d)
        if v:
            if v[0].isdigit(): tot_dusun += int(v[0])
            if v[1].isdigit(): tot_rw += int(v[1])
            if v[2].isdigit(): tot_rt += int(v[2])

    camat_first = t212_rows[0][1] if t212_rows and t212_rows[0][1] != "–" else ""
    camat_first_p = t212_rows[0][2] if t212_rows and len(t212_rows[0]) > 2 and t212_rows[0][2] != "–" else ""
    camat_last = t212_rows[-1][1] if t212_rows and t212_rows[-1][1] != "–" else ""
    camat_last_p = t212_rows[-1][2] if t212_rows and len(t212_rows[-1]) > 2 and t212_rows[-1][2] != "–" else ""

    urban_desas = [r[1] for r in t215_rows if len(r) > 3 and "perkotaan" in r[3].lower()]
    rural_desas = [r[1] for r in t215_rows if len(r) > 3 and "perdesaan" in r[3].lower()]

    if camat_first and camat_last and camat_first != camat_last:
        teks_camat_id = (
            f"Sejak awal berdirinya, Kecamatan {nama_singkat} sudah banyak mengalami pergantian pemimpin. "
            f"Jabatan Camat {nama_singkat} pertama dijabat oleh {camat_first} ({camat_first_p}). "
            f"Dalam perkembangannya, kepemimpinan kecamatan terus berlanjut hingga saat ini dijabat oleh {camat_last} ({camat_last_p})."
        )
        teks_camat_en = (
            f"Since its inception, {nama_en} District has experienced many changes in leadership. "
            f"The first position of Head of {nama_en} District was held by {camat_first} ({camat_first_p}). "
            f"Over time, district leadership has continued through to the present term held by {camat_last} ({camat_last_p})."
        )
    else:
        teks_camat_id = (
            f"Dalam menyelenggarakan tata kelola pemerintahan di tingkat kecamatan, Camat bertindak sebagai pemimpin dan koordinator pemerintahan wilayah di Kecamatan {nama_singkat}."
        )
        teks_camat_en = (
            f"In administering governance at the district level, the Camat serves as the regional government leader and coordinator in {nama_en} District."
        )

    mandiri_cnt = sum(1 for r in t216_rows if "mandiri" in str(r[2]).lower())
    maju_cnt = sum(1 for r in t216_rows if "maju" in str(r[2]).lower())
    berkembang_cnt = sum(1 for r in t216_rows if "berkembang" in str(r[2]).lower())

    idm_parts_id = []
    idm_parts_en = []
    if mandiri_cnt > 0:
        idm_parts_id.append(f"{mandiri_cnt} desa berstatus Mandiri")
        idm_parts_en.append(f"{mandiri_cnt} Independent Village(s)")
    if maju_cnt > 0:
        idm_parts_id.append(f"{maju_cnt} desa Maju")
        idm_parts_en.append(f"{maju_cnt} Advanced Village(s)")
    if berkembang_cnt > 0:
        idm_parts_id.append(f"{berkembang_cnt} desa Berkembang")
        idm_parts_en.append(f"{berkembang_cnt} Developing Village(s)")

    str_idm_id = ", ".join(idm_parts_id) if idm_parts_id else "seluruh desa terus ditingkatkan kemandirian ekonominya"
    str_idm_en = ", ".join(idm_parts_en) if idm_parts_en else "village autonomy continues to be promoted"

    tot_pns = "–"
    pns_lk = "–"
    pns_pr = "–"
    for r in t221_rows:
        if len(r) > 3 and any(k in r[0].lower() for k in ["kecamatan", "pemerintah", "kelurahan", "jumlah"]):
            if r[3] not in ["–", "...", ""]:
                tot_pns = r[3]
                pns_lk = r[1]
                pns_pr = r[2]
                break

    str_urban = ", ".join(urban_desas)
    if urban_desas:
        teks_desa_id = (
            f"Kecamatan {nama_singkat} pada tahun 2025 terdiri dari {len(desa_list)} desa/kelurahan yang terbagi menjadi {tot_dusun} dusun, {tot_rw} RW, dan {tot_rt} RT. "
            f"Berdasarkan klasifikasi perdesaan dan perkotaan, {len(urban_desas)} desa/kelurahan yaitu {str_urban} merupakan wilayah perkotaan, sedangkan {len(rural_desas)} desa lainnya merupakan wilayah perdesaan.\\\n\\\n"
            f"Berdasarkan status Indeks Desa Membangun (IDM), capaian kemandirian desa mencakup {str_idm_id}."
        )
        teks_desa_en = (
            f"{nama_en} District in 2025 consists of {len(desa_list)} villages/subdistricts divided into {tot_dusun} dusun, {tot_rw} RW, and {tot_rt} RT. "
            f"Based on the classification of rural and urban areas, {len(urban_desas)} village(s) ({str_urban}) are urban areas, while {len(rural_desas)} other villages are rural areas.\\\n\\\n"
            f"Based on the Developing Village Index (IDM), village autonomy achievements include {str_idm_en}."
        )
    else:
        teks_desa_id = (
            f"Kecamatan {nama_singkat} pada tahun 2025 terdiri dari {len(desa_list)} desa yang terbagi menjadi {tot_dusun} dusun, {tot_rw} RW, dan {tot_rt} RT, "
            f"dengan klasifikasi wilayah perdesaan yang didukung kelembagaan masyarakat tingkat rukun tetangga dan rukun warga.\\\n\\\n"
            f"Berdasarkan status Indeks Desa Membangun (IDM), capaian kemandirian desa mencakup {str_idm_id}."
        )
        teks_desa_en = (
            f"{nama_en} District in 2025 consists of {len(desa_list)} villages divided into {tot_dusun} dusun, {tot_rw} RW, and {tot_rt} RT, "
            f"with rural classifications supported by neighborhood and community unit institutions.\\\n\\\n"
            f"Based on the Developing Village Index (IDM), village autonomy achievements include {str_idm_en}."
        )

    if tot_pns not in ["–", "...", "0"]:
        teks_pns_id = (
            f"Penyelenggaraan pelayanan publik di lingkungan Pemerintah Kecamatan {nama_singkat} didukung oleh "
            f"{tot_pns} orang Pegawai Negeri Sipil (PNS), yang terdiri dari {pns_lk} orang laki-laki dan {pns_pr} orang perempuan. "
            f"Aparatur kecamatan berperan penting dalam koordinasi administrasi kewilayahan dan fasilitasi pembangunan desa."
        )
        teks_pns_en = (
            f"Public service delivery within {nama_en} District Government is supported by "
            f"{tot_pns} Civil Servants (PNS), consisting of {pns_lk} males and {pns_pr} females. "
            f"District officials play an essential role in regional administrative coordination and village development facilitation."
        )
    else:
        teks_pns_id = (
            f"Aparatur sipil negara di lingkungan Pemerintah Daerah Kecamatan {nama_singkat} menjalankan fungsi pelayanan publik, "
            f"koordinasi administrasi perizinan, dan fasilitasi pembangunan antardesa."
        )
        teks_pns_en = (
            f"Civil servants within the {nama_en} District Government perform public service functions, "
            f"administrative coordination, and development facilitation among villages."
        )

    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Kepala Daerah] \\
  #v(2pt)
  {teks_camat_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Pemerintah Desa] \\
  #v(2pt)
  {teks_desa_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Pegawai Negeri Sipil] \\
  #v(2pt)
  {teks_pns_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Regional Head] \\
  #v(2pt)
  {teks_camat_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Village Government] \\
  #v(2pt)
  {teks_desa_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Civil Service] \\
  #v(2pt)
  {teks_pns_en}
]"""

    technical_notes_bab2 = [
        (
            "Kecamatan adalah bagian wilayah dari daerah kabupaten/kota yang dipimpin oleh Camat. Kecamatan diatur sesuai dengan ketentuan Undang-Undang Nomor 23 Tahun 2014 tentang Pemerintahan Daerah.",
            "District is part of the region of the district / city led by Camat. District is regulated in accordance with the provisions of Law No. 23 of 2014 on Regional Government."
        ),
        (
            "Desa/Kelurahan adalah wilayah yang dipimpin oleh kepala desa/kepala kelurahan (lurah) yang berada di bawah koordinasi camat.",
            "Village/Subdistrict is a region led by the village head/subdistrict head (lurah) who is under the coordination of district head."
        ),
        (
            "Rukun Tetangga (RT) dan Rukun Warga (RW) digunakan untuk mengidentifikasi satuan lingkungan setempat. RT dan RW merupakan organisasi yang dibentuk melalui musyawarah oleh masyarakat setempat serta diakui dan dibina oleh Pemerintah untuk menjadi mitra dalam pemberdayaan masyarakat. Pembentukan RT dan RW sejalan dengan besaran jumlah penduduk di suatu wilayah.",
            "RT and RW are used to identify local environmental units. RT and RW are organisations formed through deliberation by local communities and recognized and built by the Government to become partners in community empowerment. The formation of RT and RW is in line with the size of the population in a region."
        ),
        (
            "Klasifikasi Wilayah adalah golongan suatu wilayah administrasi setingkat desa/kelurahan yang ditentukan berdasarkan standar atau ciri wilayah perkotaan dan perdesaan.",
            "Regional Classification is a group of administrative regions as high as village/subdistrict specified based on standards or characteristics of urban and rural areas."
        ),
        (
            "Indeks Desa Membangun (IDM) merupakan indeks komposit yang dibentuk dari tiga indeks, yaitu Indeks Ketahanan Sosial (IKS), Indeks Ketahanan Ekonomi (IKE), dan Indeks Ketahanan Ekologi/Lingkungan (IKL). Nilai IDM yang semakin tinggi menunjukkan kondisi desa yang semakin baik dari segi sosial, ekonomi, dan ekologi. IDM dapat menentukan status desa menjadi Desa Mandiri, Maju, Berkembang, Tertinggal, dan Sangat Tertinggal berdasarkan nilai dari indeks-indeks tersebut.",
            "Index of Developing Village is a composite index formed from three indices, namely Social Resilience Index, Economic Resilience Index, and Ecological/Environmental.Resilience Index. The higher Index of Developing Village values indicate the better of the village in terms of social, economic, and ecological terms. Index of Developing Village can determine the status of the village to be \\\"Mandiri\\\", \\\"Maju\\\", \\\"Berkembang\\\", \\\"Tertinggal\\\" and \\\"Sangat Tertinggal\\\" Village based on the value of these indexes."
        ),
        (
            "Pegawai Negeri Sipil (PNS) adalah setiap warga negara Republik Indonesia yang telah memenuhi syarat yang ditentukan, diangkat oleh pejabat yang berwenang dan diserahi tugas dalam jabatan negeri, atau diserahi tugas negara lainnya, dan digaji berdasarkan peraturan perundang-undangan yang berlaku. PNS terdiri dari PNS pusat dan PNS daerah.",
            "Civil Service (PNS) is any citizen of the Republic of Indonesia who has qualified as specified, appointed by the authorized officials and assigned duties in state office, or assigned to other state duties, and paid under applicable legislation. The PNS consists of the central PNS and the local PNS."
        )
    ]

    bab2_intro = render_chapter_intro(
        chapter_num=2,
        title_id="PEMERINTAHAN",
        title_en="GOVERNMENT",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab2
    )

    sec_214 = f"{t214_markup}\n#pagebreak()\n" if has_214 else ""

    sec_21 = render_subchapter_heading("2.1", "Wilayah Administratif", "Administrative Area")
    sec_22 = render_subchapter_heading("2.2", "Sumber Daya Manusia", "Human Resources")

    return f"""
// ==========================================
// BAB 2: PEMERINTAHAN (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================
{bab2_intro}
{chart_section}
// ==========================================
// TABEL DATA BAB 2 (1 HALAMAN 1 TABEL)
// ==========================================
{sec_21}{t211_markup}
#pagebreak()

{t212_markup}
#pagebreak()

{t213_markup}
#pagebreak()

{sec_214}{t215_markup}
#pagebreak()

{t216_markup}
#pagebreak()

{sec_22}{t221_markup}
#pagebreak()

{t222_markup}
"""
