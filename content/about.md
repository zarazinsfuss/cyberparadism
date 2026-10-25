+++
title = "About"
description = "What this site is, where the aesthetic came from, who maintains it, and how it is built."
date = 2026-10-25

[extra]
eyebrow = "Colophon"
+++

## The project

This is the home of the Cyberparadism aesthetic on the web. It holds the founding [manifesto](@/manifesto.md), a [field guide](@/field-guide/_index.md) to the aesthetic's settings, visual language, shapes and palette, and a [gallery](@/gallery/_index.md) of pieces with their provenance. The aim is to be the reference people reach for when they want to understand, recognize or make Cyberparadism.

## Names

The aesthetic is also called **Cyber Paradise**, **Cybergenesis** and **Neogenesis** (or Neogenesism). Usage varies by community; this site uses Cyberparadism throughout.

## Timeline

| When | What |
|---|---|
| 2010s | The aesthetic takes shape in online aesthetics communities and is formalized as an entry on the Aesthetics Wiki. |
| April 2023 | The [Cyberparadism Manifesto](https://github.com/zarazinsfuss/cyberparadism-manifesto) is published on GitHub; the eight Laws and the Signs follow in May, the resources section in November. |
| January 2024 | The first version of this website goes live. |
| December 2025 | The site is rebuilt with Zola; the gallery and the first encyclopedic article are added. |
| October 2026 | Relaunch: a new design that follows the aesthetic's own palette and shape language, the field guide, and a gallery with per-piece provenance. |

## The emblem

<figure>
  <img src="/img/emblem-original.png" alt="The original Cyberparadism emblem: a hexagonal badge containing a lotus flower above stylized waves, with stars above." width="256" height="256" style="width: 128px; height: 128px; background: #E5E4E2; padding: 12px">
  <figcaption>The original raster emblem. The site's header uses a vector redrawing of it.</figcaption>
</figure>

The emblem is a hexagon holding a lotus over water under a starry sky. The hexagon stands for enclosure and efficiency, the shape the aesthetic returns to most. The lotus is life emerging clean from water, a long-standing image of renewal. The waves are the lagoon and the coast. The stars are the frontier.

## The site

The design follows the aesthetic it describes: the imagery is the wilderness, the interface is the enclave. Small, precise, quiet. Text never sits on top of a photograph, there is one motif per page at most, and nothing moves unless you ask it to.

- **Palette**: the ten colors from the [field guide](@/field-guide/palette.md). A day theme on platinum with teal accents, and a night theme on charcoal with aquamarine accents. The toggle in the header switches between them; the choice is remembered in your browser only.
- **Type**: [Newsreader](https://github.com/productiontype/Newsreader) for reading and [Sora](https://github.com/sora-xor/sora-font) for labels, both under the SIL Open Font License and served from this site, with no third-party requests.
- **Build**: [Zola](https://www.getzola.org/), a static site generator. Images are resized at build time from the originals in the repository; no scripts or trackers are loaded.
- **Machine-readable**: a sitemap, an RSS feed, JSON-LD structured data on every page, and [llms.txt](/llms.txt) with [llms-full.txt](/llms-full.txt) so that AI tools can read the whole site as plain text.
- **Hosting**: GitHub Pages, deployed on every push to the main branch. The source is on [GitHub](https://github.com/zarazinsfuss/cyberparadism), and every page has an edit link at the bottom.

## License

All text and images on this site are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Attribution is appreciated but not required. The fonts remain under their own open license.

## Maintainer and contact

The site is maintained by zarazinsfuss and made in Switzerland. Questions, corrections and proposals are best raised as [issues on GitHub](https://github.com/zarazinsfuss/cyberparadism/issues). The [contribute page](@/contribute.md) explains how to add artwork or writing.
