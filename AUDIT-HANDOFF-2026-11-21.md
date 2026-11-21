# AUDIT-HANDOFF 2026-11-21 (PIC catatankajian)

## 1. Rekap baru (rutin)

- Commit `94b21c1`: sesi 85, Salman ITB (daring), SPN Salman Online Batch 23 Day 6 Sesi 2,
  Faisyal Muhammad Syahri Alwi, M.I.Kom, "Praktik Pembuatan Visi Pernikahan dan Visi Keluarga" (21 Nov 2026).
  Entri `ustadz[]` baru `faisyal-muhammad-syahri-alwi-m-i-kom` (bio dari flyer resmi; tidak ada sumber web publik lain).
  SEO diregenerasi.
- Validasi lokal sebelum push: JSON valid (round-trip identik), ID unik, rujukan ID sesi baru ada, HTML rekap
  well-formed, canonical = `recapUrl`, dashboard lokal 320 dan 430 px menampilkan sesi baru tanpa overflow,
  rekap baru 200.

## 2. Temuan: langkah "Terbitkan ke GitHub Pages" gagal, artifact tidak ditemukan

| Run | Pemicu | Upload artifact | Terbitkan | Uji pasca-deploy | Error |
|---|---|---|---|---|---|
| 44881148566 | push `94b21c1` | success (ID 14698136247, 3.532.209 byte) | failure | skipped | `Found 0 artifact(s)` / `No artifacts named "github-pages" were found` |
| 44881189574 | workflow_dispatch | success (ID 14698376468) | failure | skipped | sama |
| 44881495594 | workflow_dispatch (jeda ~3 menit) | success | failure | skipped | sama |

**Tervalidasi:**
- Artifact `github-pages` ada dan tidak expired menurut API `actions/runs/{id}/artifacts` (dicek setelah run gagal).
- SHA action identik dengan run sukses terakhir 43691935750 (15 Nov): checkout `11d5960`, configure-pages `983d773`,
  upload-pages-artifact `56afc60`, deploy-pages `d6db901`, upload-artifact `ea165f8`. Jadi bukan perubahan versi action.
- githubstatus.com (dibuka 21 Nov ~07:40 UTC): Actions, Pages, API Requests "Operational"; tidak ada insiden 21 Nov.
- `deploy.yml` tidak berubah sejak run sukses 15 Nov.

**Kesimpulan sendiri (belum terbukti):**
- Kemungkinan gangguan di sisi GitHub pada listing artifact dalam run yang sama (pesan error deploy-pages sendiri
  menyarankan cek githubstatus dan ulangi nanti). Isi commit tidak relevan dengan error ini.
- Dampak: situs live masih versi sebelumnya (84 sesi); sesi 85 belum tayang. Tidak ada kerusakan pada situs live.

## 3. Langkah lanjut

- Push handoff ini memicu run baru (percobaan ke-4). Bila masih gagal, ulangi `workflow_dispatch` beberapa saat kemudian.
- Usulan bila gagal berulang (menunggu konfirmasi Amal; mengubah `deploy.yml`): pisahkan menjadi dua job
  (`build` upload artifact, `deploy` dengan `needs: build`), sesuai pola yang direkomendasikan README actions/deploy-pages.
  Kriteria uji pasca-deploy tidak diubah.

## 4. Update ~07:50 UTC (sesi PIC berikutnya)

**Rekap baru (rutin):**
- Commit `bd9aa20`: sesi 86, Salman ITB (daring), SPN Salman Online Batch 23 Day 6 Sesi 1, Sri Haryati, S.E., M.Ag,
  "Parenting dan Visi Keluarga" (21 Nov 2026). Entri `ustadz[]` baru `sri-haryati-s-e-m-ag` (bio dari flyer resmi;
  tidak ada sumber web publik lain). Rekap menautkan sesi 85 (Day 6 Sesi 2) dan rekap Sofiana (Day 2 Sesi 1).
  SEO diregenerasi.
- Validasi lokal sebelum push: JSON round-trip identik, ID unik, rujukan ID sesi baru ada, HTML rekap well-formed,
  canonical = `recapUrl`, dashboard lokal 320 dan 430 px menampilkan sesi baru tanpa overflow, rekap baru 200.

**Deploy:** run 44882005112 (push `bd9aa20`) gagal dengan error yang sama (`Found 0 artifact(s)`). Total 5 run gagal hari ini.

