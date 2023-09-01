import discord
import sys
import logging
import random
import os

from typing import TYPE_CHECKING

from discord import app_commands
from discord.ext import commands

from ballsdex import __version__ as ballsdex_version
from ballsdex.settings import settings
from ballsdex.core.models import Ball, balls as countryballs
from ballsdex.core.models import NewsArticle
from ballsdex.core.models import BallInstance
from ballsdex.core.models import Player
from ballsdex.core.utils.tortoise import row_count_estimate

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.info")

def mention_app_command(app_command: app_commands.Command | app_commands.Group) -> str:
    if "mention" in app_command.extras:
        return app_command.extras["mention"]
    else:
        if isinstance(app_command, app_commands.ContextMenu):
            return f"`{app_command.name}`"
        else:
            return f"`/{app_command.name}`"

class NewsCommands(discord.ui.View):
	def __init__(self, allticles, index, timeout=180):
		super().__init__(timeout=timeout)
		self.allticles = allticles
		self.index = index
		print(self.index)

	@discord.ui.button(label="<<", style=discord.ButtonStyle.gray)
	async def tailbtn(self, interaction: discord.Interaction, button):
		self.index = 0
		article = self.allticles[self.index]
		await interaction.response.edit_message(embed=Info.make_embed(article), view=NewsCommands(self.allticles, self.index))

	@discord.ui.button(label="Page -1", style=discord.ButtonStyle.blurple)
	async def backwardbtn(self, interaction: discord.Interaction, button):
		if self.index > 0:   self.index -= 1
		article = self.allticles[self.index]
		await interaction.response.edit_message(embed=Info.make_embed(article), view=NewsCommands(self.allticles, self.index))

	@discord.ui.button(label="Page +1", style=discord.ButtonStyle.blurple)
	async def forwardbtn(self, interaction: discord.Interaction, button):
		if self.index < len(self.allticles)-1:   self.index += 1
		article = self.allticles[self.index]
		await interaction.response.edit_message(embed=Info.make_embed(article), view=NewsCommands(self.allticles, self.index))

	@discord.ui.button(label=">>", style=discord.ButtonStyle.gray)
	async def headbtn(self, interaction: discord.Interaction, button):
		self.index = len(self.allticles)-1
		article = self.allticles[self.index]
		await interaction.response.edit_message(embed=Info.make_embed(article), view=NewsCommands(self.allticles, self.index))

class Info(commands.Cog):
    """
    Simple info commands.
    """

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    async def _get_10_balls_emojis(self) -> list[discord.Emoji]:
        balls: list[Ball] = random.choices(
            [x for x in countryballs.values() if x.enabled], k=min(10, len(countryballs))
        )
        emotes: list[discord.Emoji] = []

        for ball in balls:
            if emoji := self.bot.get_emoji(ball.emoji_id):
                emotes.append(emoji)

        return emotes

    def make_embed(article, format="%d/%m/%y"):
        date = article.date.strftime(format)
        embed = discord.Embed(title="Microballs News", description="Here you can read the latest news", color=article.color)
        embed.add_field(name=article.title, value=article.content)
        embed.set_footer(text=f"Created on {date}")
        return embed

    @app_commands.command(description="Latest microballs news!")
    async def news(self, interaction: discord.Interaction):
        allticles = await NewsArticle.all()
        index = len(allticles)-1
        latest = allticles[index]
        await interaction.response.send_message(embed=Info.make_embed(latest), view=NewsCommands(allticles, index))

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        score = {player.id: 0 for player in await Player.all()}
        instances = await BallInstance.all()
        for instance in instances:
            score[await instance.player] += 1

        await interaction.response.send_message(str(score))

    @app_commands.command()
    async def about(self, interaction: discord.Interaction):
        """
        Get information about this bot.
        """
        embed = discord.Embed(
            title=f"{settings.bot_name} Discord bot", color=discord.Colour.blurple()
        )

        try:
            balls = await self._get_10_balls_emojis()
        except Exception:
            log.error("Failed to fetch 10 balls emotes", exc_info=True)
            balls = []

        balls_count = len([x for x in countryballs.values() if x.enabled])
        players_count = await row_count_estimate("player")
        balls_instances_count = await row_count_estimate("ballinstance")

        assert self.bot.user
        assert self.bot.application
        try:
            assert self.bot.application.install_params
        except AssertionError:
            invite_link = discord.utils.oauth_url(
                self.bot.application.id,
                permissions=discord.Permissions(
                    manage_webhooks=True,
                    read_messages=True,
                    send_messages=True,
                    manage_messages=True,
                    embed_links=True,
                    attach_files=True,
                    use_external_emojis=True,
                    add_reactions=True,
                ),
                scopes=("bot", "applications.commands"),
            )
        else:
            invite_link = discord.utils.oauth_url(
                self.bot.application.id,
                permissions=self.bot.application.install_params.permissions,
                scopes=self.bot.application.install_params.scopes,
            )
        embed.description = (
            f"{' '.join(str(x) for x in balls)}\n"
            f"{settings.about_description}\n"
            f"*Running version **[{ballsdex_version}]({settings.github_link}/releases)***\n\n"
            f"**{balls_count}** {settings.collectible_name}s to collect\n"
            f"**{players_count}** players that caught "
            f"**{balls_instances_count}** {settings.collectible_name}s\n"
            f"**{len(self.bot.guilds)}** servers playing\n\n"
            "This bot was made by the Pantonian Coders:\nDjango07, millipede, e_, Magestick, sebbog\nOriginal bot developed by El Laggron (laggron42)\n\n"
            "Main artists are:\ntheforgettabledino, sebbog, Magestick & Rusty Potato\n\n"
            "Thanks goes out to all micronations out there who contributed artwork / balls\n\n"
            "For request of adding your micronation as a ball, please go to our support server and file a request!\n"
            f"[Discord Support Server]({settings.discord_invite})\n\n MicronationsBalls: [Invite me]({invite_link})\n"
            f"[Invite me - alternative link]({settings.discord_bot_invite})\n"
            f"[Source code]({settings.github_link})\n"
            f"[Terms of Service]({settings.terms_of_service}) • "
            f"[Privacy policy]({settings.privacy_policy})\n\n\n"
            ":heart: PANTONIA LOVES YOU! :heart:\n\n"
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        v = sys.version_info
        embed.set_footer(
            text=f"\nPython {v.major}.{v.minor}.{v.micro} • discord.py {discord.__version__}"
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def help(self, interaction: discord.Interaction):
        """
        Show the list of commands from the bot.
        """
        assert self.bot.user
        embed = discord.Embed(
            title=f"{settings.bot_name} Discord bot - help menu", color=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        for cog in self.bot.cogs.values():
            if cog.qualified_name == "Admin":
                continue
            content = ""
            for app_command in cog.walk_app_commands():
                content += f"{mention_app_command(app_command)}: {app_command.description}\n"
            if not content:
                continue
            embed.add_field(name=cog.qualified_name, value=content, inline=False)

        await interaction.response.send_message(embed=embed)
