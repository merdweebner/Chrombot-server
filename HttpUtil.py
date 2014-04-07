#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from SUtils import writeFile, logger
from UpyunUtil import UpyunUtil
from config import gConfig
class HttpUtil():
    def __init__(self):
        pass

    @staticmethod
    def download(obj):
        logger.debug('download url: '+obj['url'])
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
                'Proxy-Connection': 'keep-alive',
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'max-age=0',
                'Cookie': 'UTMPKEY=14367518; UTMPNUM=13792; UTMPUSERID=guest; LOGINTIME=1396536377'
            }
            proxies = None
            if gConfig["downloadUsingProxy"]["enabled"]:
                proxies = gConfig["downloadUsingProxy"]["proxies"]
            r = requests.get(obj['url'], headers=headers, proxies=proxies)
            r.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
        except Exception as e:
            logger.exception(e.message)
            # namespace.emit('downloadError', obj)
            return None
        else:
            # save file
            if(obj.get('saveat') == 'upyun'):
                return UpyunUtil.uploadStream(r.content, obj)
            else:
                saveurl = writeFile(obj['savename'], obj.get('savedir'), r.content, 'wb')
                obj['saveurl'] = saveurl
                return obj