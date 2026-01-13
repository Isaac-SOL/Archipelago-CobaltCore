import itertools
import random
from typing import ClassVar, Dict, Set, List, Mapping, Any
from BaseClasses import Tutorial, Item, ItemClassification, Location, MultiWorld, Region, Entrance, CollectionState
from .Items import item_table, find_items
from ..AutoWorld import WebWorld, World
from .Options import CobaltCoreOptions, WinCondition, TotalMemoriesRequired, DifficultyLogic
from .Locations import location_table, find_locations_max, find_locations_base
from ..generic.Rules import set_rule
from .Constants import *

CHARACTERS = ["Dizzy", "Riggs", "Peri", "Isaac", "Drake", "Max", "Books", "CAT"]
CARD_RARITIES = ["Common", "Uncommon", "Rare"]
ARTIFACT_RARITIES = ["Common", "Boss"]
SHIPS = ["Artemis", "Ares", "Jupiter", "Gemini", "Tiderunner"]


class CobaltCoreWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Cobalt Core for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "cobalt-core_en.md",
        "cobalt-core/en",
        ["SaltyIsaac"]
    )]


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
            for i in range(data.amount):
                location_name_to_id[f"{name} {i + 1}"] = data.address + i

    # These fields must not be initialized here as they will be modified at runtime
    location_name_to_eff_amount: dict[str, int]

    starting_characters: list[str]
    non_starting_characters: list[str]
    starting_ship: str
    non_starting_ships: list[str]
    starting_cards: list[str]

    dont_register_items: list[str]
    dont_register_locations: list[str]

    fixed_client_seed: int

    # Fill item groups
    item_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Ships": find_items(item_type="Ship"),
        "Characters": find_items(item_type="Character"),
        "Memories": find_items(item_type="Memory"),
        "Cards": find_items(item_type="Card"),
        "Artifacts": find_items(item_type="Artifact")
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
        "Artifacts": find_locations_max(loc_type="Artifact")
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

    def generate_early(self) -> None:
        # Ensure validity of options
        if not self.options.shuffle_cards and not self.options.shuffle_artifacts:
            raise Exception("You must either set shuffle_cards or shuffle_artifacts to true.")

        # Save main seed to be used for randomizations client-side
        self.fixed_client_seed = random.randint(1, 10000000)

        # Save amounts of each location to modify them
        self.location_name_to_eff_amount = {name: data.amount for name, data in location_table.items()}

        # Select starting ship and characters
        self.starting_characters = list(self.options.starting_characters.value)
        if len(self.starting_characters) < 3:
            self.non_starting_characters = [c for c in CHARACTERS if c not in self.starting_characters]
            self.random.shuffle(self.non_starting_characters)
            self.starting_characters += self.non_starting_characters[:3 - len(self.starting_characters)]
        self.starting_ship = SHIPS[self.options.starting_ship.value]
        self.non_starting_ships = [s for s in SHIPS if s != self.starting_ship]

        # Select starting cards
        if self.options.randomize_starting_cards.value:
            self.starting_cards = []
            for c in CHARACTERS:
                possible_cards = list(self.item_name_groups[f"{c} Cards"])
                # Ensure we have at least one easy-to-use offensive card for each character at the start
                possible_cards_offensive = [c for c in possible_cards if item_table[c].offensive_start]
                # CAT is an exception to this (her starting cards are weird)
                if len(possible_cards_offensive) > 0:
                    oc = possible_cards_offensive[self.random.randint(0, len(possible_cards_offensive) - 1)]
                    possible_cards.remove(oc)
                    sc = possible_cards[self.random.randint(0, len(possible_cards) - 1)]
                    self.starting_cards += [oc, sc]
        else:
            self.starting_cards = [item for item, data in item_table.items() if data.type == "Card" and data.starter]
        for card in self.starting_cards:
            data = item_table[card]
            self.location_name_to_eff_amount[f"{data.character} {data.rarity} Card"] -= 1

        # Prevent starting items from being registered
        self.dont_register_items = ["Victory", self.starting_ship] + self.starting_characters + self.starting_cards
        # These locations actually aren't great in an archipelago setting
        self.dont_register_locations = list(find_locations_base(loc_type="Ship")) + list(find_locations_base(loc_type="Character"))
        # We replace them with additional cards or artifacts
        appendable_locations = []
        if self.options.shuffle_cards.value:
            appendable_locations += find_locations_base(loc_type="Card")
        if self.options.shuffle_artifacts.value:
            appendable_locations += find_locations_base(loc_type="Artifact")
        additional_items = 0
        while additional_items < len(self.dont_register_locations):
            rand_location = random.choice(appendable_locations)
            if 1 < self.location_name_to_eff_amount[rand_location] < max_fill_location:
                self.location_name_to_eff_amount[rand_location] += 1
                additional_items += 1

        if not self.options.additional_character_memories.value:
            self.dont_register_items += ["Books Memory", "CAT Memory"]
            self.dont_register_locations += ["Fix Books's Timeline", "Fix CAT's Timeline"]
        if not self.options.shuffle_memories.value:
            self.dont_register_items += self.item_name_groups["Memories"]
        if not self.options.shuffle_cards.value:
            self.dont_register_items += self.item_name_groups["Cards"]
            self.dont_register_locations += find_locations_base(loc_type="Card")
        if not self.options.shuffle_artifacts.value:
            self.dont_register_items += self.item_name_groups["Artifacts"]
            self.dont_register_locations += find_locations_base(loc_type="Artifact")

    def create_regions(self) -> None:
        # Here Regions are abstract and represent characters
        self.multiworld.regions += [
            self.create_region('Menu', None, ['Starting Bonus']),
            self.create_region('General',
                               find_locations_base(loc_character="").difference(self.dont_register_locations),
                               [f"Find {c}" for c in CHARACTERS])
        ]
        self.multiworld.regions += [
            self.create_region(f"{c} Items",
                               find_locations_base(loc_character=c).difference(self.dont_register_locations),
                               [])
            for c in CHARACTERS
        ]

        # Link up regions
        self.multiworld.get_entrance('Starting Bonus', self.player).connect(
            self.multiworld.get_region('General', self.player))
        for c in CHARACTERS:
            self.multiworld.get_entrance(f"Find {c}", self.player).connect(
                self.multiworld.get_region(f"{c} Items", self.player))

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
        for c in self.starting_characters + self.starting_cards + [self.starting_ship]:
            self.multiworld.push_precollected(self.create_item(c))

        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            if name in self.dont_register_items:
                continue
            item = self.create_item(name)
            pool.append(item)
        self.multiworld.itempool += pool

    def create_item(self, name: str) -> "CobaltCoreItem":
        return CobaltCoreItem(name, self.player, self.options)

    def set_rules(self) -> None:
        def character_can_complete_run(state: CollectionState, character: str):
            if not state.has(character, self.player):
                return False
            # Soft difficulty logic
            has_cards = True
            has_artifacts = True
            if self.options.difficulty_logic == DifficultyLogic.option_count_all:
                has_cards = state.has_group(f"{character} Cards", self.player, 10)  # Character Cards
                has_artifacts = state.has_group(f"Artifacts", self.player, 10)  # All Artifacts
            elif self.options.difficulty_logic == DifficultyLogic.option_count_rare:
                has_cards = state.has_group(f"{character} Rare Cards", self.player, 2)  # Character Rare Cards
                has_artifacts = state.has_group(f"Boss Artifacts", self.player, 3)  # All Boss Artifacts
            if not self.options.shuffle_cards.value:
                has_cards = True
            if not self.options.shuffle_artifacts.value:
                has_artifacts = True
            return has_cards and has_artifacts

        def player_can_complete_run(state: CollectionState, set_characters=None, forbidden_characters=None) -> bool:
            if set_characters is None:
                set_characters = []
            if forbidden_characters is None:
                forbidden_characters = []
            # If the characters given can't complete, then the player can't complete
            if not all(map(lambda c: character_can_complete_run(state, c), set_characters)):
                return False
            # Otherwise we count if we can reach 3 completable characters using the other found characters
            unset_found_characters = [c for c in CHARACTERS if state.has(c, self.player)
                                      and c not in set_characters + forbidden_characters]
            found_win_count = sum(map(lambda c: character_can_complete_run(state, c), unset_found_characters))
            return found_win_count + len(set_characters) >= 3

        for c in CHARACTERS:
            set_rule(self.multiworld.get_entrance(f"Find {c}", self.player),
                     lambda state, c=c: state.has(c, self.player))
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

        # set_rule(self.multiworld.get_location("Discover 40 Artifacts", self.player),
        #          lambda state: state.has_group("Artifacts", self.player, 40))
        # set_rule(self.multiworld.get_location("Win on Hard Difficulty", self.player),
        #          lambda state: player_can_complete_run(state))
        # set_rule(self.multiworld.get_location("Win on Normal Difficulty", self.player),
        #          lambda state: player_can_complete_run(state))
        # set_rule(self.multiworld.get_location("Win 10 Games", self.player),
        #          lambda state: player_can_complete_run(state) and state.has_group("Characters", self.player, 5))
        # set_rule(self.multiworld.get_location("Win without starting characters", self.player),
        #          lambda state: player_can_complete_run(state, [], self.starting_characters))
        # set_rule(self.multiworld.get_location("Win with Isaac", self.player),
        #          lambda state: player_can_complete_run(state, ["Isaac"]))
        # set_rule(self.multiworld.get_location("Win with Drake", self.player),
        #          lambda state: player_can_complete_run(state, ["Drake"]))

        set_rule(self.multiworld.get_location("Complete Future Memory", self.player), can_complete_goal)
        if self.options.do_future_memory.value:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        else:
            self.multiworld.completion_condition[self.player] = can_complete_goal

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "starting_characters": self.starting_characters,
            "starting_ship": self.starting_ship,
            "shuffle_ship_parts": self.options.shuffle_ship_parts.value,
            "starting_cards": self.starting_cards,
            "minimum_difficulty": self.options.minimum_difficulty.value,
            "win_condition": self.options.win_condition.value,
            "memories_required_total": self.options.memories_required_total.value,
            "memories_required_per_character": self.options.memories_required_per_character.value,
            "add_character_memories": self.options.additional_character_memories.value,
            "shuffle_memories": self.options.shuffle_memories.value,
            "do_future_memory": self.options.do_future_memory.value,
            "shuffle_cards": self.options.shuffle_cards.value,
            "shuffle_artifacts": self.options.shuffle_artifacts.value,
            "check_card_difficulty": self.options.check_card_difficulty.value,
            "rarer_checks_later": self.options.rarer_checks_later.value,
            "get_more_found_items": self.options.get_more_found_items.value,
            "immediate_card_rewards": self.options.immediate_card_rewards.value,
            "immediate_card_attributes": self.options.immediate_card_attributes.value,
            "immediate_artifact_rewards": self.options.immediate_artifact_rewards.value,
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
        super(CobaltCoreItem, self).__init__(
            name,
            ItemClassification.progression if item_data.progression else ItemClassification.filler,
            code,
            player
        )
