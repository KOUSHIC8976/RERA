                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import argparse

from smarts.core.sumo_road_network import SumoRoadNetwork
from smarts.sstudio.sstypes import MapSpec


def generate_glb_from_sumo_file(sumo_net_file: str, out_glb_dir: str):
    """Creates a geometry file from a sumo map file."""
    map_spec = MapSpec(sumo_net_file)
    road_network = SumoRoadNetwork.from_spec(map_spec)
    road_network.to_glb(out_glb_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "sumo2mesh.py",
        description="Utility to export sumo road networks to mesh files.",
    )
    parser.add_argument("net", help="sumo net file (*.net.xml)", type=str)
    parser.add_argument("output_path", help="where to write the mesh file", type=str)
    args = parser.parse_args()

    generate_glb_from_sumo_file(args.net, args.output_path)
