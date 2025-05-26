# orchestrator.py
import uuid
from typing import Dict, Union, Optional, Any, Type

# Assuming these files are in the same directory or accessible in PYTHONPATH
from . import a2a_types  # Contains A2A JSON-RPC type definitions
from .events import SAFEvent # Defines SAFEvent
from .executable import SAFExecutable # Abstract class for core logic
from .session import Session, InMemorySession # Session management
from . import event_utility # Import the event utility module

class A2AOrchestrator:
    """
    Orchestrates interactions between A2A (Agent-to-Agent) style JSON-RPC events
    and SAFEvents, managing sessions and invoking SAFExecutables.
    Event conversion logic is handled by the event_utility module.
    Allows for flexible Session implementations.
    """

    def __init__(self, executable: SAFExecutable, session_class: Type[Session] = InMemorySession):
        """
        Initializes the A2AOrchestrator.

        Args:
            executable: An instance of SAFExecutable that will process SAFEvents.
            session_class: The class to use for session instantiation. 
                           Defaults to InMemorySession. Must be a subclass of Session.
        """
        self._executable = executable
        self._sessions: Dict[str, Session] = {}  # In-memory store for active sessions
        self._session_class: Type[Session] = session_class # Store the session class

    def _get_or_create_session(self, session_id: Optional[str] = None, initial_state: Optional[Dict[str, Any]] = None) -> Session:
        """
        Retrieves an existing session or creates a new one using the configured session_class.
        If session_id is None, a new session_id is generated.

        Args:
            session_id: The ID of the session to retrieve or create.
            initial_state: Optional initial state for a new session.

        Returns:
            The Session object.
        """
        if session_id is None:
            session_id = str(uuid.uuid4()) # Generate a new session ID if not provided
        
        if session_id not in self._sessions:
            # Create a new session instance using the specified session class
            self._sessions[session_id] = self._session_class(session_id=session_id, initial_state=initial_state)
        return self._sessions[session_id]

    async def async_run(self, request: a2a_types.JSONRPCRequest) -> a2a_types.JSONRPCResponse:
        """
        Main entry point for handling incoming A2A JSON-RPC requests.
        It routes the request to appropriate handlers based on the method.

        Args:
            request: The A2A JSONRPCRequest object.

        Returns:
            An A2A JSONRPCResponse object.
        """
        session_id_from_req: Optional[str] = None

        # Extract session ID from request parameters if available
        if hasattr(request.params, 'sessionId') and request.params.sessionId is not None:
            session_id_from_req = request.params.sessionId
        elif isinstance(request.params, a2a_types.TaskSendParams): 
             session_id_from_req = request.params.sessionId # TaskSendParams auto-generates sessionId if not present

        current_session = self._get_or_create_session(session_id=session_id_from_req)
        
        # Handle SendTaskRequest
        if isinstance(request, a2a_types.SendTaskRequest):
            params: a2a_types.TaskSendParams = request.params
            
            # Convert A2A message to an internal SAFEvent
            input_safevent = event_utility.a2a_message_to_safevent(params.message)
            await current_session.add_event(input_safevent) # Add user's input event to session history

            response_safevent: SAFEvent
            try:
                # Execute the core logic using the provided SAFExecutable
                response_safevent = await self._executable.execute(input_safevent)
            except Exception as e:
                # If executable fails, create an error SAFEvent
                error_message = f"Core logic execution error: {str(e)}"
                response_safevent = SAFEvent(
                    author=self._executable.__class__.__name__ if self._executable else "OrchestratorError",
                    parts=[a2a_types.TextPart(text=error_message)],
                    error_code="EXECUTABLE_EXCEPTION",
                    error_message=error_message,
                    turn_complete=True 
                )
            
            await current_session.add_event(response_safevent) # Add agent's response event to session history

            # Process any state updates indicated by the response event
            if response_safevent.actions and response_safevent.actions.a2a_state_update:
                if isinstance(response_safevent.actions.a2a_state_update, dict):
                    for key, value in response_safevent.actions.a2a_state_update.items():
                        await current_session.update_state_value(key, value)

            # Convert the response SAFEvent back to an A2A JSON-RPC response
            a2a_response = await event_utility.safevent_to_a2a_task_response(
                response_safevent, params, current_session, request.id
            )
            return a2a_response

        # Handle GetTaskRequest
        elif isinstance(request, a2a_types.GetTaskRequest):
            params: a2a_types.TaskQueryParams = request.params
            
            # Determine the session to query based on request parameters
            session_to_query = self._get_or_create_session(session_id=params.sessionId if params.sessionId else current_session.session_id)

            all_session_events = await session_to_query.get_events()
            if not all_session_events:
                # If session is empty, return TaskNotFoundError
                return a2a_types.JSONRPCResponse(
                    id=request.id, 
                    error=a2a_types.TaskNotFoundError(
                        message=f"Task {params.id} (session {session_to_query.session_id}) is empty or not found.", 
                        data={"id": params.id, "sessionId": session_to_query.session_id}
                    )
                )

            latest_event_in_session = all_session_events[-1]
            effective_response_safevent_for_status: SAFEvent
            
            # If the latest event is from the user, the task is still awaiting agent processing
            if latest_event_in_session.author == 'user':
                effective_response_safevent_for_status = SAFEvent(
                    author="system_orchestrator", 
                    parts=[a2a_types.TextPart(text="Task received, awaiting agent processing or further input.")],
                    turn_complete=False 
                )
            else:
                # Otherwise, use the latest event from the agent/system for status
                effective_response_safevent_for_status = latest_event_in_session
            
            # Convert the status SAFEvent to an A2A JSON-RPC response
            a2a_response = await event_utility.safevent_to_a2a_task_response(
                effective_response_safevent_for_status, params, session_to_query, request.id
            )
            return a2a_response
            
        # Handle unimplemented methods
        else:
            return a2a_types.JSONRPCResponse(
                id=request.id,
                error=a2a_types.MethodNotFoundError(message=f"Method '{request.method}' not implemented by this orchestrator.")
            )

