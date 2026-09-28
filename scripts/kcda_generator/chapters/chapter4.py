"""Chapter 4: Sosial dan Kesejahteraan Rakyat Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table, render_subchapter_heading, get_edu_two_tier_header
from ..chart_generator import get_chapter4_charts
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter4(cfg: Dict[str, Any], out_dir: Optional[Any] = None, fig_no: int = 5) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_kab_en = regency.get("nama_en", "Mempawah Regency")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    desa_list = cfg.get("desa_list", [])
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter4_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None, fig_no=fig_no)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    podes_catatan = "1Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries"
    podes_sumber = "Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/BPS–Statistics Indonesia, Village Potential Data Collecting"
    edu_sumber = "Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama / Ministry of Education, Culture, Research, and Technology & Ministry of Religious Affairs"

    # Ekstraksi angka pendidikan (Tabel 4.1.2)
    rows_412_raw = get_kecamatan_tab_rows("4.1.2", nama_singkat)
    edu_map = {}
    if len(rows_412_raw) > 3:
        for r in rows_412_raw[3:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                lvl = r[0].split('\n')[0].strip()
                jml = clean_cell_value(r[6] if len(r) > 6 and r[6].strip() else (r[5] if len(r) > 5 else "–"))
                edu_map[lvl.lower()] = jml

    def get_edu_val(key):
        for k, v in edu_map.items():
            if key in k:
                return v
        return "–"

    sd_count = get_edu_val("dasar")
    smp_count = get_edu_val("pertama")
    sma_count = get_edu_val("atas")
    smk_count = get_edu_val("kejuruan")

    # Ekstraksi angka kesehatan (Tabel 4.2.1)
    rows_421_raw = get_kecamatan_tab_rows("4.2.1", nama_singkat)
    kes_map = {}
    if len(rows_421_raw) > 2:
        for r in rows_421_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                sarana = r[0].split('\n')[0].strip()
                y2025 = clean_cell_value(r[3] if len(r) > 3 else "–")
                kes_map[sarana.lower()] = y2025

    def get_kes_val(key):
        for k, v in kes_map.items():
            if key in k:
                return v
        return "–"

    p_inap = get_kes_val("rawat inap")
    p_non = get_kes_val("tanpa")

    teks_edu_id = (
        f"Ketersediaan fasilitas pendidikan akan sangat menunjang dalam meningkatkan mutu pendidikan. "
        f"Pada tahun ajaran 2025/2026, terdapat {sd_count} Sekolah Dasar (SD) di Kecamatan {nama_singkat}. "
        f"Jumlah Sekolah Menengah Pertama (SMP) tercatat sebanyak {smp_count} sekolah, sedangkan pada jenjang "
        f"Sekolah Menengah Atas (SMA) terdapat {sma_count} sekolah dan Sekolah Menengah Kejuruan (SMK) sebanyak {smk_count} sekolah."
    )
    teks_edu_en = (
        f"The availability of educational facilities plays an important role in improving the quality of education. "
        f"In the 2025/2026 academic year, {nama_en} District had {sd_count} primary schools (SD), "
        f"{smp_count} junior high schools (SMP), {sma_count} senior high school(s) (SMA), and {smk_count} vocational high school(s) (SMK)."
    )

    teks_kes_id = (
        f"Fasilitas kesehatan merupakan sarana prasarana yang vital di suatu wilayah. "
        f"Pada tahun 2025, fasilitas kesehatan yang tersedia di Kecamatan {nama_singkat} meliputi "
        f"{p_inap} Puskesmas rawat inap, {p_non} Puskesmas tanpa rawat inap, serta sarana apotek/toko obat "
        f"yang menunjang peningkatan derajat kesehatan masyarakat."
    )
    teks_kes_en = (
        f"Health facilities are essential infrastructure in a region. "
        f"In 2025, health facilities available in {nama_en} District included "
        f"{p_inap} inpatient Public Health Center, {p_non} outpatient Public Health Center, and pharmacies "
        f"supporting the improvement of public health."
    )

    # Penjelasan Teknis & Ulasan Bab 4 (2 Kolom Resmi Sesuai Gambar 1 & Gambar 2)
    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Pendidikan] \\
  #v(2pt)
  {teks_edu_id}
]
#v(8pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Kesehatan] \\
  #v(2pt)
  {teks_kes_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Education] \\
  #v(2pt)
  {teks_edu_en}
]
#v(8pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Health] \\
  #v(2pt)
  {teks_kes_en}
]"""
    technical_notes_bab4 = [
        (
            """Jenjang Pendidikan Formal terdiri atas pendidikan dasar, pendidikan menengah, dan pendidikan tinggi. Jenis pendidikan yang diajarkan mencakup pendidikan umum, kejuruan, akademik, profesi, vokasi, keagamaan, dan khusus.

a. Pendidikan Dasar berbentuk Sekolah Dasar (SD) dan Madrasah Ibtidaiyah (MI) atau bentuk lain yang sederajat serta Sekolah Menengah Pertama (SMP) dan Madrasah Tsanawiyah (MTs) atau bentuk lain yang sederajat.

b. Pendidikan Menengah berbentuk Sekolah Menengah Atas (SMA), Madrasah Aliyah (MA), Sekolah Menengah Kejuruan (SMK), dan Madrasah Aliyah Kejuruan (MAK), atau bentuk lain yang sederajat.

c. Pendidikan Tinggi merupakan jenjang Pendidikan setelah pendidikan menengah yang mencakup program pendidikan diploma, sarjana, magister, spesialis, dan doktor yang diselenggarakan oleh perguruan tinggi. Perguruan tinggi dapat berbentuk akademi, politeknik, sekolah tinggi, atau institut.""",
            """The Formal Education Level consists of primary education, secondary education, and high education. The kind of education that taught consists of general education, vocational, academic, professional, religious, and specific education.

a. The Primary Education consists of Elementary School and Islamic Elementary School or other equivalent forms and Junior High School and MTs or other equivalent forms.

b. The Secondary Education consists of the senior high school, Madrasah Aliyah, Vocational School, and Vocational Madrasah Aliyah, or other equivalent forms.

c. The Tertiary Education consists of the education level after the secondary education that consists of diplomas, bachelor, master, specialist, and doctoral degrees that are held by the college. The universities can be academy, polytechnic, college, or institute."""
        ),
        (
            """Rumah Sakit adalah tempat pemeriksaan dan perawatan kesehatan, biasanya berada di bawah pengawasan dokter/tenaga medis, yang melayani penderita yang sakit untuk berobat rawat jalan atau rawat inap. Undang-undang RI No. 44 Tahun 2009 tentang rumah sakit mengelompokkan rumah sakit berdasarkan jenis pelayanan yang diberikan menjadi:

Rumah Sakit Umum adalah rumah sakit yang memberikan pelayanan kesehatan pada semua bidang dan jenis penyakit.

Rumah Sakit khusus adalah rumah sakit yang memberikan pelayanan utama pada satu bidang atau satu jenis penyakit tertentu berdasarkan disiplin ilmu, golongan umur, organ, jenis penyakit, atau kekhususan lainnya.""",
            """Hospital is a place for health check, usually controlled/supervised by doctors/medical personnel to serve the ill patients to get outpatient or inpatient treatment services. The law of the Republic of Indonesia Number 44 year 2009 concerning about hospital have been grouping hospital based on the type of service being given into:

General Hospital is a hospital that provides health services in all areas and types of diseases.

Special Hospital is a hospital that provides primary care in one area or one particular type of disease base on dicipline, age group, organ, type of disease, or other specificity."""
        ),
        (
            """Pusat Kesehatan Masyarakat (Puskesmas) adalah unit pelaksana teknis dinas kesehatan kabupaten/kota yang mempunyai fungsi utama sebagai penyelenggara pelayanan kesehatan tingkat pertama. Wilayah kerja puskesmas maksimal adalah satu kecamatan. Untuk dapat menjangkau wilayah kerjanya, puskesmas mempunyai jaringan pelayanan yang meliputi unit Puskesmas Pembantu (Pustu), unit Puskesmas Keliling (Puskel), dan unit bidan desa/komunitas (Peraturan Menteri Kesehatan RI No. 75 Tahun 2014 tentang Pusat Kesehatan Masyarakat).""",
            """Public Health Center is technical implementation unit of regency health department that have the primary function as a first-level health care providers. The working area standard of public health center is one district and to reach their working areas, public health centers have a service network covering subsidiary of public health center, mobile public health center units, and midwife units (Regulation of the Minister of Health of Indonesia Number 75 Year 2014 about Public Health Center)."""
        )
    ]

    bab4_intro = render_chapter_intro(
        chapter_num=4,
        title_id="SOSIAL DAN KESEJAHTERAAN RAKYAT",
        title_en="SOCIAL AND WELFARE",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab4
    )

    # --- 4.1.1 Fasilitas Pendidikan di Desa (Podes) ---
    rows_411_raw = get_kecamatan_tab_rows("4.1.1", nama_singkat)
    t411_rows = []
    
    # Cari letak 'Template yang dipakai' di raw rows
    template_idx = None
    for idx, r in enumerate(rows_411_raw):
        if r and any("template yang dipak" in str(c).lower() or "template yang dipakai" in str(c).lower() for c in r):
            template_idx = idx
            break

    if template_idx is not None and len(rows_411_raw) > template_idx + 2:
        for r in rows_411_raw[template_idx + 3:]:
            if r and str(r[0]).strip() and not any(str(r[0]).lower().startswith(x) for x in ['sumber', 'catatan', 'tingkat', '(']):
                jenjang = str(r[0]).strip()
                y2023 = clean_cell_value(r[1] if len(r) > 1 else "–")
                y2024 = clean_cell_value(r[2] if len(r) > 2 else "–")
                y2025 = clean_cell_value(r[3] if len(r) > 3 else "–")
                t411_rows.append([jenjang, y2023, y2024, y2025])
    elif len(rows_411_raw) > 2:
        for r in rows_411_raw[2:]:
            if r and str(r[0]).strip() and not any(str(r[0]).lower().startswith(x) for x in ['sumber', 'catatan', 'tabel']):
                jenjang = str(r[0]).strip()
                y2023 = clean_cell_value(r[1] if len(r) > 1 else "–")
                y2024 = clean_cell_value(r[2] if len(r) > 2 else "–")
                y2025 = clean_cell_value(r[3] if len(r) > 3 else "–")
                t411_rows.append([jenjang, y2023, y2024, y2025])

    if not t411_rows:
        default_jenjang = [
            "Taman Kanak-Kanak (TK)/Raudatul Athfal (RA)/Bustanul Athfal (BA)\n Kindergarten",
            "Sekolah Dasar (SD)/Madrasah Ibtidaiyah (MI)\n Primary School",
            "Sekolah Menengah Pertama (SMP)/Madrasah Tsanawiyah (MTs)\n Junior High School",
            "Sekolah Menengah Atas (SMA)/Madrasah Aliyah (MA)\n Senior High School",
            "Sekolah Menengah Kejuruan (SMK)\n Vocational High School",
            "Akademi/Perguruan Tinggi\n Academy/University"
        ]
        t411_rows = [[j, "–", "–", "–"] for j in default_jenjang]

    t411_markup = render_typst_table(
        table_no="4.1.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di {nama_resmi}, 2023–2025",
        title_en=f"Number of Villages#super[1]/Subdistricts Having Educational Facilities by Educational Level in {nama_en} District, 2023–2025",
        headers=["Tingkat Pendidikan\nEducational Level", "2023#super[2]", "2024#super[3]", "2025#super[3]"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t411_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"2 Kantor Camat {nama_singkat}/ {nama_singkat} District Office\n3 Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/ BPS-Statistics Indonesia, Village Potential Data Collecting",
        note="1 Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait / Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries"
    )

    def extract_edu_rows(raw_rows):
        res = []
        if len(raw_rows) > 3:
            for r in raw_rows[3:]:
                if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan', 'tingkat', '(']):
                    lvl = r[0].strip()
                    n24 = clean_cell_value(r[1] if len(r) > 1 else "–")
                    n25 = clean_cell_value(r[2] if len(r) > 2 else "–")
                    s24 = clean_cell_value(r[3] if len(r) > 3 else "–")
                    s25 = clean_cell_value(r[4] if len(r) > 4 else "–")
                    j24 = clean_cell_value(r[5] if len(r) > 5 else "–")
                    j25 = clean_cell_value(r[6] if len(r) > 6 else "–")
                    res.append([lvl, n24, n25, s24, s25, j24, j25])
        if not res:
            default_jenjang = [
                "Taman Kanak-Kanak (TK)", "Raudatul Athfal (RA)",
                "Sekolah Dasar (SD)", "Madrasah Ibtidaiyah (MI)",
                "Sekolah Menengah Pertama (SMP)", "Madrasah Tsanawiyah (MTs)",
                "Sekolah Menengah Atas (SMA)", "Sekolah Menengah Kejuruan (SMK)",
                "Madrasah Aliyah (MA)", "Jumlah / Total"
            ]
            res = [[j, "–", "–", "–", "–", "–", "–"] for j in default_jenjang]
        return res

    edu_headers_7 = [
        "Tingkat Pendidikan\nEducational Level",
        "Negeri/Public\n2024/2025",
        "Negeri/Public\n2025/2026",
        "Swasta/Private\n2024/2025",
        "Swasta/Private\n2025/2026",
        "Jumlah/Total\n2024/2025",
        "Jumlah/Total\n2025/2026"
    ]
    edu_cols_7 = ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)"]
    edu_widths_7 = ["1.9fr", "1.0fr", "1.0fr", "1.0fr", "1.0fr", "1.0fr", "1.0fr"]

    edu_custom_hdr = get_edu_two_tier_header("2024/2025", "2025/2026")

    # --- 4.1.2 Satuan Pendidikan (TK, SD, SMP, SMA) ---
    rows_412_raw = get_kecamatan_tab_rows("4.1.2", nama_singkat)
    t412_rows = extract_edu_rows(rows_412_raw)
    t412_markup = render_typst_table(
        table_no="4.1.2",
        title_id=f"Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025 dan 2025/2026",
        title_en=f"Number of Schools by Educational Level in {nama_en} District, 2024/2025 and 2025/2026",
        headers=edu_headers_7,
        col_numbers=edu_cols_7,
        rows=t412_rows,
        col_widths=edu_widths_7,
        source=edu_sumber,
        custom_header=edu_custom_hdr,
        header_rows_count=2
    )

    # --- 4.1.3 Jumlah Pendidik/Guru ---
    rows_413_raw = get_kecamatan_tab_rows("4.1.3", nama_singkat)
    t413_rows = extract_edu_rows(rows_413_raw)
    t413_markup = render_typst_table(
        table_no="4.1.3",
        title_id=f"Jumlah Pendidik Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025 dan 2025/2026",
        title_en=f"Number of Teachers by Educational Level in {nama_en} District, 2024/2025 and 2025/2026",
        headers=edu_headers_7,
        col_numbers=edu_cols_7,
        rows=t413_rows,
        col_widths=edu_widths_7,
        source=edu_sumber,
        custom_header=edu_custom_hdr,
        header_rows_count=2
    )

    # --- 4.1.4 Jumlah Peserta Didik/Murid ---
    rows_414_raw = get_kecamatan_tab_rows("4.1.4", nama_singkat)
    t414_rows = extract_edu_rows(rows_414_raw)
    t414_markup = render_typst_table(
        table_no="4.1.4",
        title_id=f"Jumlah Peserta Didik Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025 dan 2025/2026",
        title_en=f"Number of Pupils by Educational Level in {nama_en} District, 2024/2025 and 2025/2026",
        headers=edu_headers_7,
        col_numbers=edu_cols_7,
        rows=t414_rows,
        col_widths=edu_widths_7,
        source=edu_sumber,
        custom_header=edu_custom_hdr,
        header_rows_count=2
    )

    # --- 4.2.1 Sarana Kesehatan ---
    rows_421_raw = get_kecamatan_tab_rows("4.2.1", nama_singkat)
    t421_rows = []
    if len(rows_421_raw) > 2:
        for r in rows_421_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                sarana = r[0].strip()
                y2023 = clean_cell_value(r[1] if len(r) > 1 else "–")
                y2024 = clean_cell_value(r[2] if len(r) > 2 else "–")
                y2025 = clean_cell_value(r[3] if len(r) > 3 else "–")
                t421_rows.append([sarana, y2023, y2024, y2025])
    if not t421_rows:
        default_sarana = [
            "Rumah Sakit / Hospital", "Puskesmas Rawat Inap / Inpatient Health Center",
            "Puskesmas Tanpa Rawat Inap / Outpatient Health Center", "Puskesmas Pembantu (Pustu) / Sub-Health Center",
            "Poliklinik/Balai Pengobatan / Clinic", "Tempat Praktik Dokter / Doctor's Practice",
            "Tempat Praktik Bidan / Midwife's Practice", "Poskesdes/Polindes / Village Health Post",
            "Apotek / Pharmacy", "Toko Obat / Medicine Shop"
        ]
        t421_rows = [[s, "–", "–", "–"] for s in default_sarana]

    t421_markup = render_typst_table(
        table_no="4.2.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan yang Memiliki Sarana Kesehatan Menurut Jenis Sarana Kesehatan di {nama_resmi}, 2023–2025",
        title_en=f"Number of Villages#super[1]/Subdistricts Having Health Facilities by Type of Health Facilities in {nama_en} District, 2023–2025",
        headers=["Jenis Sarana Kesehatan\nType of Health Facilities", "2023#super[2]", "2024#super[3]", "2025#super[3]"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t421_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"2Kantor Camat {nama_singkat}/ {nama_singkat} District Office \n3Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/BPS–Statistics Indonesia, Village Potential Data Collecting",
        note=podes_catatan
    )

    # --- 4.3.1 Penerangan Jalan Utama ---
    rows_431_raw = get_kecamatan_tab_rows("4.3.1", nama_singkat)
    t431_rows = []
    if len(rows_431_raw) > 2:
        for r in rows_431_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                sumber_p = r[0].strip()
                y2023 = clean_cell_value(r[1] if len(r) > 1 else "–")
                y2024 = clean_cell_value(r[2] if len(r) > 2 else "–")
                y2025 = clean_cell_value(r[3] if len(r) > 3 else "–")
                t431_rows.append([sumber_p, y2023, y2024, y2025])
    if not t431_rows:
        default_light = [
            "Listrik Pemerintah / State Electricity",
            "Listrik Non-Pemerintah / Non-State Electricity",
            "Non Listrik / Non-Electric"
        ]
        t431_rows = [[s, "–", "–", "–"] for s in default_light]

    t431_markup = render_typst_table(
        table_no="4.3.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan Menurut Sumber Penerangan Jalan Utama Desa/Kelurahan di {nama_resmi}, 2023–2025",
        title_en=f"Number of Villages#super[1]/Subdistricts by Source of Main Street Illumination in {nama_en} District, 2023–2025",
        headers=["Sumber Penerangan Jalan Utama\nSource of Main Street Illumination", "2023#super[2]", "2024#super[3]", "2025#super[3]"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t431_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"2Kantor Camat {nama_singkat}/ {nama_singkat} District Office \n3Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/BPS–Statistics Indonesia, Village Potential Data Collecting",
        note=podes_catatan
    )

    # --- 4.3.2 Bahan Bakar Memasak ---
    rows_432_raw = get_kecamatan_tab_rows("4.3.2", nama_singkat)
    t432_rows = []
    if len(rows_432_raw) > 2:
        for r in rows_432_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                bb = r[0].strip()
                jml = clean_cell_value(r[1] if len(r) > 1 else "–")
                t432_rows.append([bb, jml])
    if not t432_rows:
        default_fuel = [
            "Gas Kota / City Gas", "LPG 3 kg / 3 kg LPG", "LPG > 3 kg / > 3 kg LPG",
            "Minyak Tanah / Kerosene", "Kayu Bakar / Firewood", "Lainnya / Others"
        ]
        t432_rows = [[s, "–"] for s in default_fuel]

    t432_markup = render_typst_table(
        table_no="4.3.2",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan Menurut Jenis Bahan Bakar untuk Memasak yang Digunakan Sebagian Besar Keluarga di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts by Type of Cooking Fuel Used by Majority Family in {nama_en} District, 2025",
        headers=["Jenis Bahan Bakar Memasak\nType of Cooking Fuel", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t432_rows,
        col_widths=["3.4fr", "1.4fr"],
        source=podes_sumber,
        note=podes_catatan
    )

    # --- 4.4.1 Bencana Alam ---
    rows_441_raw = get_kecamatan_tab_rows("4.4.1", nama_singkat)
    t441_rows = []
    if len(rows_441_raw) > 2:
        for r in rows_441_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                bencana = r[0].strip()
                jml = clean_cell_value(r[1] if len(r) > 1 else "–")
                t441_rows.append([bencana, jml])
    if not t441_rows:
        default_disaster = [
            "Tanah Longsor / Landslide", "Banjir / Flood", "Banjir Bandang / Flash Flood",
            "Gempa Bumi / Earthquake", "Gelombang Pasang Laut / Tidal Wave", "Angin Puyuh/Puting Beliung / Tornado",
            "Gunung Meletus / Volcanic Eruption", "Kebakaran Hutan dan Lahan / Forest and Land Fire", "Kekeringan / Drought"
        ]
        t441_rows = [[s, "–"] for s in default_disaster]

    t441_markup = render_typst_table(
        table_no="4.4.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan yang Mengalami Kejadian Bencana Alam Menurut Jenis Bencana Alam di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Natural Disaster Events by Type in {nama_en} District, 2025",
        headers=["Jenis Bencana Alam\nType of Natural Disaster", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t441_rows,
        col_widths=["3.4fr", "1.4fr"],
        source=podes_sumber,
        note=podes_catatan
    )

    # --- 4.4.2 Korban Jiwa Bencana Alam ---
    rows_442_raw = get_kecamatan_tab_rows("4.4.2", nama_singkat)
    t442_rows = []
    if len(rows_442_raw) > 2:
        for r in rows_442_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                bencana = r[0].strip()
                jml = clean_cell_value(r[1] if len(r) > 1 else "–")
                t442_rows.append([bencana, jml])
    if not t442_rows:
        t442_rows = [[s, "–"] for s in ["Tanah Longsor / Landslide", "Banjir / Flood", "Angin Puyuh/Puting Beliung / Tornado", "Kebakaran Hutan dan Lahan / Forest and Land Fire"]]

    t442_markup = render_typst_table(
        table_no="4.4.2",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan yang Terdapat Korban Jiwa Akibat Bencana Alam Menurut Jenis Bencana Alam di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Fatalities Due to Natural Disasters by Type in {nama_en} District, 2025",
        headers=["Jenis Bencana Alam\nType of Natural Disaster", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t442_rows,
        col_widths=["3.4fr", "1.4fr"],
        source=podes_sumber,
        note=podes_catatan
    )

    # --- 4.4.3 Fasilitas Mitigasi Bencana ---
    rows_443_raw = get_kecamatan_tab_rows("4.4.3", nama_singkat)
    t443_rows = []
    if len(rows_443_raw) > 2:
        for r in rows_443_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                fasilitas = r[0].strip()
                if "pembuatan" in fasilitas.lower() and "normalisasi" in fasilitas.lower():
                    fasilitas = "Pembuatan, perawatan, atau normalisasi sungai, kanal, tanggul, dll\nManufacture, maintenance, or normalization of rivers, canals, etc"
                jml = clean_cell_value(r[1] if len(r) > 1 else "–")
                t443_rows.append([fasilitas, jml])
    if not t443_rows:
        default_mitigasi = [
            "Sistem Peringatan Dini Bencana Alam / Early Warning System",
            "Sistem Peringatan Dini Khusus Tsunami / Tsunami Early Warning System",
            "Perlengkapan Keselamatan / Safety Equipment",
            "Rambu-rambu dan Jalur Evakuasi Bencana / Evacuation Signs and Routes",
            "Pembuatan, Perawatan, atau Normalisasi / Construction, Maintenance, or Normalization"
        ]
        t443_rows = [[s, "–"] for s in default_mitigasi]

    t443_markup = render_typst_table(
        table_no="4.4.3",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Fasilitas/Upaya Antisipasi/Mitigasi Bencana Alam Menurut Jenis di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Mitigation Facilities in {nama_en} District, 2025",
        headers=["Jenis Fasilitas/Upaya Antisipasi/Mitigasi\nType of Facilities/Efforts for Anticipation/Mitigation", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t443_rows,
        col_widths=["3.4fr", "1.4fr"],
        source=podes_sumber,
        note=podes_catatan
    )

    sec_41 = render_subchapter_heading("4.1", "Pendidikan", "Education")
    sec_42 = render_subchapter_heading("4.2", "Kesehatan", "Health")
    sec_43 = render_subchapter_heading("4.3", "Perumahan dan Lingkungan", "Housing and Environment")
    sec_44 = render_subchapter_heading("4.4", "Sosial Lainnya", "Religion and Other Social Affairs")

    return f"""
// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT
// ==========================================
{bab4_intro}
{chart_section}
// ==========================================
// TABEL DATA BAB 4 (1 HALAMAN 1 TABEL)
// ==========================================
{sec_41}{t411_markup}
#pagebreak()

{t412_markup}
#pagebreak()

{t413_markup}
#pagebreak()

{t414_markup}
#pagebreak()

{sec_42}{t421_markup}
#pagebreak()

{sec_43}{t431_markup}
#pagebreak()

{t432_markup}
#pagebreak()

{sec_44}{t441_markup}
#pagebreak()

{t442_markup}
#pagebreak()

{t443_markup}
"""
