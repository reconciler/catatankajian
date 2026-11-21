#!/usr/bin/env bash
# Susun folder _site/ berisi HANYA berkas publik situs.
#
# Dipakai dua kali di .github/workflows/deploy.yml (sejak 21 Nov 2026):
#   - job "build": isi _site/ yang di-upload sebagai artifact dan diterbitkan;
#   - job "deploy": menyusun ulang _site/ dari commit yang sama untuk uji pasca-deploy.
# Satu sumber daftar berkas, supaya isi yang diuji = isi yang diterbitkan.
#
# Menambah berkas/folder situs baru? Tambahkan di sini (lihat CLAUDE.md,
# bagian "Berkas yang tayang di situs").
#
# Jalankan dari root repo: bash scripts/susun_site.sh
set -euo pipefail

if [ ! -f index.html ] || [ ! -f data.json ]; then
  echo "susun_site.sh: jalankan dari root repo (index.html/data.json tidak ditemukan)" >&2
  exit 1
fi

rm -rf _site
mkdir -p _site
cp index.html data.json og-image.png favicon.svg robots.txt sitemap.xml _site/
cp -r rekap _site/rekap
if [ -d lib ]; then cp -r lib _site/lib; fi
# Berkas internal (CLAUDE.md, AUDIT-HANDOFF-*.md, COORDINATION-NOTE-*.md,
# scripts/, .github/) SENGAJA tidak disalin -- tidak boleh tayang publik.
