import argparse
import sys
import threading
from typing import Dict, List, Any, Union, Callable

from colorama import Back, Fore, init, Style
from nornir.core import Nornir, Config, Inventory
from nornir.core.task import Task
from nornir.core.task import Result

init(autoreset=True, strip=False)
LOCK = threading.Lock()


def parse_cli_args(raw_args: List[str]) -> dict:
    """
    Parse CLI provided arguments; ignore unrecognized.

    Arguments:
        raw_args: List of CLI provided arguments

    Returns:
        cli_args: Processed CLI arguments

    Raises:
        N/A  # noqa

    """
    parser = argparse.ArgumentParser(description="Nornir Script Wrapper")
    parser.add_argument(
        "-w",
        "--workers",
        help="number of workers to set for global configuration",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-l",
        "--limit",
        help="limit to host or comma separated list of hosts",
        type=str.lower,
        default="",
    )
    parser.add_argument(
        "-g",
        "--groups",
        help="limit to group or comma separated list of groups",
        type=str.lower,
        default="",
    )
    parser.add_argument(
        "-t", "--tags", help="names of tasks to explicitly run", type=str.lower, default=""
    )
    parser.add_argument("-s", "--skip", help="names of tasks to skip", type=str.lower, default="")
    args, _ = parser.parse_known_args(raw_args)
    cli_args = {
        "workers": args.workers if args.workers else False,
        "limit": set(args.limit.split(",")) if args.limit else False,
        "groups": set(args.groups.split(",")) if args.groups else False,
        "run_tags": set(args.tags.split(",")) if args.tags else [],
        "skip_tags": set(args.skip.split(",")) if args.skip else [],
    }
    return cli_args


def patch_inventory(cli_args: dict, inv: Inventory) -> Inventory:
    """
    Patch nornir inventory configurations per cli arguments.

    Arguments:
        cli_args: Updates from CLI to update in Nornir objects
        inv: nornir.core.inventory.Inventory object; Initialized Nornir Inventory object

    Returns:
        inv: nornir.core.inventory.Inventory object; Updated Nornir Inventory object

    Raises:
        N/A  # noqa

    """
    if cli_args["limit"]:
        valid_hosts = []
        invalid_hosts = []
        for host in cli_args["limit"]:
            if host in inv.hosts.keys():
                valid_hosts.append(host)
            else:
                invalid_hosts.append(host)
        if invalid_hosts:
            print(
                "Host limit contained invalid host(s), ignoring: "
                f"{[host for host in invalid_hosts]}"
            )
        inv = inv.filter(filter_func=lambda h: h.name in valid_hosts)

    elif cli_args["groups"]:
        valid_groups = [g for g in cli_args["groups"] if g in inv.groups.keys()]
        invalid_groups = [g for g in cli_args["groups"] if g not in inv.groups.keys()]
        if invalid_groups:
            print(
                "Group limit contained invalid group(s), ignoring: "
                f"{[host for host in invalid_groups]}"
            )
        inv = inv.filter(filter_func=lambda h: any(True for g in valid_groups if g in h.groups))
    return inv


def patch_config(cli_args: dict, conf: Config) -> Config:
    """
    Patch nornir core configurations per cli arguments.

    Arguments:
        cli_args: Updates from CLI to update in Nornir objects
        conf: nornir.core.configuration.Config object; Initialized Nornir Config object

    Returns:
        conf: nornir.core.configuration.Config object; Updated Nornir Config object

    Raises:
        N/A  # noqa

    """
    if cli_args["workers"]:
        conf.core.num_workers = cli_args["workers"]

    return conf


def nornsible_task_message(msg: str) -> None:
    """
    Handle printing pretty messages for nornsible_task decorator

    Args:
        msg: message to beautifully print to stdout

    Returns:
         N/A

    Raises:
        N/A  # noqa

    """
    LOCK.acquire()
    try:
        print(f"{Style.BRIGHT}{Back.CYAN}{Fore.WHITE}{msg}{'-' * (80 - len(msg))}")
    finally:
        LOCK.release()


def nornsible_task(wrapped_func: Callable) -> Callable:
    """
    Decorate an "operation" -- execute or skip the operation based on tags

    Args:
        wrapped_func: function to wrap in tag processor

    Returns:
        tag_wrapper: wrapped function

    Raises:
        N/A  # noqa

    """

    def tag_wrapper(
        task: Task, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Union[Callable, Result]:
        if {wrapped_func.__name__}.intersection(task.nornir.skip_tags):
            msg = f"---- {task.host} skipping task {wrapped_func.__name__} "
            nornsible_task_message(msg)
            return Result(host=task.host, result="Task skipped!", failed=False, changed=False)
        if not task.nornir.run_tags:
            return wrapped_func(task, *args, **kwargs)
        if {wrapped_func.__name__}.intersection(task.nornir.run_tags):
            return wrapped_func(task, *args, **kwargs)
        msg = f"---- {task.host} skipping task {wrapped_func.__name__} "
        nornsible_task_message(msg)
        return Result(host=task.host, result="Task skipped!", failed=False, changed=False)

    tag_wrapper.__name__ = wrapped_func.__name__
    return tag_wrapper


def InitNornsible(nr: Nornir) -> Nornir:
    """
    Patch nornir object based on cli arguments

    Arguments:
        nr: Nornir object

    Returns:
        nr: Nornir object; modified if cli args dictate the need to do so; otherwise passed as is

    Raises:
        N/A  # noqa

    """
    cli_args = parse_cli_args(sys.argv[1:])

    nr.run_tags = cli_args.pop("run_tags")
    nr.skip_tags = cli_args.pop("skip_tags")

    if any(a for a in cli_args.values()):
        nr.config = patch_config(cli_args, nr.config)
        nr.inventory = patch_inventory(cli_args, nr.inventory)
        return nr

    return nr
