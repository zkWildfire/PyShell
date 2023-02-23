from abc import ABC

class IModule(ABC):
    """
    Represents a module that can be loaded by Nautilus scripts.
    Modules typically represent an executable which Nautilus scripts will invoke
      via `ICommand` instances. For complex modules that support multiple
      different types of commands, the module will define multiple methods that
      return `ICommand` instances.
    """
