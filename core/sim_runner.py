import torch
import numpy as np
from tqdm import tqdm
from functools import partial
import gymnasium as gym

                       
from SMARTS.smarts.core.agent_interface import AgentInterface
from SMARTS.smarts.core.controllers import ActionSpaceType
from SMARTS.smarts.env.gymnasium.wrappers.parallel_env import ParallelEnv
from SMARTS.smarts.env.utils.observation_conversion import ObservationOptions
from SMARTS.smarts.env.utils.action_conversion import ActionOptions

              
from policies.baseline_adapter import BaselineAVAdapter
from policies.adversarial_rl import AdversarialRiskEngine
from policies.human_parametric import ParametricHumanDriver
from risk.metrics import RiskMetricEngine
from risk.event_detector import EventDetector

class ScenarioDiscoveryRunner:
    """
    The main execution loop for the Risk Amplification Engine.
    Coordinates the GPU-batched environments, the AV policy, and the Adversarial search
    [cite_start]using the official SMARTS ParallelEnv [cite: 1, 298-301].
    """
    def __init__(self, scenarios: list, num_envs=16, max_steps=1000, device="cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.num_envs = num_envs
        self.max_steps = max_steps
        
        print(f"Initializing RRAE Runner on {self.device} with {num_envs} parallel SMARTS environments...")
        
        print(f"Initializing RRAE Runner on {self.device} with {num_envs} parallel SMARTS environments...")
        
                                                                          
                                                                                     
                                                                                                   
        def make_env(sim_name, **kwargs):
            from smarts.core.agent_interface import AgentInterface
            from smarts.core.controllers import ActionSpaceType
            
            interfaces = {
                "av_agent": AgentInterface(
                    waypoint_paths=True,
                    action=ActionSpaceType.Continuous, 
                    max_episode_steps=max_steps,
                ),
                "adv_agent": AgentInterface(
                    waypoint_paths=True,
                    action=ActionSpaceType.Continuous, 
                    max_episode_steps=max_steps,
                )
            }
            
            return gym.make(
                "smarts.env:hiway-v1",
                scenarios=scenarios,
                agent_interfaces=interfaces,
                sim_name=sim_name,
                headless=True,
                observation_options=ObservationOptions.unformatted, 
                action_options=ActionOptions.unformatted,
            )

        env_constructors = [
            partial(make_env, sim_name=f"rrae_sim_{i}") for i in range(num_envs)
        ]

        self.env = ParallelEnv(
            env_constructors=env_constructors,
            auto_reset=True,
            seed=42,
        )

        self.env = ParallelEnv(
            env_constructors=env_constructors,
            auto_reset=True,
            seed=42,
        )
        
                                                
                                                                                               
        self.av_policy = BaselineAVAdapter(device=self.device)
        self.adversarial_rl = AdversarialRiskEngine(obs_dim=12, device=self.device)
        self.human_decoder = ParametricHumanDriver(device=self.device)
        
                                              
        self.risk_engine = RiskMetricEngine(device=self.device)
        self.event_detector = EventDetector()

    def run(self):
        """Executes the closed-loop safety boundary discovery."""
        batched_terminateds = [{"__all__": False} for _ in range(self.num_envs)]
        batched_truncateds = [{"__all__": False} for _ in range(self.num_envs)]
        
        print("Starting SMARTS instances... (this may take a moment)")
        batched_observations, _ = self.env.reset()
        
        print("Commencing Adversarial Search...")
        
        for step in tqdm(range(self.max_steps)):
            
                                                             
            pos_tensor, vel_tensor, acc_tensor, obs_tensor = self._extract_kinematics(batched_observations)
            
                                                    
                                                                                          
            av_actions = self.av_policy.get_actions(obs_tensor) 
            raw_adv_actions = self.adversarial_rl.select_action(obs_tensor)
            
                                                                    
            adv_actions = raw_adv_actions.cpu().numpy()[:, :3] 
            
                                                            
            batched_actions = self._pack_actions(
                av_actions, adv_actions, batched_terminateds, batched_truncateds
            )
            
                                              
            (
                batched_observations,
                batched_rewards,
                batched_terminateds,
                batched_truncateds,
                batched_infos,
            ) = self.env.step(batched_actions)
            
                                                                
                                                                  
            ras_scores = self.risk_engine.calculate_ras(pos_tensor, vel_tensor, acc_tensor)
            
                                                                                        
            mock_min_ttcs = torch.rand((self.num_envs,), device=self.device) * 5.0 
            
            events_found = self.event_detector.evaluate_batch(step, ras_scores, mock_min_ttcs, batched_infos)
            
                                                   
            loss = -ras_scores.mean() 
            self.adversarial_rl.update_policy(loss)
            
        print(f"Search Complete. Discovered {len(self.event_detector.discovered_events)} boundary events.")
        self.env.close()

    def _extract_kinematics(self, batched_obs):
        """Converts lists of SMARTS unformatted observations to PyTorch tensors."""
        positions, velocities, accelerations, flat_obs = [], [], [], []

        for env_obs in batched_obs:
            env_pos, env_vel, env_acc = [], [], []
            
                              
            if "av_agent" in env_obs:
                ego = env_obs["av_agent"].ego_vehicle_state
                env_pos.append(ego.position[:2])
                env_vel.append(ego.linear_velocity[:2])
                env_acc.append(ego.linear_acceleration[:2])
                
                                                                                       
                flat_obs.append(list(ego.position[:2]) + list(ego.linear_velocity[:2]) + list(ego.linear_acceleration[:2]) * 2)
            else:
                env_pos.append([999.0, 999.0]); env_vel.append([0.0, 0.0]); env_acc.append([0.0, 0.0])
                flat_obs.append([0.0]*12)

                                       
            if "adv_agent" in env_obs:
                ego = env_obs["adv_agent"].ego_vehicle_state
                env_pos.append(ego.position[:2])
                env_vel.append(ego.linear_velocity[:2])
                env_acc.append(ego.linear_acceleration[:2])
            else:
                env_pos.append([-999.0, -999.0]); env_vel.append([0.0, 0.0]); env_acc.append([0.0, 0.0])

            positions.append(env_pos)
            velocities.append(env_vel)
            accelerations.append(env_acc)

        return (
            torch.tensor(positions, dtype=torch.float32, device=self.device),
            torch.tensor(velocities, dtype=torch.float32, device=self.device),
            torch.tensor(accelerations, dtype=torch.float32, device=self.device),
            torch.tensor(flat_obs, dtype=torch.float32, device=self.device)                     
        )

    def _pack_actions(self, av_actions, adv_actions, batched_terms, batched_truncs):
        """Packs continuous actions into the Dict structure expected by ParallelEnv."""
        batched_step_actions = []
        for i in range(self.num_envs):
            actions = {}
                                                                                                 
            if not batched_terms[i].get("av_agent", False) and not batched_truncs[i].get("av_agent", False):
                actions["av_agent"] = av_actions[i]
                
            if not batched_terms[i].get("adv_agent", False) and not batched_truncs[i].get("adv_agent", False):
                actions["adv_agent"] = adv_actions[i]
                
            batched_step_actions.append(actions)
        return batched_step_actions