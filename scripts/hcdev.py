"""
Script to aid with HomeControl development
"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
import logging
from pathlib import Path
import subprocess
import sys
import tomllib

logger = logging.getLogger()

PACKAGES_DIRECTORY = Path("./packages")


def run_shell_command(args: list[str], capture_output: bool = False):
    """Run a shell command"""

    return subprocess.run(
        args,
        check=True,
        capture_output=capture_output,
    )


def get_package_dependencies(package_dir: Path) -> list[str]:
    """Returns the dependencies of a package with the given path"""

    with open(package_dir / "pyproject.toml", "rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)
        dependencies = pyproject_data["project"].get("dependencies")
    return dependencies


def find_local_package_names() -> list[str]:
    """Returns a list of the local homecontrol package names"""

    logger.info("Finding local packages...")
    package_names = [
        folder.name for folder in PACKAGES_DIRECTORY.glob("*") if folder.is_dir()
    ]
    logger.info("Found %s", ", ".join(package_names))
    return package_names


def setup_venv(package_name: str):
    """Sets up the venv of the a local homecontrol package given its path"""

    package_dir = PACKAGES_DIRECTORY / package_name
    package_dependencies = get_package_dependencies(package_dir)

    # Figure out which homecontrol packages are required (remove any GitHub references)
    required_homecontrol_packages = [
        package_dependency.split("@")[0]
        for package_dependency in package_dependencies
        if package_dependency.startswith("homecontrol")
    ]

    logger.info("Creating venv for %s...", package_name)

    # Create a venv for the package
    run_shell_command([sys.executable, "-m", "venv", f"{package_dir}/.venv"])

    # Install each local dependency as required
    for required_homecontrol_package in required_homecontrol_packages:
        logger.info("Installing homecontrol dependencies for %s...", package_name)

        run_shell_command(
            [
                f"{package_dir}/.venv/bin/python",
                "-m",
                "pip",
                "install",
                "-e",
                PACKAGES_DIRECTORY / required_homecontrol_package,
            ],
            capture_output=True,
        )

    # Now setup the package itself
    run_shell_command(
        [
            f"{package_dir}/.venv/bin/python",
            "-m",
            "pip",
            "install",
            "-e",
            package_dir,
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


class CommandSetup(BaseCommand):
    """Command to setup a development environment"""

    help: str = "Sets up a development environment"

    def add_arguments(self, parser: ArgumentParser):
        pass

    def run(self, args: Namespace):
        # Obtain a list of the packages to setup
        package_names = find_local_package_names()

        # TODO: This may need to be recursive later

        # Want to setup each package separately
        for package_name in package_names:
            setup_venv(package_name)


class CommandUpdateRequirements(BaseCommand):
    """Command to update the requirements.txt in each package"""

    help: str = "Updates all requirements.txt's"

    def add_arguments(self, parser: ArgumentParser):
        pass

    def run(self, args: Namespace):
        # Obtain a list of the packages to update
        package_names = find_local_package_names()

        # Want to update each package separately
        for package_name in package_names:
            # Delete the existing venv
            package_dir = PACKAGES_DIRECTORY / package_name

            # Remove the existing venv
            logger.info("Removing the existing venv for %s", package_name)
            run_shell_command(["rm", "-rf", package_dir / ".venv"])

            # Setup the new venv
            setup_venv(package_name)

            # Save the result of pip freeze in a requirements.txt
            result = run_shell_command(
                [
                    f"{package_dir}/.venv/bin/python",
                    "-m",
                    "pip",
                    "freeze",
                ],
                capture_output=True,
            )
            requirements = result.stdout.decode().split("\n")

            # Requirements for production
            with open(
                package_dir / "requirements.txt", "w", encoding="utf-8"
            ) as requirements_file:
                for requirement in requirements:
                    if requirement and package_name not in requirement:
                        if (
                            "git+ssh://git@github.com/2851999/homecontrol-mono.git"
                            in requirement
                        ):
                            requirements_file.write(
                                requirement.replace("-e ", "") + "\n"
                            )
                        else:
                            requirements_file.write(requirement + "\n")

            # Requirements for dev
            with open(
                package_dir / "requirements-dev.txt", "w", encoding="utf-8"
            ) as requirements_file:
                for requirement in requirements:
                    if requirement and package_name not in requirement:
                        if (
                            "git+ssh://git@github.com/2851999/homecontrol-mono.git"
                            in requirement
                        ):
                            dev_package = requirement.split("=")[-1]
                            requirements_file.write(f"./{dev_package}\n")
                        else:
                            requirements_file.write(requirement + "\n")


COMMANDS: dict[str, BaseCommand] = {
    "setup": CommandSetup(),
    "update-requirements": CommandUpdateRequirements(),
}


def main():
    """Execute the main script"""

    parser = ArgumentParser(
        prog="hcdev", description="Script to aid with HomeControl development"
    )
    subparsers = parser.add_subparsers(
        title="Subcommands", help="Subcommand help", dest="subcommand", required=True
    )

    # Add the commands
    for command_key, command in COMMANDS.items():
        subparser = subparsers.add_parser(command_key, help=command.help)
        command.add_arguments(subparser)

    logging.basicConfig(level=logging.INFO)

    # Parse and initiate the command
    args = parser.parse_args()
    COMMANDS[args.subcommand].run(args)


if __name__ == "__main__":
    main()
