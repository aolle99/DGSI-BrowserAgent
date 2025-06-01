import os
import asyncio
from pathlib import Path
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import logging

load_dotenv()

# Configura logging detallado para depuración
logging.basicConfig(level=logging.DEBUG)

#os.environ["PWDEBUG"] = "1"

def read_pdf_content(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f'PDF file not found at {pdf_path}')

    pdf = PdfReader(pdf_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text() or ''
    return text


class LoggingChatOpenAI(ChatOpenAI):
    def invoke(self, *args, **kwargs):
        print(f"[LLM INPUT] {args} {kwargs}")
        result = super().invoke(*args, **kwargs)
        print(f"[LLM OUTPUT] {result}")
        return result


async def main():
    logging.info('Iniciando main()')
    # Read and summarize PDF content
    pdf_path = str(Path(__file__).parent / 'curso.pdf')
    logging.info(f'Intentando leer PDF en: {pdf_path}')
    pdf_content = read_pdf_content(pdf_path)
    logging.info('PDF leído correctamente')

    # Initialize the browser with Chrome instance
    logging.info('Inicializando el navegador...')
    browser = Browser(
        config=BrowserConfig(
            # You'll need to adjust this path based on your OS
            chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=False  # Set to True if you don't want to see the browser
        )
    )
    logging.info('Navegador inicializado')

    # Configuración para usar LM Studio como backend local compatible con OpenAI
    # Asegúrate de que LM Studio esté corriendo y sirviendo el modelo en modo API OpenAI
    # Puedes configurar las variables de entorno en un archivo .env o aquí directamente
    # Ejemplo de variables de entorno necesarias:
    # OPENAI_API_KEY=sk-local  # cualquier string, LM Studio no valida la key
    # OPENAI_API_BASE=http://localhost:1234/v1  # o el puerto que uses en LM Studio

    # Nombre del modelo cargado en LM Studio (debe coincidir con el nombre exacto en LM Studio)
    modelo_local = "lmstudio-community/Qwen3-8B-MLX-4bit"  # <-- Cambia esto por el nombre de tu modelo

    # Create the agent with a task to write the summary
    logging.info('Creando el agente...')
    agent = Agent(
        task=f"""Ve a docs.google.com. 
                Ten en cuenta que el contenido de la web es en catalan, asi que traduce el contenido al castellano.
                Crea un nuevo documento en google docs.
                Escribe un resumen claro y conciso del siguiente contenido, organizándolo con títulos y bullet points apropiados: 

                {pdf_content}

                Después de escribir el resumen, asegúrate de guardar el documento con un nombre apropiado.""",
        #task="Ve a https://example.com y dime qué ves en la página.",
        llm=LoggingChatOpenAI(
            model=modelo_local,
            openai_api_base="http://localhost:1234/v1",  # Cambia el puerto si usas otro
            openai_api_key="sk-local"  # cualquier string
        ),
        browser=browser,
    )
    logging.info('Agente creado')

    # Run the agent
    logging.info('Ejecutando agent.run()...')
    await agent.run()
    logging.info('agent.run() finalizado')
    await browser.close()
    logging.info('Navegador cerrado')

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())