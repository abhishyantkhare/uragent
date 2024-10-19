import json

from fastapi.openapi.utils import get_openapi
from src.api import app

with open("openapi.json", "w") as f:
    json.dump(
        get_openapi(
            title="Engram Backend API",
            version=app.version,
            routes=app.routes,
            separate_input_output_schemas=False,
        ),
        f,
    )
