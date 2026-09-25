"""
Core Vector SVG Engine for KCDA 2026 Typst Engine.
Menyediakan fungsi dasar parsing angka, format angka Indonesia, header gambar dwibahasa BPS,
serta generator grafik horizontal dan grouped bar chart berbasis SVG.
"""

from typing import List, Dict, Any, Optional

def parse_number(val: Any) -> Optional[float]:
    """Mengekstrak angka float dari string cell Google Sheets/tabel lokal."""
    if val is None:
        return None
    s = str(val).strip()
    if s in ["", "-", "...", "–", "null", "None"]:
        return None
    s_clean = s.replace(".", "").replace(",", ".").replace("%", "").strip()
    try:
        return float(s_clean)
    except ValueError:
        return None

def format_id_number(val: float, is_decimal: bool = False) -> str:
    """Format angka sesuai standar Indonesia (koma untuk desimal, titik untuk ribuan)."""
    if is_decimal or (val % 1 != 0):
        formatted = f"{val:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        formatted = f"{int(round(val)):,}"
        return formatted.replace(",", ".")

def format_figure_header(fig_no: str, title_id: str, title_en: str) -> str:
    """
    Menghasilkan blok penamaan Gambar dwibahasa 2-kolom berstandar resmi BPS:
    Gambar
    ────── [No]  [Judul ID (Bold)]
    Figures      [Judul EN (Bold Italic)]
    """
    clean_fig = fig_no.replace(".", "_")
    return f"""#metadata("fig_{clean_fig}") <fig_{clean_fig}>
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
          #text(7.5pt, weight: "bold")[Gambar]
        ] \\
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[{fig_no}]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[{title_id}] \\
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[{title_en}]
  ]
)"""

def generate_horizontal_bar_chart(
    labels: List[str],
    values: List[float],
    unit: str = "",
    color: str = "#0284C7",
    width: int = 340,
    sort_descending: bool = True
) -> str:
    """
    Menghasilkan SVG Horizontal Bar Chart modern beresolusi tajam.
    Secara default diurutkan (sort_descending=True) dari nilai tertinggi ke terendah.
    """
    n = len(labels)
    if n == 0:
        return ""

    if sort_descending and len(values) == n:
        pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]

    max_val = max(values) if values else 1
    if max_val == 0:
        max_val = 1
    ceil_val = max_val * 1.15

    left_margin = 100
    right_margin = 45
    top_margin = 18
    bottom_margin = 18
    row_height = 19
    height = top_margin + bottom_margin + n * row_height
    plot_width = width - left_margin - right_margin

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}pt" style="font-family: \'Liberation Sans\', Arial, sans-serif;">',
        f'<rect width="{width}" height="{height}" fill="#FAFAFA" rx="4"/>'
    ]

    # Grid lines & ticks
    num_ticks = 4
    for i in range(num_ticks + 1):
        x = left_margin + (i / num_ticks) * plot_width
        val_tick = (i / num_ticks) * ceil_val
        val_str = f"{int(val_tick):,}".replace(",", ".")
        svg.append(f'<line x1="{x}" y1="{top_margin}" x2="{x}" y2="{height - bottom_margin}" stroke="#F1F5F9" stroke-width="0.8" stroke-dasharray="2,2"/>')
        svg.append(f'<text x="{x}" y="{height - 5}" font-size="5.5" fill="#94A3B8" text-anchor="middle">{val_str}</text>')

    svg.append(f'<line x1="{left_margin}" y1="{top_margin}" x2="{left_margin}" y2="{height - bottom_margin}" stroke="#CBD5E1" stroke-width="1"/>')

    # Bars & Labels
    bar_height = 11
    for i, (label, val) in enumerate(zip(labels, values)):
        y = top_margin + i * row_height + 4
        bar_w = (val / ceil_val) * plot_width if ceil_val > 0 else 0
        val_display = format_id_number(val, is_decimal=(unit in ["%", "km²", "ha"]))
        unit_str = f" {unit}" if unit else ""

        # Label desa di kiri sumbu
        svg.append(f'<text x="{left_margin - 6}" y="{y + bar_height - 2.5}" font-size="6.5" fill="#334155" text-anchor="end">{label}</text>')
        # Bar SVG
        svg.append(f'<rect x="{left_margin}" y="{y}" width="{bar_w}" height="{bar_height}" rx="2" fill="{color}"/>')
        # Angka nilai di kanan bar
        svg.append(f'<text x="{left_margin + bar_w + 4}" y="{y + bar_height - 2.5}" font-size="6" font-weight="bold" fill="#1E293B">{val_display}{unit_str}</text>')

    svg.append("</svg>")
    return "\n".join(svg)

