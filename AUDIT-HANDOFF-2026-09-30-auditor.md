# Audit handoff — 2026-09-30 (balasan Auditor)

Dari: sesi "Auditor Project" (`session_01V7K2gPxpghoLSqB74zsXWV`)
Untuk: sesi PIC `catatankajian`
Konteks: `AUDIT-HANDOFF-2026-09-30.md` dari PIC `bikin-cv-taaruf` (bagian 4 sampai 6).
Amal meminta Auditor memeriksa pembaruan repo itu dan mengoordinasikannya ke
PIC lain.

Penanda: **[Terverifikasi]** = diperiksa langsung Auditor lewat git, API GitHub,
atau grep. **[Usulan Auditor]** = penilaian Auditor, belum divalidasi sumber luar
dan belum disetujui Amal. **[Belum terverifikasi]** = tidak bisa diperiksa dari
sesi Auditor.

## 1. Hasil audit repo ini: risiko satu origin

Latar: ketiga situs berbagi origin `https://reconciler.github.io`, jadi
`localStorage` dipakai bersama. Draf CV di `bikin-cv-taaruf` (kunci
`ctgv1_draft_v1`) memuat data kesehatan dan status pernikahan.

- **[Terverifikasi]** `index.html` baris 24 memuat
  `https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.min.js` tanpa atribut
  `integrity` dan `crossorigin`. Ini satu-satunya skrip pihak ketiga di repo ini,
  dan ia berjalan di origin yang sama dengan draf CV.
- **[Terverifikasi]** `fetch('data.json')` (baris 177) same-origin. Tidak ada
  pemakaian `localStorage`/`sessionStorage`/`indexedDB` di `index.html` maupun
  di seluruh `rekap/`. Tidak ada `<script src>` atau `<iframe>` di `rekap/`.
- **[Terverifikasi]** Dua rekap memuat gambar penghitung pengunjung dari
  `hits.sh` lewat `<img>`: `kajian-alhikmah-ddn2-maksum-20-juni-2026.html`
  (baris 744) dan `kajian-darussalam-gta-arif-21-juni-2026.html` (baris 408).
  Gambar tidak menjalankan skrip di origin kita, tetapi IP dan Referer
  pengunjung terlihat oleh `hits.sh`.
- **[Usulan Auditor]** Risiko Fuse.js: versi dipatok persis (6.6.2), sehingga
  kemungkinan disusupi kecil. Dampaknya besar bila terjadi, karena skrip itu bisa
  membaca draf CV. Penilaian ini pengetahuan umum Auditor, tidak dicek ulang ke
  sumber sesi ini. Preseden: PIC `bikin-cv-taaruf` menutup risiko serupa untuk
  jsPDF dengan menyalin file ke repo (`lib/`) setelah mencocokkan integritas
  tarball npm.
- **[Usulan Auditor]** Dua opsi, menunggu keputusan Amal (jangan diubah sebelum itu):
  (a) salin `fuse.min.js` 6.6.2 ke `lib/`, cocokkan integritas dengan tarball npm,
  ganti tag script ke path lokal. Ini yang Auditor sarankan: menghapus
  ketergantungan runtime pada CDN. (b) Tambah `integrity` dan
  `crossorigin="anonymous"` pada tag jsDelivr.
- `hits.sh`: pertahankan atau hapus, keputusan Amal dan PIC. Bila dipertahankan,
  klaim "tanpa analitik" tidak boleh dipakai untuk situs ini.

## 2. Permintaan: pasang menu "Tentang" (pola dari bikin-cv-taaruf)

- Sumber: handoff PIC `bikin-cv-taaruf` bagian 5, yang menyatakan Amal meminta
  pola ini diduplikat. Auditor meneruskannya atas permintaan Amal untuk
  mengoordinasikan pembaruan itu. Bila Amal di sesi Anda menyatakan lain,
  arahan Amal yang berlaku.
- Pola lengkap dan alasan desain ada di `CLAUDE.md` `bikin-cv-taaruf`. Ringkasan
  dan daftar resmi ada di `CLAUDE.md` repo ini.
- Yang diminta dari PIC (`index.html` adalah berkas inti PIC):
  1. Satu akordeon "Menu" di header, tertutup, menutup dengan klik di luar dan Esc.
     Isi berurutan: bagian khusus proyek (bila ada), Tentang, Proyek lain. Tanpa
     deskripsi singkat.
  2. Tinggi header tidak bertambah. Uji di lebar 320 sampai 430 px dengan font asli.
  3. Hanya tautan biasa. Tautan luar memakai `target="_blank" rel="noopener noreferrer"`.
  4. Pil ke Jadwal Kajian yang sudah ada di header: dipertahankan atau dilebur ke
     menu, putuskan bersama Amal.
  5. URL Instagram di `index.html` saat ini `https://instagram.com/amalwoodworking`;
     daftar resmi memakai `https://www.instagram.com/amalwoodworking/`.
- **Penting:** repo ini terbit otomatis di setiap push ke `main`. Uji lengkap
  sebelum push (seperti pola `bikin-cv-taaruf`: Chromium headless, header 320
  sampai 430 px, tanpa geser horizontal).
- **[Usulan Auditor, opsional]** Jalankan pemeriksaan aksesibilitas otomatis
  (mis. axe-core lewat Playwright). PIC `bikin-cv-taaruf` menemukan 61 kolom
  isian tanpa nama yang terbaca pembaca layar di aplikasinya; perbaikannya
  hanya atribut.
- Setelah selesai, catat hasilnya di berkas `AUDIT-HANDOFF-<tanggal>.md` milik PIC
  supaya Auditor bisa memverifikasi lewat git.

## 3. Temuan tambahan (rendah, perlu keputusan Amal, jangan diubah dulu)

- **[Terverifikasi]** `deploy.yml` baris 48: `upload-pages-artifact` dengan
  `path: "."`. Seluruh isi root repo ikut artifact Pages, termasuk `CLAUDE.md`,
  `AUDIT-HANDOFF-*.md`, `COORDINATION-NOTE-*.md`, dan `scripts/`.
- **[Belum terverifikasi]** Apakah berkas itu benar terlayani di URL publik. Akses
  ke `reconciler.github.io` diblokir dari sesi Auditor. Amal bisa mengecek dengan
  membuka `https://reconciler.github.io/catatankajian/CLAUDE.md` di browser.
- Sumbernya migrasi Auditor (`1b1b978`), bukan PIC. Menunggu keputusan Amal.
  **[Usulan Auditor]** Bila Amal ingin berkas itu tidak tayang: langkah workflow
  menyalin hanya berkas situs ke folder `_site/` dan mengunggah folder itu.
