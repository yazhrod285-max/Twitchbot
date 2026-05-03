import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

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
        # ❌ ignore ses propres messages
        if message.echo:
            return

        texte = message.content.strip()

        if not texte:
            return

        try:
            translated = GoogleTranslator(source='auto', target='fr').translate(texte)
        except:
            return

        # ❌ si identique → pas de réponse
        if texte.lower() == translated.lower():
            return

        # ✅ UNE SEULE réponse (la bonne)
        await message.channel.send(
            f"@{message.author.name} a dit : [ {translated} ]"
        )

bot = Bot()
bot.run()
