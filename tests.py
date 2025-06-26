from functions.file_commands import get_files_info, get_file_content, write_file, run_python_file
'''
print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))

print(get_file_content("calculator", "lorem.txt"))

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
'''


test_cases = [
    {
        "prompt": "read the contents of main.py",
        "expected_function": "get_file_content",
        "expected_args": {"file_path": "main.py"},
    },
{
        "prompt": "write 'hello' to main.txt",
        "expected_function": "write_file",
        "expected_args": {"file_path": "main.txt", "content": "hello"},
    },
    {
        "prompt": "run main.py",
        "expected_function": "run_python_file",
        "expected_args": {"file_path": "main.py"},
    },
    {
        "prompt": "list the contents of the pkg directory",
        "expected_function": "get_files_info",
        "expected_args": {"directory": "pkg"},
    }
]

for case in test_cases:
    print(f'Prompt: "{case["prompt"]}"')
    print(f'Should call: {case["expected_function"]}({case["expected_args"]})')