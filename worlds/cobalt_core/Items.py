import typing

from typing import Dict, Set
from .Constants import *


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: str
    progression: bool
    progressive_amount: int = 1
    character: str = ""
    rarity: str = ""
    starter: bool = False


def find_items(item_type=None, item_rarity=None, item_character=None) -> Set[str]:
    return set([name for name, data in item_table.items()
                if (item_type is None or data.type == item_type)
                and (item_rarity is None or data.rarity == item_rarity)
                and (item_character is None or data.character == item_character)])


item_table: Dict[str, ItemData] = {
    # Ships
    "Artemis":    ItemData(ship_off,     "Ship", True),
    "Ares":       ItemData(ship_off + 1, "Ship", True),
    "Jupiter":    ItemData(ship_off + 2, "Ship", True),
    "Gemini":     ItemData(ship_off + 3, "Ship", True),
    "Tiderunner": ItemData(ship_off + 4, "Ship", True),

    # Characters
    "Dizzy": ItemData(character_off,     "Character", True),
    "Riggs": ItemData(character_off + 1, "Character", True),
    "Peri":  ItemData(character_off + 2, "Character", True),
    "Isaac": ItemData(character_off + 3, "Character", True),
    "Drake": ItemData(character_off + 4, "Character", True),
    "Max":   ItemData(character_off + 5, "Character", True),
    "Books": ItemData(character_off + 6, "Character", True),
    "CAT":   ItemData(character_off + 7, "Character", True),

    # Memories
    "Dizzy Memory": ItemData(memory_off,     "Memory", True, progressive_amount=3, character="Dizzy"),
    "Riggs Memory": ItemData(memory_off + 1, "Memory", True, progressive_amount=3, character="Riggs"),
    "Peri Memory":  ItemData(memory_off + 2, "Memory", True, progressive_amount=3, character="Peri"),
    "Isaac Memory": ItemData(memory_off + 3, "Memory", True, progressive_amount=3, character="Isaac"),
    "Drake Memory": ItemData(memory_off + 4, "Memory", True, progressive_amount=3, character="Drake"),
    "Max Memory":   ItemData(memory_off + 5, "Memory", True, progressive_amount=3, character="Max"),
    "Books Memory": ItemData(memory_off + 6, "Memory", True, progressive_amount=3, character="Books"),
    "CAT Memory":   ItemData(memory_off + 7, "Memory", True, progressive_amount=3, character="CAT"),

    "Victory": ItemData(None, "Future Memory", True),

    # CARDS

    # Dizzy
    "Big Shield":       ItemData(card_off + dizzy_off + C,     "Card", True, character="Dizzy", rarity="Common"),
    "Block Shot":       ItemData(card_off + dizzy_off + C + 1, "Card", True, character="Dizzy", rarity="Common", starter=True),
    "Boost Capacitors": ItemData(card_off + dizzy_off + C + 2, "Card", True, character="Dizzy", rarity="Common"),
    "Button Mash":      ItemData(card_off + dizzy_off + C + 3, "Card", True, character="Dizzy", rarity="Common"),
    "Deflection":       ItemData(card_off + dizzy_off + C + 4, "Card", True, character="Dizzy", rarity="Common"),
    "Momentum":         ItemData(card_off + dizzy_off + C + 5, "Card", True, character="Dizzy", rarity="Common"),
    "Shield Surge":     ItemData(card_off + dizzy_off + C + 6, "Card", True, character="Dizzy", rarity="Common", starter=True),
    "Stun Charge":      ItemData(card_off + dizzy_off + C + 7, "Card", True, character="Dizzy", rarity="Common"),
    "Stun Shot":        ItemData(card_off + dizzy_off + C + 8, "Card", True, character="Dizzy", rarity="Common"),

    "Acid Cannon":      ItemData(card_off + dizzy_off + UC,     "Card", True, character="Dizzy", rarity="Uncommon"),
    "Blocker Burnout":  ItemData(card_off + dizzy_off + UC + 1, "Card", True, character="Dizzy", rarity="Uncommon"),
    "Converter":        ItemData(card_off + dizzy_off + UC + 2, "Card", True, character="Dizzy", rarity="Uncommon"),
    "EMP":              ItemData(card_off + dizzy_off + UC + 3, "Card", True, character="Dizzy", rarity="Uncommon"),
    "Multi Stun":       ItemData(card_off + dizzy_off + UC + 4, "Card", True, character="Dizzy", rarity="Uncommon"),
    "Pulse Barrier":    ItemData(card_off + dizzy_off + UC + 5, "Card", True, character="Dizzy", rarity="Uncommon"),
    "Refresh Interval": ItemData(card_off + dizzy_off + UC + 6, "Card", True, character="Dizzy", rarity="Uncommon"),

    "Corrosion Beam": ItemData(card_off + dizzy_off + R,     "Card", True, character="Dizzy", rarity="Rare"),
    "Mitosis":        ItemData(card_off + dizzy_off + R + 1, "Card", True, character="Dizzy", rarity="Rare"),
    "Payback":        ItemData(card_off + dizzy_off + R + 2, "Card", True, character="Dizzy", rarity="Rare"),
    "Shield Gun":     ItemData(card_off + dizzy_off + R + 3, "Card", True, character="Dizzy", rarity="Rare"),
    "Stun Source":    ItemData(card_off + dizzy_off + R + 4, "Card", True, character="Dizzy", rarity="Rare"),

    # Riggs
    "Bolt":           ItemData(card_off + riggs_off + C,     "Card", True, character="Riggs", rarity="Common"),
    "Draw Shot":      ItemData(card_off + riggs_off + C + 1, "Card", True, character="Riggs", rarity="Common", starter=True),
    "Evasive Shot":   ItemData(card_off + riggs_off + C + 2, "Card", True, character="Riggs", rarity="Common"),
    "Juke":           ItemData(card_off + riggs_off + C + 3, "Card", True, character="Riggs", rarity="Common"),
    "Options":        ItemData(card_off + riggs_off + C + 4, "Card", True, character="Riggs", rarity="Common"),
    "Panic":          ItemData(card_off + riggs_off + C + 5, "Card", True, character="Riggs", rarity="Common"),
    "Quick Thinking": ItemData(card_off + riggs_off + C + 6, "Card", True, character="Riggs", rarity="Common"),
    "Scramble":       ItemData(card_off + riggs_off + C + 7, "Card", True, character="Riggs", rarity="Common", starter=True),
    "Whiplash":       ItemData(card_off + riggs_off + C + 8, "Card", True, character="Riggs", rarity="Common"),

    "Charge Beam":      ItemData(card_off + riggs_off + UC,     "Card", True, character="Riggs", rarity="Uncommon"),
    "Echo":             ItemData(card_off + riggs_off + UC + 1, "Card", True, character="Riggs", rarity="Uncommon"),
    "Fleetfoot":        ItemData(card_off + riggs_off + UC + 2, "Card", True, character="Riggs", rarity="Uncommon"),
    "Now Or Never":     ItemData(card_off + riggs_off + UC + 3, "Card", True, character="Riggs", rarity="Uncommon"),
    "Prepare":          ItemData(card_off + riggs_off + UC + 4, "Card", True, character="Riggs", rarity="Uncommon"),
    "Selective Memory": ItemData(card_off + riggs_off + UC + 5, "Card", True, character="Riggs", rarity="Uncommon"),
    "Vamoose":          ItemData(card_off + riggs_off + UC + 6, "Card", True, character="Riggs", rarity="Uncommon"),

    "Ace":             ItemData(card_off + riggs_off + R,     "Card", True, character="Riggs", rarity="Rare"),
    "Hand Cannon":     ItemData(card_off + riggs_off + R + 1, "Card", True, character="Riggs", rarity="Rare"),
    "Second Opinions": ItemData(card_off + riggs_off + R + 2, "Card", True, character="Riggs", rarity="Rare"),
    "Strafe":          ItemData(card_off + riggs_off + R + 3, "Card", True, character="Riggs", rarity="Rare"),
    "Think Twice":     ItemData(card_off + riggs_off + R + 4, "Card", True, character="Riggs", rarity="Rare"),

    # Peri
    "Escalate":      ItemData(card_off + peri_off + C,     "Card", True, character="Peri", rarity="Common"),
    "Extra Battery": ItemData(card_off + peri_off + C + 1, "Card", True, character="Peri", rarity="Common"),
    "Feint":         ItemData(card_off + peri_off + C + 2, "Card", True, character="Peri", rarity="Common"),
    "Lunge":         ItemData(card_off + peri_off + C + 3, "Card", True, character="Peri", rarity="Common", starter=True),
    "Multi Blast":   ItemData(card_off + peri_off + C + 4, "Card", True, character="Peri", rarity="Common"),
    "Multi Shot":    ItemData(card_off + peri_off + C + 5, "Card", True, character="Peri", rarity="Common", starter=True),
    "Overpower":     ItemData(card_off + peri_off + C + 6, "Card", True, character="Peri", rarity="Common"),
    "Scoot":         ItemData(card_off + peri_off + C + 7, "Card", True, character="Peri", rarity="Common"),
    "Wave Charge":   ItemData(card_off + peri_off + C + 8, "Card", True, character="Peri", rarity="Common"),

    "Barrage":           ItemData(card_off + peri_off + UC,     "Card", True, character="Peri", rarity="Uncommon"),
    "Battle Repair":     ItemData(card_off + peri_off + UC + 1, "Card", True, character="Peri", rarity="Uncommon"),
    "Flux":              ItemData(card_off + peri_off + UC + 2, "Card", True, character="Peri", rarity="Uncommon"),
    "Frontloaded Blast": ItemData(card_off + peri_off + UC + 3, "Card", True, character="Peri", rarity="Uncommon"),
    "Power Play":        ItemData(card_off + peri_off + UC + 4, "Card", True, character="Peri", rarity="Uncommon"),
    "Rev the Engines":   ItemData(card_off + peri_off + UC + 5, "Card", True, character="Peri", rarity="Uncommon"),
    "Sidestep":          ItemData(card_off + peri_off + UC + 6, "Card", True, character="Peri", rarity="Uncommon"),

    "Endless Magazine": ItemData(card_off + peri_off + R,     "Card", True, character="Peri", rarity="Rare"),
    "Inverter":         ItemData(card_off + peri_off + R + 1, "Card", True, character="Peri", rarity="Rare"),
    "Parry":            ItemData(card_off + peri_off + R + 2, "Card", True, character="Peri", rarity="Rare"),
    "Table Flip":       ItemData(card_off + peri_off + R + 3, "Card", True, character="Peri", rarity="Rare"),
    "Weaken Hull":      ItemData(card_off + peri_off + R + 4, "Card", True, character="Peri", rarity="Rare"),

    # Isaac
    "Attack Drone":   ItemData(card_off + isaac_off + C,     "Card", True, character="Isaac", rarity="Common", starter=True),
    "Flex Move":      ItemData(card_off + isaac_off + C + 1, "Card", True, character="Isaac", rarity="Common"),
    "Missile Shot":   ItemData(card_off + isaac_off + C + 2, "Card", True, character="Isaac", rarity="Common"),
    "Parallel Shift": ItemData(card_off + isaac_off + C + 3, "Card", True, character="Isaac", rarity="Common", starter=True),
    "Shield Drone":   ItemData(card_off + isaac_off + C + 4, "Card", True, character="Isaac", rarity="Common"),
    "Shift Shot":     ItemData(card_off + isaac_off + C + 5, "Card", True, character="Isaac", rarity="Common"),
    "Small Boulder":  ItemData(card_off + isaac_off + C + 6, "Card", True, character="Isaac", rarity="Common"),
    "Solar Breeze":   ItemData(card_off + isaac_off + C + 7, "Card", True, character="Isaac", rarity="Common"),
    "Space Mine":     ItemData(card_off + isaac_off + C + 8, "Card", True, character="Isaac", rarity="Common"),

    "Battalion":        ItemData(card_off + isaac_off + UC,     "Card", True, character="Isaac", rarity="Uncommon"),
    "Boulder Bundle":   ItemData(card_off + isaac_off + UC + 1, "Card", True, character="Isaac", rarity="Uncommon"),
    "Bubble Field":     ItemData(card_off + isaac_off + UC + 2, "Card", True, character="Isaac", rarity="Uncommon"),
    "Large Boulders":   ItemData(card_off + isaac_off + UC + 3, "Card", True, character="Isaac", rarity="Uncommon"),
    "Radio Control":    ItemData(card_off + isaac_off + UC + 4, "Card", True, character="Isaac", rarity="Uncommon"),
    "Repair Kit":       ItemData(card_off + isaac_off + UC + 5, "Card", True, character="Isaac", rarity="Uncommon"),
    "Striker Squadron": ItemData(card_off + isaac_off + UC + 6, "Card", True, character="Isaac", rarity="Uncommon"),

    "Bay Overload":  ItemData(card_off + isaac_off + R,     "Card", True, character="Isaac", rarity="Rare"),
    "Energy Drone":  ItemData(card_off + isaac_off + R + 1, "Card", True, character="Isaac", rarity="Rare"),
    "Jupiter Drone": ItemData(card_off + isaac_off + R + 2, "Card", True, character="Isaac", rarity="Rare"),
    "Rock Factory":  ItemData(card_off + isaac_off + R + 3, "Card", True, character="Isaac", rarity="Rare"),
    "Scattershot":   ItemData(card_off + isaac_off + R + 4, "Card", True, character="Isaac", rarity="Rare"),

    # Drake
    "Combustion Engine":  ItemData(card_off + drake_off + C,     "Card", True, character="Drake", rarity="Common"),
    "Desperate Measures": ItemData(card_off + drake_off + C + 1, "Card", True, character="Drake", rarity="Common"),
    "EMP Slug":           ItemData(card_off + drake_off + C + 2, "Card", True, character="Drake", rarity="Common", starter=True),
    "Exothermic Release": ItemData(card_off + drake_off + C + 3, "Card", True, character="Drake", rarity="Common"),
    "Explosive Slug":     ItemData(card_off + drake_off + C + 4, "Card", True, character="Drake", rarity="Common"),
    "Firewall":           ItemData(card_off + drake_off + C + 5, "Card", True, character="Drake", rarity="Common"),
    "Heatsink":           ItemData(card_off + drake_off + C + 6, "Card", True, character="Drake", rarity="Common", starter=True),
    "Hot Compress":       ItemData(card_off + drake_off + C + 7, "Card", True, character="Drake", rarity="Common"),
    "Hotfoot":            ItemData(card_off + drake_off + C + 8, "Card", True, character="Drake", rarity="Common"),

    "Aggressive Armoring": ItemData(card_off + drake_off + UC,     "Card", True, character="Drake", rarity="Uncommon"),
    "Flash Point":         ItemData(card_off + drake_off + UC + 1, "Card", True, character="Drake", rarity="Uncommon"),
    "Heatwave":            ItemData(card_off + drake_off + UC + 2, "Card", True, character="Drake", rarity="Uncommon"),
    "Sear":                ItemData(card_off + drake_off + UC + 3, "Card", True, character="Drake", rarity="Uncommon"),
    "Solar Flair":         ItemData(card_off + drake_off + UC + 4, "Card", True, character="Drake", rarity="Uncommon"),
    "Ventilator":          ItemData(card_off + drake_off + UC + 5, "Card", True, character="Drake", rarity="Uncommon"),
    "Volatile Vapor":      ItemData(card_off + drake_off + UC + 6, "Card", True, character="Drake", rarity="Uncommon"),

    "Freeze Dry":          ItemData(card_off + drake_off + R,     "Card", True, character="Drake", rarity="Rare"),
    "From Hell's Heart":   ItemData(card_off + drake_off + R + 1, "Card", True, character="Drake", rarity="Rare"),
    "Pillage and Plunder": ItemData(card_off + drake_off + R + 2, "Card", True, character="Drake", rarity="Rare"),
    "Serenity":            ItemData(card_off + drake_off + R + 3, "Card", True, character="Drake", rarity="Rare"),
    "Thermal Battery":     ItemData(card_off + drake_off + R + 4, "Card", True, character="Drake", rarity="Rare"),

    # Max
    "Admin Deploy":    ItemData(card_off + max_off + C,     "Card", True, character="Max", rarity="Common", starter=True),
    "Cloud Save":      ItemData(card_off + max_off + C + 1, "Card", True, character="Max", rarity="Common"),
    "Dice Roll":       ItemData(card_off + max_off + C + 2, "Card", True, character="Max", rarity="Common"),
    "Math.Max":        ItemData(card_off + max_off + C + 3, "Card", True, character="Max", rarity="Common"),
    "Reroll":          ItemData(card_off + max_off + C + 4, "Card", True, character="Max", rarity="Common", starter=True),
    "Reroute":         ItemData(card_off + max_off + C + 5, "Card", True, character="Max", rarity="Common"),
    "Shuffle Shot":    ItemData(card_off + max_off + C + 6, "Card", True, character="Max", rarity="Common"),
    "System Security": ItemData(card_off + max_off + C + 7, "Card", True, character="Max", rarity="Common"),
    "Worm":            ItemData(card_off + max_off + C + 8, "Card", True, character="Max", rarity="Common"),

    "Branch Prediction": ItemData(card_off + max_off + UC,     "Card", True, character="Max", rarity="Uncommon"),
    "Enrage":            ItemData(card_off + max_off + UC + 1, "Card", True, character="Max", rarity="Uncommon"),
    "Escape Artist":     ItemData(card_off + max_off + UC + 2, "Card", True, character="Max", rarity="Uncommon"),
    "Lazy Barrage":      ItemData(card_off + max_off + UC + 3, "Card", True, character="Max", rarity="Uncommon"),
    "Memory Leak":       ItemData(card_off + max_off + UC + 4, "Card", True, character="Max", rarity="Uncommon"),
    "Root Access":       ItemData(card_off + max_off + UC + 5, "Card", True, character="Max", rarity="Uncommon"),
    "Spacer":            ItemData(card_off + max_off + UC + 6, "Card", True, character="Max", rarity="Uncommon"),

    "Backup Stick":     ItemData(card_off + max_off + R,     "Card", True, character="Max", rarity="Rare"),
    "Clean Exhaust":    ItemData(card_off + max_off + R + 1, "Card", True, character="Max", rarity="Rare"),
    "Overclock":        ItemData(card_off + max_off + R + 2, "Card", True, character="Max", rarity="Rare"),
    "Save State":       ItemData(card_off + max_off + R + 3, "Card", True, character="Max", rarity="Rare"),
    "Total Cache Wipe": ItemData(card_off + max_off + R + 4, "Card", True, character="Max", rarity="Rare"),

    # Books
    "Glimmer Shot":       ItemData(card_off + books_off + C,     "Card", True, character="Books", rarity="Common"),
    "Mage Hand":          ItemData(card_off + books_off + C + 1, "Card", True, character="Books", rarity="Common", starter=True),
    "Magi-Battery":       ItemData(card_off + books_off + C + 2, "Card", True, character="Books", rarity="Common"),
    "Meteor":             ItemData(card_off + books_off + C + 3, "Card", True, character="Books", rarity="Common"),
    "Mining Drill":       ItemData(card_off + books_off + C + 4, "Card", True, character="Books", rarity="Common"),
    "Sapphire Shield":    ItemData(card_off + books_off + C + 5, "Card", True, character="Books", rarity="Common"),
    "Swizzle Shift":      ItemData(card_off + books_off + C + 6, "Card", True, character="Books", rarity="Common"),
    "Unpolished Crystal": ItemData(card_off + books_off + C + 7, "Card", True, character="Books", rarity="Common", starter=True),
    "Zircon Zip":         ItemData(card_off + books_off + C + 8, "Card", True, character="Books", rarity="Common"),

    "Avid Reader":     ItemData(card_off + books_off + UC,     "Card", True, character="Books", rarity="Uncommon"),
    "Block Evolution": ItemData(card_off + books_off + UC + 1, "Card", True, character="Books", rarity="Uncommon"),
    "Bloodstone Bolt": ItemData(card_off + books_off + UC + 2, "Card", True, character="Books", rarity="Uncommon"),
    "Catch":           ItemData(card_off + books_off + UC + 3, "Card", True, character="Books", rarity="Uncommon"),
    "Mineral Deposit": ItemData(card_off + books_off + UC + 4, "Card", True, character="Books", rarity="Uncommon"),
    "Ol' Reliable":    ItemData(card_off + books_off + UC + 5, "Card", True, character="Books", rarity="Uncommon"),
    "Shardpack":       ItemData(card_off + books_off + UC + 6, "Card", True, character="Books", rarity="Uncommon"),

    "Medusa Field":      ItemData(card_off + books_off + R,     "Card", True, character="Books", rarity="Rare"),
    "Overflowing Power": ItemData(card_off + books_off + R + 1, "Card", True, character="Books", rarity="Rare"),
    "Perfect Specimen":  ItemData(card_off + books_off + R + 2, "Card", True, character="Books", rarity="Rare"),
    "Quantum Quarry":    ItemData(card_off + books_off + R + 3, "Card", True, character="Books", rarity="Rare"),
    "Zero Draw":         ItemData(card_off + books_off + R + 4, "Card", True, character="Books", rarity="Rare"),

    # CAT
    "Defensive Mode": ItemData(card_off + cat_off + C,     "Card", True, character="CAT", rarity="Common"),
    "Dizzy.EXE":      ItemData(card_off + cat_off + C + 1, "Card", True, character="CAT", rarity="Common", starter=True),
    "Drake.EXE":      ItemData(card_off + cat_off + C + 2, "Card", True, character="CAT", rarity="Common", starter=True),
    "Isaac.EXE":      ItemData(card_off + cat_off + C + 3, "Card", True, character="CAT", rarity="Common", starter=True),
    "Max.EXE":        ItemData(card_off + cat_off + C + 4, "Card", True, character="CAT", rarity="Common", starter=True),
    "Peri.EXE":       ItemData(card_off + cat_off + C + 5, "Card", True, character="CAT", rarity="Common", starter=True),
    "Riggs.EXE":      ItemData(card_off + cat_off + C + 6, "Card", True, character="CAT", rarity="Common", starter=True),

    "Aegis":              ItemData(card_off + cat_off + UC,     "Card", True, character="CAT", rarity="Uncommon"),
    "Books.EXE":          ItemData(card_off + cat_off + UC + 1, "Card", True, character="CAT", rarity="Uncommon", starter=True),
    "CAT.EXE":            ItemData(card_off + cat_off + UC + 2, "Card", True, character="CAT", rarity="Uncommon", starter=True),
    "I Frames":           ItemData(card_off + cat_off + UC + 3, "Card", True, character="CAT", rarity="Uncommon"),
    "Jack of All Trades": ItemData(card_off + cat_off + UC + 4, "Card", True, character="CAT", rarity="Uncommon"),
    "Quick Fix":          ItemData(card_off + cat_off + UC + 5, "Card", True, character="CAT", rarity="Uncommon"),
    "Temporal Anomaly":   ItemData(card_off + cat_off + UC + 6, "Card", True, character="CAT", rarity="Uncommon"),

    "Adaptability": ItemData(card_off + cat_off + R,     "Card", True, character="CAT", rarity="Rare"),
    "AI Overflow":  ItemData(card_off + cat_off + R + 1, "Card", True, character="CAT", rarity="Rare"),
    "Prism":        ItemData(card_off + cat_off + R + 2, "Card", True, character="CAT", rarity="Rare"),
    "Time Skip":    ItemData(card_off + cat_off + R + 3, "Card", True, character="CAT", rarity="Rare"),

    # ARTIFACTS

    # Basic
    "Nanofiber Hull":        ItemData(artifact_off + C,      "Artifact", True, rarity="Common"),
    "Overcharger":           ItemData(artifact_off + C + 1,  "Artifact", True, rarity="Common"),
    "Crosslink":             ItemData(artifact_off + C + 2,  "Artifact", True, rarity="Common"),
    "Shield Memory":         ItemData(artifact_off + C + 3,  "Artifact", True, rarity="Common"),
    "Jumper Cables":         ItemData(artifact_off + C + 4,  "Artifact", True, rarity="Common"),
    "Hull Plating":          ItemData(artifact_off + C + 5,  "Artifact", True, rarity="Common"),
    "Armored Bay":           ItemData(artifact_off + C + 6,  "Artifact", True, rarity="Common"),
    "Recalibrator":          ItemData(artifact_off + C + 7,  "Artifact", True, rarity="Common"),
    "Grazer Beam":           ItemData(artifact_off + C + 8,  "Artifact", True, rarity="Common"),
    "Jet Thrusters":         ItemData(artifact_off + C + 9,  "Artifact", True, rarity="Common"),
    "Prepped Batteries":     ItemData(artifact_off + C + 10, "Artifact", True, rarity="Common"),
    "Energy Refund":         ItemData(artifact_off + C + 11, "Artifact", True, rarity="Common"),
    "Overclocked Generator": ItemData(artifact_off + C + 12, "Artifact", True, rarity="Common"),
    "Cockpit Lock-On":       ItemData(artifact_off + C + 13, "Artifact", True, rarity="Common"),
    "Stun Calibrator":       ItemData(artifact_off + C + 14, "Artifact", True, rarity="Common"),
    "Ion Converter":         ItemData(artifact_off + C + 15, "Artifact", True, rarity="Common"),
    "Fracture Detection":    ItemData(artifact_off + C + 16, "Artifact", True, rarity="Common"),
    "Ricochet Paddle":       ItemData(artifact_off + C + 17, "Artifact", True, rarity="Common"),
    "Adaptive Plating":      ItemData(artifact_off + C + 18, "Artifact", True, rarity="Common"),
    "Piercer":               ItemData(artifact_off + C + 19, "Artifact", True, rarity="Common"),
    "Heal Booster":          ItemData(artifact_off + C + 20, "Artifact", True, rarity="Common"),
    "Jettison Hatch":        ItemData(artifact_off + C + 21, "Artifact", True, rarity="Common"),
    "Sharp Edges":           ItemData(artifact_off + C + 22, "Artifact", True, rarity="Common"),
    "Chaff Emitters":        ItemData(artifact_off + C + 23, "Artifact", True, rarity="Common"),

    "Radar Subwoofer":       ItemData(artifact_off + C + 24, "Artifact", True, rarity="Common"),

    "Glass Cannon":     ItemData(artifact_off + R,     "Artifact", True, rarity="Boss"),
    "Simplicity":       ItemData(artifact_off + R + 1, "Artifact", True, rarity="Boss"),
    "Dirty Engines":    ItemData(artifact_off + R + 2, "Artifact", True, rarity="Boss"),
    "Genesis":          ItemData(artifact_off + R + 3, "Artifact", True, rarity="Boss"),
    "Hi Freq Intercom": ItemData(artifact_off + R + 4, "Artifact", True, rarity="Boss"),

    "Warp Mastery":              ItemData(artifact_off + R + 5,  "Artifact", True, rarity="Boss"),
    "Hunter Wings":              ItemData(artifact_off + R + 6,  "Artifact", True, rarity="Boss"),
    "Ares Cannon V2":            ItemData(artifact_off + R + 7,  "Artifact", True, rarity="Boss"),
    "Jupiter Drone Hub Booster": ItemData(artifact_off + R + 8,  "Artifact", True, rarity="Boss"),
    "Gemini Core Booster":       ItemData(artifact_off + R + 9,  "Artifact", True, rarity="Boss"),
    "Mooring Line V2":           ItemData(artifact_off + R + 10, "Artifact", True, rarity="Boss"),

    # Dizzy
    "Photon Condenser": ItemData(artifact_off + dizzy_off + C,     "Artifact", True, character="Dizzy", rarity="Common"),
    "Shield Reserves":  ItemData(artifact_off + dizzy_off + C + 1, "Artifact", True, character="Dizzy", rarity="Common"),
    "Rebound Reagent":  ItemData(artifact_off + dizzy_off + C + 2, "Artifact", True, character="Dizzy", rarity="Common"),
    "Regenerator":      ItemData(artifact_off + dizzy_off + C + 3, "Artifact", True, character="Dizzy", rarity="Common"),

    "Shield Burst": ItemData(artifact_off + dizzy_off + R,     "Artifact", True, character="Dizzy", rarity="Boss"),
    "Prototype 22": ItemData(artifact_off + dizzy_off + R + 1, "Artifact", True, character="Dizzy", rarity="Boss"),

    # Riggs
    "Quickdraw":               ItemData(artifact_off + riggs_off + C,     "Artifact", True, character="Riggs", rarity="Common"),
    "Perpetual Motion Device": ItemData(artifact_off + riggs_off + C + 1, "Artifact", True, character="Riggs", rarity="Common"),
    "Caffeine Rush":           ItemData(artifact_off + riggs_off + C + 2, "Artifact", True, character="Riggs", rarity="Common"),

    "Demon Thrusters": ItemData(artifact_off + riggs_off + R,     "Artifact", True, character="Riggs", rarity="Boss"),
    "Flywheel":        ItemData(artifact_off + riggs_off + R + 1, "Artifact", True, character="Riggs", rarity="Boss"),

    # Peri
    "Dakka Drum":    ItemData(artifact_off + peri_off + C,     "Artifact", True, character="Peri", rarity="Common"),
    "Revenge Drive": ItemData(artifact_off + peri_off + C + 1, "Artifact", True, character="Peri", rarity="Common"),
    "Premeditation": ItemData(artifact_off + peri_off + C + 2, "Artifact", True, character="Peri", rarity="Common"),

    "Power Diversion": ItemData(artifact_off + peri_off + R,     "Artifact", True, character="Peri", rarity="Boss"),
    "Berserker Drive": ItemData(artifact_off + peri_off + R + 1, "Artifact", True, character="Peri", rarity="Boss"),

    # Isaac
    "Wave Control":    ItemData(artifact_off + isaac_off + C,     "Artifact", True, character="Isaac", rarity="Common"),
    "Bubbler":         ItemData(artifact_off + isaac_off + C + 1, "Artifact", True, character="Isaac", rarity="Common"),
    "Garvel Recycler": ItemData(artifact_off + isaac_off + C + 2, "Artifact", True, character="Isaac", rarity="Common"),
    "Drone Piercer":   ItemData(artifact_off + isaac_off + C + 3, "Artifact", True, character="Isaac", rarity="Common"),

    "Radio Repeater": ItemData(artifact_off + isaac_off + R,     "Artifact", True, character="Isaac", rarity="Boss"),
    "Salvage Arm":    ItemData(artifact_off + isaac_off + R + 1, "Artifact", True, character="Isaac", rarity="Boss"),

    # Drake
    "Pressure Fuse":       ItemData(artifact_off + drake_off + C,     "Artifact", True, character="Drake", rarity="Common"),
    "Subzero Heatsinks":   ItemData(artifact_off + drake_off + C + 1, "Artifact", True, character="Drake", rarity="Common"),
    "Ignition Coil":       ItemData(artifact_off + drake_off + C + 2, "Artifact", True, character="Drake", rarity="Common"),
    "Heat Distiller":      ItemData(artifact_off + drake_off + C + 3, "Artifact", True, character="Drake", rarity="Common"),
    "Next Gen Insulation": ItemData(artifact_off + drake_off + C + 4, "Artifact", True, character="Drake", rarity="Common"),

    "Thermo Reactor": ItemData(artifact_off + drake_off + R, "Artifact", True, character="Drake", rarity="Boss"),

    # Max
    "Safety Lock":  ItemData(artifact_off + max_off + C,     "Artifact", True, character="Max", rarity="Common"),
    "Sticky Note":  ItemData(artifact_off + max_off + C + 1, "Artifact", True, character="Max", rarity="Common"),
    "Right Click":  ItemData(artifact_off + max_off + C + 2, "Artifact", True, character="Max", rarity="Common"),
    "Strong Start": ItemData(artifact_off + max_off + C + 3, "Artifact", True, character="Max", rarity="Common"),

    "Flow State":             ItemData(artifact_off + max_off + R,     "Artifact", True, character="Max", rarity="Boss"),
    "Tridimensional Cockpit": ItemData(artifact_off + max_off + R + 1, "Artifact", True, character="Max", rarity="Boss"),
    "Lightspeed Boot Disk":   ItemData(artifact_off + max_off + R + 2, "Artifact", True, character="Max", rarity="Boss"),

    # Books
    "Grimoire":        ItemData(artifact_off + books_off + C,     "Artifact", True, character="Books", rarity="Common"),
    "Resonance Fork":  ItemData(artifact_off + books_off + C + 1, "Artifact", True, character="Books", rarity="Common"),
    "Shard Enchanter": ItemData(artifact_off + books_off + C + 2, "Artifact", True, character="Books", rarity="Common"),
    "Shard Collector": ItemData(artifact_off + books_off + C + 3, "Artifact", True, character="Books", rarity="Common"),
    "Rock Collection": ItemData(artifact_off + books_off + C + 4, "Artifact", True, character="Books", rarity="Common"),

    "Zero Doubler": ItemData(artifact_off + books_off + R, "Artifact", True, character="Books", rarity="Boss"),

    # CAT
    "Standby Mode":    ItemData(artifact_off + cat_off + C,     "Artifact", True, character="CAT", rarity="Common"),
    "Initial Booster": ItemData(artifact_off + cat_off + C + 1, "Artifact", True, character="CAT", rarity="Common"),
    "Multi Threading": ItemData(artifact_off + cat_off + C + 2, "Artifact", True, character="CAT", rarity="Common"),

    "Summon Control": ItemData(artifact_off + cat_off + R, "Artifact", True, character="CAT", rarity="Boss"),
}
