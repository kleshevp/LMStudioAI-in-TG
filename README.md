# 🤖 Telegram AI Chatbot (aiogram + LM Studio)

This is a **Telegram chatbot** built with `aiogram 3.x` and `OpenAI API client`.  
It connects to **LM Studio** (or any OpenAI-compatible API) and allows users to chat with a local AI model.

---

## 🚀 Features
- Works in private chats or when replying to the bot  
- Chat history stored per user  
- `/clear` command to reset conversation  
- Configurable model, API base URL, and token limit  
- **Streaming mode** (bot updates the message gradually while AI generates a response)  
- Async and efficient (`aiogram 3.x`)  

---

## 📂 Project structure

```
project/
├── bot.py        # Main bot logic
├── config.py     # Config loader
├── .env          # Secrets and settings
└── README.md

```

---

Да, у тебя там markdown немного "плавает" из-за отступов перед блоками кода. В VSCode (и на GitHub) внутри нумерованных списков достаточно **3 пробела** перед блоком кода, а не 4. Если поставить больше — оно ломает формат.

Вот исправленный кусок, который будет отображаться ровно:

## ⚙️ Setup

1. Install dependencies:
   ```bash
   pip install aiogram openai python-dotenv
   ```

2. Create `.env` file:

   ```ini
   BOT_TOKEN=your_bot_api_token_here
   OPENAI_API_KEY=lm-studio
   OPENAI_BASE_URL=http://localhost:1234/v1
   OPENAI_MODEL=gemma-2-2b-it
   STREAM_MODE=true
   ```

3. Run the bot:

   ```bash
   python bot.py
   ```

---

## 💡 Usage

* Start a private chat with the bot.
* Send a message → bot responds using the AI model.
* Use `/clear` to reset your chat history.
* If `STREAM_MODE=true` → the bot updates the message gradually while the model generates a response.

---

## 🛠 Notes

* Default `MAX_HISTORY` is `8192` messages per user.
* Works with **LM Studio**, **Ollama**, or **OpenAI API** (if base URL is changed).
* Streaming mode respects Telegram limits (not too frequent updates).
