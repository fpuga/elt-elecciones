"""Usage example.

def my_function(data):
    # your function implementation here
    return len(data)


def file_filter(filename):
    return filename.endswith(".txt")


processor = ZipFileProcessor("my_archive.zip")
processor.add_function(FileFunction(file_filter, my_function))
processor.process()
"""

# Take care, rigth know this method is extracting the files more than one time
# when multiple functions used
import os
import tempfile
import zipfile


class FileFunction(object):
    """A class that represents a function to be applied to a file."""

    def __init__(self, filter_function, apply_function, apply_function_config=None):
        """Initialize a FileFunction object.

        Args:
            filter_function (function): A function that takes a file name as input and returns True if the file should be processed, False otherwise.
            apply_function (function): A function that takes file data as input and performs some operation on it.
            apply_function_config (dict): Aditional parameters for the apply_function
        """
        self._filter_function = filter_function
        self._apply_function = apply_function
        self._apply_function_config = apply_function_config

    def filter(self, filename):
        return self._filter_function(filename)

    def apply(self, data):
        return self._apply_function(data, self._apply_function_config)


class ZipFileProcessor(object):
    """A class for processing files in a zip archive based on a filter and applyable function."""

    def __init__(self, archive_file):
        """Initialize a ZipFileProcessor object.

        Args:
            archive_file (str): The path to the zip archive file.
        """
        self.archive_file = archive_file
        self.functions = []

    def add_function(self, file_function):
        self.functions.append(file_function)

    def process_on_raw_data(self):
        """Process files in the zip archive based on the filter and applyable function."""
        with zipfile.ZipFile(self.archive_file, "r") as archive:
            for file in archive.namelist():
                for func in self.functions:
                    if func.filter(file):
                        data = archive.read(file)
                        func.apply(data)

    def process_on_all_extracted(self):
        with zipfile.ZipFile(self.archive_file, "r") as archive:
            with tempfile.TemporaryDirectory() as tempdir:
                archive.extractall(tempdir)
                for file in os.listdir(tempdir):
                    for func in self.functions:
                        if func.filter(file):
                            func.apply(os.path.join(tempdir, file))

    def process(self):
        with zipfile.ZipFile(self.archive_file, "r") as archive:
            with tempfile.TemporaryDirectory() as tempdir:
                for file in archive.namelist():
                    for func in self.functions:
                        if func.filter(file):
                            filepath = archive.extract(file, tempdir)
                            func.apply(filepath)
