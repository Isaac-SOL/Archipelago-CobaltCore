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


class StartingCharactersAmount(Range):
    """Determines how many characters you will start the game with.
    If you want to specify characters to start with, use forced_starting_characters.
    Then, more characters will be added at random until the specified amount is reached.

    If you want to start with less than 3 characters:
    You need to install the mod "Custom Run Options" and set cro_is_installed to true.

    It's set to 3 by default to mimic the vanilla game. However, because of this, many items will be available
    from the start (big sphere 1). If this is an issue for you, lower this number."""
    display_name = "Starting Characters Amount"
    range_start = 1
    range_end = 8
    default = 3


class CROIsInstalled(Toggle):
    """Only set this on if you have installed the mod "Custom Run Options" (can be found on NexusMods).
    This will allow you to set starting_characters_amount below 3."""
    display_name = "Custom Run Options is installed"


class ForcedStartingCharacters(OptionSet):
    """Forces these characters to be unlocked at the start of the game.
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


class ShuffleShipParts(Choice):
    """Whether to shuffle the parts of every ship from the start.
    off: The ship parts are not shuffled.
    at_start: The ship parts are shuffled at the start and stay in that order between runs.
    every_run: The ship parts are shuffled in a new order every run."""
    display_name = "Shuffle Ship Parts"
    option_off = 0
    option_at_start = 1
    option_every_run = 2
    default = 1


class TotalMemoriesRequired(Range):
    """The minimum amount of memories required across all characters to complete the goal.
    If you set this to 1, then this parameter does not matter (see the next two parameters)"""
    display_name = "Memories Required (Total)"
    range_start = 1
    range_end = 24
    default = 1


class PerCharacterMemoriesRequired(Range):
    """The minimum amount of memories required per character to complete the goal.
    Works in tandem with characters_required to set the amount of characters that need to clear that condition.
    For example, if your goal should be 'At least 6 charaters need at least 2 memories unlocked',
            you should set memories_required_total = 1, memories_required_per_character = 2, characters_required = 6.
    You can also have, for example: 'At least 16 memories unlocked in total, with at least one on each character',
            which would be memories_required_total = 16, memories_required_per_character = 1, characters_required = 8."""
    display_name = "Memories Required (Per Character)"
    range_start = 1
    range_end = 3
    default = 1


class CharactersRequired(Range):
    """This is how many characters need to have the specified amount of memories in memories_required_per_character
    to complete the goal (see above for more details).
    Note that for the purposes of Archipelago, empty memories have been added for CAT and Books,
    which is why you can require up to 8 characters.
    If you set this to 1, then only memories_required_total matters."""
    display_name = "Characters Required"
    range_start = 1
    range_end = 8
    default = 8


class ShuffleMemories(Toggle):
    """Whether character memories will be shuffled into the multiworld.
    This adds 24 checks, and makes the goal into a 'mcguffin hunt'."""
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


class RandomizeStartingCards(Choice):
    """Whether to randomize which two cards each character starts a run with.
    off: The starting cards are not randomized.
    at_start: The starting cards are randomized and stay the same between runs.
    every_run: The starting cards are randomized every run, from the pool of unlocked cards.
               If forced_starting_cards are set (see below), they are only applied during generation.
    every_run_forced: The starting cards are randomized every run, from the pool of unlocked cards.
                      If forced_starting_cards are set (see below), they are applied every run."""
    display_name = "Randomize Starting Cards"
    option_off = 0
    option_at_start = 1
    option_every_run = 2
    option_every_run_forced = 3
    default = 1


class ForcedStartingCards(ItemSet):
    """Only active if randomize_starting_cards is set to at_start or every_run.
    Forces these cards to be among the starting cards.
    Only set up to 2 per character. If there are less, the rest are randomized.
    You cannot force starting cards for CAT, they use the vanilla behavior (random summons).

    Example: ['Evasive Shot', 'Hand Cannon', 'Shuffle Shot'] will:
    - Force the 2 starting cards for Riggs,
    - Force one starting card for Max and randomize the other,
    - And all starting cards for the other characters will be randomized."""
    display_name = "Starting Cards"
    default = frozenset([])


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
    Also note that infinite cards such as Dice Roll will not disappear even if they're Single Use.
    (you may want to take a look at immediate_rewards_blacklist)
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
    Remember that some artifacts are not strictly positive! (you may want to take a look at immediate_rewards_blacklist)
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
    This makes it easier to get specific items you want without commiting an entire run to it.
    Particularly useful if you're starting with less than three characters."""
    display_name = "Add Node to Swap Characters"


class ImmediateRewardsBlacklist(ItemSet):
    """For immediate_card_rewards, immediate_artifact_rewards and modifiers_mode,
    the items in this list will never be given immediately.
    You can also use item name groups."""
    display_name = "Immediate Rewards Blacklist"
    default = frozenset([])


class UnlockedCardBootOption(DefaultOnToggle):
    """Adds a boot option for every run that allows you to add an unlocked card to your deck."""
    display_name = "Unlocked Card Boot Option"


class UnlockedArtifactBootOption(Choice):
    """Adds a boot option for every run that allows you to add an unlocked artifact to your deck.
    off: Does not add this option.
    limited: Choose among up to 8 randomly-selected unlocked artifacts.
    all: Choose among all unlocked artifacts. (This will quickly become the best choice.)"""
    display_name = "Unlocked Artifact Boot Option"
    option_off = 0
    option_limited = 1
    option_all = 2
    default = 1


