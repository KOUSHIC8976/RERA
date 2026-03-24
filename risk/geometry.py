import torch
import numpy as np

class BoundaryGeometryExtractor:
    """
    Phase 3: Mathematical Differentiation Layer.
    Extracts the topological properties of the safety boundary.
    """
    def __init__(self, surrogate, device="cuda"):                                              
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.surrogate = surrogate
        
    def evaluate_epsilon_neighborhood(self, base_config_tensor: torch.Tensor, epsilon=0.05, num_samples=100):
        """
        Calculates Variance Explosion in an ε-neighborhood.
        """
        self.surrogate.model.eval()
        with torch.no_grad():
                                          
            noise = (torch.rand((num_samples, 3), device=self.device) * 2 - 1) * epsilon
            neighborhood_configs = torch.clamp(base_config_tensor + noise, 0.0, 1.0)
            
                                                   
            risks = self.surrogate.model(neighborhood_configs).squeeze()
            
            risk_variance = torch.var(risks).item()
            max_gradient = (torch.max(risks) - torch.min(risks)).item() / (epsilon * 2)
            
            return risk_variance, max_gradient

    def estimate_curvature_spectral_norm(self, base_config_tensor: torch.Tensor):
        """
        Approximates the Spectral Norm of the Hessian matrix.
        """
        self.surrogate.model.eval()
        
                                                                       
        base_leaf = base_config_tensor.detach().clone()
        base_leaf.requires_grad_(True)
        
                                         
        risk = self.surrogate.model(base_leaf)
        gradients = torch.autograd.grad(risk, base_leaf, create_graph=True)[0]
        
                                                      
        eps = 1e-4
        hessian = torch.zeros((3, 3), device=self.device)
        
        for i in range(3):
                                                                       
            pert_tensor = base_leaf.detach().clone()
            pert_tensor[0, i] += eps
            pert_tensor.requires_grad_(True)
            
                                                
            risk_plus = self.surrogate.model(pert_tensor)
            grad_plus = torch.autograd.grad(risk_plus, pert_tensor)[0]
            
                                                          
            hessian[i] = (grad_plus.squeeze() - gradients.squeeze()) / eps
            
        spectral_norm = torch.linalg.matrix_norm(hessian, ord=2).item()
        
        return spectral_norm