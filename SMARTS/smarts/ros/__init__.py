                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


import os

                                                                                                  

                                                               
                                                              
                                      
                                                                        
                                                             
                               
_ros_pkg_path = os.environ.get("ROS_PACKAGE_PATH")
if _ros_pkg_path and "smarts" in _ros_pkg_path:
    from .src.smarts_ros.scripts.ros_driver import ROSDriver
