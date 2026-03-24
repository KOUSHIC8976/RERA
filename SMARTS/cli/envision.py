                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import click


@click.group(
    name="envision",
    help="Commands to utilize an Envision server. The Envision web server is used for visualization purposes. See `scl envision COMMAND --help` for further options.",
)
def envision_cli():
    pass


@envision_cli.command(name="start", help="Start an Envision server.")
@click.option("-p", "--port", help="Port Envision will run on.", default=8081)
@click.option(
    "-c",
    "--max_capacity",
    help=(
        "Max capacity in MB of Envision's playback buffer. The larger the more contiguous history "
        "Envision can store."
    ),
    default=500,
    type=float,
)
def start_server(port, max_capacity):
    from envision.server import run

    run(max_capacity_mb=max_capacity, port=port)


envision_cli.add_command(start_server)
