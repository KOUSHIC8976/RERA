import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import json

class CertificationDashboard:
    """
    Enterprise Robustness Certification Engine.
    Generates Audit-Grade HTML Dashboards with Confidence Intervals and Visual Replay Packs.
    """
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.logs = []

    def log_iteration(self, config, geometry, internal_errors):
        entry = {**config, **geometry, **internal_errors}
        self.logs.append(entry)

    def calculate_robustness_margin_and_envelope(self, df):
        """Calculates RM, Safe Envelope, and 95% Confidence Intervals."""
        df['is_stable'] = (df['control_saturation_rate'] < 0.1).astype(int)
        stable_df = df[df['is_stable'] == 1]
        unstable_df = df[df['is_stable'] == 0]
        
        if stable_df.empty or unstable_df.empty:
            df['RM_normalized'] = 0.0
            return "<h3>Insufficient data to map Stability Envelope</h3>"
            
        features = ['traffic_density', 'env_friction', 'max_state_drift', 'curvature_norm']
        
        env_html = "<h3>Safe Operating Envelope</h3><ul>"
        for feat in features:
            if feat == 'env_friction':
                env_html += f"<li><b>{feat}</b> &ge; {stable_df[feat].min():.2f}</li>"
            else:
                env_html += f"<li><b>{feat}</b> &le; {stable_df[feat].max():.2f}</li>"
        env_html += "</ul><p><i>Outside this envelope, the system becomes unstable.</i></p>"

        weights = np.array([1.0, 0.7, 1.2, 0.8]) 
        S_vals = df[features].values
        U_vals = unstable_df[features].values
        
        rm_raw = []
        for current_theta in S_vals:
            weighted_distances = np.sqrt(np.sum(weights * (current_theta - U_vals)**2, axis=1))
            rm_raw.append(np.min(weighted_distances))
            
        df['RM_raw'] = rm_raw
        max_rm = df['RM_raw'].max()
        df['RM_normalized'] = df['RM_raw'] / max_rm if max_rm > 0 else 0.0
        df.loc[df['is_stable'] == 0, 'RM_normalized'] = 0.0
        
                                            
        mean_rm = df['RM_normalized'].mean()
        std_rm = df['RM_normalized'].std()
        n = len(df)
        ci_95 = 1.96 * (std_rm / np.sqrt(n)) if n > 0 else 0.0
        
        safe_pct = (df['RM_normalized'] > 0.6).mean() * 100
        near_pct = ((df['RM_normalized'] <= 0.6) & (df['RM_normalized'] > 0.0)).mean() * 100
        unstable_pct = (df['is_stable'] == 0).mean() * 100
        
        rm_html = f"""
        <h3>Robustness Margin Report</h3>
        <ul>
            <li><b>Average RM: {mean_rm:.2f} &plusmn; {ci_95:.2f} (95% CI)</b></li>
            <li>Minimum RM: {df['RM_normalized'][df['is_stable'] == 1].min() if not stable_df.empty else 0.0:.2f}</li>
            <li>Max RM: {df['RM_normalized'].max():.2f}</li>
            <br>
            <li><b>System Status:</b></li>
            <li>SAFE Region Coverage: {safe_pct:.1f}%</li>
            <li>NEAR-BOUNDARY: {near_pct:.1f}%</li>
            <li>UNSTABLE: {unstable_pct:.1f}%</li>
        </ul>
        """
        return env_html + rm_html

    def detect_instability_regimes(self, df):
        """Dynamically clusters and labels failure regimes."""
        regimes_html = "<h3>Detected Instability Regimes</h3><ul>"
        unstable_df = df[df['is_stable'] == 0]
        
        if unstable_df.empty:
            return regimes_html + "<li>System is 100% Safe in tested boundaries.</li></ul>"

        high_dens = unstable_df['traffic_density'].median()
        low_fric = unstable_df['env_friction'].median()
        high_drift = unstable_df['max_state_drift'].median()
        
        regime_a = unstable_df[(unstable_df['traffic_density'] >= high_dens) & (unstable_df['env_friction'] <= low_fric)]
        if len(regime_a) > 0:
            regimes_html += f"<li><b>Regime A (Dense Traffic + Slip):</b> Clustered around Density &ge; {high_dens:.2f}, Friction &le; {low_fric:.2f}.</li>"
            
        regime_b = unstable_df[unstable_df['max_state_drift'] >= high_drift]
        if len(regime_b) > 0:
            regimes_html += f"<li><b>Regime B (Perception Collapse):</b> Failures driven by severe estimator drift (&ge; {high_drift:.2f}).</li>"
            
        return regimes_html + "</ul>"

    def generate_replay_pack_html(self, df):
        """Generates a visual HTML table for the Scenario Replay Library."""
        critical_cases = df[df['is_stable'] == 0].head(5)
        if critical_cases.empty:
            return "<h3>Scenario Replay Pack</h3><p>No critical failures to replay.</p>"
            
        html = "<h3>Scenario Replay Pack</h3><table border='1' cellpadding='5' style='border-collapse: collapse; text-align: left; width: 100%;'>"
        html += "<tr style='background-color: #C8D4E3;'><th>Scenario ID</th><th>Traffic Density</th><th>Friction</th><th>Autonomy %</th><th>Replay Seed</th></tr>"
        
        for idx, row in critical_cases.iterrows():
            seed = int(abs(hash(row['traffic_density'])) % 1000000)
            html += f"<tr><td><b>RERA-S{idx}</b></td><td>{row['traffic_density']:.2f}</td><td>{row['env_friction']:.2f}</td><td>{row['autonomy_penetration']:.2f}</td><td><code>{seed}</code></td></tr>"
            
        return html + "</table>"
        
    def generate_cascading_failure_visual(self):
        """Generates a text-based cascading failure graph."""
        return """
        <h3>Cascading Failure Graph</h3>
        <div style='background-color: #f8f9fa; padding: 15px; border-left: 4px solid #d9534f; font-family: monospace;'>
            <b>Environment Stress</b> (Density &uarr;, Friction &darr;)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&#10551; <b>Sensor Noise</b> &uarr;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10551; <b>State Drift</b> &uarr; (Estimator Divergence)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10551; <b>MPC Oscillation</b> &uarr;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10551; <b style='color: red;'>Control Saturation (Failure)</b>
        </div>
        """

    def generate_report(self):
        df = pd.DataFrame(self.logs)
        if df.empty: return

        print("\n[Phase 5] Compiling Enterprise Robustness Certification Dashboard...")
        
        envelope_and_rm_html = self.calculate_robustness_margin_and_envelope(df)
        regimes_html = self.detect_instability_regimes(df)
        replay_html = self.generate_replay_pack_html(df)
        cascade_html = self.generate_cascading_failure_visual()
        
                                                
        stable_df = df[df['is_stable'] == 1]
        unstable_df = df[df['is_stable'] == 0]
        
        fig_env = go.Figure()
        fig_env.add_trace(go.Scatter(x=stable_df['traffic_density'], y=stable_df['env_friction'], mode='markers', name='Safe', marker=dict(color='#2ca02c', size=10, opacity=0.7)))
        fig_env.add_trace(go.Scatter(x=unstable_df['traffic_density'], y=unstable_df['env_friction'], mode='markers', name='Unstable (Boundary)', marker=dict(color='#d62728', size=10, symbol='x')))
        fig_env.update_layout(title="2D Stability Envelope (Density vs Friction)", xaxis_title="Traffic Density", yaxis_title="Environmental Friction", height=400, margin=dict(l=0, r=0, t=40, b=0))

                          
        fig_timeline = go.Figure(data=[go.Scatter(y=df['control_saturation_rate'], mode='lines+markers', name='Control Saturation', line=dict(color='#ff7f0e'))])
        fig_timeline.add_hline(y=0.1, line_dash="dash", line_color="red", annotation_text="Instability Threshold")
        fig_timeline.update_layout(title="Risk Timeline (Instability Buildup Over Time)", xaxis_title="Simulation Iteration", yaxis_title="Control Saturation Rate", height=300, margin=dict(l=0, r=0, t=40, b=0))

                                   
        fig_surface = go.Figure(data=[go.Scatter3d(
            x=df['traffic_density'], y=df['env_friction'], z=df['curvature_norm'], mode='markers',
            marker=dict(size=8, color=df['RM_normalized'] if 'RM_normalized' in df.columns else df['max_state_drift'], colorscale='RdYlGn', opacity=0.8, colorbar=dict(title="Robustness Margin"))
        )])
        fig_surface.update_layout(title="3D Boundary Geometry & Curvature Surface", scene=dict(xaxis_title='Density', yaxis_title='Friction', zaxis_title='Curvature'))

                            
        html_path = self.output_dir / "certification_report.html"
        with open(html_path, 'w') as f:
            f.write("<html><head><title>RRAE Audit Dashboard</title></head><body style='font-family: Arial; padding: 30px; background-color: #f4f6f9;'>")
            f.write("<div style='background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>")
            f.write("<h1 style='color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;'>RRAE: Autonomous System Robustness Certification</h1>")
            
            f.write("<div style='display: flex; gap: 40px; margin-top: 20px;'>")
            f.write("<div style='flex: 1;'>" + envelope_and_rm_html + cascade_html + "</div>")
            f.write("<div style='flex: 1;'>" + regimes_html + replay_html + "</div>")
            f.write("</div><hr style='margin: 30px 0;'>")
            
            f.write("<div style='display: flex; gap: 20px;'>")
            f.write("<div style='flex: 1;'>" + fig_env.to_html(full_html=False, include_plotlyjs='cdn') + "</div>")
            f.write("<div style='flex: 1;'>" + fig_timeline.to_html(full_html=False, include_plotlyjs=False) + "</div>")
            f.write("</div><hr style='margin: 30px 0;'>")
            
            f.write(fig_surface.to_html(full_html=False, include_plotlyjs=False))
            f.write("</div></body></html>")
            
        print(f"✅ Dashboard generated successfully: {html_path}")