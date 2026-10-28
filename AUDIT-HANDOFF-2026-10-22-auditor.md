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

## 5. Verifikasi lanjutan Auditor (23 Okt 2026) **[Terverifikasi kecuali disebut lain]**

- **Landmark `<header>`/`<main>` (`fcc89c4`, run #36 success):** Auditor mengulang uji pada `main`: screenshot halaman penuh **identik** (hash sama) dibanding `2fa531f` di 320/375/430 px, tinggi hero sama (151,4/151,4/152), axe semua aturan 0 pelanggaran (sebelumnya `landmark-one-main` dan `region`). Diterima.
- **Temuan Netlify (22 Okt):** project Netlify `catatankajian` masih terhubung ke repo dan membuat deploy production tiap push ke `main`, termasuk push yang hanya mengubah dokumen (deploy 22 Okt 03:17 UTC dari komit `ac67346`, "1 asset changed"). Kemungkinan seluruh isi repo ikut tayang di `netlify.app` **[inferensi, tidak terkonfirmasi]**. Amal melaporkan 23 Okt (chat Auditor) bahwa kedua project Netlify sudah ditangguhkan. Auditor memeriksa efeknya dengan melihat apakah push ini memicu deploy baru; hasilnya dicatat di handoff berikutnya.
- **Untuk PIC:** jangan menyatakan "Netlify tidak dipakai" di dokumen atau laporan tanpa bukti dari sisi Netlify. Jangan mengubah apa pun di Netlify. `CLAUDE.md` bagian awal sudah dikoreksi Auditor.

## 6. Verifikasi Auditor atas field `gender` di `ustadz[]` (28 Okt 2026; laporan PIC `AUDIT-HANDOFF-2026-10-28.md`)

Penanda: **[Diperiksa Auditor]** dijalankan Auditor sendiri; **[Laporan PIC]** tidak dijalankan ulang; **[Inferensi]** kesimpulan, bukan sumber.

- **[Diperiksa Auditor]** `data.json` `f750883` dibanding `caf8e31`: `ustadz[]` 50 entri, semua punya `gender` (L 48, P 2; tidak ada nilai lain). Di luar field itu, satu-satunya perubahan `ustadz[]` adalah entri baru `damar-wahyu-wijayanti-...` (rekap #70, penambahan rutin). `kitab[]` dan `themes[]` tidak berubah; `sessions[]` dan `masjid[]` bertambah satu karena rekap #70.
- **[Diperiksa Auditor]** Uji di Chromium (server lokal, jaringan luar diblokir): profil `aa-gym` menampilkan "USTADZ", `elma-fitria-st` "USTADZAH", `dr-jaja-nurjanah-m-a` "USTADZ" (setelah `gender` diisi). Label agregat tetap "Ustadz/Ustadzah" (hero-stats "50 Ustadz/Ustadzah", opsi filter, aria-label). 0 galat halaman. `ustadzLabel(u)` berfallback ke "Ustadz/Ustadzah" bila `gender` kosong.
- **[Diperiksa Auditor, via API Actions]** Run #47 sampai #51 `success` (head `f750883`).
- **[Laporan PIC, tidak dijalankan ulang]** axe 0 pelanggaran, `build_seo.py` tanpa diff lain.
- **[Inferensi, sama dengan pengakuan PIC]** 47 nilai awal diisi dari gelar, kunya, dan pola nama, tidak dicek per orang ke sumber publik; satu nilai (Dr. Jaja Nurjanah, M.A.) dari konfirmasi langsung Amal. Auditor membaca 48 nama berlabel L: tidak ada penanda nama perempuan (ustadzah, binti, Hj., Siti, dll.). Risiko residu: label keliru di profil publik satu orang bila ada nama yang sebenarnya perempuan; fallback gabungan bukan salah satu gender sehingga aman bila dikosongkan.
- **Klasifikasi wajib lapor: tepat** (perubahan skema `data.json`). Tidak ada tindak lanjut untuk PIC. Usulan ringan untuk Amal: bila ada nama yang ragu, cukup kosongkan `gender`-nya.

## 7. Verifikasi Auditor atas restrukturisasi filter `index.html` (28 Okt 2026; laporan PIC `AUDIT-HANDOFF-2026-10-28.md`, komit `08e15c1`..`f8eb320`)

Penanda: **[Diperiksa Auditor]** dijalankan Auditor sendiri; **[Laporan PIC]** tidak dijalankan ulang; **[Usulan]** menunggu keputusan Amal.

- **[Diperiksa Auditor]** Chromium, server lokal, jaringan luar diblokir, head `3fc1702`. **15/15 lulus:**
  - Accordion diuji lewat `getComputedStyle(...).display` (bukan atribut): tertutup default = `none`; klik "Filter" = `grid` dan `aria-expanded=true`; klik lagi = `none`.
  - Baris chip: "Semua" + 8 tema; angka tiap chip = jumlah sesi di `data.json` (33, 9, 9, 5, 4, 4, 4, 2); urut dari terbanyak.
  - Kaskade: untuk **ke-8 tema**, opsi dropdown masjid/ustadz/kitab = himpunan yang Auditor hitung sendiri dari `data.json`; ganti tema mereset masjid yang tak punya sesi di tema baru.
  - axe 0 pelanggaran dan tanpa geser horizontal pada 320/375/430 px, terang dan gelap, dengan accordion tertutup, terbuka, dan tema terpilih; 0 galat halaman.
- **[Diperiksa Auditor, via API Actions]** Run `success` untuk kelima komit dan head.
- **[Diperiksa Auditor] Bug accordion yang dilaporkan PIC terbukti dan sudah benar diperbaiki:** pemindai Auditor (elemen berstatus `hidden` yang `display`-nya bukan `none`) mendeteksi `#filterBar` = `grid` pada `6a17ce8` dan 0 temuan pada head. Pemindai yang sama dijalankan di keempat situs (lihat bagian bersama di bawah).
- **[Temuan Auditor, keparahan rendah, bukan regresi berat; [Usulan]]** Tautan dengan kombinasi tema + masjid yang tidak punya sesi bersama (contoh: `#/?theme=aqidah&masjid=al-ikhlas-dukuh-bima`, sesi sebenarnya 0) menghasilkan keadaan tak konsisten: chip "Aqidah" aktif, badge Filter "1" dan ringkasan menyebut masjid, tetapi dropdown masjid menampilkan "Semua Masjid" (opsinya tersaring), dan hasil "0 dari 70 sesi" tanpa penjelasan. UI sendiri tidak bisa membuat kombinasi ini (chip mereset); hanya tautan buatan tangan atau tautan lama. **Usulan perbaikan:** setelah membaca URL (`state` dari query), terapkan reset yang sama dengan klik chip (`themeFilteredLists`), atau tampilkan pesan hasil kosong. Aplikasi memang tidak punya pesan hasil kosong sebelum perubahan ini juga (dicek di `9bba790`). Perubahan ini menyentuh perilaku, jadi menunggu keputusan Amal; tidak mendesak.
- **[Laporan PIC, tidak dijalankan ulang]** `build_seo.py` tanpa diff lain di semua komit.
- **Tampilan berubah signifikan** (baris chip + accordion); belum dilihat di perangkat nyata (aturan 11).
