# Cyberparadism · website

The home of the Cyberparadism aesthetic on the web: the founding manifesto, a field guide to the aesthetic's settings, visual language, shapes and palette, and a gallery of pieces with their provenance.

**Site:** https://zarazinsfuss.github.io/cyberparadism/

Cyberparadism is a techno-optimist aesthetic that sets a small, highly advanced human enclave inside lush and untamed nature, where mature technology quietly provides abundance. It took shape in online aesthetics communities, was formalized on the Aesthetics Wiki, and was given a manifesto in 2022.

## Structure

The site is built with [Zola](https://www.getzola.org/).

```
content/
  _index.md              front page copy and the three doors
  manifesto.md           founding document (2022), lightly copyedited
  contribute.md          what fits, provenance, license, how to submit
  about.md               colophon, timeline, emblem, build notes
  field-guide/           nine reference chapters, ordered by weight
  gallery/<slug>/        one folder per piece: index.md + the JPEG master
  articles/_index.md     redirect kept for old links
templates/               Tera templates, partials and shortcodes
sass/style.scss          design tokens, day and night themes, components
static/                  fonts (self-hosted, OFL), icons, social image
```

Gallery images are resized at build time from the masters in `content/gallery/`; the derivatives land in `static/processed_images/`, which is ignored by git. `scripts/build-llms.py` generates `static/llms.txt` and `static/llms-full.txt` from the content before every build, so AI tools can read the site as plain text; both files are ignored by git as well.

## Contributing

Artwork and writing are welcome. The [contribute page](https://zarazinsfuss.github.io/cyberparadism/contribute/) explains what fits, how provenance is stated and the CC0 terms. Use the issue forms for an [artwork](https://github.com/zarazinsfuss/cyberparadism/issues/new?template=artwork-submission.yml) or [article](https://github.com/zarazinsfuss/cyberparadism/issues/new?template=article-submission.yml) submission, or open a pull request.

## Building

Tool versions and tasks are managed with [mise](https://mise.jdx.dev/).

```bash
mise trust && mise install   # installs Zola
mise run serve               # http://127.0.0.1:1111 with live reload
mise run build               # production build into public/ (runs the llms task first)
mise run check               # build plus link check
mise run llms                # regenerate static/llms.txt and static/llms-full.txt
mise run clean               # remove public/ and all generated files
```

Pushes to `main` are deployed to GitHub Pages by the workflow in `.github/workflows/`.

## License

All text and images are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). The fonts (Newsreader, Sora) are under the SIL Open Font License.

Made in Switzerland.
