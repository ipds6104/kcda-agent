"""Chapter 7: Perbankan, Koperasi dan Perdagangan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter7(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())

    # Penjelasan Teknis & Ulasan Bab 7 Resmi BPS
    rows_71 = get_kecamatan_tab_rows("7.1", nama_singkat)
    bank_cnt = "–"
    if len(rows_71) > 2:
        for r in rows_71[2:]:
            if r and "pemerintah" in r[0].lower():
                bank_cnt = clean_cell_value(r[1] if len(r) > 1 else "–")
                break

    if bank_cnt != "–" and bank_cnt != "0":
        teks_fin_id = (
            f"Perbankan dan koperasi merupakan lembaga keuangan yang berperan penting dalam menggerakkan perekonomian masyarakat. "
            f"Pada tahun 2025 di Kecamatan {nama_singkat}, tercatat keberadaan Bank Umum Pemerintah di {bank_cnt} desa/kelurahan, "
            f"serta lembaga koperasi yang beroperasi di wilayah kecamatan guna mendukung permodalan usaha masyarakat."
        )
        teks_fin_en = (
            f"Banks and cooperatives are vital financial institutions that drive the community economy. "
            f"In 2025, in {nama_en} District, Government Commercial Banks were available in {bank_cnt} village(s)/subdistrict(s), "
            f"along with cooperatives operating across the district to support business capital."
        )
    else:
        teks_fin_id = (
            f"Perbankan dan koperasi merupakan lembaga keuangan yang berperan dalam menggerakkan perekonomian masyarakat. "
            f"Di Kecamatan {nama_singkat}, keberadaan sarana lembaga keuangan bank dan koperasi simpan pinjam "
            f"terus menunjang kelancaran transaksi serta akses permodalan bagi usaha masyarakat."
        )
        teks_fin_en = (
            f"Banks and cooperatives are financial institutions playing an important role in driving the community economy. "
            f"In {nama_en} District, the presence of banking and cooperative facilities "
            f"continues to support smooth transactions and capital access for local enterprises."
        )

    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[Perbankan dan Koperasi] \\
  #v(2pt)
  {teks_fin_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[Banking and Cooperatives] \\
  #v(2pt)
  {teks_fin_en}
]"""

    technical_notes_bab7 = [
        (
            "Bank adalah badan usaha yang menghimpun dana dari masyarakat dalam bentuk simpanan, dan menyalurkannya kepada masyarakat dalam rangka meningkatkan taraf hidup rakyat banyak.",
            "Bank is business entity that raise funds from the public in deposits and distribute it to the public in order to improve the living standard of the people."
        ),
        (
            "Bank Umum adalah bank yang dapat memberikan jasa dalam lalu lintas pembayaran (Undang-Undang Nomor 7 Tahun 1992 Tentang Perbankan).",
            "Commercial Bank is a bank that can provide services in payment transfer (Law Number 7 Year 1992 About Banking)."
        ),
        (
            "Bank Perkreditan Rakyat adalah bank yang menerima simpanan hanya dalam bentuk deposito berjangka, tabungan, dan/atau bentuk lainnya yang dipersamakan dengan itu.",
            "Rural bank is a bank that accepts saving in time deposits, savings, or others."
        ),
        (
            "Koperasi adalah badan usaha yang beranggotakan orang-seorang atau badan hukum koperasi dengan melandaskan kegiatannya berdasarkan prinsip:\n\na. Keanggotaannya sukarela dan terbuka;\n\nb. Pengelolaannya dilakukan secara demokratis;\n\nc. Pembagian sisa hasil usahanya dilakukan secara adil, sebanding dengan besarnya jasa usaha masing-masing anggota;\n\nd. Pemberian balas jasa yang terbatas terhadap modal; dan\n\ne. Kemandirian, serta sekaligus sebagai gerakan ekonomi rakyat yang berdasarkan atas asas kekeluargaan.",
            "Cooperative is a business entity consisting of people or cooperative legal entities which activities are based on the principles:\n\na. Membership is voluntary and open;\n\nb. Management is conducted democratically;\n\nc. Benefits are distributed proportionally according to the member’s share;\n\nd. Remuneration is limited to the capital; and\n\ne. Independence, as well as the people’s economic movement based on the principle of kinship."
        ),
        (
            "Kelompok Pertokoan adalah sejumlah toko yang terdiri dari minimal sepuluh toko dan mengelompok. Dalam satu kelompok pertokoan, jumlah bangunan fisiknya bisa lebih dari satu.",
            "Shopping Complex is a group of shops consisting at least ten stores and clumped. In one shopping complex, number of physical buildings can be more than one."
        ),
        (
            "Pasar dengan Bangunan Permanen/Semi Permanen adalah pasar yang menggunakan bangunan tetap dan memiliki lantai, atap, baik berdinding maupun tidak.",
            "Market in the Permanent/Semi Permanent Building is a market that uses the permanent building and have floor, roof, whether it walled or not."
        ),
        (
            "Pasar Tanpa Bangunan adalah pasar yang tidak berada dalam bangunan, termasuk pasar terapung.",
            "Market Without Building is a market that is not located within the building, including the floating market."
        ),
        (
            "Mini Market adalah tempat usaha yang menjual berbagai jenis barang secara eceran dengan sistem pelayanan mandiri dan semua barang memiliki label harga, dengan luas bangunan kurang dari 400 m².",
            "Mini Market is a place of business which sell various kinds of goods at retail by self-service system and everything has a price tag, with a building area of less than 400 m²."
        ),
        (
            "Restoran adalah tempat usaha yang mempergunakan seluruh bangunan secara permanen untuk menyediakan jasa pangan yang pengolahannya dan penyajiannya secara langsung di tempat sesuai dengan keinginan para pengguna jasa.",
            "Restaurant is a place of business that use the entire building permanently to provide food processing services and presented directly in place in accordance with the wishes of service users."
        )
    ]

    bab7_intro = render_chapter_intro(
        chapter_num=7,
        title_id="PERBANKAN, KOPERASI, DAN PERDAGANGAN",
        title_en="BANKING, COOPERATIVE, AND TRADE",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab7
    )

    def extract_rows(table_no: str, fallback_rows: List[List[str]]) -> List[List[str]]:
        raw_rows = get_kecamatan_tab_rows(table_no, nama_singkat)
        if len(raw_rows) > 2:
            extracted = []
            for r in raw_rows[2:]:
                if len(r) >= 2 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["sumber", "catatan", "tabel"]):
                    item = r[0].strip()
                    val = clean_cell_value(r[1]) if len(r) > 1 else "–"
                    extracted.append([item, val])
            if extracted:
                return extracted
        return fallback_rows

    sumber_podes = "Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/BPS–Statistics Indonesia, Village Potential Data Collecting"
    catatan_podes = "#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries"

    # --- 7.1 Bank ---
    fallback_71 = [
        ["Bank Umum Pemerintah\nGovernment Bank", "0"],
        ["Bank Umum Swasta\nPrivate Bank", "0"],
        ["Bank Perkreditan Rakyat (BPR)\nRural Bank", "0"]
    ]
    t71_rows = extract_rows("7.1", fallback_71)
    t71_markup = render_typst_table(
        table_no="7.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Lembaga Keuangan Bank Menurut Jenis Bank di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Bank by Type of Bank in {nama_en} District, 2025",
        headers=["Jenis Bank\nType of Bank", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t71_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    # --- 7.2 Koperasi ---
    fallback_72 = [
        ["Koperasi Unit Desa (KUD)\nVillage Cooperative Unit", "0"],
        ["Koperasi industri kecil dan kerajinan rakyat (Kopinkra)\nSmall industry and citizen handicraft cooperative", "0"],
        ["Koperasi simpan pinjam (kospin)\nSavings and loan cooperative", "0"],
        ["Koperasi lainnya\nOther cooperative", "0"]
    ]
    t72_rows = extract_rows("7.2", fallback_72)
    t72_markup = render_typst_table(
        table_no="7.2",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Koperasi Aktif Menurut Jenis Koperasi di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Active Cooperatives by Type in {nama_en} District, 2025",
        headers=["Jenis Koperasi\nType of Cooperative", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t72_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    # --- 7.3 Sarana Perdagangan ---
    fallback_73 = [
        ["Kelompok pertokoan\nShopping complexs", "0"],
        ["Pasar dengan bangunan permanen\nMarkets in permanent building", "0"],
        ["Pasar dengan bangunan semi permanen\nMarket in semi permanent building", "0"],
        ["Pasar tanpa bangunan\nMarket without permanent building", "0"],
        ["Mini market/swalayan/supermarket", "0"],
        ["Restoran/rumah makan\nRestaurant/food stall", "0"]
    ]
    t73_rows = extract_rows("7.3", fallback_73)
    t73_markup = render_typst_table(
        table_no="7.3",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Perdagangan Menurut Jenis Sarana Perdagangan di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Trade Facilities by Type in {nama_en} District, 2025",
        headers=["Jenis Sarana Perdagangan\nType of Trade Facilities", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t73_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    return f"""
// ==========================================
// ISI BAB 7: ULASAN NARASI & TABEL DATA
// ==========================================
{bab7_intro}
// ==========================================
// TABEL DATA BAB 7 (1 HALAMAN 1 TABEL)
// ==========================================
{t71_markup}
#pagebreak()

{t72_markup}
#pagebreak()

{t73_markup}
"""
