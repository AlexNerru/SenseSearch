class Film:
	emotags = []
	def __init__(self, name):
		self._name = name

class Tag:
	name =""
	percent = 0
	def __init__(self, name, percent):
		self.name = name
		self.percent = percent

