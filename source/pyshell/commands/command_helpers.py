from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_result import CommandResult

def enable_if(result: bool | CommandResult) -> CommandFlags:
    """
    Helper method used to conditionally enable execution of a command.
    @param result Condition that determines whether the command should be
      executed. If this is a boolean, the command will only be run if the
      boolean is True. If this is a `CommandResult`, the command will only be
      run if the command was run and the result is successful.
    @ingroup commands
    """
    if isinstance(result, bool):
        return CommandFlags.STANDARD if result else CommandFlags.INACTIVE
    else:
        return CommandFlags.STANDARD if result.success else CommandFlags.INACTIVE
