                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import os
import subprocess
import sys
from typing import Optional


def _usage_error(msg: Optional[str] = None):
    if msg:
        print(f"ERROR:  {msg}")
    print("usage:  python -m smarts.ros setup_node [install_path]")
    print(
        "\twhere install_path is an optional existing folder into which to put the node"
    )
    sys.exit(-1)


if __name__ == "__main__":
    if not 2 <= len(sys.argv) <= 3 or sys.argv[1] != "setup_node":
        _usage_error()

                                                                                                      

    mod_path = os.path.dirname(__file__)

    install_arg = ""
    install_path = f"{mod_path}/install"
    if len(sys.argv) >= 3:
        install_path = sys.argv[2]
        if not os.path.isdir(install_path):
            _usage_error(f"install_path ({install_path}) does not exist.")
        install_arg = f"-DCMAKE_INSTALL_PREFIX={install_path}"

    source_ros = ""
    if (
        os.environ.get("ROS_VERSION", 0) != 1
        or os.environ.get("ROS_DISTRO", "a")[0] < "k"
    ):
        ros_base = "/opt/ros"
        for distro in ["noetic", "melodic", "lunar", "kinetic"]:
            ros_distro = os.path.join(ros_base, distro)
            if os.path.isdir(ros_distro):
                break
        else:
            print(
                "cannot find appropriate ROS v1 distribution.  SMARTS requires kinetic or newer."
            )
            sys.exit()
        source_ros = f". {ros_distro}/setup.sh && "
    print("setting up ROS node for SMARTS...")
                                                                             
                                                                                       
    default_path = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    subprocess.check_call(
        f"{source_ros}catkin_make {install_arg} install",
        shell=True,
        cwd=mod_path,
        env={"PATH": default_path},
    )
    print(f"\nnow run:  source {install_path}/setup.bash")
