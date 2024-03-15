from typing import Annotated

from annotated_types import Len
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from pastemc.models.common import FileObjectResponse, ObjectNotFound
from pastemc.utils.s3api import list_objects

router = APIRouter(tags=["File Operations"])


@router.get(
    "/fetch/{file_id}",
    response_model=FileObjectResponse,
    summary="Get File URL by file_id",
    responses={404: {"model": ObjectNotFound}},
)
async def fetch_file(file_id: Annotated[str, Len(10, 26)]):
    if len(file_id) == 26:  # full ULID
        return FileObjectResponse.public(file_id=file_id)
    else:  # partial ULID, with timestamp (1-10 digits)
        if objects_list := await list_objects(prefix=file_id):
            return FileObjectResponse.public(file_id=objects_list[0].object_name)
        else:
            return JSONResponse(
                ObjectNotFound.make(file_id), status_code=status.HTTP_404_NOT_FOUND
            )
