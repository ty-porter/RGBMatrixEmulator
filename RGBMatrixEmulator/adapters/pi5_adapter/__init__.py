from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.logger import Logger

import sys
from pathlib import Path
import numpy as np


class Pi5Adapter(BaseAdapter):
    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.matrix = None
        self.framebuffer = None
        self.pixel_swizzle = None

        self.__ensure_pi5_runtime()

    def load_emulator_window(self):
        config = self.options.pi5

        # Validate n_planes
        if config.n_planes > 10:
            config.n_planes = 10
        elif config.n_planes < 1:
            Logger.warning(
                f"n_planes must be at least 1. Got {config.n_planes}, setting to 1."
            )
            config.n_planes = 1

        # Validate n_temporal_planes
        valid_temporal = [0, 2, 4]
        if config.n_temporal_planes not in valid_temporal:
            closest = min(
                valid_temporal, key=lambda x: abs(x - config.n_temporal_planes)
            )
            Logger.warning(
                f"Invalid n_temporal_planes {config.n_temporal_planes}. "
                f"Snapping to closest valid value: {closest}."
            )
            config.n_temporal_planes = closest

        if config.n_temporal_planes > config.n_planes:
            # Find max valid value <= n_planes
            new_val = max(
                [v for v in valid_temporal if v <= config.n_planes], default=0
            )
            Logger.warning(
                f"n_temporal_planes ({config.n_temporal_planes}) cannot be greater than n_planes ({config.n_planes}). "
                f"Reducing to {new_val}."
            )
            config.n_temporal_planes = new_val

        if config.n_addr_lines == 5 and self.height < 64:
            Logger.critical(
                f"n_addr_lines=5 requires a display height of at least 64 pixels. Current height: {self.height}"
            )
            sys.exit(1)

        # Configure Geometry
        pinout_str = config.pinout

        # Handle LED Sequence (RGB vs BGR vs Other)
        # Check if BGR is requested and if there is a BGR pinout variant
        sequence = config.led_rgb_sequence.upper()

        if sequence == "BGR":
            # Attempt to find the BGR variant of the pinout
            # Typical naming convention: AdafruitMatrixBonnet -> AdafruitMatrixBonnetBGR
            bgr_pinout_str = f"{pinout_str}BGR"
            if hasattr(piomatter.Pinout, bgr_pinout_str):
                pinout_str = bgr_pinout_str
                # Handled by hardware/pinout, so we don't need to software swizzle
                sequence = "RGB"  # Treat as normal for rest of pipeline
            else:
                Logger.warning(
                    f"BGR Sequence requested but pinout '{bgr_pinout_str}' not found in piomatter.Pinout. Will attempt software pixel swap."
                )

        # Resolve Pinout Enum
        if hasattr(piomatter.Pinout, pinout_str):
            pinout = getattr(piomatter.Pinout, pinout_str)
        else:
            Logger.warning(
                f"Pinout '{pinout_str}' not found in piomatter.Pinout. Defaulting to AdafruitMatrixBonnet."
            )
            pinout = piomatter.Pinout.AdafruitMatrixBonnet

        # Setup Software Swizzle if needed
        # We need to map RGB (original) to Dest Sequence
        # Common cases: RGB (0,1,2), RBG (0,2,1), GRB (1,0,2), GBR (1,2,0), BRG (2,0,1), BGR (2,1,0)
        # Note: If we handled BGR via pinout, sequence is set to "RGB" above so we skip this.
        if sequence != "RGB":
            swizzle_map = {
                "RGB": [0, 1, 2],
                "RBG": [0, 2, 1],
                "GRB": [1, 0, 2],
                "GBR": [1, 2, 0],
                "BRG": [2, 0, 1],
                "BGR": [2, 1, 0],
            }

            if sequence in swizzle_map:
                self.pixel_swizzle = swizzle_map[sequence]
                Logger.info(
                    f"Using software pixel swizzle for sequence '{sequence}': {self.pixel_swizzle}"
                )
            else:
                Logger.warning(
                    f"Unknown LED sequence '{sequence}'. Display colors may be incorrect."
                )

        rotation_str = config.rotation
        if hasattr(piomatter.Orientation, rotation_str):
            rotation = getattr(piomatter.Orientation, rotation_str)
        else:
            Logger.warning(
                f"Rotation '{rotation_str}' not found in piomatter.Orientation. Defaulting to Normal."
            )
            rotation = piomatter.Orientation.Normal

        if "Active3" not in pinout_str and config.n_lanes > 2:
            Logger.warning(
                f"Pinout '{pinout_str}' does not support multiple lanes. "
                "Setting n_lanes to 2."
            )
            config.n_lanes = 2

        if config.n_lanes == 2 and "Active3" not in pinout_str:
            # Simple Geometry
            geometry = piomatter.Geometry(
                width=self.width,
                height=self.height,
                n_planes=config.n_planes,
                n_addr_lines=config.n_addr_lines,
                n_temporal_planes=config.n_temporal_planes,
                rotation=rotation,
            )
        else:
            if config.n_lanes < 2:
                Logger.warning(
                    f"Active3 pinouts require n_lanes >= 2. Got {config.n_lanes}, setting to 2."
                )
                config.n_lanes = 2

            pixelmap = None
            if config.n_lanes > 1 or "Active3" in pinout_str:
                try:
                    from adafruit_blinka_raspberry_pi5_piomatter.pixelmappers import (
                        simple_multilane_mapper,
                    )

                    pixelmap = simple_multilane_mapper(
                        self.width, self.height, config.n_addr_lines, config.n_lanes
                    )
                except ImportError:
                    Logger.warning(
                        "Could not import simple_multilane_mapper. Active3/Multilane support may fail."
                    )

            geometry = piomatter.Geometry(
                width=self.width,
                height=self.height,
                n_addr_lines=config.n_addr_lines,
                n_planes=config.n_planes,
                n_temporal_planes=config.n_temporal_planes,
                n_lanes=config.n_lanes,
                map=pixelmap,
            )

        self.framebuffer = np.zeros(
            shape=(geometry.height, geometry.width, 3), dtype=np.uint8
        )

        self.matrix = piomatter.PioMatter(
            colorspace=piomatter.Colorspace.RGB888Packed,
            pinout=pinout,
            framebuffer=self.framebuffer,
            geometry=geometry,
        )

        # Register cleanup to clear the screen on exit
        import atexit

        def cleanup():
            if self.framebuffer is not None and self.matrix is not None:
                self.framebuffer.fill(0)
                self.matrix.show()
                # Deinit if possible, though show() with 0s might be enough
                # self.matrix.deinit() # PioMatter object might not support deinit or it's automatic on GC

        atexit.register(cleanup)

        self.loaded = True

    def draw_to_screen(self, pixels):
        if not self.loaded:
            return

        # pixels is (height, width, 3)
        try:
            pixel_data = np.array(pixels, dtype=np.uint8)

            # Apply software swizzle if configured
            if self.pixel_swizzle:
                pixel_data = pixel_data[:, :, self.pixel_swizzle]

            np.copyto(self.framebuffer, pixel_data)
            self.matrix.show()
        except Exception as e:
            # Throttle logging?
            pass

    def __ensure_pi5_runtime(self):
        """
        Validates that the code is running on a Raspberry Pi 5
        and has the necessary dependencies installed.
        """
        is_pi5 = False
        try:
            model_path = Path("/proc/device-tree/model")
            if model_path.exists():
                model_name = model_path.read_text().strip()
                if "Raspberry Pi 5" in model_name:
                    is_pi5 = True
        except Exception:
            pass

        if not is_pi5:
            Logger.critical(
                "This module is designed exclusively for the Raspberry Pi 5."
            )
            sys.exit(1)

        try:
            import adafruit_blinka_raspberry_pi5_piomatter as piomatter
        except ImportError:
            Logger.critical(
                "Pi5 adapter cannot load due to missing dependencies for Raspberry Pi 5.\n"
                "Please install dependencies using the [pi5] feature option:\n"
                "    pip install RGBMatrixEmulator[pi5]"
            )
            sys.exit(1)
