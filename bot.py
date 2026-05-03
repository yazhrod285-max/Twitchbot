import os
from twitchio.ext import commands
from langdetect import detect
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

# ✅ TES CHANNELS DIRECTEMENT ICI
channels_list = ["biohazardbattles", "le_zombie_des_mers"]

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=channels_list
        )

    async def event_ready(self):
        print(f"✅ Bot connecté : {self.nick}")
        print(f"📺 Channels : {channels_list}")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content.strip()

        # Ignore messages trop courts
        if len(texte) < 2:
            return

        try:
            langue_detectee = detect(texte)

            # ❌ Ignore le français
            if langue_detectee == "fr":
                return

            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            # ❌ Sécurité anti bug (évite traduire "bonjour")
            if traduction.lower() == texte.lower():
                return

            # ✅ UN SEUL MESSAGE (celui que tu veux)
            await message.channel.send(
                f"@{message.author.name} a dit en {langue_detectee} : [ {traduction} ]"
            )

        except Exception as e:
            print("Erreur :", e)


bot = Bot()
bot.run()
