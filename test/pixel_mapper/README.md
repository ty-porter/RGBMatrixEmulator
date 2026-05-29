# Pixel mapper tests

RGBME generally assumes an upright, rectangular emulated matrix that represents the physical arrangement of one or more daisy-chained physical LED panels.

Pixel mapper tests generate a "golden image" reference that maps panels via a panel ID to show how this arrangement might create the image. `<parallel #>.<panel #>` ID labels are positional. They number each panel by its row and column in the emulated image, not by its place in the physical daisy-chain.

This is in contrast to how `rpi-rgb-led-matrix`'s mappers account for panel wiring (such as a U-mapper bends a chain back on itself or a V-mapper stacks it into columns with `:Z` flippping to alternate panels). On real hardware a given screen position carries a specific chained panel. RGBMatrixEmulator doesn't drive real LEDs or model that wiring. It only reproduces the overall transform from pixel buffer to screen space, such as a change in dimensions or an affine transformation of the pixel buffer. Because of this discrepancy, panel IDs here won't necessarily match what a wired matrix would show. Instead, they describe where a cell lands in the emulated image which is all that is needed for image correctness.
