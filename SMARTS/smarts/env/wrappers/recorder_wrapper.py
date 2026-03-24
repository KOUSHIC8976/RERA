             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os
from pathlib import Path

import gymnasium as gym

from smarts.env.wrappers.gif_recorder import GifRecorder


class RecorderWrapper(gym.Wrapper):
    """
    A Wrapper that interacts the gym environment with the GifRecorder to record video step by step.
    """

    def __init__(self, video_name: str, env: gym.Env):

        root_path = Path(__file__).parents[3]                         
        video_folder = os.path.join(
            root_path, "videos"
        )                                                    
        Path.mkdir(
            Path(video_folder), exist_ok=True
        )                                    

        super().__init__(env)
        self.video_name_folder = os.path.join(
            video_folder, video_name
        )                                                                                                                                                            
        self.gif_recorder = None
        self.recording = False
        self.current_frame = -1

    def reset(self, **kwargs):
        """
        Reset the gym environment and restart recording.
        """
        observations = super().reset(**kwargs)
        if self.recording == False:
            self.start_recording()

        return observations

    def start_recording(self):
        """
        Start the gif recorder and capture the first frame.
        """
        if self.gif_recorder is None:
            self.gif_recorder = GifRecorder(self.video_name_folder, self.env)
        image = super().render(mode="rgb_array")
        self.gif_recorder.capture_frame(self.next_frame_id(), image)
        self.recording = True

    def stop_recording(self):
        """
        Stop recording.
        """
        self.recording = False

    def step(self, action):
        """
        Step the environment using the action and record the next frame.
        """
        observations, rewards, dones, infos = super().step(action)
        if self.recording == True:
            image = super().render(mode="rgb_array")
            self.gif_recorder.capture_frame(self.next_frame_id(), image)

        return observations, rewards, dones, infos

    def next_frame_id(self):
        """
        Get the id for next frame.
        """
        self.current_frame += 1
        return self.current_frame

    def close(self):
        """
        Close the recorder by deleting the image folder and generate the gif file.
        """
        if self.gif_recorder is not None:
            self.gif_recorder.generate_gif()
            self.gif_recorder.close_recorder()
            self.gif_recorder = None
            self.recording = False

    def __del__(self):
        self.close()
