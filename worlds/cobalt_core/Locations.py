import typing

from typing import Dict, Set
from .Constants import *


class LocationData(typing.NamedTuple):
    address: typing.Optional[int]
    type: str
    character: str = ""
    rarity: str = ""
    amount: int = 1


def find_locations_base(loc_type=None, loc_rarity=None, loc_character=None) -> Set[str]:
    return set([name for name, data in location_table.items()
                if (loc_type is None or data.type == loc_type)
                and (loc_rarity is None or data.rarity == loc_rarity)
                and (loc_character is None or data.character == loc_character)])


def find_locations_max(loc_type=None, loc_rarity=None, loc_character=None) -> Set[str]:
    multi_location_set = find_locations_base(loc_type, loc_rarity, loc_character)
    res_set = []
    for loc in multi_location_set:
        data = location_table[loc]
        for i in range(data.amount):
            res_set.append(loc if data.amount == 1 else f"{loc} {i + 1}")
    return set(res_set)


location_table: Dict[str, LocationData] = {
    # Ship unlocks
    "[ARTEMIS FILLER]":                LocationData(ship_off, "Ship"),
    "Win on Hard Difficulty":          LocationData(ship_off + 1, "Ship"),
    "Discover 40 Artifacts":           LocationData(ship_off + 2, "Ship"),
    "Win without starting characters": LocationData(ship_off + 3, "Ship"),
    "Win 10 Games":                    LocationData(ship_off + 4, "Ship"),

    # Character unlocks
    "[DIZZY FILLER]":                 LocationData(character_off,     "Character"),
    "[RIGGS FILLER]":                 LocationData(character_off + 1, "Character"),
    "[PERI FILLER]":                  LocationData(character_off + 2, "Character"),
    "Win on Normal":                  LocationData(character_off + 3, "Character"),
    "Win with Isaac":                 LocationData(character_off + 4, "Character"),
    "Win with Drake":                 LocationData(character_off + 5, "Character"),
    "Complete Lazuli Nebula 5 Times": LocationData(character_off + 6, "Character"),
    "[CAT FILLER]":                   LocationData(character_off + 7, "Character"),

    # Memory Unlocks
    "Fix Dizzy's Timeline": LocationData(memory_off,      "Memory", character="Dizzy", amount=3),
    "Fix Riggs's Timeline": LocationData(memory_off + 10, "Memory", character="Riggs", amount=3),
    "Fix Peri's Timeline":  LocationData(memory_off + 20, "Memory", character="Peri",  amount=3),
    "Fix Isaac's Timeline": LocationData(memory_off + 30, "Memory", character="Isaac", amount=3),
    "Fix Drake's Timeline": LocationData(memory_off + 40, "Memory", character="Drake", amount=3),
    "Fix Max's Timeline":   LocationData(memory_off + 50, "Memory", character="Max",   amount=3),
    "Fix Books's Timeline": LocationData(memory_off + 60, "Memory", character="Books", amount=3),
    "Fix CAT's Timeline":   LocationData(memory_off + 70, "Memory", character="CAT",   amount=3),

    "Complete Future Memory": LocationData(None, "Future Memory"),

    # Cards
    "Dizzy Common Card":   LocationData(card_off + dizzy_off + C,  "Card", character="Dizzy", rarity="Common",   amount=9),
    "Dizzy Uncommon Card": LocationData(card_off + dizzy_off + UC, "Card", character="Dizzy", rarity="Uncommon", amount=7),
    "Dizzy Rare Card":     LocationData(card_off + dizzy_off + R,  "Card", character="Dizzy", rarity="Rare",     amount=5),

    "Riggs Common Card":   LocationData(card_off + riggs_off + C,  "Card", character="Riggs", rarity="Common",   amount=9),
    "Riggs Uncommon Card": LocationData(card_off + riggs_off + UC, "Card", character="Riggs", rarity="Uncommon", amount=7),
    "Riggs Rare Card":     LocationData(card_off + riggs_off + R,  "Card", character="Riggs", rarity="Rare",     amount=5),

    "Peri Common Card":   LocationData(card_off + peri_off + C,  "Card", character="Peri", rarity="Common",   amount=9),
    "Peri Uncommon Card": LocationData(card_off + peri_off + UC, "Card", character="Peri", rarity="Uncommon", amount=7),
    "Peri Rare Card":     LocationData(card_off + peri_off + R,  "Card", character="Peri", rarity="Rare",     amount=5),

    "Isaac Common Card":   LocationData(card_off + isaac_off + C,  "Card", character="Isaac", rarity="Common",   amount=9),
    "Isaac Uncommon Card": LocationData(card_off + isaac_off + UC, "Card", character="Isaac", rarity="Uncommon", amount=7),
    "Isaac Rare Card":     LocationData(card_off + isaac_off + R,  "Card", character="Isaac", rarity="Rare",     amount=5),

    "Drake Common Card":   LocationData(card_off + drake_off + C,  "Card", character="Drake", rarity="Common",   amount=9),
    "Drake Uncommon Card": LocationData(card_off + drake_off + UC, "Card", character="Drake", rarity="Uncommon", amount=7),
    "Drake Rare Card":     LocationData(card_off + drake_off + R,  "Card", character="Drake", rarity="Rare",     amount=5),

    "Max Common Card":   LocationData(card_off + max_off + C,  "Card", character="Max", rarity="Common",   amount=9),
    "Max Uncommon Card": LocationData(card_off + max_off + UC, "Card", character="Max", rarity="Uncommon", amount=7),
    "Max Rare Card":     LocationData(card_off + max_off + R,  "Card", character="Max", rarity="Rare",     amount=5),

    "Books Common Card":   LocationData(card_off + books_off + C,  "Card", character="Books", rarity="Common",   amount=9),
    "Books Uncommon Card": LocationData(card_off + books_off + UC, "Card", character="Books", rarity="Uncommon", amount=7),
    "Books Rare Card":     LocationData(card_off + books_off + R,  "Card", character="Books", rarity="Rare",     amount=5),

    "CAT Common Card":   LocationData(card_off + cat_off + C,  "Card", character="CAT", rarity="Common",   amount=7),
    "CAT Uncommon Card": LocationData(card_off + cat_off + UC, "Card", character="CAT", rarity="Uncommon", amount=7),
    "CAT Rare Card":     LocationData(card_off + cat_off + R,  "Card", character="CAT", rarity="Rare",     amount=4),

    # Artifacts
    "Basic Artifact":      LocationData(artifact_off + C, "Artifact", rarity="Common", amount=25),
    "Basic Boss Artifact": LocationData(artifact_off + R, "Artifact", rarity="Boss",   amount=11),

    "Dizzy Artifact":      LocationData(artifact_off + dizzy_off + C, "Artifact", character="Dizzy", rarity="Common", amount=4),
    "Dizzy Boss Artifact": LocationData(artifact_off + dizzy_off + R, "Artifact", character="Dizzy", rarity="Boss",   amount=2),

    "Riggs Artifact":      LocationData(artifact_off + riggs_off + C, "Artifact", character="Riggs", rarity="Common", amount=3),
    "Riggs Boss Artifact": LocationData(artifact_off + riggs_off + R, "Artifact", character="Riggs", rarity="Boss",   amount=2),

    "Peri Artifact":      LocationData(artifact_off + peri_off + C, "Artifact", character="Peri", rarity="Common", amount=3),
    "Peri Boss Artifact": LocationData(artifact_off + peri_off + R, "Artifact", character="Peri", rarity="Boss",   amount=2),

    "Isaac Artifact":      LocationData(artifact_off + isaac_off + C, "Artifact", character="Isaac", rarity="Common", amount=4),
    "Isaac Boss Artifact": LocationData(artifact_off + isaac_off + R, "Artifact", character="Isaac", rarity="Boss",   amount=2),

    "Drake Artifact":      LocationData(artifact_off + drake_off + C, "Artifact", character="Drake", rarity="Common", amount=5),
    "Drake Boss Artifact": LocationData(artifact_off + drake_off + R, "Artifact", character="Drake", rarity="Boss",   amount=1),

    "Max Artifact":      LocationData(artifact_off + max_off + C, "Artifact", character="Max", rarity="Common", amount=4),
    "Max Boss Artifact": LocationData(artifact_off + max_off + R, "Artifact", character="Max", rarity="Boss",   amount=3),

    "Books Artifact":      LocationData(artifact_off + books_off + C, "Artifact", character="Books", rarity="Common", amount=5),
    "Books Boss Artifact": LocationData(artifact_off + books_off + R, "Artifact", character="Books", rarity="Boss",   amount=1),

    "CAT Artifact":      LocationData(artifact_off + cat_off + C, "Artifact", character="CAT", rarity="Common", amount=3),
    "CAT Boss Artifact": LocationData(artifact_off + cat_off + R, "Artifact", character="CAT", rarity="Boss",   amount=1),
}
