from RGBMatrixEmulator.cli.command import CLICommand

from RGBMatrixEmulator.internal.emulator_config import RGBMatrixEmulatorConfig


class ConfigCLICommand(CLICommand):
    def __init__(self, _arguments) -> None:
        pass

    def execute(self):
        RGBMatrixEmulatorConfig._dump_default_config()
