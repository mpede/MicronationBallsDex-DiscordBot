from discord import app_commands
from discord.ext import commands
from ballsdex.packages.battles.Battle import Battle
from ballsdex.core.bot import BallsDexBot
import discord, random

class DummyBall:
	def __init__(self, name):
		self.name = name

class DummyInst:
	def __init__(self, hp, ap, ball):
		self.health = hp
		self.attack = ap
		self.countryball = ball

		self.cached_regime = None
		self.cached_economy = None
		self.shiny = None
		self.special_card = None

PANTONIA = DummyInst(12,5,DummyBall("Pantonia"))
OLDLUNARIA = DummyInst(5,12,DummyBall("Old Lunaria"))
NEWYORK = DummyInst(8,4,DummyBall("New York"))
WESTARCTICA = DummyInst(4,8,DummyBall("West Arctica"))
TDC = DummyInst(6,9,DummyBall("TDC"))
CODERSUNION = DummyInst(9,6,DummyBall("Coders Union"))
TAKAYA = DummyInst(10,4,DummyBall("Takaya"))
soldiersA = [PANTONIA,OLDLUNARIA,TDC,TAKAYA,CODERSUNION]
soldiersB = [NEWYORK,WESTARCTICA,TDC,TAKAYA,CODERSUNION]

class BattleAcceptView(discord.ui.View):
	def __init__(self, usera, target, timeout=180):
		super().__init__(timeout=timeout)
		self.acceptable = False
		self.target = target
		self.usera = usera

	@discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
	async def accept(self, interaction: discord.Interaction, button):
		global soldiersA, soldiersB
		if not interaction.user == self.target:
			await interaction.response.send_message(f"<@{interaction.user.id}> This message was not meant for you")
			return
		usera = self.usera.display_name # confuzzled, arent you!
		userb = interaction.user.display_name
		battle = Battle(usera, userb, soldiersA, soldiersB)
		resp = battle.prepmsg()
		button.disabled = True
		await interaction.response.send_message(resp[0], view=resp[1])

class Battles(commands.GroupCog):

	def __init__(self, bot):
		self.bot = bot
		self.battles = {}

	@app_commands.command(description="Duke it out with somebody!")
	@app_commands.describe(opponent="Who you want to battle")
	async def start(self, interaction: discord.Interaction, opponent: discord.User):
		#global soldiersA, soldiersB
		#usera = interaction.user.display_name
		#userb = opponent.display_name
		#battle = Battle(id, usera, userb, soldiersA, soldiersB)
		#resp = battle.prepmsg()
		await interaction.response.send_message(f"<@{interaction.user.id}> BALLS!", view=BattleAcceptView(interaction.user, opponent))
