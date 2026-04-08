from .bases import CobaltCoreTestBase


class TestStartWithTwoCharacters(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 2
    }


class TestStartWithOneCharacter(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 1
    }