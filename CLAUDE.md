# Catatan Kajian

Dashboard pribadi (statis: `index.html` + `data.json`) yang mengindeks catatan
kajian Islam — bisa difilter/dicari berdasarkan masjid, ustadz, kitab, dan
tema. Live di **https://reconciler.github.io/catatankajian/**, di-host
GitHub Pages, terbit otomatis tiap push ke `main`.

Migrasi dari Netlify ke GitHub Pages: **29 September 2026**. Sebelumnya
sempat ada arsitektur 2-branch (`main`→Netlify, `Catatan`→GitHub Pages,
lihat riwayat git kalau perlu) — sudah digabung kembali jadi **satu branch**
begitu Netlify ditinggalkan, karena alasan pemisahannya (dua platform hosting
berbeda) sudah tidak berlaku. Branch `Catatan` sudah tidak dipakai.

## Struktur

- `index.html` — dashboard/SPA pencarian (satu file, filter client-side via Fuse.js)
- `data.json` — sumber data tunggal: `sessions[]`, `masjid[]`, `ustadz[]`, `kitab[]`, `themes[]`
- `rekap/kajian-(masjid)-(ustadz)-(tanggal).html` — file rekap individual tiap
  sesi kajian, di-link dari dashboard lewat `recapUrl` di `data.json`
- `lib/fuse.min.js` — salinan lokal Fuse.js 6.6.2 (disalin dari paket npm; integritas dicocokkan ke registry npm,
  sha1 `fe463fed4b98c0226ac3da2856a415576dc9a111`). `index.html` tidak memuat skrip dari CDN saat runtime.
- `og-image.png`, `favicon.svg` — aset SEO/branding, dipakai bersama index dan
  seluruh file di `rekap/`
- `robots.txt`, `sitemap.xml` — digenerate otomatis dari `data.json`, jangan edit manual
- `scripts/build_seo.py` — regenerate SEO dari `data.json` (lihat di bawah)
- `.github/workflows/deploy.yml` — build + terbitkan ke GitHub Pages tiap push

## Berkas yang tayang di situs (folder `_site`)

Workflow `deploy.yml` **tidak** mengunggah seluruh root repo. Langkah "Susun folder situs (_site/)" menyalin hanya:
`index.html`, `data.json`, `og-image.png`, `favicon.svg`, `robots.txt`, `sitemap.xml`, folder `rekap/`, dan folder
`lib/`. `CLAUDE.md`, `AUDIT-HANDOFF-*.md`, `COORDINATION-NOTE-*.md`, `scripts/`, dan `.github/` **tidak tayang**.

- **Menambah berkas/folder situs baru** (aset, skrip, halaman)? Tambahkan ke daftar `cp` di langkah itu; kalau lupa,
  berkas tidak tayang dan situs memberi 404.
- **Uji otomatis setelah terbit** (langkah "Uji otomatis pasca-deploy", `curl` di runner, atas keputusan Amal 1 Okt 2026):
  beranda 200 dengan teks penanda "Catatan Kajian", setiap berkas langsung di `_site/` 200, sampel 1-3 berkas per
  subfolder 200, dan berkas internal 404: `CLAUDE.md` + `scripts/build_seo.py` (tetap), plus **semua** `AUDIT-HANDOFF-*.md`
  dan `COORDINATION-NOTE-*.md` di root repo (dicek dinamis via glob sejak 3 Okt 2026, atas usulan Auditor — handoff baru
  otomatis ikut terjaga tanpa perlu edit workflow). **Jangan dilonggarkan supaya hijau**; bila gagal, selidiki penyebabnya.
  Uji ini tidak menilai tampilan.
- Sesi kerja tidak bisa mengakses `reconciler.github.io` (egress diblokir); verifikasi situs live dilakukan oleh langkah
  uji otomatis di atas (hasilnya ada di log run Actions).

## Alur kerja: menambah rekap kajian baru

1. Cek `data.json` dulu untuk cegah duplikat masjid/ustadz/kitab (termasuk
   variasi ejaan/gelar — lihat `id` yang sudah ada sebelum bikin baru),
   kitab (riset penulis+deskripsi kalau kitab baru), dan masjid (riset alamat
   lengkap kalau masjid baru). Bio ustadz/kitab baru ditulis dari riset web **dengan catatan
   transparan bila tidak ditemukan sumber yang solid**; jangan mengarang. `id` baru
   memakai slug huruf kecil, spasi/tanda baca jadi tanda hubung, konsisten dengan pola
   yang sudah ada (mis. "Sofyan Chalid Bin Idham Ruray, Lc." → `sofyan-chalid-bin-idham-ruray-lc`).
