import typing
from dataclasses import dataclass

from Options import Option, Choice, OptionSet, DefaultOnToggle, Range, PerGameCommonOptions, Toggle, StartInventoryPool, \
    ItemSet


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


class ShuffleShipParts(OptionSet):
    """Whether to shuffle the parts of every ship from the start.
    off: The ship parts are not shuffled.
    at_start: The ship parts are shuffled at the start and stay in that order between runs.
    every_run: The ship parts are shuffled in a new order every run."""
    display_name = "Shuffle Ship Parts"
    option_off = 0
    option_at_start = 1
    option_every_run = 2
    default = 1


class WinCondition(Choice):
    """What the goal is for this player.
    total_memories: The player will have to accumulate a certain amount of memories across all characters.
    memory_per_character: The player will have to accumulate a certain amount of memories for every character."""
    display_name = "Win Condition"
    option_total_memories = 0
    option_memory_per_character = 1
    default = 1


class TotalMemoriesRequired(Range):
    """If win_condition is set to total_memories, how many memories are needed across all characters to complete the goal.
    Note: also pay attention to additional_character_memories which count towards this."""
    display_name = "Memories Required (Total)"
    range_start = 1
    range_end = 24
    default = 8


class PerCharacterMemoriesRequired(Range):
    """If win_condition is set to memory_per_character, how many memories are needed per character to complete the goal.
    Note: if additional_character_memories is true, Books and CAT will be included."""
    display_name = "Memories Required (Per Character)"
    range_start = 1
    range_end = 3
    default = 1


class AddCharacterMemories(DefaultOnToggle):
    """Whether the game should add dummy memories for Books and CAT that will count towards the goal."""
    display_name = "Add Character Memories (for Books and CAT)"


class ShuffleMemories(Toggle):
    """Whether character memories will be shuffled into the multiworld.
    This adds 18 checks, or 24 if add_character_memories is set to true."""
    display_name = "Shuffle Memories"
    default = False


class UnlockMemoryForAllCharacters(Toggle):
    """If this option is set, when you complete a run, you will be able to unlock one memory for all of your
    selected characters at once. This is recommended for synced runs."""
    display_name = "Unlock Memory For All Characters"
    default = True


class DoFutureMemory(DefaultOnToggle):
    """Whether the player will have to do the Future Memory sequence to complete the game once they have fulfilled
    their win condition. Otherwise, the game will immediately be completed."""
    display_name = "Do Future Memory to Complete the Game"


class RandomizeStartingCards(DefaultOnToggle):
    """Whether to randomize which cards each character starts a run with.
    off: The starting cards are not randomized.
    at_start: The starting cards are randomized and stay the same between runs.
    every_run: The starting cards are randomized every run, from the pool of unlocked cards."""
    display_name = "Randomize Starting Cards"
    option_off = 0
    option_at_start = 1
    option_every_run = 2
    default = 1


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


class ImmediateCardAttributes(OptionSet):
    """If immediate_card_rewards is not set to "never", determines which additional attributes cards received this way
    will have. You can choose multiple attributes.
    Note that if you choose neither "Temporary" nor "Single Use", these cards will stay in your deck unless removed
    by some other means.
    Valid attributes: Temporary, Single Use, Exhaust, Discount, Recycle, Retain"""
    display_name = "Received Card's Attributes"
    valid_keys = {
        "Temporary",
        "Single Use",
        "Exhaust",
        "Discount",
        "Recycle",
        "Retain"
    }
    default = frozenset(["Single Use"])


class ImmediateArtifactRewards(Choice):
    """Determines under which conditions the game will immediately add an artifact to your current run
    when it is found in the multiworld (provided you have started a run).
    never: Do not automatically add found artifacts.
    if_has_deck: Only add the artifact if you have the corresponding character.
    if_local: Only add the artifact if you found it yourself.
    if_local_and_has_deck: Only add the artifact if you found it yourself, and you have the corresponding character.
    always: Always automatically add the artifact"""
    display_name = "Immediate Artifact Rewards"
    option_never = 0
    option_if_has_deck = 1
    option_if_local = 2
    option_if_local_and_has_deck = 3
    option_always = 4
    default = 4


class ShuffleCards(DefaultOnToggle):
    """Whether card unlocks will be shuffled into the multiworld. This adds about 160 checks."""
    display_name = "Shuffle Cards"


