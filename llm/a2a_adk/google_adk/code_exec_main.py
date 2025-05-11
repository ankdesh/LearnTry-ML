from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from task_manager import AgentTaskManager
from code_execute import CodeExecAgent  # Import CodeExecAgent
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
        
        # Define capabilities and skills for the Code Execution Agent
        capabilities = AgentCapabilities(streaming=True, stateTransitionHistory=True)
        skill = AgentSkill(
            id="execute_python_code",
            name="Generate and Execute Python Code",
            description="Executes Python code to perform calculations or other tasks.",
            tags=["code execution", "python", "calculator"],
            examples=["Execute `5 * 5`", "Run `import math; math.log(10)`"],
        )
        agent_card = AgentCard(
            name="Code Execution Agent",
            description="This agent executes Python code to perform calculations.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=CodeExecAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=CodeExecAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=CodeExecAgent()), # Instantiate with CodeExecAgent
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
