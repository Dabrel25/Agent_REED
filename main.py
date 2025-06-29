import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import file_commands

# Parse command line arguments
verbose = "--verbose" in sys.argv

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Validate API key
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Check for prompt argument
if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] == "--verbose"):
    print("Usage: python script.py [--verbose] \"<your prompt>\"")
    print("Please include a prompt as an argument")
    sys.exit(1)

# Extract prompt (handle verbose flag)
if "--verbose" in sys.argv:
    # Remove --verbose from argv to get the actual prompt
    args_without_verbose = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    if not args_without_verbose:
        print("Usage: python script.py [--verbose] \"<your prompt>\"")
        print("Please include a prompt as an argument")
        sys.exit(1)
    prompt = args_without_verbose[0]
else:
    prompt = sys.argv[1]

# Initialize messages
messages = [
    types.Content(role='user', parts=[types.Part(text=prompt)])
]

# Function schemas
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
                description="The path to the Python file to run, relative to the working directory.",
            ),
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
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

# Function mapping
function_map = {
    "get_files_info": file_commands.get_files_info,
    "get_file_content": file_commands.get_file_content,
    "run_python_file": file_commands.run_python_file,
    "write_file": file_commands.write_file,
}


def call_function(function_call_part, verbose=False):
    """Execute a function call and return the result."""
    function_name = function_call_part.function_call.name
    function_args = dict(function_call_part.function_call.args)  # Convert to dict

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name in function_map:
        try:
            # Add working directory to function arguments
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
        except Exception as e:
            error_msg = f"Error executing {function_name}: {str(e)}"
            if verbose:
                print(error_msg)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": error_msg},
                    )
                ],
            )
    else:
        error_msg = f"Unknown function: {function_name}"
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": error_msg},
                )
            ],
        )


# System prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories using get_files_info
- Read file contents using get_file_content
- Execute Python files using run_python_file
- Write or create files using write_file

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Be systematic in your approach:
1. First understand what the user is asking for
2. List relevant files if needed to understand the project structure
3. Read necessary files to understand the current state
4. Make your changes or provide your analysis
5. Test your changes if applicable

Always provide clear explanations of what you're doing and why.
"""

# Main conversation loop
max_iterations = 20
iteration_count = 0

try:
    for iteration_count in range(max_iterations):
        if verbose:
            print(f"\n--- Iteration {iteration_count + 1} ---")

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        if not response.candidates:
            print("No response candidates received")
            break

        found_function_call = False

        for candidate in response.candidates:
            # Add the assistant's response to messages
            messages.append(candidate.content)

            # Process any function calls
            for part in candidate.content.parts:
                if part.function_call:
                    function_call_result = call_function(part, verbose)
                    messages.append(function_call_result)
                    found_function_call = True

        # If no function calls were made, this is the final response
        if not found_function_call:
            if response.text:
                print("Final response:")
                print(response.text)
            else:
                print("No text response available")
            break

    # If we hit max iterations
    if iteration_count == max_iterations - 1:
        print(f"\nReached maximum iterations ({max_iterations})")
        if response.text:
            print("Last response:")
            print(response.text)

except Exception as e:
    print(f"Error during conversation: {str(e)}")
    if verbose:
        import traceback

        traceback.print_exc()
    sys.exit(1)

finally:
    # Print verbose information if requested
    if verbose and 'response' in locals():
        print(f"\n--- Debug Information ---")
        print(f"User prompt: {prompt}")
        if hasattr(response, 'usage_metadata'):
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Total iterations: {iteration_count + 1}")