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
    d71 = {}
    if len(rows_71) > 2:
        for r in rows_71[2:]:
            if r and len(r) > 1 and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                d71[r[0].lower().split('\n')[0].strip()] = clean_cell_value(r[1])

    rows_72 = get_kecamatan_tab_rows("7.2", nama_singkat)
    d72 = {}
    if len(rows_72) > 2:
        for r in rows_72[2:]:
            if r and len(r) > 1 and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                d72[r[0].lower().split('\n')[0].strip()] = clean_cell_value(r[1])

    rows_73 = get_kecamatan_tab_rows("7.3", nama_singkat)
    d73 = {}
    if len(rows_73) > 2:
        for r in rows_73[2:]:
            if r and len(r) > 1 and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                d73[r[0].lower().split('\n')[0].strip()] = clean_cell_value(r[1])

    bg = int(d71.get('bank umum pemerintah', '0')) if d71.get('bank umum pemerintah', '0').isdigit() else 0
    bs = int(d71.get('bank umum swasta', '0')) if d71.get('bank umum swasta', '0').isdigit() else 0
    bb = int(d71.get('bank perkreditan rakyat (bpr)', '0')) if d71.get('bank perkreditan rakyat (bpr)', '0').isdigit() else 0

    kud = int(d72.get('koperasi unit desa (kud)', '0')) if d72.get('koperasi unit desa (kud)', '0').isdigit() else 0
    kospin = int(d72.get('koperasi simpan pinjam (kospin)', '0')) if d72.get('koperasi simpan pinjam (kospin)', '0').isdigit() else 0

    toko = int(d73.get('kelompok pertokoan', '0')) if d73.get('kelompok pertokoan', '0').isdigit() else 0
    pasar_p = int(d73.get('pasar dengan bangunan permanen', '0')) if d73.get('pasar dengan bangunan permanen', '0').isdigit() else 0
    pasar_sp = int(d73.get('pasar dengan bangunan semi permanen', '0')) if d73.get('pasar dengan bangunan semi permanen', '0').isdigit() else 0
    mini = int(d73.get('mini market/swalayan/supermarket', '0')) if d73.get('mini market/swalayan/supermarket', '0').isdigit() else 0
    resto = int(d73.get('restoran/rumah makan', '0')) if d73.get('restoran/rumah makan', '0').isdigit() else 0

    bank_id_parts = []
    bank_en_parts = []
    if bg > 0:
        bank_id_parts.append(f"{bg} desa memiliki Bank Umum Pemerintah")
        bank_en_parts.append(f"{bg} village(s) had Government Commercial Banks")
    if bs > 0:
        bank_id_parts.append(f"{bs} desa memiliki Bank Umum Swasta")
        bank_en_parts.append(f"{bs} village(s) had Private Commercial Banks")
    if bb > 0:
        bank_id_parts.append(f"{bb} desa memiliki Bank Perkreditan Rakyat (BPR)")
        bank_en_parts.append(f"{bb} village(s) had Rural Banks (BPR)")

    kop_id_parts = []
    kop_en_parts = []
    if kud > 0:
        kop_id_parts.append(f"Koperasi Unit Desa (KUD) di {kud} desa")
        kop_en_parts.append(f"Village Cooperative Units (KUD) in {kud} village(s)")
    if kospin > 0:
        kop_id_parts.append(f"Koperasi Simpan Pinjam di {kospin} desa")
        kop_en_parts.append(f"Savings and Loan Cooperatives in {kospin} village(s)")

    if bank_id_parts:
        str_bank_id = f"Keberadaan lembaga perbankan tercatat di mana {', '.join(bank_id_parts)}. "
        str_bank_en = f"The presence of banking institutions was recorded where {', '.join(bank_en_parts)}. "
    else:
        str_bank_id = f"Aktivitas perbankan masyarakat ditunjang oleh agen layanan perbankan tanpa kantor serta jaringan bank di kecamatan sekitar. "
        str_bank_en = f"Community banking activities are supported by branchless banking agents and banking networks in neighboring districts. "

    if kop_id_parts:
        str_kop_id = f"Di sektor perkoperasian, terdapat {' dan '.join(kop_id_parts)} yang berperan aktif memperkuat permodalan usaha warga."
        str_kop_en = f"In the cooperative sector, there were {' and '.join(kop_en_parts)} actively strengthening capital for local businesses."
    else:
        str_kop_id = f"Lembaga keuangan mikro dan kelompok simpan pinjam masyarakat terus didorong guna memfasilitasi permodalan usaha perdesaan."
        str_kop_en = f"Microfinance institutions and community loan groups continue to be encouraged to facilitate rural enterprise capital."

    teks_fin_id = (
        f"Lembaga keuangan perbankan dan koperasi memegang peranan krusial dalam mendukung likuiditas permodalan dan pertumbuhan ekonomi wilayah. "
        f"{str_bank_id}{str_kop_id}"
    )
    teks_fin_en = (
        f"Banking institutions and cooperatives play a vital role in supporting capital liquidity and regional economic growth. "
        f"{str_bank_en}{str_kop_en}"
    )

    pasar_tot = pasar_p + pasar_sp
    dagang_id_parts = []
    dagang_en_parts = []
    if pasar_tot > 0:
        dagang_id_parts.append(f"pasar permanen/semi permanen di {pasar_tot} desa/kelurahan")
        dagang_en_parts.append(f"permanent/semi-permanent markets in {pasar_tot} village(s)")
    if toko > 0:
        dagang_id_parts.append(f"kelompok pertokoan di {toko} desa/kelurahan")
        dagang_en_parts.append(f"shopping complexes in {toko} village(s)")
    if mini > 0:
        dagang_id_parts.append(f"minimarket/swalayan di {mini} desa/kelurahan")
        dagang_en_parts.append(f"minimarkets/supermarkets in {mini} village(s)")
    if resto > 0:
        dagang_id_parts.append(f"restoran/rumah makan di {resto} desa/kelurahan")
        dagang_en_parts.append(f"restaurants/food stalls in {resto} village(s)")

    if dagang_id_parts:
        teks_trade_id = (
            f"Aktivitas perdagangan dan distribusi barang konsumsi di Kecamatan {nama_singkat} berkembang dengan ketersediaan "
            f"{', '.join(dagang_id_parts)}. Keberadaan sarana perniagaan ini memastikan kelancaran rantai pasok kebutuhan pokok bagi masyarakat."
        )
        teks_trade_en = (
            f"Trade and consumer goods distribution activities in {nama_en} District thrive with the availability of "
            f"{', '.join(dagang_en_parts)}. These commercial amenities ensure smooth supply chains of basic necessities for the community."
        )
    else:
        teks_trade_id = (
            f"Aktivitas perniagaan dan pemenuhan kebutuhan pokok masyarakat di Kecamatan {nama_singkat} bertumpu pada jaringan toko kelontong tradisional "
            f"serta pasar berkala antardesa yang menghubungkan produsen lokal dengan konsumen."
        )
        teks_trade_en = (
            f"Commercial activities and basic necessity fulfillment in {nama_en} District rely on traditional grocery store networks "
            f"and periodic inter-village markets connecting local producers with consumers."
        )

    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Perbankan dan Koperasi] \\
  #v(2pt)
  {teks_fin_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Sarana Perdagangan] \\
  #v(2pt)
  {teks_trade_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Banking and Cooperatives] \\
  #v(2pt)
  {teks_fin_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Trade Facilities] \\
  #v(2pt)
  {teks_trade_en}
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
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Cooperative by Type of Cooperative in {nama_en} District, 2025",
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
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Trade Facilities by Type of Trade Facilities in {nama_en} District, 2025",
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
