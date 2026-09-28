"""
Frontmatter: TOC, LOT, LOG, & Explanatory Notes for KCDA 2026.
Menangani Halaman Daftar Isi, Daftar Tabel, Daftar Gambar, dan Penjelasan Umum.
Format diselaraskan 100% dengan standar acuan BPS (foto 3EB00F00C37CA2448B231D.jpg & 3EB04675B2F1B6EA719590.jpg).
"""

from typing import Dict, Any

def render_toc_and_notes(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()
    slug = cfg.get("slug", "")
    issn = cfg.get("issn", "")
    volume = cfg.get("volume", "Volume 17, 2026")
    issn_header = f"#align(right)[#text(8pt)[ISSN {issn}]]\n#v(4pt)\n" if issn else ""

    has_214 = slug not in ["mempawah-hilir", "sungai-pinyuh"]
    year_213 = "2025" if slug == "toho" else "2026"
    year_214 = "2025" if slug == "toho" else "2026"

    toc_214_entry = f"""#v(5pt)
#toc_table_entry("2.1.4", "Nama-Nama Kepala Dusun di Kecamatan {nama_singkat}, {year_214}", "Names of Hamlet Heads in {nama_en} District, {year_214}", get_page_arabic(<tab_2_1_4>))""" if has_214 else ""

    return f"""// ==========================================
// 8. DAFTAR ISI / CONTENTS
// ==========================================
#pagebreak()
#metadata("daftar_isi") <daftar_isi>

#set text(font: "Liberation Sans", size: 7.8pt, fill: rgb("#1F2937"), hyphenate: false)
#set par(leading: 0.48em)

#let get_page_roman(lbl, default: "-") = context {{
  let elems = query(lbl)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("i", p)
  }} else {{
    default
  }}
}}

#let get_page_arabic(lbl, default: "-") = context {{
  let elems = query(lbl)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  }} else {{
    default
  }}
}}

// Helper functions for Dot Leaders in DAFTAR ISI
#let toc_chapter(no, id_title, en_title, page_val) = {{
  grid(
    columns: (16pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}}

#let toc_subchapter(no, id_title, en_title, page_val) = {{
  grid(
    columns: (14pt, 24pt, 1fr, auto),
    column-gutter: (0pt, 4pt, 6pt),
    align: (top + left, top + left, top + left, bottom + right),
    [],
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}}

#let toc_section(id_title, en_title, page_val) = {{
  grid(
    columns: (1fr, auto),
    column-gutter: 6pt,
    align: (bottom + left, bottom + right),
    [#id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
    [#page_val]
  )
}}

// Helper functions for Dot Leaders in DAFTAR TABEL
#let toc_table_chapter(no, id_title, en_title, page_val) = {{
  grid(
    columns: (30pt, 1fr, auto),
    column-gutter: 6pt,
    align: (top + left, top + left, bottom + right),
    [#text(weight: "bold")[#no]],
    [#text(weight: "bold")[#upper(id_title)/#text(style: "italic")[#upper(en_title)]]],
    [#text(weight: "bold")[#page_val]]
  )
}}

#let toc_table_subchapter(no, id_title, en_title, page_val) = {{
  grid(
    columns: (30pt, 1fr, auto),
    column-gutter: 6pt,
    align: (top + left, top + left, bottom + right),
    [#text(weight: "bold")[#no]],
    [#text(weight: "bold")[#id_title/#text(style: "italic")[#en_title]]],
    [#text(weight: "bold")[#page_val]]
  )
}}

#let toc_table_entry(no, id_title, en_title, page_val) = {{
  grid(
    columns: (30pt, 1fr),
    column-gutter: 6pt,
    align: (top + left, top + left),
    [#no],
    [
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#id_title #box(width: 1fr, repeat[ . ])],
        [#page_val]
      )
      #v(2pt)
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
        [#text(style: "italic")[#page_val]]
      )
    ]
  )
}}

// Helper functions for Dot Leaders in DAFTAR GAMBAR
#let toc_figure_entry(no, id_title, en_title, page_val) = {{
  grid(
    columns: (26pt, 1fr),
    column-gutter: 6pt,
    align: (top + left, top + left),
    [#no],
    [
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#id_title #box(width: 1fr, repeat[ . ])],
        [#page_val]
      )
      #v(2pt)
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
        [#text(style: "italic")[#page_val]]
      )
    ]
  )
}}

{issn_header}#align(center)[
  #text(10pt, weight: "bold")[DAFTAR ISI/]#text(10pt, weight: "bold", style: "italic")[CONTENTS]

  #v(2pt)
  #text(9pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026]

  #text(8.5pt, style: "italic")[{nama_en} District in Figures 2026]

  #v(1pt)
  #text(7.5pt)[{volume}]
]

#v(6pt)
#align(right)[
  #text(7.5pt)[halaman] \
  #text(7pt, style: "italic")[page]
]
#v(2pt)

#toc_section("Kata Pengantar", "Preface", get_page_roman(<kata_pengantar>))
#v(2pt)
#toc_section("Daftar Isi", "Contents", get_page_roman(<daftar_isi>))
#v(2pt)
#toc_section("Daftar Tabel", "List of Tables", get_page_roman(<daftar_tabel>))
#v(2pt)
#toc_section("Daftar Gambar", "List of Figures", get_page_roman(<daftar_gambar>))
#v(2pt)
#toc_section("Penjelasan Umum", "Explanatory Notes", get_page_roman(<penjelasan_umum>))
#v(3pt)

#toc_chapter("1", "Geografi", "Geography", get_page_arabic(<bab1>))
#v(2pt)
#toc_chapter("2", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(1.5pt)
#toc_subchapter("2.1", "Wilayah Administratif", "Administrative Area", get_page_arabic(<tab_2_1_1>))
#v(1.5pt)
#toc_subchapter("2.2", "Sumber Daya Manusia", "Human Resources", get_page_arabic(<tab_2_2_1>))
#v(2.5pt)
#toc_chapter("3", "Penduduk", "Population", get_page_arabic(<bab3>))
#v(2.5pt)
#toc_chapter("4", "Sosial dan Kesejahteraan Rakyat", "Social And Welfare", get_page_arabic(<bab4>))
#v(1.5pt)
#toc_subchapter("4.1", "Pendidikan", "Education", get_page_arabic(<tab_4_1_1>))
#v(1.5pt)
#toc_subchapter("4.2", "Kesehatan", "Health", get_page_arabic(<tab_4_2_1>))
#v(1.5pt)
#toc_subchapter("4.3", "Perumahan dan Lingkungan", "Housing and Environment", get_page_arabic(<tab_4_3_1>))
#v(1.5pt)
#toc_subchapter("4.4", "Sosial Lainnya", "Religion and Other Social Affairs", get_page_arabic(<tab_4_4_1>))
#v(2.5pt)
#toc_chapter("5", "Pertanian", "Agriculture", get_page_arabic(<bab5>))
#v(2.5pt)
#toc_chapter("6", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(1.5pt)
#toc_subchapter("6.1", "Pariwisata", "Tourism", get_page_arabic(<tab_6_1_1>))
#v(1.5pt)
#toc_subchapter("6.2", "Transportasi", "Transportation", get_page_arabic(<tab_6_2_1>))
#v(1.5pt)
#toc_subchapter("6.3", "Komunikasi", "Communication", get_page_arabic(<tab_6_3_1>))
#v(2.5pt)
#toc_chapter("7", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))
#v(3pt)
#toc_section("Daftar Pustaka", "Bibliography", get_page_arabic(<daftar_pustaka>))

#pagebreak()

// ==========================================
// 9. DAFTAR TABEL / LIST OF TABLES
// ==========================================
#metadata("daftar_tabel") <daftar_tabel>
{issn_header}#align(center)[
  #text(10pt, weight: "bold")[DAFTAR TABEL/]#text(10pt, weight: "bold", style: "italic")[LIST OF TABLES]
]

#v(8pt)
#grid(
  columns: (30pt, 1fr, auto),
  column-gutter: 6pt,
  [Tabel \\ #text(style: "italic")[Table]],
  [],
  [#align(right)[halaman \\ #text(style: "italic")[page]]]
)
#v(6pt)

#toc_table_chapter("1", "Geografi", "Geography", get_page_arabic(<bab1>))
#v(5pt)
#toc_table_entry("1.1", "Luas Daerah Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Total Area by Villages/Subdistricts in {nama_en} District, 2025", get_page_arabic(<tab_1_1>))
#v(5pt)
#toc_table_entry("1.2", "Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten/Kota Menurut Desa/Kelurahan di Kecamatan {nama_singkat} (km), 2025", "Distance to District Capital and Regency Capital by Villages/Subdistricts in {nama_en} District (km), 2025", get_page_arabic(<tab_1_2>))
#v(5pt)
#toc_table_entry("1.3", "Batas Administrasi Kecamatan {nama_singkat} Menurut Arah Mata Angin, 2025", "Administrative Borders of {nama_en} District by Cardinal Direction, 2025", get_page_arabic(<tab_1_3>))
#v(5pt)
#toc_table_entry("1.4", "Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025", "Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025", get_page_arabic(<tab_1_4>))

#v(7pt)
#toc_table_chapter("2", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(4pt)
#toc_table_subchapter("2.1", "Wilayah Administratif", "Administrative Area", get_page_arabic(<tab_2_1_1>))
#v(4pt)
#toc_table_entry("2.1.1", "Jumlah Rukun Warga (RW) dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of Rukun Warga and Rukun Tetangga by Villages/Subdistricts in {nama_en} District, 2025", get_page_arabic(<tab_2_1_1>))
#v(5pt)
#toc_table_entry("2.1.2", "Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan {nama_singkat}", "Names of District Heads of {nama_en} District", get_page_arabic(<tab_2_1_2>))
#v(5pt)
#toc_table_entry("2.1.3", "Nama-Nama Kepala Desa/Lurah di Kecamatan {nama_singkat}, {year_213}", "Names of Village Heads in {nama_en} District, {year_213}", get_page_arabic(<tab_2_1_3>))
{toc_214_entry}
#v(5pt)
#toc_table_entry("2.1.5", "Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di Kecamatan {nama_singkat}, 2020", "Urban and Rural Classification of Village/Subdistrict in {nama_en} District, 2020", get_page_arabic(<tab_2_1_5>))
#v(5pt)
#toc_table_entry("2.1.6", "Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan {nama_singkat}, 2024", "Village Status Based on Developing Village Index (IDM) in {nama_en} District, 2024", get_page_arabic(<tab_2_1_6>))

#v(6pt)
#toc_table_subchapter("2.2", "Sumber Daya Manusia", "Human Resources", get_page_arabic(<tab_2_2_1>))
#v(4pt)
#toc_table_entry("2.2.1", "Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin di Kecamatan {nama_singkat}, 2025", "Number of Government Employee by Local Government and Sex in {nama_en} District, 2025", get_page_arabic(<tab_2_2_1>))
#v(5pt)
#toc_table_entry("2.2.2", "Jumlah Pegawai Negeri Sipil Pemerintah Kecamatan {nama_singkat} Menurut Tingkat Pendidikan dan Jenis Kelamin, 2025", "Number of Government Employee of {nama_en} District Government by Educational Level and Sex, 2025", get_page_arabic(<tab_2_2_2>))

#v(7pt)
#toc_table_chapter("3", "Penduduk", "Population", get_page_arabic(<bab3>))
#v(5pt)
#toc_table_entry("3.1", "Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Population, Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in {nama_en} District, 2025", get_page_arabic(<tab_3_1>))

#v(7pt)
#toc_table_chapter("4", "Sosial dan Kesejahteraan Rakyat", "Social and Welfare", get_page_arabic(<bab4>))
#v(4pt)
#toc_table_subchapter("4.1", "Pendidikan", "Education", get_page_arabic(<tab_4_1_1>))
#v(4pt)
#toc_table_entry("4.1.1", "Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2023–2025", "Number of Villages/Subdistricts Having Educational Facilities by Educational Level in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_1_1>))
#v(5pt)
#toc_table_entry("4.1.2", "Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2024/2025 dan 2025/2026", "Number of Schools by Educational Level in {nama_en} District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_2>))
#v(5pt)
#toc_table_entry("4.1.3", "Jumlah Pendidik Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2024/2025 dan 2025/2026", "Number of Teachers by Educational Level in {nama_en} District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_3>))
#v(5pt)
#toc_table_entry("4.1.4", "Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2024/2025 dan 2025/2026", "Number of Pupils by Educational Level in {nama_en} District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_4>))

#v(6pt)
#toc_table_subchapter("4.2", "Kesehatan", "Health", get_page_arabic(<tab_4_2_1>))
#v(4pt)
#toc_table_entry("4.2.1", "Banyaknya Desa/Kelurahan yang Memiliki Sarana Kesehatan Menurut Jenis Sarana Kesehatan di Kecamatan {nama_singkat}, 2023–2025", "Number of Villages/Subdistricts Health Facilities by Type of Health Facilities in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_2_1>))

#v(6pt)
#toc_table_subchapter("4.3", "Perumahan dan Lingkungan", "Housing and Environment", get_page_arabic(<tab_4_3_1>))
#v(4pt)
#toc_table_entry("4.3.1", "Banyaknya Desa/Kelurahan Menurut Sumber Penerangan Jalan Utama Desa/Kelurahan di Kecamatan {nama_singkat}, 2023–2025", "Number of Villages/Subdistricts by Source of Main Street Illumination in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_3_1>))
#v(5pt)
#toc_table_entry("4.3.2", "Banyaknya Desa/Kelurahan Menurut Jenis Bahan Bakar untuk Memasak yang Digunakan Sebagian Besar Keluarga di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts by Type of Cooking Fuel Used by Majority Family in {nama_en} District, 2025", get_page_arabic(<tab_4_3_2>))

#v(6pt)
#toc_table_subchapter("4.4", "Sosial Lainnya", "Religion and Other Social Affairs", get_page_arabic(<tab_4_4_1>))
#v(4pt)
#toc_table_entry("4.4.1", "Banyaknya Desa/Kelurahan yang Mengalami Kejadian Bencana Alam Menurut Jenis Bencana Alam di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Natural Disaster Events by Type in {nama_en} District, 2025", get_page_arabic(<tab_4_4_1>))
#v(5pt)
#toc_table_entry("4.4.2", "Banyaknya Desa/Kelurahan yang Terdapat Korban Jiwa Akibat Bencana Alam Menurut Jenis Bencana Alam di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Fatalities Due to Natural Disasters by Type in {nama_en} District, 2025", get_page_arabic(<tab_4_4_2>))
#v(5pt)
#toc_table_entry("4.4.3", "Banyaknya Desa/Kelurahan dengan Keberadaan Fasilitas/Upaya Antisipasi/Mitigasi Bencana Alam Menurut Jenis di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Availability of Mitigation Facilities in {nama_en} District, 2025", get_page_arabic(<tab_4_4_3>))

#v(7pt)
#toc_table_chapter("5", "Pertanian", "Agriculture", get_page_arabic(<bab5>))
#v(5pt)
#toc_table_entry("5.1", "Luas Panen Tanaman Sayuran dan Buah–buahan Semusim Menurut Jenis Tanaman di Kecamatan {nama_singkat} (ha), 2022–2025", "Harvested Area of Seasonal Vegetables and Fruits by Kind of Plant in {nama_en} District (ha), 2022–2025", get_page_arabic(<tab_5_1>))
#v(5pt)
#toc_table_entry("5.2", "Produksi Tanaman Sayuran dan Buah–buahan Semusim Menurut Jenis Tanaman di Kecamatan {nama_singkat} (kuintal), 2022–2025", "Production of Seasonal Vegetables and Fruits by Kind of Plant in {nama_en} District (quintal), 2022–2025", get_page_arabic(<tab_5_2>))
#v(5pt)
#toc_table_entry("5.3", "Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan {nama_singkat} (m²), 2022–2025", "Harvested Area of Medicinal Plants by Kind of Plant in {nama_en} District (sq.m), 2022–2025", get_page_arabic(<tab_5_3>))
#v(5pt)
#toc_table_entry("5.4", "Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan {nama_singkat} (kg), 2022–2025", "Production of Medicinal Plants by Kind of Plant in {nama_en} District (kg), 2022–2025", get_page_arabic(<tab_5_4>))
#v(5pt)
#toc_table_entry("5.5", "Luas Panen Tanaman Hias Menurut Jenis Tanaman di Kecamatan {nama_singkat} (m²), 2022–2025", "Harvested Area of Ornamental Plants by Kind of Plant in {nama_en} District (sq.m), 2022–2025", get_page_arabic(<tab_5_5>))
#v(5pt)
#toc_table_entry("5.6", "Produksi Tanaman Hias Menurut Jenis Tanaman di Kecamatan {nama_singkat} (tangkai), 2022–2025", "Production of Ornamental Plants by Kind of Plant in {nama_en} District (stalks), 2022–2025", get_page_arabic(<tab_5_6>))
#v(5pt)
#toc_table_entry("5.7", "Produksi Buah–buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan {nama_singkat} (kuintal), 2022–2025", "Production of Annual Fruits and Vegetables by Kind of Plant in {nama_en} District (quintal), 2022–2025", get_page_arabic(<tab_5_7>))

#v(7pt)
#toc_table_chapter("6", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(4pt)
#toc_table_subchapter("6.1", "Pariwisata", "Tourism", get_page_arabic(<tab_6_1_1>))
#v(4pt)
#toc_table_entry("6.1.1", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Akomodasi Menurut Jenis Akomodasi di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Availability of Accommodation Facilities by Type of Accommodation in {nama_en} District, 2025", get_page_arabic(<tab_6_1_1>))
#v(6pt)
#toc_table_subchapter("6.2", "Transportasi", "Transportation", get_page_arabic(<tab_6_2_1>))
#v(4pt)
#toc_table_entry("6.2.1", "Banyaknya Desa/Kelurahan Menurut Prasarana dan Sarana Transportasi Antardesa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts by Transportation Infrastructure and Facilities Between Villages/Subdistricts in {nama_en} District, 2025", get_page_arabic(<tab_6_2_1>))
#v(6pt)
#toc_table_subchapter("6.3", "Komunikasi", "Communication", get_page_arabic(<tab_6_3_1>))
#v(4pt)
#toc_table_entry("6.3.1", "Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos/Pos Pembantu/Rumah Pos, Pos Keliling, dan Perusahaan/Agen Jasa Ekspedisi Swasta di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Postal and Expedition Services in {nama_en} District, 2025", get_page_arabic(<tab_6_3_1>))

#v(7pt)
#toc_table_chapter("7", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))
#v(5pt)
#toc_table_entry("7.1", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Lembaga Keuangan Bank Menurut Jenis Bank di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Availability of Bank by Type of Bank in {nama_en} District, 2025", get_page_arabic(<tab_7_1>))
#v(5pt)
#toc_table_entry("7.2", "Banyaknya Desa/Kelurahan dengan Keberadaan Koperasi Aktif Menurut Jenis Koperasi di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Availability of Active Cooperatives by Type in {nama_en} District, 2025", get_page_arabic(<tab_7_2>))
#v(5pt)
#toc_table_entry("7.3", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Perdagangan Menurut Jenis Sarana Perdagangan di Kecamatan {nama_singkat}, 2025", "Number of Villages/Subdistricts with Availability of Trade Facilities by Type in {nama_en} District, 2025", get_page_arabic(<tab_7_3>))

#pagebreak()

// ==========================================
// 10. DAFTAR GAMBAR / LIST OF FIGURES
// ==========================================
#metadata("daftar_gambar") <daftar_gambar>
{issn_header}#align(center)[
  #text(10pt, weight: "bold")[DAFTAR GAMBAR/]#text(10pt, weight: "bold", style: "italic")[LIST OF FIGURES]
]

#v(8pt)
#grid(
  columns: (26pt, 1fr, auto),
  column-gutter: 6pt,
  [Gambar \\ #text(style: "italic")[Figure]],
  [],
  [#align(right)[halaman \\ #text(style: "italic")[page]]]
)
#v(6pt)

#toc_figure_entry("1", "Peta Wilayah Kecamatan {nama_singkat}, 2025", "Map of {nama_en} District, 2025", get_page_arabic(<fig_peta>))
#v(5pt)
#toc_figure_entry("2", "Jarak ke Ibukota Kecamatan Menurut Desa/Kelurahan di Kecamatan {nama_singkat} (km), 2025", "Distance to District Capital by Village/Subdistrict in {nama_en} District (km), 2025", get_page_arabic(<fig_1_1>))
#v(5pt)
#toc_figure_entry("3", "Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of RT by Village in {nama_en} District, 2025", get_page_arabic(<fig_2_1>))
#v(5pt)
#toc_figure_entry("4", "Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan {nama_singkat}, 2025", "Population by Sex in {nama_en} District, 2025", get_page_arabic(<fig_3_1>))
#v(5pt)
#toc_figure_entry("5", "Banyaknya Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2025", "Number of School Facilities by Level in {nama_en} District, 2025", get_page_arabic(<fig_4_1>))
#v(5pt)
#toc_figure_entry("6", "Produksi Tanaman Hortikultura Unggulan di Kecamatan {nama_singkat}, 2025", "Production of Leading Horticulture Crops in {nama_en} District, 2025", get_page_arabic(<fig_5_1>))
#v(5pt)
#toc_figure_entry("7", "Prasarana dan Sarana Komunikasi Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Communication Infrastructure by Village in {nama_en} District, 2025", get_page_arabic(<fig_6_1>))
#v(5pt)
#toc_figure_entry("8", "Keberadaan Sarana Perdagangan dan Koperasi Aktif di Kecamatan {nama_singkat}, 2025", "Trading Facilities and Active Cooperatives in {nama_en} District, 2025", get_page_arabic(<fig_7_1>))

#pagebreak()

// ==========================================
// 11. PENJELASAN UMUM / EXPLANATORY NOTES
// ==========================================
#metadata("penjelasan_umum") <penjelasan_umum>
{issn_header}#align(center)[
  #text(10pt, weight: "bold")[PENJELASAN UMUM/]#text(10pt, weight: "bold", style: "italic")[EXPLANATORY NOTES]
]

#v(8pt)
#text(8pt)[
Tanda-tanda, satuan-satuan, dan lain-lainnya yang digunakan dalam publikasi ini adalah sebagai berikut: \\
#text(style: "italic")[Symbols, measurement units, and acronyms which are used in this publication, are as follows:]
]

#v(6pt)
#text(8.5pt, weight: "bold")[1. TANDA-TANDA/]#text(8.5pt, weight: "bold", style: "italic")[SYMBOLS]
#v(3pt)
#grid(
  columns: (34pt, auto, 1fr),
  row-gutter: 4.5pt,
  [*...*], [ : ], [Data tidak tersedia / #text(style: "italic")[Data not available]],
  [*–*], [ : ], [Tidak ada atau nol / #text(style: "italic")[Null or zero]],
  [*0*], [ : ], [Data dapat diabaikan / #text(style: "italic")[Data negligible]],
  [*,*], [ : ], [Tanda desimal / #text(style: "italic")[Decimal point]],
  [*NA*], [ : ], [Data tidak dapat ditampilkan / #text(style: "italic")[Not applicable]],
  [*e*], [ : ], [Angka perkiraan / #text(style: "italic")[Estimated figures]],
  [*x*], [ : ], [Angka sementara / #text(style: "italic")[Preliminary figures]],
  [*xx*], [ : ], [Angka sangat sementara / #text(style: "italic")[Very preliminary figures]],
  [*r*], [ : ], [Angka diperbaiki / #text(style: "italic")[Revised figures]]
)

#v(8pt)
#text(8.5pt, weight: "bold")[2. SATUAN/]#text(8.5pt, weight: "bold", style: "italic")[UNITS]
#v(3pt)
#text(7.5pt)[
barel / #text(style: "italic")[barrel] : 158,99 liter/litres = 1/6,2898 m³ \\
hektar (ha) / #text(style: "italic")[hectare (ha)] : 10.000 m² \\
kilometer (km) / #text(style: "italic")[kilometres (km)] : 1.000 meter/meters (m) \\
knot / #text(style: "italic")[knot] : 1,8523 km/jam (km/hour) \\
kuintal / #text(style: "italic")[quintal] : 100 kg \\
KWh : 1.000 Watt hour \\
MWh : 1.000 KWh \\
liter (untuk beras) / #text(style: "italic")[litre (for rice)] : 0,80 kg \\
ons / #text(style: "italic")[ounce] : 28,31 gram/grams \\
ton : 1.000 kg \\
#v(3pt)
Satuan lain: buah, dus, butir, helai/lembar, kaleng, batang, pulsa, ton kilometer (ton-km), jam, menit, persen (%). \\
#text(style: "italic")[Other units: unit, pack, pieces, sheet, tin, pulse, ton-kilometres (ton-km), hour, minute, percent (%).] \\
#v(3pt)
Perbedaan angka di belakang koma disebabkan oleh pembulatan angka. \\
#text(style: "italic")[The difference in decimal numbers is caused by rounding.]
]
"""
