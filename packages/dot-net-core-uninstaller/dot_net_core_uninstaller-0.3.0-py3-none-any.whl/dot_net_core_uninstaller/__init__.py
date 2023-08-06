import logging
import os
import platform
import re
import shutil
import subprocess
import sys

import tabulate

__all__ = ["__version__", "Uninstaller"]

__version__ = '0.3.0'

WINDOWS_DOTNET_PATH = 'C:\\ProgramData\\Package Cache'


def is_windows() -> bool:
    """
    Checks is the current OS is windows or not.

    :return: ``True`` for windows OS
    """
    if platform.system().lower() == 'windows':
        return True
    return False


class Uninstaller:
    """
    Removes the version .Net Core SDK and Runtime.
    """

    def __init__(self):
        """
        :raise FileNotFoundError
        """

        try:
            dotnet_version = subprocess.check_output(["dotnet", "--version"]).strip()
            print(f".Net Version found: {dotnet_version.decode('utf-8')}")
        except FileNotFoundError as e:
            logging.error(".Net Core SDK is not installed")
            sys.exit(1)

    @staticmethod
    def _list_dotnet_sdks():
        dotnet_sdks = subprocess.check_output(["dotnet", "--list-sdks"]).decode('utf-8').split('\n')[:-1]

        return dotnet_sdks

    @staticmethod
    def _list_dotnet_runtimes():
        dotnet_runtimes = subprocess.check_output(["dotnet", "--list-runtimes"]).decode('utf-8').split('\n')[:-1]

        return dotnet_runtimes

    def convert_to_dict(self) -> dict:
        """
        Converts subprocess requests to dictionary.

        :return: A dictionary of version number with its path
        :rtype: dict
        """

        _sdk = []
        _runtime = []

        for sdk in self._list_dotnet_sdks():
            sdk_version = re.search(r"\d+\.\d+\.?\d+", sdk).group(0)
            sdk_path = re.search(r"\[.*?\]", sdk).group(0)
            _sdk.append([sdk_version, sdk_path[1:-1]])

        for runtime in self._list_dotnet_runtimes():
            runtime_version = re.search(r"\d+\.\d+\.?\d+", runtime).group(0)
            runtime_path = re.search(r"\[.*?\]", runtime).group(0)
            _runtime.append([runtime_version, runtime_path[1:-1]])

        out = {
            "sdk": {},
            "runtime": {}
        }
        for key, val in _sdk:
            out['sdk'].setdefault(key, []).append(os.path.join(val, key))
        for key, val in _runtime:
            out['runtime'].setdefault(key, []).append(os.path.join(val, key))

        return out

    def delete_sdk(self, version: str = None):
        """
        Deletes the path of the given version, if available.

        :param version: Version number of .Net Core SDK to delete
        :raise OSError
        """

        if is_windows():
            raise OSError("This method is not supported in Windows, use 'delete_sdk_runtime_windows()'")

        converted_dict = self.convert_to_dict()

        if version:
            _sdk_path = converted_dict['sdk'].get(version)
            if not _sdk_path:
                print(f"Paths not found for .Net Core SDK version {version}.")
                sys.exit(1)

            print()
            print(tabulate.tabulate([[p] for p in _sdk_path],
                                    headers=[f"Deleting SDK Version: {version}"],
                                    tablefmt="grid", colalign=("center",)))

            for path in _sdk_path:
                shutil.rmtree(path)

            print("Done.")

    def delete_runtime(self, version: str = None):
        """
        Deletes the path of the given version, if available.

        :param version: Version number of .Net Core Runtime to delete
        :raise OSError
        """

        if is_windows():
            raise OSError("This method is not supported in Windows, use 'delete_sdk_runtime_windows()'")

        converted_dict = self.convert_to_dict()

        if version:
            _runtime_paths = converted_dict['runtime'].get(version)
            if not _runtime_paths:
                print(f"Paths not found for .Net Core Runtime version {version}.")
                sys.exit(1)

            print()
            print(tabulate.tabulate([[p] for p in _runtime_paths],
                                    headers=[f"Deleting Runtime Version: {version}"],
                                    tablefmt="grid", colalign=("center",)))

            for path in _runtime_paths:
                shutil.rmtree(path)

            print("Done.")

    def list_dotnet(self):
        """
        Lists all the installed .Net Core SDKs and Runtimes.
        """
        paths = self.convert_to_dict()

        print()
        print(tabulate.tabulate([[p, "\n".join(v)] for p, v in paths['sdk'].items()],
                                headers=["SDK Version", "Path"],
                                tablefmt="grid", colalign=("center",)))
        print()
        print(tabulate.tabulate([[p, "\n".join(v)] for p, v in paths['runtime'].items()],
                                headers=["Runtime Version", "Path"],
                                tablefmt="grid", colalign=("center",)))

    def delete_sdk_runtime_windows(self, version: str):
        """
        Uninstalls .Net core SDK from windows.

        :raise OSError
        :raise AttributeError
        :raise FileNotFoundError
        """

        if not is_windows():
            raise OSError("This method is not supported in POSIX, use 'delete_sdk()' or 'delete_runtime()'")

        sdk_versions = [sdk_versions for sdk_versions in self.convert_to_dict()['sdk']]

        sdk_path = None

        if version in sdk_versions and is_windows():
            for root, dirs, files in os.walk(WINDOWS_DOTNET_PATH):
                for file in files:
                    logging.debug("Searching in path - %s", file)
                    try:
                        if re.search(rf'dotnet-sdk-{version}.*', file).group(0):
                            logging.debug('Found SDK in - %s', file)
                            sdk_path = os.path.join(root, file)
                    except AttributeError:
                        pass
        else:
            print(f".Net Core SDK {version} not found.")

        if sdk_path is not None:
            print("Opening the uninstaller")
            subprocess.run([sdk_path, '/passive', '/uninstall'])
            print(f'.Net Core SDK version {version} removed.')
        else:
            FileNotFoundError("Uninstaller not found, use Control Panel to uninstall")

