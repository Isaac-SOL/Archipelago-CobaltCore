from BaseClasses import MultiWorld, Region, Entrance
from . import CHARACTERS, CobaltCoreLocation
from .Locations import find_locations, location_table


def create_regions(multiworld, player: int):
    # Here Regions are abstract and represent characters

    multiworld.regions += [
        create_region(multiworld, player, 'Menu', None, ['Starting Bonus']),
        create_region(multiworld, player, 'General', find_locations(loc_character=""),
                      [f"Find {c}" for c in CHARACTERS])
    ]
    multiworld.regions += [
        create_region(multiworld, player, f"{c} Items", find_locations(loc_character=c), [])
        for c in CHARACTERS
    ]

    # link up regions
    multiworld.get_entrance('Starting Bonus', player).connect(multiworld.get_region('General', player))
    for c in CHARACTERS:
        multiworld.get_entrance(f"Find {c}", player).connect(multiworld.get_region(f"{c} Items", player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = location_table[location].address
            location = CobaltCoreLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
