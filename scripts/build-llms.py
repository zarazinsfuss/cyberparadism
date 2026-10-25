#!/usr/bin/env python3
"""Generate static/llms.txt and static/llms-full.txt from the site content.

Run by `mise run llms` (and therefore by `mise run build` and `mise run serve`).
No dependencies beyond the standard library; works on Python 3.8+.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
STATIC = os.path.join(ROOT, "static")

PALETTE = [
    ("Teal", "#008080", "Primary accent. Deep water, shade under canopy, links and emphasis on light surfaces."),
    ("Aquamarine", "#7FFFD4", "Shallow lagoon light. Highlights, selections, links on dark surfaces."),
    ("Jungle Green", "#29AB87", "Canopy and living systems. Secondary accent, active states, markers."),
    ("Turquoise", "#40E0D0", "Mid-water. Gradients between teal and aquamarine, hover states."),
    ("Cyan", "#00FFFF", "Pure signal light. Interface glow and holographic cues. Use sparingly."),
    ("Folly", "#FF004F", "The single vivid accent. Alerts, a lone flower, a warning light. Never more than one per scene."),
    ("Silver", "#C0C0C0", "Machined metal and hairlines."),
    ("Platinum", "#E5E4E2", "Ceramic surfaces, pale concrete, the ground of a light interface."),
    ("Charcoal", "#333333", "Ink, shadow, the ground of a dark interface."),
    ("White", "#FFFFFF", "Glare, cloud, blank material."),
]
SHAPES = [
    ("Sphere", "Habitats, craft, pressure vessels. Closed and complete."),
    ("Dome", "The enclave's signature. Shelter that admits the sky."),
    ("Cone", "Spires, towers and antennae reaching out of the canopy."),
    ("Pyramid", "Monumental calm. Stable mass against wild terrain."),
    ("Hexagon", "Enclosure and efficiency. The emblem's frame."),
    ("Helix", "Life engineering made visible. Ramps, towers, growth."),
    ("Lattice", "Glazing, shells and structure. Repetition without clutter."),
    ("Ring", "Atolls, stations, orbital terraces. A centre held open."),
    ("Branching", "Fractal columns and canopies. Structure that grew."),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def base_url():
    m = re.search(r'^base_url\s*=\s*"([^"]+)"', read(os.path.join(ROOT, "config.toml")), re.M)
    return m.group(1).rstrip("/")


BASE = base_url()


def split_front_matter(text):
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n?(.*)", text, re.S)
    if not m:
        return {}, text
    fm, body = m.group(1), m.group(2)
    data = {}
    section = ""
    current_array = None  # (key, list) for [[extra.terms]]-style arrays of tables
    for line in fm.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("[[") and s.endswith("]]"):
            key = s[2:-2]
            data.setdefault(key, []).append({})
            current_array = key
            section = ""
            continue
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1]
            current_array = None
            continue
        m2 = re.match(r'([A-Za-z_][\w-]*)\s*=\s*(.*)$', s)
        if not m2:
            continue
        key, raw = m2.group(1), m2.group(2).strip()
        if raw.startswith('"') and raw.endswith('"'):
            val = raw[1:-1]
        elif raw.startswith("["):
            val = re.findall(r'"([^"]*)"', raw)
        elif raw in ("true", "false"):
            val = raw == "true"
        else:
            try:
                val = int(raw)
            except ValueError:
                val = raw
        if current_array:
            data[current_array][-1][key] = val
        elif section:
            data[section + "." + key] = val
        else:
            data[key] = val
    return data, body.strip()


def page(path):
    data, body = split_front_matter(read(path))
    rel = os.path.relpath(path, CONTENT)
    if rel.endswith("/index.md"):
        url = rel[: -len("index.md")]
    elif rel.endswith("_index.md"):
        url = rel[: -len("_index.md")]
    else:
        url = rel[: -len(".md")] + "/"
    data["_url"] = BASE + "/" + url
    data["_body"] = body
    data["_path"] = path
    return data


def internal_link(target):
    # @/field-guide/palette.md#anchor -> https://.../field-guide/palette/#anchor
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    p = target[2:]
    if p.endswith("/_index.md"):
        p = p[: -len("_index.md")]
    elif p.endswith("/index.md"):
        p = p[: -len("index.md")]
    elif p.endswith(".md"):
        p = p[:-3] + "/"
    return BASE + "/" + p + anchor


def render_body(body, gallery_by_slug):
    out = []
    for line in body.splitlines():
        s = line.strip()
        if s in ("{% <note> %}", "{% </note> %}"):
            continue
        m = re.match(r'\{\{ <pieces slugs=\{\[(.*?)\]\} /> \}\}', s)
        if m:
            slugs = re.findall(r'"([^"]+)"', m.group(1))
            refs = ["%s (%s)" % (gallery_by_slug[x]["title"], gallery_by_slug[x]["_url"]) for x in slugs if x in gallery_by_slug]
            out.append("See in the gallery: " + "; ".join(refs) + ".")
            continue
        m = re.match(r'\{\{ <fig piece="([^"]+)"(?: caption="([^"]*)")? /> \}\}', s)
        if m:
            g = gallery_by_slug.get(m.group(1))
            if g:
                cap = (m.group(2) + " " if m.group(2) else "")
                out.append("Figure: %s%s (%s)." % (cap, g["title"], g["_url"]))
            continue
        if s == "{{ <palette /> }}":
            out.append("| Color | Hex | Role |")
            out.append("|---|---|---|")
            for n, h, r in PALETTE:
                out.append("| %s | %s | %s |" % (n, h, r))
            continue
        if s == "{{ <shapes /> }}":
            for n, d in SHAPES:
                out.append("- **%s**: %s" % (n, d))
            continue
        line = re.sub(r'\(@/([^)]+)\)', lambda mm: "(" + internal_link("@/" + mm.group(1)) + ")", line)
        line = re.sub(r"<cite>(.*?)</cite>", r"\1", line)
        line = re.sub(r"<[^>]+>", "", line) if "<dl" in line or "<dt" in line or "<dd" in line or "</dl" in line else line
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    manifesto = page(os.path.join(CONTENT, "manifesto.md"))
    about = page(os.path.join(CONTENT, "about.md"))
    contribute = page(os.path.join(CONTENT, "contribute.md"))
    guide_index = page(os.path.join(CONTENT, "field-guide", "_index.md"))
    chapters = sorted(
        (page(os.path.join(CONTENT, "field-guide", f)) for f in os.listdir(os.path.join(CONTENT, "field-guide")) if f.endswith(".md") and f != "_index.md"),
        key=lambda p: p.get("weight", 0),
    )
    gallery_index = page(os.path.join(CONTENT, "gallery", "_index.md"))
    pieces = []
    for d in sorted(os.listdir(os.path.join(CONTENT, "gallery"))):
        idx = os.path.join(CONTENT, "gallery", d, "index.md")
        if os.path.isfile(idx):
            p = page(idx)
            p["_slug"] = d
            pieces.append(p)
    pieces.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    by_slug = {p["_slug"]: p for p in pieces}

    desc = re.search(r'^description\s*=\s*"([^"]+)"', read(os.path.join(ROOT, "config.toml")), re.M).group(1)

    # ---- llms.txt ----
    L = []
    L.append("# Cyberparadism")
    L.append("")
    L.append("> " + desc)
    L.append("")
    L.append("Cyberparadism is a techno-optimist aesthetic that sets a small, highly advanced human enclave inside lush or dramatic nature. It took shape in online aesthetics communities, was formalized on the Aesthetics Wiki, and was given a manifesto in 2022. This site holds the founding manifesto, a field guide to the aesthetic's settings, visual language, shapes and palette, and a gallery of pieces with stated provenance. All text and images are dedicated to the public domain under CC0 1.0 and may be quoted, reused and remixed without attribution. Other names for the aesthetic: Cyber Paradise, Cybergenesis, Neogenesis.")
    L.append("")
    L.append("The full text of every page is available in one file at %s/llms-full.txt." % BASE)
    L.append("")
    L.append("## Manifesto")
    L.append("")
    L.append("- [%s](%s): %s" % (manifesto["title"], manifesto["_url"], manifesto["description"]))
    L.append("")
    L.append("## Field guide")
    L.append("")
    L.append("- [%s](%s): %s" % (guide_index["title"], guide_index["_url"], guide_index["description"]))
    for c in chapters:
        L.append("- [%s](%s): %s" % (c["title"], c["_url"], c["description"]))
    L.append("")
    L.append("## Gallery")
    L.append("")
    L.append("- [%s](%s): %s" % (gallery_index["title"], gallery_index["_url"], gallery_index["description"]))
    for p in pieces:
        L.append("- [%s](%s): %s %s, by %s." % (p["title"], p["_url"], p["description"], p.get("extra.method", ""), p.get("extra.creator", "")))
    L.append("")
    L.append("## Optional")
    L.append("")
    L.append("- [%s](%s): %s" % (about["title"], about["_url"], about["description"]))
    L.append("- [%s](%s): %s" % (contribute["title"], contribute["_url"], contribute["description"]))
    L.append("- [Source repository](https://github.com/zarazinsfuss/cyberparadism): Zola source for this site, issue forms for submissions.")
    L.append("- [RSS feed](%s/rss.xml)" % BASE)
    L.append("")

    # ---- llms-full.txt ----
    F = []
    F.append("# Cyberparadism: full text")
    F.append("")
    F.append("> " + desc)
    F.append("")
    F.append("Everything below is dedicated to the public domain under CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/). Canonical site: %s/. Index of pages: %s/llms.txt." % (BASE, BASE))
    F.append("")

    def section(p, heading_level=1, extra_lines=None):
        F.append("#" * heading_level + " " + p["title"])
        F.append("")
        F.append("Source: " + p["_url"])
        if p.get("description"):
            F.append("")
            F.append(p["description"])
        if extra_lines:
            F.append("")
            F.extend(extra_lines)
        body = render_body(p["_body"], by_slug)
        if body:
            F.append("")
            F.append(body)
        if p.get("extra.terms"):
            F.append("")
            for t in p["extra.terms"]:
                F.append("- **%s**: %s" % (t["name"], t["definition"]))
        F.append("")
        F.append("---")
        F.append("")

    section(manifesto)
    F.append("# Field guide")
    F.append("")
    F.append("Source: " + guide_index["_url"])
    F.append("")
    F.append(render_body(guide_index["_body"], by_slug))
    F.append("")
    for c in chapters:
        section(c, 2)
    F.append("# Gallery")
    F.append("")
    F.append("Source: " + gallery_index["_url"])
    F.append("")
    F.append(render_body(gallery_index["_body"], by_slug))
    F.append("")
    for p in pieces:
        prov = [
            "Creator: %s. Method: %s. Added: %s. Setting: %s. Motifs: %s. License: CC0 1.0." % (
                p.get("extra.creator", ""), p.get("extra.method", ""), p.get("extra.added", ""),
                ", ".join(p.get("taxonomies.settings", [])), ", ".join(p.get("taxonomies.motifs", [])),
            ),
            "Image: %s%s" % (p["_url"], p.get("extra.image", "")),
        ]
        section(p, 2, prov)
    section(about)
    section(contribute)

    os.makedirs(STATIC, exist_ok=True)
    with open(os.path.join(STATIC, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L).rstrip() + "\n")
    with open(os.path.join(STATIC, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(F).rstrip() + "\n")
    print("wrote static/llms.txt (%d lines) and static/llms-full.txt (%d lines)" % (len(L), len(F)))


if __name__ == "__main__":
    sys.exit(main())
