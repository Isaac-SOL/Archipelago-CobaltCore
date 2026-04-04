from .bases import CobaltCoreTestBase
from .. import ShuffleArtifacts, ModifiersMode


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


class TestShuffleArtifactsOnly(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple,
        "shuffle_cards": False,
        "randomize_starting_cards": False
    }


class TestDontShuffleCardsButStillStarting(CobaltCoreTestBase):
    options = {
        "shuffle_artifacts": ShuffleArtifacts.option_simple,
        "shuffle_cards": False,
        "randomize_starting_cards": True
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
