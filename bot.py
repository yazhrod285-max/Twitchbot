import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")
CHANNELS = os.getenv("CHANNELS")

if not CHANNELS:
    raise Exception("CHANNELS manquant dans Railway")

channels_list = CHANNELS.split(",")

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
        # ❌ ignore les messages du bot
        if message.author.name.lower() == self.nick.lower():
            return

        texte = message.content.strip()

        # ❌ ignore messages trop courts (évite "hello", "ok", etc.)
        if len(texte) < 5:
            return

        # ❌ ignore messages déjà traités
        if "🌍" in texte:
            return

        # Traduction
        try:
            translated = GoogleTranslator(source='auto', target='fr').translate(texte)
        except:
            return

        # ❌ ignore si déjà français ou quasi identique
        if texte.lower() == translated.lower():
            return

        # ❌ ignore traductions trop simples (genre hello → bonjour)
        if translated.lower() in ["bonjour", "salut"]:
            return

        # ✅ UNIQUEMENT traduction utile
        await message.channel.send(
            f"🌍 {message.author.name} → {translated}"
        )

bot = Bot()
bot.run()
