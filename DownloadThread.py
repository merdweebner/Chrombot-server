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

        savedir = data.get('savedir') or os.path.join(os.path.expanduser('~'), 'Downloads')
        if data.get('url') and data.get('savename'):
            savename = data['savename'];
            split_index = savename.find('_album_')
            album_name = savename[split_index+len('_album_'):len(savename)].strip()
            savename = savename[0:split_index]
            savedir = os.path.join(savedir,album_name)
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            
            st = os.path.join(savedir, savename);
            urllib.urlretrieve(data['url'], st, scheduler)
            if(os.path.exists(st)):
                return st

        return False
