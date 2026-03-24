                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               

import logging
import multiprocessing
import os
import shutil
import subprocess
import sys
from multiprocessing import Process, Semaphore, synchronize
from pathlib import Path
from typing import Any, Callable, List

logger = logging.getLogger(__name__)
LOG_DEFAULT = logger.info


def build_scenario(
    scenario: str,
    clean: bool = False,
    seed: int = 42,
    log: Callable[[Any], None] = LOG_DEFAULT,
):
    """Build a scenario."""

    log(f"Building: {scenario}")

    if clean:
        clean_scenario(scenario)

    scenario_root = Path(scenario)

    scenario_py = scenario_root / "scenario.py"
    if scenario_py.exists():
        _install_requirements(scenario_root, log)

        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "scenario_builder.py",
                    str(scenario_py.absolute()),
                    str(seed),
                ],
                cwd=Path(__file__).parent,
            )
        except subprocess.CalledProcessError as e:
            raise SystemExit(e)


def build_scenarios(
    scenarios: List[str],
    clean: bool = False,
    seed: int = 42,
    log: Callable[[Any], None] = LOG_DEFAULT,
):
    """Build a list of scenarios."""

    if not scenarios:
                                                                       
                                                              
        scenarios = ["scenarios"]

    concurrency = max(1, multiprocessing.cpu_count() - 1)
    sema = Semaphore(concurrency)
    all_processes = []
    for scenarios_path in scenarios:
        for subdir, _, _ in os.walk(scenarios_path):
            if _is_scenario_folder_to_build(subdir):
                p = Path(subdir)
                scenario = f"{scenarios_path}/{p.relative_to(scenarios_path)}"
                proc = Process(
                    target=_build_scenario_proc,
                    kwargs={
                        "scenario": scenario,
                        "semaphore": sema,
                        "clean": clean,
                        "seed": seed,
                        "log": log,
                    },
                )
                all_processes.append(proc)
                proc.start()

    for proc in all_processes:
        proc.join()


def _build_scenario_proc(
    scenario: str,
    semaphore: synchronize.Semaphore,
    clean: bool,
    seed: int,
    log: Callable[[Any], None] = LOG_DEFAULT,
):

    semaphore.acquire()
    try:
        build_scenario(scenario=scenario, clean=clean, seed=seed, log=log)
    finally:
        semaphore.release()


def _is_scenario_folder_to_build(path: str) -> bool:
    if os.path.exists(os.path.join(path, "waymo.yaml")):
                                                        
        return False
    if os.path.exists(os.path.join(path, "scenario.py")):
        return True
    from smarts.sstudio.sstypes import MapSpec

    map_spec = MapSpec(path)
    road_map, _ = map_spec.builder_fn(map_spec)
    return road_map is not None


def clean_scenario(scenario: str):
    """Remove all cached scenario files in the given scenario directory."""

    to_be_removed = [
        "map.glb",
        "map_spec.pkl",
        "bubbles.pkl",
        "missions.pkl",
        "flamegraph-perf.log",
        "flamegraph.svg",
        "flamegraph.html",
        "*.rou.xml",
        "*.rou.alt.xml",
        "social_agents/*",
        "traffic/*.rou.xml",
        "traffic/*.smarts.xml",
        "history_mission.pkl",
        "*.shf",
        "*-AUTOGEN.net.xml",
        "build.db",
    ]
    p = Path(scenario)

    shutil.rmtree(p / "build", ignore_errors=True)
    shutil.rmtree(p / "traffic", ignore_errors=True)
    shutil.rmtree(p / "social_agents", ignore_errors=True)

    for file_name in to_be_removed:
        for f in p.glob(file_name):
                         
            f.unlink()


def _install_requirements(scenario_root, log: Callable[[Any], None] = LOG_DEFAULT):
    import os

    requirements_txt = scenario_root / "requirements.txt"
    if requirements_txt.exists():
        import zoo.policies

        path = Path(os.path.dirname(zoo.policies.__file__)).absolute()
                                                                        
                                               
        pip_index_proc = subprocess.Popen(
            ["twistd", "-n", "web", "--path", path],
                                                
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        pip_install_cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_txt),
        ]

        log(f"Installing scenario dependencies via '{' '.join(pip_install_cmd)}'")

        try:
            subprocess.check_call(pip_install_cmd, stdout=subprocess.DEVNULL)
        finally:
            pip_index_proc.terminate()
            pip_index_proc.wait()