class SeenItemsAtShop(Choice):
    """Adds an option at Cleo's shop to get any AP item that you've seen at least once when picking rewards.
    This is recommended as part of larger system that avoids being stuck because of randomness.
    off: Does not add this option.
    this_run: You can only get AP items that you've seen in this run.
    my_characters: You can get AP items that you've seen in any run,
                   but only those that are tied to your current characters.
    all: You can get any AP item that you've seen in any run."""
    display_name = "Seen Items at Shop"
    option_off = 0
    option_this_run = 1
    option_my_characters = 2
    option_all = 3
    default = 2


class FillersCanBeTraps(DefaultOnToggle):
    """With this setting, filler items can be traps.
    At the moment, filler items only happen in very specific scenarios (mostly, if you use start_inventory_from_pool)"""
    display_name = "Filler Items can be Traps"


class AdditionalTraps(Range):
    """Adds traps to the item pool. This also adds as many checks, which will be randomly distributed
    as AP cards or artifacts."""
    display_name = "Additional Traps"
    range_start = 0
    range_end = 96
    default = 8


class ModifiersMode(Choice):
    """How daily modifiers will apply to your game.
    off: There will be no daily modifiers in your game.
    immediate: Modifiers will be items in the pool. When found, the modifier is applied until the end of the run.
               (some modifiers are excluded)
    unlockable: Modifiers will be items in the pool. Once found, new runs can randomly have this modifier.
    immediate_and_unlockable: Combines both effects.
    all_at_start: All modifiers can randomly apply to your new runs from the start."""
    display_name = "Modifiers Mode"
    option_off = 0
    option_immediate = 1
    option_unlockable = 2
    option_immediate_and_unlockable = 3
    option_all_at_start = 4
    default = 1


class ModifiersBlacklist(ItemSet):
    """Modifiers in this list will never be applied to your runs, neither randomly nor immediately.
    The modifiers are:
    - Binary Bosses: all bosses happen in a binary system
    - Boss Advantage: Start with a boss artifact
    - Core Corruption: Start with 2 corrupted cores
    - Enemy Shuffler: Enemies are shuffled at the start of the battle
    - Jupiter Toys: All battles have 2 jupiter drones, with one turned towards us
    - No Skips: Can't skip rewards
    - Scaffolds: Start with 2 scaffolds in the middle of the ship
    - Shuffler: Start shuffled (doesn't matter much if the setting is already set for AP)
    - One Hit Wonder: Start with 1 hull, cannot overheat
    - Supernova: Start with more HP, Most battles have a hot star
    - Sword and Shield: Start with more HP, enemies have 1 powerdrive
    - Draft Mode: Start by drafting 15 cards instead of the usual starter decks
    - Thin Deck: Start without colorless cards and a corrupted core
    - Only A upgrades: You can only do A upgrades
    - Only B upgrades: You can only do B upgrades"""
    display_name = "Modifiers Blacklist"
    default = frozenset([])


class SuperSecretSpecialCards(DefaultOnToggle):
    """Intended for syncs."""
    display_name = "Super Secret Special Cards"


# Actual option groups are specified in the WebWorld in __init__.py
@dataclass
class CobaltCoreOptions(PerGameCommonOptions):

    # Generic options
    start_inventory_from_pool: StartInventoryPool

    # Initial Parameters
    starting_ship: StartingShip
    starting_characters_amount: StartingCharactersAmount
    cro_is_installed: CROIsInstalled
    forced_starting_characters: ForcedStartingCharacters
    shuffle_ship_parts: ShuffleShipParts
    randomize_starting_cards: RandomizeStartingCards
    forced_starting_cards: ForcedStartingCards

    # Difficulty Management
    difficulty_logic: DifficultyLogic
    check_card_difficulty: CheckCardDifficulty

    # Goal
    memories_required_total: TotalMemoriesRequired
    memories_required_per_character: PerCharacterMemoriesRequired
    characters_required: CharactersRequired
    shuffle_memories: ShuffleMemories
    unlock_memory_for_all_characters: UnlockMemoryForAllCharacters
    do_future_memory: DoFutureMemory

    # Item Pools
    shuffle_cards: ShuffleCards
    shuffle_artifacts: ShuffleArtifacts
    modifiers_mode: ModifiersMode
    modifiers_blacklist: ModifiersBlacklist

    # Immediate Rewards
    immediate_card_rewards: ImmediateCardRewards
    immediate_card_attributes: ImmediateCardAttributes
    immediate_artifact_rewards: ImmediateArtifactRewards
    immediate_rewards_blacklist: ImmediateRewardsBlacklist

    # Miscellaneous Tweaks
    rewards_tweak: RewardsTweak
    auto_release_characters: AutoReleaseCharacters
    swap_character_node: SwapCharacterNode
    fillers_can_be_traps: FillersCanBeTraps
    additional_traps: AdditionalTraps
    unlocked_card_boot_option: UnlockedCardBootOption
    unlocked_artifact_boot_option: UnlockedArtifactBootOption
    seen_items_at_shop: SeenItemsAtShop
    super_secret_special_cards: SuperSecretSpecialCards
