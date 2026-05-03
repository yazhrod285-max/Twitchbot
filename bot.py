import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

# Récupération du token
TOKEN = os.getenv("TOKEN")

# Récupération des chaînes (séparées par des virgules)
CHANNELS = os.getenv("CHANNELS")

# Sécurité si jamais la variable est vide
if CHANNELS:
    CHANNELS = CHANNELS.split(",")
else:
    CHANNELS = []

print("TOKEN =", TOKEN)
print("CHANNELS =", CHANNELS)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=CHANNELS
        )

    async def event_ready(self):
        print(f"Bot connecté : {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content

        # Traduction automatique
        try:
            traduction = GoogleTranslator(source="auto", target="fr").translate(texte)

            if traduction and traduction.lower() != texte.lower():
                await message.channel.send(traduction)

        except Exception as e:
            print("Erreur traduction :", e)

        # Commande simple
        if texte.lower() == "hello":
            await message.channel.send(f"Salut {message.author.name}")

bot = Bot()
bot.run()
