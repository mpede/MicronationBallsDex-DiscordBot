from ballsdex.packages.battles.BattlingBall import BattlingBall
import discord

INITMSG = '''```ansi
It is the battle of the century!
\x1b[31m^USERA\x1b[39m vs. \x1b[34m^USERB\x1b[39m

Fighting Balls:
\x1b[31m^TEAMA

\x1b[34m^TEAMB

In-combat Balls:
\x1b[31m^ACTIVA\x1b[39m vs. \x1b[34m^ACTIVB\x1b[39m

''' # i know, it looks unreadable as fuck

class Comps(discord.ui.View):
	def __init__(self, battle, timeout=180):
		super().__init__(timeout=timeout)
		self.battle = battle

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
		activaname = "Nobody"
		activbname = "Nobody"
		for ball in self.teama:
			teamanames.append(ball.countryball.short_name)
		for ball in self.teamb:
			teambnames.append(ball.countryball.short_name)

		if not self.activa == None:
			activaname = self.activa.countryball.short_name
		if not self.activb == None:
			activbname = self.activb.countryball.short_name

		msg = INITMSG
		msg = msg.replace("^USERA", self.usera)
		msg = msg.replace("^USERB", self.userb)
		msg = msg.replace("^TEAMA", ", ".join(teamanames))
		msg = msg.replace("^TEAMB", ", ".join(teambnames))
		msg = msg.replace("^ACTIVA", activaname)
		msg = msg.replace("^ACTIVB", activbname)
		msg += "\n```"
		return (msg,Comps(self))