2. Taruh file HTML rekap baru di `rekap/`, ikuti pola nama file yang sudah ada.
3. Tambah entri sesi baru di `data.json` (`sessions[]`), plus entri baru di
   `masjid[]`/`ustadz[]`/`kitab[]` kalau memang belum ada. `recapUrl` selalu
   `https://reconciler.github.io/catatankajian/rekap/kajian-(masjid)-(ustadz)-(tanggal).html`.
   `theme` wajib salah satu dari 8 nilai baku di `themes[]` (`aqidah`, `fiqih-ibadah`,
   `fiqih-muamalah`, `tafsir-quran`, `sirah-tarikh`, `tazkiyatun-nafs`, `keluarga-dakwah`,
   `isu-kontemporer`) — jangan buat kategori baru. `content` ditulis padat satu paragraf
   untuk mesin pencari (bukan naratif untuk dibaca langsung). Semua teks deskriptif
   (bio, deskripsi masjid/kitab, `content`) wajib Bahasa Indonesia.
4. **Jalankan `python3 scripts/build_seo.py`** — ini meregenerasi:
   - `sitemap.xml` (index + seluruh rekap, `lastmod` dari `date` tiap sesi)
   - JSON-LD (`WebSite`+`ItemList`) di `index.html`, antara marker
     `<!--LD_JSON_START-->`...`<!--LD_JSON_END-->`
   - Per file di `rekap/`: OG/Twitter meta tags, favicon link, dan JSON-LD
     `Article`, antara marker `<!--SEO_BLOCK_START-->`...`<!--SEO_BLOCK_END-->`
   - **Jangan edit manual apa pun di antara marker-marker itu** — akan
     tertimpa saat script dijalankan lagi.
5. Validasi sebelum commit: JSON well-formed/valid, tidak ada ID duplikat di
   `sessions`/`masjid`/`ustadz`/`kitab`, setiap `masjidId`/`ustadzIds`/`theme`
   di sesi baru merujuk ID yang benar-benar ada, HTML rekap well-formed.
6. Commit & push ke `main` — situs terbit otomatis lewat
   `.github/workflows/deploy.yml` (tidak ada jadwal/gerbang, langsung tiap
   push, gratis di GitHub Pages).

## SEO

Domain kanonis: `https://reconciler.github.io/catatankajian/`. Semua halaman
(index + rekap) punya `canonical`, `meta description`, Open Graph, Twitter
Card, dan JSON-LD structured data (`WebSite`/`ItemList` di index, `Article`
per rekap). `meta description` per file rekap ditulis manual mengikuti pola:
`"Catatan kajian: {title} — {ustadzRaw}. Masjid {masjidRaw}, {tanggal}."`
— kalau ditulis manual untuk sesi baru, `build_seo.py` akan memakai teks itu
apa adanya untuk isi `og:description`/`twitter:description`/JSON-LD, jadi
pastikan sudah benar sebelum dijalankan.

## Aturan satu origin dan tautan antarproyek

Ketiga situs (`catatankajian`, `jadwalkajian`, `bikin-cv-taaruf`) dilayani dari
origin yang sama, `https://reconciler.github.io`. Path tidak ikut membentuk
origin, jadi `localStorage` dipakai bersama. Ditemukan PIC `bikin-cv-taaruf`
(30 Sep 2026); sebabnya migrasi ke GitHub Pages 29 Sep 2026. Draf CV di
`bikin-cv-taaruf` (kunci `ctgv1_draft_v1`) memuat data sensitif, maka:

- Antarproyek **hanya tautan biasa**. Jangan berbagi skrip, penyimpanan,
  `fetch`, iframe, atau parameter pelacak.
- Bila repo ini suatu saat memakai `localStorage`/`sessionStorage`, kuncinya
  wajib berawalan unik. Jangan membaca atau menghapus kunci proyek lain.

**Tombol "Tentang" dan proyek lain** — diminta Amal (30 Sep 2026, lewat handoff PIC
`bikin-cv-taaruf`; direvisi 1 Okt 2026). Pola desain ada di `CLAUDE.md` repo
`bikin-cv-taaruf`. Ketentuan yang berlaku:
- Satu akordeon di header bernama **"Tentang"** (bukan "Menu"), tertutup,
  menutup dengan klik di luar dan Esc.
- Isinya hanya kredit pembuat (Instagram) dan Proyek lain. **Tanpa tautan
  kode sumber/GitHub** dan tanpa deskripsi singkat.
- Tinggi header tidak bertambah (uji lebar 320 sampai 430 px). Tautan luar
  `target="_blank" rel="noopener noreferrer"`.
