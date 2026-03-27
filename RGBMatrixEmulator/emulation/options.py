from RGBMatrixEmulator.internal.emulator_config import RGBMatrixEmulatorConfig


class RGBMatrixOptions:
    def __init__(self) -> None:
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

        # Pi5 Adapter
        self.pi5 = emulator_config.pi5

    def window_size(self) -> tuple[int, int]:
        return (
            self.cols * self.pixel_size * self.chain_length,
            self.rows * self.pixel_size * self.parallel,
        )

    def window_size_str(self, pixel_text: str = "") -> str:
        width, height = self.window_size()

        return f"{width} x {height} {pixel_text}"
