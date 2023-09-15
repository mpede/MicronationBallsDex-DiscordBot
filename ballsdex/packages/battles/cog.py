from discord import app_commands
from discord.ext import commands
from ballsdex.packages.battles.Battle import Battle
from ballsdex.packages.players.countryballs_paginator import CountryballsSelector
from ballsdex.core.bot import BallsDexBot
from ballsdex.core.models import Player, BallInstance
from tortoise.exceptions import DoesNotExist
import discord, random

async def nothing(): # im evil himself
	pass

class BallSelectSingular(CountryballsSelector):
	selectionfunc = nothing

	async def ball_selected(self, interaction: discord.Interaction, ball_instance: BallInstance):
		await self.selectionfunc(interaction, ball_instance)
	def on_select(self, func):
		self.selectionfunc = func

class BallSelectMultiple(CountryballsSelector):
	selectionfunc = nothing

	@discord.ui.select(min_values=5, max_values=5)
	async def select_ball_menu(self, interaction: discord.Interaction, item: discord.ui.Select):
		await interaction.response.defer(thinking=True)
		instances = [await BallInstance.get(id=x) for x in interaction.data.get("values")]
		await self.ball_selected(interaction, instances)

	async def ball_selected(self, interaction: discord.Interaction, instances):
		await self.selectionfunc(interaction, instances)

	def on_select(self, func):
		self.selectionfunc = func


class BattleAcceptView(discord.ui.View):
	def __init__(self, balls, users, timeout=180):
		super().__init__(timeout=timeout)
		self.balls = balls
		self.users = users


	@discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
	async def accept(self, interaction: discord.Interaction, button):
		if not interaction.user == self.users[1]:
			await interaction.response.send_message(content=f"<@{interaction.user.id}> This message was not meant for you!", ephemeral=True)
			return

		paginator = BallSelectMultiple(interaction, self.balls[0])

		@paginator.on_select
		async def selected(interaction, instances):
			deck1 = instances

			paginator = BallSelectMultiple(interaction, self.balls[1])
			@paginator.on_select
			async def selectedd(interaction, instances):
				deck2 = instances
				await interaction.followup.send(f"{deck1} {deck2} <-- two deckz")

			await paginator.start(content=f"<@{self.users[1].id}> Please choose your deck")

		await paginator.start(content=f"<@{self.users[0].id}> Please choose your deck")

	@discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
	async def decline(self, interaction: discord.Interaction, button):
		if not interaction.user == self.users[1]:
			await interaction.response.send_message(content=f"<@{interaction.user.id}> This message was not meant for you!", ephemeral=True)
			return

		await interaction.response.edit_message(content=f"This battle has been declined", view=None)

class Battles(commands.GroupCog):

	def __init__(self, bot):
		self.bot = bot
		self.battles = {}

	@app_commands.command(description="Duke it out with somebody!")
	@app_commands.describe(opponent="Who you want to battle")
	async def start(self, interaction: discord.Interaction, opponent: discord.User):
		try:
			playera = await Player.get(discord_id=interaction.user.id)
			playerb = await Player.get(discord_id=opponent.id)
			await playera.fetch_related("balls")
			await playerb.fetch_related("balls")
			ballsA = await playera.balls.all()
			ballsB = await playerb.balls.all()
			if len(ballsA) < 5 or len(ballsB) < 5: raise DoesNotExist("nuh uh")
		except DoesNotExist:
			await interaction.response.send_message("You or your opponent do not have enough balls to partake in battle!", ephemeral=True)
			return
		await interaction.response.send_message(f"<@{opponent.id}>, <@{interaction.user.id}> wants to battle you!\nDo you accept?", view=BattleAcceptView((ballsA, ballsB), (interaction.user, opponent)))
