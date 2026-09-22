# Catatan Kajian

Dashboard pribadi (statis: `index.html` + `data.json`) yang mengindeks catatan
kajian Islam — bisa difilter/dicari berdasarkan masjid, ustadz, kitab, dan
tema. Live di **catatankajian.netlify.app**, deploy otomatis dari repo ini via
Netlify (mingguan, Jumat).

## Struktur

- `index.html` — dashboard/SPA pencarian (satu file, filter client-side via Fuse.js)
- `data.json` — sumber data tunggal: `sessions[]`, `masjid[]`, `ustadz[]`, `kitab[]`, `themes[]`
- `kajian-(masjid)-(ustadz)-(tanggal).html` — rekap individual tiap sesi kajian, flat di root, di-link dari dashboard
- `og-image.png`, `favicon.svg` — aset SEO/branding, dipakai bersama di semua halaman
- `robots.txt`, `sitemap.xml` — digenerate otomatis, jangan edit manual
- `scripts/build_seo.py` — regenerate SEO dari `data.json`

## Alur kerja: menambah rekap kajian baru

1. Cek `data.json` dulu untuk cegah duplikat masjid/ustadz/kitab (termasuk
   variasi ejaan/gelar — lihat `id` yang sudah ada sebelum bikin baru)
   dan kitab (riset penulis+deskripsi kalau kitab baru).
2. Taruh file HTML rekap baru di root, ikuti pola nama file yang sudah ada.
3. Tambah entri sesi baru di `data.json` (`sessions[]`), plus entri baru di
   `masjid[]`/`ustadz[]`/`kitab[]` kalau memang belum ada.
4. **Jalankan `python3 scripts/build_seo.py`** — ini meregenerasi:
   - `sitemap.xml` (index + seluruh rekap, `lastmod` dari `date` tiap sesi)
   - JSON-LD (`WebSite` + `ItemList`) di `index.html`, antara marker
     `<!--LD_JSON_START-->` ... `<!--LD_JSON_END-->`
   - Per file rekap: OG/Twitter meta tags, favicon link, dan JSON-LD
     `Article`, antara marker `<!--SEO_BLOCK_START-->` ... `<!--SEO_BLOCK_END-->`
   - **Jangan edit manual apa pun di antara marker-marker itu** — akan
     tertimpa saat script dijalankan lagi.
5. Validasi sebelum commit: JSON valid, tidak ada ID duplikat di
   `sessions`/`masjid`/`ustadz`/`kitab`, setiap `masjidId`/`ustadzIds`/`theme`
   di sesi baru merujuk ID yang benar-benar ada.
6. Commit & push ke branch utama.

## SEO

Domain kanonis: `https://catatankajian.netlify.app`. Semua halaman (index +
rekap) punya `canonical`, `meta description`, Open Graph, Twitter Card, dan
JSON-LD structured data (`WebSite`/`ItemList` di index, `Article` per rekap).
`meta description` per file rekap ditulis manual mengikuti pola:
`"Catatan kajian: {title} — {ustadzRaw}. Masjid {masjidRaw}, {tanggal}."`
— kalau ditulis manual untuk sesi baru, `build_seo.py` akan memakai teks itu
apa adanya untuk isi `og:description`/`twitter:description`/JSON-LD, jadi
pastikan sudah benar sebelum dijalankan.
