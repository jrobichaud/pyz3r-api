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
    response = client.post("/alttpr/daily", json={"sprite": "Peach"})
    assert type(response.data) == bytes


@pytest.mark.asyncio
def test_settings(client):
    response = client.get("/alttpr/settings")
    assert type(response.data) == str
