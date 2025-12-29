from .bases import CobaltCoreTestBase


class TestStartingCardsRandomized(CobaltCoreTestBase):
    options = {
        "randomize_starting_cards": True
    }


class TestStartingCardsStandard(CobaltCoreTestBase):
    options = {
        "randomize_starting_cards": False
    }
