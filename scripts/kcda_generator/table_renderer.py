"""Table renderer helper for KCDA 2026 Typst documents following BPS standards (A5 Paper)."""

import re
from typing import List, Optional
from .config import get_regency_info

def format_bilingual_header(header_text: str) -> str:
    """
    Memformat teks header tabel dwibahasa sesuai Pedoman BPS:
    1. Jika ada baris kedua: dicetak miring (italic).
    2. Jika satu baris dan dipisahkan '/': garis miring tanpa spasi dan kata bahasa asing dicetak miring.
    Menggunakan #strong agar aman dari tabrakan operator block comment Typst ('*/').
    """
    if "\n" in header_text:
        parts = header_text.split("\n", 1)
        id_part = parts[0].strip()
        en_part = parts[1].strip().strip("_")
        return f"[#strong[{id_part}] \\ #text(6pt, weight: \"bold\", style: \"italic\")[{en_part}]]"
    elif " / " in header_text and not any(k in header_text for k in ["SD", "SMP", "SMA", "SMK", "PT"]):
        parts = header_text.split(" / ", 1)
        id_part = parts[0].strip()
        en_part = parts[1].strip().strip("_")
        return f"[#strong[{id_part}]/#text(weight: \"bold\", style: \"italic\")[{en_part}]]"
    else:
        return f"[#strong[{header_text.strip()}]]"

def format_bilingual_stub(cell_val: str) -> str:
    """
    Memformat stub/nilai sel dwibahasa sesuai Pedoman BPS:
    Jika memuat pasangan dwibahasa (contoh 'Bawang Merah / Shallots', 'Jumlah / Total', 'Banjir / Flood'):
    Ubah menjadi format baku 'Bawang Merah/_Shallots_' (slash tanpa spasi, istilah asing miring).
    Jika alternatif bahasa Indonesia ('Kelompok Pertokoan / Ruko', 'Angin Puyuh / Puting Beliung'),
    satukan dengan slash rapi 'Kelompok Pertokoan/Ruko'.
    """
    bilingual_indicators = {
        "shallots", "chili", "pepper", "tomato", "eggplant", "beans", "cucumber", 
        "spinach", "ginger", "galangal", "turmeric", "durian", "mango", "orange", 
        "banana", "papaya", "pineapple", "rambutan", "total", "male", "female",
        "public", "private", "hospital", "phc", "clinic", "pharmacy", "landslide",
        "flood", "earthquake", "tidal", "wave", "disaster", "drought", "fire",
        "tsunami", "outpatient", "inpatient", "unit", "post", "courier", "facility",
        "head", "director", "in charge", "compilers", "editors", "writers", "layouters"
    }
    if " / " in cell_val:
        parts = cell_val.split(" / ", 1)
        id_t = parts[0].strip()
        en_t = parts[1].strip().strip("_")
        # Tokenize kata pada bagian kedua
        words = set(re.findall(r'[a-zA-Z]+', en_t.lower()))
        if words.intersection(bilingual_indicators):
            return f"{id_t}/_{en_t}_"
        else:
            return f"{id_t}/{en_t}"
    return cell_val

