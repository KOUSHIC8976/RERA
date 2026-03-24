             

                                                                        

                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          

                                                                            
                                                     

                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os

                                                                                                 
_hashseed = os.getenv("PYTHONHASHSEED")
if _hashseed is None:
    _hashseed = 42
                                                                               
    os.environ["PYTHONHASHSEED"] = f"{_hashseed}"
elif _hashseed == "random":
    import logging

    logging.warning(
        "PYTHONHASHSEED is 'random'. Simulation and generation may be unpredictable."
    )
