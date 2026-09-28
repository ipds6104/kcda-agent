"""Chapter 5: Pertanian Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter5_charts
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter5(cfg: Dict[str, Any], out_dir: Optional[Any] = None, fig_no: int = 5) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten Mempawah")
    nama_kab_en = regency.get("nama_en", "Mempawah Regency")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter5_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None, fig_no=fig_no)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else ""

    # Ekstraksi komoditas pertanian unggulan 2025
    rows_52 = get_kecamatan_tab_rows("5.2", nama_singkat)
    items_52 = []
    if len(rows_52) > 2:
        for r in rows_52[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["sumber", "catatan", "jenis", "sayur"]):
                name = r[0].split("\n")[0].split("/")[0].strip()
                val_str = clean_cell_value(r[4] if len(r) > 4 else (r[3] if len(r) > 3 else "0"))
                try:
                    vf = float(val_str.replace(".", "").replace(",", "."))
                    if vf > 0:
                        items_52.append((name, vf, val_str))
                except Exception:
                    pass

    rows_54 = get_kecamatan_tab_rows("5.4", nama_singkat)
    items_54 = []
    if len(rows_54) > 2:
        for r in rows_54[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["sumber", "catatan", "jenis"]):
                name = r[0].split("\n")[0].split("/")[0].strip()
                val_str = clean_cell_value(r[4] if len(r) > 4 else (r[3] if len(r) > 3 else "0"))
                try:
                    vf = float(val_str.replace(".", "").replace(",", "."))
                    if vf > 0:
                        items_54.append((name, vf, val_str))
                except Exception:
                    pass

    rows_57 = get_kecamatan_tab_rows("5.7", nama_singkat)
    items_57 = []
    if len(rows_57) > 2:
        for r in rows_57[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["sumber", "catatan", "jenis", "buah", "sayur"]):
                name = r[0].split("\n")[0].split("/")[0].strip()
                val_str = clean_cell_value(r[4] if len(r) > 4 else (r[3] if len(r) > 3 else "0"))
                try:
                    vf = float(val_str.replace(".", "").replace(",", "."))
                    if vf > 0:
                        items_57.append((name, vf, val_str))
                except Exception:
                    pass

    top_sayur = max(items_52, key=lambda x: x[1]) if items_52 else ("Sayuran Semusim", 0, "–")
    top_bio = max(items_54, key=lambda x: x[1]) if items_54 else ("Jahe", 0, "–")
    top_buah = max(items_57, key=lambda x: x[1]) if items_57 else ("Buah Tahunan", 0, "–")

    if top_sayur[1] > 0 and top_bio[1] > 0 and top_buah[1] > 0:
        teks_horti_id = (
            f"Pada tahun 2025, produksi tanaman sayuran semusim terbesar di Kecamatan {nama_singkat} adalah {top_sayur[0]} yaitu sebesar {top_sayur[2]} kuintal. "
            f"Untuk produksi tanaman biofarmaka, {top_bio[0]} merupakan komoditas dengan produksi terbesar yaitu {top_bio[2]} kg. "
            f"Sementara itu, untuk produksi buah-buahan tahunan terbesar dicatat oleh komoditas {top_buah[0]} sebanyak {top_buah[2]} kuintal."
        )
        teks_horti_en = (
            f"In 2025, the largest seasonal vegetable crop production in {nama_en} District was {top_sayur[0]} at {top_sayur[2]} quintals. "
            f"For medicinal plants production, {top_bio[0]} was the leading commodity with {top_bio[2]} kg. "
            f"Meanwhile, the largest annual fruit production was recorded by {top_buah[0]} reaching {top_buah[2]} quintals."
        )
    else:
        teks_horti_id = (
            f"Sektor pertanian khususnya hortikultura tanaman pangan, sayuran, dan buah-buahan di Kecamatan {nama_singkat} "
            f"terus dibudidayakan guna memenuhi kebutuhan konsumsi masyarakat lokal dan pasokan komoditas ke daerah sekitar."
        )
        teks_horti_en = (
            f"The agricultural sector, particularly food crops, vegetables, and fruit horticulture in {nama_en} District, "
            f"continues to be cultivated to fulfill local consumption needs and supply commodities to surrounding areas."
        )

    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[Hortikultura] \\
  #v(2pt)
  {teks_horti_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[Horticulture] \\
  #v(2pt)
  {teks_horti_en}
]"""

    technical_notes_bab5 = [
        (
            """Tanaman sayuran dan buah-buahan semusim

a. Tanaman sayuran semusim adalah tanaman yang bermanfaat sebagai sayur, sebagai sumber vitamin, mineral, dan lain-lain yang berumur kurang dari satu tahun. Pada umumnya bagian yang digunakan sebagai sayur berupa daun, bunga, buah, dan umbi.

b. Tanaman buah-buahan semusim adalah tanaman yang menghasilkan buah segar sebagai sumber vitamin, mineral, dan lain-lain yang berumur kurang dari satu tahun dan berbatang lunak. Pada umumnya buah yang dihasilkan dapat dikonsumsi tanpa dimasak terlebih dahulu.""",
            """Seasonal vegetable and fruit plants

a. Seasonal vegetable plants are used/consumed as vegetables, which are the sources of vitamin, mineral, etc that are aged less than 1 year. In general, parts that consumed are in the form of leaves, flower, fruits, and tubers.

b. Seasonal fruit plants are plants that produce fresh fruit as a sources of vitamin, mineral, etc that aged less than 1 year and soft trunked. Generally, the fruit produced can be consumed without being cooked first."""
        ),
        (
            """Tanaman buah-buahan dan sayuran tahunan

a. Tanaman buah-buahan tahunan adalah tanaman yang menghasilkan buah segar sebagai sumber vitamin, mineral, dan lain-lain yang berumur satu tahun atau lebih dan berbatang keras. Pada umumnya buah yang dihasilkan dapat dikonsumsi tanpa dimasak terlebih dahulu.

b. Tanaman sayuran tahunan adalah tanaman yang bermanfaat sebagai sayur, sebagai sumber vitamin, mineral, dan lain-lain yang berumur satu tahun atau lebih. Pada umumnya bagian yang digunakan sebagai sayur berupa daun, bunga, buah, dan umbi.""",
            """Annual fruit and vegetable plants

a. Annual fruit plants are plants that produce fresh fruit as sources of vitamin, mineral, etc that are aged more than 1 year and hard trunked. Generally, the fruit produced can be consumed without being cooked first.

b. Annual vegetable plants are plants used as vegetables as sources of vitamin, mineral, etc that is aged more than 1 year. In general, the parts that consumed are in the form of leaves, flower, fruits, and tubers."""
        ),
        (
            """Tanaman biofarmaka adalah tanaman yang bermanfaat untuk obat-obatan, kosmetik, dan kesehatan yang dikonsumsi atau digunakan dari bagian-bagian tanaman, seperti daun, batang, buah, umbi (rimpang) ataupun akar.""",
            """Medicinal plants are plants that are beneficial for medicines, cosmetics, and health which are consumed or used from parts of plants, such as leaves, stems, fruits, tubers (rhizomes) or roots."""
        ),
        (
            """Tanaman hias adalah tanaman yang mempunyai nilai keindahan baik bentuk, warna daun, tajuk maupun bunganya, sering digunakan untuk penghias pekarangan dan lain sebagainya.""",
            """Ornamental plants are plants which have an aesthetic value, either in shape, leaf colour, canopy or flower, and are often used as yard decorators."""
        ),
        (
            """Luas panen untuk tanaman sayuran: luas tanaman yang dipanen sekaligus/habis/dibongkar dan luas tanaman yang dipanen berkali-kali (lebih dari satu kali)/belum habis.

a. Tanaman yang dipanen sekaligus/habis/dibongkar adalah tanaman yang sehabis panen langsung dibongkar/dicabut, terdiri dari bawang merah, bawang putih, bawang daun, kentang, kol/kubis, kembang kol, petsai/sawi, wortel, lobak, dan kacang merah.

b. Tanaman yang dipanen berkali-kali (lebih dari satu kali)/belum habis adalah tanaman yang pemanenannya lebih dari satu kali dan biasanya dibongkar apabila panenan terakhir sudah tidak memadai lagi, terdiri dari: kacang panjang, cabai besar, cabai rawit, jamur, tomat, terung, buncis, ketimun, labu siam, kangkung, bayam, melon, semangka, dan blewah.""",
            """Harvested area of vegetables: area of entirely harvested/demolished plant and plant that is harvested several times/undemolished.

a. Entirely harvested/demolished plants are plants usually harvested once and demolished to be substituted by other plants, consisting of: shallots, garlic, welsh onion, potato, cabbage, cauliflower, chinese cabbage, carrots, radish, and red beans.

b. Plants that are harvested several times/undemolished are plants usually harvested more than once and demolished in the case that the last harvest was economically not profitable. They consist of: yard long beans, chili, small chili, mushroom, tomatoes, eggplant, green beans, cucumber, chayote, water spinach, spinach, melon, watermelon, and cantaloupe."""
        ),
        (
            """Produksi adalah hasil menurut bentuk produk dari setiap tanaman sayuran, buah-buahan, biofarmaka, dan tanaman hias yang diambil berdasarkan luas yang dipanen/tanaman yang menghasilkan pada bulan/triwulan laporan.""",
            """Production is the standard production quantity form of vegetable, fruit, medicinal and ornamental plant based on harvested area/the number of production plants reported monthly/quarterly."""
        )
    ]

    bab5_intro = render_chapter_intro(
        chapter_num=5,
        title_id="PERTANIAN",
        title_en="AGRICULTURE",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab5
    )

    def extract_pertanian_rows(table_no, default_items):
        rows_raw = get_kecamatan_tab_rows(table_no, nama_singkat)
        res = []
        if len(rows_raw) > 2:
            for r in rows_raw[2:]:
                if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan', 'jenis tanaman', '(']):
                    t_name = r[0].replace('\r', '').replace('\n', ' ').strip()
                    # Simpan baris header kelompok/kategori (misal Sayuran/Vegetables:, Buah-buahan/Fruits:)
                    if t_name.endswith(':') or any(cat in t_name.lower() for cat in ['sayuran/vegetables', 'buah–buahan/fruits', 'buah-buahan/fruits', 'sayuran/ vegetables', 'buah–buahan / fruits']):
                        res.append([t_name, "", "", "", ""])
                        continue
                    # Fix typo cabai keiting -> Cabai keriting
                    if "cabai keiting" in t_name.lower():
                        t_name = "Cabai keriting / Curly Chili"
                    elif "cabai keriting" in t_name.lower() and "/" not in t_name:
                        t_name = "Cabai keriting / Curly Chili"
                    y22 = clean_cell_value(r[1] if len(r) > 1 else "–")
                    y23 = clean_cell_value(r[2] if len(r) > 2 else "–")
                    y24 = clean_cell_value(r[3] if len(r) > 3 else "–")
                    y25 = clean_cell_value(r[4] if len(r) > 4 else "–")
                    res.append([t_name, y22, y23, y24, y25])
        if not res:
            res = [[s, "–", "–", "–", "–"] for s in default_items]
        return res

    # --- 5.1 & 5.2 Sayuran ---
    sayuran_list = [
        "Bawang Merah / Shallots",
        "Cabai Besar / Big Chili",
        "Cabai keriting / Curly Chili",
        "Cabai Rawit / Cayenne Pepper",
        "Tomat / Tomato",
        "Terung / Eggplant",
        "Kacang Panjang / Long Beans",
        "Ketimun / Cucumber",
        "Kangkung / Water Spinach",
        "Bayam / Spinach"
    ]
    t51_rows = extract_pertanian_rows("5.1", sayuran_list)
    t51_markup = render_typst_table(
        table_no="5.1",
        title_id=f"Luas Panen Tanaman Sayuran dan Buah–buahan Semusim Menurut Jenis Tanaman di {nama_resmi} (ha), 2022–2025",
        title_en=f"Harvested Area of Seasonal Vegetables and Fruits by Kind of Plant in {nama_en} District (ha), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t51_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-SBS)"
    )

    t52_rows = extract_pertanian_rows("5.2", sayuran_list)
    t52_markup = render_typst_table(
        table_no="5.2",
        title_id=f"Produksi Tanaman Sayuran dan Buah–buahan Semusim Menurut Jenis Tanaman di {nama_resmi} (kuintal), 2022–2025",
        title_en=f"Production of Seasonal Vegetables and Fruits by Kind of Plant in {nama_en} District (quintal), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t52_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-SBS)"
    )

    # --- 5.3 & 5.4 Biofarmaka ---
    bio_list = [
        "Jahe / Ginger",
        "Lengkuas / Galangal",
        "Kencur / East Indian Galangal",
        "Kunyit / Turmeric",
        "Lempuyang",
        "Temulawak / Java Turmeric"
    ]
    t53_rows = extract_pertanian_rows("5.3", bio_list)
    t53_markup = render_typst_table(
        table_no="5.3",
        title_id=f"Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di {nama_resmi} (m²), 2022–2025",
        title_en=f"Harvested Area of Medicinal Plants by Kind of Plant in {nama_en} District (sq.m), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t53_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TBF)"
    )

    t54_rows = extract_pertanian_rows("5.4", bio_list)
    t54_markup = render_typst_table(
        table_no="5.4",
        title_id=f"Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di {nama_resmi} (kg), 2022–2025",
        title_en=f"Production of Medicinal Plants by Kind of Plant in {nama_en} District (kg), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t54_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TBF)"
    )

    # --- 5.5 & 5.6 Tanaman Hias ---
    hias_list = [
        "Anggrek Pot / Pot Orchid",
        "Anggrek Potong / Cut Orchid",
        "Krisan / Chrysanthemum",
        "Mawar / Rose",
        "Sedap Malam / Tuberose"
    ]
    t55_rows = extract_pertanian_rows("5.5", hias_list)
    t55_markup = render_typst_table(
        table_no="5.5",
        title_id=f"Luas Panen Tanaman Hias Menurut Jenis Tanaman di {nama_resmi} (m²), 2022–2025",
        title_en=f"Harvested Area of Ornamental Plants by Kind of Plant in {nama_en} District (sq.m), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t55_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TH) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TH)"
    )

    t56_rows = extract_pertanian_rows("5.6", hias_list)
    t56_markup = render_typst_table(
        table_no="5.6",
        title_id=f"Produksi Tanaman Hias Menurut Jenis Tanaman di {nama_resmi} (tangkai), 2022–2025",
        title_en=f"Production of Ornamental Plants by Kind of Plant in {nama_en} District (stalks), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t56_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TH) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TH)"
    )

    # --- 5.7 Buah-Buahan & Sayuran Tahunan ---
    buah_list = [
        "Durian / Durian",
        "Mangga / Mango",
        "Jeruk Siam / Orange",
        "Pisang / Banana",
        "Pepaya / Papaya",
        "Nanas / Pineapple",
        "Rambutan / Rambutan",
        "Jambu Biji / Guava",
        "Alpukat / Avocado",
        "Sukun / Breadfruit"
    ]
    t57_rows = extract_pertanian_rows("5.7", buah_list)
    t57_markup = render_typst_table(
        table_no="5.7",
        title_id=f"Produksi Buah–buahan dan Sayuran Tahunan Menurut Jenis Tanaman di {nama_resmi} (kuintal), 2022–2025",
        title_en=f"Production of Annual Fruits and Vegetables by Kind of Plant in {nama_en} District (quintal), 2022–2025",
        headers=["Jenis Tanaman\nKind of Plant", "2022", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t57_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST) / BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)"
    )

    return f"""
// ==========================================
// BAB 5: PERTANIAN (PENJELASAN TEKNIS & GAMBAR)
// ==========================================
{bab5_intro}
{chart_section}
// ==========================================
// TABEL DATA BAB 5 (1 HALAMAN 1 TABEL)
// ==========================================
{t51_markup}
#pagebreak()

{t52_markup}
#pagebreak()

{t53_markup}
#pagebreak()

{t54_markup}
#pagebreak()

{t55_markup}
#pagebreak()

{t56_markup}
#pagebreak()

{t57_markup}
"""
