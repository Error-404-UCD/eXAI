import os
# Use this class if you want to rename your directories as required for classification
class FileManager:
    # script to change label file names
    def rename_files_in_directory(root_dir):
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
    root_directory = "./../../data/MNIST"
    if os.path.isdir(root_directory):
        FileManager.rename_files_in_directory(root_directory)
    else:
        print(f"The provided path {root_directory} is not a valid directory.")