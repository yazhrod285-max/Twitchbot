import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print("BOT CONNECTE")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content

        try:
            traduction = GoogleTranslator(source="auto", target="fr").translate(texte)
            if traduction and traduction.lower() != texte.lower():
                await message.channel.send("Traduction : " + traduction)
        except Exception as e:
            print("Erreur traduction:", e)

        if message.content.lower() == "!hello":
            await message.channel.send("Salut " + message.author.name)

bot = Bot()
bot.run()
