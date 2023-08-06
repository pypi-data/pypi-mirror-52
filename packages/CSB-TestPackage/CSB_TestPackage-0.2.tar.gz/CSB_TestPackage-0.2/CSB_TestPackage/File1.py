import logging


class Adder:
	def __init__(self, logger):
		self.result = 0
		self.logger = logger
		self.logger.info("Adder Init Successfully Called")

	def add_val(self, a, b):
		self.result = a + b
		return self.result