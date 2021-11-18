from RGBMatrixEmulator.adapters.pygame import Pygame
from RGBMatrixEmulator.adapters.terminal import Terminal
from RGBMatrixEmulator.adapters.turtle import Turtle

ADAPTER_TYPES = {
    'pygame':   Pygame,
    'terminal': Terminal,
    'turtle':   Turtle
}