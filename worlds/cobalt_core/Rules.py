from BaseClasses import MultiWorld
from . import CHARACTERS
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class CobaltCoreLogic(LogicMixin):
    def _cobalt_core_can_win(self, player: int) -> bool:
        return self.has_group("Memories", player, 8)


def set_rules(multiworld: MultiWorld, player: int):
    for c in CHARACTERS:
        set_rule(multiworld.get_entrance(f"Find {c}", player), lambda state: state.has(c, player))
    multiworld.completion_condition[player] = lambda state: state._cobalt_core_can_win(player)
