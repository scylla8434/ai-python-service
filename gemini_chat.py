import sys
import cohere

def main():
    try:
        # Check if correct number of arguments provided
        if len(sys.argv) != 3:
            print("Usage: python gemini_chat.py <question> <api_key>")
            sys.exit(1)
            
        question = sys.argv[1]
        api_key = sys.argv[2]
        
        # Validate inputs
        if not question.strip():
            print("Error: Question cannot be empty")
            sys.exit(1)
            
        if not api_key.strip():
            print("Error: API key cannot be empty")
            sys.exit(1)

        # Initialize Cohere client
        co = cohere.Client(api_key)
        
        # Generate response
        response = co.generate(
            model='command',
            prompt=question,
            max_tokens=256
        )
        
        # Print the response
        print(response.generations[0].text.strip())
        
    except cohere.error.CohereAPIError as e:
        print(f"Cohere API Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()