**Tervalidasi tambahan:**
- Runner image beda: run sukses 15 Nov `ubuntu-26.04` versi 20261111.82.6; run gagal 21 Nov versi 20261116.202.1.
  Runner version sama (2.338.2). Kaitannya dengan error belum terbukti.
- Error yang sama dilaporkan publik di repo lain dengan `deploy-pages@v4`, satu job:
  - indextables/indextables-site PR #4 (20 Nov 2026): artifact ada menurut API; solusi mereka naik ke
    `upload-pages-artifact` v5 + `deploy-pages` v5. Hasilnya belum terbukti di PR itu.
  - Hawaii-Appleseed/Hawaii-Appleseed-website issue #125 (19 Nov 2026).
  - actions/deploy-pages issue #451 (7 Okt 2026): lookup artifact kosong bila upload dan deploy di job yang sama.
    Pelapor: memisah job build/deploy memperbaikinya. Belum ada respons maintainer.

**Kesimpulan sendiri (belum terbukti):** kemungkinan perubahan di sisi GitHub sejak sekitar 19 Nov membuat lookup
artifact di job yang sama gagal. Isi commit tidak relevan.

**Usulan (menunggu konfirmasi Amal di chat PIC; mengubah `deploy.yml`), satu perubahan per push (aturan 6):**
1. Pisah job: `build` (checkout, configure-pages, susun `_site`, upload) dan `deploy` (`needs: build`, deploy-pages,
   lalu uji pasca-deploy). Kriteria uji tidak diubah.
2. Bila masih gagal: naikkan `upload-pages-artifact` ke v5 dan `deploy-pages` ke v5.

**Dampak:** situs live masih 84 sesi. Sesi 85 dan 86 sudah di repo dan tayang otomatis begitu deploy berhasil.

**Hasil (tervalidasi, log Actions):** run 44882147791 (push `bbf440c`, handoff di atas, 07:51 UTC) **sukses**:
`Found 1 artifact(s)`, terbit, uji pasca-deploy lolos semua (beranda 200, berkas internal 404, canonical 86 rekap =
`recapUrl`). Sesi 85 dan 86 sudah tayang. Tanpa perubahan `deploy.yml`.

**Koreksi (07:52 UTC):** kesimpulan "pulih" di commit `10199fb` keliru. Run berikutnya 44882211088 (push `10199fb`,
isi situs sama) **gagal lagi** dengan error yang sama. Hari ini 1 dari 7 run sukses.

**Kesimpulan sendiri:** error **intermiten**, bukan sudah pulih; cocok dengan pola issue #451 (lookup di job yang sama).
Situs live tetap versi run sukses 44882147791 (86 sesi): langkah deploy gagal sebelum membuat deployment, jadi tidak
menimpa situs. Risiko ke depan: tiap push rekap baru berpeluang gagal terbit dan perlu `workflow_dispatch` ulang.
Usulan 1 (pisah job) disarankan; menunggu konfirmasi Amal.

## 5. Perubahan pipeline: pisah job (commit `9848614`, ~07:58 UTC)

**Persetujuan:** Amal di chat PIC (21 Nov 2026, 14:55 WIB), menjawab usulan pisah job: "iya lakukan action yang
tidak perlu konfirmasi manual, selama tujuan besarnya tercapai".

**Perubahan:**
- `deploy.yml`: job `build` (checkout, configure-pages, susun `_site/`, upload artifact) lalu job `deploy`
  (`needs: build`; deploy-pages, checkout, susun ulang `_site/`, uji pasca-deploy). Versi action tidak berubah.
- Daftar berkas publik dipindah ke `scripts/susun_site.sh` (satu sumber; dipanggil kedua job). `CLAUDE.md` bagian
  Struktur dan "Berkas yang tayang" diperbarui.
- Uji pasca-deploy tidak diubah.

**Validasi lokal sebelum push:** actionlint 0 issue; `_site/` dari skrip identik (`diff -r`) dengan perintah lama;
simulasi langkah uji terhadap server lokal: jalur sukses exit 0, jalur gagal (CLAUDE.md ikut tayang) exit 1.

**Hasil (tervalidasi, log Actions), 6 run pada `9848614`:**

