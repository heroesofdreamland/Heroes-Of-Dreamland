from enum import Enum


class AnimationType(Enum):
    ATTACK = 'attack'
    CAST = 'cast'
    STUN = 'stun'
    IDLE = 'idle'
    RUN = 'run'
    RESURRECTION = 'resurrection'
    DEATH_WITH_RESURRECTION = 'death_with_resurrection'
    BREATHING = 'breathing'
    DEATH = 'death'
    PREVIEW = 'preview'
    USED = 'used'
    HIDE = 'hide'
    VIEW = 'view'
    SPAWN = 'spawn'
    FIELD = 'field'
    SHIELD = 'shield'
    PREVIEW_STORE = 'preview_store'
    FLIES = 'flies'
    EXPLODE = 'explode'
    LEVEL_UP = 'level_up2'
