from config import gConfig
from DownloadThread import DownloadThread
class TaskManager(object):
    def __init__(self):
        self.__downloadThreads = [DownloadThread() for i in range(gConfig['downloadThreads'])]
        for x in self.__downloadThreads:
            x.setDaemon(True)
            x.start()

    # @log_it(('begin','end'), logging.INFO, logArgs=False, logReturnValue=False)
    # def stopTask(self, taskOption):
    #     for x in self.__downloadThreads:
    #         x.stopTaskIfRight(taskOption)

    # # @log_it(('begin','end'), logging.INFO, logArgs=False, logReturnValue=False)
    # def stopAllTasks(self):
    #     for x in self.__downloadThreads:
    #         x.stopTaskIfRight(None, True)

    def exit(self):
        pass

gMan = TaskManager()


if __name__ == '__main__':
    from datas import gData
    gData.downloadQueue.put({
        'url': 'http://douban.com',
        'savename': 'test.html',
        'savedir': '/home/revir/tmp'
    })
    gData.cleanAll()