import os
from twitchio.ext import commands
from langdetect import detect
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

channels_list = ["biohazardbattles", "le_zombie_des_mers"]

# 🔥 mapping langues → code propre
LANG_MAP = {
    "en": "en",  # anglais
    "fr": "fr",  # français
    "es": "es",
    "de": "de",
    "it": "it",
    "pt": "pt",
    "ru": "ru",
    "ja": "jp",
    "ko": "kr",
    "zh-cn": "cn",
    "zh-tw": "tw",
    "ar": "sa",
    "hi": "in",
    "tr": "tr",
    "nl": "nl",
    "pl": "pl",
    "sv": "se",
    "no": "no",
    "da": "dk",
    "fi": "fi",
}

# 🔥 correction langues similaires
LANG_FIX = {
    "mk": "ru",
    "uk": "ru",
    "bg": "ru",
    "be": "ru",
}

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=channels_list
        )

    async def event_ready(self):
        print(f"✅ Bot connecté : {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        texte = message.content.strip().lower()

        if len(texte) < 2:
            return

        mots_fr = ["salut", "bonjour", "bonsoir", "coucou", "ça va", "cc"]
        if texte in mots_fr:
            return

        try:
            langue = detect(texte)

            # 🔥 correction
            if langue in LANG_FIX:
                langue = LANG_FIX[langue]

            # ignore français
            if langue == "fr":
                return

            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            if traduction.lower() == texte:
                return

            # 🔥 mapping vers code propre
            code_affiche = LANG_MAP.get(langue, langue)

            await message.channel.send(
                f"🌍 @{message.author.name} a dit en {code_affiche} : [ {traduction} ]"
            )

        except Exception as e:
            print("Erreur :", e)


bot = Bot()
bot.run()
