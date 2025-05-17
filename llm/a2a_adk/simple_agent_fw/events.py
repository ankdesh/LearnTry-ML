import time
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

import a2a_types

# from .a2a_types import Part # Use relative import if in a package


class EventActions(BaseModel):
    """
    Defines actions that might be triggered or associated with an event.
    Important for side-effects & control.
    """
    a2a_state_update: Optional[Any] = Field(
        default=None,
        description="State update related to Agent-to-Agent communication. Structure to be defined later."
    )
    # Add other actions here as needed


class SAFEvent(BaseModel):
    """
    Custom Event Model for SAF (System Agent Framework) interactions.
    This event structure is used for communication within the system,
    representing messages, agent actions, or system notifications.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this specific event."
    )
    timestamp: float = Field(
        default_factory=time.time,
        description="Creation time of the event as a Unix timestamp (seconds since epoch)."
    )
    author: str = Field(
        description="Identifies the originator of the event, e.g., 'user', 'agent_name', 'system'."
    )
    parts: List[a2a_types.Part] = Field(
        description="A list of content parts (text, file, data) representing the main payload of the event."
    )
    turn_complete: Optional[bool] = Field(
        default=None,
        description="Indicates whether the response from a model or agent is complete for the current turn."
    )
    partial: Optional[bool] = Field(
        default=None,
        description="Indicates if this event is part of a larger, potentially streamed, message."
    )
    actions: Optional[EventActions] = Field(
        default=None,
        description="Optional actions associated with this event, important for side-effects and control flow."
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Error code if the event represents an error. Code may vary by model or system component."
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if the event represents an error."
    )
    custom_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arbitrary key-value metadata that can be attached to the event for custom purposes."
    )


# Example Usage (can be removed or kept for testing)
if __name__ == "__main__":

    # Example 1: A simple text message from a user
    user_event = SAFEvent(
        parts=[a2a_types.TextPart(text="Hello, how are you?")],
        author="user_Alice"
    )
    print("--- User Event ---")
    print(user_event.model_dump_json(indent=2))

    # Example 2: An agent's response with an action and custom metadata
    agent_actions = EventActions(
        a2a_state_update={"some_state_key": "new_value"})
    agent_event = SAFEvent(
        parts=[
            a2a_types.TextPart(
                text="I am doing well! I have updated the task."),
            a2a_types.DataPart(
                data={"task_id": "task_123", "new_status": "completed"})
        ],
        author="WeatherAgent",
        actions=agent_actions,
        turn_complete=True,
        custom_metadata={"confidence_score": 0.95,
                         "source_api": "OpenWeatherMap"}
    )
    print("\n--- Agent Event ---")
    print(agent_event.model_dump_json(indent=2))

    # Example 3: An error event
    # Content might be minimal or absent for some errors, but 'parts' is not optional.
    # So, we provide an empty list or a relevant text part.
    error_event = SAFEvent(
        parts=[a2a_types.TextPart(text="Failed to process your request.")],
        author="system_Orchestrator",
        error_code="E5001",
        error_message="Database connection timed out.",
        turn_complete=True  # Even errors complete a "turn"
    )
    print("\n--- Error Event ---")
    print(error_event.model_dump_json(indent=2))

    # Example 4: A partial event (e.g., for streaming)
    partial_event = SAFEvent(
        parts=[a2a_types.TextPart(
            text="This is the first part of a long story...")],
        author="StoryTellerAgent",
        partial=True
    )
    print("\n--- Partial Event ---")
    print(partial_event.model_dump_json(indent=2))
