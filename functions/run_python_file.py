import os
import subprocess
from google.genai import types

DEF_TIMEOUT_S: int = 30

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file with a path relative to the working directory and optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the file path call"
            ),
        },
        required=["file_path"]
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, full_file_path]) != abs_working_dir: 
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.isfile(full_file_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        if not full_file_path.endswith("py"):
            return f"Error: \"{file_path}\" is not a Python file"

        command: list[str] = ["python", full_file_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
                command,
                capture_output=True,
                text=True, 
                timeout=DEF_TIMEOUT_S
        )
        result: list[str] = []
        return_code = completed_process.returncode 
        if return_code != 0:
            result.append(f"Process exited with code {return_code}")

        stdout: str = completed_process.stdout 
        stderr: str = completed_process.stderr

        if stdout == "" and stderr == "":
            result.append("No output produced")
        elif stdout != "":
            result.append(f"STDOUT: {stdout}")
        elif stderr != "":
             result.append(f"STDERR: {stderr}")
        return "\n".join(result)

    except Exception as err:
        return f"Error: executing Python file: {err}"    

