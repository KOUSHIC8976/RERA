                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from pathlib import Path
from typing import Optional

import click


@click.group(
    name="benchmark",
    help="Utilities for running integrated ML benchmarks. See `scl benchmark COMMAND --help` for further options.",
)
def benchmark_cli():
    pass


@click.command(
    "run",
)
@click.argument("benchmark_id", nargs=1, metavar="<benchmark_id>")
@click.argument("agent_locator", nargs=1, metavar="<agent_locator>")
@click.option(
    "--benchmark-listing",
    type=str,
    default=None,
    help="Directs to a different listing file.",
)
@click.option(
    "--auto-install",
    is_flag=True,
    default=False,
    help="Attempt to auto install requirements.",
)
def run(
    benchmark_id: str,
    agent_locator: str,
    benchmark_listing: Optional[str],
    auto_install: bool,
):
    """This runs a given benchmark.

    Use `scl benchmark list` to see the available benchmarks.

    \b
    <benchmark_id> is formatted like BENCHMARK_NAME==BENCHMARK_VERSION.
    <agent_locator> is the locator string for the registered agent.

    An example use: `scl benchmark run --auto-install driving_smarts==0.0 random-relative-target-pose-agent-v0`
    """
    from smarts.benchmark import BENCHMARK_LISTING_FILE, run_benchmark

    benchmark_id, _, benchmark_version = benchmark_id.partition("==")

    run_benchmark(
        benchmark_name=benchmark_id,
        benchmark_version=float(benchmark_version) if benchmark_version else None,
        agent_locator=agent_locator,
        benchmark_listing=Path(benchmark_listing)
        if benchmark_listing is not None
        else BENCHMARK_LISTING_FILE,
        auto_install=auto_install,
    )


@click.command("list")
@click.option(
    "--benchmark-listing",
    type=str,
    default=None,
    help="Directs to a different listing file.",
)
def list_benchmarks(benchmark_listing: Optional[str]):
    """Lists available benchmarks that can be used for `scl benchmark run`."""
    from smarts.benchmark import BENCHMARK_LISTING_FILE
    from smarts.benchmark import list_benchmarks as _list_benchmarks

    benchmarks = _list_benchmarks(
        Path(benchmark_listing)
        if benchmark_listing is not None
        else BENCHMARK_LISTING_FILE,
    )["benchmarks"]

    print("BENCHMARK_NAME".ljust(29) + "BENCHMARK_ID".ljust(25) + "VERSIONS")

    def _format_versions(versions):
        return ", ".join(f"{d['version']}" for d in versions)

    print(
        "\n".join(
            f"- {info['name']}:".ljust(29)
            + f"{id_.ljust(25)}{_format_versions(info['versions'])}"
            for id_, info in benchmarks.items()
        )
    )


benchmark_cli.add_command(run)
benchmark_cli.add_command(list_benchmarks)
