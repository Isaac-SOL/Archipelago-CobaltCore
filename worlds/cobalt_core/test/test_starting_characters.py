from .bases import CobaltCoreTestBase


class CobaltCoreTestStartingCharacters(CobaltCoreTestBase):

    def test_has_forced_characters(self):
        """Test that the forced characters are indeed included in the starting characters"""
        if "forced_starting_characters" in self.options:
            for forced_char in self.options["forced_starting_characters"]:
                self.assertTrue(any(item.name == forced_char for item in self.multiworld.precollected_items[self.player]))


class TestStartWithTwoCharacters(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 2,
        "cro_is_installed": True
    }


class TestStartWithOneCharacter(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 1,
        "cro_is_installed": True
    }


class TestStartWithSpecificParty(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 3,
        "forced_starting_characters": ["Isaac", "Drake", "Max"]
    }


class TestStartWithSpecificSolo(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 1,
        "forced_starting_characters": ["Max"],
        "cro_is_installed": True
    }


class TestStartWithSpecificCharInParty(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 3,
        "forced_starting_characters": ["Max"]
    }


class TestMoreForcedCharsThanParty(CobaltCoreTestStartingCharacters):
    options = {
        "starting_characters_amount": 1,
        "forced_starting_characters": ["Isaac", "Drake", "Max"],
        "cro_is_installed": True
    }