class ShuffleArtifacts(Choice):
    """How Artifact unlocks will be shuffled into the multiworld. This adds about 80 checks.
    off: Artifacts will not be shuffled into the multiworld.
    simple: Archipelago artifacts will give one archipelago item.
    double: Most Archipelago artifacts will give two items (there will be about half as many to find)
            This is the default because there are relatively few artifact offerings compared to the amount of checks."""
    display_name = "Shuffle Artifacts"
    option_off = 0
    option_simple = 1
    option_double = 2
    default = 2


class CheckCardDifficulty(Range):
    """If shuffle_cards is set to true, determines the base cost of cards that send items in the multiworld.
    This also determines the strength of the A and B upgrades, which cost up to 2 less and 1 less respectively.
    A value of -1 means that the card costs 0 and lets you draw 1, making it effectively free.
    Do note that getting these cards is easy and has little impact on your deck since they self-destruct.
    That is why the cost is set to 2 by default."""
    display_name = "Check Card Difficulty"
    range_start = -1
    range_end = 4
    default = 2


class RewardsTweak(Choice):
    """Makes unlocked cards and artifacts appear more often in offerings.
    Otherwise, It might be very hard to get them at the beginning.
    none: Do not tweak card and artifact rewards.
    more_unlocked: Get unlocked cards and artifacts a bit more often.
    all_unlocked: All cards and artifacts found in rewards are unlocked.
    """
    display_name = "Rewards Tweak"
    option_none = 0
    option_more_unlocked = 1
    option_all_unlocked = 2
    default = 1


class DifficultyLogic(Choice):
    """How the generator determines how far you can get with a given character.
    count_all: Counts all the character's cards and artifacts (including basic ones).
               This is the safest option, but makes all cards and artifacts progression items.
    count_rare: Only counts rare cards and boss artifacts (including basic ones).
                This makes rare cards and boss artifacts progression items.
    dont_count: A character is considered completable as soon as it's unlocked.
                You might be forced to do some very difficult runs!"""
    display_name = "Difficulty Logic"
    option_count_all = 0
    option_count_rare = 1
    option_dont_count = 2
    default = 1


class AutoReleaseCharacters(Range):
    """When you complete a character by finishing a run with them a certain amount of times,
    release all items associated with that character instantly, so you don't need to play them anymore.
    The value corresponds to the amount of memory unlocks that you need to do for that to happen.
    A value of 0 deactivates this option."""
    display_name = "Auto-Release Characters"
    range_start = 0
    range_end = 3
    default = 0


class SwapCharacterNode(DefaultOnToggle):
    """Adds a node to every map that allows you to swap one of your characters with any unlocked character.
    This makes it easier to get specific items you want without commiting an entire run to it."""
    display_name = "Add Node to Swap Characters"


class ImmediateRewardsBlacklist(ItemSet):
    """No matter what the settings for immediate_card_rewards and immediate_artifact_rewards are,
    the items in this list will be excluded.
    You can also use item name groups (explained below)."""
    display_name = "Immediate Rewards Blacklist",
    default = frozenset([])


# Actual option groups are specified in the WebWorld in __init__.py
@dataclass
class CobaltCoreOptions(PerGameCommonOptions):

    # Generic options
    start_inventory_from_pool: StartInventoryPool

    # Initial Parameters
    starting_ship: StartingShip
    starting_characters: StartingCharacters
    shuffle_ship_parts: ShuffleShipParts
    randomize_starting_cards: RandomizeStartingCards

    # Difficulty Management
    difficulty_logic: DifficultyLogic
    check_card_difficulty: CheckCardDifficulty

    # Goal
    win_condition: WinCondition
    memories_required_total: TotalMemoriesRequired
    memories_required_per_character: PerCharacterMemoriesRequired
    additional_character_memories: AddCharacterMemories
    shuffle_memories: ShuffleMemories
    unlock_memory_for_all_characters: UnlockMemoryForAllCharacters
    do_future_memory: DoFutureMemory

    # Item Pools
    shuffle_cards: ShuffleCards
    shuffle_artifacts: ShuffleArtifacts

    # Immediate Rewards
    immediate_card_rewards: ImmediateCardRewards
    immediate_card_attributes: ImmediateCardAttributes
    immediate_artifact_rewards: ImmediateArtifactRewards
    immediate_rewards_blacklist: ImmediateRewardsBlacklist

    # Miscellaneous Tweaks
    rewards_tweak: RewardsTweak
    auto_release_characters: AutoReleaseCharacters
    swap_character_node: SwapCharacterNode
