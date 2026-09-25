---
name: kcda-onboarding
description: Proactive onboarding and configuration skill for KCDA Agent. Guides coding agents to interview users and customize config/regency.yaml for any BPS Regency/City office.
---

# KCDA Agent Onboarding & Customization Protocol

Dokumen panduan ini ditujukan bagi **Coding Agent** (Antigravity IDE, Antigravity CLI / AGY) saat pertama kali mendeteksi repositori ini dibuka oleh pengguna baru dari BPS Kabupaten/Kota manapun di Indonesia.

---

## 1. Misi & Peran Agen

Sebagai coding agent dalam repositori ini, tugas Anda adalah **memandu dan mengonfigurasi generator publikasi KCDA** agar sepenuhnya mencerminkan identitas daerah pengguna.

> [!IMPORTANT]
> **Pemisahan Peran yang Tegas**:
> - **Coding Agent (Anda)**: Menjalankan arsitektur kompilasi Typst, validasi schema tabel, pemuatan data lokal/Google Sheets, pembuatan chart SVG, dan penjagaan kualitas tipografi naskah buku resmi BPS ukuran A5.
> - **Data Collector / Rekan BPS (Pengguna)**: Memberikan daftar kecamatan, nama pejabat kepala kantor, tautan Google Sheets tabel wajib, dan berkas foto/desain kover.

---

## 2. Pemicu Onboarding (Activation Triggers)

Skill ini aktif apabila salah satu kondisi terpenuhi:
1. `config/regency.yaml` memiliki properti `is_template_default: true` atau belum ada (masih memakai `regency.example.yaml`).
2. Perintah `python3 scripts/kcda.py status` atau `python3 scripts/kcda.py validate` mengeluarkan peringatan:
   `🚨 PERINGATAN PLACEHOLDER TEMPLATE: Repositori ini saat ini masih menggunakan konfigurasi contoh (Kabupaten Mempawah).`
3. Pengguna meminta: *"Bantu saya siapkan publikasi KCDA untuk BPS [Nama Kabupaten/Kota]"*.

---

## 3. Alur Wawancara Interaktif (Interview Workflow)

Lakukan wawancara santai dan terstruktur kepada pengguna secara bertahap:

### Tahap 1: Identitas Daerah & Instansi
Tanyakan kepada pengguna:
1. **Nama Kabupaten / Kota**: contoh *"Kabupaten Sambas"* atau *"Kota Pontianak"*.
2. **Nama Bahasa Inggris**: contoh *"Sambas Regency"* atau *"Pontianak Municipality"*.
3. **Ibukota Kabupaten**: contoh *"Sambas"*.
4. **Alamat Kantor BPS & Kontak**: alamat jalan, telepon, email satker, dan website resmi BPS daerah.
5. **Kode Satker & Kode Wilayah BPS**: contoh kode wilayah 4-digit `6101` dan satker `61010`.

### Tahap 2: Metadata Pimpinan Kantor
Tanyakan identitas Kepala BPS yang menandatangani Kata Pengantar:
1. **Nama Lengkap & Gelar**: contoh *"Dr. Ir. Nama Pejabat, M.Si."*.
2. **NIP**: 18 digit NIP.
3. **Foto & Tanda Tangan**:
   - Minta pengguna meletakkan foto portrait transparan di `assets/kepala_bps.png`.
   - Minta tanda tangan transparan di `assets/ttd_kepala_bps.png`.

### Tahap 3: Daftar Kecamatan & Desa
Tanyakan daftar kecamatan di wilayah tersebut:
- Untuk setiap kecamatan:
  - Nama resmi & nama singkat.
  - Kode wilayah 7 digit (misal: `6101010`).
  - Nomor katalog & nomor publikasi.
  - Nama PIC / Koordinator Statistik Kecamatan (KSK/PML).
  - Ibukota kecamatan.
  - Daftar nama desa/kelurahan.
  - Berkas kover depan dan belakang di `assets/covers/`.

### Tahap 4: Sumber Data Google Sheets
Jelaskan kepada pengguna bahwa data tabel diinput melalui Google Sheets:
- Buka panduan skema di `config/tables_schema.json` atau `docs/GOOGLE_SHEETS_GUIDE.md`.
- Setiap tabel wajib memiliki spreadsheet dengan tab per nama kecamatan.
- Masukkan Google Sheet ID ke dalam `config/tables_schema.json` atau mapping konfigurasi.

---

## 4. Finalisasi Konfigurasi

Setelah informasi terkumpul:
1. Tulis perubahan ke `config/regency.yaml`.
2. **Ubah `is_template_default: false`** agar Placeholder Guard tidak lagi memunculkan peringatan.
3. Jalankan validasi diagnostik di terminal:
   ```bash
   python3 scripts/kcda.py validate
   ```
4. Jalankan kompilasi uji coba salah satu kecamatan:
   ```bash
   python3 scripts/kcda.py generate --kecamatan <slug-kecamatan>
   ```
5. Tunjukkan hasil PDF di `outputs/<slug-kecamatan>/` kepada pengguna!
