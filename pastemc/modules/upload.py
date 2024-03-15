from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
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
            "description": "`file_id` of the uploaded file",
            "headers": {
                "Location": {
                    "$ref": "#/components/schemas/FileObjectResponse/properties/url"
                }
            },
        },
    },
)
async def upload_file(
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
    return JSONResponse(
        FileObjectResponse.public(file_id=file_id).model_dump(),
        status_code=status.HTTP_201_CREATED,
        headers={"Location": get_object_url(file_id)},
    )