def generate_grouped_horizontal_bar_chart(
    labels: List[str],
    series_data: List[Dict[str, Any]],
    width: int = 340,
    sort_descending: bool = True
) -> str:
    """
    Menghasilkan SVG Grouped Horizontal Bar Chart (misal: Laki-laki vs Perempuan).
    series_data: [{'name': 'Laki-laki / Male', 'color': '#0284C7', 'values': [...]}, ...]
    """
    n = len(labels)
    if n == 0:
        return ""

    if sort_descending:
        totals = [sum(s["values"][i] for s in series_data) for i in range(n)]
        sorted_indices = sorted(range(n), key=lambda idx: totals[idx], reverse=True)
        labels = [labels[i] for i in sorted_indices]
        for s in series_data:
            s["values"] = [s["values"][i] for i in sorted_indices]

    all_vals = [v for s in series_data for v in s["values"]]
    max_val = max(all_vals) if all_vals else 1
    ceil_val = max_val * 1.18

    left_margin = 95
    right_margin = 40
    top_margin = 24
    bottom_margin = 16
    num_series = len(series_data)
    bar_h = 7
    row_height = num_series * bar_h + 8
    height = top_margin + bottom_margin + n * row_height
    plot_width = width - left_margin - right_margin

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}pt" style="font-family: \'Liberation Sans\', Arial, sans-serif;">',
        f'<rect width="{width}" height="{height}" fill="#FAFAFA" rx="4"/>'
    ]

    # Legend at top
    leg_x = left_margin
    for s in series_data:
        raw_name = s["name"]
        if "/" in raw_name:
            p = raw_name.split("/", 1)
            legend_html = f'{p[0].strip()}/<tspan font-style="italic">{p[1].strip()}</tspan>'
        else:
            legend_html = raw_name

        svg.append(f'<rect x="{leg_x}" y="8" width="11" height="7" rx="2" fill="{s["color"]}"/>')
        svg.append(f'<text x="{leg_x + 15}" y="14" font-size="6" font-weight="bold" fill="#334155">{legend_html}</text>')
        leg_x += len(raw_name) * 4.4 + 25

    # Grid lines
    num_ticks = 4
    for i in range(num_ticks + 1):
        x = left_margin + (i / num_ticks) * plot_width
        val_tick = (i / num_ticks) * ceil_val
        val_str = f"{int(val_tick):,}".replace(",", ".")
        svg.append(f'<line x1="{x}" y1="{top_margin}" x2="{x}" y2="{height - bottom_margin}" stroke="#F1F5F9" stroke-width="0.8" stroke-dasharray="2,2"/>')
        svg.append(f'<text x="{x}" y="{height - 4}" font-size="5.5" fill="#94A3B8" text-anchor="middle">{val_str}</text>')

    svg.append(f'<line x1="{left_margin}" y1="{top_margin}" x2="{left_margin}" y2="{height - bottom_margin}" stroke="#CBD5E1" stroke-width="1"/>')

    for i, label in enumerate(labels):
        group_top = top_margin + i * row_height + 3
        label_y = group_top + (num_series * bar_h) / 2 + 1.5
        svg.append(f'<text x="{left_margin - 6}" y="{label_y}" font-size="6.5" fill="#334155" text-anchor="end">{label}</text>')

        for s_idx, s in enumerate(series_data):
            y = group_top + s_idx * bar_h
            val = s["values"][i]
            bar_w = (val / ceil_val) * plot_width if ceil_val > 0 else 0
            val_display = format_id_number(val, is_decimal=False)
            svg.append(f'<rect x="{left_margin}" y="{y}" width="{bar_w}" height="{bar_h - 1.5}" rx="1.5" fill="{s["color"]}"/>')
            svg.append(f'<text x="{left_margin + bar_w + 3}" y="{y + bar_h - 2.5}" font-size="5.5" fill="#475569">{val_display}</text>')

    svg.append("</svg>")
    return "\n".join(svg)
