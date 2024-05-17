import os

# Define the folder containing the files (use '.' for the current directory)
folder_path = "."

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the filename starts with 'test_'
    if filename.startswith("test_"):
        # Define the new filename without the prefix
        new_filename = filename[5:]  # Remove the first 5 characters 'test_'
        # Generate the full paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed "{filename}" to "{new_filename}"')

print("Renaming complete.")
