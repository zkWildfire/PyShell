from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List

class AddCommand(ExternalCommand):
    """
    Defines a command that runs `git add`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        files: List[str | Path] = [],
        untracked_only: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param files List of files to add. If empty, all files will be added.
        @param untracked_only Whether to only add untracked files.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["add"]
        if untracked_only:
            args.append("-u")

        for file in files:
            args.append(str(file))
        else:
            args.append(".")

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
