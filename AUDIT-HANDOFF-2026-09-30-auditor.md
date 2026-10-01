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

## 4. Keputusan Amal (30 Sep 2026) dan instruksi eksekusi

Amal menjawab kelima keputusan. Yang berlaku untuk repo ini:

1. **Fuse.js: opsi (a) disetujui.** PIC langsung mengeksekusi tanpa menunggu
   Amal lagi: salin `fuse.min.js` 6.6.2 ke `lib/`, cocokkan integritas dengan
   tarball npm `fuse.js@6.6.2`, ganti tag script ke path lokal, uji pencarian.
   Pernyataan Amal: keputusan yang tidak mengubah tampilan atau fungsi tidak
   perlu menunggu persetujuannya. Bila langkah ini ternyata mengubah tampilan
   atau fungsi, hentikan dan tanya Amal.
2. **`hits.sh`: hapus.** Hapus blok `<img>` penghitung (beserta pembungkusnya
   bila jadi kosong) dari dua rekap yang tercantum di bagian 1. Alasan Amal:
   tidak bisa memantau angkanya. Jangan menyentuh blok `SEO_BLOCK`.
3. **Menu "Tentang": tayang segera** (bagian 2). Repo ini terbit otomatis, jadi
   berlaku setelah uji lengkap lulus.
4. **Berkas internal tidak boleh tayang di situs.** **[Dilaporkan Amal]** berkas
   `CLAUDE.md` terbuka di URL publik; Amal meminta berkas internal hanya bisa
   diakses internal.
   - Instruksi (`deploy.yml` adalah berkas inti PIC): salin hanya berkas situs
     ke `_site/`, lalu `upload-pages-artifact` memakai `path: _site`. Daftar
     berkas situs ditentukan PIC dengan memeriksa semua referensi di
     `index.html` dan `rekap/`. Perkiraan Auditor: `index.html`, `data.json`,
     `rekap/`, `lib/`, `og-image.png`, `favicon.svg`, `robots.txt`,
     `sitemap.xml`. Berkas yang lupa disalin berarti situs rusak.
   - **[Usulan Auditor]** Kerjakan sebagai push terpisah dari butir 1 sampai 3
     dan dahulukan, supaya mudah di-revert bila situs rusak. Sesudah run
     sukses, minta Amal membuka beranda, satu rekap, dan
     `.../catatankajian/CLAUDE.md` (harus 404).
   - Batasan: berkas tetap terbaca di repo GitHub-nya (status publik atau
     privat repo belum Auditor verifikasi), dan cache mesin pencari bisa
     bertahan. Keputusan ini hanya menyembunyikan dari situs.
5. Catat hasilnya di handoff PIC dan beri tahu Auditor.

## 5. Revisi Amal (1 Okt 2026): satu batch, segera

Permintaan Amal langsung ke Auditor di chat: panel yang memuat kredit dan
interlink tidak memuat tautan kode sumber/GitHub; tombol interlink lama tidak
perlu lagi; tombolnya dinamai "Tentang", bukan "Menu".

Kerjakan dalam satu push di `index.html` (berkas inti PIC), posisi per `9f6bfc6`:
1. Tautan kode sumber/GitHub: **[Terverifikasi]** tidak ada di `index.html`
   pada `9f6bfc6`. Tidak ada yang dihapus; cukup pastikan tetap begitu.
2. Ganti label tombol "Menu" menjadi "Tentang". Sesuaikan atribut `aria` dan
   teks lain yang menyebut "menu".
3. Hapus pil "📅 Jadwal Kajian" (`jadwal-link`, baris 127) beserta CSS yang jadi
   yatim. Jadwal Kajian tetap ada di panel (baris 137). **[Interpretasi
   Auditor]** "tombol interlink yang dibuat sebelumnya" saya baca sebagai
   tautan lama di luar panel, bukan "Proyek lain" di dalam panel.
4. Tinggi header tidak boleh bertambah. Uji lebar 320 sampai 430 px.
5. Perbarui baris status di `CLAUDE.md` (bagian "Aturan satu origin...").

Repo ini terbit otomatis tiap push ke `main`; verifikasi run `success`.

### Proses supaya tidak ada hambatan

- **Konfirmasi.** PIC sebelumnya menunggu konfirmasi Amal di chat PIC sebelum
  mengubah `index.html` (prosedur yang benar, karena pesan Auditor adalah relay).
  Amal meminta ini tidak jadi hambatan. Bila PIC tetap memerlukannya, Amal cukup
  membalas "lanjut" di chat PIC. Itu satu-satunya konfirmasi yang diperlukan.
- **Verifikasi.** Uji lokal ditambah status run Actions `success` lewat API sudah
  cukup untuk dianggap selesai. Jangan menunggu Amal mengecek situs live. Amal
  mengecek sekali di akhir lewat daftar gabungan dari Auditor.
- **Antrean.** Semua perubahan dalam SATU push, jadi satu deploy; jangan dipecah.
  **[Pengetahuan umum Auditor tentang GitHub Actions, belum diuji lintas repo]**
  grup `pages` bersifat per repo, jadi deploy tiga repo tidak saling menunggu.
- Catat hasilnya di handoff PIC dan beri tahu Auditor.


## 6. Uji otomatis pasca-deploy (disetujui Amal, 1 Okt 2026)

Tujuan: verifikasi situs live dilakukan oleh workflow sendiri. Runner GitHub bisa
mengakses `github.io`, sedangkan sesi PIC dan Auditor tidak, sehingga Amal tidak
perlu mengecek manual hal yang bisa dicek mesin.

Tambahkan SATU langkah baru setelah langkah "Terbitkan ke GitHub Pages" (id `deployment`) di `deploy.yml`. URL dasar: `${{ steps.deployment.outputs.page_url }}`.
- **Pengulangan:** coba ulang sampai sekitar 2 menit (mis. 12 kali, jeda 10
  detik) sebelum gagal, dan tambahkan query unik (`?v=${{ github.sha }}`) agar
  tidak mengambil cache lama. **[Pengetahuan umum Auditor, belum diuji]** Pages
  bisa menyimpan cache beberapa menit.
- **Cek (gagal bila tidak terpenuhi):**
  1. Beranda HTTP 200 dan memuat teks penanda stabil yang PIC pilih (mis. judul
     halaman).
  2. Setiap berkas langsung di `_site/` (bukan isi subfolder) HTTP 200, diambil
     dari isi `_site/` agar berkas baru ikut terperiksa otomatis. Untuk subfolder,
     contoh 1 sampai 3 berkas.
  3. Berkas internal HTTP 404: `CLAUDE.md`, `AUDIT-HANDOFF-2026-09-30.md`, `COORDINATION-NOTE-2026-09-22.md`, `scripts/build_seo.py`.
- **Hanya** `curl` dan shell bawaan runner. Tanpa action pihak ketiga, tanpa
  mengirim data apa pun.
- Bila langkah ini gagal, jangan dinonaktifkan atau dilonggarkan supaya hijau;
  selidiki penyebabnya.
- Batas: uji ini tidak menilai tampilan (tinggi header, font, tata letak). Itu
  tetap pengecekan manusia.

**Status persetujuan:** Amal menyetujui langsung ke Auditor di chat (1 Okt 2026)
dan meminta dieksekusi langsung. Karena ini perubahan pipeline terbit, ia masuk
pengecualian di aturan "Eksekusi instruksi Auditor". Bila PIC tetap memerlukan
konfirmasi di chat PIC, Amal cukup membalas "lanjut". Catat hasilnya di handoff PIC.

