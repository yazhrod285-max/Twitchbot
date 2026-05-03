import os
from twitchio.ext import commands
from langdetect import detect
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

channels_list = ["biohazardbattles", "le_zombie_des_mers"]

# 🌍 conversion langue → pays (approximation propre)
lang_to_country = {
    "en": "GB",
    "fr": "FR",
    "es": "ES",
    "de": "DE",
    "it": "IT",
    "pt": "PT",
    "ru": "RU",
    "ja": "JP",
    "ko": "KR",
    "zh-cn": "CN",
    "ar": "SA"
}

# 🏳️ fonction pour générer un drapeau automatiquement
def get_flag(country_code):
    if len(country_code) != 2:
        return "🌍"
    return chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))

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

        # 🔴 mots FR à ignorer
        mots_fr = ["salut", "bonjour", "bonsoir", "coucou", "ça va", "cc"]
        if texte in mots_fr:
            return

        try:
            langue = detect(texte)

            if langue == "fr":
                return

            traduction = GoogleTranslator(source='auto', target='fr').translate(texte)

            if traduction.lower() == texte:
                return

            # 🌍 récup pays + drapeau
            country = lang_to_country.get(langue, "UN")
            drapeau = get_flag(country)

            await message.channel.send(
                f"{drapeau} @{message.author.name} a dit en {langue} : [ {traduction} ]"
            )

        except Exception as e:
            print("Erreur :", e)


bot = Bot()
bot.run()
