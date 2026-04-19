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
