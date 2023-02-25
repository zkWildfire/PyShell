import os
from pathlib import Path
import platform

class PlatformStatics:
    """
    Defines static methods that abstract away platform-specific functionality.
    """
    @staticmethod
    def is_linux() -> bool:
        """
        Returns whether the current platform is Linux.
        @return Whether the current platform is Linux.
        """
        return platform.system() == "Linux"


    @staticmethod
    def is_windows() -> bool:
        """
        Returns whether the current platform is Windows.
        @return Whether the current platform is Windows.
        """
        return platform.system() == "Windows"


    @staticmethod
    def resolve_using_path(filename: str) -> Path:
        """
        Finds the path of the specified file using the system path.
        @param filename The filename to resolve.
        @throws ValueError if the file could not be found.
        @return The absolute path to the specified file.
        """
        for path in os.environ["PATH"].split(os.pathsep):
            exe_path = Path(path).joinpath(filename)
            if os.path.isfile(exe_path):
                return exe_path

        raise ValueError(
            f"Could not find a file with name '{filename}' on the PATH."
        )


    @staticmethod
    def to_executable_name(name: str) -> str:
        """
        Converts the specified name to an executable name.
        @param name The name to convert. Should not include the file extension.
        @return The executable name.
        """
        if PlatformStatics.is_windows():
            return name + ".exe"
        return name
