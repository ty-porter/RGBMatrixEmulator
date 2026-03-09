class CLICommand:
    """
    Abstract base class for CLI commands.
    """

    def execute(self) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
