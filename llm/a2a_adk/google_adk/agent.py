from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from task_manager import AgentTaskManager
from agent_template import CalculatorAgent # Import CalculatorAgent
import click
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


root_agent=CalculatorAgent() # Instantiate with CalculatorAgent
    