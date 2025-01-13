import requests
import json
import time
import sys
from typing import Generator, Optional
import re

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama3.2"):
        """Initialize the Ollama client."""
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.generate_endpoint = f"{self.base_url}/api/generate"
        
    def generate_response(self, text: str):
        """Generate and print response directly from the stream."""
        payload = {
            "model": self.model_name,
            "prompt": text,
            "stream": True
        }
        
        try:
            with requests.post(
                self.generate_endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                stream=True
            ) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line)
                            if chunk := json_response.get("response", ""):
                                # Print the chunk directly with appropriate timing
                                if chunk in ['**', '*', '_', '#']:
                                    print(chunk, end='', flush=True)
                                else:
                                    print(chunk, end='', flush=True)
                                    # Add natural pause based on content
                                    if '\n' in chunk:
                                        time.sleep(0.3)
                                    elif any(p in chunk for p in '.!?'):
                                        time.sleep(0.2)
                                    elif any(p in chunk for p in ',:;'):
                                        time.sleep(0.1)
                                    else:
                                        time.sleep(0.02)
                                
                        except json.JSONDecodeError as e:
                            print(f"\nError parsing JSON: {e}", file=sys.stderr)
                            
        except requests.exceptions.ConnectionError:
            print("\nConnection error: Please check if Ollama server is running.")
        except requests.exceptions.HTTPError as e:
            print(f"\nHTTP error occurred: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

def create_fancy_text(text: str) -> str:
    """Convert text to alternating case for stylized output."""
    return ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))

def print_thinking_animation(bot_name: str):
    """Display a thinking animation."""
    thinking_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(2):  # Show animation for 2 cycles
        for frame in thinking_frames:
            sys.stdout.write(f"\r{bot_name} is thinking {frame}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
    sys.stdout.flush()

def print_colorful_separator():
    """Print a colorful separator line."""
    print(f"\n{'─' * 50}\n")

def main():
    # Initialize client
    client = OllamaClient(model_name="llama3.2")
    bot_name = create_fancy_text("Koyna")
    
    # Print welcome message
    print("\n" + "╭" + "─" * 48 + "╮")
    print(f"│ Welcome to chat with {bot_name}! Type 'exit' to quit. │")
    print("╰" + "─" * 48 + "╯\n")
    
    try:
        while True:
            # Get user input
            user_input = input("You  :> ").strip()
            
            # Check for exit command
            if user_input.lower() == "exit":
                print(f"\n{bot_name} waves goodbye! ✨ Thanks for chatting! ✨")
                break
                
            # Skip empty inputs
            if not user_input:
                continue
            
            print_thinking_animation(bot_name)
            print(f"{bot_name} :> ", end="", flush=True)
            
            # Generate and print response directly
            client.generate_response(user_input)
            print_colorful_separator()
            
    except KeyboardInterrupt:
        print(f"\n\n{bot_name} chat session ended by user. 👋")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        
if __name__ == "__main__":
    main()