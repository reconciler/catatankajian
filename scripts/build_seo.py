#!/usr/bin/env python3
"""
Regenerate SEO artifacts for Catatan Kajian dari data.json:
  1. sitemap.xml (index + seluruh kajian-*.html)
  2. JSON-LD (WebSite + ItemList) di index.html, antara marker LD_JSON_START/END
  3. Per file kajian-*.html: OG/Twitter tags + favicon link + JSON-LD Article,
     antara marker SEO_BLOCK_START/END (idempotent — dihapus & ditulis ulang tiap run)

Jalankan setelah data.json diperbarui (sesi baru ditambah/diubah):
    python3 scripts/build_seo.py

Jangan edit manual apa pun di antara marker SEO_BLOCK_START/END atau
LD_JSON_START/END — akan tertimpa saat script ini dijalankan lagi.
"""
import json
import re
import os

BASE = "https://catatankajian.netlify.app"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BULAN_ID = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


def fmt_tanggal(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {BULAN_ID[int(m)]} {y}"


def load_data():
    with open(os.path.join(REPO_ROOT, "data.json"), encoding="utf-8") as f:
        return json.load(f)


def build_sitemap(data):
    # Rekap (kajian-*.html) di-host di branch Catatan (GitHub Pages), BUKAN di
    # branch main/Netlify -- pakai recapUrl apa adanya dari data.json, jangan
    # direkonstruksi dengan BASE (yang cuma benar untuk index.html sendiri).
    urls = [{"loc": f"{BASE}/", "lastmod": data["generatedAt"], "changefreq": "weekly", "priority": "1.0"}]
    for s in data["sessions"]:
        urls.append({"loc": s["recapUrl"], "lastmod": s["date"], "changefreq": "monthly", "priority": "0.7"})

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    path = os.path.join(REPO_ROOT, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(urls)


def build_index_jsonld(data):
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Catatan Kajian",
        "url": f"{BASE}/",
        "inLanguage": "id",
        "description": "Dashboard pencarian catatan kajian Islam — telusuri rekap kajian berdasarkan masjid, ustadz, kitab, dan tema di Jabodetabek dan sekitarnya.",
    }

    items = []
    for i, s in enumerate(sorted(data["sessions"], key=lambda x: x["date"], reverse=True), start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": s["recapUrl"],
            "name": s["title"],
        })
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Arsip Catatan Kajian",
        "itemListElement": items,
    }

    block = (
        "<!--LD_JSON_START-->\n"
        f'<script type="application/ld+json">{json.dumps(website, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        f'<script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        "<!--LD_JSON_END-->"
    )

    path = os.path.join(REPO_ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "<!--LD_JSON_START-->" in content:
        content = re.sub(
            r"<!--LD_JSON_START-->.*?<!--LD_JSON_END-->",
            block.replace("\\", "\\\\"),
            content,
            flags=re.DOTALL,
        )
    else:
        content = content.replace("</head>", block + "\n</head>")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return len(items)


def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def build_kajian_pages(data):
    """File kajian-*.html sekarang di-host di branch Catatan (GitHub Pages),
    bukan di branch main lagi. Fungsi ini jadi no-op kalau dijalankan di main
    (tidak ada file untuk diproses) -- itu normal. Kalau perlu regenerasi
    OG/JSON-LD file rekap, jalankan script ini di checkout branch Catatan."""
    masjid_by_id = {m["id"]: m for m in data["masjid"]}
    theme_by_id = {t["id"]: t["name"] for t in data["themes"]}

    updated = 0
    skipped = 0
    for s in data["sessions"]:
        fname = s["recapUrl"].rstrip("/").split("/")[-1]
        path = os.path.join(REPO_ROOT, fname)
        if not os.path.exists(path):
            skipped += 1
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        m = re.search(r'<meta name="description" content="(.*?)">', content)
        description = m.group(1) if m else f"Catatan kajian: {s['title']}"

        canonical_url = s["recapUrl"]
        masjid = masjid_by_id.get(s["masjidId"])
        theme_name = theme_by_id.get(s["theme"], s["theme"])

        article = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": s["title"],
            "description": description,
            "datePublished": s["date"],
            "inLanguage": "id",
            "isAccessibleForFree": True,
            "url": canonical_url,
            "about": theme_name,
            "author": {"@type": "Person", "name": s["ustadzRaw"]},
        }
        if masjid:
            article["contentLocation"] = {
                "@type": "Place",
                "name": masjid["name"],
                "address": masjid.get("address"),
            }
        if s.get("kitab"):
            article["mentions"] = {"@type": "Book", "name": s["kitab"]}

        block = (
            "<!--SEO_BLOCK_START-->\n"
            f'<meta property="og:type" content="article">\n'
            f'<meta property="og:title" content="{esc_attr(s["title"])}">\n'
            f'<meta property="og:description" content="{esc_attr(description)}">\n'
            f'<meta property="og:url" content="{canonical_url}">\n'
            f'<meta property="og:image" content="{BASE}/og-image.png">\n'
            f'<meta property="og:locale" content="id_ID">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{esc_attr(s["title"])}">\n'
            f'<meta name="twitter:description" content="{esc_attr(description)}">\n'
            f'<meta name="twitter:image" content="{BASE}/og-image.png">\n'
            f'<link rel="icon" type="image/svg+xml" href="{BASE}/favicon.svg">\n'
            f'<script type="application/ld+json">{json.dumps(article, ensure_ascii=False, separators=(",", ":"))}</script>\n'
            "<!--SEO_BLOCK_END-->"
        )

        if "<!--SEO_BLOCK_START-->" in content:
            new_content = re.sub(
                r"<!--SEO_BLOCK_START-->.*?<!--SEO_BLOCK_END-->",
                block.replace("\\", "\\\\"),
                content,
                flags=re.DOTALL,
            )
        else:
            new_content, n = re.subn(
                r'(<meta name="description" content="[^"]*">)',
                r"\1\n" + block.replace("\\", "\\\\"),
                content,
                count=1,
            )
            if n == 0:
                print(f"WARNING: tidak ketemu titik insersi (meta description) di {fname}, dilewati")
                continue

        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1

    return updated


def main():
    data = load_data()
    n_urls = build_sitemap(data)
    n_items = build_index_jsonld(data)
    n_pages = build_kajian_pages(data)
    print(f"sitemap.xml: {n_urls} URL")
    print(f"index.html JSON-LD: {n_items} item ItemList")
    print(f"Halaman rekap diperbarui: {n_pages}")


if __name__ == "__main__":
    main()
