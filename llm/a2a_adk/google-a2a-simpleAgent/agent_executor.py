import asyncio
import json
import os
from typing import AsyncGenerator

from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REASON_FILE = os.path.join(CURRENT_DIR, "sample_reason.txt")
PYTHON_FILE = os.path.join(CURRENT_DIR, "sample_python.py")


class HelloWorldAgent:
    """Hello World Agent."""

    async def _stream_file_content(self, file_path: str, header: str) -> AsyncGenerator[str, None]:
        """Streams file content word by word as JSON strings."""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    for word in line.strip().split():
                        if word: # Ensure word is not empty
                            yield json.dumps({"header": header, "token": word})
        except FileNotFoundError:
            yield json.dumps({"header": header, "token": f"Error: File {os.path.basename(file_path)} not found."})

    async def invoke(self) -> AsyncGenerator[str, None]:
        async for item in self._stream_file_content(REASON_FILE, "Rationale"):
            #print ("ASD0: ", item)
            yield item
        async for item in self._stream_file_content(PYTHON_FILE, "Answer"):
            #print ("ASD1: ", item)
            yield item


class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = HelloWorldAgent()

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        async for json_payload in self.agent.invoke():
            print ("ASD: ", json_payload)
            event = new_agent_text_message(json_payload)
            print ("ASD: ", event)  
            event_queue.enqueue_event(new_agent_text_message(json_payload))
            await asyncio.sleep(0)  # Yield control to the event loop

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')