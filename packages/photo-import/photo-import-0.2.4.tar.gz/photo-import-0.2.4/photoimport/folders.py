"""All the functionality to do with the filesystem

:copyright: Copyright 2019 Edward Armitage.
:license: MIT, see LICENSE for details.
"""
import os
import shutil
from datetime import date
from pathlib import Path
from typing import List, Iterable, Union


class FileMover:
    """Class for moving files into a date-organised hierarchy"""

    # pylint: disable=too-few-public-methods

    def __init__(self, base_path: str, month_only: bool) -> None:
        """
        :param base_path: The directory to build the date-organised hierarchy within
        :param month_only: Whether to store all files for a given month in the same folder, rather
                than separating by day (default is False)
        """
        self._base_path = Path(base_path)
        self._month_only = month_only

    def move_files(self, folder_date: date, paths: Union[Path, Iterable[Path]]) -> None:
        """Moves files into the appropriate directory for the given date

        If the required folder does not already exist, it will be created. If a top-level folder
        already exists (e.g. the year or month folder), the lower level (e.g. month or date)
        folders will be created alongside any existing files, and the file copied into the newly
        created directory.

        :param folder_date: The date to move the file into the directory for
        :param paths: The paths of the files to be moved
        """
        directory = self._build_path(folder_date)
        os.makedirs(directory, exist_ok=True)

        for file in [paths] if not isinstance(paths, Iterable) else list(paths):
            shutil.move(str(file), directory)

    def _build_path(self, folder_date: date) -> str:
        year = "{:04d}".format(folder_date.year)
        month = "{:02d}".format(folder_date.month)
        day = "{:02d}".format(folder_date.day)

        if self._month_only:
            path = os.path.join(str(self._base_path), year, month)
        else:
            path = os.path.join(str(self._base_path), year, month, day)

        return path


def find_all_associated_files(file: Path) -> List[Path]:
    """Finds the companion files alongside the provided the file in a given directory

    A companion file is a file within the same directory as the original file, with the same
    name (ignoring file extensions). For example photo-001.raw is a companion to photo-001.jpg,
    but photo-0011.jpg is not.

    :param file: The file to find companions for
    :return: a list of Paths containing the provided file and all companion files
    """
    return list(file.parent.glob("{}.*".format(file.stem)))
