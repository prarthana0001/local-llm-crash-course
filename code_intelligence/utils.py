import os
from typing import Generator, Optional


def find_py_files(
    root_dir: str,
    exclude_tests: bool = True,
    exclude_hidden: bool = True
) -> Generator[str, None, None]:
    """
    Walk through a directory and yield all .py file paths.

    Parameters:
        root_dir (str): Path to root directory to scan.
        exclude_tests (bool): If True, skip test files.
        exclude_hidden (bool): If True, skip dotfiles and hidden dirs.
    """
    for root, dirs, files in os.walk(root_dir):
        # Optionally skip hidden directories
        if exclude_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if not file.endswith(".py"):
                continue
            if exclude_tests and ("test" in file.lower() or file.startswith("test_")):
                continue
            if exclude_hidden and file.startswith("."):
                continue

            yield normalize_path(os.path.join(root, file))


def normalize_path(path: str) -> str:
    """
    Normalize file paths to use forward slashes and absolute paths.
    """
    return os.path.abspath(path).replace("\\", "/")
