import json, os, pprint, sys

from RGBMatrixEmulator.adapters import ADAPTER_TYPES, PixelStyle
from RGBMatrixEmulator.logger import Logger


class RGBMatrixOptions:
    def __init__(self):
        self.hardware_mapping = "EMULATED"
        self.rows = 32
        self.cols = 32
        self.chain_length = 1
        self.parallel = 1
        self.row_address_type = 0
        self.multiplexing = 0
        self.pwm_bits = 0
        self.brightness = 100
        self.pwm_lsb_nanoseconds = 130
        self.led_rgb_sequence = "RGB-EMULATED"
        self.show_refresh_rate = 0
        self.gpio_slowdown = None
        self.disable_hardware_pulsing = False

        emulator_config = RGBMatrixEmulatorConfig()

        if emulator_config.display_adapter.lower() in ADAPTER_TYPES:
            self.display_adapter = ADAPTER_TYPES[
                emulator_config.display_adapter.lower()
            ]
        elif len(ADAPTER_TYPES.keys()) > 0:
            adapter_types = ", ".join(
                '"{}"'.format(key) for key in ADAPTER_TYPES.keys()
            )

            # Try to set it to the emulator default, but if it failed to load, pick the first one that did.
            if emulator_config.DEFAULT_CONFIG.get("display_adapter") in ADAPTER_TYPES:
                default_adapter = emulator_config.DEFAULT_CONFIG.get("display_adapter")
            else:
                default_adapter = list(ADAPTER_TYPES.keys())[0]

            Logger.warning(
                '"{}" display adapter option not recognized. Valid adapters are {}. Defaulting to "{}"...'.format(
                    emulator_config.display_adapter, adapter_types, default_adapter
                )
            )
            self.display_adapter = ADAPTER_TYPES[default_adapter]
        else:
            Logger.critical(
                "Failed to find a valid display adapter to load! Check that you have installed dependencies required for your configured adapter."
            )

            sys.exit(1)

        requested_style = emulator_config.pixel_style.upper()
        self.pixel_style = PixelStyle.fetch(requested_style)

        if self.pixel_style.name == requested_style:
            if self.pixel_style not in self.display_adapter.SUPPORTED_PIXEL_STYLES:
                self.pixel_style = PixelStyle.DEFAULT
                Logger.warning(
                    """
"{}" pixel style option is not supported by adapter "{}". 
Supported pixel styles for this adapter are {}
                                                              
Defaulting to "{}"...
""".format(
                        emulator_config.pixel_style.lower(),
                        emulator_config.display_adapter.lower(),
                        ", ".join(
                            f'"{style.config_name}"'
                            for style in self.display_adapter.SUPPORTED_PIXEL_STYLES
                        ),
                        PixelStyle.DEFAULT.config_name,
                    )
                )
        else:
            Logger.warning(
                '"{}" pixel style option not recognized. Valid options are {}. Defaulting to "{}"...'.format(
                    emulator_config.pixel_style.lower(),
                    ", ".join(f'"{style.config_name}"' for style in list(PixelStyle)),
                    PixelStyle.DEFAULT.config_name,
                )
            )

        self.pixel_glow = emulator_config.pixel_glow
        if not (isinstance(self.pixel_glow, int) and self.pixel_glow >= 0):
            Logger.warning(
                '"{}" pixel bleed option not recognized. Valid options are integers >= 0. Defaulting to {}...'.format(
                    self.pixel_glow, emulator_config.DEFAULT_CONFIG.get("pixel_glow")
                )
            )

            self.pixel_glow = emulator_config.DEFAULT_CONFIG.get("pixel_glow")

        self.pixel_size = emulator_config.pixel_size
        self.pixel_outline = emulator_config.DEFAULT_CONFIG["pixel_outline"]
        self.pixel_outline = emulator_config.pixel_outline
        self.browser = emulator_config.browser
        self.emulator_title = emulator_config.emulator_title
        self.icon_path = emulator_config.icon_path

        if emulator_config.suppress_font_warnings:
            import bdfparser

            bdfparser.warnings.simplefilter("ignore")

    def window_size(self):
        return (
            self.cols * self.pixel_size * self.chain_length,
            self.rows * self.pixel_size * self.parallel,
        )

    def window_size_str(self, pixel_text=""):
        width, height = self.window_size()

        return f"{width} x {height} {pixel_text}"


class RGBMatrixEmulatorConfig:
    CONFIG_PATH = "emulator_config.json"

    DEFAULT_CONFIG = {
        "pixel_outline": 0,
        "pixel_size": 16,
        "pixel_style": "square",
        "pixel_glow": 6,
        "display_adapter": "browser",
        "icon_path": None,
        "emulator_title": None,
        "suppress_font_warnings": False,
        "suppress_adapter_load_errors": False,
        "browser": {
            "_comment": "For use with the browser adapter only.",
            "port": 8888,
            "target_fps": 24,
            "fps_display": False,
            "quality": 70,
            "image_border": True,
            "debug_text": False,
            "image_format": "JPEG",
        },
        "log_level": "info",
    }

    def __init__(self):
        self.config = self.__load_config()
        self.default_config = self.DEFAULT_CONFIG

        RGBMatrixEmulatorConfig.Utils.set_attributes(self)

    def __load_config(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH) as f:
                config = json.load(f)

            return config

        with open(self.CONFIG_PATH, "w") as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=4)

        return self.DEFAULT_CONFIG

    def __str__(self):
        return RGBMatrixEmulatorConfig.Utils.to_str(self)

    class ChildConfig:
        def __init__(self, config, default_config):
            self.config = config
            self.default_config = default_config

            RGBMatrixEmulatorConfig.Utils.set_attributes(self)

        def __str__(self):
            return RGBMatrixEmulatorConfig.Utils.to_str(self)

    class Utils:
        def to_str(obj):
            """
            Pretty prints the config object from dict.
            """
            printer = pprint.PrettyPrinter(sort_dicts=False)
            return "\n".join(
                [
                    obj.__repr__(),
                    printer.pformat(RGBMatrixEmulatorConfig.Utils.to_dict(obj)),
                ]
            )

        def to_dict(obj):
            """
            Recursively recreates the config dict from child config objects.
            """
            config = {}
            for key in obj.__dict__.keys():
                if key in ["config", "default_config"] or key[0] == "_":
                    continue

                value = obj.__dict__.get(key)

                if isinstance(value, RGBMatrixEmulatorConfig.ChildConfig):
                    value = RGBMatrixEmulatorConfig.Utils.to_dict(value)

                config[key] = value

            return config

        def set_attributes(obj):
            """
            Dynamically set attributes loaded into config and default config variables.

            Numbers, strings, and arrays are stored natively. Nested dicts are parsed into RGBMatrixEmulatorChildConfig objects recursively.
            """
            for key in obj.default_config.keys():
                if key in obj.config:
                    value = obj.config.get(key)
                    default = obj.default_config.get(key)
                else:
                    value = obj.default_config.get(key)
                    default = value

                    Logger.warning(
                        "Emulator config is missing key '{}', falling back to default '{}'. Consider adding this to your emulator config file.".format(
                            key, value
                        )
                    )

                RGBMatrixEmulatorConfig.Utils.set_attribute(obj, key, value, default)

        def set_attribute(obj, key, value, default):
            """
            Store the value as an attribute or delegate to the RGBMatrixEmulatorChildConfig to parse into a new node.
            """
            if isinstance(value, dict):
                obj.__setattr__(
                    key, RGBMatrixEmulatorConfig.ChildConfig(value, default)
                )
            else:
                obj.__setattr__(key, value)
