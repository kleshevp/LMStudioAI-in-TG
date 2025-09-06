import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI
import config

# Initialize OpenAI client
client = OpenAI(base_url=config.OPENAI_BASE_URL, api_key=config.OPENAI_API_KEY)

# Initialize Telegram bot
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Dictionary for storing user chat histories
messages: dict[int, list[dict[str, str]]] = {}

# Maximum number of stored messages per user
MAX_HISTORY = 8192


@dp.message(Command("clear"))
async def clear_history(message: Message):
    """Clear the user's chat history."""
    user_id = message.from_user.id
    if user_id in messages and messages[user_id]:
        messages[user_id] = []
        await message.answer("✅ Chat history cleared.")
    else:
        await message.answer("ℹ️ Chat history is already empty.")


@dp.message()
async def chat_handler(message: Message):
    """Handle user text messages."""
    user_id = message.from_user.id

    # Process only private chats or replies to bot
    if not (message.chat.id == user_id or message.reply_to_message):
        return

    # Initialize history for user if not exists
    if user_id not in messages:
        messages[user_id] = []

    # If history is too long, ask to clear
    if len(messages[user_id]) >= MAX_HISTORY:
        await message.answer("⚠️ Please clear chat history with /clear")
        return

    # Temporary "thinking" message
    smart = await message.answer("🤔 Thinking...")

    # Save user message
    messages[user_id].append({"role": "user", "content": message.text})

    try:
        if config.STREAM_MODE:
            # Streamed response
            stream = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages[user_id],
                temperature=0.5,
                stream=True,
            )

            response_text = ""
            buffer = ""
            update_interval = 5  # Update every 5 chunks
            counter = 0

            async for chunk in stream:
                delta = chunk.choices[0].delta
                if not delta or not delta.content:
                    continue

                token = delta.content
                response_text += token
                buffer += token
                counter += 1

                # Update Telegram message not too often
                if counter % update_interval == 0 and buffer.strip():
                    try:
                        await bot.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=smart.message_id,
                            text=response_text,
                        )
                        buffer = ""
                    except Exception:
                        pass

            # Final update
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=smart.message_id,
                text=response_text or "⚠️ Empty response",
            )

        else:
            # Non-streamed response
            completion = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages[user_id],
                temperature=0.5,
                stream=False,
            )
            response_text = completion.choices[0].message.content
            await message.answer(response_text)

        # Save assistant response
        messages[user_id].append({"role": "assistant", "content": response_text})

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

    finally:
        # Delete "thinking" message if still exists (only in non-stream mode)
        if not config.STREAM_MODE:
            try:
                await bot.delete_message(message.chat.id, smart.message_id)
            except Exception:
                pass


async def main():
    """Run the bot."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
