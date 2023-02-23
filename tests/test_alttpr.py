import pytest

from pyz3r_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {
            "TESTING": True,
            "ROM_PATH": "./Zelda no Densetsu - Kamigami no Triforce (Japan).sfc",
        }
    ).testing


@pytest.mark.asyncio
def test_daily(client):
    response = client.post("/alttpr/daily", json={"sprite": "Princess Peach"})
    assert type(response.data) == bytes


@pytest.mark.asyncio
def test_settings(client):
    response = client.get("/alttpr/settings")
    assert type(response.json) == dict


@pytest.mark.asyncio
def test_generate(client):
    response = client.post(
        "/alttpr/generate",
        json={
            "sprite": "Princess Peach",
            "settings": {
                "accessibility": "items",
                "boss_shuffle": "none",
                "dungeon_items": "standard",
                "enemy_damage": "default",
                "enemy_health": "default",
                "enemy_shuffle": "none",
                "entrance_shuffle": "none",
                "ganon_open": "7",
                "glitches_required": "none",
                "goal": "ganon",
                "hints": "on",
                "item_functionality": "normal",
                "item_placement": "advanced",
                "item_pool": "normal",
                "tower_open": "7",
                "weapons": "randomized",
                "world_state": "open",
            },
        },
    )
    assert type(response.data) == bytes