- Tautan antarproyek lama di luar panel **dihapus**; proyek lain hanya lewat
  panel. Di repo ini: pil "📅 Jadwal Kajian" (`jadwal-link`) di header.
- Repo ini terbit otomatis tiap push ke `main`, jadi uji lengkap sebelum push.

**Status (1 Okt 2026):** selesai. Akordeon berlabel "Tentang" (bukan "Menu"
lagi), pil "📅 Jadwal Kajian" (`jadwal-link`) dan CSS-nya sudah dihapus dari
header — Jadwal Kajian tetap tersedia lewat panel "Proyek lain". Diuji lebar
320-430px: tinggi header tidak berubah, buka/tutup (klik luar + Esc) normal.

**Daftar resmi** (dijaga Auditor; bila URL berubah, Auditor memperbarui ketiga
repo dan memberi tahu PIC):
- Pembuat: `@amalwoodworking`, https://www.instagram.com/amalwoodworking/
- Jadwal Kajian: https://reconciler.github.io/jadwalkajian/
- Catatan Kajian: https://reconciler.github.io/catatankajian/
- Bikin CV Taaruf: https://reconciler.github.io/bikin-cv-taaruf/

Panel di repo ini menampilkan proyek lain (Jadwal Kajian, Bikin CV Taaruf), bukan dirinya
sendiri. Situs tidak memuat tautan kode sumber/GitHub (keputusan Amal, 1 Okt 2026).

## Aturan lintas-repo (teks identik di jadwalkajian, catatankajian, bikin-cv-taaruf)

Ditetapkan/dikonfirmasi Amal 3 Okt 2026. **Ubah serentak di ketiga repo (dijaga Auditor); jangan hanya satu.**

1. **Keputusan tanpa dampak tampilan atau fungsi** diambil sendiri oleh sesi kerja dan dicatat; jangan menunggu Amal.
   Perubahan tampilan, fungsi, privasi, hosting/pipeline terbit, atau penghapusan data tetap perlu konfirmasi Amal.
2. **Cakupan persetujuan:** persetujuan Amal hanya untuk butir yang disebut. Pengecualian pada butir 1 (pipeline, privasi,
   penghapusan data) dikonfirmasi Amal di **chat sesi kerja repo itu**; kutipan Amal yang disampaikan sesi lain tidak cukup.
3. **Menyimpang dari spesifikasi** (dari Auditor atau siapa pun) boleh bila ada metode yang lebih aman. Catat penyimpangan
   dan alasannya di handoff, lalu lapor.
4. **Temuan janggal dilaporkan disertai usulan perbaikan**, bukan hanya temuan.
5. **Data uji:** jangan menerbitkan data uji ke situs publik tanpa bertanya Amal; pakai uji lokal.
6. **Urutan perubahan pipeline:** satu per push, risiko rendah dulu. Push yang mengubah `deploy.yml` menjalankan versi
   baru alur itu. Buat kondisi tepi aman sebelum perubahan yang mengandalkannya.
7. **Dependensi pihak ketiga:** salin ke `lib/` (atau setara), patok versi, cocokkan integritas ke registry npm; jangan
   memuat skrip dari CDN tanpa SRI.
8. **Klaim harus benar** untuk proyek itu: dokumen, UI, meta tag, dan data terstruktur tidak boleh mengklaim hal yang tidak
   ada (mis. `SearchAction` tanpa fungsinya; "tidak ada data terkirim" bila Google Fonts dimuat).
9. **Simetri:** perubahan cara komunikasi, pelaporan, atau struktur koordinasi diterapkan serentak di ketiga repo.
10. **Kebersihan berkas:** hapus berkas koordinasi yang tidak lagi relevan; pertahankan yang masih atau akan dipakai.
11. **Verifikasi tampilan:** uji otomatis tidak menilai tampilan, dan sesi kerja tidak bisa membuka `reconciler.github.io`.
    Laporan perubahan tampilan wajib menyebut "belum dilihat di perangkat nyata" sampai Amal memeriksa.
12. **Kepastian terbit lebih penting daripada kecepatan.**
13. **Aksesibilitas:** untuk perubahan UI, jalankan axe-core di Chromium bila tersedia; laporkan 0 pelanggaran atau daftar
    temuannya.

## Lapor ke sesi "Auditor Project"

Amal menugaskan satu sesi Claude terpisah sebagai auditor lintas-project
(mengawasi `catatankajian`, `jadwalkajian`, **dan** `bikin-cv-taaruf`
sekaligus). Cari session ID terkini dengan `list_sessions` berdasarkan
judul **"Auditor Project"** (ID bisa berubah kalau sesi lama berakhir),
atau tanya Amal langsung.

