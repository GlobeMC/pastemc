from fastapi import APIRouter, File, Form, Response, UploadFile, status
from loguru import logger

from pastemc.models.common import FileObjectResponse
from pastemc.models.minio import ObjectMetadata
from pastemc.utils.s3api import get_object_url, put_object

router = APIRouter(tags=["File Operations"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a File",
    responses={
        201: {
            "model": FileObjectResponse,
            "headers": {
                "Location": {
                    "$ref": "#/components/schemas/FileObjectResponse/properties/url"
                }
            },
        },
    },
)
async def upload_file(
    response: Response,
    file: UploadFile = File(description="the (Minecraft log) file"),
    format_type: str = Form(
        description="the format of this file, used for highlight rendering"
    ),
):
    # rewrite the content-type (MIME)
    content_mime = file.content_type
    if file.filename.split(".")[-1] in ["log"]:
        content_mime = "text/plain; charset=utf-8"

    # get the length of the file
    file.file.seek(0, 2)
    length = file.file.tell()
    file.file.seek(0)  # reset pointer

    # put to minio
    file_id = await put_object(
        data=file.file,
        length=length,
        content_type=content_mime or "application/octet-stream",
        metadata=ObjectMetadata(original_name=file.filename, format_type=format_type),
    )
    logger.info(f"file uploaded, {file.filename=}, {file_id=}, {length=}")

    # return 201 created
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = get_object_url(file_id)
    return FileObjectResponse.public(file_id=file_id)
