import os
import tempfile

import pytest
from pyz3r_api import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "ROM_PATH": "../Zelda no Densetsu - Kamigami no Triforce (Japan).sfc",
            "SM_ROM_PATH": "../Super Metroid (JU) [!].smc",
        }
    )

    yield app


@pytest.fixture
def client(app):
    with app.test_client() as testing_client:
        yield testing_client  # this is where the testing happens!


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
