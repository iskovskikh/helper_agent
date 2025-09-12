from dataclasses import dataclass

from langchain_core.language_models.chat_models import BaseChatModel

@dataclass
class CustomContext():
    llm: BaseChatModel
