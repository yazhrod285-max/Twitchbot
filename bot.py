import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

# Variables Railway
TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

# DEBUG (ça va afficher dans Railway)
print("TOKEN =", TOKEN)
print("CHANNEL =", CHANNEL)

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

        texte = message.content

        try:
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            if traduction and traduction.lower() != texte.lower():
                await message.channel.send(traduction)

        except Exception as e:
            print("Erreur traduction :", e)

        if texte.lower() == "hello":
            await message.channel.send(f"Salut {message.author.name}")

bot = Bot()
bot.run()
