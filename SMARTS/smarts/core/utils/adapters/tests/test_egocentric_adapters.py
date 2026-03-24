             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                                  
                                                                        
                                                                               
                                                                           
               
import numpy as np
import pytest

from smarts.core.controllers import ActionSpaceType
from smarts.core.observations import Observation
from smarts.core.utils.adapters.ego_centric_adapters import (
    ego_centric_observation_adapter,
    get_egocentric_adapters,
)
from smarts.core.utils.tests.fixtures import adapter_data, large_observation


def test_egocentric_observation_adapter(large_observation: Observation):
    new_obs: Observation = ego_centric_observation_adapter(large_observation)
    assert not np.allclose(
        large_observation.ego_vehicle_state.position, new_obs.ego_vehicle_state.position
    )
    assert (
        large_observation.ego_vehicle_state.heading != new_obs.ego_vehicle_state.heading
    )


def _is_same(v1, v2):
    if isinstance(v1, np.ndarray) or isinstance(v2, np.ndarray):
        return np.allclose(v1, v2)
    elif isinstance(v1, (list, tuple)):
        return np.allclose(np.asarray(v1), np.asarray(v2))
    return v1 == v2


def test_adapters(adapter_data, large_observation: Observation):
    for action_space_type, action, expected_action in adapter_data:
        obs_adapter, act_adapter = get_egocentric_adapters(action_space_type)

        _ = obs_adapter(large_observation)
        augmented_action = act_adapter(action)
        print(f"{augmented_action} vs expected {expected_action}")
        assert _is_same(
            augmented_action, expected_action
        ), f"Type: {action_space_type}, base_obs: {large_observation.ego_vehicle_state}"
