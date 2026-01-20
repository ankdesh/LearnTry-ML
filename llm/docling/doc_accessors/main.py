# main.py

from fastapi import FastAPI, Body, HTTPException
from typing import List, Union

from doc_accessors.commands import Command
from doc_accessors.data_handler import DataHandler
from types import TextPart, DataPart, FilePart

app = FastAPI(
    title="Multimodal Data Access API",
    description="An API for accessing text, table, and image data using iterators and filters.",
    version="1.0.0",
)

data_handler = DataHandler()

@app.post("/execute", response_model=List[Union[TextPart, DataPart, FilePart]])
async def execute_command(command: Command = Body(..., embed=True)):
    """
    A single endpoint to execute a command for data access.

    The command must conform to one of the defined Pydantic models.
    """
    try:
        result = data_handler.execute_command(command)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# To run this API, save the file and run the following command in your terminal:
# uvicorn main:app --reload