from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ---------- Инструменты ----------
@tool
def add_numbers(a: int, b: int) -> int:
    """Складывает два числа"""

    print(f'Складываю {a} и {b}')
    return a + b

@tool
def get_time() -> str:
    """Возвращает текущее время"""
    import datetime
    print(f'Получаю время')
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [add_numbers, get_time]

# ---------- LLM с поддержкой tool calling ----------
llm = ChatOllama(
    # model="MFDoom/deepseek-r1-tool-calling:8b",
    model="llama3.1:8b-instruct-q6_K",
)

# ---------- Агент ----------
graph = create_react_agent(llm, tools)

# ---------- Тест ----------
if __name__ == "__main__":
    inputs = {"messages": [("user", "Сколько будет 7 + 12?")]}

    for step in graph.stream(inputs):
        print(step)

    print("✅ Готово")