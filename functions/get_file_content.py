import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Show the contents of a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file that is going to be read relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)



def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, full_file_path]) != abs_working_dir: 
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(full_file_path):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        
        with open(full_file_path, "r") as f:
            file_content_string: str = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as err:
        return f"Error: {err=} {type(err)=}"
