import torch

class RiskMetricEngine:
    """
    Computes the Risk Amplification Score (RAS) using highly optimized
    PyTorch tensor operations on the GPU.
    """
    def __init__(self, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        
                                                     
        self.w_ttc = 1.5                                    
        self.w_dist = 1.0                              
        self.w_jerk = 0.5                              

    def calculate_ras(self, positions: torch.Tensor, velocities: torch.Tensor, accelerations: torch.Tensor) -> torch.Tensor:
        """
        Calculates the RAS for a batch of vehicles.
        Args:
            positions: Tensor of shape (batch, num_vehicles, 2)
            velocities: Tensor of shape (batch, num_vehicles, 2)
            accelerations: Tensor of shape (batch, num_vehicles, 2)
        Returns:
            RAS Tensor of shape (batch,)
        """
                                                                         
                                                                                   
        diff_pos = positions.unsqueeze(2) - positions.unsqueeze(1)
        distances = torch.norm(diff_pos, dim=-1)
        
                                            
        mask = torch.eye(distances.shape[1], device=self.device).bool()
        distances.masked_fill_(mask, float('inf'))
        min_distances, _ = torch.min(distances, dim=-1)
        
                                                  
                                                                   
        diff_vel = velocities.unsqueeze(2) - velocities.unsqueeze(1)
        
                                                      
        dot_product = torch.sum(diff_pos * diff_vel, dim=-1)
        
                                                                            
        approaching_mask = dot_product < 0
        
                                           
        ttc = torch.full_like(distances, float('inf'))
        ttc[approaching_mask] = - (distances[approaching_mask] ** 2) / dot_product[approaching_mask]
        min_ttc, _ = torch.min(ttc, dim=-1)

                                                      
                                                                             
                                                                                       
        braking = torch.clamp(accelerations[..., 0], max=0.0)                        
        jerk_proxy = torch.abs(braking)

                                
                                                                                                
                                                  
        eps = 1e-6
        
        risk_dist = 1.0 / (min_distances + eps)
        risk_ttc = 1.0 / (min_ttc + eps)
        risk_jerk = jerk_proxy

                                                                  
        scenario_ras = torch.mean(
            (self.w_dist * risk_dist) + 
            (self.w_ttc * risk_ttc) + 
            (self.w_jerk * risk_jerk), 
            dim=1
        )

        return scenario_ras

    def calculate_systemic_instability(self, velocities: torch.Tensor, accelerations: torch.Tensor) -> torch.Tensor:
        """
        Phase 3 Feature: Detects traffic shockwaves and cascading failures 
        across the entire simulated environment, not just near the Ego vehicle.
        
        Args:
            velocities: Tensor of shape (batch, num_vehicles, 2)
            accelerations: Tensor of shape (batch, num_vehicles, 2)
        Returns:
            Systemic Instability Score Tensor of shape (batch,)
        """
                                                                                    
                                   
        speeds = torch.norm(velocities, dim=-1)
        speed_variance = torch.var(speeds, dim=1)
        
                                            
                                                                                       
        forward_accels = accelerations[..., 0]                                 
        braking_events = torch.clamp(forward_accels, max=0.0)
        
                                                       
                                                       
        total_systemic_braking = torch.abs(torch.sum(braking_events, dim=1))
        
                                       
                                                                   
        instability_score = (speed_variance * 0.5) + (total_systemic_braking * 0.5)
        
        return instability_score
    def calculate_systemic_graph_instability(self, positions: torch.Tensor, velocities: torch.Tensor) -> torch.Tensor:
        """
        Phase 3 SOTA Feature: Computes the Spectral Radius of the Spatio-Temporal 
        Interaction Graph to detect cascading shockwaves and systemic collapse.
        """
        batch_size, num_vehicles, _ = positions.shape
        eps = 1e-6
        
                                                   
                                                                         
        diff_pos = positions.unsqueeze(2) - positions.unsqueeze(1)
        distances = torch.norm(diff_pos, dim=-1)
        
                                                                 
                                        
        adjacency_matrix = torch.exp(-distances / 10.0) 
        
                                          
        mask = torch.eye(num_vehicles, device=self.device).bool().unsqueeze(0).expand(batch_size, -1, -1)
        adjacency_matrix.masked_fill_(mask, 0.0)
        
                                                 
        diff_vel = velocities.unsqueeze(2) - velocities.unsqueeze(1)
        relative_speeds = torch.norm(diff_vel, dim=-1)
        
                                                         
                                                                                         
        propagation_matrix = adjacency_matrix * relative_speeds
        
                                                                           
                                                                           
                                                                                       
                                                                                           
        systemic_instability = torch.linalg.matrix_norm(propagation_matrix, ord=2, dim=(1, 2))
        
        return systemic_instability