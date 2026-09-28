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

def _clean_and_split_items(text: str):
    if not text:
        return []
    t = text.replace('\r\n', '\n').strip()
    raw_lines = [l.strip().lstrip(':').strip() for l in t.split('\n') if l.strip()]
    has_numbered = any(re.match(r'^\d', l) for l in raw_lines)
    if has_numbered:
        items = []
        current = ''
        for l in raw_lines:
            if re.match(r'^\d', l):
                if current:
                    items.append(current)
                current = l
            else:
                if current:
                    current += ' ' + l
                else:
                    current = l
        if current:
            items.append(current)
        return items
    else:
        return [' '.join(raw_lines)]

def format_bilingual_note_item(item: str) -> str:
    item = item.strip().lstrip(':').strip()
    if not item:
        return ''
    m_fn = re.match(r'^(\d+[\.\s]*)(.*)$', item)
    prefix = ''
    rest = item
    if m_fn and len(m_fn.group(1).strip()) <= 2:
        fn_num = m_fn.group(1).strip().rstrip('.')
        prefix = f'#super[{fn_num}] '
        rest = m_fn.group(2).strip()

    if '/' in rest:
        if ' / ' in rest:
            p_id, p_en = rest.split(' / ', 1)
        else:
            p_id, p_en = rest.split('/', 1)
        return f'{prefix}{p_id.strip()}/#text(style: "italic")[{p_en.strip()}]'
    return f'{prefix}{rest}'

def format_bilingual_note(n: Optional[str]) -> str:
    """Memformat catatan tabel dwibahasa sesuai Pedoman BPS 2023."""
    if not n:
        return ''
    items = _clean_and_split_items(n)
    return ' \\ \n'.join([format_bilingual_note_item(it) for it in items if it.strip()])

def _format_single_source_item(s: str) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_en = regency.get("nama_en", "Mempawah Regency")
    nama_bps = regency.get("nama_instansi_bps", f"BPS {nama_kab}")
    nama_bps_en = regency.get("nama_instansi_bps_en", f"BPS-Statistics of {nama_en}")

    s = s.strip()
    if not s:
        return f'{nama_bps}/#text(style: "italic")[{nama_bps_en}]'

    m_fn = re.match(r'^(\d+[\.\s]*)(.*)$', s)
    prefix = ''
    rest = s
    if m_fn and len(m_fn.group(1).strip()) <= 2 and not s.startswith('19') and not s.startswith('20'):
        fn_num = m_fn.group(1).strip().rstrip('.')
        prefix = f'#super[{fn_num}] '
        rest = m_fn.group(2).strip()

    # 1. Cek apakah sudah dwibahasa eksplisit dengan '/'
    if "/" in rest:
        if " / " in rest:
            parts = rest.split(" / ", 1)
        else:
            parts = rest.rsplit("/", 1)
        right_words = set(re.findall(r"[a-zA-Z]+", parts[1].lower()))
        if right_words.intersection(EN_SOURCE_KEYWORDS) or len(parts[1].split()) >= 2:
            id_txt = parts[0].strip()
            en_txt = parts[1].strip().strip("_")
            return f'{prefix}{id_txt}/#text(style: "italic")[{en_txt}]'

    # 2. Cek kamus persis
    s_clean = rest.replace("  ", " ")
    if s_clean in SOURCE_TRANSLATIONS:
        en = SOURCE_TRANSLATIONS[s_clean]
        clean_id = s_clean.replace(" / ", "/")
        return f'{prefix}{clean_id}/#text(style: "italic")[{en}]'

    s_slash_clean = rest.replace(" / ", "/")
    if s_slash_clean in SOURCE_TRANSLATIONS:
        en = SOURCE_TRANSLATIONS[s_slash_clean]
        return f'{prefix}{s_slash_clean}/#text(style: "italic")[{en}]'

    # 3. Pola Kantor Camat
    m_camat = re.match(r"^Kantor Camat\s+(.+)$", rest, re.IGNORECASE)
    if m_camat:
        kec = m_camat.group(1).strip()
        if " / " in kec or "/" in kec:
            parts = [p.strip() for p in re.split(r"\s*/\s*", kec)]
            id_txt = f"Kantor Camat {parts[0]}/{parts[1]}"
            en_sub = f"Regional Secretariat Governance Division of {nama_en}" if "tata pemerintahan" in parts[1].lower() else parts[1]
            en_txt = f"{parts[0]} District Office/{en_sub}"
            return f'{prefix}{id_txt}/#text(style: "italic")[{en_txt}]'
        return f'{prefix}Kantor Camat {kec}/#text(style: "italic")[{kec} District Office]'

    # 4. Pola Balai Penyuluhan Pertanian
    m_bpp = re.match(r"^Balai Penyuluhan Pertanian Kecamatan\s+(.+)$", rest, re.IGNORECASE)
    if m_bpp:
        kec = m_bpp.group(1).strip()
        return f'{prefix}Balai Penyuluhan Pertanian Kecamatan {kec}/#text(style: "italic")[Agricultural Extension Center of {kec} District]'

    # 5. Pola Dinas / Badan Kabupaten umum
    for kab_label in [nama_kab, "Kabupaten Mempawah"]:
        if kab_label in rest and "/" not in rest:
            clean_name = rest.replace(kab_label, "").strip()
            return f'{prefix}{rest}/#text(style: "italic")[{clean_name} of {nama_en}]'

    return f'{prefix}{rest}/#text(style: "italic")[{rest}]'

