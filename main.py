import argparse
import os
from dotenv import load_dotenv
from functions.call_function import available_functions
from google.genai import Client, types
from prompts import system_prompt

def main() -> None: 
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args() 
    user_prompt = args.user_prompt

    if args.verbose:
        print("User prompt:", user_prompt)    

    messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("Could not load API key")

    client = Client(api_key=api_key)
 
    response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config=types.GenerateContentConfig(
                tools = [available_functions],
                system_instruction = system_prompt,
                temperature = 0
                )
    )
    
    if not response.usage_metadata:
        raise RuntimeError("API response without metadata")
    
    metadata = response.usage_metadata
    prompt_tokens = metadata.prompt_token_count
    response_tokens = metadata.candidates_token_count
    if args.verbose:
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)

    function_calls: list[str] | None = response.function_calls
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print("Response:", response.text)

if __name__ == "__main__":
    main()
