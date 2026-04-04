# Hiato Literário Tools

Hub escalável de ferramentas acadêmicas e utilitários de texto, com processamento 100% client-side.

## Stack
- HTML
- Tailwind via CDN
- JavaScript Vanilla
- CSS próprio
- JSON para dados locais

## Estrutura
```txt
/
├── index.html
├── /tools/
├── /src/
│   ├── /js/
│   ├── /css/
│   └── /data/
├── /assets/
│   ├── /icons/
│   ├── /images/
│   └── /fonts/
```

## MVP atual
- Contador de palavras
- Gerador de capa ABNT
- Gerador de referências ABNT

## Como rodar
Basta abrir o `index.html` no navegador.

## Melhorias aplicadas
- remoção do limpador de PDF do MVP
- correção de links internos quebrados
- base CSS compartilhada em `src/css/styles.css`
- manutenção do layout atual
- melhoria de consistência entre homepage e ferramentas

## Próximos passos
- centralizar mais JS em `src/js`
- revisar regras ABNT mais específicas
- melhorar SEO de cada página
- publicar no GitHub Pages
