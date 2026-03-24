             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Set, Tuple

from smarts.core.sensor import CustomRenderSensor
from smarts.core.sensors import SensorResolver, Sensors, SensorState
from smarts.core.utils.core_logging import timeit
from smarts.core.utils.file import replace

if TYPE_CHECKING:
    from smarts.core.observations import Observation
    from smarts.core.renderer_base import RendererBase
    from smarts.core.sensor import Sensor
    from smarts.core.simulation_frame import SimulationFrame
    from smarts.core.simulation_local_constants import SimulationLocalConstants
    from smarts.core.utils.pybullet import bullet_client as bc


logger = logging.getLogger(__name__)


class LocalSensorResolver(SensorResolver):
    """This implementation of the sensor resolver completes observations serially."""

    def observe(
        self,
        sim_frame: SimulationFrame,
        sim_local_constants: SimulationLocalConstants,
        agent_ids: Set[str],
        renderer: Optional[RendererBase],
        bullet_client: bc.BulletClient,
    ) -> Tuple[Dict[str, Observation], Dict[str, bool], Dict[str, Dict[str, Sensor]]]:
                                   
                                   
                                                
                                                   
                                      
                                          
                
                                    
               
                
                                   
                                                   
                                    
                                      
        observations, dones, updated_sensors = self._gen_serialized_obs(
            sim_frame, sim_local_constants, agent_ids
        )
        phys_observations = self._gen_phys_observations(
            sim_frame, sim_local_constants, agent_ids, bullet_client, updated_sensors
        )

                                          
        for agent_id, p_obs in phys_observations.items():
            observations[agent_id] = replace(observations[agent_id], **p_obs)

        self._sync_custom_camera_sensors(sim_frame, renderer, observations)

        if renderer:
            renderer.render()

        rendering_observations = self._gen_rendered_observations(
            sim_frame, sim_local_constants, agent_ids, renderer, updated_sensors
        )

                                  
        for agent_id, r_obs in rendering_observations.items():
            observations[agent_id] = replace(observations[agent_id], **r_obs)

        return observations, dones, updated_sensors

    def _gen_serialized_obs(self, sim_frame, sim_local_constants, agent_ids):
        with timeit("serial run", logger.debug):
            (
                observations,
                dones,
                updated_sensors,
            ) = Sensors.observe_serializable_sensor_batch(
                sim_frame,
                sim_local_constants,
                agent_ids,
            )

        return observations, dones, updated_sensors

    def step(self, sim_frame: SimulationFrame, sensor_states: Iterable[SensorState]):
        """Step the sensor state."""
        for sensor_state in sensor_states:
            sensor_state.step()
