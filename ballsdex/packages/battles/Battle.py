
from ballsdex.packages.battles.BattlingBall import BattlingBall
import discord

INITMSG = '''```ansi
It is the battle of the century!
\x1b[31m^USERA\x1b[39m vs. \x1b[34m^USERB\x1b[39m

Decks:
\x1b[31m^TEAMA\x1b[39m
\x1b[34m^TEAMB\x1b[39m

In-combat Balls:
\x1b[31m^ACTIVA\x1b[39m vs. \x1b[34m^ACTIVB\x1b[39m

''' # i know, it looks unreadable as fuck

class SwitchOrPass(discord.ui.View):
	def __init__(self, battle, timeout=360):
		self.battle = battle

	@discord.ui.button(label="Switch", style=discord.ButtonStyle.green)
	async def switch(self, interaction, button):
		await interaction.response.send_message("balls moment")

class Battle:
	def __init__(self, users, decks):
		deck_a = [BattlingBall(instance) for instance in decks[0]]
		deck_b = [BattlingBall(instance) for instance in decks[1]]
		self.decks = (deck_a, deck_b)

		self.users = users
		self.actives = [None, None]
		self.ended = False

	def prepmsg(self):
		global INITMSG
		ballnames = ([], [])
		activenames = ["Nobody", "Nobody"]

		for ball in self.decks[0]:
			ballnames[0].append(ball.countryball.short_name)
		for ball in self.decks[1]:
			ballnames[1].append(ball.countryball.short_name)

		if not self.actives[0] == None:
			activaname = self.activa.countryball.short_name
		if not self.actives[1] == None:
			activbname = self.activb.countryball.short_name

		msg = INITMSG
		msg = msg.replace("^USERA", self.users[0])
		msg = msg.replace("^USERB", self.users[1])
		msg = msg.replace("^TEAMA", ", ".join(ballnames[0]))
		msg = msg.replace("^TEAMB", ", ".join(ballnames[1]))
		msg = msg.replace("^ACTIVA", activenames[0])
		msg = msg.replace("^ACTIVB", activenames[1])
		msg += "\n```"
		return (msg,SwitchOrPass(self))
