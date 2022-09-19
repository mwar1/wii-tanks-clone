from math import sqrt

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.length = sqrt(self.x*self.x + self.y*self.y)

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y

	def sub(self, vec):
		self.x -= vec.x
		self.y -= vec.y

	def normalise(self):
		if self.length > 0:
			self.x /= self.length
			self.y /= self.length

def scale(vec, factor):
	newVec = Vector2(vec.x, vec.y)
	newVec.x *= factor
	newVec.y *= factor
	return newVec

def set(newVec):
	vec = Vector2(0, 0)
	vec.x = newVec.x
	vec.y = newVec.y
	return vec

def dotProduct(vec1, vec2):
	return vec1.x*vec2.x + vec1.y*vec2.y
