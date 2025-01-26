import asyncio
import io
import pytesseract
from PIL import Image

from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased")
question: str = "What is the total amount on the receipt, which is the largest number listed on it?"


def get_text_from_image(image_bytes: io.BytesIO) -> str:
    image = Image.open(image_bytes)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


def get_data(receipt_text: str) -> str:
    result = qa_pipeline(
        question=question,
        context=receipt_text
    )
    return result['answer']


def receipt_parser(image_bytes: io.BytesIO) -> str:
    receipt_text = get_text_from_image(image_bytes)
    return get_data(receipt_text)


async def receipt_parser_async(image_bytes: io.BytesIO) -> str:
    return await asyncio.to_thread(receipt_parser, image_bytes)


async def get_text_from_image_async(image_bytes: io.BytesIO) -> str:
    """Асинхронная функция для обработки изображения без блокировки event loop."""
    return await asyncio.to_thread(get_text_from_image, image_bytes)
