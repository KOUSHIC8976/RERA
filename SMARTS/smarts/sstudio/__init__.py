                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import os
import sys

from .genscenario import gen_scenario

                                                                                                 
_hashseed = os.getenv("PYTHONHASHSEED")
if _hashseed is None:
    _hashseed = 42
                                                                               
    os.environ["PYTHONHASHSEED"] = f"{_hashseed}"
elif _hashseed == "random":
    import logging

    logging.warning(
        "PYTHONHASHSEED is 'random'. Simulation and generation may be unpredictable."
    )

from . import sstypes as types

sys.modules[f"{__name__}.{types=}".partition("=")[0]] = types
