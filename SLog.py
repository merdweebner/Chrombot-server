#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, os

def InitLog():          
    #logging level: DEBUG<INFO<WARNING<ERROR<CRITICAL(FATAL)
    logfile = 'log/chrombot_server.log'
    dirname = os.path.dirname(logfile)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)
    
    info_hd = logging.FileHandler(logfile)
    info_hd.setLevel(logging.INFO)

    debug_hd = logging.StreamHandler()
    debug_hd.setLevel(logging.DEBUG)
        
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d | %(message)s', '%H:%M:%S') 
    debug_hd.setFormatter(formatter)
    info_hd.setFormatter(formatter)

    logger.addHandler(info_hd)
    logger.addHandler(debug_hd)

    #socketIO_client 
    socketIO_client_logger = logging.getLogger('socketIO_client')
    socketIO_client_logger.addHandler(debug_hd)
    #[temp]
    # try:
    #     from raven.handlers.logging import SentryHandler
    #     from raven.conf import setup_logging
    #     sentry_handler = SentryHandler('http://a14e916c4ef347eba4633be6342d6c60:e39b735d73674f08ac9f58d188f3e512@192.168.20.110:9000/2', auto_log_stacks=True)
    #     sentry_handler.setFormatter(formatter)
    #     sentry_handler.setLevel(logging.WARNING)
    #     setup_logging(sentry_handler)
    #     logger.addHandler(sentry_handler)
    # except ImportError:
    #     pass

    return logger

