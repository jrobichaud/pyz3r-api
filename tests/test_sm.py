import pytest

from pyz3r_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {
            "TESTING": True,
            "SM_ROM_PATH": "./Super Metroid (JU) [!].smc",
        }
    ).testing


@pytest.mark.asyncio
def test_generate(client):
    response = client.post("/sm/generate")
    assert type(response.data) == bytes
