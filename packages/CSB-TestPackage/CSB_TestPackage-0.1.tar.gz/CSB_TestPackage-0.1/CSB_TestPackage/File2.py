import logging


class Subtractor:
	def __init__(self, logger):
		self.result = 0
		self.logger = logger
		self.logger.info("Subtractor Init Successfully Called")

	def sub_val(self, a, b):
		self.result = a - b
		return self.result