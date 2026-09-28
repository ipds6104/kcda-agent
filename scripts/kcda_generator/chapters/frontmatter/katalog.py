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

TIM_PENYUSUN_MAP = {
    "mempawah-hilir": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Sukma Andini",
        "pengolah_penulis": "Ihza Fikri Zaki Karunia",
        "penata_letak": "Akma Batrisyia Jazima",
        "penerjemah": "Ihza Fikri Zaki Karunia"
    },
    "mempawah-timur": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Ihza Fikri Zaki Karunia",
        "pengolah_penulis": "Akma Batrisyia Jazima",
        "penata_letak": "Sukma Andini",
        "penerjemah": "Akma Batrisyia Jazima"
    },
    "sungai-pinyuh": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Akma Batrisyia Jazima",
        "pengolah_penulis": "Sukma Andini",
        "penata_letak": "Ihza Fikri Zaki Karunia",
        "penerjemah": "Sukma Andini"
    },
    "anjongan": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Akma Batrisyia Jazima",
        "pengolah_penulis": "Ihza Fikri Zaki Karunia",
        "penata_letak": "Sukma Andini",
        "penerjemah": "Ihza Fikri Zaki Karunia"
    },
    "toho": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Ihza Fikri Zaki Karunia",
        "pengolah_penulis": "Sukma Andini",
        "penata_letak": "Akma Batrisyia Jazima",
        "penerjemah": "Sukma Andini"
    },
    "segedong": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Sukma Andini",
        "pengolah_penulis": "Akma Batrisyia Jazima",
        "penata_letak": "Ihza Fikri Zaki Karunia",
        "penerjemah": "Akma Batrisyia Jazima"
    },
    "sungai-kunyit": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Sukma Andini",
        "pengolah_penulis": "Ihza Fikri Zaki Karunia",
        "penata_letak": "Akma Batrisyia Jazima",
        "penerjemah": "Ihza Fikri Zaki Karunia"
    },
    "jongkat": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Ihza Fikri Zaki Karunia",
        "pengolah_penulis": "Akma Batrisyia Jazima",
        "penata_letak": "Sukma Andini",
        "penerjemah": "Akma Batrisyia Jazima"
    },
    "sadaniang": {
        "pengarah": "Munawir",
        "penanggung_jawab": "Munawir",
        "penyunting": "Akma Batrisyia Jazima",
        "pengolah_penulis": "Sukma Andini",
        "penata_letak": "Ihza Fikri Zaki Karunia",
        "penerjemah": "Sukma Andini"
    }
}

def render_katalog_and_contributors(cfg: Dict[str, Any]) -> str:
    regency = get_regency_info()
    instansi = get_instansi_info()
    pimpinan = get_pimpinan_info()
    pub = get_publikasi_info()

    slug = cfg.get("slug", "")
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_pub = cfg.get("no_publikasi", "-")
    no_katalog = cfg.get("no_katalog", "-")
    pic_full = cfg.get("pic_nama", "Staf BPS")
    pic_polos = cfg.get("pic_nama_polos", pic_full.split(",")[0].strip() if "," in pic_full else pic_full)
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())

    tahun_rilis = pub.get("tahun_rilis", 2026)
    volume = cfg.get("volume", f"Volume 17, {tahun_rilis}")
    issn = cfg.get("issn", "")

    nama_instansi = instansi.get("nama_resmi", "Badan Pusat Statistik")
    nama_instansi_singkat = instansi.get("nama_singkat", "BPS")
    nama_instansi_en = instansi.get("nama_en", "BPS-Statistics")
    nama_kepala = pimpinan.get("nama_polos", "Kepala BPS")

    team = TIM_PENYUSUN_MAP.get(slug, {})
    pengarah = team.get("pengarah", nama_kepala)
    penanggung_jawab = team.get("penanggung_jawab", nama_kepala)
    penyunting = team.get("penyunting", "Sukma Andini")
    pengolah_penulis = team.get("pengolah_penulis", pic_polos)
    penata_letak = team.get("penata_letak", "Sukma Andini")
    penerjemah = team.get("penerjemah", pic_polos)

    issn_katalog = f" \\\n  #v(2pt)\n  #text(weight: \"bold\")[ISSN:] {issn}" if issn else ""
    issn_tim = f"#align(right)[\n  #text(8pt)[ISSN {issn}]\n]\n" if issn else ""

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
  #text(weight: "bold")[Katalog/Catalogue:] {no_katalog}{issn_katalog} \\
  #v(2pt)
  #text(weight: "bold")[Nomor Publikasi/Publication Number:] {no_pub}
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Ukuran Buku/Book Size:] 14,8 cm x 21,0 cm \\
  #v(2pt)
  #text(weight: "bold")[Jumlah Halaman/Number of Pages:] #total_frontmatter_pages \+ #total_arabic_pages Halaman/Pages
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
  Canva.com
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
  #text(8pt)[{pengarah}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \\
  #text(8pt)[{penanggung_jawab}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \\
  #text(8pt)[{penyunting}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \\
  #text(8pt)[{pengolah_penulis}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \\
  #text(8pt)[{penata_letak}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/_Translators_] \\
  #text(8pt)[{penerjemah}]
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
  #block(width: 88%)[
    #set align(left)
    #set text(8pt)
    1. Kementerian Agama/#text(style: "italic")[Ministry of Religious Affair]
    #v(4pt)
    2. Kementerian Pendidikan dan Kebudayaan/#text(style: "italic")[Ministry of Education and Culture]
    #v(4pt)
    3. Badan Pusat Statistik/#text(style: "italic")[BPS–Statistics Indonesia]
    #v(4pt)
    4. Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]
    #v(4pt)
    5. Badan Perencanaan Pembangunan, Riset dan Inovasi Daerah Kabupaten Mempawah/#text(style: "italic")[Regional Development, Research and Innovation Agency of Mempawah Regency]
    #v(4pt)
    6. Kantor Kecamatan {nama_singkat}/#text(style: "italic")[{nama_singkat} District Office]
  ]
]
"""
