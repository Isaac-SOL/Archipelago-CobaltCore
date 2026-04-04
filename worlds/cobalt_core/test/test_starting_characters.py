from .bases import CobaltCoreTestBase


class TestStartWithTwoCharacters(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 2
    }


class TestStartWithOneCharacter(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 1
    }


class TestStartUnmanned(CobaltCoreTestBase):
    options = {
        "starting_characters_amount": 0
    }