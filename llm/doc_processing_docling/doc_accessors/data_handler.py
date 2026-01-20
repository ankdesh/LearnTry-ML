# data_handler.py

import io
import json
from typing import List, Union, Iterator
import pandas as pd
import base64
from abc import ABC, abstractmethod
from pathlib import Path

# --- Docling Imports ---
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.chunking import HybridChunker
from docling_core.types.doc import Document, PictureItem, TableItem

# --- Command and Type Imports ---
from commands import (
    Command,
    TextIteratorBySectionsCommand,
    TableIteratorByRowsCommand,
    ImageIteratorCommand,
    CompoundIteratorByTypeCommand
)
from types import TextPart, DataPart, FilePart, FileWithBytes

# --- Abstract Base Class for Data Handlers ---

class AbstractDataHandler(ABC):
    """
    Abstract base class for data handlers.
    Defines the interface for executing commands.
    """
    def execute_command(self, command: Command) -> List[Union[TextPart, DataPart, FilePart]]:
        """
        Executes a given command and returns the result.
        This method dispatches to the appropriate handler based on the command type.
        """
        if isinstance(command, CompoundIteratorByTypeCommand):
            return self._handle_compound_iterator_by_type(command)
        elif isinstance(command, TextIteratorBySectionsCommand):
            return self._handle_text_by_sections(command)
        elif isinstance(command, TableIteratorByRowsCommand):
            return self._handle_table_by_rows(command)
        elif isinstance(command, ImageIteratorCommand):
            return self._handle_image_iterator(command)
        # Add other command handlers here as needed
        else:
            raise ValueError(f"Unsupported command type: {type(command)}")

    @abstractmethod
    def _handle_compound_iterator_by_type(self, command: CompoundIteratorByTypeCommand) -> List[Union[TextPart, DataPart, FilePart]]:
        pass

    @abstractmethod
    def _handle_text_by_sections(self, command: TextIteratorBySectionsCommand) -> List[TextPart]:
        pass

    @abstractmethod
    def _handle_table_by_rows(self, command: TableIteratorByRowsCommand) -> List[DataPart]:
        pass

    @abstractmethod
    def _handle_image_iterator(self, command: ImageIteratorCommand) -> List[FilePart]:
        pass


# --- Docling-based Implementation of the Data Handler ---

class DoclingDataHandler(AbstractDataHandler):
    """
    An implementation of the data handler that uses the 'docling' library
    to process a local PDF document.
    """
    def __init__(self, document_path: str):
        self.document_path = Path(document_path)
        if not self.document_path.exists():
            raise FileNotFoundError(f"The specified document was not found: {self.document_path}")
        self._document = self._load_document()

    def _load_document(self) -> Document:
        """Loads the document using Docling's DocumentConverter."""
        pipeline_options = PdfPipelineOptions()
        pipeline_options.images_scale = 2.0  # Higher resolution for images
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        conv_res = doc_converter.convert(self.document_path)
        return conv_res.document

    def _handle_compound_iterator_by_type(self, command: CompoundIteratorByTypeCommand) -> List[Union[TextPart, DataPart, FilePart]]:
        """Handles iteration over different types within the loaded document."""
        if command.iterate_over == 'text':
            return self._iterate_text_chunks()
        elif command.iterate_over == 'table':
            return self._iterate_tables()
        elif command.iterate_over == 'image':
            return self._iterate_images()
        else:
            return []

    def _iterate_text_chunks(self) -> List[TextPart]:
        """Iterates through text chunks of the document using HybridChunker."""
        chunker = HybridChunker()
        chunk_iter = chunker.chunk(dl_doc=self._document)
        text_parts = []
        for i, chunk in enumerate(chunk_iter):
            # Context-enriched text provides better context for each chunk
            enriched_text = chunker.contextualize(chunk=chunk)
            text_parts.append(TextPart(text=enriched_text, metadata={"chunk_index": i}))
        return text_parts

    def _iterate_tables(self) -> List[DataPart]:
        """Iterates through all tables found in the document."""
        data_parts = []
        for i, element in enumerate(self._document.iterate_items()):
            if isinstance(element, TableItem):
                # Convert the table to a pandas DataFrame, then to JSON
                df = element.to_pandas()
                table_json = json.loads(df.to_json(orient='records'))
                data_parts.append(DataPart(data=table_json, metadata={"table_index": i}))
        return data_parts

    def _iterate_images(self) -> List[FilePart]:
        """Iterates through all pictures found in the document."""
        file_parts = []
        for i, element in enumerate(self._document.iterate_items()):
            if isinstance(element, PictureItem):
                pil_image = element.get_image(self._document)
                # Convert PIL image to base64
                buffered = io.BytesIO()
                pil_image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                file_parts.append(FilePart(
                    file=FileWithBytes(bytes=img_str, name=f"image_{i}.png", mimeType="image/png"),
                    metadata={"image_index": i}
                ))
        return file_parts

    # --- Dummy Implementations for other command types (can be expanded) ---

    def _handle_text_by_sections(self, command: TextIteratorBySectionsCommand) -> List[TextPart]:
        # This can be implemented more robustly by analyzing document structure
        return self._iterate_text_chunks()

    def _handle_table_by_rows(self, command: TableIteratorByRowsCommand) -> List[DataPart]:
        # A simple implementation that returns all tables
        return self._iterate_tables()

    def _handle_image_iterator(self, command: ImageIteratorCommand) -> List[FilePart]:
        # A simple implementation that returns all images
        return self._iterate_images()