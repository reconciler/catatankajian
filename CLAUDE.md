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
- `og-image.png`, `favicon.svg` — aset SEO/branding, dipakai bersama index dan
  seluruh file di `rekap/`
- `robots.txt`, `sitemap.xml` — digenerate otomatis dari `data.json`, jangan edit manual
- `scripts/build_seo.py` — regenerate SEO dari `data.json` (lihat di bawah)
- `.github/workflows/deploy.yml` — build + terbitkan ke GitHub Pages tiap push

## Alur kerja: menambah rekap kajian baru

1. Cek `data.json` dulu untuk cegah duplikat masjid/ustadz/kitab (termasuk
   variasi ejaan/gelar — lihat `id` yang sudah ada sebelum bikin baru)
   dan kitab (riset penulis+deskripsi kalau kitab baru).
2. Taruh file HTML rekap baru di `rekap/`, ikuti pola nama file yang sudah ada.
3. Tambah entri sesi baru di `data.json` (`sessions[]`), plus entri baru di
   `masjid[]`/`ustadz[]`/`kitab[]` kalau memang belum ada. `recapUrl` selalu
   `https://reconciler.github.io/catatankajian/rekap/kajian-(masjid)-(ustadz)-(tanggal).html`.
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

**Menu "Tentang" dan proyek lain** — diminta Amal (30 Sep 2026, lewat handoff PIC
`bikin-cv-taaruf`). Pola lengkap dan alasan desainnya ada di `CLAUDE.md` repo
`bikin-cv-taaruf`. Ringkas: satu akordeon "Menu" di header (tertutup, menutup
dengan klik di luar dan Esc), isi berurutan bagian khusus proyek, Tentang,
Proyek lain; tanpa deskripsi singkat; tinggi header tidak bertambah (uji lebar
320 sampai 430 px); tautan luar `target="_blank" rel="noopener noreferrer"`.
**Status: belum dipasang di repo ini.** Yang memasang PIC repo ini
(`index.html` berkas inti). Repo ini terbit otomatis tiap push ke `main`, jadi
uji lengkap sebelum push.

**Daftar resmi** (dijaga Auditor; bila URL berubah, Auditor memperbarui ketiga
repo dan memberi tahu PIC):
- Pembuat: `@amalwoodworking`, https://www.instagram.com/amalwoodworking/
- Jadwal Kajian: https://reconciler.github.io/jadwalkajian/
- Catatan Kajian: https://reconciler.github.io/catatankajian/
- Bikin CV Taaruf: https://reconciler.github.io/bikin-cv-taaruf/
- Kode sumber repo ini: https://github.com/reconciler/catatankajian

Menu di repo ini menampilkan proyek lain (Jadwal Kajian, Bikin CV Taaruf),
bukan dirinya sendiri. Pil Jadwal Kajian yang sudah ada di header boleh tetap; standardisasi bentuknya
diputuskan PIC bersama Amal.

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
