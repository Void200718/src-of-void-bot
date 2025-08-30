import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="slowmode", description="Set slowmode on the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]):
        assert isinstance(interaction.channel, (discord.TextChannel, discord.Thread))
        if isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message("Cannot set slowmode on a thread.", ephemeral=True)
            return
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Slowmode set to {seconds}s")

    @app_commands.command(name="purge", description="Delete a number of recent messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 200]):
        assert isinstance(interaction.channel, discord.TextChannel)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(name="lock", description="Lock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        assert isinstance(interaction.channel, discord.TextChannel)
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Channel locked 🔒")

    @app_commands.command(name="unlock", description="Unlock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        assert isinstance(interaction.channel, discord.TextChannel)
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Channel unlocked 🔓")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))

