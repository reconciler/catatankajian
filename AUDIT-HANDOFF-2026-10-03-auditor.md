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

## 3. Instruksi 5 Okt 2026: aturan bersama baru + perbaikan visual axe-core

Dasar: **[Keputusan Amal]** 5 Okt 2026 (chat Auditor):
- Butir lintas-repo N1-N7 dan butir baru "bahasa campur ID+English, concise" **masuk** `CLAUDE.md`; N8 dan N9 tidak.
- Temuan visual axe-core: **langsung dieksekusi** (tampilan berubah; konfirmasi Amal sudah ada, tidak perlu tanya lagi).
- Bagian bersama baru di ketiga `CLAUDE.md` (diff identik): `Aturan lintas-repo` butir 14-19 + `Preferensi melapor`.
  Baca dan patuhi. Mulai sekarang tulis handoff/laporan dengan gaya itu (concise, simpel, spesifik, campur English).
- `CLAUDE.md` catatankajian: bagian `Preferensi melapor` ditambahkan (sebelumnya tidak ada di repo ini).

### 3.1 Tugas PIC catatankajian
1. **Perbaiki handoff PIC**: `AUDIT-HANDOFF-2026-10-03.md` bagian 3 masih menulis Butir B "menunggu konfirmasi", padahal komit
   `811ce74` sudah mengerjakannya (run #18 `success`). Koreksi.
2. **Kontras warna (`color-contrast`)**: beranda (26 elemen) dan rekap (21 elemen). Cari perubahan **minimal** yang mencapai
   >= 4.5:1 terhadap latar sebenarnya: `--muted` (`#6B7A8D`) dan chip tema (`--sage` di atas `rgba(74,124,89,.12)`).
   Pertahankan hue/nuansa; hanya gelapkan. Hitung kontras tiap pasangan (teks, latar) dan catat tabel before/after.
3. **Dua push, urut risiko** (aturan 6): (a) `index.html` dulu; (b) lalu `rekap/*.html` (file inti, banyak) via replace
   terskrip. Cek `build_seo.py` tetap tidak menghasilkan diff di blok SEO; sample 3 rekap + axe.
4. Re-run axe (320 + 430) di beranda + 1 rekap. Harapan: 0 pelanggaran. Sisa (gradien/overlap) cukup dilist.
5. Before/after screenshot; sebut "belum dilihat di perangkat nyata" (butir 11). Catat hasil + run di handoff PIC.

### 3.2 Keputusan Amal 5 Okt 2026 (chat Auditor): rekap tidak diubah

- Kontras warna `rekap/*.html` **tidak perlu diubah** (final). Tugas rekap di 3.1 dibatalkan. Dicatat di `CLAUDE.md` supaya tidak muncul lagi.
- Tidak ada tugas tersisa untuk catatankajian dari instruksi 5 Okt.
