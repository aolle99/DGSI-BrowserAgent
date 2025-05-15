# DGSI-BrowserAgent

Este proyecto permite leer el contenido de un archivo PDF y, utilizando un agente automatizado con un navegador controlado por IA, crea un documento en Google Docs con un resumen estructurado del contenido del PDF.

## Requisitos

- Python 3.8+
- Google Chrome instalado (ajusta la ruta en el script si usas otro sistema operativo)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd DGSI-BrowserAgent
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea un archivo `.env` con tus credenciales de OpenAI si es necesario:
   ```env
   OPENAI_API_KEY=tu_clave
   ```

## Uso

1. Coloca el PDF que deseas resumir en `/tmp/curso.pdf` o ajusta la ruta en `pdf_to_gdocs.py`.
2. Ejecuta el script principal:
   ```bash
   python pdf_to_gdocs.py
   ```
3. El agente abrirá Google Docs, creará un nuevo documento y escribirá un resumen claro y organizado del contenido del PDF.

## Notas
- El script utiliza un agente que controla Google Chrome para automatizar la creación y edición del documento en Google Docs.
- Puedes modificar el prompt o la ruta del PDF según tus necesidades.

## Licencia
MIT 