                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


class RendererException(Exception):
    """An exception raised if a renderer is required but not available."""

    @classmethod
    def required_to(cls, thing: str) -> "RendererException":
        """Generate a `RenderException` requiring a render to do `thing`."""
        return cls(
            f"""A renderer is required to {thing}. You may not have installed the [camera-obs] dependencies required to render the camera sensor observations. Install them first using the command `pip install -e .[camera-obs]` at the source directory."""
        )


class RayException(Exception):
    """An exception raised if ray package is required but not available."""

    @classmethod
    def required_to(cls, thing):
        """Generate a `RayException` requiring a render to do `thing`."""
        return cls(
            f"""Ray Package is required to {thing}.
               You may not have installed the [rllib] or [train] dependencies required to run the ray dependent example.
               Install them first using the command `pip install -e .[train, rllib]` at the source directory to install the package ray[rllib]==1.0.1.post1"""
        )


class OpenDriveException(Exception):
    """An exception raised if `opendrive` utilities are required but not available."""

    @classmethod
    def required_to(cls, thing):
        """Generate an instance of this exception that describes what can be done to remove the exception"""
        return cls(
            f"""OpenDRIVE Package is required to {thing}.
               You may not have installed the [opendrive] dependencies required to run the OpenDRIVE dependent example.
               Install them first using the command `pip install -e .[opendrive]` at the source directory to install the necessary packages"""
        )
