from .rule import *
from .tokenisers import *
from .classifications import *

class classifier:
	
	def __init__(self, knowledge, tokeniser=default_tokeniser()):
		self.rules = []
		for line in knowledge.splitlines():
			l = line.strip()
			if len(l) > 0:
				self.rules.append(rule(l))
		self.tokeniser = tokeniser
		
	def classify(self, in_str):
		classification_list = []
	
		tokens = self.tokeniser.tokenise(in_str)
		for rule in self.rules:
			rule.match(tokens, classification_list)
		
		return classifications(tokens, classification_list)
	
