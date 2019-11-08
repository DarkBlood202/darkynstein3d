import pygame as pg
from settings import *

class Map:
	def __init__(self,filename):
		self.data = []
		with open(filename,"rt") as f:
			for line in f:
				self.data.append(line.strip())

		self.tileWidth = len(self.data[0])
		self.tileHeight = len(self.data)
		self.width = self.tileWidth*TILESIZE
		self.height = self.tileHeight*TILESIZE
