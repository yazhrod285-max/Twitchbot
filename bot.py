import os
from twitchio.ext import commands

TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"Connecté en tant que {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        if "salut" in message.content.lower():
            await message.channel.send(f"Salut {message.author.name} 👋")

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.name} ! 👋")

bot = Bot()
bot.run()
