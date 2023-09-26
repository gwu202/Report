import  os
import shutil


def all_existing_files(directory) -> set:
    all_files = [file for file in os.listdir(directory) if not file.endswith('.crdownload')]
    print("Directory Content ")
    print(all_files)
    return set(all_files)


def create_empty_directory(directory_path):
    # Check if the directory already exists

    if os.path.exists(directory_path):
        # If it exists, remove all its content
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        # If it doesn't exist, create the directory
        os.makedirs(directory_path)
