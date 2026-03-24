import torch

class EventDetector:
    """
    Monitors the Risk Amplification Score (RAS) and kinematics to flag 
    and save near-misses and boundary collapse events.
    """
    def __init__(self, ras_threshold=0.85, ttc_threshold=1.5):
        self.ras_threshold = ras_threshold
        self.ttc_threshold = ttc_threshold          
        self.discovered_events = []

    def evaluate_batch(self, step: int, ras_scores: torch.Tensor, min_ttcs: torch.Tensor, infos: tuple):
        """
        Checks a batch of parallel environments for safety boundary violations.
        """
                                                                     
        critical_mask = (ras_scores >= self.ras_threshold) | (min_ttcs <= self.ttc_threshold)
        
        critical_indices = torch.nonzero(critical_mask).squeeze(-1).cpu().numpy()
        
        for idx in critical_indices:
                                                                                 
            env_info = infos[idx]
            
            event_data = {
                "step": step,
                "env_id": idx,
                "ras_score": float(ras_scores[idx].cpu()),
                "ttc": float(min_ttcs[idx].cpu()),
                "scenario_id": env_info.get("scenario_id", "unknown"),
                "ego_position": env_info.get("ego_position", [0,0]),
                "adversary_params": env_info.get("applied_human_params", {})
            }
            
            self.discovered_events.append(event_data)
            
                                                                   
                                                     
            
        return len(critical_indices)