# Instruksi Auditor, 22 Okt 2026: proyek baru Kenali Calon dan sinkronisasi empat repo (catatankajian)

Dari: sesi "Auditor Project". Untuk: sesi kerja (PIC) repo ini. Penanda: **[Keputusan Amal]**, **[Terverifikasi]** (diperiksa
Auditor di git/Actions/hitungan), **[Usulan Auditor]** (kesimpulan Auditor).

## 1. Dasar dan batas

- **[Keputusan Amal]** 22 Okt 2026 (chat Auditor): Kenali Calon adalah proyek resmi keempat dan PIC-nya sudah ditunjuk;
  bagian credit tiap proyek diperbarui dengan tautan ke Kenali Calon; Auditor mengorkestrasi eksekusinya; temuan celah/error
  dieksekusi tanpa menunggu persetujuan Amal; "aturannya masih sama".
- **[Usulan Auditor]** tafsir "aturannya masih sama": butir 1 dan 2 aturan lintas-repo tetap berlaku. Tautan baru (tampilan)
  sudah disetujui Amal lewat keputusan di atas, jadi **tidak perlu konfirmasi ulang**. Pengecualian butir 2 (pipeline/`deploy.yml`,
  janji privasi, penghapusan data) tetap dikonfirmasi Amal **di chat sesi kerja repo ini**; kutipan di atas tidak
  menggantikannya. Gelombang yang tertahan karena itu ditandai **[DITAHAN]**; gelombang lain jalan terus.
- `CLAUDE.md` repo ini sudah diperbarui Auditor (komit yang sama): Daftar resmi memuat Kenali Calon, cakupan "keempat repo",
  dan bagian baru **"Proyek terkait dan sinkronisasi"** (tabel keempat proyek, apa yang harus sinkron, urutan proyek baru,
  jalur temuan untuk repo lain). Baca bagian itu dulu. Jalankan `git pull --rebase origin main` sebelum edit dan sebelum push.
- Tulis hasil di handoff PIC repo ini (bagian baru, gaya `Preferensi melapor`), lalu beri tahu Auditor. Jalur andal = git.

## 2. Tugas (satu push per gelombang; tiap push: verifikasi run `success`)

### Gelombang 1: tautan Kenali Calon (tampilan, disetujui Amal)
1. `index.html`, `.menu-panel`, bagian "Proyek lain": tambah setelah "Bikin CV Taaruf"
   `<a class="menu-link" href="https://reconciler.github.io/kenalicalon/" target="_blank" rel="noopener noreferrer">Kenali Calon</a>`.
   Label dan URL persis Daftar resmi.
2. Uji: validasi di alur kerja `CLAUDE.md`; `python3 scripts/build_seo.py` (harapan: tidak ada selisih lain); axe-core 320 dan 430
   (panel tertutup dan terbuka) harapan 0 pelanggaran; tinggi header sebelum = sesudah di 320/375/430; panel terbuka tidak
   terpotong di 320; pencarian tetap jalan. Sebut "tampilan berubah" (butir 11). Repo ini terbit di tiap push ke `main`.

### Gelombang 2: catatan keadaan
- Komit `4680c2c` (11 Okt, langkah cek canonical di `deploy.yml`) dibuat tanpa catatan konfirmasi Amal untuk perubahan pipeline
  (butir 2). **[Terverifikasi]** run #29 sukses dan cek berjalan setelah terbit. Catat di handoff: sudah dikonfirmasi Amal di
  chat PIC atau belum. Bila belum, gabungkan pertanyaannya dengan gelombang 3 (satu kalimat).
- Komit 10 sampai 11 Okt datang dari tiga sesi berbeda. Siapa pun yang bekerja di repo ini wajib membaca `CLAUDE.md` dan handoff
  terbaru dulu (bagian baru "Proyek terkait dan sinkronisasi" menegaskan git sebagai pegangan, bukan ID sesi).

### Gelombang 3: penjaga aset yang dirujuk `index.html` **[DITAHAN: pipeline]**
- Celah **[Terverifikasi]** dari pembacaan `deploy.yml` baris 107 sampai 119: daftar berkas top-level yang diuji diturunkan dari
  isi `_site/`, jadi berkas yang dirujuk `index.html` (mis. `data.json`, `lib/fuse.min.js`, `og-image.png`) tetapi lupa di-`cp`
  tidak pernah diuji. Simulasikan lokal sebelum mengubah (hapus satu berkas dari `_site/` sambil `index.html` tetap merujuknya).
- Perbaikan: langkah uji tambahan yang mengumpulkan aset lokal yang dirujuk `index.html` (script/link/`og:image`, serta berkas
  yang diambil JS seperti `data.json`) dan wajib 200; sampel rujukan aset di 2 sampai 3 halaman `rekap/`. Pola kerja:
  `deploy.yml` repo `kenalicalon`, langkah 4d dan 5. Berjalan setelah terbit; uji lain tidak dilonggarkan. Simulasikan jalur
  sukses dan gagal lokal. Satu push khusus.
- **Syarat:** satu kalimat ke Amal di chat PIC (boleh digabung dengan pertanyaan gelombang 2). Tanpa "ya", jangan push.

## 3. Lapor
Handoff PIC bagian baru: tabel gelombang, hasil uji (angka), run, hal yang menunggu Amal. Setelah selesai, beri tahu Auditor.

## 4. Verifikasi Auditor atas hasil PIC (22 Okt 2026, sore) **[Terverifikasi: git, Actions, uji ulang Auditor]**

| Butir | Hasil |
|---|---|
| Gelombang 1 (`380a6dd`) | Diff `index.html`: satu baris, tautan Kenali Calon, `rel="noopener noreferrer"`, `target="_blank"`. Tinggi `.hero` 151,4/151,4/152 px sama sebelum dan sesudah; axe WCAG A/AA 0 pelanggaran dengan panel tertutup dan terbuka (320 dan 430). |
| Gelombang 2 | Ratifikasi `4680c2c` tercatat di handoff PIC ("ya" di chat PIC 22 Okt). Diterima. |
| Gelombang 3 (`b66c872`) | Diff `deploy.yml` hanya penambahan (44 baris), uji lain tidak dilonggarkan, berjalan setelah terbit. Run #33 dan #34 success. Konfirmasi Amal di chat PIC tercatat. Diterima. Sampel 3 rekap cukup (aset bersama); tidak perlu diperluas. |
| Kebiasaan baik | Kesalahan sendiri (process substitution menelan exit code python) dilaporkan dan diperbaiki sebelum push. Dicatat sebagai praktik: cek exit code skrip bantu secara eksplisit. |

### Usulan opsional (keputusan PIC, butir 1; tanpa efek visual)
- axe dengan semua aturan (bukan hanya WCAG A/AA) di `index.html` menunjukkan `landmark-one-main` (1) dan `region` (11-12) **sebelum dan sesudah** perubahan ini, jadi bukan akibat tautan baru. Menambah landmark `<main>` seperti yang dilakukan jadwalkajian (butir C, 3 Okt) menghapusnya. Syarat: tangkapan layar identik (perbandingan piksel) dan tinggi header tak berubah. Kerjakan bila PIC menilai layak; catat hasilnya.
