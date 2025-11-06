import pandas as pd

# Список номеров (только цифры, без знака +)
phones = [
    # пример:
    # "77777777777",
    # "77478787878",
    # "77477474747",
    # и т.д
]

# Текст сообщения
message_text = """ВАШ_ТЕКСТ_РАССЫЛКА"""

# Формируем DataFrame и сохраняем в CSV
df = pd.DataFrame({
    "phone": phones,
    "message": [message_text] * len(phones)
})

df.to_csv("contacts.csv", index=False, encoding="utf-8")
print(f"✅ Файл contacts.csv успешно создан ({len(phones)} номеров)")
