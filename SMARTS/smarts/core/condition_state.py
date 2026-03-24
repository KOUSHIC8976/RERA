             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from enum import IntFlag


class ConditionState(IntFlag):
    """Represents the state of a condition."""

    FALSE = 0
    """This condition is false."""
    BEFORE = 1
    """This condition is false and never evaluated true before."""
    EXPIRED = 2
    """This condition is false and will never evaluate true."""
    TRUE = 4
    """This condition is true."""

    def __bool__(self) -> bool:
        return self.TRUE in self