SOURCE_TRANSLATIONS = {
    "BPS Kabupaten Mempawah": "BPS-Statistics of Mempawah Regency",
    "BPS, Pendataan Potensi Desa (Podes) 2025": "BPS-Statistics Indonesia, Village Potential Census (Podes) 2025",
    "BPS, Pendataan Potensi Desa (Podes)": "BPS-Statistics Indonesia, Village Potential Census (Podes)",
    "Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi": "Ministry of Villages, Disadvantaged Regions Development, and Transmigration",
    "Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama": "Ministry of Education, Culture, Research, and Technology & Ministry of Religious Affairs",
    "Dinas Kependudukan dan Pencatatan Sipil / BAPEDDA Kabupaten Mempawah": "Population and Civil Registration Service/Regional Development Planning Agency of Mempawah Regency",
    "Dinas Kependudukan dan Pencatatan Sipil/BAPEDDA Kabupaten Mempawah": "Population and Civil Registration Service/Regional Development Planning Agency of Mempawah Regency",
    "Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)": "Population and Civil Registration Service of Mempawah Regency (Semester II 2025)",
    "Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah / Podes 2025": "Health, Population Control, and Family Planning Service of Mempawah Regency/Podes 2025",
    "Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah/Podes 2025": "Health, Population Control, and Family Planning Service of Mempawah Regency/Podes 2025",
    "Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah / Podes 2025": "Regional Disaster Management Agency (BPBD) of Mempawah Regency/Podes 2025",
    "Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah/Podes 2025": "Regional Disaster Management Agency (BPBD) of Mempawah Regency/Podes 2025",
    "Dinas Perindagnaker Kab. Mempawah / Podes 2025": "Industry, Trade, and Manpower Service of Mempawah Regency/Podes 2025",
    "Dinas Perindagnaker Kab. Mempawah/Podes 2025": "Industry, Trade, and Manpower Service of Mempawah Regency/Podes 2025",
    "Otoritas Jasa Keuangan (OJK) / Podes 2025": "Financial Services Authority (OJK)/Podes 2025",
    "Otoritas Jasa Keuangan (OJK)/Podes 2025": "Financial Services Authority (OJK)/Podes 2025",
    "BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)": "BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-SBS)",
    "BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)": "BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TBF)",
    "BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)": "BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)",
    "Dinas Pertanian, Ketahanan Pangan dan Perikanan Kabupaten Mempawah": "Agriculture, Food Security, and Fisheries Service of Mempawah Regency",
    "Bagian Tata Pemerintahan Setda Mempawah": "Regional Secretariat Governance Division of Mempawah Regency",
    "Bagian Tata Pemerintahan Setda Kabupaten Mempawah": "Regional Secretariat Governance Division of Mempawah Regency",
}

EN_SOURCE_KEYWORDS = {
    "office", "service", "services", "ministry", "agency", "agencies", "district", "regency",
    "census", "survey", "authority", "center", "centre", "board", "bureau", "department",
    "division", "potential", "planning", "population", "statistics", "agriculture", "agricultural",
    "disaster", "education", "health", "trade", "manpower", "industry"
}

def format_bilingual_source(s: str) -> str:
    """
    Memformat nama instansi sumber dwibahasa sesuai Pedoman BPS:
    Format: [Instansi ID]/_[Instansi EN]_
    Dicetak: [Instansi ID]/#text(style: "italic")[Instansi EN]
    """
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_en = regency.get("nama_en", "Mempawah Regency")
    nama_bps = regency.get("nama_instansi_bps", f"BPS {nama_kab}")
    nama_bps_en = regency.get("nama_instansi_bps_en", f"BPS-Statistics of {nama_en}")

    s = s.strip()
    if not s:
        return f'{nama_bps}/#text(style: "italic")[{nama_bps_en}]'

    # 1. Cek apakah sudah dwibahasa eksplisit dengan '/'
    if "/" in s:
        parts = s.rsplit("/", 1)
        right_words = set(re.findall(r"[a-zA-Z]+", parts[1].lower()))
        if right_words.intersection(EN_SOURCE_KEYWORDS):
            id_txt = parts[0].strip()
            en_txt = parts[1].strip().strip("_")
            return f'{id_txt}/#text(style: "italic")[{en_txt}]'

    # 2. Cek kamus persis
    s_clean = s.replace("  ", " ")
    if s_clean in SOURCE_TRANSLATIONS:
        en = SOURCE_TRANSLATIONS[s_clean]
        clean_id = s_clean.replace(" / ", "/")
        return f'{clean_id}/#text(style: "italic")[{en}]'

    s_slash_clean = s.replace(" / ", "/")
    if s_slash_clean in SOURCE_TRANSLATIONS:
        en = SOURCE_TRANSLATIONS[s_slash_clean]
        return f'{s_slash_clean}/#text(style: "italic")[{en}]'

    # 3. Pola Kantor Camat
    m_camat = re.match(r"^Kantor Camat\s+(.+)$", s, re.IGNORECASE)
    if m_camat:
        kec = m_camat.group(1).strip()
        if " / " in kec or "/" in kec:
            parts = [p.strip() for p in re.split(r"\s*/\s*", kec)]
            id_txt = f"Kantor Camat {parts[0]}/{parts[1]}"
            en_sub = f"Regional Secretariat Governance Division of {nama_en}" if "tata pemerintahan" in parts[1].lower() else parts[1]
            en_txt = f"{parts[0]} District Office/{en_sub}"
            return f'{id_txt}/#text(style: "italic")[{en_txt}]'
        return f'Kantor Camat {kec}/#text(style: "italic")[{kec} District Office]'

    # 4. Pola Balai Penyuluhan Pertanian
    m_bpp = re.match(r"^Balai Penyuluhan Pertanian Kecamatan\s+(.+)$", s, re.IGNORECASE)
    if m_bpp:
        kec = m_bpp.group(1).strip()
        return f'Balai Penyuluhan Pertanian Kecamatan {kec}/#text(style: "italic")[Agricultural Extension Center of {kec} District]'

    # 5. Pola Dinas / Badan Kabupaten umum
    for kab_label in [nama_kab, "Kabupaten Mempawah"]:
        if kab_label in s and "/" not in s:
            clean_name = s.replace(kab_label, "").strip()
            return f'{s}/#text(style: "italic")[{clean_name} of {nama_en}]'

    return f'{s}/#text(style: "italic")[{s}]'

