import torch
import multiprocessing as mp
import numpy as np
                                                                          

def _worker(env_fn, remote, parent_remote):
    """Worker process that runs an individual SMARTS simulation."""
    parent_remote.close()
    env = env_fn()
    try:
        while True:
            cmd, data = remote.recv()
            if cmd == 'step':
                obs, reward, terminated, truncated, info = env.step(data)
                if terminated or truncated:
                    obs, _ = env.reset()
                remote.send((obs, reward, terminated, truncated, info))
            elif cmd == 'reset':
                obs, _ = env.reset()
                remote.send(obs)
            elif cmd == 'close':
                env.close()
                remote.close()
                break
    except KeyboardInterrupt:
        print("Worker terminated.")
    finally:
        env.close()

class VectorizedSmartsOrchestrator:
    """
    Spawns multiple SMARTS environments across CPU cores and batches
    their outputs into PyTorch GPU tensors for fast adversarial learning.
    """
    def __init__(self, env_fns, device: str = "cuda"):
        self.num_envs = len(env_fns)
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        
                                     
        self.remotes, self.work_remotes = zip(*[mp.Pipe() for _ in range(self.num_envs)])
        
        self.processes = []
        for work_remote, remote, env_fn in zip(self.work_remotes, self.remotes, env_fns):
            p = mp.Process(target=_worker, args=(env_fn, work_remote, remote))
            p.daemon = True
            self.processes.append(p)
            p.start()
            
        for remote in self.work_remotes:
            remote.close()

    def reset(self):
        """Resets all environments and returns a batched tensor."""
        for remote in self.remotes:
            remote.send(('reset', None))
            
                                               
        results = [remote.recv() for remote in self.remotes]
        return self._batch_observations(results)

    def step(self, batched_actions: torch.Tensor):
        """
        Sends slices of the batched GPU tensor action to individual CPU environments.
        """
                                                                       
        actions_np = batched_actions.detach().cpu().numpy()
        
        for i, remote in enumerate(self.remotes):
            remote.send(('step', actions_np[i]))
            
        results = [remote.recv() for remote in self.remotes]
        
        obs_list, rewards, terms, truncs, infos = zip(*results)
        
                                    
        batched_obs = self._batch_observations(obs_list)
        batched_rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        batched_dones = torch.tensor([t or tr for t, tr in zip(terms, truncs)], dtype=torch.float32, device=self.device)
        
        return batched_obs, batched_rewards, batched_dones, infos

    def _batch_observations(self, obs_list):
        """
        Takes a list of individual dict observations and stacks them into a batch tensor.
        """
                                                                                          
                                                                                             
                                                                             
        tensors = [obs_dict['ego_agent'] for obs_dict in obs_list]
        return torch.stack(tensors).to(self.device)

    def close(self):
        for remote in self.remotes:
            remote.send(('close', None))
        for p in self.processes:
            p.join()