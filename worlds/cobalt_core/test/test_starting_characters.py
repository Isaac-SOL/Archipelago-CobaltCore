from .bases import CobaltCoreTestBase


class TestStartWithTwoCharacters(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 2,
        "cro_is_installed": True
    }


class TestStartWithOneCharacter(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 1,
        "cro_is_installed": True
    }


class TestStartWithSpecificParty(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 3,
        "forced_starting_characters": ["Isaac", "Drake", "Max"]
    }


class TestStartWithSpecificSolo(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 1,
        "forced_starting_characters": ["Max"],
        "cro_is_installed": True
    }


class TestStartWithSpecificCharInParty(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 3,
        "forced_starting_characters": ["Max"]
    }


class TestMoreForcedCharsThanParty(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 1,
        "forced_starting_characters": ["Isaac", "Drake", "Max"],
        "cro_is_installed": True
    }
