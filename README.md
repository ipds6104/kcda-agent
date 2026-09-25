# KCDA Agent 📊🇮🇩

> **Generator Publikasi Kecamatan Dalam Angka (KCDA) Otomatis Berstandar Resmi BPS RI (Ukuran A5) yang Dirancang Khusus untuk Coding Agent.**

[![Typst](https://img.shields.io/badge/Layout_Engine-Typst_v0.13-239dad.svg)](https://typst.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![BPS Standard](https://img.shields.io/badge/Standard-BPS_Publikasi_2023-orange.svg)](https://bps.go.id)

---

## 🌟 Tentang KCDA Agent

**KCDA Agent** adalah repositori modular berkecepatan tinggi untuk menghasilkan buku publikasi resmi **Kecamatan Dalam Angka (KCDA)** untuk seluruh BPS Kabupaten/Kota di Indonesia.

Dibangun dengan arsitektur **Typst**, sistem ini dapat mengompilasi buku statistik setebal 40+ halaman berstandar cetak dalam waktu **kurang dari 2 detik** (ratusan kali lebih cepat dibandingkan LaTeX atau InDesign manual).

---

## 🤝 Pemisahan Peran yang Tegas (Human-Agent Synergy)

Repositori ini secara sengaja memisahkan tanggung jawab teknis dan pengumpulan data:

| Peran | Pihak | Tanggung Jawab Utama |
| :--- | :--- | :--- |
| 🤖 **Coding Agent** *(Antigravity / AGY)* | AI Engineer | Menjalankan orkestrasi layout Typst, rendering SVG dinamis, validasi schema tabel, pemantauan error, dan kompilasi PDF. |
| 🧑‍💼 **Data Collector / PIC BPS** | Manusia / Tim Teknis | Mengisi daftar kecamatan di `config/regency.yaml`, mengisi data di Google Sheets, dan mengunggah desain kover wilayah. |

---

## 🚀 Panduan Memulai Cepat (Quickstart)

### 1. Prasyarat Sistem
- **Python 3.10+** (dengan dependensi `pyyaml` dan `requests`):
  ```bash
  pip install pyyaml requests
  ```
- **Typst CLI v0.13.0+** ([Panduan Instalasi Typst](https://github.com/typst/typst)):
  ```bash
  # Linux (x86_64 / aarch64)
  curl -fsSL https://github.com/typst/typst/releases/download/v0.13.0/typst-x86_64-unknown-linux-musl.tar.xz | tar -xJ && mv typst-*/typst /usr/local/bin/
  ```

---

### 2. Memeriksa Status Awal Repositori
Jalankan perintah status untuk melihat kesiapan berkas:
```bash
python3 scripts/kcda.py status
```

---

### 3. Mengonfigurasi Kabupaten / Kota Anda

Secara bawaan, repositori ini menyertakan dataset contoh (Kabupaten Mempawah). Sistem dilengkapi dengan **Placeholder Guard** aktif yang akan mengingatkan Anda jika profil template belum disesuaikan.

Untuk mengonfigurasi BPS Kabupaten/Kota Anda:
1. Buat berkas konfigurasi baru:
   ```bash
   python3 scripts/kcda.py init
   ```
2. Atau minta coding agent Anda:
   > *"Bantu saya isi config/regency.yaml untuk BPS Kabupaten [Nama Daerah]"*
   
   Coding agent akan otomatis mengaktifkan skill onboarding (`.agents/skills/kcda-onboarding/SKILL.md`) dan memandu Anda tahap demi tahap.
3. Setelah disesuaikan, ubah flag di `config/regency.yaml`:
   ```yaml
   is_template_default: false
   ```

---

### 4. Menghubungkan & Menyinkronkan Google Sheets

1. Buat spreadsheet Google Sheets untuk setiap tabel wajib dengan tab per nama kecamatan.
2. Salin Spreadsheet ID ke dalam `config/tables_schema.json` (lihat panduan lengkap di [`docs/GOOGLE_SHEETS_GUIDE.md`](docs/GOOGLE_SHEETS_GUIDE.md)).
3. Sinkronkan seluruh data ke lokal:
   ```bash
   python3 scripts/kcda.py sync
   ```

---

### 5. Validasi Kesiapan Data
Jalankan audit diagnostik untuk memastikan seluruh tabel wajib 100% terisi:
```bash
python3 scripts/kcda.py validate
```

---

### 6. Mengompilasi Menjadi PDF Buku Resmi BPS

Kompilasi satu kecamatan spesifik:
```bash
python3 scripts/kcda.py generate -k mempawah-hilir
```

Atau kompilasi seluruh kecamatan di kabupaten secara serentak (batch compilation):
```bash
python3 scripts/kcda.py generate --all
```

Hasil PDF berstandar cetak akan tersimpan rapi di:
```
outputs/<slug-kecamatan>/kcda-<slug-kecamatan>.pdf
```

---

## 📁 Struktur Direktori Repositori

```
kcda-agent/
├── .agents/
│   └── skills/
│       └── kcda-onboarding/     # Panduan wawancara interaktif coding agent
├── assets/
│   ├── covers/                 # Kover depan, belakang, dan pembatas bab
│   ├── fonts/                  # Font resmi BPS (Myriad Pro / Liberation Sans)
│   ├── logo_bps.png            # Logo resmi BPS RI
│   ├── logo_se2026.png         # Logo publisitas Sensus Ekonomi 2026
│   └── kepala_bps.png          # Foto portrait pimpinan (alpha-transparent)
├── config/
│   ├── regency.yaml            # Konfigurasi master kabupaten & daftar kecamatan
│   ├── regency.example.yaml    # Template acuan konfigurasi daerah baru
│   └── tables_schema.json      # Skema kamus tabel wajib & mapping sheet ID
├── data/
│   └── raw_tables/             # Cache data tabel terstruktur dalam format JSON
├── docs/
│   ├── ARCHITECTURE.md         # Dokumentasi arsitektur sistem
│   └── GOOGLE_SHEETS_GUIDE.md  # Panduan format Google Sheets untuk operator data
├── outputs/                    # Folder output hasil kompilasi berkas Typst & PDF
├── scripts/
│   ├── kcda.py                 # Unified Command-Line Interface (CLI)
│   └── kcda_generator/         # Modul inti Python (builder, compiler, sync, dsb.)
├── GEMINI.md                   # Aturan & protokol operasi coding agent (AGY)
└── README.md
```

---

## 🛡️ Placeholder Guard

Sistem validator (`scripts/kcda_generator/validator.py`) secara aktif memverifikasi:
- Apakah repositori masih menggunakan konfigurasi template contoh Mempawah.
- Kelengkapan persentase tabel wajib per kecamatan.
- Ketersediaan aset foto pimpinan dan kover depan/belakang.

Peringatan akan otomatis dimunculkan pada terminal untuk mencegah naskah sampel template tidak sengaja terbit ke publik.

---

## 📄 Lisensi & Kontribusi

Dikembangkan untuk mendukung percepatan digitalisasi publikasi di lingkungan **Badan Pusat Statistik (BPS)** seluruh Indonesia.
Bebas digunakan, dimodifikasi, dan didistribusikan untuk kepentingan dinas dan publikasi statistik.
