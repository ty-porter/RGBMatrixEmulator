import json, os, pprint

from RGBMatrixEmulator.internal.pixel_style import PixelStyle
from RGBMatrixEmulator.internal.adapter_loader import AdapterLoader
from RGBMatrixEmulator.logger import Logger


class RGBMatrixEmulatorConfig:
    CONFIG_PATH = "emulator_config.json"

    DEFAULT_CONFIG = {
        "pixel_outline": 0,
        "pixel_size": 16,
        "pixel_style": "square",
        "pixel_glow": 6,
        "display_adapter": "browser",
        "allow_adapter_fallback": True,
        "icon_path": None,
        "emulator_title": None,
        "suppress_font_warnings": False,
        "browser": {
            "_comment": "For use with the browser adapter only.",
            "port": 8888,
            "target_fps": 60,
            "fps_display": False,
            "quality": 70,
            "image_border": True,
            "debug_text": False,
            "image_format": "JPEG",
            "open_immediately": False,
        },
        "pi5": {
            "_comment": "For use with the pi5 adapter only.",
            "pinout": "AdafruitMatrixBonnet",
            "n_addr_lines": 4,
            "rotation": "Normal",
            "n_planes": 10,
            "n_temporal_planes": 4,
            "n_lanes": 1,
            "led_rgb_sequence": "RGB",
        },
        "log_level": "info",
    }

    def __init__(self):
        self.config = self.__load_config()
        self.default_config = self.DEFAULT_CONFIG

        RGBMatrixEmulatorConfig.Utils.set_attributes(self)

        loader = AdapterLoader(requested_adapter=self.display_adapter.lower())
        self.display_adapter = loader.load(fallback=self.allow_adapter_fallback)

        self.__validate_pixel_style()
        self.__validate_pixel_glow()

        if self.suppress_font_warnings:
            import bdfparser

            bdfparser.warnings.simplefilter("ignore")

    def __load_config(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH) as f:
                config = json.load(f)

            return config

        Logger.info("Existing emulator config not found...")
        self._dump_default_config()

        return self.DEFAULT_CONFIG

    @classmethod
    def _dump_default_config(cls):
        Logger.info("Creating a new default emulator config.")
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(cls.DEFAULT_CONFIG, f, indent=4)
        Logger.info("Created emulator_config.json.")

    def __validate_pixel_style(self):
        requested_style = self.pixel_style.upper()
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
                        self.pixel_style.lower(),
                        self.display_adapter.lower(),
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
                    self.pixel_style.lower(),
                    ", ".join(f'"{style.config_name}"' for style in list(PixelStyle)),
                    PixelStyle.DEFAULT.config_name,
                )
            )

    def __validate_pixel_glow(self):
        if not (isinstance(self.pixel_glow, int) and self.pixel_glow >= 0):
            Logger.warning(
                '"{}" pixel glow option not recognized. Valid options are integers >= 0. Defaulting to {}...'.format(
                    self.pixel_glow, self.DEFAULT_CONFIG.get("pixel_glow")
                )
            )

            self.pixel_glow = self.DEFAULT_CONFIG.get("pixel_glow")

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
