#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from SUtils import writeFile, logger
class HttpUtil():
    def __init__(self):
        pass

    # [TODO] exception
    @staticmethod
    def download(obj):
        logger.debug('download url: '+obj['url'])
        r = requests.get(obj['url'])
        r.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
        
        # save file
        if(obj.get('saveat') == 'upyun'):
            pass
        else:
            writeFile(obj['savename'], obj.get('savedir'), r.content, 'wb')