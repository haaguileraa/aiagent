import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try: 
        abs_working_dir = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_working_dir, directory))
        if os.path.commonpath([abs_working_dir, full_path]) != abs_working_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"           
        if not os.path.isdir(full_path):
            return f"Error: \"{directory}\" is not a directory"
        
        # success!
        result: list[str] = []
        for path in os.listdir(full_path):
            path_to_analyze = os.path.join(full_path, path)
            result.append(
                    f"- {path}: file_size={os.path.getsize(path_to_analyze)} bytes, is_dir={os.path.isdir(path_to_analyze)}"
            )
        return "\n".join(result)
    except Exception as err:
        return f"Error: {err=} {type(err)=}"
