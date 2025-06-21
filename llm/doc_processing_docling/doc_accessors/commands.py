# commands.py

from typing import List, Literal, Union
from pydantic import BaseModel, Field

# --- Text Commands ---

class TextIteratorBySectionsCommand(BaseModel):
    modality: Literal['text']
    accessor_type: Literal['iterator']
    iterator_type: Literal['by_sections']

class TextIteratorByFixedSizeChunksCommand(BaseModel):
    modality: Literal['text']
    accessor_type: Literal['iterator']
    iterator_type: Literal['by_fixed_size_chunks']
    chunk_size: int = Field(..., description="The size of each text chunk.")

class TextFilterNearestChunksCommand(BaseModel):
    modality: Literal['text']
    accessor_type: Literal['filter']
    filter_type: Literal['n_nearest_chunks']
    chunk_id: str = Field(..., description="The ID of the chunk to find neighbors for.")
    n: int = Field(..., description="The number of nearest chunks to return.")

class TextFilterByContentCommand(BaseModel):
    modality: Literal['text']
    accessor_type: Literal['filter']
    filter_type: Literal['by_content']
    content_type: Literal['figure_list', 'table_list', 'table_of_contents']


# --- Table Commands ---

class TableIteratorByRowsCommand(BaseModel):
    modality: Literal['table']
    accessor_type: Literal['iterator']
    iterator_type: Literal['by_rows']

class TableIteratorByColumnsCommand(BaseModel):
    modality: Literal['table']
    accessor_type: Literal['iterator']
    iterator_type: Literal['by_columns']

class TableFilterByRowsCommand(BaseModel):
    modality: Literal['table']
    accessor_type: Literal['filter']
    filter_type: Literal['by_rows']
    row_indices: List[int] = Field(..., description="A list of row indices to retrieve.")

class TableFilterByColumnsCommand(BaseModel):
    modality: Literal['table']
    accessor_type: Literal['filter']
    filter_type: Literal['by_columns']
    column_names: List[str] = Field(..., description="A list of column names to retrieve.")


# --- Image Commands ---

class ImageIteratorCommand(BaseModel):
    modality: Literal['image']
    accessor_type: Literal['iterator']

class ImageFilterNearestNCommand(BaseModel):
    modality: Literal['image']
    accessor_type: Literal['filter']
    filter_type: Literal['n_nearest']
    image_id: str = Field(..., description="The ID of the image to find neighbors for.")
    n: int = Field(..., description="The number of nearest images to return.")


# --- Compound Commands (New) ---

class CompoundIteratorByTypeCommand(BaseModel):
    modality: Literal['compound']
    accessor_type: Literal['iterator']
    iterate_over: Literal['text', 'table', 'image'] = Field(..., description="The modality type to iterate over within the compound object.")


# --- Union of all commands ---

Command = Union[
    TextIteratorBySectionsCommand,
    TextIteratorByFixedSizeChunksCommand,
    TextFilterNearestChunksCommand,
    TextFilterByContentCommand,
    TableIteratorByRowsCommand,
    TableIteratorByColumnsCommand,
    TableFilterByRowsCommand,
    TableFilterByColumnsCommand,
    ImageIteratorCommand,
    ImageFilterNearestNCommand,
    CompoundIteratorByTypeCommand, # Added new command
]