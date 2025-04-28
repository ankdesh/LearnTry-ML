import asyncio
import uuid # For unique session IDs
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# --- Constants ---
APP_NAME_OPENAPI = "openapi_petstore_app"
USER_ID_OPENAPI = "user_openapi_1"
SESSION_ID_OPENAPI = f"session_openapi_{uuid.uuid4()}" # Unique session ID
AGENT_NAME_OPENAPI = "petstore_manager_agent"
GEMINI_MODEL = "gemini-2.0-flash"

# --- Sample OpenAPI Specification (JSON String) ---
# A basic Pet Store API example using httpbin.org as a mock server
openapi_spec_string = """
{
  "openapi": "3.0.0",
  "info": {
    "title": "Simple Pet Store API (Mock)",
    "version": "1.0.1",
    "description": "An API to manage pets in a store, using httpbin for responses."
  },
  "servers": [
    {
      "url": "https://httpbin.org",
      "description": "Mock server (httpbin.org)"
    }
  ],
  "paths": {
    "/get": {
      "get": {
        "summary": "List all pets (Simulated)",
        "operationId": "listPets",
        "description": "Simulates returning a list of pets. Uses httpbin's /get endpoint which echoes query parameters.",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "description": "Maximum number of pets to return",
            "required": false,
            "schema": { "type": "integer", "format": "int32" }
          },
          {
             "name": "status",
             "in": "query",
             "description": "Filter pets by status",
             "required": false,
             "schema": { "type": "string", "enum": ["available", "pending", "sold"] }
          }
        ],
        "responses": {
          "200": {
            "description": "A list of pets (echoed query params).",
            "content": { "application/json": { "schema": { "type": "object" } } }
          }
        }
      }
    },
    "/post": {
      "post": {
        "summary": "Create a pet (Simulated)",
        "operationId": "createPet",
        "description": "Simulates adding a new pet. Uses httpbin's /post endpoint which echoes the request body.",
        "requestBody": {
          "description": "Pet object to add",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": ["name"],
                "properties": {
                  "name": {"type": "string", "description": "Name of the pet"},
                  "tag": {"type": "string", "description": "Optional tag for the pet"}
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Pet created successfully (echoed request body).",
            "content": { "application/json": { "schema": { "type": "object" } } }
          }
        }
      }
    },
    "/get?petId={petId}": {
      "get": {
        "summary": "Info for a specific pet (Simulated)",
        "operationId": "showPetById",
        "description": "Simulates returning info for a pet ID. Uses httpbin's /get endpoint.",
        "parameters": [
          {
            "name": "petId",
            "in": "path",
            "description": "This is actually passed as a query param to httpbin /get",
            "required": true,
            "schema": { "type": "integer", "format": "int64" }
          }
        ],
        "responses": {
          "200": {
            "description": "Information about the pet (echoed query params)",
            "content": { "application/json": { "schema": { "type": "object" } } }
          },
          "404": { "description": "Pet not found (simulated)" }
        }
      }
    }
  }
}
"""

# --- Create OpenAPIToolset ---
generated_tools_list = []
try:
    # Instantiate the toolset with the spec string
    petstore_toolset = OpenAPIToolset(
        spec_str=openapi_spec_string,
        spec_str_type="json"
        # No authentication needed for httpbin.org
    )
    # Get all tools generated from the spec
    generated_tools_list = petstore_toolset.get_tools()
    print(f"Generated {len(generated_tools_list)} tools from OpenAPI spec:")
    for tool in generated_tools_list:
        # Tool names are snake_case versions of operationId
        print(f"- Tool Name: '{tool.name}', Description: {tool.description[:60]}...")

except ValueError as ve:
    print(f"Validation Error creating OpenAPIToolset: {ve}")
    # Handle error appropriately, maybe exit or skip agent creation
except Exception as e:
    print(f"Unexpected Error creating OpenAPIToolset: {e}")
    # Handle error appropriately

# --- Agent Definition ---
openapi_agent = LlmAgent(
    name=AGENT_NAME_OPENAPI,
    model=GEMINI_MODEL,
    tools=generated_tools_list, # Pass the list of RestApiTool objects
    instruction=f"""You are a Pet Store assistant managing pets via an API.
    Use the available tools to fulfill user requests.
    Available tools: {', '.join([t.name for t in generated_tools_list])}.
    When creating a pet, confirm the details echoed back by the API.
    When listing pets, mention any filters used (like limit or status).
    When showing a pet by ID, state the ID you requested.
    """,
    description="Manages a Pet Store using tools generated from an OpenAPI spec."
)

# --- Session and Runner Setup ---
session_service_openapi = InMemorySessionService()
runner_openapi = Runner(
    agent=openapi_agent, app_name=APP_NAME_OPENAPI, session_service=session_service_openapi
)
session_openapi = session_service_openapi.create_session(
    app_name=APP_NAME_OPENAPI, user_id=USER_ID_OPENAPI, session_id=SESSION_ID_OPENAPI
)

# --- Agent Interaction Function ---
async def call_openapi_agent_async(query):
    print("\n--- Running OpenAPI Pet Store Agent ---")
    print(f"Query: {query}")
    if not generated_tools_list:
        print("Skipping execution: No tools were generated.")
        print("-" * 30)
        return

    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not provide a final text response."
    try:
        async for event in runner_openapi.run_async(
            user_id=USER_ID_OPENAPI, session_id=SESSION_ID_OPENAPI, new_message=content
            ):
            # Optional: Detailed event logging for debugging
            # print(f"  DEBUG Event: Author={event.author}, Type={'Final' if event.is_final_response() else 'Intermediate'}, Content={str(event.content)[:100]}...")
            if event.get_function_calls():
                call = event.get_function_calls()[0]
                print(f"  Agent Action: Called function '{call.name}' with args {call.args}")
            elif event.get_function_responses():
                response = event.get_function_responses()[0]
                print(f"  Agent Action: Received response for '{response.name}'")
                # print(f"  Tool Response Snippet: {str(response.response)[:200]}...") # Uncomment for response details
            elif event.is_final_response() and event.content and event.content.parts:
                # Capture the last final text response
                final_response_text = event.content.parts[0].text.strip()

        print(f"Agent Final Response: {final_response_text}")

    except Exception as e:
        print(f"An error occurred during agent run: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for errors
    print("-" * 30)

# --- Run Examples ---
async def run_openapi_example():
    # Trigger listPets
    await call_openapi_agent_async("Show me the pets available.")
    # Trigger createPet
    await call_openapi_agent_async("Please add a new dog named 'Dukey'.")
    # Trigger showPetById
    await call_openapi_agent_async("Get info for pet with ID 123.")

# --- Execute ---
if __name__ == "__main__":
    print("Executing OpenAPI example...")
    # Use asyncio.run() for top-level execution
    try:
        asyncio.run(run_openapi_example())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("Info: Cannot run asyncio.run from a running event loop (e.g., Jupyter/Colab).")
            # If in Jupyter/Colab, you might need to run like this:
            # await run_openapi_example()
        else:
            raise e
    print("OpenAPI example finished.")
    