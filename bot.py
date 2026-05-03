import os
from twitchio.ext import commands
from langdetect import detect
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

# ✅ TES CHAÎNES
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

        texte = message.content.strip().lower()

        # ❌ ignore messages trop courts
        if len(texte) < 2:
            return

        # 🔴 bloque mots FR simples
        mots_fr = ["salut", "bonjour", "bonsoir", "coucou", "ça va", "cc"]
        if texte in mots_fr:
            return

        try:
            langue = detect(texte)

            # ❌ ignore français
            if langue == "fr":
                return

            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            # ❌ sécurité anti doublon
            if traduction.lower() == texte:
                return

            # 🌍 affichage simple et fiable
            await message.channel.send(
                f"🌍 @{message.author.name} a dit en {langue} : [ {traduction} ]"
            )

        except Exception as e:
            print("Erreur :", e)


bot = Bot()
bot.run()
