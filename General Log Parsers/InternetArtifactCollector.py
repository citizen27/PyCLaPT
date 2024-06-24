import os
import shutil
from zipfile import ZipFile
from tqdm import tqdm


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def copy_files_with_progress(source_path, destination_path, skipped_files_log):
    for root, _, files in os.walk(source_path):
        for file in tqdm(files, desc=f"Copying files", unit="file"):
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_path)
            destination_file = os.path.join(destination_path, relative_path)

            try:
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                shutil.copy2(source_file, destination_file)
            except (FileNotFoundError, Exception) as e:
                error_message = f"Error copying {source_file}: {e}"
                print(error_message)
                with open(skipped_files_log, "a") as log_file:
                    log_file.write(f"{error_message}\n")
                continue


def copy_and_zip_folders(source_path, zip_file_name):
    if os.path.exists(source_path):
        destination_folder = os.path.join(
            os.path.expanduser("~"),
            "Desktop",
            "CLaPT_Output",
            "Collected Internet Artifacts",
        )
        create_directory(destination_folder)

        destination_path = os.path.join(
            destination_folder, os.path.basename(source_path)
        )
        skipped_files_log = os.path.join(destination_folder, "skipped_files_log.txt")

        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        copy_files_with_progress(source_path, destination_path, skipped_files_log)

        zip_file_path = os.path.join(destination_folder, zip_file_name)
        with ZipFile(zip_file_path, "w") as zipf:
            files = [
                f
                for f in os.listdir(destination_path)
                if os.path.isfile(os.path.join(destination_path, f))
            ]
            for file in tqdm(files, desc=f"Zipping {zip_file_name}", unit="file"):
                file_path = os.path.join(destination_path, file)
                arc_name = os.path.relpath(file_path, destination_path)
                zipf.write(file_path, arc_name)


# Define the source directories
firefox_source_paths = [
    os.path.join(os.path.expanduser("~"), "AppData", folder, "Mozilla", "Firefox")
    for folder in ["Local", "Roaming"]
]
chrome_source_path = os.path.join(
    os.path.expanduser("~"),
    "AppData",
    "Local",
    "Google",
    "Chrome",
    "User Data",
    "Default",
)

# Define custom names for the zip files
firefox_zip_names = ["Local_Firefox.zip", "Roaming_Firefox.zip"]
chrome_zip_name = "Chrome_UserData.zip"

# Call the function to copy and zip folders with custom names
for path, name in zip(firefox_source_paths, firefox_zip_names):
    copy_and_zip_folders(path, name)

copy_and_zip_folders(chrome_source_path, chrome_zip_name)