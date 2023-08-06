from File1 import Adder
from File2 import Subtractor
import logging


class MainScript:
	def __init__(self, logger):
		self.logger = logger
		self.adder_obj = Adder(logger)
		self.subtractor_obj = Subtractor(logger)
		self.logger.info("Init Init Successfully Called")

	def add(self, a, b):
		return self.adder_obj.add_val(a, b)

	def sub(self, a, b):
		return self.subtractor_obj.sub_val(a, b)
