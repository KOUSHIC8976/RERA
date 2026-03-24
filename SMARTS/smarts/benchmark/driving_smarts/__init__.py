             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from pathlib import Path
from typing import Any, Dict, Optional

from smarts.core.utils.resources import load_yaml_config as _load_config


def load_config(path: Path) -> Optional[Dict[str, Any]]:
    """Load in a benchmark configuration."""
    if isinstance(path, (str,)):
        path = Path(path)
    return _load_config(path)