| Run | Pemicu | Langkah terbit | Artifact | Uji pasca-deploy |
|---|---|---|---|---|
| 44882640605 | push | success | Found 1 | lolos |
| 44882696487 | dispatch | success | Found 1 | lolos |
| 44882704933 | dispatch | success | Found 1 | lolos |
| 44882773465 | dispatch | success | Found 1 | **gagal**: `CLAUDE.md`, `scripts/build_seo.py` -> 503 (harus 404) |
| 44882891426 | dispatch | success | Found 1 | **gagal**: `AUDIT-HANDOFF-2026-10-22.md` -> 503 (harus 404) |
| 44883009850 | dispatch | success | Found 1 | lolos |

**Kesimpulan sendiri:**
- Masalah artifact tidak muncul lagi (6/6 terbit; sebelum pisah job 2/8). Sampel kecil, belum bukti permanen.
- 2 run merah karena 503 sesaat pada cek "internal harus 404" — masalah lama yang sama dengan bagian 2 handoff
  12 Nov, bukan akibat pisah job. Situs tetap terbit di kedua run itu.

## 7. Retry 5xx diterapkan (commit `d44cdae`, ~10:25 UTC)

**Persetujuan:** Amal di chat PIC (21 Nov 2026, 17:22 WIB): "setuju retry 5xx". Isi perubahan sama dengan bagian 6
(patch yang ditolak sebelumnya, diterapkan apa adanya). Lint dan simulasi lokal diulang sebelum push: hasil sama.

**Hasil (tervalidasi, log Actions), 6 run pada `d44cdae`:**

| Run | Pemicu | Hasil | Kena 5xx lalu pulih |
|---|---|---|---|
| 44894233046 | push | success | `AUDIT-HANDOFF-2026-09-22.md`: 503 x3, lalu 404 |
| 44894449038 | dispatch | success | - |
| 44894502153 | dispatch | success | `rekap/kajian-aladhim-setiawan-12-juli-2026.html`: 503 x1, lalu 200 |
| 44894568023 | dispatch | success | - |
| 44894624768 | dispatch | success | `AUDIT-HANDOFF-2026-09-22.md`: 503 x1, lalu 404 |
| 44894699510 | dispatch | success | - |

Semua `Found 1 artifact(s)`, 0 baris FAIL.

**Kesimpulan sendiri:** 3 dari 6 run kena 503 sesaat; dengan aturan lama (3 percobaan) run 44894233046 pasti merah.
503 juga muncul pada berkas yang harus 200 (rekap), jadi ini gangguan umum GitHub Pages, bukan khusus berkas internal.
Sampel kecil; pantau di push berikutnya.

## 6. Usulan menunggu: retry 5xx di uji pasca-deploy (diterapkan di bagian 7)

- Isi (dari usulan 12 Nov bagian 3): `check_url` memperlakukan 5xx sebagai "belum siap", retry hingga 9 percobaan
  jeda 10 detik. Kriteria lulus tidak dilonggarkan: hanya kode persis sama dengan yang diharapkan yang lulus, 5xx
  tidak pernah lulus. Kode non-5xx yang salah tetap 3 percobaan.
- Sudah disiapkan dan diuji lokal (server simulasi): 404 normal lulus; 503 dua kali lalu 404 lulus; 200 saat
  diharapkan 404 gagal; 503 permanen gagal setelah 9 percobaan (~80 detik). actionlint 0 issue.
- **Tidak di-push:** push ditolak pemeriksaan izin sesi (perubahan pipeline kedua, di luar butir yang disetujui
  eksplisit). Menunggu konfirmasi Amal yang spesifik untuk butir ini di chat PIC (aturan lintas-repo butir 2).
- Dampak bila tidak diterapkan: sebagian run tetap merah karena 503 sesaat walau situs terbit; perlu dibaca lognya.

## Untuk repo lain

- Workflow ketiga repo lain memakai pola serupa (satu origin, deploy-pages). Bila error yang sama muncul di sana,
  penyebabnya kemungkinan sama. Auditor yang menyalurkan; PIC repo ini tidak mengubah repo lain.
- Pola pisah job (bagian 5) sudah terbukti di repo ini untuk masalah artifact (6/6 terbit). Usulan ke Auditor:
  pertimbangkan untuk jadwalkajian, bikin-cv-taaruf, kenalicalon bila workflow mereka masih satu job.
- Pola retry 5xx di `check_url` (bagian 7) terbukti di repo ini (6/6 hijau, 3 run pulih dari 503). Usulan ke Auditor:
  sebarkan ke tiga repo lain bila uji pasca-deploy mereka memakai pola `check_url` serupa.
