from openai import OpenAI
from api_key import api_key
def query_gpt(prompt: str, model_name: str='gpt-4'):
    # print(prompt)
    client = OpenAI(
        base_url='https://api.openai-proxy.org/v1',
        api_key=api_key
    )

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
        timeout=15
    )
    # import pdb;pdb.set_trace()
    res = completion.choices[0].message.content
    return res