from copy import deepcopy

import pygame

from logic.core.db_service import DBService


class KeySettings:
    __key_settings = {
        'UP': pygame.KSCAN_W,
        'DOWN': pygame.KSCAN_S,
        'LEFT': pygame.KSCAN_A,
        'RIGHT': pygame.KSCAN_D,
        'ATTACK': pygame.KSCAN_SPACE,
        'ACTION': pygame.KSCAN_E,
        'STORE_SWITCH_MODE': pygame.KSCAN_U,
        'SLOT_1': pygame.KSCAN_1,
        'SLOT_2': pygame.KSCAN_2,
        'SLOT_3': pygame.KSCAN_3,
        'SLOT_4': pygame.KSCAN_4,
        'SLOT_5': pygame.KSCAN_5,
        'SLOT_6': pygame.KSCAN_6,
        'SLOT_7': pygame.KSCAN_7,
        'SLOT_8': pygame.KSCAN_8,
        'SLOT_9': pygame.KSCAN_9,
        'SLOT_10': pygame.KSCAN_0
    }

    __defaults_key_settings = deepcopy(__key_settings)

    __possible_keys = {
        pygame.KSCAN_Q: 'Q',
        pygame.KSCAN_W: 'W',
        pygame.KSCAN_E: 'E',
        pygame.KSCAN_R: 'R',
        pygame.KSCAN_T: 'T',
        pygame.KSCAN_Y: 'Y',
        pygame.KSCAN_U: 'U',
        pygame.KSCAN_I: 'I',
        pygame.KSCAN_O: 'O',
        pygame.KSCAN_P: 'P',
        pygame.KSCAN_A: 'A',
        pygame.KSCAN_S: 'S',
        pygame.KSCAN_D: 'D',
        pygame.KSCAN_F: 'F',
        pygame.KSCAN_G: 'G',
        pygame.KSCAN_H: 'H',
        pygame.KSCAN_J: 'J',
        pygame.KSCAN_K: 'K',
        pygame.KSCAN_L: 'L',
        pygame.KSCAN_Z: 'Z',
        pygame.KSCAN_X: 'X',
        pygame.KSCAN_C: 'C',
        pygame.KSCAN_V: 'V',
        pygame.KSCAN_B: 'B',
        pygame.KSCAN_N: 'N',
        pygame.KSCAN_M: 'M',
        pygame.KSCAN_SPACE: 'SPACE',
        pygame.KSCAN_TAB: 'TAB',
        pygame.KSCAN_LSHIFT: 'L_SHIFT',
        pygame.KSCAN_RSHIFT: 'R_SHIFT',
        pygame.KSCAN_KP_ENTER: 'ENTER',
        pygame.KSCAN_RALT: 'R_ALT',
        pygame.KSCAN_LALT: 'L_ALT',
        pygame.KSCAN_LCTRL: 'L_CTRL',
        pygame.KSCAN_RCTRL: 'R_CTRL',
        pygame.KSCAN_UP: 'UP',
        pygame.KSCAN_LEFT: 'LEFT',
        pygame.KSCAN_RIGHT: 'RIGHT',
        pygame.KSCAN_DOWN: 'DOWN',
        pygame.KSCAN_1: '1',
        pygame.KSCAN_2: '2',
        pygame.KSCAN_3: '3',
        pygame.KSCAN_4: '4',
        pygame.KSCAN_5: '5',
        pygame.KSCAN_6: '6',
        pygame.KSCAN_7: '7',
        pygame.KSCAN_8: '8',
        pygame.KSCAN_9: '9',
        pygame.KSCAN_0: '0',
        pygame.KSCAN_KP_PLUS: '+',
        pygame.KSCAN_KP_MINUS: '-',
        pygame.KSCAN_F1: 'F1',
        pygame.KSCAN_F2: 'F2',
        pygame.KSCAN_F3: 'F3',
        pygame.KSCAN_F4: 'F4',
        pygame.KSCAN_F5: 'F5',
        pygame.KSCAN_F6: 'F6',
        pygame.KSCAN_F7: 'F7',
        pygame.KSCAN_F8: 'F8',
        pygame.KSCAN_F9: 'F9',
        pygame.KSCAN_F10: 'F10',
        pygame.KSCAN_F11: 'F11',
        pygame.KSCAN_F12: 'F12',
        None: ''
    }
    __keys_data_path = 'resources/game_data/keys_data'

    @staticmethod
    def initialize():
        existing_keys = DBService.export_all_data(KeySettings.__keys_data_path)
        for key in existing_keys:
            KeySettings.__key_settings[key] = existing_keys[key]

    @staticmethod
    def get_current_settings():
        return KeySettings.__key_settings

    @staticmethod
    def get_possible_keys() -> dict[int | None, str]:
        return KeySettings.__possible_keys

    @staticmethod
    def get_defaults_keys() -> dict[str, int]:
        return KeySettings.__defaults_key_settings

    @staticmethod
    def get_value_for_scancode(scancode: int | None) -> str | None:
        if scancode in KeySettings.__possible_keys:
            return KeySettings.__possible_keys[scancode]
        else:
            return None

    @staticmethod
    def update(new_keys: dict[str, int]):
        for key, value in new_keys.items():
            if key in KeySettings.__key_settings and value != KeySettings.__key_settings[key]:
                DBService.insert_data(key, value, KeySettings.__keys_data_path)
                KeySettings.__key_settings[key] = value

    @staticmethod
    def get_key(key_name: str) -> int | None:
        if key_name in KeySettings.__key_settings:
            return KeySettings.__key_settings[key_name]
        else:
            return None
