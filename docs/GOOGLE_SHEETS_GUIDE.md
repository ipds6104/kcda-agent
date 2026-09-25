# Panduan Pengisian & Format Google Sheets untuk KCDA Agent

Dokumen ini ditujukan bagi **Tim Pengumpul Data / Mitra Statistik / PIC Publikasi BPS** untuk menyiapkan dan menyinkronkan data kecamatan ke dalam generator publikasi KCDA.

---

## 1. Konsep Dasar

Generator publikasi KCDA bekerja dengan membaca berkas JSON di `data/raw_tables/`. Berkas-berkas JSON ini dapat dihasilkan secara otomatis dari Google Sheets melalui modul sinkronisasi:
```bash
python3 scripts/kcda.py sync
```

---

## 2. Struktur Spreadsheet Google Sheets

Untuk setiap tabel yang ingin disinkronkan, buat **1 Google Spreadsheet** dengan aturan berikut:

1. **Satu Spreadsheet per Nomor Tabel**:
   - Contoh: Spreadsheet untuk *Tabel 1.1: Luas Daerah Menurut Desa/Kelurahan*.
2. **Nama Tab Sesuai Nama Kecamatan**:
   - Di dalam spreadsheet tersebut, buat tab sheet untuk setiap kecamatan.
   - Penamaan tab sheet menggunakan **Nama Singkat Kecamatan** (contoh: `Mempawah Hilir`, `Toho`, `Segedong`).
   - Sistem toleran terhadap spasi dan variasi huruf besar/kecil.
3. **Format Baris Tabel**:
   - **Baris 1**: Judul kolom tabel (Header Bahasa Indonesia).
   - **Baris 2**: Judul kolom tabel (Header Bahasa Inggris - opsional jika sudah ada di template).
   - **Baris 3**: Penomoran kolom `(1)`, `(2)`, `(3)`, dst.
   - **Baris 4 dan seterusnya**: Data per Desa/Kelurahan.
   - **Baris Terakhir**: Baris total atau jumlah.

---

## 3. Menghubungkan Google Sheet ke KCDA Agent

Buka berkas `config/tables_schema.json`. Setiap tabel memiliki entri seperti berikut:

```json
{
  "no": "1.1",
  "nama": "Luas Daerah Menurut Desa/Kelurahan",
  "wajib": true,
  "sheet_id": "1A2B3C4D5E6F7G8H9I0J..."
}
```

Cukup salin **Spreadsheet ID** dari URL Google Sheets Anda:
`https://docs.google.com/spreadsheets/d/`**`<SPREADSHEET_ID>`**`/edit`

Dan tempelkan ke properti `"sheet_id"`.

---

## 4. Hak Akses (Sharing Permissions)

Pastikan spreadsheet dapat diakses:
- **Opsi A (Rekomendasi Internal)**: Set sharing spreadsheet menjadi *"Anyone with the link can view"* (Siapa saja yang memiliki tautan dapat melihat).
- **Opsi B (Google Service Account / OAuth)**: Hubungkan token Google Drive API di environment sistem (`GOOGLE_ACCESS_TOKEN` atau skill `gdrive`).

---

## 5. Menjalankan Sinkronisasi

Setelah Sheet ID diisi, jalankan:
```bash
# Sinkronkan seluruh tabel yang terdaftar
python3 scripts/kcda.py sync

# Atau sinkronkan tabel tertentu saja
python3 scripts/kcda.py sync --tabel 1.1
```

Data akan langsung terunduh ke `data/raw_tables/` dan siap dikompilasi menjadi PDF buku!
