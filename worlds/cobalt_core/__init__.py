import itertools
import random
from typing import ClassVar, Dict, Set, List, Mapping, Any
from BaseClasses import Tutorial, Item, ItemClassification, Location, Region, Entrance, CollectionState
from Options import OptionGroup, OptionError
from .Items import item_table, find_items
from ..AutoWorld import WebWorld, World
from .Options import *
from .Locations import location_table, find_locations_max, find_locations_base
from ..generic.Rules import set_rule
from .Constants import *

CHARACTERS = ["Dizzy", "Riggs", "Peri", "Isaac", "Drake", "Max", "Books", "CAT"]
CARD_RARITIES = ["Common", "Uncommon", "Rare"]
ARTIFACT_RARITIES = ["Common", "Boss"]
ALL_RARITIES = set(CARD_RARITIES).union(ARTIFACT_RARITIES)
SHIPS = ["Artemis", "Ares", "Jupiter", "Gemini", "Tiderunner"]


class CobaltCoreWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Cobalt Core for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "cobalt-core_en.md",
        "cobalt-core/en",
        ["SaltyIsaac"]
    )]
    option_groups = [
        OptionGroup("Initial Parameters", [
            StartingShip,
            StartingCharactersAmount,
            CROIsInstalled,
            StartingCharacters,
            ShuffleShipParts,
            RandomizeStartingCards
        ]),
        OptionGroup("Difficulty Management", [
            DifficultyLogic,
            CheckCardDifficulty
        ]),
        OptionGroup("Goal", [
            WinCondition,
            TotalMemoriesRequired,
            PerCharacterMemoriesRequired,
            AddCharacterMemories,
            ShuffleMemories,
            UnlockMemoryForAllCharacters,
            DoFutureMemory
        ]),
        OptionGroup("Item Pools", [
            ShuffleCards,
            ShuffleArtifacts,
            ModifiersMode,
            ModifiersBlacklist
        ]),
        OptionGroup("Immediate Rewards", [
            ImmediateCardRewards,
            ImmediateCardAttributes,
            ImmediateArtifactRewards,
            ImmediateRewardsBlacklist
        ]),
        OptionGroup("Miscellaneous Tweaks", [
            RewardsTweak,
            AutoReleaseCharacters,
            SwapCharacterNode,
            FillersCanBeTraps,
            PickMissedItemsFromEveryRun
        ])
    ]


