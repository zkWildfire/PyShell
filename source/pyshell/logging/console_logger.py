from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.logger import ILogger
from pyshell.logging.logger_options import LoggerOptions

class ConsoleLogger(ILogger):
    """
    Logs all commands' output to the console.
    @ingroup logging
    """
    def __init__(self,
        print_cmd_header: bool = False,
        print_cmd_footer: bool = False):
        """
        Creates a new ConsoleLogger.
        @param print_cmd_header Whether to print command info for each command
          that is run before the command's output.
        @param print_cmd_footer Whether to print command info for each command
            that is run after the command's output.
        """
        self._print_cmd_header = print_cmd_header
        self._print_cmd_footer = print_cmd_footer


    def construct_logger(self,
        metadata: CommandMetadata,
        options: LoggerOptions,
        cwd: Path) -> ICommandLogger:
        """
        Constructs a new command logger.
        @param metadata The metadata of the command that will the command logger
          will be used for.
        @param options The options for the command logger.
        @param cwd The current working directory of the command that will the
          command logger will be used for.
        @return A new command logger instance.
        """
        return ConsoleCommandLogger(
            metadata,
            options,
            cwd,
            print_header=self._print_cmd_header,
            print_footer=self._print_cmd_footer
        )
