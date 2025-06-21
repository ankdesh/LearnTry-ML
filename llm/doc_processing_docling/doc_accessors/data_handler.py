# data_handler.py

import json
from typing import List, Union
import pandas as pd
import base64

from commands import (
    Command,
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
    CompoundIteratorByTypeCommand # Import new command
)
from a2a.types import TextPart, DataPart, FilePart, FileWithBytes

# --- Dummy Data ---

DUMMY_TEXT = {
    "doc_id_1": {
        "sections": {
            "introduction": "This is the introduction.",
            "body": "This is the main body of the document.",
            "conclusion": "This is the conclusion."
        },
        "content_lists": {
            "figure_list": ["Figure 1: A diagram.", "Figure 2: A chart."],
            "table_list": ["Table 1: Data summary.", "Table 2: More data."],
            "table_of_contents": ["Introduction", "Body", "Conclusion"]
        },
        "chunks": [
            {"id": "chunk_1", "text": "This is the first chunk of text for nearest neighbor search."},
            {"id": "chunk_2", "text": "This is the second chunk, which is a neighbor."},
            {"id": "chunk_3", "text": "This is a third, more distant chunk."},
            {"id": "chunk_4", "text": "A fourth chunk to complete the example."}
        ]
    }
}

DUMMY_TABLE = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [4, 5, 6],
    'col3': [7, 8, 9]
})

# Dummy base64 encoded 1x1 pixel red PNG
DUMMY_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/epv2AAAAABJRU5ErkJggg=="

DUMMY_IMAGES = {
    "image_1": {"id": "image_1", "data": DUMMY_IMAGE_B64},
    "image_2": {"id": "image_2", "data": DUMMY_IMAGE_B64},
    "image_3": {"id": "image_3", "data": DUMMY_IMAGE_B64},
}

# --- New Dummy Compound Data ---
DUMMY_COMPOUND_DOCUMENT = [
    {"type": "text", "id": "text_intro", "content": "This is the first text element in the compound document."},
    {"type": "table", "id": "table_summary", "content": pd.DataFrame({'Product': ['A', 'B'], 'Sales': [150, 200]})},
    {"type": "image", "id": "image_logo", "content": DUMMY_IMAGE_B64},
    {"type": "text", "id": "text_conclusion", "content": "This is the second text part, acting as a conclusion."},
]


