import pkgutil
from importlib import import_module, metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel


class AppInfo(BaseModel):
    title: str = __package__
    version: str = metadata.version(__package__)
    license_info: dict = {
        "name": "GNU Affero General Public License v3.0 or later",
        "identifier": "AGPL-3.0-or-later",
        "url": "https://www.gnu.org/licenses/agpl-3.0.html",
    }


app_info = AppInfo()


app = FastAPI(
    **app_info.model_dump(),
    servers=[{"url": "http://localhost:8000", "description": "Dev"}],
)

app.add_middleware(CORSMiddleware, allow_origins=["*"])

for module_info in pkgutil.iter_modules(["pastemc/modules"]):
    logger.info(f"found module: {module_info.name}")
    app.include_router(import_module(f"pastemc.modules.{module_info.name}").router)


@app.get(
    "/", response_model=AppInfo, summary="Get App Info", response_description="App Info"
)
async def root():
    return app_info
