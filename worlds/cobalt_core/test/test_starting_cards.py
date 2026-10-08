from .bases import CobaltCoreTestBase
from .. import CHARACTERS, item_table
from ..Options import RandomizeStartingCards


class CobaltCoreTestStartingCards(CobaltCoreTestBase):

    def get_forced_card_count(self, character: str) -> int:
        return len([card for card in self.world.options.forced_starting_cards.value if item_table[card].character == character])

    def test_starting_cards_good(self):
        """Test that starting cards follow the rules for a good start"""
        mw = self.multiworld
        starting_items = mw.precollected_items[self.player]
        starting_item_names = [item.name for item in starting_items]
        print("Starting items:", starting_item_names)
        for c in CHARACTERS:
            char_cards = set([name for name in item_table if item_table[name].character == c])
            char_card_count = len(char_cards.intersection(starting_item_names))
            # CAT doesn't have starting cards, they're handled by the game itself
            if c == "CAT":
                self.assertEqual(char_card_count, 0, f"{c} must have zero cards at the start")
            else:
                self.assertEqual(char_card_count, 2, f"{c} must have two cards at the start")
            # Max doesn't start with an offensive card. Also, if both cards are forced, then we don't check
            if c not in ["Max", "CAT"] and self.get_forced_card_count(c) < 2:
                if c == "Books" or c == "Drake":
                    generator_cards = set([name for name in item_table if item_table[name].character == c and item_table[name].generator])
                    has_gen_card = len(generator_cards.intersection(starting_item_names)) > 0
                    self.assertTrue(has_gen_card, f"{c} must have at least one generator card at the start")
                offensive_cards = set([name for name in item_table if item_table[name].character == c and item_table[name].offensive])
                has_off_card = len(offensive_cards.intersection(starting_item_names)) > 0
                self.assertTrue(has_off_card, f"{c} must have at least one offensive card at the start")


class TestStartingCardsStandard(CobaltCoreTestStartingCards):
    options = {
        "randomize_starting_cards": RandomizeStartingCards.option_off
    }


class TestStartingCardsRandomized(CobaltCoreTestStartingCards):
    options = {
        "randomize_starting_cards": RandomizeStartingCards.option_at_start
    }


class TestStartingCardsRandomizedOneForced(CobaltCoreTestStartingCards):
    options = {
        "randomize_starting_cards": RandomizeStartingCards.option_at_start,
        "forced_starting_cards": ["Evasive Shot", "Big Shield", "Shuffle Shot", "Zero Draw"]
    }


class TestStartingCardsRandomizedBothForcedInvalid(CobaltCoreTestStartingCards):
    options = {
        "randomize_starting_cards": RandomizeStartingCards.option_at_start,
        "forced_starting_cards": ["Bolt", "Juke", "Serenity", "Heatsink"]
    }
