from datetime import datetime
from importlib import metadata
from typing import Annotated

from annotated_types import Len
from pydantic import AnyHttpUrl, BaseModel, BeforeValidator, Field, computed_field
from ulid import ULID

from pastemc.utils.s3api import get_object_url

FileId = Annotated[
    str,
    BeforeValidator(lambda v: str(v)),
    Len(26),
    Field(
        examples=["01HRKVWPKNYNQKB5F209DZ85B7"], description="ULID of the uploaded file"
    ),
]
FileUrl = Annotated[
    AnyHttpUrl,
    Field(
        examples=["https://oss.example.com/pastemc/01HRKVWPKNYNQKB5F209DZ85B7"],
        description="URL of the uploaded file, directly to OSS",
    ),
]


class UploadResponse(BaseModel):
    file_id: FileId


class ObjectNotFound(BaseModel):
    details: str = "object with file_id {file_id} not found"

    @classmethod
    def make(cls, file_id: FileId):
        return cls(details=f"object with file_id {file_id} not found").model_dump()


class FileObjectResponse(BaseModel):
    file_id: FileId
    url: FileUrl
    last_modified: Annotated[
        datetime, Field(examples=["2024-03-10T17:42:50.229000+08:00"])
    ]

    @classmethod
    def public(cls, file_id: FileId):
        return cls(
            file_id=file_id,
            url=get_object_url(file_id),
            last_modified=ULID.from_str(file_id).datetime.astimezone(),
        ).model_dump()
