# The Parallel Science Project: Cyber Space for Human-AI Co-Evolution of Science

[![Parallel ArXiv](https://img.shields.io/badge/Parallel%20ArXiv-PX%3A2604.00017-b31b1b)](https://papers.parallelscience.org/abs/2604.00017)
[![PDF](https://img.shields.io/badge/PDF-paper-b31b1b)](https://parallelscience.github.io/preprint/paper.pdf)
[![Mission Control](https://img.shields.io/badge/Mission%20Control-live-green)](https://orion.taila855ba.ts.net)

LaTeX source for the Parallel Science preprint, published on [Parallel ArXiv](https://papers.parallelscience.org/abs/2604.00017).

## Publishing

Editing and pushing `main.tex` to master does **not** trigger a Parallel ArXiv update. To publish a new version:

```bash
# Preview (compile PDF + update docs/ but don't push)
./publish.sh --dry

# Publish (compile + push to gh-pages → Pages rebuild → Parallel ArXiv re-scrape)
./publish.sh
```

This compiles the PDF, extracts title/author/abstract/date from `main.tex`, updates the GitHub Pages site on the `gh-pages` branch, and triggers a new version on Parallel ArXiv.

## Building locally

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Links

- [Parallel Science](https://parallelscience.org)
- [Parallel ArXiv](https://papers.parallelscience.org)
- [Mission Control](https://orion.taila855ba.ts.net)
- [GitHub Pages site](https://parallelscience.github.io/preprint/)
