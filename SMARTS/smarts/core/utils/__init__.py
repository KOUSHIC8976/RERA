                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import sys

from . import core_logging as logging
from . import core_math as math

sys.modules[f"{__name__}.{math=}".partition("=")[0]] = math
sys.modules[f"{__name__}.{logging=}".partition("=")[0]] = logging
