import discord
from discord import app_commands
from discord.ext import commands

import config
from time import time


class Utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        start = time()
        response = await ctx.reply("pong!")
        delta = time() - start
        await response.edit(f"pong! (took {delta:.4f}s)")

    @app_commands.command(description="Get help with a bot command.")
    @app_commands.rename(ephemeral="visible")
    @app_commands.describe(command="the command to get help with", ephemeral="whether the response should be public")
    @app_commands.guilds(*config.guilds.keys())
    async def help(self, interaction: discord.Interaction, command: str, ephemeral: bool = False):
        if (command := self.bot.tree.get_command(command.lower(), guild=interaction.guild)) is None:
            await interaction.response.send_message(f"Invalid command.", ephemeral=True)

        try:
            await command.binding.send_help_message(interaction, ephemeral=ephemeral)
        except AttributeError:
            await interaction.response.send_message(
                "Help has not been configured for this command. If you would like a "
                "help message for this command, contact the bot owner.",
                ephemeral=True
            )

    @help.autocomplete("command")
    async def help_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        all_commands = self.bot.tree.get_commands(guild=interaction.guild, type=discord.AppCommandType.chat_input)
        command_names = [c.name for c in all_commands if c.name != "help"]
        return [
            app_commands.Choice(name=command, value=command) for command in command_names
            if current.lower() in command.lower()
        ]


async def setup(bot):
    await bot.add_cog(Utils(bot))
