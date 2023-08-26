# Class which defines balls that are in battle
import numpy as np


class BattlingBall:
	def __init__(self, instance):
		self.health = instance.health
		self.attack = instance.attack
		self.instance = instance
		self.capacity_enabled = False

		self.countryball = instance.countryball # These lines of code only exist so that it works perfectly with the image gen
		self.cached_regime = instance.cached_regime
		self.cached_economy = instance.cached_economy
		self.shiny = instance.shiny
		self.special_card = instance.special_card

		self.dead = False

	def activate(self):
		self.capacity_enabled = True
		# TODO: actually run capacity logic

	def attack(self, ball):
		ball.health -= self.attack
		return atack
