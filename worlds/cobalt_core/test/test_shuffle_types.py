from .bases import CobaltCoreTestBase
from .. import ShuffleArtifacts, ModifiersMode, RandomizeStartingCards, AdditionalTraps


class TestShuffleMemories(CobaltCoreTestBase):
    options = {
        "shuffle_memories": True
    }


class TestShuffleArtifactsOnly(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple,
        "shuffle_cards": False,
        "randomize_starting_cards": RandomizeStartingCards.option_off
    }


class TestDontShuffleCardsButStillStarting(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple,
        "shuffle_cards": False,
        "randomize_starting_cards": RandomizeStartingCards.option_at_start
    }


class TestShuffleCardsAndArtifacts(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple
    }


class TestDontShuffleCardsOrMemories(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple,
        "shuffle_cards": False,
        "shuffle_memories": False
    }


class TestDontShuffleArtifactsOrMemories(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_off,
        "shuffle_memories": False
    }


class TestModifiersUnlockable(CobaltCoreTestBase):
    options = {
        "modifiers_mode": ModifiersMode.option_unlockable
    }


class TestNoModifiers(CobaltCoreTestBase):
    options = {
        "modifiers_mode": ModifiersMode.option_off
    }


class TestBlacklistModifiers(CobaltCoreTestBase):
    options = {
        "modifiers_mode": ModifiersMode.option_unlockable,
        "modifiers_blacklist": ["Jupiter Toys", "Binary Bosses"]
    }


class TestBlacklistModifiersAtStart(CobaltCoreTestBase):
    options = {
        "modifiers_mode": ModifiersMode.option_all_at_start,
        "modifiers_blacklist": ["Jupiter Toys", "Binary Bosses"]
    }


class TestNoTraps(CobaltCoreTestBase):
    options = {
        "additional_traps": 0
    }


class TestMaxTraps(CobaltCoreTestBase):
    options = {
        "additional_traps": AdditionalTraps.range_end
    }


class TestMaxTrapsCardsOnly(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_off,
        "additional_traps": AdditionalTraps.range_end
    }


class TestMaxTrapsArtifactsOnly(CobaltCoreTestBase):
    options = {
        "shuffle_cards": False,
        "additional_traps": AdditionalTraps.range_end
    }
