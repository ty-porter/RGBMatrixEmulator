from RGBMatrixEmulator.display_adapters.pygame import Pygame
from RGBMatrixEmulator.display_adapters.terminal import Terminal

DISPLAY_ADAPTER_TYPES = {
    'pygame':   Pygame,
    'terminal': Terminal
}