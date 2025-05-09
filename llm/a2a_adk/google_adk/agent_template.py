from typing import Any
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from task_manager import AgentWithTaskManager

def calculator(operation: str, num1: float, num2: float) -> dict[str, Any]:
    """Performs addition or subtraction based on the given operation."""
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    else:
        return {"error": "Invalid operation. Choose 'add' or 'subtract'."}
    return {"result": result}

class CalculatorAgent(AgentWithTaskManager):
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
            "This agent performs simple calculations, specifically addition and subtraction."
        ),
        instruction="""
        You are a calculator agent capable of performing addition and subtraction.
        When a user provides a calculation request, use the 'calculator' tool to perform the calculation and return the result to the user.
        The user will provide the operation (add or subtract) and two numbers.

        Once the calculation is done, ask user if he thinks answer is correct or not. If reply is yes, message "Success" to user. If he says no, explain your 
        calculation for the user.
    """,
        tools=[
            calculator,
        ],
    )
