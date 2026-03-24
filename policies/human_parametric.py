import torch

class ParametricHumanDriver:
    """
    Translates continuous actions from the Adversarial RL agent into 
    interpretable, physical driving parameters for the SMARTS simulation.
    """
    def __init__(self, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        
                                                                      
                                                                           
        self.bounds = {
            "reaction_delay": (0.1, 1.5),                
            "aggression_factor": (0.0, 1.0),                                           
            "gap_acceptance": (0.5, 3.0),                                                         
            "lane_change_bias": (-1.0, 1.0),                                        
            "braking_aggressiveness": (1.0, 9.0)                         
        }
        
                                                                 
        self.mins = torch.tensor([b[0] for b in self.bounds.values()], device=self.device)
        self.maxs = torch.tensor([b[1] for b in self.bounds.values()], device=self.device)

    def decode_actions_to_parameters(self, normalized_actions: torch.Tensor) -> dict:
        """
        Maps batched RL actions in range [-1, 1] to physical bounds.
        Args:
            normalized_actions: Tensor of shape (batch_size, 5)
        Returns:
            Dictionary of batched physical parameters to pass to the SMARTS controller.
        """
                                    
        action_01 = (normalized_actions + 1.0) / 2.0
        
                                                                            
        physical_params = self.mins + action_01 * (self.maxs - self.mins)
        
                                                                                
        return {
            "reaction_delay": physical_params[:, 0],
            "aggression_factor": physical_params[:, 1],
            "gap_acceptance": physical_params[:, 2],
            "lane_change_bias": physical_params[:, 3],
            "braking_aggressiveness": physical_params[:, 4]
        }