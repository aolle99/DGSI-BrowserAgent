from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="lmstudio-community/Qwen3-8B-MLX-4bit",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="sk-local"
)
print(llm.invoke("Hola, ¿puedes responderme?"))