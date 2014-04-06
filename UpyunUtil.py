#!/usr/bin/env python
# -*- coding: utf-8 -*-

import upyun, simplejson, os, logging
from SUtils import logger, log_it

class UpyunUtil():
    up = None
    _spaceName = 'xiaohua123' 
    _userName = 'xiaohua123'
    _userPasswd = 'xiaohua123'
    _rootDir = 'happiness'
    _rootUrl = 'http://xiaohua123.b0.upaiyun.com/'

    # @log_it(pos=('begin', 'end'), level=logging.INFO, logArgs=False)
    @staticmethod
    def uploadStream(content, obj):
        if not UpyunUtil.up:
            UpyunUtil.up = upyun.UpYun(UpyunUtil._spaceName, UpyunUtil._userName, UpyunUtil._userPasswd)

        savedir = os.path.join(UpyunUtil._rootDir, obj.get('savedir')) if obj.get('savedir') else UpyunUtil._rootDir
        savename = os.path.join(savedir, obj['savename'])
        try:
            res = UpyunUtil.up.put(savename, content)
        except Exception as e:
            logger.exception(e.message)
            # namespace.emit('downloadError', obj)
            return None
        else:
            logger.info(simplejson.dumps(res, indent=4, ensure_ascii=False))
            obj['saveurl'] = UpyunUtil._rootUrl+savename
            # namespace.emit('uploadUpyun', obj)
            return obj