# Class which defines balls that are in battle
import numpy as np


class BattlingBall:
	def __init__(self, instance):
		self.health = instance.health
		self.attack = instance.attack
		self.instance = instance
		self.capacity_enabled = False

		self.countryball = instance.countryball

		self.dead = False

	def activate(self):
		self.capacity_enabled = True
		# TODO: actually run capacity logic

	def attack(self, ball):
		ball.health -= self.attack
		return atack
