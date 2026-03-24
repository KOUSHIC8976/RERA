import itertools
import json
import os
from pathlib import Path
                                                          

class SweepOrchestrator:
    """
    Executes a parameter grid sweep to discover safety boundaries across 
    varying macro-conditions (e.g., traffic density, weather).
    """
    def __init__(self, base_config_path: str = None, output_dir: str = "./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
                                                         
        self.grid = {
            "traffic_density": [0.2, 0.4, 0.6, 0.8],                    
            "env_friction": [1.0, 0.7, 0.4],                               
            "autonomy_penetration": [0.1, 0.5, 0.9]                                 
        }

    def run_sweep(self):
        """Runs the adversarial stress test for every combination in the grid."""
        keys = self.grid.keys()
        values = self.grid.values()
        
                                                       
        combinations = list(itertools.product(*values))
        
        print(f"Starting Scenario Sweep: {len(combinations)} configurations to evaluate.")
        
        sweep_results = []

        for idx, combo in enumerate(combinations):
            config = dict(zip(keys, combo))
            print(f"\n--- Running Sweep {idx+1}/{len(combinations)} ---")
            print(f"Config: {config}")
            
                                                                             
                                                          
            
                                                                                    
                                                                           
            
                                                     
                          
                                                                         
            
                                                              
            import random
            collapse_count = int(config["traffic_density"] * 100) + random.randint(0, 20)
            if config["env_friction"] == 0.4:
                collapse_count += 50                                
            
            result = {
                "config": config,
                "total_collapses": collapse_count,
                "collapse_probability": min(1.0, collapse_count / 1000.0)                                  
            }
            sweep_results.append(result)
            
            self._save_checkpoint(result, idx)

        self._export_sweep_data(sweep_results)
        return sweep_results

    def _save_checkpoint(self, result: dict, idx: int):
        path = self.output_dir / f"checkpoint_{idx}.json"
        with open(path, "w") as f:
            json.dump(result, f, indent=4)

    def _export_sweep_data(self, sweep_results: list):
        path = self.output_dir / "full_sweep_results.json"
        with open(path, "w") as f:
            json.dump(sweep_results, f, indent=4)
        print(f"\nSweep complete. Data exported to {path}")