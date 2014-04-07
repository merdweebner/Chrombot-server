#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, threading, shutil, simplejson, exceptions, logging
import SLog

class TaskException(Exception):
    pass

class SRepeatableTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def start(self):
        self.stop()
        self._beginTimer()
    def _beginTimer(self):
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.setDaemon(True)
        self._timer.start()
    def restart(self): 
        self.start()

    def stop(self):
        if self.__dict__.has_key("_timer"):
            self._timer.cancel()
            del self._timer
    def _run(self):
        try:
            self.function(*(self.args), **(self.kwargs))
        except KeyboardInterrupt:
            logger.info('recieved KeyboardInterrupt, SRepeatableTimer stop!')
            self.stop()
        except Exception as data:
            logger.error(str(type(data))+':'+str(data))
            logger.error('SRepeatableTimer run function error!')
            self.restart()
        else:
            self.restart()

### decorator functions
def log_it(pos=('begin'), level=logging.DEBUG, logArgs=True, logReturnValue=True, postMsg=''):
    '''Just put log at the begging or end of the func, but its format looks like markdown.
        @pos is a list, each item can be 'begin' or 'end'
        @logArgs means output the arguments or not
        @postMsg will be added at the end of the log message
        @logReturnValue means if at the end of function, it will log the return Value.
    '''
    def _log_it(func):
        def __log(*args, **kwargs):
            text = func.__name__ + ' '
            if logArgs and len(args) > 0:
                argtext = ''
                for x in args:
                    if isinstance(x, (list, dict, str, unicode, int, float, bool, type(None))):
                        argtext += simplejson.dumps(x) + ', '
                argtext = argtext.rstrip(', ')
                text += '**'+ argtext +'**'
            if logArgs and len(kwargs) > 0:
                text += ' : **' + simplejson.dumps(kwargs)+'**'
            if postMsg:
                text += ' | ' + postMsg
            if 'begin' in pos:
                logger.log(level, ' $$$begin$$$ ' + text)
            res = func(*args, **kwargs)
            if 'end' in pos:
                if res and logReturnValue:
                    text += ' | **RETURN : ' + simplejson.dumps(res) + '**'
                logger.log(level, ' $$$end$$$ ' + text)
            return res
        return __log
    return _log_it

def check_exception(func):
    def __check(*args,  **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskException as e:
            text = e.message['data']['msg']
            logger.error('TaskException: '+text)
            e.message['process'](e.message['api'], e.message['data'])
        except exceptions.EnvironmentError:
            #RemoveFile exception
            logger.exception('EnvironmentError!')
        except Exception:
            logger.exception('something wrong!')

    return __check

def argument_may_be_list(func):
    def __checkarg(obj, arg):
        res = None
        if not isinstance(arg, (tuple, list)):
            arg = [arg]
        for x in arg:
            res = func(obj, x)
        return res
    return __checkarg

### utility
def GetModuleDir():
    full_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(full_path)
    if dir_path[-1] != '/':
        dir_path += '/'
    return dir_path

def GetDomainFromUrl(strurl):
    if not strurl:
        return ''
    lpos = strurl.find('://')
    startpos = lpos + 3
    if lpos  == -1:
        logger.warning('url may be invalid: '+strurl)
        startpos = 0
    rpos = strurl.find('/', startpos+1)
    if rpos == -1:
        return strurl[startpos:]
    else:
        return strurl[startpos:rpos]

def XBool(value):
    if type(value) == str or type(value) == unicode:
        return value=='true' or value=='True'
    return bool(value)

@check_exception
def RemoveFile(item):        
    if os.path.isdir(item):
        shutil.rmtree(item) 
    else:
        os.remove(item)
        
    return True

def GetFileContent(path):
    if not os.path.exists(path):
        return ''
    ff = open(path)
    content = ff.read()
    ff.close()
    return content

def writeFile(savename, savedir, data, format="wb"):
    fileName = savename
    if(savedir):
        savedir = os.path.expanduser(savedir)
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        fileName = os.path.join(savedir, fileName)

    with open(fileName, format) as fp:
        if isinstance(data, (list, dict, str, unicode, int, float, bool, type(None))):
            simplejson.dump(data, fp, indent=4, ensure_ascii=False, encoding='utf-8')

    return fileName



def ParseCookies(content):
    linenum = 0
    cookies = []
    for line in content.split('\n'):
        linenum += 1
        line = line.strip('\r\n')
        cont = line.split(';')
        index = 0
        cookiePair = {}
        for item in cont:
            index += 1
            item = item.strip()
            dpos = item.find('=')
            if index == 1:
                cookiePair['name'] = item[:dpos]
                cookiePair['value'] = item[dpos+1:]
                continue

            if dpos == -1:
                cookiePair[item] = True
            else:
                cookiePair[item[:dpos]] = item[dpos+1:]

        cookies.append(cookiePair)

    logger.debug('Parse cookie finished: %d' % linenum)
    return cookies

toUTF8 = lambda s:s.encode('utf-8') if isinstance(s, unicode) else s
toU = lambda s:unicode(s) if isinstance(s, str) else s 

os.chdir(GetModuleDir())
logger = SLog.InitLog()

if __name__ == '__main__':

    ###Test decoration functions
    class testA(object):

        @argument_may_be_list
        @log_it(('begin', 'end'), level=logging.INFO, postMsg='so far so good.')
        def funcA(self, a):
            self.proccess(a)
            return a

        def proccess(self, s):
            print simplejson.dumps(s)

    a = testA()
    a.funcA([123, 'it is a string'])
