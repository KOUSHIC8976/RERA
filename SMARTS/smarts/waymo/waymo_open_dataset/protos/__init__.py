                                                                     
 
                                                                 
                                                                  
                                         
 
                                                
 
                                                                     
                                                                   
                                                                          
                                                                     
                                
                                                                                

try:
    import google.protobuf
except:
    raise ImportError(
        "Missing dependencies for Waymo. Install them using the command `pip install -e .[waymo]` at the source directory."
    )
