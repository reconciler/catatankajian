# Handoff PIC — 2026-10-28

Dari: sesi kerja `catatankajian` (session_01EK9Yre85jZnzA9fKsiqXA7)
Untuk: sesi "Auditor Project"
Konteks: perubahan skema `data.json` (wajib lapor, bukan sekadar entri rutin).

## Perubahan skema: field `gender` baru di `ustadz[]`

Diminta Amal langsung di chat PIC — dua langkah:

1. **Commit `47bcb7b`**: label UI "Ustadz" (generik, tidak inklusif — ada presenter perempuan di
   data) diganti "Ustadz/Ustadzah" di semua tempat (placeholder search, filter dropdown, hero-stats,
   entity header). Perbaikan teks, tanpa skema.
2. **Commit `9cc6c70`** (ini yang wajib lapor): field `gender` baru, opsional, nilai `"L"`/`"P"`, di
   tiap objek `ustadz[]`. `index.html` memakainya lewat fungsi baru `ustadzLabel(u)`: `"Ustadzah"`
   bila `gender==="P"`, `"Ustadz"` bila `"L"`, fallback label gabungan `"Ustadz/Ustadzah"` bila kosong
   — dipakai **hanya** di entity header (halaman profil satu orang). Label agregat (hero-stats, filter
   dropdown, placeholder) sengaja tetap gabungan karena mewakili campuran, bukan satu individu.

**Cara mengisi 49/50 entri** (kesimpulan sendiri, bukan hasil riset web per orang): digolongkan dari
gelar/kunya/pola nama yang secara konvensi Indonesia/Arab sangat kuat menunjukkan gender —
`KH.`/`H.`/`Buya` (gelar laki-laki eksklusif), kunya `Abu ...`/`bin ...` (laki-laki), dan untuk 2 nama
perempuan (Elma Fitria, Damar Wahyu Wijayanti) dari pola nama + konteks topik sesi. **Tidak** di-cross-check
satu-satu ke sumber publik per orang — risiko kekeliruan ada meski kecil untuk pola yang sudah sangat baku.

**1 entri sengaja dibiarkan kosong**: `dr-jaja-nurjanah-m-a` (Dr. Jaja Nurjanah, M.A.) — nama depan
"Jaja" punya preseden dipakai laki-laki di Indonesia, dan bio menyebut pernah jadi "khatib" (peran
tradisinya laki-laki), jadi genuinely ambigu. Dicoba verifikasi web (dicari "Jaja Nurjanah" + UPN
Veteran Jakarta/Muhammadiyah Jawa Barat) — tidak ketemu sumber yang bisa mengonfirmasi. **Ditanyakan
ke Amal langsung di chat PIC**, bukan ditebak. UI-nya aman untuk kasus ini (fallback ke label gabungan,
bukan salah satu gender yang salah).

## Validasi sebelum push

`build_seo.py`: tidak ada diff lain, JSON tetap valid. axe-core 0 pelanggaran, 0 error JS. Fungsional:
3 kasus diuji (gender `"L"` -> "Ustadz", `"P"` -> "Ustadzah", kosong -> fallback gabungan) — semua benar.
Label agregat dipastikan tidak berubah jadi salah satu gender.

## Update: 50/50 terisi (komit `5835eb5`, run [#50 success](https://github.com/reconciler/catatankajian/actions/runs/40608241187))

Amal konfirmasi langsung di chat PIC: **"Beliau ustadz"** — `dr-jaja-nurjanah-m-a` diisi `"L"`.
Semua 50 entri `ustadz[]` sekarang punya `gender` terisi. Tidak ada lagi yang menunggu.

## Yang perlu diketahui (bagian gender)

- Field `gender` **opsional** di skema, tapi saat ini 50/50 ustadz sudah terisi.
- Untuk entri `ustadz[]` baru ke depan: isi `gender` hanya kalau cukup yakin (didokumentasikan di
  `CLAUDE.md` langkah 1 alur kerja); kalau ragu, biarkan kosong — jangan mengarang, tanya Amal.
- Tidak ada data pribadi/sensitif di luar yang memang sudah publik di `data.json` (nama narasumber
  kajian umum, bukan data pribadi rahasia).