async def example_main():
    # Dynamically import LLMExecutable for the example
    try:
        from .llm_executable import LLMExecutable
    except ImportError:
        from llm_executable import LLMExecutable # Fallback for direct script execution

    my_executable = LLMExecutable()

    # Instantiate orchestrator with default InMemorySession
    orchestrator_default_session = A2AOrchestrator(executable=my_executable)

    # Instantiate orchestrator explicitly providing InMemorySession
    orchestrator_explicit_inmemory = A2AOrchestrator(executable=my_executable, session_class=InMemorySession)
    
    # --- Simulate first SendTaskRequest ---
    task_id_1 = str(uuid.uuid4())
    session_id_1 = str(uuid.uuid4()) 

    send_task_params_1 = a2a_types.TaskSendParams(
        id=task_id_1,
        sessionId=session_id_1,
        message=a2a_types.Message(
            role="user",
            parts=[a2a_types.TextPart(text="Hello agent, tell me a short story.")]
        )
    )
    send_task_request_1 = a2a_types.SendTaskRequest(
        id="req-s1", 
        params=send_task_params_1
    )

    print("\n--- Simulating SendTaskRequest 1 (Default Session) ---")
    send_task_response_1 = await orchestrator_default_session.handle_a2a_request(send_task_request_1)
    print(f"SendTaskResponse 1: {send_task_response_1.model_dump_json(indent=2) if send_task_response_1 else 'None'}")

    # --- Simulate GetTaskRequest for the first task ---
    get_task_params_1 = a2a_types.TaskQueryParams(
        id=task_id_1, 
        sessionId=session_id_1, 
        historyLength=5 
    )
    get_task_request_1 = a2a_types.GetTaskRequest(
        id="req-g1", 
        params=get_task_params_1
    )
    print("\n--- Simulating GetTaskRequest 1 (Default Session) ---")
    get_task_response_1 = await orchestrator_default_session.handle_a2a_request(get_task_request_1)
    print(f"GetTaskResponse 1: {get_task_response_1.model_dump_json(indent=2) if get_task_response_1 else 'None'}")


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(example_main())
    except ModuleNotFoundError as e:
        print(f"Module not found: {e}. Ensure all required .py files are accessible.")
        print("If running as a script, ensure all modules are in the same directory or PYTHONPATH is set.")
        print("If part of a package, run with 'python -m package_name.orchestrator'.")
