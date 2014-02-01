import threading, urllib, os
from datas import gData
from SUtils import logger

class DownloadThread(threading.Thread):
    """Thread to download files"""
    def __init__(self):
        self.__name = 'DownloadThread'
        threading.Thread.__init__(self, name=self.__name)
        self.__namespace = None

    def emitToClient(self, api, *args):
        if self.__namespace:
            self.__namespace.emit(api, *args)

    def run(self):
        while True:
            data = gData.downloadQueue.get()
            self.__namespace = data.get('namespace')

            self.__beforeDownload()
            self.download(data)
            self.__afterDownload()

            gData.downloadQueue.task_done()

    def __beforeDownload(self):
        logger.info('download begin...')

    def __afterDownload(self):
        logger.info('download finished!')

    def download(self, data):
        def scheduler(itemCount, itemSize, fileSize):
            percent = 100.0 * itemCount * itemSize / fileSize
            if percent > 100:
                percent = 100
            logger.debug('percent: %.2f%%' % percent)

        if(data.get('url') and data.get('savename') and data.get('savedir')):
            st = os.path.join(data['savedir'], data['savename'])
            urllib.urlretrieve(data['url'], st, scheduler)
            if(os.path.exists(st)):
                return st

        return False
