             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from dataclasses import dataclass

from smarts.sstudio.sstypes.actor.traffic_actor import TrafficActor


@dataclass(frozen=True)
class TrafficEngineActor(TrafficActor):
    """This represents an actor that should be controlled by a traffic simulator."""

    traffic_provider: str = "LocalTrafficProvider"
    """The traffic provider that the actor is intended to be handed over to."""
