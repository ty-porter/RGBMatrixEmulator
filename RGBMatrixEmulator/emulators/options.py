import json
import os

from RGBMatrixEmulator.display_adapters import DISPLAY_ADAPTER_TYPES


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

        if emulator_config.pixel_style.lower() in ['square', 'circle']:
            self.pixel_style = emulator_config.pixel_style
        else:
            print('EMULATOR: Warning! "{}" pixel style option not recognized. Valid options are "square", "circle". Defaulting to "square"...'.format(emulator_config.pixel_style))
            self.pixel_style = self.default_config['pixel_style']

        if emulator_config.display_adapter.lower() in DISPLAY_ADAPTER_TYPES:
            self.display_adapter = DISPLAY_ADAPTER_TYPES[emulator_config.display_adapter.lower()]
        else:
            self.display_adapter = DISPLAY_ADAPTER_TYPES[self.default_config['display_adapter']]


        self.pixel_size = emulator_config.pixel_size

    def window_size(self):
        return (self.cols * self.pixel_size * self.chain_length, self.rows * self.pixel_size * self.parallel)

class RGBMatrixEmulatorConfig:
    __CONFIG_PATH = 'emulator_config.json'

    def __init__(self):
        self.__config = self.__load_config()

        self.pixel_size      = self.__config.get('pixel_size', 16)
        self.pixel_style     = self.__config.get('pixel_style', 'square')
        self.display_adapter = self.__config.get('display_adapter', 'pygame')

    def __load_config(self):
        if os.path.exists(self.__CONFIG_PATH):
            with open(self.__CONFIG_PATH) as f:
                config = json.load(f)

            return config    

        with open(self.__CONFIG_PATH, 'w') as f:
            json.dump(self.__default_config(), f, indent=4)

        return self.__default_config()

    def __default_config(self):
        return {
            'pixel_size': 16,
            'pixel_style': 'square',
            'display_adapter': 'terminal'
        }