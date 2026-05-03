import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator
from langdetect import detect

TOKEN = os.getenv("TOKEN")

channels_env = os.getenv("CHANNELS")

if channels_env:
    channels_list = channels_env.split(",")
else:
    channels_list = ["biohazardbattles", "le_zombie_des_mers"]

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=channels_list
        )

    async def event_ready(self):
        print(f"Bot connecté : {self.nick}")

    async def event_message(self, message):
        # ❌ ignore tous les bots (très important)
        if message.echo or message.author.name.lower().endswith("bot"):
            return

        texte = message.content.strip()

        if not texte:
            return

        try:
            # détecte automatiquement TOUTES les langues
            langue_code = detect(texte)

            # traduit en français
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

        except:
            return

        # ❌ si déjà français → ignore
        if langue_code == "fr":
            return

        # mapping lisible (facultatif mais propre)
        langues = {
            "en": "anglais",
            "es": "espagnol",
            "de": "allemand",
            "it": "italien",
            "pt": "portugais",
            "ru": "russe",
            "ja": "japonais",
            "ko": "coréen",
            "zh-cn": "chinois",
            "ar": "arabe"
        }

        langue_nom = langues.get(langue_code, langue_code)

        # ✅ UNE SEULE réponse
        await message.channel.send(
            f"@{message.author.name} a dit en {langue_nom} : [ {traduction} ]"
        )

bot = Bot()
bot.run()
