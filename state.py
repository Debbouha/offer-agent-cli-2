from enum import Enum

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class StopReason(str, Enum):
    COMPLETED = "completed"
    MAX_ITERATIONS = "max_iterations"
    EMPTY_OUTPUT = "empty_output"
    ERROR = "error"


class ToolEvent(BaseModel):
    tool_name: str
    arguments: dict
    result: object | None = None
    error: str | None = None


class InteractionEvent(BaseModel):
    iteration: int
    interaction_id: str
    tool_events: list[ToolEvent]


class AgentState(BaseModel):
    iteration: int = 0

    status: AgentStatus = AgentStatus.RUNNING
    stop_reason: StopReason | None = None

    final_result: str | None = None
    error: str | None = None

    history: list[InteractionEvent] = Field(default_factory=list)