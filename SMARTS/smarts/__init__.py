                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

try:
    from importlib.metadata import version

    VERSION = version("smarts")
except:
                                                                                      
    import pkg_resources

                                                    
    VERSION = pkg_resources.get_distribution("smarts").version
