import random

from logic.entities.orders.assassination_order import AssassinationOrder
from logic.entities.units.models.frozen_wyverns.tier1.bomb.bomb import Bomb
from logic.entities.units.models.frozen_wyverns.tier1.wyverns_mage.wyverns_mage import WyvernsMage
from logic.entities.units.models.frozen_wyverns.tier1.warrior.warrior import Warrior
from logic.entities.units.models.frozen_wyverns.tier2.mini_treant.mini_treant import MiniTreant
from logic.entities.units.models.frozen_wyverns.tier2.skeleton_thrasher.skeleton_thrasher import SkeletonThrasher
from logic.entities.units.models.frozen_wyverns.tier2.treant.treant import Treant
from logic.entities.units.models.frozen_wyverns.tier3.necromancer.necromancer import Necromancer


def generate_order():
    order_types = [AssassinationOrder]

    enemy_types = [
        Warrior,
        WyvernsMage,
        Bomb,
        SkeletonThrasher,
        MiniTreant,
        Necromancer,
        Treant
    ]

    order_type = random.choice(order_types)
    enemy_type = random.choice(enemy_types)

    target_count = random.randint(10, 50)

    return order_type(enemy_type, target_count)