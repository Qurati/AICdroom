import openai

# Настройки прокси
proxies = {
    "http": "154.16.146.45:80",
    "https": "177.234.209.82:999",
}

# Установите прокси для библиотеки requests
openai.proxy = proxies
openai.api_key = "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"


def req(msg):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": f"{msg}"}],
    )
    return response.choices[0].message['content']

#print(req('hi'))
