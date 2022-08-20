import sys
import traceback

import discord
from discord.ext import commands
import config


extensions = (
    'cogs.utils',
    'cogs.moderation',
    'cogs.storycrafter',
)


class Sirsprite(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or('🧅-'),
            description="A bot for the Thousand Roads Discord community.  Ohoho!",
            help_command=None,
            intents=intents
        )

    def run(self):
        super().run(token=config.token)

    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")
        print('—' * 15)

        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded {extension}")
            except:
                print(f"Failed to load {extension}", file=sys.stderr)
                traceback.print_exc()

        for guild_id in config.guilds:
            await self.tree.sync(guild=self.get_guild(guild_id))


if __name__ == "__main__":
    bot = Sirsprite()
    bot.run()
