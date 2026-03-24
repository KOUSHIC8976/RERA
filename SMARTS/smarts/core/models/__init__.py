                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import sys
import warnings

import smarts.assets

warnings.warn(
    "The `smarts.core.models` module has been deprecated in favor of `smarts.assets`. Please update your code.",
    category=DeprecationWarning,
)
                                                  
sys.modules[__name__] = smarts.assets
