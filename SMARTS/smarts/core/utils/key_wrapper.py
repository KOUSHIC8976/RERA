             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
              
from typing import Sequence


class KeyWrapper(Sequence):
    """A sequence that transforms the selected in an underlying sequence using the given
    transformation key."""

    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i: int):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

    def insert(self, index: int, item):
        """Insert an item into the sequence."""
        self.it.insert(index, item)
