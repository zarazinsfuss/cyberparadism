![cyperparadism_hero.png](https://raw.githubusercontent.com/zarazinsfuss/cyberparadism-manifesto/main/cyberparadism_hero2.png)

# Cyberparadism | Website

This is the official [web presence](https://zarazinsfuss.github.io/cyberparadism/) of the Cyberparadism aesthetic that formerly originated on the Aesthetics Wiki. Cyberparadism is an aesthetics that typically depicts lush and untamed nature, wherein a small-numbered breakaway civilization uses advanced, but reasonably possible technology for self-preservation up to the point of luxurious comfort that enables them to live in a paradise, hence the name. Common themes are resource-based economy, genetic life engineering, terraformation, exoplanets or similar tropes of space frontier exploration.

**Link to the website:** [CYBERPARADISM: A techno-optimist aesthetic guiding us towards a possible future.](https://zarazinsfuss.github.io/cyberparadism/)

## Project Structure

The site is built using [Zola](https://www.getzola.org/), a fast static site generator written in Rust. The Cyberparadism website is structured as follows:

- `content/`: Contains all the markdown files which make up the content of the site.
- `static/`: Hosts all static content like images and icons.
- `templates/`: Holds the HTML templates that define the structure of different types of pages.
- `sass/`: Contains SCSS stylesheets compiled by Zola.
- `config.toml`: The main configuration file for the Zola site.
- `mise.toml`: Task runner and tool version management configuration.

## Contributing

We welcome all contributions to the Cyberparadism web presence! Whether it's adding content, improving the design, or fixing bugs, your input is valuable.

## Building the Site

This project uses [mise](https://mise.jdx.dev/) for tool version management and task running.

### Prerequisites

1. Install mise on your machine (see [mise documentation](https://mise.jdx.dev/getting-started.html))
2. Clone this repository
3. Run `mise trust` to trust the configuration
4. Run `mise install` to install Zola

### Development

```bash
# Serve the site locally with live reload
mise run serve

# Build the site for production
mise run build

# Check for broken links
mise run check

# Clean the public directory
mise run clean
```

The development server runs at `http://127.0.0.1:1111` by default.

## Reporting Issues

If you encounter any issues or have suggestions for improvements, please file an issue in this repository's Issue Tracker.

---

_Made with love in Switzerland, using [Zola](https://www.getzola.org/) and [GitHub](https://github.com)._
