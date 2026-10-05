"""Chapter 6: Pariwisata, Transportasi dan Komunikasi Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table, render_subchapter_heading
from ..config import get_regency_info
from .narrative_helper import render_chapter_intro

def render_chapter6(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = cfg.get("nama_singkat", nama_resmi.replace("Kecamatan ", "").strip())

    # Penjelasan Teknis & Ulasan Bab 6 Resmi BPS
    rows_611 = get_kecamatan_tab_rows("6.1.1", nama_singkat)
    hotel_cnt = "0"
    inn_cnt = "0"
    if len(rows_611) > 2:
        for r in rows_611[2:]:
            if r:
                r_txt = r[0].lower()
                if "hotel" in r_txt:
                    hotel_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")
                elif "penginapan" in r_txt or "inn" in r_txt:
                    inn_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")

    teks_akomodasi_id = f"tersedia sarana akomodasi berupa {hotel_cnt} hotel dan {inn_cnt} penginapan" if (hotel_cnt != "0" or inn_cnt != "0") else "tersedia sarana akomodasi dan fasilitas penunjang"
    teks_akomodasi_en = f"had accommodation facilities consisting of {hotel_cnt} hotel and {inn_cnt} inn" if (hotel_cnt != "0" or inn_cnt != "0") else "had accommodation facilities and supporting amenities"

    ulasan_id = (
        f"Pada tahun 2025, di Kecamatan {nama_singkat} {teks_akomodasi_id}. "
        f"Selain itu, tersedia jaringan komunikasi serta layanan pengiriman ekspedisi swasta yang beroperasi di wilayah kecamatan. "
        f"Seluruh wilayah di Kecamatan {nama_singkat} dapat diakses melalui jalur transportasi darat."
    )
    ulasan_en = (
        f"In 2025, {nama_en} District {teks_akomodasi_en}. "
        f"In addition, communication networks and private courier services operated across the district. "
        f"All areas in {nama_en} District are accessible by land transportation routes."
    )

    technical_notes_bab6 = [
        (
            "Hotel adalah jenis akomodasi yang mempergunakan sebagian atau keseluruhan bangunan untuk jasa pelayanan penginapan, penyedia makanan dan minuman serta jasa lainnya (seperti restoran, binatu, d.l.l) bagi masyarakat umum yang dikelola secara komersial dengan izin usaha sebagai hotel.",
            "Hotel is the kind of accommodation that use part or the whole building for lodging services, food and beverage and other services (such as restaurants, laundry, etc.) for the public which is commercially managed with a business license of hotel."
        ),
        (
            "Penginapan (Hostel/Motel/Losmen/Wisma) adalah jenis akomodasi yang mempergunakan sebagian atau keseluruhan bangunan untuk jasa pelayanan penginapan bagi umum, biasanya tanpa fasilitas pelayanan makan minum yang dikelola secara komersial dengan izin usaha bukan hotel.",
            "Inn is a type of accommodation that use part or the whole building for lodging services to the public, usually without eating and drinking facilities which is commercially managed with a business license of non-hotel."
        ),
        (
            "Prasarana Transportasi adalah sarana penunjang lalu lintas pemindahan orang dan atau barang, yang terdiri atas jalan, jembatan, dermaga, pelabuhan, dan lain-lain yang digunakan oleh warga desa untuk mobilitas dari dan ke desa terdekat.",
            "Transportation Infrastructure is a facility of supporting the transfer of people and or goods, which consists of roads, bridges, docks, harbors, etc used by villagers for mobility to and from the nearest village."
        ),
        (
            "Kantor Pos adalah tempat pemberi pelayanan komunikasi tertulis dan atau surat elektronik, layanan paket, layanan logistik, layanan transaksi keuangan, dan layanan keagenan pos untuk kepentingan umum. Rumah pos berfungsi sama seperti kantor pos dan kantor pos pembantu, bedanya rumah pos biasanya terletak di daerah terpencil.",
            "Post Office is a service provider place of written communication and or electronic mail, parcel service, logistics services, financial transaction services, postal and agency services to the public. Postal house has the same function as the post office and subsidiary of post office, the difference is that postal house usually located in remote areas."
        ),
        (
            "Pos Keliling adalah pelayanan pos (menjual, mengirim, dan menerima benda pos) keliling dengan menggunakan mobil atau sarana angkutan yang berfungsi sama seperti kantor pos atau kantor pos pembantu.",
            "Mobile Postal Service is nomadic postal service (to sell, send, and receive postal stationery) by car or transportation facility that the functions are the same as the post office or subsidiary of post office."
        ),
        (
            "Perusahaan Jasa Agen Ekspedisi Swasta adalah pelayanan pengiriman paket maupun dokumen yang dikelola oleh pihak swasta, misalnya Tiki, JNE, ESL, d.l.l.",
            "Private Expedition Service Company is packages and documents delivery service managed by privates, for example Tiki, JNE, ESL, etc."
        )
    ]

    bab6_intro = render_chapter_intro(
        chapter_num=6,
        title_id="PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI",
        title_en="TOURISM, TRANSPORTATION, AND COMMUNICATION",
        ulasan_id=ulasan_id,
        ulasan_en=ulasan_en,
        technical_notes=technical_notes_bab6
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

    # --- 6.1.1 Sarana Akomodasi ---
    fallback_611 = [
        ["Hotel", "0"],
        ["Penginapan\nInn", "0"]
    ]
    t611_rows = extract_rows("6.1.1", fallback_611)
    t611_markup = render_typst_table(
        table_no="6.1.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Akomodasi Menurut Jenis Akomodasi di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts with Availability of Accommodation Facilities by Type of Accommodation in {nama_en} District, 2025",
        headers=["Jenis Akomodasi\nType of Accommodation", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t611_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    # --- 6.2.1 Prasarana dan Sarana Transportasi Antardesa ---
    fallback_621 = [
        ["Darat/Land", "0"],
        ["Air/Water", "0"],
        ["Darat dan air/Land and water", "0"],
        ["Udara/Air", "0"]
    ]
    t621_rows = extract_rows("6.2.1", fallback_621)
    t621_markup = render_typst_table(
        table_no="6.2.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan Menurut Prasarana dan Sarana Transportasi Antardesa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts by Inter-Village/ Subdistricts Transportation Infrastructure and Facilities in {nama_en} District, 2025",
        headers=["Prasarana dan Sarana Transportasi Antardesa/Kelurahan\nTransportation Infrastructure and Facilities Between Villages/Subdistricts", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t621_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    # --- 6.3.1 Kantor Pos dan Agen Ekspedisi Swasta ---
    fallback_631 = [
        ["Kantor Pos/Pos Pembantu/Rumah Pos\nPost Office/Subsidiary of Post Office", "0"],
        ["Pos Keliling\nMobile Postal Service", "0"],
        ["Perusahaan/Agen Jasa Ekspedisi Swasta\nPrivate Expedition Service Company", "0"]
    ]
    t631_rows = extract_rows("6.3.1", fallback_631)
    t631_markup = render_typst_table(
        table_no="6.3.1",
        title_id=f"Banyaknya Desa#super[1]/Kelurahan Menurut Keberadaan Kantor Pos/Pos Pembantu/Rumah Pos, Pos Keliling, dan Perusahaan/Agen Jasa Ekspedisi Swasta di {nama_resmi}, 2025",
        title_en=f"Number of Villages#super[1]/Subdistricts by Post Office/Subsidiary of Post Office, Mobile Postal Service, Private Expedition Service Company in {nama_en} District, 2025",
        headers=["Fasilitas Pos dan Ekspedisi\nPost and Expedition Facilities", "2025"],
        col_numbers=["(1)", "(2)"],
        rows=t631_rows,
        col_widths=["3.6fr", "1.2fr"],
        source=sumber_podes,
        notes=catatan_podes
    )

    sec_61 = render_subchapter_heading("6.1", "PARIWISATA", "TOURISM")
    sec_62 = render_subchapter_heading("6.2", "TRANSPORTASI", "TRANSPORTATION")
    sec_63 = render_subchapter_heading("6.3", "KOMUNIKASI", "COMMUNICATION")

    return f"""
// ==========================================
// ISI BAB 6: ULASAN NARASI & TABEL DATA
// ==========================================
{bab6_intro}
// ==========================================
// 6.1 PARIWISATA
// ==========================================
{sec_61}
{t611_markup}
#pagebreak()

// ==========================================
// 6.2 TRANSPORTASI
// ==========================================
{sec_62}
{t621_markup}
#pagebreak()

// ==========================================
// 6.3 KOMUNIKASI
// ==========================================
{sec_63}
{t631_markup}
"""
