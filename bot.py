import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator
from langdetect import detect

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")

channels_env = "biohazardbattles,le_zombie_des_mers,maestrosfenomeno"
channels = [c.strip() for c in channels_env.split(",")]

# ===== BOT =====
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

        # 🔥 Évite les messages trop courts (anti-spam)
        if len(texte) < 4:
            return

        try:
            langue = detect(texte)

            # ✅ Traduire UNIQUEMENT si ce n'est PAS du français
            if langue != "fr":
                traduction = GoogleTranslator(source='auto', target='fr').translate(texte)
                await message.channel.send(traduction)

        except Exception as e:
            print(f"Erreur : {e}")

        await self.handle_commands(message)

# ===== LANCEMENT =====
bot = Bot()
bot.run()
