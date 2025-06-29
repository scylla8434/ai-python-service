import sys
import cohere

question = sys.argv[1]
api_key = sys.argv[2]

co = cohere.Client(api_key)
response = co.generate(
    model='command',
    prompt=question,
    max_tokens=256
)
print(response.generations[0].text.strip())
