from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.git.add_command import AddCommand
from pyshell.git.branch_command import BranchCommand
from pyshell.git.commit_command import CommitCommand
from pyshell.git.clone_command import CloneCommand
from pyshell.git.init_command import InitCommand
from pyshell.git.pull_command import PullCommand
from pyshell.git.push_command import PushCommand
from pyshell.git.status_command import StatusCommand
from pyshell.git.switch_command import SwitchCommand
from pyshell.modules.module import IModule
from typing import List, Optional

class Git(IModule):
    """
    Module that provides access to git commands.
    @ingroup modules
    @ingroup git
    """
    @staticmethod
    def add(
        files: str | Path | List[str | Path] = [],
        untracked_only: bool = False,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git add`.
        @param files The file(s) to add.
        @param untracked_only Whether to only add untracked files.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git add`.
        """
        if not isinstance(files, list):
            files = [files]
        return AddCommand(files, untracked_only, cmd_flags)(pyshell)


    @staticmethod
    def branch(
        branch: Optional[str] = None,
        create_branch: bool = False,
        show_current: bool = False,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git branch`.
        @param branch The branch to switch to.
        @param create_branch Whether to create the branch if it doesn't exist.
        @param show_current Whether to show the current branch.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git branch`.
        """
        return BranchCommand(branch, create_branch, show_current, cmd_flags)(
            pyshell
        )


    @staticmethod
    def clone(
        url: str,
        output_directory: Optional[str | Path] = None,
        depth: Optional[int] = None,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git clone`.
        @param url The URL of the repository to clone.
        @param output_directory The directory to clone the repository into.
        @param depth The depth to clone the repository to.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git clone`.
        """
        return CloneCommand(url, output_directory, depth, cmd_flags)(pyshell)


    @staticmethod
    def commit(
        message: str,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git commit`.
        @param message The commit message.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git commit`.
        """
        return CommitCommand(message, cmd_flags)(pyshell)


    @staticmethod
    def init(
        branch_name: Optional[str] = None,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git init`.
        @param branch_name The name to use for the initial branch. If not
          specified, uses the current git version's default branch name.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git init`.
        """
        return InitCommand(branch_name, cmd_flags)(pyshell)


    @staticmethod
    def pull(
        remote: Optional[str] = None,
        branch: Optional[str] = None,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git pull`.
        @param remote The remote to pull from.
        @param branch The branch to pull from the remote.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git pull`.
        """
        return PullCommand(remote, branch, cmd_flags)(pyshell)


    @staticmethod
    def push(
        remote: Optional[str] = None,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git push`.
        @param remote The remote to push to.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git push`.
        """
        return PushCommand(remote, cmd_flags)(pyshell)


    @staticmethod
    def status(
        porcelain: bool = False,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git status`.
        @param porcelain Whether to use porcelain output.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git status`.
        """
        return StatusCommand(porcelain, cmd_flags)(pyshell)


    @staticmethod
    def switch(
        branch: str,
        create_branch: bool = False,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `git switch`.
        @param branch The branch to switch to.
        @param create_branch Whether to attempt to create the branch. If this
          is set to true and the branch already exists, the command will fail.
        @param cmd_flags The flags to set for the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `git switch`.
        """
        return SwitchCommand(branch, create_branch, cmd_flags)(pyshell)
