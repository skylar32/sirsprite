from discord.ext import commands

from time import time


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        start = time()
        response = await ctx.reply("pong!")
        delta = time() - start
        await response.edit(content=f"pong! (took {delta:.4f}s)")


async def setup(bot):
    await bot.add_cog(Utils(bot))
