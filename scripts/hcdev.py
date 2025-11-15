"""
Script to aid with HomeControl development
"""

import logging
import subprocess
import sys
import tomllib
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from pathlib import Path

logger = logging.getLogger()

PACKAGES_DIRECTORY = Path("./packages")


def run_shell_command(args: list[str], capture_output: bool = False):
    """Run a shell command"""

    logger.debug("Running command '%s'", " ".join([str(arg) for arg in args]))
    result = subprocess.run(
        args,
        check=False,
        capture_output=capture_output,
    )
    if result.stdout:
        logger.debug(result.stdout.decode())
    if result.stderr:
        logger.debug(result.stderr.decode())
    result.check_returncode()
    return result


def find_local_package_names() -> list[str]:
    """Returns a list of the local homecontrol package names"""

    logger.info("Finding local packages...")
    package_names = [folder.name for folder in PACKAGES_DIRECTORY.glob("*") if folder.is_dir()]
    logger.info("Found %s", ", ".join(package_names))
    return package_names


def sync(package_name: str):
    """Syncs the a local homecontrol package given its path"""

    package_dir = PACKAGES_DIRECTORY / package_name

    logger.info("Syncing %s...", package_name)

    # Sync package with uv
    run_shell_command(["uv", "sync", "--directory", package_dir, "--extra", "dev"])


def install_optional_dependencies(package_name: str, key: str):
    """
    Installs optional dependencies to a specific package's venv
    """

    package_dir = PACKAGES_DIRECTORY / package_name
    run_shell_command(
        [
            f"{package_dir}/.venv/bin/python",
            "-m",
            "pip",
            "install",
            "-e",
            f"{package_dir}[{key}]",
        ],
        capture_output=True,
    )


class BaseCommand(ABC):
    """Base class for all commands"""

    @abstractmethod
    def add_arguments(self, parser: ArgumentParser):
        """Should add any arguments this command requires"""

    @abstractmethod
    def run(self, args: Namespace):
        """Should run the command"""

    @property
    @abstractmethod
    def help(self) -> str:
        """Should return the help message for this command"""
        return "Generic help message"


class CommandSync(BaseCommand):
    """Command to setup a development environment"""

    help: str = "Sets up a development environment"

    def add_arguments(self, parser: ArgumentParser):
        pass

    def run(self, args: Namespace):
        # Obtain a list of the packages to setup
        package_names = find_local_package_names()

        # Setup each package separately
        for package_name in package_names:
            sync(package_name)


class CommandUpgrade(BaseCommand):
    """Command to upgrade all packages in each package"""

    help: str = "Updates all requirements.txt's"

    def add_arguments(self, parser: ArgumentParser):
        pass

    def run(self, args: Namespace):
        # Obtain a list of the packages to update
        package_names = find_local_package_names()

        # Update each package separately
        for package_name in package_names:
            package_dir = PACKAGES_DIRECTORY / package_name

            # Update the packages
            logger.info("Updating all packages for %s", package_name)

            # Save the result of pip freeze in a requirements.txt
            run_shell_command(["uv", "lock", "--upgrade", "--directory", package_dir])


COMMANDS: dict[str, BaseCommand] = {
    "sync": CommandSync(),
    "upgrade": CommandUpgrade(),
}


def main():
    """Execute the main script"""

    parser = ArgumentParser(prog="hcdev", description="Script to aid with HomeControl development")
    parser.add_argument("--debug", action="store_true", help="Expand logging to debug logs")
    subparsers = parser.add_subparsers(title="Subcommands", help="Subcommand help", dest="subcommand", required=True)

    # Add the commands
    for command_key, command in COMMANDS.items():
        subparser = subparsers.add_parser(command_key, help=command.help)
        command.add_arguments(subparser)

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Initiate the command
    COMMANDS[args.subcommand].run(args)


if __name__ == "__main__":
    main()
