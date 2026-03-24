                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import argparse

from smarts.core import seed as smarts_seed


def _build(scenario_py: str, seed: int):
                                                                                     
    smarts_seed(seed)

                                                                                            
    with open(scenario_py, "rb") as source_file:
        code = compile(source_file.read(), scenario_py, "exec")
        exec(code, {"__file__": scenario_py})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_py", help="Path to the scenario.py file.", type=str)
    parser.add_argument(
        "seed",
        help="Seed that will be set before executing the scenario script.",
        type=int,
    )
    args = parser.parse_args()
    _build(args.scenario_py, args.seed)
