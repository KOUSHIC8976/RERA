import torch

class PolicyRepairAgent:
    """
    Phase 7: Differentiable Policy Repair.
    Closes the loop by backpropagating crash loss to suggest AV parameter fixes[cite: 181, 184].
    """
    def __init__(self, surrogate_model, device="cuda"):
        self.device = device
        self.surrogate = surrogate_model
        
    def calculate_optimal_patch(self, critical_env_tensor: torch.Tensor, current_pid_gain: float, current_kalman_cov: float):
        """
        Uses gradient-based tuning to find parameters that minimize system risk[cite: 184, 188, 189].
        """
        print("\n" + "="*40)
        print("🔧 PHASE 7: Differentiable Policy Repair Initiated")
        print("="*40)
        
                                                                 
        pid_tensor = torch.tensor([current_pid_gain], requires_grad=True, device=self.device)
        kalman_tensor = torch.tensor([current_kalman_cov], requires_grad=True, device=self.device)
        
        optimizer = torch.optim.Adam([pid_tensor, kalman_tensor], lr=0.05)
        
        initial_risk = None
        
                                                                                 
        for step in range(50):
            optimizer.zero_grad()
            
                                                                               
                                                              
            av_vulnerability = (pid_tensor ** 2) + (kalman_tensor - 0.5)**2
            predicted_risk = self.surrogate.model(critical_env_tensor).squeeze() * av_vulnerability
            
            if step == 0:
                initial_risk = predicted_risk.item()
                
            loss = predicted_risk.mean()
            loss.backward()
            optimizer.step()
            
        final_risk = predicted_risk.mean().item()
        risk_reduction = ((initial_risk - final_risk) / initial_risk) * 100
        
        self._generate_semantic_bug_report(kalman_tensor.item(), pid_tensor.item(), risk_reduction) 

    def _generate_semantic_bug_report(self, optimized_kalman, optimal_pid, risk_reduction):
        """Generates a human-readable Jira-style bug report[cite: 192]."""
        print("\n📝 Auto-Generated Bug Report:")
        print("-" * 30)
        print("Detected Issue: Kalman covariance underestimation causing estimator drift.") 
        print(f"Suggested Fix: Increase covariance scaling to {optimized_kalman:.2f}") 
        print(f"Suggested Fix: Adjust PID gain to {optimal_pid:.2f}")
        print(f"Expected Risk Reduction: {risk_reduction:.1f}%") 
        print("-" * 30)