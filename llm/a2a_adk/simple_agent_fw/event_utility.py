# event_utility.py
from typing import Union, Optional, List, Any

# Assuming these files are in the same directory or accessible in PYTHONPATH
from . import a2a_types # Contains A2A JSON-RPC type definitions
from .events import SAFEvent # Defines SAFEvent
from .session import Session # Session (used for type hint, and potentially for history access in future)

def a2a_message_to_safevent(a2a_message: a2a_types.Message) -> SAFEvent:
    """
    Converts an A2A Message object to an SAFEvent object.
    Logging has been removed from this version.

    Args:
        a2a_message: The a2a_types.Message object from the A2A request.

    Returns:
        An SAFEvent object.
    """
    author = a2a_message.role
    # The role from the A2A message (e.g., 'user') becomes the author of the SAFEvent.
    # Parts are directly transferred.

    input_event = SAFEvent(
        author=author,
        parts=a2a_message.parts
    )
    return input_event

async def safevent_to_a2a_task_response(
    response_safevent: SAFEvent,
    original_request_params: Union[a2a_types.TaskSendParams, a2a_types.TaskQueryParams, a2a_types.TaskIdParams], 
    session: Session, 
    request_id: Union[str, int, None]
) -> a2a_types.JSONRPCResponse:
    """
    Converts an SAFEvent (typically from an SAFExecutable) into an A2A JSONRPCResponse,
    populating Task details like status, message, and history.
    Logging has been removed from this version.

    Args:
        response_safevent: The SAFEvent that is the result of processing.
        original_request_params: The parameters from the original A2A request.
        session: The current session, used for populating history.
        request_id: The ID of the original JSON-RPC request.

    Returns:
        An A2A JSONRPCResponse object (e.g., SendTaskResponse, GetTaskResponse).
    """
    task_id = original_request_params.id # A2A Task ID from the original request
    
    # Attempt to get sessionId from original params, fallback to session object's ID
    session_id_from_req = getattr(original_request_params, 'sessionId', session.session_id)

    # The SAFEvent's parts become the content of the A2A Message from the 'agent'
    agent_message = a2a_types.Message(role="agent", parts=response_safevent.parts)

    # Determine the A2A TaskState based on the SAFEvent's properties
    task_state_val = a2a_types.TaskState.UNKNOWN
    if response_safevent.error_code:
        task_state_val = a2a_types.TaskState.FAILED
    elif response_safevent.turn_complete:
        task_state_val = a2a_types.TaskState.COMPLETED
    else:
        # If not an error and not explicitly complete, assume it's still working
        task_state_val = a2a_types.TaskState.WORKING
        
    task_status = a2a_types.TaskStatus(
        state=task_state_val,
        message=agent_message # The agent's message derived from the SAFEvent
    )
    
    # Populate A2A message history if requested
    history_messages: Optional[List[a2a_types.Message]] = None
    requested_history_length = getattr(original_request_params, 'historyLength', None)

    if requested_history_length is not None and requested_history_length > 0:
        history_messages = []
        saf_events_history_full = await session.get_events() # Get all SAFEvents from the session
        
        # Slice the history to get the last N events
        start_index = max(0, len(saf_events_history_full) - requested_history_length)
        saf_events_to_convert = saf_events_history_full[start_index:]
        
        # Convert relevant SAFEvents back to A2A Message format for history
        for event_in_history in saf_events_to_convert:
            role_for_history = 'user' if event_in_history.author == 'user' else 'agent'
            history_messages.append(
                a2a_types.Message(role=role_for_history, parts=event_in_history.parts)
            )

    # Construct the final A2A Task object
    task_result = a2a_types.Task(
        id=task_id,
        sessionId=session_id_from_req,
        status=task_status,
        history=history_messages, # Will be None if not populated
        artifacts=None # Placeholder: Artifact mapping can be implemented if needed
    )

    # If the SAFEvent represents an error, create an A2A JSONRPCError
    if response_safevent.error_code and response_safevent.error_message:
        a2a_error = a2a_types.InternalError(
            message=response_safevent.error_message,
            data={"original_error_code": response_safevent.error_code} # Include original code for reference
        )
        return a2a_types.JSONRPCResponse(id=request_id, error=a2a_error)
    
    # Return the appropriate A2A response type based on the original request
    if isinstance(original_request_params, a2a_types.TaskSendParams):
        return a2a_types.SendTaskResponse(id=request_id, result=task_result)
    elif isinstance(original_request_params, a2a_types.TaskQueryParams):
         return a2a_types.GetTaskResponse(id=request_id, result=task_result)
    else:
        # Fallback for unhandled original_request_params types
        # This returns the task_result as a generic dictionary if no specific response type matches.
        return a2a_types.JSONRPCResponse(id=request_id, result=task_result.model_dump())
