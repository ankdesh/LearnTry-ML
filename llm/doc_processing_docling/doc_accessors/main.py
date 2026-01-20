# main.py

from fastapi import FastAPI, Body, HTTPException
from typing import List, Union
import os

from commands import Command
from data_handler import DoclingDataHandler, AbstractDataHandler
from types import TextPart, DataPart, FilePart

# --- Configuration ---
# IMPORTANT: Place a PDF file named 'sample.pdf' in the same directory as this script,
# or update the path to your PDF file.
PDF_FILE_PATH = os.path.join(os.path.dirname(__file__), "sample.pdf")

app = FastAPI(
    title="Multimodal Data Access API (Docling)",
    description="An API for accessing text, table, and image data from a PDF using the docling library.",
    version="1.1.0",
)

# --- Initialize the Data Handler ---
# This single instance will load the document once on startup.
try:
    data_handler: AbstractDataHandler = DoclingDataHandler(document_path=PDF_FILE_PATH)
except FileNotFoundError as e:
    # If the file doesn't exist, we can't start the app properly.
    # In a real-world scenario, you might handle this more gracefully.
    print(f"Error: {e}")
    print("Please make sure a PDF file exists at the configured path.")
    data_handler = None

@app.post("/execute", response_model=List[Union[TextPart, DataPart, FilePart]])
async def execute_command(command: Command = Body(..., embed=True)):
    """
    A single endpoint to execute a command for data access on a PDF document.

    The command must conform to one of the defined Pydantic models.
    """
    if data_handler is None:
        raise HTTPException(
            status_code=500,
            detail="Data handler is not initialized. Check if the PDF file is missing."
        )

    try:
        result = data_handler.execute_command(command)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# To run this API:
# 1. Make sure you have a 'sample.pdf' file in the same directory.
# 2. Run the command in your terminal:
#    uvicorn main:app --reload