import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

# Récupération des variables Railway
TOKEN = os.getenv("TOKEN")
channels = os.getenv("CHANNELS").split(",")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=channels
        )

    async def event_ready(self):
        print(f"Bot connecté : {self.nick}")
        print(f"CHANNELS = {channels}")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content

        try:
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)
            await message.channel.send(traduction)
        except Exception as e:
            print(f"Erreur traduction : {e}")

        await self.handle_commands(message)

bot = Bot()
bot.run()
