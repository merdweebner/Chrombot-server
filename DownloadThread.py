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

        savedir = os.path.expanduser(data.get('savedir'))
        "".join(s for s in savedir if s.isalnum())
        if not os.path.exists(savedir):
            os.makedirs(savedir)

        savename = data['savename']
        "".join(s for s in savename if s.isalnum())
        if data.get('url') and savename:
            st = os.path.join(savedir, savename)
            urllib.urlretrieve(data['url'], st, scheduler)
            if(os.path.exists(st)):
                return st

        return False
