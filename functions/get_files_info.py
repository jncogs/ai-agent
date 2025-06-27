import os

def get_files_info(working_directory, directory=None):
    fullpath = os.path.abspath(os.path.join(working_directory, directory))

    #return f"{fullpath}"

    if not fullpath.startswith(os.path.join(os.path.abspath(working_directory))):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(fullpath):
        return f"Error: \"{directory}\" is not a directory"
    
    contents = os.listdir(fullpath)
    output = []

    for file in contents:
        try:
            output.append(f"{file}: file_size={os.path.getsize(fullpath + "/" + file)} bytes, is_dir={os.path.isdir(fullpath + "/" + file)}")
        except:
            return(f"Error: cannot parse file \"{file}\"\n{fullpath}")
    
    return "\n".join(output)
