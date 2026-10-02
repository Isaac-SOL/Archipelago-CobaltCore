from .bases import CobaltCoreTestBase


class TestGoalTotal(CobaltCoreTestBase):
    options = {
        "memories_required_total": 24,
        "memories_required_per_character": 1,
        "characters_required": 1
    }


class TestGoalTotalShuffled(CobaltCoreTestBase):
    options = {
        "memories_required_total": 24,
        "memories_required_per_character": 1,
        "characters_required": 1,
        "shuffle_memories": True
    }


class TestGoalMixed(CobaltCoreTestBase):
    options = {
        "memories_required_total": 16,
        "memories_required_per_character": 1,
        "characters_required": 8
    }


class TestGoalMixedShuffled(CobaltCoreTestBase):
    options = {
        "memories_required_total": 16,
        "memories_required_per_character": 1,
        "characters_required": 8,
        "shuffle_memories": True
    }
