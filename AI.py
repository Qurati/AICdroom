import openai

client = openai.OpenAI(
  api_key="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"
)

def req(msg):
    completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": f"{msg}"}
  ]
)
    return completion.choices[0].message.content

#print(req('hi'))
