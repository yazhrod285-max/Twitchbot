import os
from twitchio.ext import commands
from deep_translator import GoogleTranslator

# ===== VARIABLES =====
TOKEN = os.getenv("TOKEN")
channels_env = os.getenv("CHANNELS")

if not TOKEN:
    raise Exception("TOKEN manquant dans Railway")

if not channels_env:
    raise Exception("CHANNELS manquant dans Railway")

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

        try:
            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)
            await message.channel.send(traduction)
        except Exception as e:
            print(f"Erreur traduction : {e}")

        await self.handle_commands(message)

# ===== LANCEMENT =====
bot = Bot()
bot.run()
