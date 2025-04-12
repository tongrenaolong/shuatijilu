# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
# from setting import AI_API_KEY,AI_URL

# client = OpenAI(api_key=AI_API_KEY, base_url=AI_URL)
AI_API_KEY="sk-0e214e7c2b53428e99ca96c456f0ff68"
AI_URL="https://api.deepseek.com"
client = OpenAI(api_key=AI_API_KEY, base_url=AI_URL)
role_user="如何学习Python"
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": role_user},
    ],
    stream=False
)

print(response.choices[0].message.content)