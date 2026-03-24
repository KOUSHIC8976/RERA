                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

try:
    from gymnasium.envs.registration import register

    register(
        id="hiway-v1",
        entry_point="smarts.env.gymnasium.hiway_env_v1:HiWayEnvV1",
        disable_env_checker=True,
    )

    register(
        id="driving-smarts-v2022",
        entry_point="smarts.env.gymnasium.driving_smarts_2022_env:driving_smarts_2022_env",
        disable_env_checker=True,
    )

    register(
        id="platoon-v0",
        entry_point="smarts.env.gymnasium.platoon_env:platoon_env",
        disable_env_checker=True,
    )

    register(
        id="driving-smarts-v2023",
        entry_point="smarts.env.gymnasium.driving_smarts_2023_env:driving_smarts_2023_env",
        disable_env_checker=True,
    )


except ModuleNotFoundError:
    import warnings

    warnings.warn(
        "Gymnasium cannot be imported likely due to numpy version compatibility `numpy>=1.21.0`. "
        "Gymnasium environments will be unavailable. Gymnasium imports may cause a crash."
    )
