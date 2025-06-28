# *THIS README BUILT USING AI PROMPT:*
Please try writing out a basic README in Markdown format describing the functions in main.py and how they work in detail. Add an additional heading at the top with '#*THIS README BUILT USING AI PROMPT:*' followed by the prompt in standard text. Output to README.md.

## Description
This Python script, `main.py`, acts as an AI coding agent that can interact with the file system using function calls. It leverages the Gemini API to process user prompts, create function call plans, and execute those plans by interacting with the available functions.

## Available Functions
The script defines and utilizes the following functions:

*   **`get_files_info(directory)`**: Lists files and directories within a specified directory. If no directory is specified, it lists files in the working directory. It returns a dictionary containing file names and sizes.
*   **`get_file_content(file_path)`**: Reads and returns the content of a specified file. The content is truncated to a maximum of 10000 characters. It returns a dictionary with the file content.
*   **`run_python_file(file_path)`**: Executes a specified Python file. It returns a dictionary with the execution result.
*   **`write_file(file_path, content)`**: Writes the given content to the specified file. If the file does not exist, it will be created. If it exists, it will be overwritten. It returns the number of characters written to the file.

## How it Works

1.  **Initialization:**
    *   The script loads environment variables, specifically the Gemini API key.
    *   It initializes the Gemini API client.
    *   It takes a user prompt as a command-line argument.
2.  **Function Definition:**
    *   Defines the schemas for each available function, specifying their names, descriptions, and parameters. This allows the Gemini model to understand the available tools.
3.  **AI Interaction Loop:**
    *   The script enters a loop where it sends the user prompt and system prompt to the Gemini model.
    *   The Gemini model analyzes the prompt and generates a response, which may include function calls.
    *   If the response contains function calls, the script extracts the function name and arguments.
    *   The script then calls the appropriate Python function with the provided arguments.
    *   The result of the function call is sent back to the Gemini model.
    *   The loop continues until the Gemini model provides a final response without any function calls or until a maximum number of iterations is reached.
4.  **Output:**
    *   The final response from the Gemini model is printed to the console.

## Usage

To run the script, you need to provide a prompt as a command-line argument:

```bash
python main.py "Your prompt here"
```

For example:

```bash
python main.py "List all files in the current directory."
```

## Dependencies

*   `os`
*   `sys`
*   `dotenv`
*   `google.generativeai`

## Environment Variables

The script requires the following environment variable to be set:

*   `GEMINI_API_KEY`: Your Gemini API key.
