import os
import shutil
from zipfile import ZipFile

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

# Function to copy folders and zip files with progress
def copy_and_zip_folders(source_path, zip_file_name):
    if os.path.exists(source_path):
        # Define the zip file path with the custom name
        zip_file_path = os.path.join(destination_folder, zip_file_name)

        # Copy the source folder
        shutil.copytree(source_path, os.path.join(destination_folder, os.path.basename(source_path)))

        # Create the custom-named zip file
        with ZipFile(zip_file_path, 'w') as zipf:
            for root, dirs, files in os.walk(os.path.join(destination_folder, os.path.basename(source_path))):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, os.path.join(destination_folder, os.path.basename(source_path)))
                    zipf.write(file_path, arc_name)

# Call the function to copy and zip folders with custom names
copy_and_zip_folders(firefox_source_path1, firefox_zip_name1)
copy_and_zip_folders(firefox_source_path2, firefox_zip_name2)
copy_and_zip_folders(chrome_source_path1, chrome_zip_name1)
