import os
import sys

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide hould be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt string>")
        sys.exit(1)
        
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads file content for the specified file, constrained to the working directory. Truncates to 10000 characters.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file name to get content from, relative to the working directory."
                )
            }
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs given Python file, relative to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file name to run. Must be a Python file with extension .py."
                )
            }
        )
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes given content to given file path, constrained to the working directory. Creates new directory if specified does not exist. Returns number of characters written to file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Target file name to write content to. Will be created if file does not exist and will overwrite file if it does."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to file."
                )
            }
        )
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    def call_function(function_call_part, verbose=False):
        function_name = function_call_part.name
        args = function_call_part.args

        if verbose:
            print(f"Calling function: {function_name}({args})")
        print(f" - Calling function: {function_name}")

        args["working_directory"] = "./calculator"

        functions = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }
        
        if function_name in functions.keys():
            function_result = functions[function_name](**args)
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ]
            )
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
        
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
    )

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part)

        if function_call_result.parts[0].function_response.response == None:
            raise Exception("Your shit's fucked up")
        
        if sys.argv[-1] == "--verbose":
            print(f"-> {function_call_result.parts[0].function_response.response}")

    '''if response.function_calls != None:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

        if sys.argv[-1] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")'''

if __name__ == "__main__":
    main()