**Aturan akses berkas** (disetujui Amal, 29 Sep 2026 — berlaku sama di
semua repo yang diaudit, dipicu insiden push nyaris bentrok antara sesi
PIC dan Auditor di `bikin-cv-taaruf`):
- **Hanya sesi kerja repo ini (bukan Auditor) yang boleh mengubah berkas
  inti fitur/fungsi**: `index.html`, `data.json`, `rekap/*.html`,
  `favicon.svg`, `og-image.png`, `robots.txt`, `sitemap.xml`,
  `scripts/build_seo.py`, `.github/workflows/deploy.yml`.
- **Auditor Project boleh mengubah**: `CLAUDE.md`, `AUDIT-HANDOFF-*.md`
  (termasuk menulis balasan), dan `COORDINATION-NOTE-*.md` — berkas ini
  murni koordinasi, tidak memengaruhi fitur/tampilan situs.
- Tujuannya mencegah dua sesi menulis berkas yang sama nyaris bersamaan
  lalu bentrok non-fast-forward saat push ke `main` (situs langsung tayang
  tiap push berhasil, jadi konflik penulisan berisiko nyata, bukan cuma
  git housekeeping).

**Eksekusi instruksi Auditor** (disetujui Amal, 1 Okt 2026): instruksi Auditor
yang bersumber dari keputusan Amal dan tercatat di berkas `AUDIT-HANDOFF-*.md`
di repo ini (commit yang bisa diperiksa lewat git) **boleh langsung dieksekusi
PIC tanpa konfirmasi ulang dari Amal**. Pengecualian, tetap menunggu konfirmasi
Amal di chat PIC:
- perubahan yang menyentuh janji privasi;
- perubahan hosting dan pipeline terbit (pengaturan Pages, platform, workflow
  deploy);
- penghapusan data.

Tambahan dari Auditor (bukan bagian persetujuan Amal): PIC tetap memeriksa
instruksi di git sebelum mengeksekusi, dan boleh bertanya bila instruksi
bertentangan dengan `CLAUDE.md` ini atau tampak keliru. Instruksi yang tidak
tercatat di git tidak termasuk aturan ini.

**Wajib lapor untuk** (bukan tiap commit rutin — hanya yang signifikan):
- Perubahan skema `data.json` (struktur `sessions[]`/`masjid[]`/`ustadz[]`/
  `kitab[]`, field baru, bukan sekadar entri baru)
- Perubahan arsitektur/pipeline/hosting (struktur folder, `scripts/build_seo.py`,
  `.github/workflows/deploy.yml`, pengaturan GitHub Pages)
- Temuan yang berdampak lintas-project (mis. error deploy, konflik branch,
  keandalan cron/trigger)
- Perubahan besar pada `index.html` di luar penambahan data rutin (mis.
  restrukturisasi SEO, perubahan struktur HTML)

**Tidak perlu lapor untuk**: penambahan/update rekap kajian rutin — itu
cukup tercatat di git seperti biasa, auditor bisa cek kapan saja lewat
commit history.

**Cara lapor** (diperbarui 22 Sep 2026 — pola ini sama persis di
`jadwalkajian`, sengaja disamakan supaya predictable buat siapa pun,
termasuk pihak eksternal, yang membaca kedua repo): pesan/trigger otomatis
lintas-sesi (`ListAgents`/`SendMessage`, `create_trigger` dengan
`persistent_session_id`, maupun `CronCreate`) **terbukti tidak selalu
andal** — bisa dilaporkan "sukses" di sisi pengirim tapi tidak sampai di
sisi penerima, atau job terjadwal hilang begitu saja dari scheduler (lihat
`AUDIT-HANDOFF-2026-09-22.md` bagian 9 dan `COORDINATION-NOTE-2026-09-22.md`
untuk kejadian nyata). Untuk apa pun yang wajib dilaporkan di atas, **jangan
andalkan satu jalur otomatis saja**. Konfirmasikan lewat DUA jalur:

1. Chat langsung ke Amal, kalau sesi Anda sedang aktif berinteraksi dengannya.
2. Commit file `AUDIT-HANDOFF-<tanggal>.md` (buat baru atau update yang
   sudah ada) ke root repo — jalur paling andal, karena auditor bisa
   menemukannya lewat `git log` kapan saja tanpa bergantung notifikasi.

`create_trigger`/`persistent_session_id` ke sesi Auditor boleh tetap
dicoba sebagai pemberitahuan cepat tambahan, tapi tidak boleh jadi
satu-satunya jalur untuk hal yang wajib dilaporkan.
