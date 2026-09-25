# KCDA Agent - Antigravity Agent Guidelines

Repositori ini adalah generator otomatis publikasi **Kecamatan Dalam Angka (KCDA)** berstandar resmi Badan Pusat Statistik (BPS) RI untuk buku ukuran **A5**. Dirancang khusus untuk dieksekusi oleh **Coding Agent** (Antigravity IDE, Antigravity CLI / AGY).

---

## 1. Perilaku Otomatis Saat Membuka Workspace (Startup Protocol)

Setiap kali Anda (coding agent) diinisialisasi dalam repositori ini:

1. **Jalankan Pengecekan Status Pertama**:
   ```bash
   python3 scripts/kcda.py status
   ```
2. **Pendeteksian Profil Default (Placeholder Guard)**:
   - Jika terdeteksi `🚨 PERINGATAN PLACEHOLDER TEMPLATE` atau `is_template_default: true`:
     - Beritahukan pengguna secara proaktif bahwa repositori ini saat ini masih menggunakan profil contoh (Kabupaten Mempawah).
     - Tawarkan bantuan onboarding untuk mengonfigurasi profil Kabupaten/Kota mereka sendiri sesuai panduan di `.agents/skills/kcda-onboarding/SKILL.md`.

---

## 2. Pemisahan Peran Tegas (Role Division)

- **Coding Agent (Anda)**:
  - Menyusun naskah Typst (`scripts/kcda_generator/builder.py`).
  - Menghasilkan infografis SVG dinamis (`scripts/kcda_generator/chart_generator.py`).
  - Mengompilasi naskah menjadi PDF berkualitas cetak (`typst compile`).
  - Melakukan validasi konsistensi tabel dan data (`scripts/kcda.py validate`).
- **Data Collector / Rekan BPS (Pengguna)**:
  - Menyediakan metadata wilayah di `config/regency.yaml`.
  - Mengisi spreadsheet data kecamatan di Google Sheets.
  - Menyediakan berkas kover dan foto pimpinan di `assets/`.

---

## 3. Perintah CLI Utama (`scripts/kcda.py`)

Gunakan CLI resmi yang tersedia untuk setiap operasi:

| Perintah | Deskripsi |
| :--- | :--- |
| `python3 scripts/kcda.py status` | Menampilkan ringkasan status konfigurasi, kover, dan kesiapan PDF |
| `python3 scripts/kcda.py validate` | Menjalankan audit diagnostik data tabel wajib dan peringatan template |
| `python3 scripts/kcda.py sync [--tabel <no>]` | Menyinkronkan data dari Google Sheets ke `data/raw_tables/` |
| `python3 scripts/kcda.py generate -k <slug>` | Mengompilasi 1 kecamatan menjadi PDF (contoh: `-k mempawah-hilir`) |
| `python3 scripts/kcda.py generate --all` | Mengompilasi seluruh buku KCDA kabupaten secara batch |
| `python3 scripts/kcda.py init [--force]` | Menyiapkan template `config/regency.yaml` baru |

---

## 4. Kaidah Standar Publikasi BPS (Pedoman Publikasi 2023)

Saat memodifikasi naskah atau tabel, Anda **WAJIB** mematuhi:
- **Ukuran Kertas**: A5 (14.8 cm × 21.0 cm).
- **Format Judul Tabel & Grafik**: Dwibahasa (Bahasa Indonesia di atas tegak, Bahasa Inggris di bawah miring/italic).
- **Format Sumber Data (Source)**: Dwibahasa bergaris miring: `[Instansi ID]/#[Instansi EN]`.
- **Penomoran Halaman**:
  - Angka romawi kecil (`i, ii, iii, ...`) untuk bagian awal (frontmatter).
  - Angka arab (`1, 2, 3, ...`) dimulai dari Bab 1 Halaman 1.
  - Halaman ganjil di kanan (rekto), halaman genap di kiri (verso).
  - Judul bab baru selalu dimulai pada halaman ganjil (rekto).
- **Font Utama**: Menggunakan keluarga font yang tersedia di `assets/fonts/` (Myriad Pro / Liberation Sans / Arial).
