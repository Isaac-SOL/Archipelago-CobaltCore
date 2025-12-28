import typing
from dataclasses import dataclass

from Options import Option, Choice, OptionSet, DefaultOnToggle, Range, PerGameCommonOptions, Toggle


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
    """What the goal is for this player.
    total_memories: The player will have to accumulate a certain amount of memories across all characters.
    memory_per_character: The player will have to accumulate a certain amount of memories for every character."""
    display_name = "Win Condition"
    option_total_memories = 0
    option_memory_per_character = 1
    default = 1


class TotalMemoriesRequired(Range):
    """If win_condition is total_memories, how many memories are needed across all characters to complete the goal.
    Note: also pay attention to additional_character_memories which count towards this."""
    display_name = "Memories Required (Total)"
    range_start = 1
    range_end = 24
    default = 8


class PerCharacterMemoriesRequired(Range):
    """If win_condition is memory_per_character, how many memories are needed per character to complete the goal.
    Note: if additional_character_memories is true, Books and CAT will be included."""
    display_name = "Memories Required (Per Character)"
    range_start = 1
    range_end = 3
    default = 3


class AddCharacterMemories(DefaultOnToggle):
    """Whether the game should add dummy memories for Books and CAT that will count towards the goal"""
    display_name = "Add character memories (for Books and CAT)"


class ShuffleMemories(Toggle):
    """Whether character memories should be shuffled."""
    display_name = "Shuffle Memories"
    default = False


class DoFutureMemory(DefaultOnToggle):
    """Whether the player will have to do the Future Memory sequence to complete the game once they have fulfilled
    their win condition. Otherwise, the game will immediately be completed."""
    display_name = "Do Future Memory to Complete the Game"


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
    starting_ship: StartingShip
    starting_characters: StartingCharacters
    minimum_difficulty: MinimumDifficulty
    win_condition: WinCondition
    memories_required_total: TotalMemoriesRequired
    memories_required_per_character: PerCharacterMemoriesRequired
    additional_character_memories: AddCharacterMemories
    shuffle_memories: ShuffleMemories
    do_future_memory: DoFutureMemory
    randomize_starting_cards: RandomizeStartingCards
    immediate_card_rewards: ImmediateCardRewards
