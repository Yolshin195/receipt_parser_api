from typing import Annotated
import io

from litestar import Litestar, get, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from receipt_parser_service import receipt_parser_async


@get("/")
async def readme() -> dict[str, str]:
    """Handler function that returns a description of the service."""
    return {"description": "Этот сервис предназначен для распознавания текста с изображений чеков."}


@post("/")
async def receipt_parser(data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)]) -> str:
    """Handler function that returns a greeting dictionary."""
    file_bytes = await data.read()
    return await receipt_parser_async(io.BytesIO(file_bytes))


app = Litestar(
    route_handlers=[readme, receipt_parser],
    openapi_config=OpenAPIConfig(
        title="Litestar Example",
        description="Example of litestar",
        version="0.0.1",
        render_plugins=[SwaggerRenderPlugin()],
    ),
)