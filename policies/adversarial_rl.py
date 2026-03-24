import torch
import torch.nn as nn
import torch.optim as optim

class AdversarialActor(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int = 5):
        super().__init__()
                                                              
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.Mish(),                                                    
            nn.Linear(256, 256),
            nn.Mish(),
            nn.Linear(256, action_dim),
            nn.Tanh()                                                             
        )

    def forward(self, obs):
        return self.net(obs)

class AdversarialRiskEngine:
    """
    The PyTorch RL module responsible for learning scenarios that maximize the Risk Amplification Score.
    Uses CUDA Mixed Precision for Ada Lovelace acceleration.
    """
    def __init__(self, obs_dim: int, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.actor = AdversarialActor(obs_dim).to(self.device)
        self.optimizer = optim.AdamW(self.actor.parameters(), lr=3e-4)
        
                                                                 
        self.scaler = torch.cuda.amp.GradScaler()

    def select_action(self, batched_obs: torch.Tensor) -> torch.Tensor:
        """Runs fast inference to generate adversarial parameters."""
        self.actor.eval()
        with torch.no_grad():
                                                     
            with torch.cuda.amp.autocast():
                actions = self.actor(batched_obs)
        return actions

    def update_policy(self, loss: torch.Tensor):
        """Optimizes the network using AMP to prevent underflow in FP16."""
        self.actor.train()
        self.optimizer.zero_grad()
        
                                          
        self.scaler.scale(loss).backward()
        
                          
        self.scaler.step(self.optimizer)
        self.scaler.update()