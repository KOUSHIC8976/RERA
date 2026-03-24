                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import click


@click.group(
    name="diagnostic",
    help="Utilities for diagnosing the simulation performance. See `scl diagnostic COMMAND --help` for further options.",
)
def diagnostic_cli():
    pass


@click.command("run", help="Run all diagnostics.")
@click.argument("scenarios", nargs=-1, metavar="<scenarios>")
def run(scenarios):
    from smarts.diagnostic import run as _run

    _run.main(scenarios)


diagnostic_cli.add_command(run)
