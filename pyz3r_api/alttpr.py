import datetime

import aiohttp
import pyz3r
from flask import Blueprint, request, current_app, make_response


bp = Blueprint("alttpr", __name__, url_prefix="/alttpr")


@bp.route("/settings")
async def get_settings():
    alttpr = pyz3r.alttpr.ALTTPR()
    randomizer_settings = await alttpr.randomizer_settings()
    return randomizer_settings


@bp.route("/sprites")
async def sprites():
    alttpr = pyz3r.alttpr.ALTTPR()
    async with aiohttp.request(
        method="get",
        url=alttpr.baseurl + "/sprites",
        auth=alttpr.auth,
        raise_for_status=True,
    ) as resp:
        result = await resp.json()
    response = make_response(result)
    response.cache_control.max_age = 3600
    return response


@bp.post("/daily")
async def daily():
    alttpr = pyz3r.alttpr.ALTTPR()
    sprite = request.json.get("sprite", "Link")
    daily_hash = await alttpr.find_daily_hash()
    name = f"alttpr Daily {datetime.datetime.now(tz=datetime.timezone.utc).date().isoformat()} {daily_hash}.sfc"
    seed = await alttpr.retrieve(daily_hash)
    game = await seed.create_patched_game(
        current_app.config["ROM_PATH"], spritename=sprite
    )
    response = make_response(game.rom)
    response.headers.set("Content-Type", "application/octet-stream")
    response.headers.set("Content-Disposition", "attachment", filename=name)
    return response


@bp.post("/generate")
async def generate():
    alttpr = pyz3r.alttpr.ALTTPR()
    sprite = request.json.get("sprite", "Link")
    settings = request.json.get("settings")
    seed = await alttpr.generate(settings=settings)
    name = f'alttpr {datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} {seed.hash}.sfc'
    game = await seed.create_patched_game(
        current_app.config["ROM_PATH"], spritename=sprite
    )
    response = make_response(game.rom)
    response.headers.set("Content-Type", "application/octet-stream")
    response.headers.set("Content-Disposition", "attachment", filename=name)
    return response
