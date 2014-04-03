#!/usr/bin/env python
# -*- coding: utf-8 -*-

import upyun, simplejson, os
from SUtils import logger

class UpyunUtil():
    up = None
    _spaceName = 'revir' 
    _userName = 'revir'
    _userPasswd = 'qing2008'
    _rootDir = 'happiness'
    _rootUrl = 'http://revir.b0.upaiyun.com/'

    # [TODO] exception
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