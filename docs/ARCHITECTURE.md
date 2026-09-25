# Arsitektur Sistem KCDA Agent

Generator publikasi **Kecamatan Dalam Angka (KCDA)** dibangun dengan memisahkan domain data, tata letak dokumen (Typst layout engine), dan orkestrasi agentic.

---

## 1. Diagram Alur Sistem (System Flowchart)

```mermaid
flowchart TD
    subgraph Data Layer
        GS[Google Sheets Sumber Data] -->|sync_engine.py| RAW[data/raw_tables/*.json]
        CFG[config/regency.yaml] -->|config.py| LOAD[Config & Regency State]
        SCHEMA[config/tables_schema.json] -->|validator.py| VAL[Validation & Completeness]
    end

    subgraph Template & Presentation Layer
        RAW --> DL[data_loader.py]
        LOAD --> BUILD[builder.py Orchestrator]
        DL --> BUILD
        BUILD --> CH[Chapters 1-7 & Frontmatter]
        BUILD --> SVG[chart_generator.py & svg_engine]
        CH --> TYPST_SRC[kcda-slug.typ]
    end

    subgraph Output Layer
        TYPST_SRC -->|compiler.py / typst CLI| PDF[outputs/slug/kcda-slug.pdf]
    end
```

---

## 2. Struktur Modul Python (`scripts/kcda_generator/`)

- `config.py`: Parser tunggal konfigurasi daerah (`config/regency.yaml`) dengan fallback ke `regency.example.yaml`.
- `validator.py`: **Placeholder Guard** dan auditor kelengkapan tabel wajib per kecamatan.
- `data_loader.py`: Abstraksi pembacaan sel, normalisasi baris, dan ekstraksi data per tab kecamatan.
- `sync_engine.py`: Engine penarik spreadsheet Google Sheets via REST API menjadi JSON lokal.
- `table_renderer.py`: Format tabel ukuran A5 standar BPS dengan format dwibahasa otomatis (*bilingual auto-styling*).
- `chart_generator.py` & `charts/`: Generator grafik vektor murni (SVG) tanpa dependensi matplotlib yang berat.
- `builder.py`: Komposer naskah Typst ukuran A5 lengkap dari cover depan sampai backcover.
- `compiler.py`: Pemanggil compiler Typst resmi (`typst compile`) dengan deteksi font dan isolasi root.

---

## 3. Kompatibilitas BPS & Pedoman Desain

Naskah yang dihasilkan sepenuhnya patuh pada:
- **Pedoman Pembuatan Publikasi BPS 2023** (Ukuran A5, penomoran recto/verso, layout tabel dwibahasa).
- **Template Resmi KCDA BPS 2026** (Cover, halaman katalog, kata pengantar text-wrap meander, infografis pembuka bab, daftar pustaka).
- **Format Typst 0.13.0+** dengan waktu kompilasi sub-detik (~1 detik per publikasi 40+ halaman).
