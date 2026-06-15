import json
from pathlib import Path

from os import getenv
from dotenv import load_dotenv

from google.api_core.client_options import ClientOptions
from google.cloud import documentai


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"
TEMP_DIR = STORAGE_DIR / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = TEMP_DIR / "raw_invoice.json"


def extract_document(file_path, mime_type):

    load_dotenv()

    project = getenv("PROJECT")
    processor = getenv("PROCESSOR")
    location = "australia-southeast1"

    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    processor_path = client.processor_path(
        project,
        location,
        processor
    )

    with open(file_path, "rb") as file:
        content = file.read()

    raw_document = documentai.RawDocument(
        content=content,
        mime_type=mime_type
    )

    request = documentai.ProcessRequest(
        name=processor_path,
        raw_document=raw_document
    )

    result = client.process_document(
        request=request
    )

    entities = []

    for entity in result.document.entities:

        entities.append({
            "type": entity.type_,
            "mention_text": entity.mention_text,
            "confidence": entity.confidence,
            "normalized_value": (
                entity.normalized_value.text
                if entity.normalized_value
                else None
            )
        })

    with open(RAW_FILE, "w") as file:
        json.dump(
            entities,
            file,
            indent=4
        )