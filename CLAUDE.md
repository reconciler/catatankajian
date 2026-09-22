# Catatan Kajian

Dashboard pribadi (statis: `index.html` + `data.json`) yang mengindeks catatan
kajian Islam — bisa difilter/dicari berdasarkan masjid, ustadz, kitab, dan
tema. Live di **catatankajian.netlify.app**, deploy otomatis dari repo ini via
Netlify (mingguan, Jumat).

## Dua branch, dua publikasi terpisah

- **`main`** → Netlify (`catatankajian.netlify.app`) — dashboard saja:
  `index.html`, `data.json`, `robots.txt`, `sitemap.xml`, `favicon.svg`,
  `og-image.png`, `scripts/`. **Tidak ada file `kajian-*.html` di sini.**
- **`Catatan`** → GitHub Pages (`reconciler.github.io/catatankajian`) — seluruh
  file rekap individual `kajian-(masjid)-(ustadz)-(tanggal).html`, flat di
  root branch itu, plus `robots.txt`/`sitemap.xml` miliknya sendiri (domain
  GitHub Pages, bukan Netlify).

Kedua branch independen — bukan fast-forward satu sama lain. `data.json` di
`main` adalah satu-satunya sumber kebenaran untuk metadata sesi (termasuk
`recapUrl`, yang selalu memakai domain GitHub Pages); isi HTML rekap aktualnya
tinggal di `Catatan`.

`og-image.png` dan `favicon.svg` **hanya ada di `main`** — file rekap di
`Catatan` mereferensikannya lewat URL absolut ke Netlify
(`https://catatankajian.netlify.app/og-image.png` dst.), bukan path relatif,
supaya tidak salah resolve di GitHub Pages project site.

## Struktur (`main`)

- `index.html` — dashboard/SPA pencarian (satu file, filter client-side via Fuse.js)
- `data.json` — sumber data tunggal: `sessions[]`, `masjid[]`, `ustadz[]`, `kitab[]`, `themes[]`
- `og-image.png`, `favicon.svg` — aset SEO/branding, dipakai bersama (termasuk oleh file rekap di branch `Catatan`)
- `robots.txt`, `sitemap.xml` — digenerate otomatis dari `data.json`, jangan edit manual
- `scripts/build_seo.py` — regenerate SEO dari `data.json` (lihat di bawah)

## Alur kerja: menambah rekap kajian baru

1. Cek `data.json` dulu untuk cegah duplikat masjid/ustadz/kitab (termasuk
   variasi ejaan/gelar — lihat `id` yang sudah ada sebelum bikin baru)
   dan kitab (riset penulis+deskripsi kalau kitab baru).
2. Tambah entri sesi baru di `data.json` (`sessions[]`), plus entri baru di
   `masjid[]`/`ustadz[]`/`kitab[]` kalau memang belum ada. `recapUrl` selalu
   `https://reconciler.github.io/catatankajian/kajian-(masjid)-(ustadz)-(tanggal).html`.
3. **Di `main`**: jalankan `python3 scripts/build_seo.py` — meregenerasi
   `sitemap.xml` dan JSON-LD (`WebSite`+`ItemList`) di `index.html` (antara
   marker `<!--LD_JSON_START-->`...`<!--LD_JSON_END-->`), memakai `recapUrl`
   apa adanya dari `data.json` (domain GitHub Pages, bukan direkonstruksi).
   Commit & push ke `main` (lewat PR, jangan langsung ke `main`).
4. **Di branch `Catatan`** (checkout/worktree terpisah): taruh file HTML
   rekap baru, lalu jalankan `python3 scripts/build_seo.py` dari situ juga
   (fungsi `build_kajian_pages` akan mengisi OG/Twitter/JSON-LD `Article` per
   file rekap yang ada di direktori tsb, antara marker
   `<!--SEO_BLOCK_START-->`...`<!--SEO_BLOCK_END-->`) — **tapi `scripts/`
   sendiri tidak di-commit ke `Catatan`**, cukup dijalankan dari checkout
   `main` yang di-point ke direktori kerja `Catatan` (atau salin script itu
   sementara). Commit & push ke `Catatan` terpisah dari `main`.
5. **Jangan edit manual apa pun di antara marker `SEO_BLOCK`/`LD_JSON`** — akan
   tertimpa saat script dijalankan lagi.
6. Validasi sebelum commit (di kedua branch): JSON well-formed/valid, tidak
   ada ID duplikat di `sessions`/`masjid`/`ustadz`/`kitab`, setiap
   `masjidId`/`ustadzIds`/`theme` merujuk ID yang benar-benar ada, HTML rekap
   well-formed.

## SEO

Domain kanonis dashboard: `https://catatankajian.netlify.app`. Domain kanonis
tiap file rekap: `https://reconciler.github.io/catatankajian/...` (bukan
Netlify — ini beda dari `main` itu sendiri, karena file rekap secara fisik
tinggal di branch `Catatan`/GitHub Pages).

Semua halaman (index di `main` + rekap di `Catatan`) punya `canonical`,
`meta description`, Open Graph, Twitter Card, dan JSON-LD structured data
(`WebSite`/`ItemList` di index, `Article` per rekap). `meta description` per
file rekap ditulis manual mengikuti pola:
`"Catatan kajian: {title} — {ustadzRaw}. Masjid {masjidRaw}, {tanggal}."`
— kalau ditulis manual untuk sesi baru, `build_seo.py` akan memakai teks itu
apa adanya untuk isi `og:description`/`twitter:description`/JSON-LD, jadi
pastikan sudah benar sebelum dijalankan.

## Lapor ke sesi "Auditor project kajian"

Amal menugaskan satu sesi Claude terpisah sebagai auditor lintas-project
(mengawasi `catatankajian` **dan** `jadwalkajian` sekaligus — kredit Netlify
kedua situs dipakai bersama, lihat bagian kredit di `AUDIT-HANDOFF-*.md`).
Cari session ID terkini dengan `list_sessions` berdasarkan judul
**"Auditor project kajian"** (ID bisa berubah kalau sesi lama berakhir),
atau tanya Amal langsung.

**Wajib lapor untuk** (bukan tiap commit rutin — hanya yang signifikan):
- Perubahan skema `data.json` (struktur `sessions[]`/`masjid[]`/`ustadz[]`/
  `kitab[]`, field baru, bukan sekadar entri baru)
- Perubahan arsitektur/pipeline (pembagian `main`↔`Catatan`,
  `scripts/build_seo.py`, penambahan `netlify.toml`/workflow deploy)
- Temuan yang berdampak lintas-project (mis. isu kredit Netlify, error
  deploy, konflik branch, keandalan cron/trigger)
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
