"""Chapter 3: Kependudukan Generator for KCDA."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter3_charts
from ..config import get_regency_info

def render_chapter3(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten")
    nama_kab_en = regency.get("nama_en", "Regency")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", ""))
    desa_list = cfg["desa_list"]
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter3_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else "\n#v(8pt)\n"

    # --- 3.1 Penduduk ---
    rows_31_raw = get_kecamatan_tab_rows("3.1", nama_singkat)
    t31_map = {}
    for r in rows_31_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['desa', 'jumlah', 'sumber', 'catatan', 'tabel']):
            desa_name = clean_cell_value(r[0])
            lk = clean_cell_value(r[1])
            pr = clean_cell_value(r[2])
            tot = clean_cell_value(r[3])
            pct = clean_cell_value(r[4] if len(r) > 4 else "...")
            kpd = clean_cell_value(r[5] if len(r) > 5 else "...")
            t31_map[desa_name.lower()] = [desa_name, lk, pr, tot, pct, kpd]

    t31_rows = []
    for d in desa_list:
        v = t31_map.get(d.lower(), [d, "...", "...", "...", "...", "..."])
        t31_rows.append(v)

    t31_markup = render_typst_table(
        table_no="3.1",
        title_id=f"Penduduk, Distribusi Persentase Penduduk, dan Kepadatan Penduduk Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Population, Percentage Distribution of Population, and Population Density by Village/Subdistrict in {nama_en}, 2025",
        headers=[
            "Desa/Kelurahan\nVillage/Subdistrict",
            "Laki-laki\nMale",
            "Perempuan\nFemale",
            "Jumlah\nTotal",
            "Persentase\nPercentage (%)",
            "Kepadatan\nDensity (jiwa/km²)"
        ],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"],
        rows=t31_rows,
        col_widths=["2.0fr", "1.0fr", "1.0fr", "1.1fr", "1.0fr", "1.2fr"],
        source=f"Dinas Kependudukan dan Pencatatan Sipil {nama_kab} (Semester II 2025) / Population and Civil Registration Service of {nama_kab_en} (Semester II 2025)"
    )

    # Infografis Halaman Bab 3
    infografis_markup = f"\n{charts_markup}\n" if charts_markup.strip() else """
#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS KEPENDUDUKAN]\
      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan """ + nama_singkat + """]
    ]
  ]
]
"""

    return f"""
// ==========================================
// BAB 3: KEPENDUDUKAN (INFOGRAFIS & NARASI)
// ==========================================
{chart_section}
// ==========================================
// ISI BAB 3: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Berdasarkan data kependudukan registrasi semester II tahun 2025 dari Dinas Kependudukan dan Pencatatan Sipil {nama_kab}, jumlah penduduk Kecamatan {nama_singkat} terdistribusi di {len(desa_list)} desa/kelurahan dengan struktur demografi yang produktif. Komposisi penduduk laki-laki dan perempuan relatif berimbang, mencerminkan kestabilan demografis wilayah.
]
#v(12pt)

{t31_markup}
"""
