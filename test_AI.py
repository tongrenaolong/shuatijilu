# Please install OpenAI SDK first: `pip3 install openai`
import httpx
from openai import OpenAI
import ssl

# 需要关代理
AI_API_KEY = "sk-0e214e7c2b53428e99ca96c456f0ff68"
AI_URL = "https://api.deepseek.com/v1"

client = OpenAI(
    api_key=AI_API_KEY,
    base_url=AI_URL,
    http_client=httpx.Client(verify=False)  # 测试关闭 SSL 验证
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)


