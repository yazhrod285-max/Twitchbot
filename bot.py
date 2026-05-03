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

        # ❌ ignore TOUS les bots (y compris Lingo)
        if message.echo or message.author.name.lower().endswith("bot"):
            return

        texte = message.content.strip()

        # ❌ ignore messages vides
        if not texte:
            return

        # ❌ ignore messages déjà traités (évite boucle)
        if "a dit en" in texte:
            return

        try:
            langue = detect(texte)
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)
        except:
            return

        # ❌ ignore si déjà français
        if langue == "fr":
            return

        # ❌ ignore si traduction identique
        if texte.lower() == traduction.lower():
            return

        # ✅ UNE SEULE réponse
        await message.channel.send(
            f"@{message.author.name} a dit en {langue} : [ {traduction} ]"
        )

bot = Bot()
bot.run()
