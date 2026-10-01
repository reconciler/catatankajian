# Handoff PIC — 2026-09-30

Dari: sesi kerja `catatankajian` (session_01EK9Yre85jZnzA9fKsiqXA7)
Untuk: sesi "Auditor Project"
Konteks: eksekusi keputusan Amal 30 Sep 2026, diteruskan lewat
`AUDIT-HANDOFF-2026-09-30-auditor.md` bagian 2 dan 4.

Catatan: Amal baru mengonfirmasi eksekusi ini langsung ke sesi kerja
setelah notifikasi pertama (bagian 4 auditor) diterima — sesi ini tidak
langsung mengeksekusi hanya berdasarkan notifikasi relay, menunggu
konfirmasi eksplisit di percakapan langsung dulu.

## Status: keempat poin sudah dieksekusi dan di-deploy

**Push 1 (`15ab738`)** — bagian 4 (artifact path), terpisah dan lebih dulu
sesuai saran:
- `deploy.yml`: step baru menyusun `_site/` berisi hanya berkas publik
  (`index.html`, `data.json`, `rekap/`, `og-image.png`, `favicon.svg`,
  `robots.txt`, `sitemap.xml`, `lib/`) sebelum `upload-pages-artifact`.
  `CLAUDE.md`/`AUDIT-HANDOFF-*.md`/`COORDINATION-NOTE-*.md`/`scripts/`/
  `.github/` sengaja tidak disalin.
- Deploy: [run 36752887174](https://github.com/reconciler/catatankajian/actions/runs/36752887174) — `success`.
- **Amal perlu verifikasi manual** (sesi ini tidak bisa fetch domain
  publik): buka `https://reconciler.github.io/catatankajian/CLAUDE.md` —
  harus 404.

**Push 2 (`5a49bc7`)** — bagian 1-3:
1. Fuse.js → `lib/fuse.min.js`. Integritas dicocokkan terhadap
   `registry.npmjs.org/fuse.js/6.6.2` (sha1 `fe463fed4b98c0226ac3da2856a415576dc9a111`
   dan sha512/`integrity` registry — keduanya cocok persis dengan file
   yang disalin). `index.html` tidak lagi memuat skrip jsDelivr saat
   runtime. Diuji: pencarian tetap berfungsi (Playwright headless, query
   "tauhid" → 62 jadi 12 hasil, tanpa error JS).
2. Blok `<img>` `hits.sh` dihapus di `kajian-alhikmah-ddn2-maksum-20-juni-2026.html`
   dan `kajian-darussalam-gta-arif-21-juni-2026.html`. `SEO_BLOCK` tidak
   disentuh. Dikonfirmasi: `grep -r hits.sh rekap/` nihil.
3. Menu "Tentang" dipasang: akordeon tertutup default di header,
   isi Tentang + Proyek lain (Jadwal Kajian, Bikin CV Taaruf), tautan
   luar `target="_blank" rel="noopener noreferrer"`. Posisi panel
   dihitung dinamis via `getBoundingClientRect` + `position:fixed` —
   percobaan pertama pakai anchor CSS statis ke parent flex, meluber ke
   luar viewport saat header wrap di layar sempit (ketemu lewat
   screenshot Playwright, diperbaiki sebelum push). Diuji lebar
   320/375/430px: tinggi header tidak berubah, tidak ada scroll
   horizontal, buka/tutup benar (klik luar + Esc), `aria-expanded`
   ter-update. Sekalian diseragamkan: pil "Jadwal Kajian" dan link
   Instagram footer → `rel="noopener noreferrer"`, URL Instagram
   dicocokkan ke daftar resmi (`https://www.instagram.com/amalwoodworking/`).
- Deploy: [run 36752990305](https://github.com/reconciler/catatankajian/actions/runs/36752990305) — `success`.
- **Amal perlu verifikasi manual visual** (sesi ini tidak bisa fetch
  domain publik): buka beranda, coba tombol "Menu", cek search masih
  jalan.

## Update — 1 Okt 2026

Dikonfirmasi langsung oleh Amal di chat ("iya saya setuju" / "boleh untuk
semuanya") untuk 3 hal: aturan standing eksekusi instruksi Auditor, batch
revisi tombol "Tentang", dan smoke test pasca-deploy.

**Push `2fa44bc`** (batch 2+3 digabung jadi satu push/satu deploy, sesuai
saran Auditor):

1. **Revisi tombol "Tentang"** (bagian 5 handoff Auditor): label "Menu" →
   "Tentang"; pil "📅 Jadwal Kajian" (`jadwal-link`) dan CSS-nya dihapus dari
   header — tetap ada lewat panel "Proyek lain". Diuji ulang Playwright
   320/375/430px: tinggi header tidak berubah, tidak ada scroll horizontal,
   buka/tutup (klik luar + Esc) normal, tanpa error JS. `CLAUDE.md` bagian
   status diperbarui.

2. **Smoke test pasca-deploy** (bagian 6 handoff Auditor): langkah baru di
   `deploy.yml` setelah "Terbitkan ke GitHub Pages" — retry beranda ~2 menit
   + cek teks penanda, cek semua berkas top-level `_site/` (dinamis dari isi
   direktori saat build) + sampel 1-3 berkas per subfolder, pastikan 4 berkas
   internal 404. Hanya `curl`+shell, tanpa action pihak ketiga/kirim data.
   **Divalidasi 2x sebelum push**: simulasi lokal jalur sukses (exit 0) dan
   jalur gagal (sengaja bocorkan 1 file test → terdeteksi FAIL, exit 1).

**Hasil run sungguhan** ([run 36808163182](https://github.com/reconciler/catatankajian/actions/runs/36808163182)):
semua 9 step `conclusion: success`, termasuk langkah "Uji otomatis
pasca-deploy" (2 detik — beranda langsung 200 di percobaan pertama, tanpa
retry). Step-level `success` di API Actions = exit 0 skrip = semua
pengecekan lolos terhadap situs live sungguhan (bukan simulasi).

## Yang belum/tidak diverifikasi dari sesi ini

- Byte-for-byte diff `lib/fuse.min.js` terhadap yang sebelumnya disajikan
  jsDelivr tidak dilakukan (jsDelivr tidak bisa diakses dari sandbox ini) —
  tapi karena versi dipatok 6.6.2 dan integritas dicocokkan ke npm
  (sumber jsDelivr sendiri), risikonya dianggap setara dengan opsi yang
  disetujui Amal.
- Tidak menyentuh workflow lain atau repo lain.
