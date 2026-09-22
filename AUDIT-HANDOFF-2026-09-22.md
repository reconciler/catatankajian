# Ringkasan Handoff — Sesi Sinkronisasi & SEO Catatan Kajian

**Untuk:** sesi Claude "Auditor project kajian" (belum berjalan saat catatan ini
ditulis)
**Dari:** sesi Claude Code `catatankajian-c0` (session_01EK9Yre85jZnzA9fKsiqXA7)
**Ditulis:** 22 September 2026
**Status keseluruhan:** semua pekerjaan di bawah sudah di-push ke remote,
divalidasi lokal. **PR #1 SENGAJA BELUM DI-MERGE** — lihat bagian "Item
tertunda" di bawah, ini bukan kelalaian.

---

## 1. Konteks awal

Repo `reconciler/catatankajian` adalah dashboard pribadi (statis, `index.html`
+ `data.json`) yang mengindeks catatan kajian Islam pemilik repo (Amal). Live
di `catatankajian.netlify.app`. Sebelum sesi ini: `noindex, nofollow` aktif
(sengaja diblokir dari search engine), 62 file rekap (`kajian-*.html`) semua
flat di root branch `main`, tidak ada SEO metadata, tidak ada dokumentasi
repo (`CLAUDE.md`).

Tugas berkembang bertahap dalam satu sesi panjang:
1. Sinkronisasi mingguan biasa — tambah 5 rekap kajian baru (12–19 Sep 2026)
2. Buka situs untuk terindeks search engine (atas persetujuan eksplisit user)
3. Audit gap SEO dibanding repo sibling `jadwalkajian`, lalu tutup gap-nya
4. **Perubahan arsitektur besar**: pisah file rekap ke branch `Catatan`
   terpisah (GitHub Pages), `main` jadi dashboard-only (Netlify)
