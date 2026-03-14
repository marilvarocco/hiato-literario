import json
import os
import re
import shutil
from pathlib import Path
from html import escape

SITE_URL = "www.hiatoliterario.com"
SITE_NAME = "Hiato Literário"

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "entries.json"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def slugify(text: str) -> str:
    text = text.lower().strip()

    replacements = {
        "á": "a", "à": "a", "â": "a", "ã": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_base(title: str, description: str, canonical: str, content: str) -> str:
    base = read_file(TEMPLATES_DIR / "base.html")
    return (
        base.replace("{{TITLE}}", escape(title))
            .replace("{{DESCRIPTION}}", escape(description))
            .replace("{{CANONICAL}}", escape(canonical))
            .replace("{{CONTENT}}", content)
    )


def render_word_page(entry: dict) -> str:
    palavra = entry["palavra"]
    classe = entry.get("classe", "Palavra")
    significado = entry.get("significado", "")
    sinonimos = ", ".join(entry.get("sinonimos", [])) or "Não informado"
    silabas = entry.get("silabas", "Não informado")
    tonicidade = entry.get("tonicidade", "Não informado")
    categoria = entry.get("categoria", "dicionario").capitalize()

    tpl = read_file(TEMPLATES_DIR / "palavra.html")
    content = (
        tpl.replace("{{PALAVRA}}", escape(palavra))
           .replace("{{CLASSE}}", escape(classe))
           .replace("{{SIGNIFICADO}}", escape(significado))
           .replace("{{SINONIMOS}}", escape(sinonimos))
           .replace("{{SILABAS}}", escape(silabas))
           .replace("{{TONICIDADE}}", escape(tonicidade))
           .replace("{{CATEGORIA}}", escape(categoria))
    )

    slug = slugify(palavra)
    canonical = f"{SITE_URL}/palavra/{slug}/"
    title = f"Significado de {palavra} - Dicionário e gramática | {SITE_NAME}"
    description = f"Veja o significado de {palavra}, sinônimos, divisão silábica e tonicidade."

    return render_base(title, description, canonical, content)


def build_home(entries: list[dict]) -> None:
    items = []
    for entry in sorted(entries, key=lambda x: x["palavra"].lower())[:200]:
        slug = slugify(entry["palavra"])
        items.append(
            f"""
            <div class="card">
              <h2><a href="/palavra/{slug}/">{escape(entry['palavra'])}</a></h2>
              <p class="muted">{escape(entry.get('classe', 'Palavra'))}</p>
              <p>{escape(entry.get('significado', ''))}</p>
            </div>
            """
        )

    palavras_js = [
        {
            "palavra": e["palavra"],
            "slug": slugify(e["palavra"])
        }
        for e in entries
    ]

    content = f"""
    <section class="card">
      <h1>Dicionário e gramática da língua portuguesa</h1>
      <p>
        Pesquise significados, sinônimos, divisão silábica, tonicidade e conceitos gramaticais.
      </p>

      <div class="search">
        <input type="text" id="searchInput" placeholder="Digite uma palavra..." />
        <button onclick="goSearch()">Buscar</button>
      </div>
    </section>

    <section class="card">
      <h2>Páginas em destaque</h2>
      <div class="grid">
        {''.join(items)}
      </div>
    </section>

    <script>
      const palavras = {json.dumps(palavras_js, ensure_ascii=False)};

      function normalizeText(text) {{
        return text
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\\u0300-\\u036f]/g, "");
      }}

      function goSearch() {{
        const value = document.getElementById("searchInput").value.trim();
        if (!value) return;

        const normalized = normalizeText(value);
        const found = palavras.find(p => normalizeText(p.palavra) === normalized);

        if (found) {{
          window.location.href = "/palavra/" + found.slug + "/";
          return;
        }}

        alert("Palavra não encontrada ainda no banco local.");
      }}

      document.getElementById("searchInput").addEventListener("keydown", function(e) {{
        if (e.key === "Enter") goSearch();
      }});
    </script>
    """

    html = render_base(
        title=f"{SITE_NAME} | Dicionário, gramática e análise de palavras",
        description="Consulte significados, sinônimos, divisão silábica, tonicidade e conceitos gramaticais.",
        canonical=f"{SITE_URL}/",
        content=content
    )

    write_file(OUTPUT_DIR / "index.html", html)


def build_word_pages(entries: list[dict]) -> list[str]:
    urls = [f"{SITE_URL}/"]

    for entry in entries:
        slug = slugify(entry["palavra"])
        page_html = render_word_page(entry)
        path = OUTPUT_DIR / "palavra" / slug / "index.html"
        write_file(path, page_html)
        urls.append(f"{SITE_URL}/palavra/{slug}/")

    return urls


def build_sitemap(urls: list[str]) -> None:
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{escape(url)}</loc>")
        xml.append("  </url>")

    xml.append("</urlset>")
    write_file(OUTPUT_DIR / "sitemap.xml", "\n".join(xml))


def build_robots() -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    write_file(OUTPUT_DIR / "robots.txt", content)


def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    entries = json.loads(read_file(DATA_FILE))

    build_home(entries)
    urls = build_word_pages(entries)
    build_sitemap(urls)
    build_robots()

    print(f"Build concluído. Arquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
