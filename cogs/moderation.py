from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

import config


SETUP_GUILDS = [guild for guild in config.guilds if config.guilds[guild].get("setup_mode", False)]

class ReportModal(discord.ui.Modal, title='Submit a report to the community staff'):
    report = discord.ui.TextInput(
        label='Enter your report here',
        style=discord.TextStyle.long,
        placeholder='Be as detailed with your report as you can.',
        required=True
    )
    submitter = discord.ui.TextInput(
        label='Username (if you want follow-up from staff)',
        placeholder='Leave blank to submit anonymously',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        staff_channel = interaction.guild.get_channel_or_thread(config.guilds[interaction.guild_id]['staff'])
        report_embed = discord.Embed(
            title="⚠️ New user report submitted",
            description=self.report.value,
            timestamp=datetime.now(),
            color=discord.Color.lighter_gray()
        )
        if self.submitter.value:
            report_embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url
            )
        else:
            report_embed.set_author(name="Anonymously submitted")
        await staff_channel.send(embed=report_embed)
        await interaction.response.send_message(f"Report submitted.", ephemeral=True)


class ReportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Submit report', style=discord.ButtonStyle.green, custom_id='report_view:submit')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(ReportModal())


class ContextMenuReport(discord.ui.Modal):
    report = discord.ui.TextInput(
        label='Enter your report here',
        style=discord.TextStyle.long,
        placeholder='Be as detailed with your report as you can.',
        required=True
    )
    submitter = discord.ui.TextInput(
        label='Your username (if you want follow-up)',
        placeholder='Leave blank to submit anonymously',
        required=False
    )

    def __init__(self, user: discord.Member, message: discord.Message = None):
        super().__init__(title=f"Reporting {user.display_name}")
        self.user = user
        self.message = message

    async def on_submit(self, interaction: discord.Interaction) -> None:
        staff_channel = interaction.guild.get_channel_or_thread(config.guilds[interaction.guild_id]['staff'])
        report_embed = discord.Embed(
            title="⚠️ New user report submitted",
            description=self.report.value,
            timestamp=datetime.now(),
            color=discord.Color.lighter_gray()
        )
        if self.submitter.value:
            report_embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url
            )
        else:
            report_embed.set_author(name="Anonymously submitted")
        report_embed.add_field(
            name="Reported user",
            value=self.user.mention
        )
        if self.message:
            report_embed.add_field(
                name="Reported message",
                value=f"[Jump to message]({self.message.jump_url})"
            )
        await staff_channel.send(embed=report_embed)
        await interaction.response.send_message(f"Your report has been submitted.", ephemeral=True)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_guilds = [guild for guild in config.guilds if config.guilds[guild].get("setup_mode", False)]

    @app_commands.command()
    @app_commands.guilds(*SETUP_GUILDS)
    async def prepare_report_view(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Create the report submission master post."""
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("❌ You're not authorized to use that command.", ephemeral=True)
            return
        embed = discord.Embed(
            title="Questions, comments, or concerns about the server?",
            description="Click the button below to send a report to the server staff. To submit an anonymous "
                        "report, leave the `username` field blank.  The report will be seen by all staff.",
            color=discord.Color.lighter_gray()
        )
        post = await channel.send(embed=embed, view=ReportView())
        await interaction.response.send_message(f"Success.  ID: `{post.id}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
    for guild in config.guilds:
        if 'report_post_id' in config.guilds[guild]:
            bot.add_view(ReportView(), message_id=config.guilds[guild]['report_post_id'])

    guilds = [bot.get_guild(guild_id) for guild_id in config.guilds.keys()]

    @bot.tree.context_menu(name="Report user", guilds=guilds)
    async def report_user(interaction: discord.Interaction, user: discord.Member | discord.User):
        """File a report to server staff against a server user."""
        await interaction.response.send_modal(ContextMenuReport(user))

    @bot.tree.context_menu(name="Report message", guilds=guilds)
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        """File a report to server staff against a particular message."""
        await interaction.response.send_modal(ContextMenuReport(message.author, message))
