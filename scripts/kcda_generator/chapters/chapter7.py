"""Chapter 7: Perbankan, Koperasi dan Perdagangan Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..config import get_regency_info

def render_chapter7(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    regency = get_regency_info()
    nama_kab = regency.get("nama_resmi", "Kabupaten")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]

    # --- 7.1 Sarana Perdagangan ---
    perdagangan_types = [
        "Pasar dengan Bangunan Permanen",
        "Pasar dengan Bangunan Semi Permanen",
        "Pasar Tanpa Bangunan",
        "Kelompok Pertokoan / Ruko",
        "Minimarket / Supermarket",
        "Restoran / Rumah Makan / Warung Makan",
        "Hotel / Penginapan / Losmen"
    ]
    t71_rows = [[p, "...", "...", "..."] for p in perdagangan_types]
    t71_markup = render_typst_table(
        table_no="7.1",
        title_id=f"Banyaknya Sarana Perdagangan Menurut Jenis Sarana di {nama_resmi}, 2023–2025",
        title_en=f"Number of Trade Facilities by Type in {nama_en}, 2023–2025",
        headers=["Jenis Sarana Perdagangan\nType of Trade Facility", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t71_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"Dinas Perindagnaker {nama_kab} / Podes 2025"
    )

    # --- 7.2 Koperasi ---
    koperasi_types = [
        "Koperasi Unit Desa (KUD)",
        "Koperasi Simpan Pinjam (KSP)",
        "Koperasi Lainnya (Non-KUD)",
        "Jumlah / Total"
    ]
    t72_rows = [[k, "...", "...", "..."] for k in koperasi_types]
    t72_markup = render_typst_table(
        table_no="7.2",
        title_id=f"Banyaknya Koperasi Aktif Menurut Jenis Koperasi di {nama_resmi}, 2023–2025",
        title_en=f"Number of Active Cooperatives by Type in {nama_en}, 2023–2025",
        headers=["Jenis Koperasi\nType of Cooperative", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t72_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source=f"Dinas Perindagnaker {nama_kab} / Podes 2025"
    )

    # --- 7.3 Lembaga Keuangan ---
    keuangan_types = [
        "Bank Umum Pemerintah (BRI, Mandiri, BNI, BTN, dll.)",
        "Bank Umum Swasta",
        "Bank Perekonomian Rakyat (BPR)",
        "Kantor Pegadaian"
    ]
    t73_rows = [[f, "...", "...", "..."] for f in keuangan_types]
    t73_markup = render_typst_table(
        table_no="7.3",
        title_id=f"Banyaknya Lembaga Keuangan Menurut Jenis Lembaga di {nama_resmi}, 2023–2025",
        title_en=f"Number of Financial Institutions by Type in {nama_en}, 2023–2025",
        headers=["Jenis Lembaga Keuangan\nType of Financial Institution", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t73_rows,
        col_widths=["2.8fr", "0.9fr", "0.9fr", "0.9fr"],
        source="Otoritas Jasa Keuangan (OJK) / Podes 2025"
    )

    return f"""
// ==========================================
// ISI BAB 7: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Aktivitas perniagaan di Kecamatan {nama_singkat} berkembang dinamis didukung oleh sarana perdagangan tradisional (pasar dan warung rakyat) serta jaringan minimarket modern. Keberadaan lembaga perbankan, koperasi, dan lembaga keuangan mikro memegang peranan krusial dalam memperluas inklusi keuangan serta akses permodalan bagi usaha mikro, kecil, dan menengah (UMKM).
]
#v(12pt)

{t71_markup}
#pagebreak()

{t72_markup}
#v(10pt)
{t73_markup}
"""
