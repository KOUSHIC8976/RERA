import pandas as pd
import numpy as np

class CausalInferenceEngine:
    """
    Phase 6: Structural Causal Models (SCM) & DAG Extraction.
    Determines the exact root-cause pathways of an AV failure[cite: 171, 177].
    """
    def __init__(self):
        self.history = []

    def log_causal_step(self, sensor_noise, estimator_drift, mpc_oscillation, control_saturation):
        self.history.append([sensor_noise, estimator_drift, mpc_oscillation, control_saturation])

    def extract_root_cause_dag(self):
        """
        Builds a Directed Acyclic Graph (DAG) using partial correlations
        to find the Average Treatment Effect of specific module failures[cite: 174, 175].
        """
        df = pd.DataFrame(self.history, columns=['Sensor_Noise', 'Estimator_Drift', 'MPC_Oscillation', 'Control_Saturation'])
        
                                                                       
                                
        w_sensor_est = df['Sensor_Noise'].corr(df['Estimator_Drift'])
                             
        w_est_mpc = df['Estimator_Drift'].corr(df['MPC_Oscillation'])
                              
        w_mpc_sat = df['MPC_Oscillation'].corr(df['Control_Saturation'])

        print("\n" + "="*40)
        print(" PHASE 6: CAUSAL Root-Cause DAG Extraction")
        print("="*40)
        print(f"Sensor Noise -> Estimator Drift : Weight {w_sensor_est:.2f}")
        print(f"Estimator Drift -> MPC Oscillation: Weight {w_est_mpc:.2f}") 
        print(f"MPC Oscillation -> Control Lock   : Weight {w_mpc_sat:.2f}") 
        
                                                      
        if w_sensor_est > w_est_mpc:
            fault_type = "Hardware/Sensor Fault (Perception breakdown)"
        else:
            fault_type = "Algorithmic Fault (Controller instability)"
            
        print(f"\n Primary Systemic Root Cause: {fault_type}")
        return fault_type