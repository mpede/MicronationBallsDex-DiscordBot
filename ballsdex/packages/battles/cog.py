from discord import app_commands
from discord.ext import commands
from ballsdex.packages.battles.Battle import Battle
from ballsdex.packages.players.countryballs_paginator import CountryballsSelector
from ballsdex.core.bot import BallsDexBot
from ballsdex.core.models import Player, BallInstance
from tortoise.exceptions import DoesNotExist
import discord, random

#class DeckSelectionView(discord.ui.View):
#	def __init__(self

class BallSelectSingular(CountryballsSelector):
	async def ball_selected(self, interaction: discord.Interaction, ball_instance: BallInstance):
		await interaction.send_message("DUCK!")

class BallSelectMultiple(CountryballsSelector):

	@discord.ui.select(min_values=5, max_values=5)
	async def select_ball_menu(self, interaction: discord.Interaction, item: discord.ui.Select):
		await interaction.response.defer(thinking=True)
		#ball_instance = await BallInstance.get(id=int(interaction.data.get("values")[0]))
 		instances = [await BallInstance.get(id=x) for x in interaction.data.get("values")]
		await self.ball_selected(interaction, instances)

	async def ball_selected(self, interaction: discord.Interaction, instances):
		await interaction.send_message("balls!!!")


'''
class DeckSelectionView(discord.ui.View):
	def __init__(self, usera, userb, ballsA, ballsB, timeout=180):
		super().__init__(timeout=timeout)
		self.usera = usera
		self.userb = userb
		self.ballsA = ballsA
		self.ballsB = ballsB
		self.randomA = None
		self.randomB = None

	@discord.ui.button(label="Random", style=discord.ButtonStyle.gray)
	async def randomButton(self, interaction: discord.Interaction, button):
		await interaction.response.send_message(f"Has somebody chosen? {self.somebodypressed}")
		self.somebodypressed = True

	@discord.ui.button(label="Select yourself", style=discord.ButtonStyle.gray)
	async def chooseButton(self, interaction: discord.Interaction, button):
		await interaction.response.send_message(f"Has somebody chosen? {self.somebodypressed}")
		self.somebodypressed = True
''' # im just gonna do this later
'''
class DeckSelect(discord.ui.View):
	def __init__(self, balls, users, timeout=180):
		super().__init__(timeout=timeout)
		self.balls = balls
		self.users = users

		self.deckA = []
		self.deckB = []

		self.optionsA = [discord.SelectOption()
'''

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

		#await interaction.response.edit_message(content=f"<@{self.challenger.id}> <@{self.target.id}> Please choose your method of deck selection", view=DeckSelectionView(self.users, self.balls))
		paginator = BallSelectSingular(interaction, self.balls[0])
		await paginator.start(content="balls")

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
