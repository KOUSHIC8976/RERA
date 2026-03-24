             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass

from smarts.sstudio.sstypes.constants import MAX


@dataclass(frozen=True)
class BubbleLimits:
    """Defines the capture limits of a bubble."""

    hijack_limit: int = MAX
    """The maximum number of vehicles the bubble can hijack"""
    shadow_limit: int = MAX
    """The maximum number of vehicles the bubble can shadow"""

    def __post_init__(self):
        if self.shadow_limit is None:
            raise ValueError("Shadow limit must be a non-negative real number")
        if self.hijack_limit is None or self.shadow_limit < self.hijack_limit:
            raise ValueError("Shadow limit must be >= hijack limit")
