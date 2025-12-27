from typing import ClassVar, Dict, Set
from BaseClasses import Tutorial, Item, ItemClassification, Location
from .Items import item_table, find_items
from .Regions import create_regions
from ..AutoWorld import WebWorld, World
from .Options import CobaltCoreOptions
from .Locations import location_table, find_locations

CHARACTERS = ["Dizzy", "Riggs", "Peri", "Isaac", "Drake", "Max", "Cat"]
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
    location_name_to_id = {name: data.address for name, data in location_table.items()}

    starting_characters: list[str]
    non_starting_characters: list[str]
    starting_ship: str
    non_starting_ships: list[str]

    # Fill item groups
    item_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Ships": find_items(item_type="Ship"),
        "Characters": find_items(item_type="Character"),
        "Memories": find_items(item_type="Memory")
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
        "Ship Unlocks": find_locations(loc_type="Ship"),
        "Character Unlocks": find_locations(loc_type="Character"),
        "Memory Unlocks": find_locations(loc_type="Memory")
    }
    for r in CARD_RARITIES:
        item_name_groups[f"{r} Cards"] = find_locations(loc_type="Card", loc_rarity=r)
    for r in ARTIFACT_RARITIES:
        item_name_groups[f"{r} Artifacts"] = find_locations(loc_type="Artifact", loc_rarity=r)
    for c in CHARACTERS:
        item_name_groups[f"{c} Cards"] = find_locations(loc_type="Card", loc_character=c)
        item_name_groups[f"{c} Artifacts"] = find_locations(loc_type="Artifact", loc_character=c)
        for r in CARD_RARITIES:
            item_name_groups[f"{c} {r} Cards"] = find_locations(loc_type="Card", loc_character=c, loc_rarity=r)
        for r in ARTIFACT_RARITIES:
            item_name_groups[f"{c} {r} Artifacts"] = find_locations(loc_type="Artifact", loc_character=c, loc_rarity=r)

    def generate_early(self) -> None:
        self.starting_characters = list(self.options.starting_characters.value)
        if len(self.starting_characters) < 3:
            self.non_starting_characters = [c for c in CHARACTERS if c not in self.starting_characters]
            self.random.shuffle(self.non_starting_characters)
            self.starting_characters += self.non_starting_characters[:3 - len(self.starting_characters)]
        self.starting_ship = SHIPS[self.options.starting_ship.value]
        self.non_starting_ships = [s for s in SHIPS if s != self.starting_ship]

    def create_items(self) -> None:
        # Starting items
        for c in self.starting_characters:
            self.multiworld.push_precollected(CobaltCoreItem(c, self.player))
        self.multiworld.push_precollected(CobaltCoreItem(self.starting_ship, self.player))

        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            if name == self.starting_ship or name in self.starting_characters:
                continue
            item = CobaltCoreItem(name, self.player)
            pool.append(item)
        self.multiworld.itempool += pool

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)


class CobaltCoreLocation(Location):
    game = "Cobalt Core"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(CobaltCoreLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True


class CobaltCoreItem(Item):
    game = "Cobalt Core"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(CobaltCoreItem, self).__init__(
            name,
            ItemClassification.progression if item_data.progression else ItemClassification.filler,
            item_data.code,
            player
        )
