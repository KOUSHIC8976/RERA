             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from typing import Callable, Optional


def duplicates(iterable, key: Optional[Callable] = None):
    """Finds all values that are duplicates."""
    seen = set()

    matcher = iterable
    if key is not None:
        matcher = map(key, iterable)

    for v, m in zip(iterable, matcher):
        if m in seen:
            yield m, v
        else:
            seen.add(m)
