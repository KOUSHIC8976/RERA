             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from dataclasses import dataclass


@dataclass
class EnvironmentArguments:
    """The base for arguments for an environment."""

    pass


@dataclass(unsafe_hash=True)
class EnvironmentConfiguration:
    """A base environment configuration."""

    id: str
    """The gymnasium registered id of the environment."""
