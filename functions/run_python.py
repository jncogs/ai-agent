import os
import subprocess

def run_python_file(working_directory, file_path):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))

    if not fullpath.startswith(os.path.join(os.path.abspath(working_directory))):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(fullpath):
        return f"Error: File \"{file_path}\" not found."
    
    directory, file_extension = os.path.splitext(fullpath)
    if file_extension != ".py" and file_extension != ".PY":
        return f"Error: \"{file_path}\" is not a Python file."
    
    commands = [
        "python",
        file_path,
    ]

    try:
        result = subprocess.run(commands,
                                cwd=working_directory,
                                text=True,
                                timeout=30,
                                capture_output=True
                                )
    except:
        return f"Error: executing Python file: {file_path}"
    
    output = []
    output.append(f"STDOUT:{result.stdout}")
    output.append(f"STDERR:{result.stderr}")
    if result.returncode != 0:
        output.append(f"Process existed with code {result.returncode}")
    
    if result.stdout == None:
        return "No output produced"

    return output