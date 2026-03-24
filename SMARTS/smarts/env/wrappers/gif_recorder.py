             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import logging
import sys

import gymnasium as gym
import numpy as np

try:
    from moviepy.editor import ImageClip, ImageSequenceClip
except (ImportError, ModuleNotFoundError):
    logging.warning(sys.exc_info())
    logging.warning(
        "You may not have installed the [gym] dependencies required to capture the video. Install them first with the `smarts[gym]` extras."
    )

    raise

import shutil
import time
from pathlib import Path


class GifRecorder:
    """
    Uses images (such as from gym's ``"rgb_array"``) to create a gif file.
    """

    def __init__(self, video_name_folder: str, env: gym.Env):
        timestamp_str = time.strftime("%Y%m%d-%H%M%S")
        self.frame_folder = (
            video_name_folder + "_" + timestamp_str
        )                                                                                                 
        self.env = env

        Path.mkdir(
            Path(self.frame_folder), exist_ok=True
        )                                                       

        self._video_root_path = str(
            Path(video_name_folder).parent
        )                          
        self._video_name = str(Path(video_name_folder).name)                     

    def capture_frame(self, step_num: int, image: np.ndarray):
        """
        Create image according to the ``"rgb_array"`` and store it with step number in the destination folder
        """
        with ImageClip(image) as image_clip:
            image_clip.save_frame(
                f"{self.frame_folder}/{self._video_name}_{step_num}.jpeg"
            )

    def generate_gif(self):
        """
        Use the images in the same folder to create a gif file.
        """
        with ImageSequenceClip(self.frame_folder, fps=10) as clip:
            clip.write_gif(f"{self._video_root_path}/{self._video_name}.gif")
        clip.close()

    def close_recorder(self):
        """
        close the recorder by deleting the image folder.
        """
        shutil.rmtree(self.frame_folder, ignore_errors=True)
