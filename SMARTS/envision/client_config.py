             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple


class SingleAttributeOverride(NamedTuple):
    """Options for filtering out attributes."""

    enabled: bool
    """If the stream value is enabled."""
    default: Any
    """The default value for the stream if not enabled."""
    max_count: int = sys.maxsize
    """The maximum number of elements an iterable attribute can contain."""


def _default_override():
    return SingleAttributeOverride(True, None)


@dataclass(frozen=True)
class EnvisionStateFilter:
    """A state filtering tool."""

    actor_data_filter: Dict[str, SingleAttributeOverride]
    """Actor filtering."""
    simulation_data_filter: Dict[str, SingleAttributeOverride]
    """Simulation filtering."""

    @classmethod
    def default(cls):
        """Give a new default filter."""

        return cls(defaultdict(_default_override), defaultdict(_default_override))
