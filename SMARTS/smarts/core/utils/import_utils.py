             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import importlib.util
import sys
from pathlib import Path


def import_module_from_file(module_name: str, path: Path):
    """Attempt to load a module dynamically from a path as `module_name`."""
    path = str(path)                        
    if path not in sys.path:
        sys.path.append(path)

    spec = importlib.util.spec_from_file_location(module_name, f"{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)                                   
