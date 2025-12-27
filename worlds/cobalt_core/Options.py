import typing
from dataclasses import dataclass

from Options import Option, Choice, OptionSet, DefaultOnToggle, Range, PerGameCommonOptions
from worlds.ladx.Options import DefaultOffToggle


class StartingShip(Choice):
    """Determines which ship you will start the game with."""
    display_name = "Starting Ship"
    option_Artemis = 0
    option_Ares = 1
    option_Jupiter = 2
    option_Gemini = 3
    option_Tiderunner = 4


class StartingCharacters(OptionSet):
    """Determine which characters you will start the game with.
    If there are less than 3 characters, more will be added at random.
    Valid names: Dizzy, Riggs, Peri, Isaac, Drake, Max, Books, CAT"""
    display_name = "Starting Characters"
    valid_keys = {
        "Dizzy",
        "Riggs",
        "Peri",
        "Isaac",
        "Drake",
        "Max",
        "Books",
        "CAT"
    }
    default = frozenset([])


class MinimumDifficulty(Choice):
    """Determines the minimum difficulty allowed in your game."""
    display_name = "Minimum Difficulty"
    option_normal = 0
    option_hard = 1
    option_harder = 2
    option_hardest = 3
    default = 0


class WinCondition(Choice):
    option_total_memories = 0
    option_memory_per_character = 1


class TotalMemoriesRequired(Range):
    range_start = 1
    range_end = 24
    default = 24


class PerCharacterMemoriesRequired(Range):
    range_start = 1
    range_end = 3
    default = 3


class AddCharacterMemories(DefaultOnToggle):
    display_name = "Add character memories (for Books and CAT)"


class ShuffleMemories(DefaultOffToggle):
    """Whether character memories should be shuffled."""
    display_name = "Shuffle Memories"


class DoFutureMemory(DefaultOnToggle):
    pass


class RandomizeStartingCards(DefaultOnToggle):
    """Whether to randomize which cards each character starts a run with."""
    display_name = "Randomize Starting Cards"


class ImmediateCardRewards(Choice):
    """Determines under which conditions the game will immediately add a card to your current deck
    when it is found in the multiworld (provided you have started a run).
    never: Do not automatically add found cards to our deck.
    if_has_deck: Only add the card if you have the corresponding character.
    if_local: Only add the card if you found it yourself.
    if_local_and_has_deck: Only add the card if you found it yourself, and you have the corresponding character.
    always: Always automatically add the card"""
    display_name = "Immediate Card Rewards"
    option_never = 0
    option_if_has_deck = 1
    option_if_local = 2
    option_if_local_and_has_deck = 3
    option_always = 4
    default = 4


@dataclass
class CobaltCoreOptions(PerGameCommonOptions):
    starting_ship = StartingShip
    starting_characters = StartingCharacters
    minimum_difficulty = MinimumDifficulty
    win_condition = WinCondition
    memories_required_total = TotalMemoriesRequired
    memories_required_per_character = PerCharacterMemoriesRequired
    additional_character_memories = AddCharacterMemories
    do_future_memory = DoFutureMemory
    randomize_starting_cards = RandomizeStartingCards
    immediate_card_rewards = ImmediateCardRewards
