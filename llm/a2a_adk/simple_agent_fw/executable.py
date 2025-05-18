from events import SAFEvent
from abc import ABC


class SAFExecutable(ABC):
    """
    Class which represents an executable logic
    """

    def __init__(self, stream=False):
        """
        Args:
            stream (bool, optional): Can execute function generate stream of events. Defaults to False.
        """
        self._stream = stream

    async def execute(self, event: SAFEvent) -> SAFEvent:
        """Impolements the core logic of the SAFExecutable.

        This method serves as the single entry point for processing an SAFEvent.
        It encapsulates the core logic, which could involve interacting with an LLM,
        performing imperative actions, or any other processing necessary. It can generate single 
        event of stream of events.

        Args:
            event: The input SAFEvent to be processed.
        Returns:
            An SAFEvent representing the result of the execution.
        """
        raise NotImplementedError
