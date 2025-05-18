from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional

# Assuming events.py is in the same package directory
# EventActions might not be directly used here, SAFEvent is.
from events import SAFEvent


class Session(ABC):
    """
    Abstract base class for a session.
    A session typically holds a sequence of events and a state dictionary.
    """

    @abstractmethod
    async def add_event(self, event: SAFEvent) -> None:
        """Adds an event to the session's history."""
        pass

    @abstractmethod
    async def get_events(self) -> List[SAFEvent]:
        """Retrieves all events from the session's history."""
        pass

    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """Retrieves the entire session state as a dictionary."""
        pass

    @abstractmethod
    async def update_state_value(self, key: str, value: Any) -> None:
        """Updates or sets a specific key-value pair in the session state."""
        pass

    @abstractmethod
    async def get_state_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Retrieves a value for a specific key from the session state."""
        pass



class InMemorySession(Session):
    """
    An in-memory implementation of the Session.
    Stores events in a list and state in a dictionary.
    """

    def __init__(self, session_id: str, initial_state: Optional[Dict[str, Any]] = None):
        """
        Initializes an InMemorySession.
        :param session_id: A unique identifier for this session.
        :param initial_state: An optional dictionary to pre-populate the session's state.
        """
        self.session_id: str = session_id
        self._events: List[SAFEvent] = []
        self._state: Dict[str, Any] = dict(
            initial_state) if initial_state is not None else {}

    async def add_event(self, event: SAFEvent) -> None:
        self._events.append(event)

    async def get_events(self) -> List[SAFEvent]:
        """Retrieves a copy of all events from the session's history."""
        return list(self._events)  # Return a copy

    async def get_events_by_author(self, author: str) -> List[SAFEvent]:
        """Returns all events authored by a specific author."""
        return [event for event in await self.get_events() if event.author == author]

    async def get_events_with_actions(self) -> List[SAFEvent]:
        """Returns all events that have associated actions."""
        return [event for event in await self.get_events() if event.actions is not None]

    async def get_events_with_state_updates(self) -> List[SAFEvent]:
        """Returns all events that have A2A state updates in their actions."""
        return [
            event for event in await self.get_events()
            if event.actions and event.actions.a2a_state_update is not None
        ]

    async def get_state(self) -> Dict[str, Any]:
        return dict(self._state)  # Return a copy

    async def update_state_value(self, key: str, value: Any) -> None:
        self._state[key] = value

    async def get_state_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Retrieves a value for a specific key from the session state."""
        return self._state.get(key, default)

    async def get_last_n_events(self, n: int) -> List[SAFEvent]:
        """Returns the last N events."""
        if (n <= 0):
            return []
        return self._events[-n:] if n <= len(self._events) else self._events

    async def get_last_user_event(self) -> Optional[SAFEvent]:
        """Returns the most recent event authored by 'user' (or common user identifiers)."""
        user_author = "user"
        for event in reversed(await self.get_events()):
            if event.author == user_author:
                return event
        return None

    async def get_last_agent_event(self, agent_author: str = "agent") -> Optional[SAFEvent]:
        """Returns the most recent event authored by an agent."""
        for event in reversed(await self.get_events()):
            if event.author.lower() == agent_author.lower():
                return event
        return None
