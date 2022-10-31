from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
import os


def solveCaptcha(imagePath):
    PROJECT_ID = os.getenv('PROJECT_ID')
    LOCATION = "us"
    PROCESSOR_ID = os.getenv('PROCESSOR_ID')
    FILE_PATH = imagePath
    MIME_TYPE = "image/jpeg"

    docai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-documentai.googleapis.com")
    )
    RESOURCE_NAME = docai_client.processor_path(
        PROJECT_ID, LOCATION, PROCESSOR_ID)
    with open(FILE_PATH, "rb") as image:
        image_content = image.read()
    raw_document = documentai.RawDocument(
        content=image_content, mime_type=MIME_TYPE)
    request = documentai.ProcessRequest(
        name=RESOURCE_NAME, raw_document=raw_document)
    result = docai_client.process_document(request=request)
    document_object = result.document
    return document_object.text
