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

## Yang perlu diketahui

- Field `gender` **opsional** di skema, tapi saat ini 50/50 ustadz sudah terisi.
- Untuk entri `ustadz[]` baru ke depan: isi `gender` hanya kalau cukup yakin (didokumentasikan di
  `CLAUDE.md` langkah 1 alur kerja); kalau ragu, biarkan kosong — jangan mengarang, tanya Amal.
- Tidak ada data pribadi/sensitif di luar yang memang sudah publik di `data.json` (nama narasumber
  kajian umum, bukan data pribadi rahasia).
