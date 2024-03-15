<div align="center">

# pastemc

</div>

## Launch

Rename `.config.example.yaml` to `.config.yaml`, then,

Dev Launch:

``` bash
uvicorn pastemc.main:app --reload --host 0.0.0.0
```

Prod Launch:

``` bash
uvicorn pastemc.main:app --host 0.0.0.0 --port 8056
```
