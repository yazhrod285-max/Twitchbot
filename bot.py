import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

# Récupération des variables Railway
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
        print(f"Bot connecté : {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content

        # Traduction automatique
        try:
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            if traduction and traduction.lower() != texte.lower():
                await message.channel.send(traduction)

        except Exception as e:
            print("Erreur traduction :", e)

        # Commande simple
        if texte.lower() == "hello":
            await message.channel.send(f"Salut {message.author.name}")

# Lancement du bot
bot = Bot()
bot.run()
