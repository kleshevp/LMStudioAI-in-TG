import telebot
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
bot = telebot.TeleBot('BOT API') # API из BotFather
messages = {}  # Словарь для сохранения сообщений по user_id


@bot.message_handler(content_types=["text"])
def ping(message):
    user_id = message.from_user.id
    if "/clear" == message.text:
        if user_id in messages:
            messages[user_id] = []  # Очищаем историю сообщений пользователя
            bot.reply_to(message, "История чата очищена.")
        else:
            bot.reply_to(message, "История чата пуста.")
    elif message.reply_to_message or message.chat.id == user_id:
        if user_id not in messages:
            messages[user_id] = []
        elif len(messages[user_id]) >= 8192: # Кол-во токенов при загрузке нейросети в LM Studio
            bot.reply_to(message, "Очистите историю с помощью команды /clear")
        smart = bot.reply_to(message, "Я думаю...")

        # Сохраняем сообщение пользователя в словаре
        messages[user_id].append({"role": "user", "content": message.text})
        completion = client.chat.completions.create(
            model="gemma-2-2b-it(можно найти в настройках API LM Studio",
            messages=messages[user_id],
            temperature=0.5,
            stream=False,
        )
        bot.reply_to(message, completion.choices[0].message.content)
        messages[user_id].append({"role": "assistant", "content": completion.choices[0].message.content})
        bot.delete_message(message.chat.id, smart.message_id)
    else:
        pass

bot.polling(none_stop=True)