def render_typst_table(
    table_no: str,
    title_id: str,
    title_en: str,
    headers: List[str],
    col_numbers: List[str],
    rows: List[List[str]],
    col_widths: Optional[List[str]] = None,
    source: Optional[str] = None,
    note: Optional[str] = None
) -> str:
    """Merender tabel berstandar BPS untuk buku ukuran A5 dengan format judul dua kolom dan penegakan kaidah dwibahasa."""
    if source is None:
        reg = get_regency_info()
        source = reg.get("nama_instansi_bps", "BPS")
    num_cols = len(headers)
    if col_widths and len(col_widths) == num_cols:
        col_spec = "(" + ", ".join(col_widths) + ")"
    else:
        widths = ["2.2fr"] + ["1.0fr"] * (num_cols - 1)
        col_spec = "(" + ", ".join(widths) + ")"

    header_cells = ", ".join([format_bilingual_header(h) for h in headers])
    col_num_cells = ", ".join([f"[#strong[{cn}]]" for cn in col_numbers])

    rendered_rows = []
    for r in rows:
        cells = []
        for c in r:
            formatted_c = format_bilingual_stub(str(c))
            cells.append(f"[{formatted_c}]")
        rendered_rows.append(", ".join(cells))

    rows_str = ",\n  ".join(rendered_rows)
    note_str = f"#v(-2pt)\n#text(6pt, fill: luma(60))[Catatan/#text(style: \"italic\")[Note] : {note}]\n" if note else ""
    formatted_source = format_bilingual_source(source)
    clean_no = table_no.replace(".", "_")

    markup = f"""
#metadata("tab_{clean_no}") <tab_{clean_no}>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \\
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[{table_no}]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[{title_id}] \\
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[{title_en}]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: {col_spec},
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 {{ cmyk(0%, 20%, 90%, 0%) }}
                      else if row == 1 {{ cmyk(0%, 10%, 45%, 0%) }}
                      else if calc.even(row) {{ rgb("#FFF8E7") }}
                      else {{ rgb("#FFF4D4") }},
  align: (col, row) => if row <= 1 {{ center + horizon }}
                       else if col == 0 {{ left + horizon }}
                       else {{ right + horizon }},
  table.header({header_cells}, {col_num_cells}),
  {rows_str}
)
{note_str}#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {formatted_source}]
#v(8pt)
"""
    return markup
