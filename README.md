<div align="center">

# pastemc

</div>

## Launch

Install Python `>= 3.12` and [Poetry](https://python-poetry.org/docs/#installation), then,

Run `poetry install`, then,

[Active virtual environment](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment), then,

Rename `.config.example.yaml` to `.config.yaml`, then,

Dev Launch:

``` bash
uvicorn pastemc.main:app --reload --host 0.0.0.0 --port 8056
```

Prod Launch:

``` bash
uvicorn pastemc.main:app --host 0.0.0.0 --port 8056
```
