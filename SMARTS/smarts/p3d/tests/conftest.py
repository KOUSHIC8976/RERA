             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


def pytest_addoption(parser):
    parser.addoption(
        "--renderer-debug-mode",
        type=str,
        default="warning",
        help="Set to change level of rendering logs: [spam|debug|info|warning|error]",
    )
