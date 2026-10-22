# Handoff PIC — 2026-10-22

Dari: sesi kerja `catatankajian` (session_01EK9Yre85jZnzA9fKsiqXA7)
Untuk: sesi "Auditor Project"
Konteks: eksekusi `AUDIT-HANDOFF-2026-10-22-auditor.md` (proyek baru Kenali Calon + sinkronisasi empat repo).

## Ringkasan: ketiga gelombang selesai

| Gelombang | Status | Commit | Run | Konfirmasi |
|---|---|---|---|---|
| 1 — tautan Kenali Calon | Selesai | `380a6dd` | [#32 success](https://github.com/reconciler/catatankajian/actions/runs/39711116029) | Sudah disetujui Amal (chat Auditor 22 Okt, tampilan, bukan pipeline) |
| 2 — ratifikasi `4680c2c` | Selesai (dokumentasi saja) | — | — | **Ya**, langsung di chat PIC 22 Okt 2026 |
| 3 — uji aset dirujuk sumber | Selesai | `b66c872` | [#33 success](https://github.com/reconciler/catatankajian/actions/runs/39714906273) | **Ya**, langsung di chat PIC 22 Okt 2026 (pipeline, rule 2) |

## Gelombang 1 — tautan Kenali Calon

Ditambahkan ke `.menu-panel` "Proyek lain" di `index.html`, setelah "Bikin CV Taaruf": label dan URL persis Daftar resmi.

**Tervalidasi lokal sebelum push:**
- `build_seo.py`: tidak ada diff lain di luar `index.html`.
- axe-core 4.13.0, 320/375/430px, panel tertutup+terbuka: **0 pelanggaran**.
- Tinggi `.hero` closed==open di ketiga lebar (tidak membesar).
- Bounding box panel tidak keluar viewport di ketiga lebar (tidak terpotong).
- Search tetap jalan ("tauhid" 65 sesi total -> 12 hasil, 0 error JS).
- Screenshot panel terbuka 320px dicek visual — tiga tautan tampil benar.

Tampilan berubah (rule 11): tidak menahan pekerjaan, cukup dicatat di sini.

## Gelombang 2 — ratifikasi commit `4680c2c`

**Temuan:** commit `4680c2c` (11 Okt, langkah cek canonical di `deploy.yml`) dibuat sesi kerja lain
(session_01NqqmSNHqyHxR33SZygRy6i) tanpa catatan konfirmasi Amal untuk perubahan pipeline di pesan commit maupun
di handoff mana pun (dicek: tidak ada `AUDIT-HANDOFF-2026-10-1*.md`). **Tervalidasi:** run #29 sukses dan cek
canonical berjalan di produksi sejak itu — fungsinya benar, hanya proses konfirmasinya yang tidak tercatat.

**Ditanyakan langsung ke Amal di chat PIC 22 Okt 2026 (bukan via relay Auditor): "Ya"** — disahkan retroaktif.
Tidak ada perubahan kode untuk butir ini, murni catatan.

## Gelombang 3 — uji aset dirujuk sumber (menutup celah nyata)

**Celah [dikonfirmasi ulang oleh PIC]:** langkah "Uji otomatis pasca-deploy" yang lama menurunkan daftar berkas
yang diuji dari isi `_site/` saat ini (`find _site ...`). Kalau sebuah berkas baru dirujuk `index.html`/`rekap/*.html`
tapi lupa ditambahkan ke daftar `cp` di langkah "Susun folder situs", berkas itu tidak pernah masuk `_site/` —
dan karena loop lama hanya mengiterasi isi `_site/`, berkas yang hilang itu **tidak pernah diuji sama sekali**
(bukan FAIL, diam saja), sehingga run tetap hijau walau situs publik rusak (mis. `lib/fuse.min.js` hilang ->
pencarian mati total di situs live).

**Perbaikan:** langkah baru (bagian 5 "Uji otomatis pasca-deploy") yang mengekstrak referensi aset lokal
langsung dari `index.html` (sumber, bukan `_site/`) + sampel 3 file `rekap/*.html` pertama (alfabetis, deterministik)
— `href`/`src` relatif, tag `meta` same-origin (`og:image` dll.), serta path di `fetch()` lokal — lalu cek tiap
satu 200 terhadap situs live. Independen dari isi `_site/`, jadi menangkap tepat kasus "lupa cp".

**Validasi (dua lapis, sebelum push):**
1. Skrip berdiri sendiri (standalone): jalur sukses lolos; jalur gagal (hapus `lib/` dari `_site` lokal, sambil
   `index.html` tetap merujuknya) terdeteksi FAIL dengan benar.
   - **Kesalahan sendiri ditemukan+diperbaiki di sini:** percobaan pertama memakai process-substitution
     (`< <(python3 ...)`) untuk membaca output python — ternyata python sempat crash (`ValueError` dari bug
     regex-unpacking saya sendiri) dan shell **diam-diam tetap melapor sukses** (exit 0) karena exit code python
     tidak pernah dicek lewat process substitution. Diperbaiki: python menulis ke file sementara, exit code-nya
     dicek eksplisit sebelum lanjut.
2. Skrip utuh persis isi `deploy.yml`, di-dedent persis cara YAML block-scalar memprosesnya (baseline 10 spasi
   seragam — sama seperti langkah canonical yang sudah terbukti jalan di produksi), dijalankan dari tiruan
   repo-root lengkap (index.html, rekap/ asli 65 file, berkas internal untuk uji 404) melawan `_site` lokal:
   - Jalur sukses: exit 0, semua 7 aset sumber + seluruh check lain lolos.
   - Jalur gagal (`lib/` dihapus dari `_site`): exit 1. **Terbukti langsung:** langkah sampel-subfolder lama
     memang diam saja untuk kasus ini (tidak muncul OK maupun FAIL untuk `lib`) — hanya check baru yang
     menangkap celah ini.

**Verifikasi live (run [#33](https://github.com/reconciler/catatankajian/actions/runs/39714906273), `success`):**
log Actions sungguhan menunjukkan ketujuh baris `OK [aset dirujuk sumber]` terhadap domain live
`reconciler.github.io`, bukan simulasi.

## Verifikasi Auditor (dicatat di `AUDIT-HANDOFF-2026-10-22-auditor.md` bagian 4)

Auditor memeriksa ulang gelombang 1-3 langsung (git, Actions, uji ulang) — **diterima semua**, termasuk sampel
3 rekap untuk Gelombang 3 (dinilai cukup, tidak perlu diperluas). Kebiasaan melaporkan+memperbaiki kesalahan
sendiri (bug process-substitution) dicatat sebagai praktik baik.

## Usulan opsional Auditor — dikerjakan: landmark `<header>`/`<main>`

Auditor menemukan (axe semua rule, bukan cuma WCAG A/AA, pada hasil Gelombang 1): `landmark-one-main` (1) dan
`region` (11-12) sudah ada **sebelum** perubahan ini (bukan akibat tautan Kenali Calon). Usulan: tambah landmark
semantik seperti pola `jadwalkajian`. Ditandai rule 1 (tanpa dampak tampilan/fungsi) — PIC putuskan sendiri,
syarat: screenshot identik piksel + tinggi header tak berubah.

**Dikerjakan** (commit `fcc89c4`, run [#36 success](https://github.com/reconciler/catatankajian/actions/runs/39715962255)):
`<div class="hero">` -> `<header class="hero">`; `<main>` membungkus disclaimer+filterbar+result-count+`#main`.
Tidak ada perubahan CSS/JS (dicek: tidak ada selector tag-spesifik atau DOM traversal yang bergantung struktur ini).

**Hasil uji (320/375/430px):**
- axe-core semua rule: `landmark-one-main`+`region`, 2 pelanggaran -> **0**, di ketiga lebar.
- Screenshot full-page before/after, pixelmatch: **0 piksel beda** dari total ~1 juta piksel per lebar, di
  ketiga lebar.
- Tinggi `.hero`: sama persis sebelum/sesudah di ketiga lebar (151,4 / 151,4 / 152,0 px).
- Search ("tauhid" -> 12/65) dan panel "Tentang" tetap jalan, 0 error JS.
- `build_seo.py`: tidak ada diff lain.

## Yang perlu diketahui

- Tampilan (Gelombang 1, dan landmark di atas — meski piksel identik) belum dilihat di perangkat nyata oleh
  Amal — per rule 11, dianggap tidak bermasalah sampai ada laporan sebaliknya, tidak menahan pekerjaan.
- Uji pasca-deploy sekarang 5 lapis: beranda, berkas top-level+subfolder dari `_site/`, berkas internal 404,
  canonical rekap, dan aset dirujuk sumber. Celah kelas "lupa cp" untuk berkas yang dirujuk dari `rekap/*.html`
  selain 3 sampel masih mungkin lolos — kalau Auditor mau memperluas sampel, itu usulan terpisah.
- Tidak ada data pribadi/sensitif ditulis di handoff ini.
