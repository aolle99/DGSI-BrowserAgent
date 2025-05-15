import os
import asyncio
# from pathlib import Path # Ya no se usa directamente
# from PyPDF2 import PdfReader # Ya no se lee PDF
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Se mantiene para la conexión con LM Studio
from browser_use import Agent, Browser, BrowserConfig  # Se mantiene para la interacción con el navegador
from pydantic.types import SecretStr # Importa SecretStr


load_dotenv()


async def main():
    # POR FAVOR, REEMPLAZA ESTA URL CON LA URL REAL DE TU FORMULARIO DE GOOGLE
    google_form_url = 'https://forms.gle/jxPW2oosScnPZtEo6'

    if google_form_url == 'URL_DEL_FORMULARIO_DE_GOOGLE_AQUI':
        print("IMPORTANTE: Edita el script y reemplaza 'URL_DEL_FORMULARIO_DE_GOOGLE_AQUI' "
              "con la URL real del formulario de Google que deseas procesar.")
        return

    # Initialize the browser with Chrome instance
    browser = Browser(
        config=BrowserConfig(
            # Puede que necesites ajustar esta ruta según tu sistema operativo
            browser_binary_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            headless=False  # Ponlo en True si no quieres que se vea el navegador
        )
    )
    secret_api_key = SecretStr('lm-studio')

    # Crea el agente con la tarea de procesar el Formulario de Google
    agent = Agent(
        task=f"""
        1. Navega a la siguiente URL del formulario de Google: {google_form_url}
        2. Examina cuidadosamente la página para identificar cada una de las preguntas presentes en el formulario.
        3. Para cada pregunta que identifiques:
            a. Formula una consulta de búsqueda concisa y efectiva para encontrar la respuesta en internet.
            b. Utiliza tus capacidades de navegación y búsqueda en internet para encontrar la respuesta más precisa y relevante a esa pregunta.
        4. Prepara un listado que contenga cada pregunta del formulario junto con la respuesta que encontraste para ella.
           El formato debería ser algo como:
           Pregunta 1: [Texto de la pregunta 1]
           Respuesta Encontrada: [Respuesta para la pregunta 1]

           Pregunta 2: [Texto de la pregunta 2]
           Respuesta Encontrada: [Respuesta para la pregunta 2]

           Y así sucesivamente para todas las preguntas.
        5. Presenta este listado final. No intentes rellenar, modificar o enviar el formulario. Tu objetivo es solo extraer las preguntas y encontrar sus respuestas.
        """,
        llm=ChatOpenAI(
            model='qwen3-8b',
            # Reemplaza esto con el identificador del modelo en LM Studio
            base_url='http://localhost:1234/v1',  # URL del servidor de LM Studio
            api_key=secret_api_key
        ),
        browser=browser,
    )

    # Run the agent
    print(f"Intentando procesar el formulario de Google en: {google_form_url}")
    print("Por favor, ten paciencia, esto puede tardar un poco...")
    await agent.run()
    await browser.close()

    input('Presiona Enter para cerrar...')


if __name__ == '__main__':
    asyncio.run(main())