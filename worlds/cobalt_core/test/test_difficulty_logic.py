from .bases import CobaltCoreTestBase
from .. import DifficultyLogic


class TestDifficultyCountRare(CobaltCoreTestBase):
    options = {
        "difficulty_logic": DifficultyLogic.option_count_rare
    }


class TestDifficultyDontCount(CobaltCoreTestBase):
    options = {
        "difficulty_logic": DifficultyLogic.option_dont_count
    }
