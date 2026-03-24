                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
                      
                                                                                          
                                                            
import importlib
import re
import warnings
from typing import Dict

                                          
NAME_CONSTRAINT_REGEX = re.compile(r"^(?:[\w:-]+\/)?([\w:.-]+)-(v(\d+)|latest)$")


def is_valid_locator(locator: str):
    """Validate the given locator."""
                                                      
    return NAME_CONSTRAINT_REGEX.search(locator)


def find_attribute_spec(name):
    """Finds the attribute specification from a reachable module.
    Args:
        name:
            The module and attribute name (i.e. smarts.core.lidar:Lidar, ...)
    """
    module_name, attribute_name = name.split(":")
    module = importlib.import_module(module_name)
    attribute_spec = getattr(module, attribute_name)
    return attribute_spec


class ClassFactory:
    """A named factory that can preconfigure generation of objects."""

    def __init__(self, name, entrypoint=None, **kwargs):
        self.name = name
        self.entrypoint = entrypoint
        self._kwargs = kwargs

        if self.entrypoint is None:
            raise EnvironmentError(
                f"Entry-point is empty for: '{self.name}'. Provide an entry-point"
            )

    def make(self, **kwargs):
        """Provides an object from the entrypoint. Overriding predefined keyword arguments with
        the given keyword arguments.
        """
        if self.entrypoint is None:
            raise AttributeError(f"Entry-point does not exist for name `{self.name}`")
        _kwargs = self._kwargs.copy()
        _kwargs.update(kwargs)
        if callable(self.entrypoint):
            instance = self.entrypoint(**_kwargs)
        else:
            type_spec = find_attribute_spec(self.entrypoint)
            instance = type_spec(**_kwargs)

        return instance

    def __repr__(self):
        return f"""ClassFactory(
  name={self.name},
  entrypoint={self.entrypoint},
  kwargs={self._kwargs},
)"""


class ClassRegister:
    """A listing of key named class factories."""

    def __init__(self):
        self.index: Dict[str, ClassFactory] = {}

    def register(self, name, entry_point=None, **kwargs):
        """Registers a new factory with the given locator as the key.
        Args:
            locator: The key value of the factory.
            entry_point: The factory method.
            kwargs: Predefined arguments to the factory method.
        """

        if name in self.index:
            warnings.warn(
                f"Resident named '{name}' was already registered. Overwriting existing registration."
            )
        self.index[name] = ClassFactory(name, entry_point, **kwargs)

    def find_factory(self, locator):
        """Locates a factory given a locator."""
        self._raise_on_invalid_locator(locator)

        mod_name, _, name = locator.partition(":")
        if name != "":
                                          
            try:
                                                                                      
                                                                                                         
                module = importlib.import_module(mod_name)
            except ImportError as exc:
                import sys

                raise ImportError(
                    f"Ensure that `{mod_name}` module can be found from your "
                    f"PYTHONPATH and name=`{locator}` exists (e.g. was registered "
                    "manually or downloaded).\n"
                    f"`PYTHONPATH`: `{sys.path}`"
                ) from exc
        else:
                                           
            name = mod_name

        try:
                                                  
                                              
            return self.index[name]
        except KeyError as exc:
            raise NameError(f"Locator not registered in lookup: {locator}") from exc

    def make(self, locator, **kwargs):
        """Calls the factory with `locator` name key supplying the keyword arguments as argument
        overrides.
        """
        factory = self.find_factory(locator)
        instance = factory.make(**kwargs)
        return instance

    def all(self):
        """Lists all available factory objects."""
        return self.index.values()

    def __repr__(self) -> str:
        columns = 3
        max_justify = float("-inf")
        for name in self.index.keys():
            max_justify = max(max_justify, len(name))

        out = ""
        for i, name in enumerate(self.index.keys()):
            out = f"{out}{name.ljust(max_justify)} "
            if i % columns == 0 and len(self.index) != i + 1:
                out += "\n"
        out += "\n"

        return out

    def _raise_on_invalid_locator(self, locator: str):
        if not is_valid_locator(locator):
                                                                            
            raise ValueError(
                f"Cannot register invalid locator={locator}. E.g. syntax: "
                '"module:name-v0".'
            )
