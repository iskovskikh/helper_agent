from typing import Annotated

from langgraph.graph.message import add_messages
from pydantic import BaseModel , Field

from langchain_core.messages import BaseMessage


class AgentState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)
    # messages: list[BaseMessage] = Field(default_factory=list)
