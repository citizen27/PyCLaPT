import os
import shutil
from zipfile import ZipFile
from tqdm import tqdm

# Define the source directories
firefox_source_path1 = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Mozilla", "Firefox")
firefox_source_path2 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox")
chrome_source_path1 = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Default")

# Define custom names for the zip files
firefox_zip_name1 = "Local_Firefox.zip"
firefox_zip_name2 = "Roaming_Firefox.zip"
chrome_zip_name1 = "Chrome_UserData.zip"

# Define the destination folder
destination_folder = os.path.join(os.path.expanduser("~"), "Desktop", "CLaPT_Output", "Collected Internet Artifacts")

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Function to copy files with a custom copy function
def copy_files_with_progress(source_path, destination_path, skipped_files_log):
    for root, _, files in os.walk(source_path):
        for file in tqdm(files, desc=f"Copying files", unit="file"):
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_path)
            destination_file = os.path.join(destination_path, relative_path)

            try:
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                shutil.copy2(source_file, destination_file)
            except FileNotFoundError:
                print(f"File not found: {source_file}. Skipping...")
                with open(skipped_files_log, 'a') as log_file:
                    log_file.write(f"File not found: {source_file}\n")
                continue
            except Exception as e:
                print(f"Error copying {source_file}: {e}")
                continue


# Function to copy folders and zip files with progress
def copy_and_zip_folders(source_path, zip_file_name):
    if os.path.exists(source_path):
        # Define the zip file path with the custom name
        zip_file_path = os.path.join(destination_folder, zip_file_name)

        # Define the destination path
        destination_path = os.path.join(destination_folder, os.path.basename(source_path))

        # Define the skipped files log file
        skipped_files_log = os.path.join(destination_folder, "skipped_files_log.txt")

        # Check if the destination folder exists and remove it
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        # Copy files with progress and log skipped files
        copy_files_with_progress(source_path, destination_path, skipped_files_log)

        # Create the custom-named zip file with progress bar
        with ZipFile(zip_file_path, 'w') as zipf:
            files = [f for f in os.listdir(destination_path) if os.path.isfile(os.path.join(destination_path, f))]
            for file in tqdm(files, desc=f"Zipping {zip_file_name}", unit="file"):
                file_path = os.path.join(destination_path, file)
                arc_name = os.path.relpath(file_path, destination_path)
                zipf.write(file_path, arc_name)

# Call the function to copy and zip folders with custom names
copy_and_zip_folders(firefox_source_path1, firefox_zip_name1)
copy_and_zip_folders(firefox_source_path2, firefox_zip_name2)
copy_and_zip_folders(chrome_source_path1, chrome_zip_name1)
