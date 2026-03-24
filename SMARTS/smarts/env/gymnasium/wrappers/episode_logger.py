                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
from typing import Any, Dict, Iterator, Tuple

import gymnasium as gym

from smarts.core.utils.episodes import EpisodeLog, EpisodeLogs

Action = Any


class EpisodeLogger(gym.Wrapper):
    """Wraps a gym environment with simple episode logging capabilities."""

    def __init__(self, env: gym.Env, col_width: int = 18):
        super(EpisodeLogger, self).__init__(env)
        self._current_episode = None
        self._closed = False
        self._log_iter = self._episode_logs(col_width)

    def step(self, action: Action):
        """Mark a step for logging."""
        step_vals = super().step(action)
        self._current_episode.record_step(*step_vals)
        return step_vals

    def reset(self) -> Tuple[Any, Dict[str, Any]]:
        """Mark an episode reset for logging."""

        out = super().reset()
        self._current_episode: EpisodeLog = next(self._log_iter)
        self._current_episode.record_scenario(self.scenario_log)
        return out

    def close(self):
        """Cap off the episode logging."""

        self._closed = True
        try:
            next(self._log_iter)
        except:
            pass
        return super().close()

    def _episode_logs(self, col_width) -> Iterator[EpisodeLog]:
        with EpisodeLogs(col_width) as episode_logs:
            while not self._closed:
                yield episode_logs.reset()
            episode_logs.reset()
