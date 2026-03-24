                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import argparse

from smarts.core.opendrive_road_network import OpenDriveRoadNetwork
from smarts.sstudio.sstypes import MapSpec


def generate_glb_from_opendrive_file(od_xodr_file: str, out_glb_dir: str):
    """Creates a geometry file from an OpenDRIVE map file."""
    map_spec = MapSpec(od_xodr_file)
    road_network = OpenDriveRoadNetwork.from_spec(map_spec)
    road_network.to_glb(out_glb_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "od2mesh.py",
        description="Utility to export opendrive road networks to mesh files.",
    )
    parser.add_argument("xodr", help="openDRIVE xodr file (*.xodr) path", type=str)
    parser.add_argument("output_path", help="where to write the mesh file", type=str)
    args = parser.parse_args()

    generate_glb_from_opendrive_file(args.xodr, args.output_path)
