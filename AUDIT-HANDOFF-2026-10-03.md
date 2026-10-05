# Handoff PIC — 2026-10-03 (ekstraksi aturan, Butir A)

Dari: sesi kerja `catatankajian` (session_01EK9Yre85jZnzA9fKsiqXA7)
Untuk: sesi "Auditor Project"
Konteks: eksekusi `AUDIT-HANDOFF-2026-10-03-auditor.md` bagian 2.1 (Butir A) dan 2.3.

## 1. Ditambahkan langsung ke `CLAUDE.md` repo ini

Keputusan Amal yang eksplisit dan khusus repo ini, dari brief awal sesi ini, belum
tertulis formal — ditambahkan ke bagian "Alur kerja" langkah 1 dan 3 (commit ini):

1. 8 kategori `theme` baku (`aqidah`, `fiqih-ibadah`, `fiqih-muamalah`, `tafsir-quran`,
   `sirah-tarikh`, `tazkiyatun-nafs`, `keluarga-dakwah`, `isu-kontemporer`) — jangan buat
   kategori baru.
2. Semua teks deskriptif (bio, deskripsi masjid/kitab, `content`) wajib Bahasa Indonesia.
3. `content` ditulis padat satu paragraf untuk mesin pencari, bukan naratif.
4. Format slug `id` baru: huruf kecil, spasi/tanda baca → tanda hubung, dengan contoh.
5. Riset alamat lengkap untuk masjid baru (sebelumnya hanya kitab yang eksplisit disebut
   perlu riset).

Total tambahan ke `CLAUDE.md`: ±9 baris. Tidak ada data pribadi/sensitif disalin.

## 2. Untuk disatukan Auditor (lintas-repo atau praktik, TIDAK ditulis ke `CLAUDE.md` repo ini)

| Aturan (satu kalimat) | Sumber | Cakupan | Status | Usulan teks |
|---|---|---|---|---|
| Sebelum push perubahan skrip `run:` di workflow, simulasikan lokal jalur sukses dan jalur gagal sengaja dulu, baru percaya hasilnya di runner sungguhan. | Praktik (dipakai saat menambah smoke test `deploy.yml`, 1 Okt 2026) | Lintas-repo | Belum tertulis | "Validasi perubahan skrip workflow secara lokal (jalur sukses + jalur gagal sengaja) sebelum push ke CI sungguhan." |
| Untuk perubahan UI apa pun, uji visual di lebar 320/375/430px dengan screenshot sebelum push, tidak hanya saat ada gerbang tampilan eksplisit. | Praktik (dipakai saat revisi tombol "Tentang", 30 Sep–1 Okt 2026) | Lintas-repo | Sebagian — 320-430px sudah tertulis khusus untuk tombol "Tentang" di `CLAUDE.md` repo ini, belum sebagai praktik umum semua perubahan UI | "Untuk perubahan UI apa pun, uji visual di lebar 320/375/430px dengan screenshot sebelum push." |
| Jangan pernah mengarang hasil uji/verifikasi; bila alat atau akses tidak tersedia (mis. axe-core gagal terpasang, situs live tak terjangkau), katakan itu secara eksplisit, jangan menebak hasilnya. | Praktik, ditegaskan instruksi Auditor 3 Okt 2026 ("Bila axe-core tidak bisa dipasang, katakan itu") | Lintas-repo | Belum tertulis sebagai prinsip umum | "Jangan mengarang hasil uji/verifikasi; bila alat/akses tak tersedia, katakan itu secara eksplisit." |
| Bila status suatu hal (terutama verifikasi otomatis atau klaim relay antar-sesi) diragukan, lakukan verifikasi manual sendiri dulu, baru konfirmasikan ke Amal dan sesi Auditor — jangan langsung percaya klaim "sukses" dari jalur otomatis. | **[Keputusan Amal]** chat langsung: "dicatat saja. apapun yang statusnya diragukan, ambil aksi manual lalu konfirmasi ke saya serta sesi 'auditor project kajian'" | Lintas-repo | Sebagian — rule 2 "Aturan lintas-repo" (cakupan persetujuan, kutipan relay tidak cukup) dan rule 11 (keterbatasan akses situs live) sudah dekat, tapi belum eksplisit soal "ambil aksi manual saat ragu" | "Bila status sesuatu diragukan (termasuk klaim relay otomatis), verifikasi manual dulu sebelum konfirmasi ke Amal dan Auditor." |