class CobaltCoreWorld(World):
    """
    A sci-fi roguelike deckbuilder with a deep new single-axis spin on tactics games! Dodge missiles,
    line up your cannons, and blast 'em out of the sky... Then get to the bottom of these time loops,
    before it's too late!
    """
    game = "Cobalt Core"

    options_dataclass = CobaltCoreOptions
    options: CobaltCoreOptions

    web = CobaltCoreWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = {}
    for name, data in location_table.items():
        if data.amount == 1:
            location_name_to_id[name] = data.address
        else:
            for i in range(data.amount if data.type == "Memory" else max(data.amount, max_fill_location)):
                location_name_to_id[f"{name} {i + 1}"] = data.address + i

    # These fields must not be initialized here as they will be modified at runtime
    location_name_to_eff_amount: dict[str, int]

    starting_characters: list[str]
    non_starting_characters: list[str]
    starting_ship: str
    non_starting_ships: list[str]
    starting_cards: list[str]
    starting_modifiers: list[str]

    dont_pool_items: list[str]
    dont_register_locations: list[str]

    additional_fillers: int

    fixed_client_seed: int

    # Fill item groups
    item_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Ships": find_items(item_type="Ship"),
        "Characters": find_items(item_type="Character"),
        "Memories": find_items(item_type="Memory"),
        "Cards": find_items(item_type="Card"),
        "Artifacts": find_items(item_type="Artifact"),
        "Basic Artifacts": find_items(item_type="Artifact", item_character=""),
        "Basic Boss Artifacts": find_items(item_type="Artifact", item_rarity="Boss", item_character=""),
        "Modifiers": find_items(item_type="Modifier"),
        "Filler Items": find_items(item_type="Filler"),
        "Traps": find_items(item_type="Trap")
    }
    for r in CARD_RARITIES:
        item_name_groups[f"{r} Cards"] = find_items(item_type="Card", item_rarity=r)
    for r in ARTIFACT_RARITIES:
        item_name_groups[f"{r} Artifacts"] = find_items(item_type="Artifact", item_rarity=r)
    for c in CHARACTERS:
        item_name_groups[f"{c} Cards"] = find_items(item_type="Card", item_character=c)
        item_name_groups[f"{c} Artifacts"] = find_items(item_type="Artifact", item_character=c)
        for r in CARD_RARITIES:
            item_name_groups[f"{c} {r} Cards"] = find_items(item_type="Card", item_character=c, item_rarity=r)
        for r in ARTIFACT_RARITIES:
            item_name_groups[f"{c} {r} Artifacts"] = find_items(item_type="Artifact", item_character=c, item_rarity=r)

    # Fill location groups
    location_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Ship Unlocks": find_locations_max(loc_type="Ship"),
        "Character Unlocks": find_locations_max(loc_type="Character"),
        "Memory Unlocks": find_locations_max(loc_type="Memory"),
        "Cards": find_locations_max(loc_type="Card"),
        "Artifacts": find_locations_max(loc_type="Artifact"),
        "Basic Artifacts": find_locations_max(loc_type="Artifact", loc_character=""),
        "Basic Boss Artifacts": find_locations_max(loc_type="Artifact", loc_rarity="Boss", loc_character="")
    }
    for r in CARD_RARITIES:
        location_name_groups[f"{r} Cards"] = find_locations_max(loc_type="Card", loc_rarity=r)
    for r in ARTIFACT_RARITIES:
        location_name_groups[f"{r} Artifacts"] = find_locations_max(loc_type="Artifact", loc_rarity=r)
    for c in CHARACTERS:
        location_name_groups[f"{c} Cards"] = find_locations_max(loc_type="Card", loc_character=c)
        location_name_groups[f"{c} Artifacts"] = find_locations_max(loc_type="Artifact", loc_character=c)
        for r in CARD_RARITIES:
            location_name_groups[f"{c} {r} Cards"] = find_locations_max(loc_type="Card", loc_rarity=r, loc_character=c)
        for r in ARTIFACT_RARITIES:
            location_name_groups[f"{c} {r} Artifacts"] = find_locations_max(loc_type="Artifact", loc_rarity=r,
                                                                            loc_character=c)

    def get_base_loc_eff_amount(self, loc: str) -> int:
        if loc in self.dont_register_locations:
            return 0
        return self.location_name_to_eff_amount[loc]

    def get_current_location_amount(self) -> int:
        total = 0
        total += self.get_base_loc_eff_amount(f"Basic Artifact")
        total += self.get_base_loc_eff_amount(f"Basic Boss Artifact")
        for c in CHARACTERS:
            if self.options.shuffle_memories.value:
                total += self.get_base_loc_eff_amount(f"Fix {c}'s Timeline")
            total += self.get_base_loc_eff_amount(f"{c} Artifact")
            total += self.get_base_loc_eff_amount(f"{c} Boss Artifact")
            for r in CARD_RARITIES:
                total += self.get_base_loc_eff_amount(f"{c} {r} Card")
        return total

    def get_current_item_amount(self) -> int:
        total = 0
        for name, data in item_table.items():
            if name not in self.dont_pool_items:
                total += data.progressive_amount
        return total

    def generate_early(self) -> None:
        # Ensure validity of options
        if self.options.shuffle_cards == ShuffleArtifacts.option_off and not self.options.shuffle_artifacts:
            raise OptionError("You must either set shuffle_cards or shuffle_artifacts, or both.")
        if self.options.starting_characters_amount < 3 and not self.options.cro_is_installed.value:
            raise OptionError("If you want to start with less than 3 characters,"
                              "\nyou must install the 'Custom Run options' mod and set cro_is_installed to true.")

        # Save main seed to be used for randomizations client-side
        self.fixed_client_seed = self.random.randint(1, 10000000)

        # Save amounts of each location to modify them
        self.location_name_to_eff_amount = {name: data.amount for name, data in location_table.items()}

        # Select starting items
        starting_characters_amount = self.options.starting_characters_amount.value
        self.starting_characters = list(self.options.starting_characters.value)
        if len(self.starting_characters) < starting_characters_amount:
            self.non_starting_characters = [c for c in CHARACTERS if c not in self.starting_characters]
            self.random.shuffle(self.non_starting_characters)
            self.starting_characters += self.non_starting_characters[:starting_characters_amount - len(self.starting_characters)]
        self.starting_ship = SHIPS[self.options.starting_ship.value]
        self.non_starting_ships = [s for s in SHIPS if s != self.starting_ship]
        if self.options.modifiers_mode == ModifiersMode.option_all_at_start:
            self.starting_modifiers = [m for m in self.item_name_groups["Modifiers"]
                                       if m not in self.options.modifiers_blacklist.value]
        else:
            self.starting_modifiers = []

        # Select starting cards
        if self.options.randomize_starting_cards.value != RandomizeStartingCards.option_off:
            self.starting_cards = []
            for c in CHARACTERS:
                possible_cards = list(self.item_name_groups[f"{c} Cards"])
                # Ensure we have at least one easy-to-use offensive card for each character at the start
                possible_cards_offensive = [card for card in possible_cards if item_table[card].offensive]
                possible_cards_gen = [card for card in possible_cards if item_table[card].generator]
                # CAT is an exception to this (her starting cards are weird)
                if len(possible_cards_offensive) > 0:
                    oc = possible_cards_offensive[self.random.randint(0, len(possible_cards_offensive) - 1)]
                    # For Books/Drake, ensure we have at least one easy-to-use shard/heat generating card
                    eff_possible_cards = possible_cards_gen \
                        if len(possible_cards_gen) > 0 and oc not in possible_cards_gen \
                        else possible_cards
                    if oc in eff_possible_cards:
                        eff_possible_cards.remove(oc)
                    sc = eff_possible_cards[self.random.randint(0, len(eff_possible_cards) - 1)]
                    self.starting_cards += [oc, sc]
        else:
            self.starting_cards = [item for item, data in item_table.items() if data.type == "Card" and data.starter]
        for card in self.starting_cards:
            data = item_table[card]
            self.location_name_to_eff_amount[f"{data.character} {data.rarity} Card"] -= 1

        # Prevent starting items from being registered
        self.dont_pool_items = (["Victory", self.starting_ship] + self.starting_characters + self.starting_cards
                                + list(self.item_name_groups["Filler Items"])
                                + list(self.item_name_groups["Traps"]))
        # These locations actually aren't great in an archipelago setting
        self.dont_register_locations = list(find_locations_base(loc_type="Ship")) + list(find_locations_base(loc_type="Character"))

        # Exclude memories if needed
        if not self.options.additional_character_memories.value:
            self.dont_pool_items += ["Books Memory", "CAT Memory"]
            self.dont_register_locations += ["Fix Books's Timeline", "Fix CAT's Timeline"]
        # If we don't shuffle memories, the items aren't added to the pool but the locations are still created
        # as events with locked event items
        if not self.options.shuffle_memories.value:
            self.dont_pool_items += self.item_name_groups["Memories"]
        # Don't shuffle cards and artifacts if needed
        if not self.options.shuffle_cards.value:
            self.dont_pool_items += self.item_name_groups["Cards"]
            self.dont_register_locations += find_locations_base(loc_type="Card")
        if self.options.shuffle_artifacts.value == ShuffleArtifacts.option_off:
            self.dont_pool_items += self.item_name_groups["Artifacts"]
            self.dont_register_locations += find_locations_base(loc_type="Artifact")
        # Don't shuffle modifiers if needed
        if self.options.modifiers_mode.value in [ModifiersMode.option_off, ModifiersMode.option_all_at_start]:
            self.dont_pool_items += self.item_name_groups["Modifiers"]
        elif self.options.modifiers_mode.value == ModifiersMode.option_immediate:
            self.dont_pool_items += [item for item in self.item_name_groups["Modifiers"] if item_table[item].mod_start]
        # Blacklists
        self.dont_pool_items += list(self.options.modifiers_blacklist.value)

        # Even out items and locations
        appendable_locations = []
        if self.options.shuffle_cards.value:
            appendable_locations += find_locations_base(loc_type="Card")
        if self.options.shuffle_artifacts.value != ShuffleArtifacts.option_off:
            appendable_locations += find_locations_base(loc_type="Artifact")
        while self.get_current_location_amount() < self.get_current_item_amount():
            rand_location = self.random.choice(appendable_locations)
            if 1 < self.location_name_to_eff_amount[rand_location] < max_fill_location:
                self.location_name_to_eff_amount[rand_location] += 1
        self.additional_fillers = max(self.get_current_location_amount() - self.get_current_item_amount(), 0)

    def create_regions(self) -> None:
        # Here Regions are abstract and represent characters
        self.multiworld.regions += [
            self.create_region('Menu', None, ['Starting Bonus']),
            self.create_region('General',
                               find_locations_base(loc_type="Memory")
                               .union(find_locations_base(loc_type="Future Memory"))
                               .difference(self.dont_register_locations),
                               [f"Find {c}" for c in CHARACTERS] + [f"Find {r} Items" for r in ALL_RARITIES])
        ]
        self.multiworld.regions += [
            self.create_region(f"{r} Items",
                               find_locations_base(loc_character="", loc_rarity=r).difference(self.dont_register_locations),
                               [])
            for r in ALL_RARITIES
        ]
        self.multiworld.regions += [
            self.create_region(f"{c} Items",
                               exits=[f"Find {c} {r} Items" for r in ALL_RARITIES])
            for c in CHARACTERS
        ]
        self.multiworld.regions += [
            self.create_region(f"{c} {r} Items",
                               find_locations_base(loc_character=c, loc_rarity=r).difference(self.dont_register_locations),
                               [])
            for c in CHARACTERS
            for r in ALL_RARITIES
        ]

        # Link up regions
        self.multiworld.get_entrance('Starting Bonus', self.player).connect(
            self.multiworld.get_region('General', self.player))
        for r in ALL_RARITIES:
            self.multiworld.get_entrance(f"Find {r} Items", self.player).connect(
                self.multiworld.get_region(f"{r} Items", self.player))
        for c in CHARACTERS:
            self.multiworld.get_entrance(f"Find {c}", self.player).connect(
                self.multiworld.get_region(f"{c} Items", self.player))
            for r in ALL_RARITIES:
                self.multiworld.get_entrance(f"Find {c} {r} Items", self.player).connect(
                    self.multiworld.get_region(f"{c} {r} Items", self.player))

        if not self.options.shuffle_memories.value:
            for c in CHARACTERS:
                if self.options.additional_character_memories.value or c not in ["Books", "CAT"]:
                    for i in range(3):
                        (self.multiworld.get_location(f"Fix {c}'s Timeline {i + 1}", self.player)
                         .place_locked_item(self.create_item(f"{c} Memory")))

        # Victory Condition
        (self.multiworld.get_location("Complete Future Memory", self.player)
         .place_locked_item(self.create_item(f"Victory")))

    def create_region(self, name: str, locations=None, exits=None) -> Region:
        ret = Region(name, self.player, self.multiworld)
        if locations:
            for location in locations:
                sub_locations = self.create_multi_location(location, parent=ret)
                ret.locations += sub_locations
        if exits:
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))

        return ret

    def create_multi_location(self, name: str, parent=None) -> List["CobaltCoreLocation"]:
        res = []
        location_data = location_table[name]
        address = location_data.address
        # If memories aren't shuffled, they are events
        if self.options is not None and not self.options.shuffle_memories.value and location_data.type == "Memory":
            address = None
        for i in range(self.location_name_to_eff_amount[name]):
            # Here we check the actual base amount of cards to make it consistent with location_name_to_id
            loc_name = name if location_data.amount == 1 else f"{name} {i + 1}"
            res.append(CobaltCoreLocation(self.player, loc_name, address, parent))
            if address is not None:
                address += 1
        return res

    def create_items(self) -> None:
        # Starting items
        for c in self.starting_characters + self.starting_cards + [self.starting_ship] + self.starting_modifiers:
            self.multiworld.push_precollected(self.create_item(c))

        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            if name in self.dont_pool_items:
                continue
            for i in range(data.progressive_amount):
                item = self.create_item(name)
                pool.append(item)
        for i in range(self.additional_fillers):
            item = self.create_filler()
            pool.append(item)
        self.multiworld.itempool += pool

    def create_item(self, name: str) -> "CobaltCoreItem":
        return CobaltCoreItem(name, self.player, self.options)

    def get_filler_item_name(self) -> str:
        fillers = list(self.item_name_groups["Filler Items"])
        if self.options.fillers_can_be_traps.value:
            fillers += list(self.item_name_groups["Traps"])
        return self.random.choice(tuple(fillers))

    def set_rules(self) -> None:
        def character_clears_soft_logic(state: CollectionState, character: str,
                                             count_all_amount: int, count_rare_amount: int):
            if not state.has(character, self.player):
                return False
            # Soft difficulty logic
            has_cards = True
            has_artifacts = True
            if self.options.difficulty_logic == DifficultyLogic.option_count_all:
                has_cards = state.has_group(f"{character} Cards", self.player, count_all_amount)  # Character Cards
                basic_artifacts = state.count_group(f"Basic Artifacts", self.player)
                char_artifacts = state.count_group(f"{character} Artifacts", self.player)
                has_artifacts = basic_artifacts + char_artifacts >= count_all_amount  # All Artifacts
            elif self.options.difficulty_logic == DifficultyLogic.option_count_rare:
                has_cards = state.has_group(f"{character} Rare Cards", self.player, count_rare_amount)  # Character Rare Cards
                basic_artifacts = state.count_group(f"Basic Boss Artifacts", self.player)
                char_artifacts = state.count_group(f"{character} Boss Artifacts", self.player)
                has_artifacts = basic_artifacts + char_artifacts >= count_all_amount  # All Boss Artifacts
            if not self.options.shuffle_cards.value:
                has_cards = True
            if self.options.shuffle_artifacts.value == ShuffleArtifacts.option_off:
                has_artifacts = True
            return has_cards and has_artifacts
        
        def character_can_find_uncommon(state: CollectionState, character: str):
            return character_clears_soft_logic(state, character, 3, 1)
        
        def character_can_find_rare(state: CollectionState, character: str):
            return character_clears_soft_logic(state, character, 5, 2)
        
        def character_can_find_boss(state: CollectionState, character: str):
            return character_clears_soft_logic(state, character, 8, 3)
        
        def character_can_complete_run(state: CollectionState, character: str):
            return character_clears_soft_logic(state, character, 10, 4)

        def player_clears_soft_logic(state: CollectionState, character_logic_function,
                                     set_characters=None, forbidden_characters=None, any_char=False) -> bool:
            if set_characters is None:
                set_characters = []
            if forbidden_characters is None:
                forbidden_characters = []
            # If the characters given can't complete, then the player can't complete
            aggregate_func = any if any_char else all
            if (len(set_characters) > 0
                    and not aggregate_func(map(lambda c: character_logic_function(state, c), set_characters))):
                return False
            # Otherwise we count if we can reach enough completable characters using the other found characters
            unset_found_characters = [c for c in CHARACTERS if state.has(c, self.player)
                                      and c not in set_characters + forbidden_characters]
            found_win_count = sum(map(lambda c: character_logic_function(state, c), unset_found_characters))
            return found_win_count + len(set_characters) >= (1 if any_char else 3)

        def player_can_find_uncommon(state: CollectionState, set_characters=None, forbidden_characters=None) -> bool:
            return player_clears_soft_logic(state, character_can_find_uncommon, set_characters, forbidden_characters,
                                            any_char=True)

        def player_can_find_rare(state: CollectionState, set_characters=None, forbidden_characters=None) -> bool:
            return player_clears_soft_logic(state, character_can_find_rare, set_characters, forbidden_characters,
                                            any_char=True)

        def player_can_find_boss(state: CollectionState, set_characters=None, forbidden_characters=None) -> bool:
            return player_clears_soft_logic(state, character_can_find_boss, set_characters, forbidden_characters)

        def player_can_complete_run(state: CollectionState, set_characters=None, forbidden_characters=None) -> bool:
            return player_clears_soft_logic(state, character_can_complete_run, set_characters, forbidden_characters)

        def player_can_find_rarity(state: CollectionState, rarity: str,
                                   set_characters=None, forbidden_characters=None) -> bool:
            if rarity == "Uncommon":
                return player_can_find_uncommon(state, set_characters, forbidden_characters)
            elif rarity == "Rare":
                return player_can_find_rare(state, set_characters, forbidden_characters)
            elif rarity == "Boss":
                return player_can_find_boss(state, set_characters, forbidden_characters)
            return True

        for r in ALL_RARITIES:
            set_rule(self.multiworld.get_entrance(f"Find {r} Items", self.player),
                     lambda state, r=r: player_can_find_rarity(state, r))
        for c in CHARACTERS:
            set_rule(self.multiworld.get_entrance(f"Find {c}", self.player),
                     lambda state, c=c: state.has(c, self.player))
            for r in ALL_RARITIES:
                set_rule(self.multiworld.get_entrance(f"Find {c} {r} Items", self.player),
                         lambda state, c=c, r=r: state.has(c, self.player) and player_can_find_rarity(state, r))
            if self.options.additional_character_memories.value or c not in ["Books", "CAT"]:
                for i in range(3):
                    set_rule(self.multiworld.get_location(f"Fix {c}'s Timeline {i + 1}", self.player),
                             lambda state, c=c: player_can_complete_run(state, [c]))

        def can_complete_goal(state: CollectionState) -> bool:
            if self.options.win_condition == WinCondition.option_total_memories:
                return state.has_group("Memories", self.player, self.options.memories_required_total.value)
            else:  # option_per_character_memories
                for c in CHARACTERS:
                    if self.options.additional_character_memories.value or c not in ["Books", "CAT"]:
                        if not state.has(f"{c} Memory", self.player,
                                         count=self.options.memories_required_per_character.value):
                            return False
                return True

        set_rule(self.multiworld.get_location("Complete Future Memory", self.player), can_complete_goal)
        if self.options.do_future_memory.value:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        else:
            self.multiworld.completion_condition[self.player] = can_complete_goal

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "version_tag": "1.2.0",
            "starting_characters": self.starting_characters,
            "cro_is_installed": self.options.cro_is_installed.value,
            "starting_ship": self.starting_ship,
            "shuffle_ship_parts": self.options.shuffle_ship_parts.value,
            "randomize_starting_cards": self.options.randomize_starting_cards.value,
            "starting_cards": self.starting_cards,
            "win_condition": self.options.win_condition.value,
            "memories_required_total": self.options.memories_required_total.value,
            "memories_required_per_character": self.options.memories_required_per_character.value,
            "add_character_memories": self.options.additional_character_memories.value,
            "shuffle_memories": self.options.shuffle_memories.value,
            "unlock_memory_for_all_characters": self.options.unlock_memory_for_all_characters.value,
            "do_future_memory": self.options.do_future_memory.value,
            "shuffle_cards": self.options.shuffle_cards.value,
            "shuffle_artifacts": self.options.shuffle_artifacts.value,
            "modifiers_mode": self.options.modifiers_mode.value,
            "modifiers_blacklist": self.options.modifiers_blacklist.value,
            "check_card_difficulty": self.options.check_card_difficulty.value,
            "rewards_tweak": self.options.rewards_tweak.value,
            "auto_release_characters": self.options.auto_release_characters.value,
            "swap_character_node": self.options.swap_character_node.value,
            "pick_missed_items_from_every_run": self.options.pick_missed_items_from_every_run.value,
            "immediate_card_rewards": self.options.immediate_card_rewards.value,
            "immediate_card_attributes": self.options.immediate_card_attributes.value,
            "immediate_artifact_rewards": self.options.immediate_artifact_rewards.value,
            "immediate_rewards_blacklist": self.options.immediate_rewards_blacklist.value,
            "fixed_client_seed": self.fixed_client_seed
        }


