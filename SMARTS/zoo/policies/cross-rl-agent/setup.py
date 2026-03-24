                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
                                                              

from cross_rl_agent.version import VERSION
from setuptools import setup

setup(
    name="cross-rl-agent",
    description="cross rl agent example",
    version=VERSION,
    packages=[
        "cross_rl_agent",
    ],
    include_package_data=True,
    install_requires=[
        "tensorflow==2.2.1",
        "smarts==0.7.0rc0",
    ],
)
