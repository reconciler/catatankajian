# AUDIT-HANDOFF 2026-11-12 (PIC catatankajian)

## 1. Rekap baru (rutin)

- Commit `fa19247`: sesi 81, Salman ITB (daring), Kelas Fikih Munakahat 2/4, Ust. Zulkarnain, S.Th.I,
  "Hak dan Kewajiban Pasutri dalam Islam" (9 Nov 2026). Bio `zulkarnain-s-th-i` ditambah sesi 2. SEO diregenerasi.
- Validasi lokal sebelum push: JSON valid, ID unik, rujukan ID sesi baru ada, HTML rekap well-formed,
  canonical = `recapUrl`, dashboard lokal (430 px) menampilkan sesi baru, rekap baru 200.

## 2. Temuan: uji pasca-deploy merah karena 503 pada cek "internal (harus 404)"

| Run | Pemicu | Langkah "Terbitkan ke GitHub Pages" | Uji pasca-deploy | Baris FAIL |
|---|---|---|---|---|
| 43138329582 #1 | push `fa19247` | success | failure | `AUDIT-HANDOFF-2026-10-03.md -> 503` |
| 43138329582 #2 | re-run failed jobs | failure | - | "Multiple artifacts named github-pages" (efek re-run dalam run yang sama, bukan masalah situs) |
| 43139080515 | workflow_dispatch, `fa19247` | success | failure | `AUDIT-HANDOFF-2026-10-28.md -> 503` |
| 43139294120 | push `0403a2f` (handoff ini; isi situs sama + rekap sesi 81) | success | **success** | - (semua uji lolos, canonical 81 rekap OK) |

**Tervalidasi (log Actions):**
- Semua cek lain OK, termasuk beranda 200, berkas publik 200, sampel rekap 200, berkas internal lain 404,
  canonical 81 rekap = `recapUrl`.
- Tiap run hanya satu URL internal yang kena 503, URL-nya berbeda tiap run. `check_url` mencoba 3x jeda 5 detik;
  503 bertahan ~15 detik.
- Run sebelumnya (`405d21a`, 12 Nov 01:27 UTC, dan run 8 Nov ke belakang) hijau.

**Kesimpulan sendiri (belum terbukti):**
- Penyebab kemungkinan gangguan sesaat GitHub Pages pada respons 404 (bukan isi commit; commit ini tidak
  menyentuh berkas internal maupun `deploy.yml`). Status resmi GitHub hari ini tidak bisa dibuka dari sesi
  (githubstatus.com tidak ada di allowlist); pencarian web tidak menemukan insiden Pages tercatat 12 Nov 2026.
- Situs terbit (langkah publish success tiga kali). Run ketiga hijau mendukung dugaan gangguan sesaat, tetapi
  belum membuktikan penyebabnya.

**Catatan:** re-run "failed jobs" di run yang sama tidak bisa dipakai untuk workflow ini (artifact `github-pages`
ganda). Untuk mengulang uji, pakai `workflow_dispatch` (run baru).

## 3. Usulan perbaikan (menunggu konfirmasi Amal; mengubah `deploy.yml`)

- `check_url`: anggap 5xx sebagai "belum siap", retry lebih panjang (mis. 6x, jeda 10 detik). Kriteria lulus
  **tidak dilonggarkan**: tetap wajib tepat 404 untuk berkas internal dan 200 untuk berkas publik; 5xx tidak
  pernah dihitung lulus.
- Bila terbukti di repo ini, pola yang sama relevan untuk jadwalkajian, bikin-cv-taaruf, kenalicalon
  (origin sama, uji serupa).

## Untuk repo lain

- Lihat bagian 2-3: kemungkinan run merah serupa di repo lain bila gangguan 503 masih terjadi. Auditor yang
  menyalurkan; PIC repo ini tidak mengubah repo lain.
