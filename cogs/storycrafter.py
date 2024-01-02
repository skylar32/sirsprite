import discord
from discord import app_commands
from discord.ext import commands

import sys
import config


class StorycrafterEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, is_prompt: bool):
        super().__init__(color=discord.Color.lighter_gray()
        )
        if is_prompt:
            self.set_author(
                name=f"Storycrafter prompt from {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )
        if 'rules_link' in config.guilds[interaction.guild_id]['storycrafter']:
            self.add_field(
                name="What is this?" if is_prompt else "More info",
                value=f"[Click here]({config.guilds[interaction.guild_id]['storycrafter']['rules_link']})"
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
            storycrafter_channel = interaction.guild.get_channel(
                    config.guilds[interaction.guild_id]['storycrafter']['channel_id']
            )
            ping = '🔔' + interaction.guild.get_role(
                config.guilds[interaction.guild_id]['storycrafter']['role_id']
            ).mention

            quoted_prompt = "\n".join((f"> {line}" for line in self.prompt.value.splitlines()))

            if interaction.channel == storycrafter_channel:
                await interaction.response.send_message(
                    f"{quoted_prompt}\n{ping}",
                    embed=StorycrafterEmbed(interaction, is_prompt=True)
                )
            else:
                await storycrafter_channel.send(
                    f"{quoted_prompt}\n{ping}",
                    embed=StorycrafterEmbed(interaction, is_prompt=True)
                )
                await interaction.response.send_message(
                    f"Prompt posted to {storycrafter_channel.mention}!", ephemeral=True
                )


class Storycrafter(commands.Cog):
    """Commands for sharing story-related prompts."""
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    async def send_help_message(self, interaction: discord.Interaction, ephemeral: bool = True):
        if "storycrafter" not in config.guilds[interaction.guild.id]:
            await interaction.response.send_message("Storycrafter is not configured for this server.")

        storycrafter_guild_config = config.guilds[interaction.guild.id]['storycrafter']
        storycrafter_thread = self.bot.get_channel(storycrafter_guild_config ['thread_id'])
        message_content = (
            "💬 **What is Storycrafter?** ✍️\n"
            "Storycrafter is a community thread for sharing and answering fun questions that will get "
            "writers thinking about their stories in new ways. Questions are posted through this bot's "
            f"`/storycrafter` command and shared in the {storycrafter_thread.mention} thread."
        )

        embed = StorycrafterEmbed(interaction, is_prompt=False)
        if embed.fields:
            await interaction.response.send_message(message_content, embed=embed, ephemeral=ephemeral)
        else:
            await interaction.response.send_message(message_content, ephemeral=ephemeral)

    @app_commands.command()
    @app_commands.guilds(*config.guilds.keys())
    async def storycrafter(self, interaction: discord.Interaction):
        """Post a Storycrafter prompt for community discussion."""
        await interaction.response.send_modal(StorycrafterPromptModal())


async def setup(bot):
    await bot.add_cog(Storycrafter(bot))
