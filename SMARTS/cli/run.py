                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os
import signal
import subprocess
import sys
import time
import webbrowser
from contextlib import contextmanager

import click


@contextmanager
def kill_process_group_afterwards():
    os.setpgrp()
    try:
        yield
    finally:
                                        
        os.killpg(0, signal.SIGKILL)


@click.command(
    name="run",
    help="Run an experiment on a scenario",
    context_settings=dict(ignore_unknown_options=True),
)
@click.option(
    "--envision",
    is_flag=True,
    default=False,
    help="Start up Envision server at the specified port when running an experiment",
)
@click.option(
    "-p",
    "--envision_port",
    help="Port on which Envision will run.",
    default=None,
)
@click.argument(
    "script_path", type=click.Path(exists=True), metavar="<script>", required=True
)
@click.argument("script_args", nargs=-1, type=click.UNPROCESSED)
def run_experiment(envision, envision_port, script_path, script_args):
    with kill_process_group_afterwards():
        if envision:
            if envision_port is None:
                envision_port = 8081
            subprocess.Popen(
                [
                    "scl",
                    "envision",
                    "start",
                    "-p",
                    str(envision_port),
                ],
            )
                                                                  
            time.sleep(2)
            url = "http://localhost:" + str(envision_port)
            webbrowser.open_new_tab(url)

        if (not envision) and envision_port:
            click.echo(
                "Port passed without starting up the envision server. Use the --envision option to start the server along with the --envision port option."
            )

        script = subprocess.Popen(
            [sys.executable, script_path, *script_args],
        )
        script.communicate()
