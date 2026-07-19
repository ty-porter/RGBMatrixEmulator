from RGBMatrixEmulator.internal.emulator_config import RGBMatrixEmulatorConfig
from RGBMatrixEmulator.internal.screen import Screen


class RGBMatrixOptions:
    def __init__(self) -> None:
        self.hardware_mapping: str = "EMULATED"
        self.rows: int = 32
        self.cols: int = 32
        self.chain_length: int = 1
        self.parallel: int = 1
        self.row_address_type: int = 0
        self.multiplexing: int = 0
        self.pwm_bits: int = 0
        self.brightness: int = 100
        self.pwm_lsb_nanoseconds: int = 130
        self.led_rgb_sequence: str = "RGB-EMULATED"
        self.pixel_mapper_config: str = ""
        self.show_refresh_rate: int = 0
        self.gpio_slowdown: int | None = None
        self.disable_hardware_pulsing: bool = False

        emulator_config = RGBMatrixEmulatorConfig()

        self.display_adapter = emulator_config.display_adapter
        self.pixel_style = emulator_config.pixel_style
        self.pixel_glow = emulator_config.pixel_glow
        self.pixel_size = emulator_config.pixel_size
        self.pixel_outline = emulator_config.DEFAULT_CONFIG["pixel_outline"]
        self.pixel_outline = emulator_config.pixel_outline

        # Browser Adapter
        self.browser = emulator_config.browser
        self.emulator_title = emulator_config.emulator_title
        self.icon_path = emulator_config.icon_path

    @property
    def screen(self) -> Screen:
        """The emulated screen model (mapper geometry + render).

        Built lazily and cached, so it snapshots the configured options rather
        than the defaults present at construction time."""
        if not hasattr(self, "_screen"):
            self._screen = Screen(self)

        return self._screen
