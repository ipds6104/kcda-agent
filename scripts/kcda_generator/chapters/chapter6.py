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

    h_val = int(hotel_cnt) if hotel_cnt.isdigit() else 0
    inn_val = int(inn_cnt) if inn_cnt.isdigit() else 0

    akom_id_list = []
    akom_en_list = []
    if h_val > 0:
        akom_id_list.append(f"{h_val} hotel")
        akom_en_list.append(f"{h_val} hotel(s)")
    if inn_val > 0:
        akom_id_list.append(f"{inn_val} penginapan/losmen")
        akom_en_list.append(f"{inn_val} inn(s)")

    if akom_id_list:
        teks_akom_id = f"Ketersediaan sarana akomodasi pariwisata di Kecamatan {nama_singkat} tercatat sebanyak {' dan '.join(akom_id_list)} guna menunjang mobilitas wisatawan dan perjalanan dinas."
        teks_akom_en = f"The availability of tourism accommodation facilities in {nama_en} District was recorded at {' and '.join(akom_en_list)} to support visitor mobility and business travel."
    else:
        teks_akom_id = f"Sarana akomodasi wisata di Kecamatan {nama_singkat} bertumpu pada fasilitas hunian singgah dan penginapan di sekitar wilayah kecamatan."
        teks_akom_en = f"Tourism accommodation facilities in {nama_en} District rely on lodging and transit residential facilities in adjacent areas."

    rows_621 = get_kecamatan_tab_rows("6.2.1", nama_singkat)
    darat_cnt = "0"
    darat_air_cnt = "0"
    if len(rows_621) > 2:
        for r in rows_621[2:]:
            if r:
                r_txt = r[0].lower()
                if "darat dan air" in r_txt:
                    darat_air_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")
                elif "darat" in r_txt:
                    darat_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")

    d_val = int(darat_cnt) if darat_cnt.isdigit() else 0
    da_val = int(darat_air_cnt) if darat_air_cnt.isdigit() else 0

    if da_val > 0:
        teks_trans_id = f"Prasarana dan sarana transportasi antardesa di Kecamatan {nama_singkat} dilayani melalui jalur darat di {d_val} desa/kelurahan serta perpaduan jalur darat dan air di {da_val} desa/kelurahan."
        teks_trans_en = f"Inter-village transportation infrastructure and facilities in {nama_en} District were served via land routes in {d_val} village(s) as well as combined land and water routes in {da_val} village(s)."
    else:
        teks_trans_id = f"Seluruh desa/kelurahan di Kecamatan {nama_singkat} ({d_val} desa/kelurahan) telah terhubung dan dapat diakses dengan mudah melalui prasarana dan sarana transportasi darat."
        teks_trans_en = f"All villages in {nama_en} District ({d_val} village(s)) are connected and readily accessible through land transportation infrastructure and facilities."

    rows_631 = get_kecamatan_tab_rows("6.3.1", nama_singkat)
    pos_cnt = "0"
    eksp_cnt = "0"
    if len(rows_631) > 2:
        for r in rows_631[2:]:
            if r:
                r_txt = r[0].lower()
                if "kantor pos" in r_txt:
                    pos_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")
                elif "ekspedisi" in r_txt:
                    eksp_cnt = clean_cell_value(r[1] if len(r) > 1 else "0")

    p_val = int(pos_cnt) if pos_cnt.isdigit() else 0
    e_val = int(eksp_cnt) if eksp_cnt.isdigit() else 0

    kom_id_parts = []
    kom_en_parts = []
    if p_val > 0:
        kom_id_parts.append(f"{p_val} desa memiliki kantor pos/pos pembantu")
        kom_en_parts.append(f"{p_val} village(s) had post office facilities")
    if e_val > 0:
        kom_id_parts.append(f"{e_val} desa dilayani agen ekspedisi swasta")
        kom_en_parts.append(f"{e_val} village(s) served by private courier agencies")

    if kom_id_parts:
        teks_kom_id = f"Layanan komunikasi dan pengiriman logistik kian berkembang dengan {' serta '.join(kom_id_parts)} yang mempermudah sirkulasi barang dan perniagaan masyarakat."
        teks_kom_en = f"Communication and courier logistics services continue to expand with {' and '.join(kom_en_parts)}, facilitating the flow of goods and local commerce."
    else:
        teks_kom_id = f"Jaringan telekomunikasi seluler dan layanan logistik terus diperluas guna memenuhi kebutuhan komunikasi dan perniagaan daring masyarakat antardesa."
        teks_kom_en = f"Cellular telecommunication networks and delivery logistics continue to expand to fulfill inter-village communication and e-commerce needs."

    ulasan_id = f"""#block[
  #text(8pt, weight: "bold")[1. #h(2pt) Pariwisata dan Akomodasi] \\
  #v(2pt)
  {teks_akom_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Transportasi Antardesa] \\
  #v(2pt)
  {teks_trans_id}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Komunikasi dan Pos] \\
  #v(2pt)
  {teks_kom_id}
]"""

    ulasan_en = f"""#block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Tourism and Accommodation] \\
  #v(2pt)
  {teks_akom_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Inter-Village Transportation] \\
  #v(2pt)
  {teks_trans_en}
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Communication and Postal Services] \\
  #v(2pt)
  {teks_kom_en}
]"""

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
