                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
import base64
import glob
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import Dict

import cv2
import numpy as np
from PIL import Image

from smarts.core.utils.core_logging import isnotebook


def flatten_obs(sim_obs):
    """Convert the observation into tuples of observations (for purposes of flattening boids)."""
    obs = []
    for agent_id, agent_obs in sim_obs.items():
        if agent_obs is None:
            continue
        elif isinstance(agent_obs, dict):                 
            for vehicle_id, vehicle_obs in agent_obs.items():
                obs.append((vehicle_id, vehicle_obs))
        else:
            obs.append((agent_id, agent_obs))
    return obs


def vis_sim_obs(sim_obs) -> Dict[str, np.ndarray]:
    """Convert the observations into format for mp4 video output."""
    vis_images = defaultdict(list)

    for agent_id, agent_obs in flatten_obs(sim_obs):
        drivable_area = getattr(agent_obs, "drivable_area_grid_map", None)
        if drivable_area is not None:
            image = drivable_area.data
            image = image[:, :, [0, 0, 0]]
            image = image.astype(np.uint8)
            vis_images[f"{agent_id}-DrivableAreaGridMap"].append(image)

        ogm = getattr(agent_obs, "occupancy_grid_map", None)
        if ogm is not None:
            image: np.ndarray = ogm.data
            image = image[:, :, [0, 0, 0]]
            image = image.astype(np.uint8)
            vis_images[f"{agent_id}-OGM"].append(image)

        rgb = getattr(agent_obs, "top_down_rgb", None)
        if rgb is not None:
            image = rgb.data
            image = image.astype(np.uint8)
            vis_images[f"{agent_id}-Top-Down-RGB"].append(image)

    return {key: np.array(images) for key, images in vis_images.items()}


def show_notebook_videos(path="videos", height="400px", split_html=""):
    """Render a video in a python display. Usually for jupyter notebooks."""
    if not isnotebook():
        return
    from IPython import display as ipythondisplay

    html = []
    for mp4 in Path(path).glob("*.mp4"):
        video_b64 = base64.b64encode(mp4.read_bytes())
        html.append(
            """<video alt="{}" autoplay
                      loop controls style="height: {};">
                      <source src="data:video/mp4;base64,{}" type="video/mp4" />
                 </video>""".format(
                mp4, height, video_b64.decode("ascii")
            )
        )
    ipythondisplay.display(ipythondisplay.HTML(data=split_html.join(html)))
