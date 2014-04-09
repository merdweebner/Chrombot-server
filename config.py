#!/usr/bin/env python
# -*- coding: utf-8 -*-
gConfig = {
    "downloadThreads": 3,  #not used any more
    "downloadUsingProxy": {
        "enabled": True,
        "proxies": {
            'http': 'http://127.0.0.1:8087', 
            'https': 'https://127.0.0.1:8087'
        }
    },
    "downloadTimeout": 1   #download timeout, used by requests.get()
}
