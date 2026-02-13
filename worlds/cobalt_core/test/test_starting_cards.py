from .bases import CobaltCoreTestBase
from .. import CHARACTERS, item_table


def test_starting_cards_good_standalone(self: CobaltCoreTestBase):
    """Test that starting cards follow the rules for a good start"""
    mw = self.multiworld
    state = mw.state
    starting_items = mw.precollected_items[self.player]
    starting_item_names = [item.name for item in starting_items]
    print("Starting items:", starting_item_names)
    for c in CHARACTERS:
        if c == "CAT":
            char_cards = set([name for name in item_table if item_table[name].character == c])
            char_card_count = len(char_cards.intersection(starting_item_names))
            self.assertEqual(char_card_count, 0, f"{c} must have zero cards at the start")
        elif c != "Max":
            if c == "Books" or c == "Drake":
                generator_cards = set([name for name in item_table if item_table[name].character == c and item_table[name].generator])
                has_gen_card = len(generator_cards.intersection(starting_item_names)) > 0
                self.assertTrue(has_gen_card, f"{c} must have at least one generator card at the start")
            offensive_cards = set([name for name in item_table if item_table[name].character == c and item_table[name].offensive])
            has_off_card = len(offensive_cards.intersection(starting_item_names)) > 0
            self.assertTrue(has_off_card, f"{c} must have at least one offensive card at the start")


class TestStartingCardsRandomized(CobaltCoreTestBase):
    options = {
        "randomize_starting_cards": True
    }

    def test_starting_cards_good(self):
        """Test that randomized starting cards follow the rules for a good start"""
        test_starting_cards_good_standalone(self)


class TestStartingCardsStandard(CobaltCoreTestBase):
    options = {
        "randomize_starting_cards": False
    }

    def test_starting_cards_good(self):
        """Test that basic starting cards follow the rules for a good start"""
        test_starting_cards_good_standalone(self)
