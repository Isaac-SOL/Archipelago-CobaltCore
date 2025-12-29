import itertools
from typing import ClassVar, Dict, Set, List, Mapping, Any
from BaseClasses import Tutorial, Item, ItemClassification, Location, MultiWorld, Region, Entrance, CollectionState
from .Items import item_table, find_items
from ..AutoWorld import WebWorld, World
from .Options import CobaltCoreOptions, WinCondition, TotalMemoriesRequired
from .Locations import location_table, find_locations_max, find_locations_base
from ..generic.Rules import set_rule

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
        self.starting_cards = [item for item, data in item_table.items() if data.type == "Card" and data.starter]
        for card in self.starting_cards:
            data = item_table[card]
            self.location_name_to_eff_amount[f"{data.character} {data.rarity} Card"] -= 1

        # Prevent starting items from being registered
        self.dont_register_items = ["Victory", self.starting_ship] + self.starting_characters + self.starting_cards
        # self.dont_register_locations = ["[ARTEMIS FILLER]"] + list(self.location_name_groups["Character Unlocks"])[:len(self.starting_characters)]
        self.dont_register_locations = []
        if not self.options.shuffle_memories.value:
            self.dont_register_items += self.item_name_groups["Memories"]

    def create_regions(self) -> None:
        # Here Regions are abstract and represent characters
        self.multiworld.regions += [
            self.create_region('Menu', None, ['Starting Bonus']),
            self.create_region('General', find_locations_base(loc_character="")
                               .difference(self.dont_register_locations), [f"Find {c}" for c in CHARACTERS])
        ]
        self.multiworld.regions += [
            self.create_region(f"{c} Items", find_locations_base(loc_character=c)
                               .difference(self.dont_register_locations), [])
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
        for c in self.starting_characters:
            self.multiworld.push_precollected(self.create_item(c))
        self.multiworld.push_precollected(self.create_item(self.starting_ship))

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
            has_cards = state.has_group(f"{character} Cards", self.player, 10)  # Character Cards
            has_artifacts = state.has_group(f"Artifacts", self.player, 10)  # All Artifacts
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
            for i in range(3):
                set_rule(self.multiworld.get_location(f"Fix {c}'s Timeline {i + 1}", self.player),
                         lambda state, c=c: player_can_complete_run(state, [c]))

        def can_complete_goal(state: CollectionState) -> bool:
            if self.options.win_condition == WinCondition.option_total_memories:
                return state.has_group("Memories", self.player, self.options.memories_required_total.value)
            else:  # option_per_character_memories
                for c in CHARACTERS:
                    if not state.has(f"{c} Memory", self.player,
                                     count=self.options.memories_required_per_character.value):
                        return False
                return True

        set_rule(self.multiworld.get_location("Discover 40 Artifacts", self.player),
                 lambda state: state.has_group("Artifacts", self.player, 40))
        set_rule(self.multiworld.get_location("Win on Hard Difficulty", self.player),
                 lambda state: player_can_complete_run(state))
        set_rule(self.multiworld.get_location("Win on Normal Difficulty", self.player),
                 lambda state: player_can_complete_run(state))
        set_rule(self.multiworld.get_location("Win 10 Games", self.player),
                 lambda state: player_can_complete_run(state))
        set_rule(self.multiworld.get_location("Win without starting characters", self.player),
                 lambda state: player_can_complete_run(state, [], self.starting_characters))
        set_rule(self.multiworld.get_location("Win with Isaac", self.player),
                 lambda state: player_can_complete_run(state, ["Isaac"]))
        set_rule(self.multiworld.get_location("Win with Drake", self.player),
                 lambda state: player_can_complete_run(state, ["Drake"]))

        set_rule(self.multiworld.get_location("Complete Future Memory", self.player), can_complete_goal)
        if self.options.do_future_memory.value:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        else:
            self.multiworld.completion_condition[self.player] = can_complete_goal

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "starting_characters": self.starting_characters
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
