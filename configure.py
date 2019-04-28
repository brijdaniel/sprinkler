from configparser import ConfigParser

class Configure(ConfigParser):
	def __init__(self):
		super(Configure, self).__init__()
		self.file = '/home/pi/sprinkler/config.ini'
		self.config = ConfigParser()
		self.config.read(self.file)
		
	def read(self, section, key):
		self.file = '/home/pi/sprinkler/config.ini'
		self.config = ConfigParser()
		self.config.read(self.file)
		return self.config.get(section, key)

	def set(self, section, key, value):
		self.file = '/home/pi/sprinkler/config.ini'
		self.config = ConfigParser()
		self.config.read(self.file)
		self.config.set(section, key, value)
		with open ('/home/pi/sprinkler/config.ini','w') as file:
			self.config.write(file)
