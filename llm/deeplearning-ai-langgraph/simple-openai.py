import openai
import re
import httpx
import os
from openai import OpenAI

client = OpenAI()
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)
print (chat_completion.choices[0].message.content)
