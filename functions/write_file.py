import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="(Over-)writes any file-type with the given content in a path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents of the file to be written"
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, full_file_path]) != abs_working_dir: 
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isdir(full_file_path):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"

        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        with open(full_file_path, "w") as f:
            f.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    
    except Exception as err:
        return f"Error: {err=} {type(err)=}"
        
