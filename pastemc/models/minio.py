import httpx
from pydantic import BaseModel


class ObjectMetadata(BaseModel):
    original_name: str
    format_type: str

    @classmethod
    def from_headers(cls, headers: httpx.Headers):
        return cls(
            **{k: headers.get(f"x-amz-meta-{k}") for k in cls.model_fields.keys()}
        )
