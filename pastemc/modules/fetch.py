from typing import Annotated

from annotated_types import Len
from fastapi import APIRouter, Path, Response, status

from pastemc.models.common import FileObjectResponse, ObjectNotFound
from pastemc.utils.s3api import list_objects

router = APIRouter(tags=["File Operations"])


@router.get(
    "/fetch/{file_id}",
    response_model=FileObjectResponse,
    summary="Get File URL by file_id",
    responses={404: {"model": ObjectNotFound}},
)
async def fetch_file(
    response: Response,
    file_id: Annotated[
        str,
        Len(10, 26),
        Path(
            description="this field accepts:\n- full ULID (26 digits)\n- partial ULID, with timestamp (at least 10 digits)",
            examples=["01HRKVWPKNYNQKB5F209DZ85B7", "01HRKVWPKN"],
        ),
    ],
):
    if len(file_id) == 26:  # full ULID
        return FileObjectResponse.public(file_id=file_id)
    else:  # partial ULID, with timestamp (at least 10 digits)
        if objects_list := await list_objects(prefix=file_id):
            return FileObjectResponse.public(file_id=objects_list[0].object_name)
        else:
            response.code = status.HTTP_404_NOT_FOUND
            return ObjectNotFound.make(file_id)
