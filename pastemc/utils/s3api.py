import ssl
from tempfile import SpooledTemporaryFile

import httpx
from miniopy_async import Minio
from ulid import ULID

from pastemc.models.minio import ObjectMetadata
from pastemc.models.settings import SETTINGS

oss = Minio(**SETTINGS.s3.model_dump(exclude=["bucket", "subpath", "public_endpoint"]))

verify_context = httpx.create_ssl_context(
    verify=ssl.create_default_context(), http2=True
)


async def put_object(
    data: SpooledTemporaryFile, length: int, content_type: str, metadata: ObjectMetadata
):
    file_id = ULID()

    await oss.put_object(
        bucket_name=SETTINGS.s3.bucket,
        object_name=f"{SETTINGS.s3.subpath}{file_id}",
        data=data,
        length=length,
        content_type=content_type,
        metadata=metadata.model_dump(),
    )
    return file_id


def get_object_url(file_id: str, internal: bool = False) -> str:
    return f"{SETTINGS.s3.public_endpoint if internal else SETTINGS.s3.public_endpoint}{SETTINGS.s3.subpath}{file_id}"


async def get_object(file_id: str):
    async with httpx.AsyncClient(verify=verify_context) as client:
        resp = await client.get(get_object_url(file_id, internal=True))
    return resp


async def list_objects(prefix: str):
    return await oss.list_objects(
        bucket_name=SETTINGS.s3.bucket,
        prefix=prefix.removeprefix("/"),
    )