class CobaltCoreLocation(Location):
    game = "Cobalt Core"

    def __init__(self, player: int, name: str, address, parent=None):
        super(CobaltCoreLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True


class CobaltCoreItem(Item):
    game = "Cobalt Core"

    def __init__(self, name, player: int = None, options: CobaltCoreOptions = None):
        item_data = item_table[name]
        code = item_data.code
        # If memories aren't shuffled, they are events
        if options is not None and not options.shuffle_memories.value and item_data.type == "Memory":
            code = None
        # Adapt classification depending on what is actually being counted for progression
        progression = item_data.progression
        if options.difficulty_logic == DifficultyLogic.option_dont_count \
                and (item_data.type == "Card" or item_data.type == "Artifact"):
            progression = False
        if options.difficulty_logic == DifficultyLogic.option_count_rare \
                and ((item_data.type == "Card" and item_data.rarity != "Rare")
                     or (item_data.type == "Artifact" and item_data.rarity != "Boss")):
            progression = False
        classification = ItemClassification.progression if progression else ItemClassification.useful
        if item_data.type == "Filler":
            classification = ItemClassification.filler
        elif item_data.type == "Trap":
            classification = ItemClassification.trap
        super(CobaltCoreItem, self).__init__(
            name,
            classification,
            code,
            player
        )
