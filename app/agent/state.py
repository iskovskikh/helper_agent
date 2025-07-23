from typing import Annotated

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class AgentState(BaseModel):
    messages: Annotated[list, add_messages]
