import os

def get_file_content(working_directory, file_path):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))

    if not fullpath.startswith(os.path.join(os.path.abspath(working_directory))):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(fullpath):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    
    MAX_CHARS = 10000

    with open(fullpath, "r") as f:
        try:
            file_content_string = f.read(MAX_CHARS)
        except:
            return f"Error: Could not open {file_path}"
    
    if len(file_content_string) == MAX_CHARS:
        return file_content_string + f"\n[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
    return file_content_string