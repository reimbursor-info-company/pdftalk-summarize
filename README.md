# pdftalk-summarize

Resumen extractivo offline (estilo TextRank) para texto y PDFs, pensado para
usarse junto a [pdftalk](https://github.com/reimbursor-info-company/pdftalk)
antes de convertir un documento largo a audio.

No requiere internet, modelos descargables, ni claves de API.

## Instalación

```bash
pip install pdftalk-summarize          # solo resumen de texto
pip install pdftalk-summarize[pdf]     # incluye soporte de PDF y audio (pdftalk)
```

## Uso en Python

```python
from pdftalk_summarize import summarize, summarize_pdf

resumen = summarize(texto_largo, ratio=0.2)
resumen_pdf = summarize_pdf("documento.pdf", ratio=0.2)
```

## Uso por línea de comandos

```bash
pdftalk-summarize documento.pdf -o resumen.txt --ratio 0.2
pdftalk-summarize documento.pdf --audio resumen.wav
```
