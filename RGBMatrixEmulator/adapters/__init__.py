ADAPTERS = {
    "browser": {
        "path": "RGBMatrixEmulator.adapters.browser_adapter.adapter",
        "class": "BrowserAdapter",
        "fallback": True,
    },
    "pygame": {
        "path": "RGBMatrixEmulator.adapters.pygame_adapter",
        "class": "PygameAdapter",
        "fallback": True,
    },
    "sixel": {
        "path": "RGBMatrixEmulator.adapters.sixel_adapter",
        "class": "SixelAdapter",
        "fallback": True,
    },
    "terminal": {
        "path": "RGBMatrixEmulator.adapters.terminal_adapter",
        "class": "TerminalAdapter",
        "fallback": True,
    },
    "tkinter": {
        "path": "RGBMatrixEmulator.adapters.tkinter_adapter",
        "class": "TkinterAdapter",
        "fallback": True,
    },
    "turtle": {
        "path": "RGBMatrixEmulator.adapters.turtle_adapter",
        "class": "TurtleAdapter",
        "fallback": True,
    },
    "raw": {
        "path": "RGBMatrixEmulator.adapters.raw_adapter",
        "class": "RawAdapter",
        "fallback": False,
    },
    "pi5": {
        "path": "RGBMatrixEmulator.adapters.pi5_adapter",
        "class": "Pi5Adapter",
        "fallback": False,
    },
}
