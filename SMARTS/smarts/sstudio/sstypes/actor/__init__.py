             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    """This is the base description/spec type for traffic actors."""

    name: str
    """The name of the actor. This must be unique."""
