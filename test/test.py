from os import *

class Test:
	var = '1'
	def show1(self):
		print self.var

class Test2(Test):
	def show2(self):
		print self.var;
		self.show1()

if __name__ == "__main__":
	test = Test2()
	test.show1()
	test.show2()

