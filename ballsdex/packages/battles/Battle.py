from ballsdex.packages.battles.BattlingBall import BattlingBall
import discord

INITMSG = '''```ansi
It is the battle of the century!
\x1b[31m^USERA\x1b[39m vs. \x1b[34m^USERB\x1b[39m

Fighting Balls:
\x1b[31m^TEAMA

\x1b[34m^TEAMB

''' # i know, it looks unreadable as fuck

class Comps(discord.ui.View):
	def __init__(self, battle, timeout=180):
		super().__init__(timeout=timeout)
		self.battle = battle


	@discord.ui.button(label="test button", style=discord.ButtonStyle.primary)
	async def btn(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message("amogum")

	

class Battle:
	def __init__(self, usera, userb, teama, teamb):
		self.teama = []
		self.teamb = []
		self.activa = None
		self.activb = None
		self.ended = False


		for i in range(5):
			self.teama.append(BattlingBall(teama[i]))

		for i in range(5):
			self.teamb.append(BattlingBall(teamb[i]))

		self.usera = usera
		self.userb = userb

	def prepmsg(self):
		global INITMSG
		teamanames = []
		teambnames = []
		for ball in self.teama:
			teamanames.append(ball.countryball.name)
		for ball in self.teamb:
			teambnames.append(ball.countryball.name)

		msg = INITMSG
		msg = msg.replace("^USERA", self.usera)
		msg = msg.replace("^USERB", self.userb)
		msg = msg.replace("^TEAMA", ", ".join(teamanames))
		msg = msg.replace("^TEAMB", ", ".join(teambnames))
		msg += "\n```"
		return (msg,Comps(self))

	def reward(self, winner):
		pass

	def action(self, achoice, bchoice):
		self.activa = teama[achoice]
		self.activb = teamb[bchoice]

		winner = {True: "a", False: "b"}[a.attack>b.attack] # sorry, i got a little too silly

		if winner == "a":
			deadb[bchoice] = self.activb
		else:
			deada[achoice] = self.activa

		self.reward(winner)
