             

                                                                        

                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          

                                                                            
                                                     

                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import click

from cli.benchmark import benchmark_cli
from cli.diagnostic import diagnostic_cli
from cli.envision import envision_cli
from cli.run import run_experiment
from cli.studio import scenario_cli
from cli.waymo import waymo_cli
from cli.zoo import zoo_cli


@click.group()
def scl():
    """
    The SMARTS command line interface.
    Use --help with each command for further information.
    """
    pass


scl.add_command(envision_cli)
scl.add_command(benchmark_cli)
scl.add_command(scenario_cli)
scl.add_command(zoo_cli)
scl.add_command(run_experiment)
scl.add_command(waymo_cli)
scl.add_command(diagnostic_cli)

if __name__ == "__main__":
    scl()
