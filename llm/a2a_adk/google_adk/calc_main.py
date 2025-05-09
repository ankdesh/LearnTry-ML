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


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10002)
def main(host, port):
    try:
        # Check for API key only if Vertex AI is not configured
        # if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
        #     if not os.getenv("GOOGLE_API_KEY"):
        #         raise MissingAPIKeyError(
        #             "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
        #         )
        
        # Define capabilities and skills for the Calculator Agent
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="perform_calculation",
            name="Perform Calculation",
            description="Performs addition or subtraction on two numbers.",
            tags=["calculator", "math"],
            examples=["What is 5 plus 3?", "Calculate 10 minus 4."],
        )
        agent_card = AgentCard(
            name="Calculator Agent",
            description="This agent performs simple calculations (addition and subtraction).",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=CalculatorAgent.SUPPORTED_CONTENT_TYPES, # Use CalculatorAgent's modes
            defaultOutputModes=CalculatorAgent.SUPPORTED_CONTENT_TYPES, # Use CalculatorAgent's modes
            capabilities=capabilities,
            skills=[skill], # Use the calculator skill defined above
        )
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=CalculatorAgent()), # Instantiate with CalculatorAgent
            host=host,
            port=port,
        )
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)
    
if __name__ == "__main__":
    main()
