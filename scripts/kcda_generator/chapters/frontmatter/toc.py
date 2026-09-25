"""
Frontmatter: TOC, LOT, LOG, & Explanatory Notes for KCDA 2026.
Menangani Halaman Daftar Isi (vii), Daftar Tabel (viii), Daftar Gambar (ix), dan Penjelasan Umum (x).
"""

from typing import Dict, Any

def render_toc_and_notes(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()
    issn = cfg.get("issn")
    volume = cfg.get("volume", "Volume 48, 2026")
    issn_header = f"#align(right)[#text(7pt)[ISSN: {issn}]]\n#v(4pt)\n" if issn else ""

    return f"""// ==========================================
// 8. DAFTAR ISI / CONTENTS
// ==========================================
#metadata("daftar_isi") <daftar_isi>

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

// Helper functions for Dot Leaders
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

#let toc_section(title_markup, page_val) = {{
  grid(
    columns: (1fr, auto),
    column-gutter: 6pt,
    align: (bottom + left, bottom + right),
    [#title_markup #box(width: 1fr, repeat[ . ])],
    [#page_val]
  )
}}

#let toc_subchapter(no, id_title, en_title, page_val) = {{
  grid(
    columns: (24pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}}

#let toc_entry_item(no, id_title, en_title, page_val) = {{
  grid(
    columns: (24pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}}

{issn_header}#align(center)[
  #text(10pt, weight: "bold")[DAFTAR ISI/CONTENTS] \\
  #v(2pt)
  #text(9pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026] \\
  #text(8.5pt, style: "italic")[{nama_en} District in Figures 2026] \\
  #v(1pt)
  #text(7.5pt)[{volume}]
]

#v(8pt)
#align(right)[
  #text(7.5pt)[Halaman] \\
  #text(7pt, style: "italic")[Page]
]
#v(4pt)

#toc_section([Kata Pengantar], get_page_roman(<kata_pengantar>))
#v(4pt)
#toc_section([_Preface_], get_page_roman(<preface>))
#v(4pt)
#toc_section([Daftar Isi/_Contents_], get_page_roman(<daftar_isi>))
#v(4pt)
#toc_section([Daftar Tabel/_List of Tables_], get_page_roman(<daftar_tabel>))
#v(4pt)
#toc_section([Daftar Gambar/_List of Figures_], get_page_roman(<daftar_gambar>))
#v(4pt)
#toc_section([Penjelasan Umum/_Explanatory Notes_], get_page_roman(<penjelasan_umum>))
#v(6pt)

#toc_chapter("1.", "Geografi dan Iklim", "Geography and Climate", get_page_arabic(<bab1>))
#v(4pt)
#toc_chapter("2.", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(4pt)
#toc_chapter("3.", "Penduduk", "Population", get_page_arabic(<bab3>))
#v(4pt)
#toc_chapter("4.", "Sosial dan Kesejahteraan Rakyat", "Social and Welfare", get_page_arabic(<bab4>))
#v(4pt)
#toc_chapter("5.", "Pertanian, Kehutanan, Perikanan, dan Peternakan", "Agriculture, Forestry, Livestock, & Fishery", get_page_arabic(<bab5>))
#v(4pt)
#toc_chapter("6.", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(4pt)
#toc_chapter("7.", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))
#v(6pt)
#toc_section([Daftar Pustaka/_Bibliography_], get_page_arabic(<daftar_pustaka>))

#pagebreak()

// ==========================================
// 9. DAFTAR TABEL / LIST OF TABLES
// ==========================================
#metadata("daftar_tabel") <daftar_tabel>
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR TABEL/]#text(10pt, weight: "bold", style: "italic")[LIST OF TABLES]
]

#v(10pt)
#grid(
  columns: (24pt, 1fr, auto),
  column-gutter: (4pt, 6pt),
  [*Tabel*\\ _Table_], [], [*Halaman*\\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Luas Daerah Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Total Area by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Distance to Subdistrict and Regency Capital by Village in {nama_en} District, 2025", get_page_arabic(<tab_1_2>))
#v(5pt)
#toc_entry_item("1.3", "Batas Administrasi Kecamatan {nama_singkat} Menurut Arah Mata Angin, 2025", "Administrative Borders of {nama_en} District by Cardinal Direction, 2025", get_page_arabic(<tab_1_3>))
#v(5pt)
#toc_entry_item("1.4", "Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025", "Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025", get_page_arabic(<tab_1_4>))
#v(5pt)
#toc_entry_item("2.1.1", "Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of Hamlets, RW, and RT by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_2_1_1>))
#v(5pt)
#toc_entry_item("2.1.2", "Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan {nama_singkat}", "Names of District Heads of {nama_en} District", get_page_arabic(<tab_2_1_2>))
#v(5pt)
#toc_entry_item("2.1.3", "Nama-Nama Kepala Desa di Kecamatan {nama_singkat}, 2025", "Names of Village Heads in {nama_en} District, 2025", get_page_arabic(<tab_2_1_3>))
#v(5pt)
#toc_entry_item("3.1", "Penduduk, Distribusi Persentase, Kepadatan, dan Rasio Jenis Kelamin Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Population, Percentage Distribution, Density, and Sex Ratio by Village in {nama_en} District, 2025", get_page_arabic(<tab_3_1>))
#v(5pt)
#toc_entry_item("4.1.1", "Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2023–2025", "Number of Villages Having Educational Facilities by Level in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_1_1>))
#v(5pt)
#toc_entry_item("4.2.1", "Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan {nama_singkat}, 2023–2025", "Number of Health Facilities by Type in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_2_1>))
#v(5pt)
#toc_entry_item("5.1", "Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis di Kecamatan {nama_singkat} (ha), 2022–2025", "Harvested Area of Vegetables and Seasonal Fruits by Type in {nama_en} District (ha), 2022–2025", get_page_arabic(<tab_5_1>))
#v(5pt)
#toc_entry_item("6.1.1", "Keberadaan Sarana Akomodasi Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Accommodation Facilities by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_6_1_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Lembaga Keuangan Bank Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Banking Financial Institutions by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_7_1>))

#pagebreak()

// ==========================================
// 10. DAFTAR GAMBAR / LIST OF FIGURES
// ==========================================
#metadata("daftar_gambar") <daftar_gambar>
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR GAMBAR/]#text(10pt, weight: "bold", style: "italic")[LIST OF FIGURES]
]

#v(10pt)
#grid(
  columns: (24pt, 1fr, auto),
  column-gutter: (4pt, 6pt),
  [*Gambar*\\ _Figure_], [], [*Halaman*\\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di Kecamatan {nama_singkat}, 2025", "Distance from Village/Subdistrict to District Capital in {nama_en} District, 2025", get_page_arabic(<fig_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Luas Wilayah Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Total Area by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<fig_1_2>))
#v(5pt)
#toc_entry_item("2.1", "Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of RT by Village in {nama_en} District, 2025", get_page_arabic(<fig_2_1>))
#v(5pt)
#toc_entry_item("3.1", "Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan {nama_singkat}, 2025", "Population by Sex in {nama_en} District, 2025", get_page_arabic(<fig_3_1>))
#v(5pt)
#toc_entry_item("4.1", "Banyaknya Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2025", "Number of School Facilities by Level in {nama_en} District, 2025", get_page_arabic(<fig_4_1>))
#v(5pt)
#toc_entry_item("5.1", "Produksi Tanaman Hortikultura Unggulan di Kecamatan {nama_singkat}, 2025", "Production of Leading Horticulture Crops in {nama_en} District, 2025", get_page_arabic(<fig_5_1>))
#v(5pt)
#toc_entry_item("6.1", "Prasarana dan Sarana Komunikasi Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Communication Infrastructure by Village in {nama_en} District, 2025", get_page_arabic(<fig_6_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Sarana Perdagangan dan Koperasi Aktif di Kecamatan {nama_singkat}, 2025", "Trading Facilities and Active Cooperatives in {nama_en} District, 2025", get_page_arabic(<fig_7_1>))

#pagebreak()

// ==========================================
// 11. PENJELASAN UMUM / EXPLANATORY NOTES
// ==========================================
#metadata("penjelasan_umum") <penjelasan_umum>
#align(center)[
  #text(10pt, weight: "bold")[PENJELASAN UMUM/]#text(10pt, weight: "bold", style: "italic")[EXPLANATORY NOTES]
]

#v(10pt)
#text(8pt)[
Tanda-tanda khusus, singkatan, serta kesepakatan penulisan yang digunakan dalam publikasi ini adalah sebagai berikut: \\
_Special signs, abbreviations, and conventions used in this publication are as follows:_
]

#v(8pt)
#grid(
  columns: (32pt, 1fr),
  row-gutter: 6pt,
  [*...*], [Data belum tersedia / _Data not yet available_],
  [*–*], [Data tidak ada atau bernilai nol / _Data not available or zero value_],
  [*0 / 0,0*], [Angka lebih kecil dari 0,5 / _Figure less than 0.5_],
  [*x*], [Data dirahasiakan untuk menjaga kerahasiaan individu/unit usaha / _Confidential data_],
  [*ha*], [Hektar / _Hectare_],
  [*km*], [Kilometer / _Kilometer_],
  [*km²*], [Kilometer persegi / _Square kilometer_],
  [*RT/RW*], [Rukun Tetangga / Rukun Warga (_Neighborhood / Hamlet units_)]
)

#v(12pt)
#text(8pt)[
Catatan Pembulatan: Karena adanya pembulatan, angka-angka dalam penjumlahan baris/kolom mungkin tidak selalu sama persis dengan total penjumlahan. \\
_Rounding Note: Due to rounding, figures in line/column totals may not strictly equal the sum of constituent elements._
]
"""