def format_bilingual_source(s: str) -> str:
    """
    Memformat nama instansi sumber dwibahasa sesuai Pedoman BPS:
    Format: [Instansi ID]/_[Instansi EN]_
    Dicetak: [Instansi ID]/#text(style: "italic")[Instansi EN]
    """
    if not s:
        return ''
    items = _clean_and_split_items(s)
    return ' \\ \n'.join([_format_single_source_item(it) for it in items if it.strip()])

def format_cell_value(val: str, table_no: str = "", col_idx: int = 0) -> str:
    s = str(val).strip()
    if s in ["0", "0.0", "0,0", "0,00", "0.00"]:
        return "–"
    clean_tno = table_no.rstrip(".")
    if clean_tno.startswith("5.") and s in ["...", "…", "-", "—", ""]:
        return "–"
    if re.match(r"^\d{4,}$", s):
        try:
            n = int(s)
            if not (1900 <= n <= 2099):
                s = f"{n:,}".replace(",", ".")
        except ValueError:
            pass
    return format_bilingual_stub(s)

def get_cell_alignment(val: str, col_idx: int, header_text: str = "") -> str:
    if col_idx == 0:
        if header_text.strip().lower() in ["no", "no."]:
            return "center + horizon"
        return "left + horizon"
    clean = re.sub(r'#super\[\d+\]', '', val)
    has_letters = any(c.isalpha() for c in clean)
    if has_letters and not re.match(r'^(–|\-|\.\.\.|…|NA|x|xx|e|r)$', clean.strip()):
        return "left + horizon"
    return "right + horizon"

def render_typst_table(
    table_no: str,
    title_id: str,
    title_en: str,
    headers: List[str],
    col_numbers: List[str],
    rows: List[List[str]],
    col_widths: Optional[List[str]] = None,
    source: Optional[str] = None,
    note: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """Merender tabel berstandar BPS untuk buku ukuran A5 dengan format judul dua kolom dan penegakan kaidah dwibahasa."""
    if note is None and notes is not None:
        note = notes
    if source is None or note is None:
        try:
            from .config import get_tables_schema
            schema = get_tables_schema()
            clean_tno = table_no.rstrip('.')
            for item in schema:
                if item.get("no", "").rstrip(".") == clean_tno:
                    if source is None and item.get("sumber"):
                        source = item.get("sumber")
                    if note is None and item.get("catatan"):
                        note = item.get("catatan")
                    break
        except Exception:
            pass

    if source is None:
        reg = get_regency_info()
        source = reg.get("nama_instansi_bps", "BPS")

    num_cols = len(headers)
    if col_widths and len(col_widths) == num_cols:
        col_spec = "(" + ", ".join(col_widths) + ")"
    else:
        widths = ["2.2fr"] + ["1.0fr"] * (num_cols - 1)
        col_spec = "(" + ", ".join(widths) + ")"

    header_cells = ", ".join([f"table.cell(align: center + horizon)[{format_bilingual_header(h)}]" for h in headers])
    col_num_cells = ", ".join([f"table.cell(align: center + horizon)[#strong[{cn}]]" for cn in col_numbers])

    rendered_rows = []
    for r in rows:
        cells = []
        for col_idx, c in enumerate(r):
            h_text = headers[col_idx] if col_idx < len(headers) else ""
            formatted_c = format_cell_value(str(c), table_no=table_no, col_idx=col_idx)
            cell_align = get_cell_alignment(formatted_c, col_idx=col_idx, header_text=h_text)
            cells.append(f"table.cell(align: {cell_align})[{formatted_c}]")
        rendered_rows.append(", ".join(cells))

    rows_str = ",\n  ".join(rendered_rows)
    formatted_note = format_bilingual_note(note)
    note_str = f"""#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[{formatted_note}]]
)
""" if formatted_note else ""

    formatted_source = format_bilingual_source(source)
    clean_no = re.sub(r'[^a-zA-Z0-9_\-]', '_', table_no)

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
          #text(10pt, weight: "bold")[Tabel]
        ] \\
        #v(-3.5pt)
        #text(8pt, style: "italic")[Tables]
      ],
      [
        #text(10pt, weight: "bold")[{table_no}]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[{title_id}] \\
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[{title_en}]
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
  table.header({header_cells}, {col_num_cells}),
  {rows_str}
)
{note_str}#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[{formatted_source}]]
)
#v(8pt)
"""
    return markup
