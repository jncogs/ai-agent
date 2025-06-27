import os

def write_file(working_directory, file_path, content):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))

    if not fullpath.startswith(os.path.join(os.path.abspath(working_directory))):
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
    
    directory = os.path.dirname(fullpath)
    
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            return f"Error: could not create \"{directory}\" for some reason"
    
    try:
        with open(fullpath, "w") as f:
            f.write(content)
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except:
        return f"Error: Could not write to \"{file_path}\""