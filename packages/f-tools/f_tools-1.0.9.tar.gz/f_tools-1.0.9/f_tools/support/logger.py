"""Logger object and functions"""

import logging
import sys


class Logger:
	""" Logger class
	Contains a basic logger
	"""
	def __init__(self, name='f_tools', level=logging.DEBUG, template='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
		formatter = logging.Formatter(template)
		ch = logging.StreamHandler()
		ch.setLevel(level)
		ch.setFormatter(formatter)

		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)
		self.logger.addHandler(ch)

	def debug(self, msg: str):
		self.logger.debug(msg)

	def info(self, msg: str):
		self.logger.info(msg)

	def warn(self, msg: str):
		self.logger.warning(msg)

	def error(self, msg: str):
		self.logger.error(msg)

	def fatal(self, msg: str):
		self.logger.fatal(msg)
		sys.exit(1)
