import os
import asyncio
from pathlib import Path
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()


def read_pdf_content(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f'PDF file not found at {pdf_path}')

    pdf = PdfReader(pdf_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text() or ''
    return text


async def main():
    # Read and summarize PDF content
    pdf_path = '/tmp/curso.pdf'
    pdf_content = read_pdf_content(pdf_path)

    # Initialize the browser with Chrome instance
    browser = Browser(
        config=BrowserConfig(
            # You'll need to adjust this path based on your OS
            chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=False  # Set to True if you don't want to see the browser
        )
    )

    # Create the agent with a task to write the summary
    agent = Agent(
        task=f"""Ve a docs.google.com y crea un nuevo documento. 
                Escribe un resumen claro y conciso del siguiente contenido, organizándolo con títulos y bullet points apropiados: 

                {pdf_content}

                Después de escribir el resumen, asegúrate de guardar el documento.""",
        llm=ChatOpenAI(model='gpt-4o'),
        browser=browser,
    )

    # Run the agent
    await agent.run()
    await browser.close()

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())