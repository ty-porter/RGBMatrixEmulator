import argparse, sys

from RGBMatrixEmulator.cli.config import ConfigCLICommand
from RGBMatrixEmulator.logger import Logger


class CLI:
    COMMANDS = {
        # Full commands
        "config": ConfigCLICommand,
        # Aliases
        "c": ConfigCLICommand,
    }

    @staticmethod
    def execute():
        parser = argparse.ArgumentParser(
            description="RGBMatrixEmulator command line interface."
        )
        subparsers = parser.add_subparsers(
            dest="command", required=True, help="Available commands"
        )

        # "config" command
        subparsers.add_parser(
            "config",
            aliases=["c"],
            help="Initialize and manipulate emulator_config.json files",
        )

        args = parser.parse_args()

        if args.command not in CLI.COMMANDS:
            Logger.critical(f"Error: Unknown command '{args.command}'")
            sys.exit(1)

        cmd = CLI.COMMANDS[args.command]
        cmd(args).execute()


def run_cli():
    CLI.execute()
