import argparse
import os
import sys
from config import MAX_ITERATIONS, MODEL 
from dotenv import load_dotenv
from functions.call_function import available_functions, call_function
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

    if not api_key:
        raise RuntimeError("Could not load API key")

    client = Client(api_key=api_key)
 
    process_message(client, messages, args.verbose)


        
def process_message(client: Client, messages: list[types.Content], verbose: bool) -> None:
    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(
                    model = MODEL,
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
        if verbose:
            print("Prompt tokens:", prompt_tokens)
            print("Response tokens:", response_tokens)
        
        if not response.candidates:
            raise RuntimeError("No candidates obtained from the response")
        
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        function_calls: list[str] | None = response.function_calls
        if not function_calls:
            print("Response:", response.text)
            return 

        function_results = []
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            parts = function_call_result.parts
            if not parts:
                raise Exception(f"Error on function call {function_call.name}: parts is empty")
            function_response = parts[0].function_response
            if not function_response:
                raise Exception("Function response is None")
            function_result = function_response.response
            if not function_result:
                raise Exception("Response is None")

            function_results.append(parts[0])
            if verbose:
                print(f"-> {function_result}")

        messages.append(types.Content(role="user", parts=function_results))
    print("Error: could not get final response")
    sys.exit(1)

if __name__ == "__main__":
    main()
