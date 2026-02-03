from .bases import CobaltCoreTestBase


class TestAllShipsAtStart(CobaltCoreTestBase):
    options = {
        "start_inventory_from_pool": {
            "Artemis": 1,
            "Ares": 1,
            "Jupiter": 1,
            "Gemini": 1,
            "Tiderunner": 1
        }
    }
