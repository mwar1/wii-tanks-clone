from math import sqrt, acos

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
		self.length = sqrt(self.x*self.x + self.y*self.y)

class Mat2:
	def __init__(self, p0, p1, p2, p3):
		self.p0 = p0
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3

def vecMatMult(vec, mat):
	newVec = Vector2(0, 0)
	newVec.x = vec.x * mat.p0 + vec.y * mat.p1
	newVec.y = vec.x * mat.p2 + vec.y * mat.p3
	return newVec

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

def angle(vec1, vec2):
	return acos( dotProduct(vec1, vec2) / (vec1.length * vec2.length) )
