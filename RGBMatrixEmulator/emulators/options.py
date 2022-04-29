import json
import os

from RGBMatrixEmulator.adapters import ADAPTER_TYPES


class RGBMatrixOptions:
    def __init__(self):
        self.hardware_mapping = 'EMULATED'
        self.rows = 32
        self.cols = 32
        self.chain_length = 1
        self.parallel = 1
        self.row_address_type = 0
        self.multiplexing = 0
        self.pwm_bits = 0
        self.brightness = 100
        self.pwm_lsb_nanoseconds = 130
        self.led_rgb_sequence = 'RGB-EMULATED'
        self.show_refresh_rate = 0
        self.gpio_slowdown = None
        self.disable_hardware_pulsing = False

        emulator_config = RGBMatrixEmulatorConfig()

        if emulator_config.display_adapter.lower() in ADAPTER_TYPES:
            self.display_adapter = ADAPTER_TYPES[emulator_config.display_adapter.lower()]
        else:
            adapter_types = ', '.join('"{}"'.format(key) for key in ADAPTER_TYPES.keys())
            print('EMULATOR: Warning! "{}" display adapter option not recognized. Valid adapters are {}. Defaulting to "pygame"...'.format(emulator_config.display_adapter, adapter_types))
            self.display_adapter = ADAPTER_TYPES[emulator_config.DEFAULT_CONFIG.get('display_adapter')]

        self.pixel_style = emulator_config.DEFAULT_CONFIG.get('pixel_style')
        config_pixel_style = emulator_config.pixel_style.lower()

        if config_pixel_style in emulator_config.VALID_PIXEL_STYLES:
            if config_pixel_style != self.pixel_style:
                if self.display_adapter.SUPPORTS_ALTERNATE_PIXEL_STYLE:
                    self.pixel_style = emulator_config.pixel_style
                else:
                    print('EMULATOR: Warning! "{}" pixel style option is not supported by adapter "{}". Defaulting to "square"...'.format(config_pixel_style, emulator_config.display_adapter.lower()))
        else:
            print('EMULATOR: Warning! "{}" pixel style option not recognized. Valid options are "square", "circle". Defaulting to "square"...'.format(config_pixel_style))

        self.pixel_size = emulator_config.pixel_size

    def window_size(self):
        return (self.cols * self.pixel_size * self.chain_length, self.rows * self.pixel_size * self.parallel)

class RGBMatrixEmulatorConfig:

    __CONFIG_PATH = 'emulator_config.json'

    VALID_PIXEL_STYLES = ['square', 'circle']
    DEFAULT_CONFIG = {
        'pixel_size': 16,
        'pixel_style': 'square',
        'display_adapter': 'pygame'
    }

    def __init__(self):
        self.__config = self.__load_config()

        self.pixel_size      = self.__config.get('pixel_size',      16)
        self.pixel_style     = self.__config.get('pixel_style',     'square')
        self.display_adapter = self.__config.get('display_adapter', 'pygame')

    def __load_config(self):
        if os.path.exists(self.__CONFIG_PATH):
            with open(self.__CONFIG_PATH) as f:
                config = json.load(f)

            return config    

        with open(self.__CONFIG_PATH, 'w') as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=4)

        return self.DEFAULT_CONFIG
