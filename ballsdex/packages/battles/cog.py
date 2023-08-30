from discord import app_commands
from discord.ext import commands
from ballsdex.packages.battles.Battle import Battle
from ballsdex.core.bot import BallsDexBot
from ballsdex.core.models import Player
from tortoise.exceptions import DoesNotExist
import discord, random

class BattleAcceptView(discord.ui.View):
	def __init__(self, ballsA, ballsB, challenger, target, timeout=180):
		super().__init__(timeout=timeout)
		self.acceptable = False
		self.target = target
		self.challenger = challenger
		self.ballsA = ballsA
		self.ballsB = ballsB

	@discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
	async def accept(self, interaction: discord.Interaction, button):
		if not interaction.user == self.target:
			await interaction.response.send_message(f"<@{interaction.user.id}> This message was not meant for you!", ephemeral=True)
			return

		button.disabled = True

		soldiersA = []
		soldiersB = []

		for i in range(5):
			ballA = random.choice(self.ballsA)
			ballB = random.choice(self.ballsB)
			self.ballsA.remove(ballA)
			self.ballsB.remove(ballB)
			soldiersA.append(ballA)
			soldiersB.append(ballB)

		usera = self.challenger.display_name
		userb = self.target.display_name

		battle = Battle(usera, userb, soldiersA, soldiersB)
		resp = battle.prepmsg()
		await interaction.response.edit_message(content=f"<@{self.target.id}>, <@{self.challenger.id}> wants to battle you!\nDo you accept?", view=self)
		await interaction.response.send_message(resp[0], view=resp[1])

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
		await interaction.response.send_message(f"<@{opponent.id}>, <@{interaction.user.id}> wants to battle you!\nDo you accept?", view=BattleAcceptView(ballsA, ballsB, interaction.user, opponent))
