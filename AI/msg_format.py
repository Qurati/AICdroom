import re


def escape_markdown(text):
    # Экранируем все спецсимволы, которые требуют защиты в MarkdownV2
    return re.sub(r'([\[\]()~>#+\-=|{}.!])', r'\\\1', text)


def format_response(role_text, answer, ai_name):
    ai_name = escape_markdown(ai_name)
    role_text = escape_markdown(role_text)
    answer = escape_markdown(answer)
    if "преподаватель" in role_text:
        role_line = f"📚 *Учитель ({ai_name}) отвечает:*"
    elif "психолог" in role_text:
        role_line = f"🧠 *Психолог ({ai_name}) говорит:*"
    elif "технический специалист" in role_text:
        role_line = f"🛠 *Техподдержка ({ai_name}):*"
    else:
        role_line = f"🤖 *{ai_name} отвечает:*"

    # Для программиста — используем markdown-блок кода
    if "программист" in role_text:
        return f"{role_line}\n\n ``` {answer}```"
    elif "психолог" in role_text:
        return f"{role_line}\n\n_{answer}_"
    else:
        return f"{role_line}\n\n{answer}"
