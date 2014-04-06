#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
from socketio.namespace import BaseNamespace
from flask import Flask, Response, request
from socketio import socketio_manage
from socketio.server import SocketIOServer
# from socketio.mixins import RoomsMixin, BroadcastMixin
from SUtils import logger, writeFile
from datas import gData
from TaskManager import gMan
from UrlsManager import gUrls
from HttpUtil import HttpUtil
import sys, simplejson

app = Flask(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

def _log_it(func):
    def __log(*args, **kwargs):
        text = func.__name__ + ' '
        print text

        res = func(*args, **kwargs)
        return res
    return __log

class SuperNamespace(BaseNamespace):

    # @log_it(level=logging.INFO)
    def recv_connect(self):
        self.emit('connected')
       
    # @log_it(level=logging.INFO)
    def on_addFile(self, data):
        data['namespace'] = self
        gData.downloadQueue.put(data)
        # data['saveat'] = 'upyun'
        # HttpUtil.download(data, self)

    # @log_it(level=logging.debug)
    def on_addHtml(self, data):
        logger.debug('addHtml: '+simplejson.dumps(data))
        gUrls.add(data)

    # @log_it(level=logging.debug, logArgs=False)
    def on_getHtml(self, data):
        logger.debug('getHtml')
        val = gUrls.pop()
        if val:
            data['htmlInfo'] = val
        self.emit('html', data)

    # @log_it(level=logging.INFO, logArgs=False)
    def on_writeJSON(self, obj):
        logger.info('on_writeJSON')
        writeFile(obj['savename'], obj.get('savedir'), obj['data'], 'w')

    # @log_it(pos=('begin', 'end'), level=logging.INFO, logArgs=False)
    def on_downloadItems(self, obj):
        logger.info('on_downloadItems')
        for item in obj.get('downloadItems'):
            if(item.get('savename') and item.get('url')):
                ret = HttpUtil.download(item)
                if ret and type(ret) == dict:
                    item.update(ret)
                else:
                    logger.error('downloadItem error!')
        self.emit('downloadItemsFinished', obj)
        logger.info('on_downloadItems finished')

    def on_taskFinished(self):
        logger.info('taskFinished!');

@app.route('/')
def onindex():
    return 'Hello, this is SafeSiteSuper.'

@app.route('/socket.io/<path:rest>')
def socketio(rest):
    try:
        socketio_manage(request.environ, {'/super': SuperNamespace}, request)
    except:
        logger.error('socketio_manage failed!!!')

    return Response()

if __name__ == '__main__':
    try:
        SocketIOServer(('0.0.0.0', 5000), app, namespace="socket.io", policy_server=False).serve_forever()
    except KeyboardInterrupt:
        logger.info('### KeyboardInterrupt...')
        gMan.exit()
        
