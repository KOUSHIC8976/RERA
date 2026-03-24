             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import importlib
import pathlib
import subprocess
import sys
from typing import Any, Dict, List, Optional

BENCHMARK_LISTING_FILE = (
    pathlib.Path(__file__).parent.absolute() / "benchmark_listing.yaml"
)


def auto_install_requirements(benchmark_spec: Dict[str, Any]):
    """Install dependencies as specified by the configuration given."""
                                                       
    requirements: List[str] = benchmark_spec.get("requirements", [])
    if len(requirements) > 0:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                *requirements,
            ]
        )


def _benchmark_at_version(target, version):
    versions = target["versions"]
    if not version:
        return versions[-1]

    for benchmark_at_version in versions:
        if benchmark_at_version["version"] == version:
            return benchmark_at_version

    def _format_versions(versions):
        return ", ".join(f"{d['version']}" for d in versions)

    raise KeyError(
        f"Version `{version}` was not found. Try from versions: {_format_versions(versions)}"
    )


def _get_entrypoint(path, name):
    module = importlib.import_module(path)
    entrypoint = module.__getattribute__(name)
    return entrypoint


def run_benchmark(
    benchmark_name: str,
    benchmark_version: Optional[float],
    agent_locator: str,
    benchmark_listing: pathlib.Path,
    debug_log: bool = False,
    auto_install: bool = False,
):
    """Runs a benchmark with the given configuration. Use `scl benchmark list` to see the available
    benchmarks.

    Args:
        benchmark_name(str): The name of the benchmark to run.
        benchmark_version(float|None): The version of the benchmark.
        agent_locator(str): Locator string for the registered agent.
        benchmark_listing(pathlib.Path): A configuration file that lists benchmark metadata and must list
            the target benchmark.
        debug_log: Debug to `stdout`.
    """
    from smarts.core.utils.resources import load_yaml_config_with_substitution

    listing_dict = load_yaml_config_with_substitution(benchmark_listing)

    benchmarks = listing_dict["benchmarks"]

    try:
        benchmark_group = benchmarks[benchmark_name]
    except KeyError as err:
        raise RuntimeError(
            f"`{benchmark_name}` not found in config `{BENCHMARK_LISTING_FILE}`."
        ) from err

    benchmark_spec = _benchmark_at_version(benchmark_group, benchmark_version)

    if auto_install:
        auto_install_requirements(benchmark_spec)

    module, _, name = benchmark_spec["entrypoint"].rpartition(".")
    entrypoint = _get_entrypoint(module, name)
    entrypoint(
        **benchmark_spec.get("params", {}),
        agent_locator=agent_locator,
        debug_log=debug_log,
    )


def list_benchmarks(benchmark_listing):
    """Lists details of the currently available benchmarks."""
    from smarts.core.utils.resources import load_yaml_config_with_substitution

    return load_yaml_config_with_substitution(pathlib.Path(benchmark_listing))
