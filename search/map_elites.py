import numpy as np

class MAPElitesArchive:
    """
    State-of-the-Art Quality-Diversity algorithm. 
    Maintains an archive of the "highest risk" scenarios discovered across 
    a discretized grid of macro-conditions, perfectly mapping the phase transition.
    """
    def __init__(self, grid_resolution=20):
        self.res = grid_resolution
                                                                                                      
        self.archive_scores = np.zeros((self.res, self.res)) 
        self.archive_params = np.empty((self.res, self.res), dtype=object)

    def _get_bin(self, density: float, friction: float):
        """Maps continuous parameters [0, 1] to discrete grid bins."""
        x = min(int(density * self.res), self.res - 1)
        y = min(int(friction * self.res), self.res - 1)
        return x, y

    def add_evaluation(self, config: dict, risk_score: float, adv_params: dict):
        """
        Attempts to add a newly simulated scenario to the archive.
        It only enters the archive if it is the MOST dangerous scenario ever seen
        for that specific density/friction combination.
        """
        x, y = self._get_bin(config["traffic_density"], config["env_friction"])
        
        if risk_score > self.archive_scores[x, y]:
            self.archive_scores[x, y] = risk_score
            self.archive_params[x, y] = {
                "macro_config": config,
                "adversarial_human_params": adv_params
            }
            return True                                                       
        return False

    def get_phase_diagram(self):
        """Returns the fully mapped 2D boundary transition matrix."""
        return self.archive_scores