5. Temuan risiko kredit Netlify dari sesi lain ("Integrasi dua project
   kajian") — keputusan tunda merge PR #1

## 2. Perubahan pada `data.json` (branch `main`, sudah live-ready)

5 sesi kajian baru ditambahkan (id 58–62), 12–19 September 2026:
masjid Jami' Al-Barkah, Baitussalam, dan 3 sesi Nurul Iman. 3 ustadz baru
ditambahkan ke array `ustadz[]` (`ahmad-zainuddin-lc`, `harits-abu-naufal`,
`waskito-aji-nugroho-lc-m-a`) — bio ditulis dari riset web, dengan catatan
transparan bila tidak ditemukan sumber solid. Tidak ada masjid/kitab baru
(semua match entri existing). `generatedAt` diperbarui ke `2026-09-22`.

Validasi yang sudah dijalankan: JSON well-formed, tidak ada ID duplikat di
`sessions`/`masjid`/`ustadz`/`kitab`, semua `masjidId`/`ustadzIds`/`theme`
merujuk ID yang benar-benar ada.

## 3. Perubahan arsitektur: dua branch, dua publikasi

**Ini perubahan paling signifikan di sesi ini — auditor wajib paham ini
sebelum menilai apa pun lainnya.**

- **`main` → Netlify** (`catatankajian.netlify.app`): HANYA dashboard.
  `index.html`, `data.json`, `robots.txt`, `sitemap.xml`, `favicon.svg`,
  `og-image.png`, `scripts/build_seo.py`, `CLAUDE.md`. **Tidak ada satu pun
  file `kajian-*.html` di branch ini lagi** (sengaja dihapus, lihat commit
  `62df416`).
- **`Catatan` → GitHub Pages** (`reconciler.github.io/catatankajian`):
  seluruh 62 file `kajian-*.html`, plus `robots.txt`/`sitemap.xml` miliknya
  sendiri (domain GitHub Pages).

Alasan pemisahan: `recapUrl` di `data.json` **sejak sebelum sesi ini** sudah
memakai domain GitHub Pages — jadi ini bukan keputusan baru saya, melainkan
menyelaraskan implementasi dengan rencana yang sudah lama ada tapi belum
dieksekusi. Branch `Catatan` sendiri sebelumnya ada tapi basi/stale (berhenti
di commit lama `f11aad7`, ancestor dari `main`, tertinggal 19 rekap).

**Eksekusi (kronologis, semua sudah di-push ke `origin/Catatan`):**
- Commit `bca78ce` — isi ulang `Catatan` dengan 62 rekap terkini + SEO
  (canonical/og:url/JSON-LD mengarah ke domain GitHub Pages)
- Commit `02281fa` — **perbaikan bug**: favicon href relatif (`/favicon.svg`)
  salah untuk GitHub Pages project site (resolve ke root domain, bukan
  `/catatankajian/`). Diganti absolut ke Netlify.

**Di `main`** (branch kerja `claude/sinkronisasi-catatan-kajian-j9cx52`,
commit `62df416`): hapus 62 file rekap, perbaiki `scripts/build_seo.py` agar
`sitemap.xml`/JSON-LD `index.html` memakai `recapUrl` apa adanya dari
`data.json` (sebelumnya salah — direkonstruksi dengan domain Netlify, padahal
file-nya sudah tidak ada di sana).

**Precondition yang sudah dipenuhi sebelum penghapusan dari `main`:** user
mengonfirmasi eksplisit bahwa GitHub Pages sudah aktif dan live dari branch
`Catatan` (dicek manual oleh user sendiri — saya tidak punya akses fetch ke
domain manapun dari sandbox ini, lihat bagian 6).

## 4. Paritas SEO dengan `jadwalkajian`

Sesi ini juga meng-audit repo sibling `reconciler/jadwalkajian` (dashboard
jadwal kajian, arsitektur berbeda — single-page, prune otomatis via GitHub
Actions) untuk membandingkan level SEO. Gap yang ditemukan dan ditutup di
`catatankajian`:

| Item | Status sebelum | Status sekarang |
|---|---|---|
| Favicon | Tidak ada | `favicon.svg` (ikon buku terbuka) |
| Open Graph + Twitter Card | Tidak ada | Ada di index + semua rekap |
| og-image | Tidak ada | `og-image.png` 2400×1260, dibuat via Playwright screenshot HTML/CSS lokal |
| JSON-LD | Tidak ada | `WebSite`+`ItemList` di index, `Article` per rekap |
| Script regenerasi otomatis | Tidak ada | `scripts/build_seo.py` |
| Dokumentasi repo | Tidak ada `CLAUDE.md` | Ada, mendokumentasikan arsitektur 2-branch |

Satu hal yang **sengaja tidak** ditambahkan: `SearchAction` schema.org di
index — dashboard ini filter client-side murni (Fuse.js, tanpa URL query
pattern), jadi menambahkan itu berarti mengklaim fungsi yang tidak benar-benar
ada.

## 5. Isu kredit Netlify — alasan PR #1 ditunda

Sesi lain ("Integrasi dua project kajian", session_01V7K2gPxpghoLSqB74zsXWV)
mengirim notifikasi terjadwal berisi: saldo kredit deploy tim Netlify `Amal`
(teamId `6a5428ecac08571f1637be92`, dipakai bersama `catatankajian` +
`jadwalkajian`) ada di **14,9/300** — di bawah 15 kredit yang dibutuhkan per
production deploy. Breakdown klaim: 19 deploy manual × 15 kredit = 285,
semua sebelum sesi-sesi Claude mulai bantu. Regrant berikutnya **12 Oktober
2026**.

Saya cross-check sebagian: tim memang plan Free (terverifikasi via Netlify
API `get-team`), situs memang git-linked dengan auto-deploy aktif
(terverifikasi dari komentar bot Netlify di PR #1), dan repo memang tidak
punya gate deploy apa pun (`netlify.toml`) yang bisa mencegah auto-deploy
saat push ke `main`. Angka pasti 14,9 sendiri **divalidasi langsung oleh
user** dari dashboard Netlify (saya tidak bisa memverifikasi angka itu
sendiri — tidak ada API read untuk saldo kredit di toolset saya).

**Keputusan user (eksplisit, dikonfirmasi 22 Sep 2026):** tunda merge PR #1
sampai 12 Oktober 2026. Alasan: merge kemungkinan besar memicu percobaan
production deploy otomatis yang gagal karena kredit kurang. Merge PR itu
sendiri aman dari sisi git (tidak butuh kredit) — risikonya murni di
percobaan deploy Netlify setelahnya.

Komentar penjelasan sudah diposting ke PR #1:
https://github.com/reconciler/catatankajian/pull/1#issuecomment-5780659161

## 6. Keterbatasan environment yang relevan untuk auditor

- **Egress diblokir**: sandbox sesi ini tidak bisa `curl`/`WebFetch` ke domain
  apa pun di luar API resmi (termasuk `catatankajian.netlify.app` dan
  `reconciler.github.io`) — kebijakan organisasi, bukan masalah sesaat.
  Semua verifikasi "live site" dalam sesi ini dilakukan lewat API resmi
  (Netlify MCP, GitHub MCP), BUKAN dengan benar-benar membuka halaman.
  Auditor perlu tahu ini sebelum mengasumsikan sesuatu "sudah dicek visual".
- **Cron/scheduled check bersifat session-only**: tidak bertahan lintas sesi,
  auto-expire maksimal 7 hari. Tidak ada mekanisme reminder otomatis yang
  bisa menjangkau 12 Oktober 2026 dari sesi ini.

## 7. Item yang masih perlu diverifikasi manual (oleh user atau auditor)

- [ ] Render visual live `catatankajian.netlify.app` pasca-deploy (belum
      di-deploy — PR #1 masih pending)
- [ ] Render visual live `reconciler.github.io/catatankajian` — user sudah
      konfirmasi lisan bahwa ini aktif, tapi belum ada verifikasi otomatis
      dari sisi Claude manapun
- [ ] Saldo kredit Netlify aktual di tanggal audit (bisa sudah berubah dari
      14,9 yang tercatat 22 Sep)
- [ ] Apakah PR #1 sudah di-merge oleh user (auditor harus cek `git log
      origin/main` dan `pull_request_read` PR #1 sebelum asumsi apa pun)

## 8. File/lokasi kunci untuk audit

- `data.json` (branch `main`) — sumber kebenaran tunggal untuk metadata sesi
- `scripts/build_seo.py` (branch `main`) — cara regenerasi sitemap/JSON-LD
- `CLAUDE.md` (branch `main`) — dokumentasi arsitektur & alur kerja lengkap
- PR #1: https://github.com/reconciler/catatankajian/pull/1
- Branch `Catatan`: https://github.com/reconciler/catatankajian/tree/Catatan
