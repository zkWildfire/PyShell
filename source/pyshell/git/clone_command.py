from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List, Optional

class CloneCommand(ExternalCommand):
    """
    Defines a command that runs `git clone`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        url: str,
        output_directory: Optional[str | Path] = None,
        depth: Optional[int] = None,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param url The URL to clone from.
        @param output_directory The directory to clone into.
        @param depth The depth to clone.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["clone"]
        if depth:
            args.append("--depth")
            args.append(str(depth))
        args.append(url)
        if output_directory:
            args.append(str(output_directory))

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
