import os

class FileManager:
    """
    A class used to manage file operations in a directory.

    Methods
    -------
    rename_files_in_directory(root_dir : str)
        Renames all files in the given directory and its subdirectories.
        The new name for each file is based on the containing folder name and an index.
    """
    def rename_files_in_directory(root_dir):
        """
        Rename files in a directory and its subdirectories.

        Parameters
        ----------
        root_dir : str
            The root directory where the files to be renamed are located. The function will traverse all subdirectories.

        Returns
        -------
        None
        """

        for dirpath, dirnames, filenames in os.walk(root_dir):
            folder_name = os.path.basename(dirpath)
            for i, filename in enumerate(filenames):
                file_ext = os.path.splitext(filename)[1]
                new_name = f"{folder_name}_{i + 1}{file_ext}"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    """
    The main function that checks if the provided root directory is valid 
    and then calls the rename_files_in_directory method to rename files.

    Parameters
    ----------
    root_directory : str
        The path to the root directory where files need to be renamed.
    
    Returns
    -------
    None
    """
    root_directory = "./../../data/MNIST"
    if os.path.isdir(root_directory):
        FileManager.rename_files_in_directory(root_directory)
    else:
        print(f"The provided path {root_directory} is not a valid directory.")