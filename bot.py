import os
from twitchio.ext import commands
from langdetect import detect
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

# ✅ Tes chaînes
channels_list = ["biohazardbattles", "le_zombie_des_mers"]

# 🌍 mapping langue → pays (pour drapeaux)
lang_to_country = {
    "en": "US",   # anglais → USA (plus logique que GB sur Twitch)
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

# 🏳️ fonction pour générer les vrais drapeaux
def get_flag(country_code):
    try:
        return ''.join(chr(127397 + ord(c)) for c in country_code.upper())
    except:
        return "🌍"

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

        # 🔴 mots FR à ignorer (anti bug)
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

            # 🌍 récup drapeau
            country = lang_to_country.get(langue, "UN")
            drapeau = get_flag(country)

            # ✅ message final propre
            await message.channel.send(
                f"{drapeau} @{message.author.name} a dit en {langue} : [ {traduction} ]"
            )

        except Exception as e:
            print("Erreur :", e)


bot = Bot()
bot.run()