## Perubahan besar `index.html`: tema jadi filter upfront (bukan penambahan data rutin)

Diminta Amal langsung di chat PIC (brainstorm → mockup Artifact canvas 2+1 opsi → pilih → implementasi
bertahap, beberapa commit). Melaporkan karena ini restrukturisasi UI/UX dashboard, bukan entri rutin.

**Commit `08e15c1`** — tema jadi baris chip (scroll horizontal, "Jelajahi Tema") tepat di bawah
disclaimer, bukan dropdown ke-4. Filter bar sisa 3 dropdown (masjid/ustadz-ustadzah/kitab).

**Commit `6a17ce8`** — 3 dropdown sisanya disembunyikan di balik tombol "Filter" (accordion, pola
toggle sama seperti "Tentang"), collapsed default. Badge angka + ringkasan nama tetap tampil saat
filter aktif meski accordion ditutup.

**Commit `7f4ff25`** — **bug nyata, laporan Amal** (akses live via Brave in-app browser dari link bio
Instagram): accordion tidak bisa dibuka/tutup. Akar masalah: `.filterbar{display:grid}` (CSS situs)
dan `[hidden]{display:none}` (bawaan browser) punya spesifisitas sama — aturan situs menang di seri
ini, jadi atribut `hidden` ter-set benar oleh JS tapi `computedDisplay` tetap `grid`, elemen tidak
pernah benar-benar sembunyi. **Celah pengujian saya sendiri**: validasi sebelumnya cuma cek atribut
`.hidden`, bukan `getComputedStyle().display` (tampilan sungguhan) — lolos tanpa terdeteksi sampai
dicek manual oleh Amal. Diperbaiki: `.filterbar[hidden]{display:none}` (spesifisitas lebih tinggi).
**Dicatat sebagai praktik untuk diri sendiri ke depan**: validasi visibilitas via `getComputedStyle`,
bukan cuma atribut DOM. Commit yang sama juga mengurutkan chip tema dari jumlah sesi terbanyak dan
memendekkan labelnya ke istilah paling umum dipahami awam (mapping terpisah, tidak mengubah nama
lengkap di `data.json`).

**Commit `f8eb320`** — tema jadi filter utama untuk kaskade: opsi masjid/ustadz/kitab di accordion
otomatis dipersempit ke yang punya sesi di tema terpilih. **Keputusan Amal langsung di chat**: kalau
pilihan yang sudah ada jadi tidak valid setelah ganti tema, direset otomatis (bukan dibiarkan jadi
kombinasi tak valid). Lingkup sengaja dibatasi: masjid/ustadz/kitab tidak saling mempersempit satu
sama lain, cuma mengikuti tema — ditanya soal full bidirectional faceting (tiap filter saling
terkoneksi), direkomendasikan tidak dikerjakan di repo ini (dataset kecil — 70 sesi, kompleksitas
tidak sepadan manfaatnya di skala ini), Amal belum meminta itu dikerjakan.

**Validasi tiap commit** (lokal, sebelum push): `build_seo.py` tidak ada diff lain di semua commit;
axe-core 0 pelanggaran di 320/375/430px di semua commit; tidak ada scroll horizontal; search tetap
jalan; 0 error JS. Commit `f8eb320` diuji dengan skenario nyata dari `data.json` (tema "Isu
Kontemporer" → masjid "Al Fattah" [hanya ada di tema itu] → ganti ke "Aqidah" → masjid ter-reset
otomatis, hasil tetap benar). Semua run Actions terkait: success, diverifikasi satu per satu.

## Yang perlu diketahui (bagian filter)

- Tampilan berubah signifikan (chip row + accordion) — belum dilihat di perangkat nyata oleh Amal;
  per rule 11, dianggap tidak bermasalah sampai ada laporan sebaliknya.
- Bug accordion di atas: pelajaran untuk sesi mana pun yang menambah toggle show/hide berbasis
  atribut `hidden` — selalu pastikan tidak ada aturan CSS lain dengan `display` eksplisit pada
  elemen yang sama (spesifisitas sama = aturan penulis menang atas `[hidden]` bawaan browser).
