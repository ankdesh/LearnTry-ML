from typing import Any
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from task_manager import AgentWithTaskManager
from google.adk.tools import built_in_code_execution

# def calculator(operation: str, num1: float, num2: float) -> dict[str, Any]:
#     """Performs addition or subtraction based on the given operation."""
#     if operation == "add":
#         result = num1 + num2
#     elif operation == "subtract":
#         result = num1 - num2
#     else:
#         return {"error": "Invalid operation. Choose 'add' or 'subtract'."}
#     return {"result": result}

class CodeExecAgent(AgentWithTaskManager):
  """A simple calculator agent."""

  SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

  def __init__(self):
    self._agent = self._build_agent()
    self._user_id = "remote_agent"
    self._runner = self._build_runner()

  def get_processing_message(self) -> str:
      return "Calculating..."

  def _build_runner(self) -> Runner:
    """Builds the agent runner."""
    return Runner(
      app_name=self._agent.name,
      agent=self._agent,
      artifact_service=InMemoryArtifactService(),
      session_service=InMemorySessionService(),
      memory_service=InMemoryMemoryService(),
    )

  def _build_agent(self) -> LlmAgent:
    """Builds the LLM agent for the calculator."""
    return LlmAgent(
        model="gemini-2.0-flash-001",
        name="calculator_agent",
        description=(
            "This agent performs simple calculations using python code"
        ),
        instruction="""
            1. Generate the python code to answer the query. 
            2. Execute the Python code to perform calculations using the code execution tool provided.
            3. Send the final answer to user only as single number."
    """,
        tools=[
            built_in_code_execution,
        ],
    )
