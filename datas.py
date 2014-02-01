import Queue

class Datas(object):

	def __init__(self):
		self.__downloadQueue = Queue.Queue()

	@property
	def downloadQueue(self):
		return self.__downloadQueue

	def cleanAll(self):
		self.__downloadQueue.join()


gData = Datas()