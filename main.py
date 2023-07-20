import os
import openai

openai.api_key = os.environ.get('API_KEY')

def chat_with_gpt3(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply

# Example usage
user_prompt = "Tell me a joke."
response = chat_with_gpt3(user_prompt)
print("Assistant:", response)