class DataHandler:
    def execute_command(self, command: Command) -> List[Union[TextPart, DataPart, FilePart]]:
        if isinstance(command, TextIteratorBySectionsCommand):
            return self._handle_text_by_sections(command)
        elif isinstance(command, TextIteratorByFixedSizeChunksCommand):
            return self._handle_text_by_fixed_size_chunks(command)
        elif isinstance(command, TextFilterNearestChunksCommand):
            return self._handle_text_nearest_chunks(command)
        elif isinstance(command, TextFilterByContentCommand):
            return self._handle_text_by_content(command)
        elif isinstance(command, TableIteratorByRowsCommand):
            return self._handle_table_by_rows(command)
        elif isinstance(command, TableIteratorByColumnsCommand):
            return self._handle_table_by_columns(command)
        elif isinstance(command, TableFilterByRowsCommand):
            return self._handle_table_filter_by_rows(command)
        elif isinstance(command, TableFilterByColumnsCommand):
            return self._handle_table_filter_by_columns(command)
        elif isinstance(command, ImageIteratorCommand):
            return self._handle_image_iterator(command)
        elif isinstance(command, ImageFilterNearestNCommand):
            return self._handle_image_filter_nearest_n(command)
        # --- Handle new compound command ---
        elif isinstance(command, CompoundIteratorByTypeCommand):
            return self._handle_compound_iterator_by_type(command)
        else:
            raise ValueError("Unsupported command")

    # --- New Handler for Compound Modality ---
    def _handle_compound_iterator_by_type(self, command: CompoundIteratorByTypeCommand) -> List[Union[TextPart, DataPart, FilePart]]:
        results = []
        for item in DUMMY_COMPOUND_DOCUMENT:
            if item["type"] == command.iterate_over:
                if item["type"] == "text":
                    results.append(TextPart(text=item["content"], metadata={"id": item["id"]}))
                elif item["type"] == "table":
                    # For tables, we can return the entire table as one DataPart
                    df = item["content"]
                    table_json = df.to_dict() # json.loads(df.to_json(orient='records'))
                    print ("Table JSON:", table_json)
                    results.append(DataPart(data=table_json))
                elif item["type"] == "image":
                    results.append(FilePart(
                        file=FileWithBytes(bytes=item["content"], name=item["id"], mimeType="image/png"),
                        metadata={"id": item["id"]}
                    ))
        return results

    def _handle_text_by_sections(self, command: TextIteratorBySectionsCommand) -> List[TextPart]:
        sections = DUMMY_TEXT["doc_id_1"]["sections"]
        return [TextPart(text=content, metadata={"section": title}) for title, content in sections.items()]

    def _handle_text_by_fixed_size_chunks(self, command: TextIteratorByFixedSizeChunksCommand) -> List[TextPart]:
        full_text = " ".join(DUMMY_TEXT["doc_id_1"]["sections"].values())
        return [
            TextPart(text=full_text[i:i + command.chunk_size])
            for i in range(0, len(full_text), command.chunk_size)
        ]

    def _handle_text_nearest_chunks(self, command: TextFilterNearestChunksCommand) -> List[TextPart]:
        # This is a dummy implementation. A real implementation would use vector embeddings.
        all_chunks = DUMMY_TEXT["doc_id_1"]["chunks"]
        # Find the index of the target chunk
        try:
            start_index = next(i for i, chunk in enumerate(all_chunks) if chunk["id"] == command.chunk_id)
        except StopIteration:
            return []

        # Get the n surrounding chunks (simplified logic)
        start = max(0, start_index - command.n // 2)
        end = min(len(all_chunks), start_index + command.n // 2 + 1)

        # Exclude the chunk itself if n is even
        nearest = [chunk for i, chunk in enumerate(all_chunks[start:end]) if chunk["id"] != command.chunk_id]

        return [TextPart(text=chunk["text"], metadata={"id": chunk["id"]}) for chunk in nearest[:command.n]]

    def _handle_text_by_content(self, command: TextFilterByContentCommand) -> List[TextPart]:
        content_list = DUMMY_TEXT["doc_id_1"]["content_lists"].get(command.content_type, [])
        return [TextPart(text=item) for item in content_list]

    def _handle_table_by_rows(self, command: TableIteratorByRowsCommand) -> List[DataPart]:
        return [
            DataPart(data=json.loads(DUMMY_TABLE.iloc[[i]].to_json(orient='records'))[0])
            for i in range(len(DUMMY_TABLE))
        ]

    def _handle_table_by_columns(self, command: TableIteratorByColumnsCommand) -> List[DataPart]:
        return [
            DataPart(data={col: DUMMY_TABLE[col].tolist()})
            for col in DUMMY_TABLE.columns
        ]

    def _handle_table_filter_by_rows(self, command: TableFilterByRowsCommand) -> List[DataPart]:
        filtered_df = DUMMY_TABLE.iloc[command.row_indices]
        return [DataPart(data=json.loads(filtered_df.to_json(orient='records')))]

    def _handle_table_filter_by_columns(self, command: TableFilterByColumnsCommand) -> List[DataPart]:
        filtered_df = DUMMY_TABLE[command.column_names]
        return [DataPart(data=json.loads(filtered_df.to_json(orient='records')))]

    def _handle_image_iterator(self, command: ImageIteratorCommand) -> List[FilePart]:
        return [
            FilePart(file=FileWithBytes(bytes=img["data"], name=img["id"], mimeType="image/png"))
            for img in DUMMY_IMAGES.values()
        ]

    def _handle_image_filter_nearest_n(self, command: ImageFilterNearestNCommand) -> List[FilePart]:
        # Dummy implementation
        all_images = list(DUMMY_IMAGES.values())
        return [
            FilePart(file=FileWithBytes(bytes=img["data"], name=img["id"], mimeType="image/png"))
            for img in all_images[:command.n] if img["id"] != command.image_id
        ]