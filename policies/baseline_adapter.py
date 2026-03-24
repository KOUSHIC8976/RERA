import torch
import numpy as np

class BaselineAVAdapter:
    """
    Phase 4: Cross-Module Coupling Layer.
    Simulates the internal pipeline of an AV (Perception -> Kalman -> PID) 
    to track how external adversarial noise cascades into fatal control saturation.
    """
    def __init__(self, device="cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
                                                  
        self.previous_estimates = None

    def get_actions_and_internals(self, batched_true_obs: torch.Tensor, environmental_stress: float):
        """
        Processes true physics through the AV's simulated internal stack.
        Returns physical actions AND internal module error metrics.
        """
        batch_size = batched_true_obs.shape[0]
        
                                                                               
                                                                               
        perception_noise = torch.randn_like(batched_true_obs) * (0.01 + environmental_stress * 0.1)
        perceived_obs = batched_true_obs + perception_noise
        
                                                  
                                                                                               
        state_drift = torch.norm(perceived_obs - batched_true_obs, dim=1)
        
                                            
                                                                                      
        base_throttle = 0.5
        steering_correction = perceived_obs[:, 1] * 0.1                            
        
        actions = torch.zeros((batch_size, 3), device=self.device)
        actions[:, 0] = base_throttle - (state_drift * 0.05)           
        actions[:, 1] = 0.0        
        actions[:, 2] = steering_correction           
        
                                        
                                                                                                   
                                                
        saturation_flag = (torch.abs(actions[:, 2]) >= 0.95).float()
        
                                 
        actions = torch.clamp(actions, -1.0, 1.0)

                                          
        internal_metrics = {
            "mean_state_drift": state_drift.mean().item(),
            "max_state_drift": state_drift.max().item(),
            "control_saturation_rate": saturation_flag.mean().item()                                  
        }

        return actions.cpu().numpy(), internal_metrics