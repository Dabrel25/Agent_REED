import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import file_commands


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


if len(sys.argv) < 2:
    print("Please include a prompt:")
    sys.exit(1)

prompt = sys.argv[1]


messages = [
    types.Content(role = 'user', parts = [types.Part(text = prompt)])
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
    description="Reads the contents of a file and returns it as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. Must be a regular file, not a directory.",
            ),
        }
    )
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory. This should not overwrite existing files.",
            ),
        }
    )
)
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes content to a file, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file to write, relative to the working directory. This should not overwrite existing files.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The content to write to the file.",
            ),
        }
    )
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file,
    ]
)


function_map = {
    "get_files_info": file_commands.get_files_info,
    "get_file_content": file_commands.get_file_content,
    "run_python_file": file_commands.run_python_file,
    "write_file":  file_commands.write_file,

}

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_name in function_map:
        function_args["working_directory"] = "./calculator"
        actual_function = function_map[function_name]
        function_execution = actual_function(**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_execution},
                )
            ],
        )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


for i in range(20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.candidates[0].content.parts[0].function_call:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_result = call_function(part, "--verbose" in sys.argv)
                messages.append(function_call_result)
    else:
        # There are NO function calls - agent is done!
        print(f"Final response:\n{response.text}")
        break  # Exit the loop

if ("--verbose" in sys.argv):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls:
    for function_call_part in response.function_calls:

        function_call_result = call_function(function_call_part, "--verbose" in sys.argv)

        # Check if the result has the expected structure and print if verbose
        if function_call_result.parts[0].function_response.response:
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            raise Exception("Function call failed to return expected response structure")
else:
    print(f"Response: {response.text}")