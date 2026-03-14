from pathlib import Path
import json

# raiz do projeto
ROOT = Path(__file__).resolve().parent.parent

PASTA_PALAVRAS = ROOT / "palavra"
ARQUIVO_SAIDA = ROOT / "palavras.js"

palavras = []

for pasta in sorted(PASTA_PALAVRAS.iterdir()):
    if pasta.is_dir():

        index_file = pasta / "index.html"

        if index_file.exists():

            palavras.append({
                "palavra": pasta.name,
                "pasta": pasta.name
            })

conteudo = "const PALAVRAS = " + json.dumps(
    palavras,
    ensure_ascii=False,
    indent=2
) + ";"

ARQUIVO_SAIDA.write_text(conteudo, encoding="utf-8")

print("Arquivo palavras.js gerado com sucesso!")
print("Total de palavras:", len(palavras))
