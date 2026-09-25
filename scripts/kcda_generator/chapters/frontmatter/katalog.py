"""
Frontmatter: Katalog, Tim Penyusun, & Kontributor Data for KCDA.
Menangani Halaman Katalog (ii), Tim Penyusun (iii), dan Kontributor Data (iv).
"""

from typing import Dict, Any
from ...config import (
    get_regency_info,
    get_instansi_info,
    get_pimpinan_info,
    get_publikasi_info
)

def render_katalog_and_contributors(cfg: Dict[str, Any]) -> str:
    regency = get_regency_info()
    instansi = get_instansi_info()
    pimpinan = get_pimpinan_info()
    pub = get_publikasi_info()

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_pub = cfg.get("no_publikasi", "-")
    no_katalog = cfg.get("no_katalog", "-")
    pic_polos = cfg.get("pic_nama_polos", "Staf BPS")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())

    tahun_rilis = pub.get("tahun_rilis", 2026)
    volume = cfg.get("volume", f"Volume 1, {tahun_rilis}")
    issn = cfg.get("issn")

    nama_instansi = instansi.get("nama_resmi", "Badan Pusat Statistik")
    nama_instansi_singkat = instansi.get("nama_singkat", "BPS")
    nama_instansi_en = instansi.get("nama_en", "BPS-Statistics")
    nama_kepala = pimpinan.get("nama_polos", "Kepala BPS")

    issn_katalog = f"\n  #v(2pt)\n  #text(weight: \"bold\")[ISSN:] {issn} \\\\" if issn else ""
    issn_tim = f"#align(right)[\n  #text(7pt, fill: luma(120))[ISSN {issn}]\n]\n" if issn else ""

    return f"""// ==========================================
// 3. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================

// Judul Publikasi Langsung di Bagian Atas (Hitam)
#text(10.5pt, weight: "bold", fill: black)[KECAMATAN {nama_singkat.upper()} DALAM ANGKA {tahun_rilis}] \\
#v(1pt)
#text(9pt, style: "italic", fill: black)[{nama_en.upper()} DISTRICT IN FIGURES {tahun_rilis}] \\
#v(2pt)
#text(7.5pt, fill: black)[{volume}]

#let total_frontmatter_pages = context {{
  let elems = query(<transisi_isi>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    let final_p = if calc.odd(p) {{ p + 1 }} else {{ p }}
    numbering("i", final_p)
  }} else {{
    "xii"
  }}
}}
#let total_arabic_pages = context {{
  let elems = query(<akhir_buku>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  }} else {{
    "28"
  }}
}}

#v(9pt)
#text(7.5pt)[
  #text(weight: "bold")[Katalog/Catalogue:] {no_katalog}{issn_katalog}
  #v(2pt)
  #text(weight: "bold")[Nomor Publikasi/Publication Number:] {no_pub}
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Ukuran Buku/Book Size:] 14,8 cm x 21,0 cm \\
  #v(2pt)
  #text(weight: "bold")[Jumlah Halaman/Number of Pages:] #total_frontmatter_pages+#total_arabic_pages Halaman/Pages
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyusun Naskah/Manuscript Drafter:] \\
  #text(weight: "bold")[{nama_instansi_singkat}] \\
  #text(style: "italic")[{nama_instansi_en}]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyunting/Editor:] \\
  #text(weight: "bold")[{nama_instansi_singkat}] \\
  #text(style: "italic")[{nama_instansi_en}]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Pembuat Kover/Cover Designer:] \\
  #text(weight: "bold")[{nama_instansi_singkat}] \\
  #text(style: "italic")[{nama_instansi_en}]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Sumber Ilustrasi/Illustration Source:] \\
  {nama_instansi_singkat}
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penerbit/Publisher:] \\
  #text(weight: "bold")[© {nama_instansi}/]#text(style: "italic")[{nama_instansi_en}]
]

#v(1fr)

#text(6.8pt)[
  #text(weight: "bold")[Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik] \\
  #v(2pt)
  #text(style: "italic")[It is prohibited to reproduce and/or duplicate part or all of this book for commercial purpose without permission from BPS-Statistics Indonesia]
]

#pagebreak()

// ==========================================
// 4. TIM PENYUSUN / COMPILERS (HALAMAN iii)
// ==========================================
{issn_tim}#v(0.6cm)

#align(center)[
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \\
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka {tahun_rilis}] \\
  #text(8pt, style: "italic")[{nama_en} District in Figures {tahun_rilis}] \\
  #text(7.5pt)[{volume}]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/_Director_] \\
  #text(8pt)[{nama_kepala}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \\
  #text(8pt)[{nama_kepala}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \\
  #text(8pt)[Tim Kerja IPDS / Tim Publikasi]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \\
  #text(8pt)[{pic_polos}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \\
  #text(8pt)[KCDA Agent]
]

#pagebreak()

// ==========================================
// 5. KONTRIBUTOR DATA / DATA CONTRIBUTORS (HALAMAN iv)
// ==========================================
#v(0.6cm)
#align(center)[
  #text(10.5pt, weight: "bold")[KONTRIBUTOR DATA/_DATA CONTRIBUTORS_] \\
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka {tahun_rilis}] \\
  #text(8pt, style: "italic")[{nama_en} District in Figures {tahun_rilis}] \\
  #text(7.5pt)[{volume}]
]
#v(16pt)

#align(center)[
  #block(width: 82%)[
    #set align(left)
    #set text(8pt)
    1. Kantor Camat {nama_singkat}
    #v(3pt)
    2. Kantor Desa/Kelurahan se-Kecamatan {nama_singkat}
    #v(3pt)
    3. Korwil Bidang Pendidikan Kecamatan {nama_singkat}
    #v(3pt)
    4. Puskesmas se-Kecamatan {nama_singkat}
    #v(3pt)
    5. Kantor Urusan Agama (KUA) Kecamatan {nama_singkat}
    #v(3pt)
    6. Balai Penyuluhan Pertanian (BPP) Kecamatan {nama_singkat}
    #v(3pt)
    7. Dinas dan Instansi Terkait Pemerintah Daerah
  ]
]
"""
