import discord
from discord import app_commands
from discord.ext import commands

import sys
import config


class StorycrafterEmbed(discord.Embed):
    def __init__(self, description, interaction):
        super().__init__(
            title="New Storycrafter prompt!",
            description=description,
            color=discord.Color.lighter_gray()
        )
        self.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        if 'role_link' in config.guilds[interaction.guild_id]['storycrafter']:
            self.add_field(
                name="Want notifications?",
                value=f"[Click here]({config.guilds[interaction.guild_id]['storycrafter']['role_link']})"
            )


class StorycrafterPromptModal(discord.ui.Modal, title='Submit a Storycrafter prompt'):
    prompt = discord.ui.TextInput(
        label='Prompt',
        style=discord.TextStyle.long,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        if 'storycrafter' in config.guilds[interaction.guild_id]:
            storycrafter_thread = interaction.guild.get_channel_or_thread(
                    config.guilds[interaction.guild_id]['storycrafter']['thread_id']
            )
            alert_channel = storycrafter_thread.parent
            prompt = await storycrafter_thread.send(
                '🔔' + interaction.guild.get_role(
                    config.guilds[interaction.guild_id]['storycrafter']['role_id']
                ).mention,
                embed=StorycrafterEmbed(self.prompt.value, interaction)
            )
            success_embed = discord.Embed(
                title=f"New Storycrafter prompt posted!",
                description=f"Join the discussion in {storycrafter_thread.mention}!\n"
                            f"[Jump to prompt]({prompt.jump_url})",
                color=discord.Color.lighter_gray()
            )
            if interaction.channel == alert_channel:
                await interaction.response.send_message(
                    embed=success_embed
                )
            else:
                await alert_channel.send(embed=success_embed)
                await interaction.response.send_message(
                    f"Prompt posted to {storycrafter_thread.mention}.",
                    ephemeral=True
                )

        else:
            await interaction.response.send_message(
                "Storycrafter is not currently supported in this server.",
                ephemeral=True
            )


class Storycrafter(commands.Cog):
    """Commands for sharing story-related prompts."""
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    async def send_help_message(self, interaction: discord.Interaction, ephemeral: bool = True):
        if "storycrafter" not in config.guilds[interaction.guild.id]:
            await interaction.response.send_message("Storycrafter is not configured for this server.")
        else:
            await interaction.response.send_message("Test help message.")

    @app_commands.command()
    @app_commands.guilds(*config.guilds.keys())
    async def storycrafter(self, interaction: discord.Interaction):
        """Post a Storycrafter prompt for community discussion."""
        await interaction.response.send_modal(StorycrafterPromptModal())


async def setup(bot):
    for guild_id in config.guilds:
        guild = config.guilds[guild_id]
        if 'storycrafter' in guild:
            storycrafter_thread = bot.get_channel(guild['storycrafter']['thread_id'])
            try:
                await storycrafter_thread.join()
            except AttributeError:
                print(
                    f"Storycrafter thread in {guild['name']} is archived and was not joined.",
                    file=sys.stderr
                )
    await bot.add_cog(Storycrafter(bot))
