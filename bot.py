import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator
from openai import OpenAI

TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"Bot connecté : {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        text = message.content

        # 🔹 Traduction automatique
        try:
            translated = GoogleTranslator(source='auto', target='fr').translate(text)
            if translated.lower() != text.lower():
                await message.channel.send(translated)
                return
        except:
            pass

        # 🔹 IA (ChatGPT)
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Tu es un bot Twitch sympa."},
                    {"role": "user", "content": text}
                ],
                max_tokens=100
            )

            answer = response.choices[0].message.content
        except:
            answer = "😅 petit bug, réessaie"

        await message.channel.send(answer)

bot = Bot()
bot.run()
