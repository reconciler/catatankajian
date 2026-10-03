# Instruksi Auditor — 3 Okt 2026 (aturan lintas-repo dan ekstraksi aturan)

Dari: sesi "Auditor Project" (`session_01V7K2gPxpghoLSqB74zsXWV`)
Untuk: sesi PIC `catatankajian`

Penanda: **[Terverifikasi]** = diperiksa Auditor langsung. **[Keputusan Amal]** = disampaikan Amal di chat Auditor.

## 1. Dasar
- **[Keputusan Amal]** 3 Okt 2026: bagian "Aturan lintas-repo" ditulis ke ketiga `CLAUDE.md`, dan tiap PIC diminta mengekstrak aturan berguna dari obrolannya dengan Amal.
- Instruksi ini tercatat di git sehingga boleh dieksekusi sesuai aturan "Eksekusi instruksi Auditor"; butir yang menyentuh `deploy.yml` tetap menunggu konfirmasi Amal di chat PIC.

## 2. Perubahan Auditor 3 Okt 2026 (atas keputusan Amal: "eksekusi semua usulanmu")

- `CLAUDE.md` mendapat bagian **"Aturan lintas-repo"** (13 butir; teks **identik** di ketiga repo, diverifikasi dengan diff).
  Baca bagian itu sebelum bekerja; ia berlaku sebagai aturan tetap.
- `CLAUDE.md` catatankajian diperbarui agar sesuai kenyataan: ditambah `lib/fuse.min.js` di Struktur, bagian baru **"Berkas yang tayang di situs (folder `_site`)"** (daftar berkas, uji pasca-deploy, batas verifikasi), dan catatan transparansi sumber untuk bio ustadz/kitab baru. Semua dicocokkan dengan `deploy.yml`.

### 2.1 Butir untuk PIC catatankajian
- **Butir A (dokumen, boleh langsung):** tugas ekstraksi di 2.3. Periksa juga bagian baru di `CLAUDE.md` terhadap `deploy.yml` dan koreksi bila ada yang keliru (Auditor menulisnya dari pembacaan workflow, bukan dari uji).
- **Butir B (menunggu "lanjut" Amal di chat PIC, menyentuh `deploy.yml`):** uji 404 pasca-terbit saat ini memeriksa daftar tetap (`CLAUDE.md`, `AUDIT-HANDOFF-2026-09-30.md`, `COORDINATION-NOTE-2026-09-22.md`, `scripts/build_seo.py`). Samakan dengan bikin-cv-taaruf: periksa **semua** `AUDIT-HANDOFF-*.md` dan `COORDINATION-NOTE-*.md` 404. Alasan: simetri (butir 9) dan handoff baru otomatis terjaga. Jangan melonggarkan uji lain.
- **Butir C (uji, boleh langsung):** jalankan axe-core di Chromium terhadap beranda dan satu halaman rekap (lebar 320 dan 430) sebagai garis dasar (butir 13). Laporkan temuan. Perbaikan yang hanya menambah atribut aksesibilitas tanpa efek visual boleh langsung dan dilaporkan; yang mengubah tampilan/fungsi menunggu Amal. Bila axe-core tidak bisa dipasang, katakan itu.

### 2.3. Tugas: ekstrak aturan berguna dari obrolan Anda dengan Amal

Amal meminta tiap PIC mengekstrak aturan dan keputusan yang berguna dari obrolannya dengan Anda dan belum tertulis
formal. Auditor sudah melakukannya untuk sesi Auditor dan dokumen di git; **chat langsung Amal dengan Anda tidak
terjangkau dari sesi Auditor**, jadi hanya Anda yang bisa melakukannya.

**Sumber:** seluruh riwayat percakapan sesi Anda dengan Amal (termasuk bagian sebelum pemadatan konteks), pesan
komit, dan handoff Anda.

**Yang dicari:** keputusan, aturan, atau preferensi Amal yang **berlaku ke depan** dan belum ada di `CLAUDE.md`
repo inidan dokumen lain. Abaikan keputusan sekali pakai yang sudah selesai dan status pekerjaan.

**Format tiap butir** (tabel di handoff Anda): aturan (satu kalimat) | sumber (kutipan pendek Amal + tanggal, atau
"praktik" bila belum diputuskan Amal) | cakupan (repo ini saja atau lintas-repo) | status (sudah tertulis di mana,
atau belum) | usulan teks (maksimal dua baris).

**Cara memproses:**
- Butir yang **keputusan eksplisit Amal dan khusus repo ini**: tambahkan langsung ke `CLAUDE.md` repo ini, ringkas
  (rincian panjang ke `docs/` bila repo punya), dan catat di handoff Anda.
- Butir **lintas-repo** atau yang hanya **praktik** (belum diputuskan Amal): jangan ditulis ke `CLAUDE.md`; cukup
  didaftar di handoff. Auditor yang menyatukan supaya bagian "Aturan lintas-repo" tetap identik di ketiga repo, lalu
  Amal memutuskan.
- Jangan mengubah kode atau workflow untuk tugas ini. Jaga `CLAUDE.md` tetap ringkas (tambahan sekitar 30 baris
  paling banyak).
- **Jangan menyalin data pribadi atau sensitif** (isi CV, kontak, kredensial, token); kutip seperlunya.

**Lapor:** commit ke repo (jalur utama). Beri tahu Auditor lewat pesan hanya sebagai tambahan.