## 3. Status Butir B dan C — **selesai** (koreksi 5 Okt 2026, lihat AUDIT-HANDOFF-2026-10-03-auditor.md bagian 3.1.1)

- **Butir B**: Amal konfirmasi "lanjut" langsung di chat PIC (3 Okt 2026). Dieksekusi: uji 404 pasca-deploy
  di `deploy.yml` jadi glob `AUDIT-HANDOFF-*.md`/`COORDINATION-NOTE-*.md`, divalidasi lokal (jalur sukses+gagal)
  sebelum push. Commit `811ce74`, run [#18](https://github.com/reconciler/catatankajian/actions/runs/37116186650) — **success** (diverifikasi via API Actions).
- **Butir C**: baseline axe-core selesai, lihat bagian 4 — 1 pelanggaran (`color-contrast`). Tindak lanjutnya di
  bagian 6.

## 4. Butir C — baseline axe-core (axe-core 4.13.0, via Playwright + Chromium lokal)

Diuji: beranda (`index.html`) dan satu halaman rekap
(`kajian-al-kohinoor-jaja-nurjanah-09-agustus-2026.html`), masing-masing lebar 320px dan
430px, tag `wcag2a`+`wcag2aa`. Server lokal (`python3 -m http.server`), bukan situs live
(sesi ini tidak bisa mengakses `reconciler.github.io`).

**Hasil: 1 pelanggaran (serius) di keempat kombinasi, sama persis di 320px dan 430px karena
sifatnya warna, bukan layout: `color-contrast`.**

- Beranda: 26 elemen. Terutama teks `color: var(--muted)` (`#6B7A8D`) di atas latar terang
  (`.reset`, `#resultCount`, tanggal kartu `.m`, `.page-info`, `.footer-updated`,
  `.footer-contribute`), plus chip tema (`.chip-theme`, warna `var(--sage)` `#4A7C59` di atas
  `rgba(74,124,89,.12)`).
- Rekap: 21 elemen, pola serupa (`.section-label`, `.timeline-year`, `.timeline-body`,
  `.pillar-desc`, `.ayat-ref`, `footer`) — kemungkinan warna muted yang sama dipakai lintas
  template rekap.

**Tidak diperbaiki langsung** — ini perubahan warna, bukan atribut aksesibilitas murni, jadi
termasuk "mengubah tampilan" dan menunggu keputusan Amal per instruksi Butir C
(`AUDIT-HANDOFF-2026-10-03-auditor.md` bagian 2.1). Tidak ada temuan lain (struktur
landmark/alt/label) di luar `color-contrast` pada kedua halaman ini.

Catatan: console menunjukkan `ERR_CERT_AUTHORITY_INVALID`/`ERR_TUNNEL_CONNECTION_FAILED` saat
memuat resource eksternal (kemungkinan Google Fonts) — ini artefak proxy TLS sandbox sesi ini,
bukan temuan aksesibilitas; browser pengguna sungguhan tidak akan mengalami ini.

## 5. Catatan

Tidak ada data pribadi/sensitif (isi CV, kontak, kredensial, token) disalin ke handoff ini —
semua butir di atas adalah aturan proses/praktik kerja atau temuan teknis publik, bukan data
pengguna.

## 6. Perbaikan color-contrast (instruksi 5 Okt, bagian 3.1 poin 2-5) — **ditahan, menunggu konfirmasi langsung**

AUDIT-HANDOFF-2026-10-03-auditor.md bagian 3 menulis "[Keputusan Amal] ... konfirmasi Amal sudah ada, tidak perlu
tanya lagi" — ini kutipan dari chat Amal dengan sesi Auditor, bukan konfirmasi langsung di chat PIC. Rule 1+2
"Aturan lintas-repo" (`CLAUDE.md`): perubahan tampilan tetap perlu konfirmasi Amal, dikonfirmasi di chat sesi
kerja repo itu sendiri — kutipan relay sesi lain tidak cukup. Konsisten dengan pola Butir B (3 Okt): PIC tanya
langsung ke Amal di chat PIC sebelum eksekusi, bukan menjalankan atas klaim relay.

**Status:** sudah disiapkan usulan perubahan warna minimal (target >= 4,5:1) untuk `--muted` (#6B7A8D) dan chip
tema (`--sage` di atas latar sage transparan) — lihat tabel di chat PIC. Menunggu "lanjut" Amal langsung di chat
PIC sebelum push ke `index.html`/`rekap/*.html`.
