from .bases import CobaltCoreTestBase


class TestShuffleMemories(CobaltCoreTestBase):
    options = {
        "shuffle_memories": True
    }


class TestNoAdditionalMemories(CobaltCoreTestBase):
    options = {
        "additional_character_memories": False
    }


class TestShuffleAndNoAdditionalMemories(CobaltCoreTestBase):
    options = {
        "shuffle_memories": True,
        "additional_character_memories": False
    }


class TestDontShuffleCards(CobaltCoreTestBase):
    options = {
        "shuffle_cards": False,
        "randomize_starting_cards": False
    }


class TestDontShuffleCardsButStillStarting(CobaltCoreTestBase):
    options = {
        "shuffle_cards": False,
        "randomize_starting_cards": True
    }


class TestDontShuffleArtifacts(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": False
    }


class TestDontShuffleCardsOrMemories(CobaltCoreTestBase):
    options = {
        "shuffle_cards": False,
        "shuffle_memories": False
    }


class TestDontShuffleArtifactsOrMemories(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": False,
        "shuffle_memories": False
    }
