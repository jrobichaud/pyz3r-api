import base64
import pyz3r
from flask import Blueprint, current_app, make_response, request

from pyz3r_api.ips_utils import patch_with_ips

bp = Blueprint("sm", __name__, url_prefix="/sm")


@bp.post("/generate")
async def generate():
    request_data = request.json
    skills_preset = request_data.get("skills_preset", "regular")
    settings_preset = request_data.get("settings_preset", "default")
    race = request_data.get("race", False)
    seed = await pyz3r.smvaria.SuperMetroidVaria.create(
        skills_preset=skills_preset,
        settings_preset=settings_preset,
        race=race,
    )

    patch_data = base64.b64decode(seed.data["ips"])
    with open(current_app.config["SM_ROM_PATH"], "rb") as f:
        file_data = bytearray(f.read())

    patch_with_ips(file_data, patch_data)

    response = make_response(file_data)
    response.headers.set("Content-Type", "application/octet-stream")
    response.headers.set(
        "Content-Disposition", "attachment", filename=seed.data["fileName"]
    )
    return response
