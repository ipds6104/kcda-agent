"""
Helper module for Chapter Preamble: Divider page, 2-column Ulasan, and 2-column Penjelasan Teknis.
Matches BPS official KCDA publication standard (gambar 1 & gambar 2).
"""

from typing import List, Tuple

def render_chapter_intro(
    chapter_num: int,
    title_id: str,
    title_en: str,
    ulasan_id: str,
    ulasan_en: str,
    technical_notes: List[Tuple[str, str]]
) -> str:
    """
    Renders:
    1. Chapter Divider full-bleed page (image Bab_{chapter_num}.jpg) with label <bab{chapter_num}>
    2. Ulasan / Description 2-column page (Even page)
    3. Penjelasan Teknis / Technical Notes 2-column page (Odd page)
    """
    id_notes_cells = []
    en_notes_cells = []
    for idx, (nid, nen) in enumerate(technical_notes, 1):
        id_notes_cells.append(f'[{idx}.], [{nid}]')
        en_notes_cells.append(f'[{idx}.], [{nen}]')

    id_notes_str = ",\n      ".join(id_notes_cells)
    en_notes_str = ",\n      ".join(en_notes_cells)

    init_counter = """
#in_frontmatter.update(false)
#counter(page).update(1)
""" if chapter_num == 1 else ""

    markup = f"""
// ----------------------------------------------------
// BAB {chapter_num}: {title_id} ({title_en})
// ----------------------------------------------------
#pagebreak()
{init_counter}#set page(margin: 0pt, header: none, footer: none)
#metadata("bab{chapter_num}") <bab{chapter_num}>
#image("/assets/dividers/Bab_{chapter_num}.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("{title_id}") <chapter_title>
#metadata("{title_en}") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      {id_notes_str}
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      {en_notes_str}
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    {ulasan_id}
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    {ulasan_en}
  ]
)

#pagebreak()
"""
    return markup
