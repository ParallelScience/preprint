#!/usr/bin/env python3
"""Extract metadata from main.tex and update docs/index.html + docs/paper.pdf."""

import os
import re
import shutil
from datetime import datetime, timezone, timedelta

DIR = os.path.dirname(os.path.abspath(__file__))


def extract_title(tex: str) -> str:
    m = re.search(r"\\title\{(.+?)\}", tex, re.DOTALL)
    if not m:
        return "Untitled"
    title = m.group(1).strip()
    # Clean LaTeX: remove line breaks, commands
    title = re.sub(r"\\\\\[.*?\]", " ", title)  # \\[4pt] etc.
    title = re.sub(r"\\\\", " ", title)
    title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    title = re.sub(r"[{}]", "", title)
    title = title.replace("--", "\u2013")
    title = re.sub(r"\s+", " ", title).strip()
    return title


def extract_author(tex: str) -> str:
    m = re.search(r"\\author\{(.+?)\}", tex, re.DOTALL)
    if not m:
        return "Unknown"
    author = m.group(1).strip()
    author = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", author)
    author = re.sub(r"[{}\\]", "", author)
    return re.sub(r"\s+", " ", author).strip()


def extract_abstract(tex: str) -> str:
    m = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", tex, re.DOTALL)
    if not m:
        return ""
    abstract = m.group(1).strip()
    abstract = abstract.replace("\\%", "%")
    abstract = re.sub(r"~", " ", abstract)
    # Convert \href{url}{text} to HTML links
    abstract = re.sub(
        r"\\href\{([^}]+)\}\{([^}]+)\}",
        r'<a href="\1" style="color:var(--accent);text-decoration:none;">\2</a>',
        abstract,
    )
    # Clean remaining LaTeX
    abstract = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", abstract)
    abstract = re.sub(r"[{}]", "", abstract)
    abstract = abstract.replace("---", "\u2014")
    abstract = re.sub(r"\s+", " ", abstract).strip()
    return abstract


def main():
    tex_path = os.path.join(DIR, "main.tex")
    pdf_path = os.path.join(DIR, "main.pdf")
    index_path = os.path.join(DIR, "docs", "index.html")

    with open(tex_path) as f:
        tex = f.read()

    title = extract_title(tex)
    author = extract_author(tex)
    abstract = extract_abstract(tex)

    # AOE = UTC-12
    aoe = timezone(timedelta(hours=-12))
    now = datetime.now(aoe)
    date = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S") + " AOE"

    print(f"  Title:  {title}")
    print(f"  Author: {author}")
    print(f"  Date:   {date} {time_str}")

    # Copy PDF
    shutil.copy2(pdf_path, os.path.join(DIR, "docs", "paper.pdf"))
    print("  Copied docs/paper.pdf")

    # Update index.html
    with open(index_path) as f:
        html = f.read()

    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html)
    html = re.sub(r"<h1>.*?</h1>", f"<h1>{title}</h1>", html, flags=re.DOTALL)
    html = re.sub(r"<span>Author:.*?</span>", f"<span>Author: {author}</span>", html)
    html = re.sub(r"<span>Date:.*?</span>", f"<span>Date: {date}</span>", html)
    html = re.sub(r"<span>Time:.*?</span>", f"<span>Time: {time_str}</span>", html)
    html = re.sub(
        r'(<div class="abstract">\s*<h2>Abstract</h2>\s*<p>).*?(</p>)',
        rf"\g<1>{abstract}\2",
        html,
        flags=re.DOTALL,
    )

    with open(index_path, "w") as f:
        f.write(html)
    print("  Updated docs/index.html")


if __name__ == "__main__":
    main()
