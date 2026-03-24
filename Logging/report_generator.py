import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class SafetyReportGenerator:
    """
    Consumes JSON sweep data and generates quantifiable safety surface 
    estimations, phase diagrams, and risk escalation curves.
    """
    def __init__(self, results_path: str = "./results/full_sweep_results.json", output_dir: str = "./reports"):
        self.results_path = results_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.results_path, "r") as f:
            self.raw_data = json.load(f)
            
        self._build_dataframe()

    def _build_dataframe(self):
        """Flattens the nested JSON into a Pandas DataFrame for plotting."""
        flat_data = []
        for entry in self.raw_data:
            row = entry["config"].copy()
            row["collapse_probability"] = entry["collapse_probability"]
            row["total_collapses"] = entry["total_collapses"]
            flat_data.append(row)
            
        self.df = pd.DataFrame(flat_data)

    def generate_phase_diagram(self):
        """
        Creates a 2D Heatmap (Phase Diagram) showing the safety boundary.
        E.g., Traffic Density vs. Environmental Friction.
        """
                                         
        pivot_table = self.df.pivot_table(
            values='collapse_probability', 
            index='env_friction',           
            columns='traffic_density',         
            aggfunc='mean'
        )

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            pivot_table, 
            annot=True, 
            cmap="YlOrRd",                                  
            cbar_kws={'label': 'System Collapse Probability'}
        )
        
        plt.title('Safety Boundary Phase Diagram: Mixed-Autonomy')
        plt.xlabel('Traffic Density (Vehicles / 100m)')
        plt.ylabel('Environmental Friction (1.0=Dry, 0.4=Icy)')
        
                                                                                                
        plt.gca().invert_yaxis() 
        
        out_path = self.output_dir / "phase_diagram.png"
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Phase diagram saved to {out_path}")

    def generate_risk_escalation_curve(self):
        """Plots how fast the adversarial engine amplifies risk over time."""
                                                                                      
                                                                 
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=self.df, 
            x='autonomy_penetration', 
            y='collapse_probability', 
            hue='traffic_density',
            marker='o'
        )
        
        plt.title('Risk Escalation vs. Autonomy Penetration')
        plt.xlabel('Autonomy Penetration (Ratio of AVs)')
        plt.ylabel('Collapse Probability')
        
        out_path = self.output_dir / "risk_escalation.png"
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Risk escalation curve saved to {out_path}")

    def run_all_reports(self):
        print("Generating RRAE Validation Reports...")
        self.generate_phase_diagram()
        self.generate_risk_escalation_curve()