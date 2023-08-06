# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:21:30 2019

@author: ggang.liu
"""

import time
import logging
import requests
from datetime import datetime, timedelta 

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a',
                        filename='auto-auth.log',
                        filemode='w'
                        )

def auth(auth_ip, user_name, user_password):
    """
    This function will help to authenticate once only
    """
    payload = {}
    payload['username'] = user_name
    payload['password'] = user_password
    success_flag = 'User Authentication : Success'
    ret = False
    
    with requests.Session() as s:
        p = s.post(auth_ip, data=payload)
        if success_flag in p.text:
            ret = True

    return ret


def period_auth(auth_ip, user_name, user_password, hours=0, minutes=2):
    """
    This function will help to authenticate periodically
    """
    periodSecond     = 60 #second
    internal_hours   = hours
    internal_minutes = minutes
        
    nextTime = currentTime = datetime.now() 
    logging.info("internal_hours = {}, internal_minutes = {}".format(internal_hours, internal_minutes))
    logging.info("Task started, at {}, next time is {}".format(str(currentTime), str(nextTime)))
    
    while True:
        currentTime = datetime.now() 
        if currentTime >= nextTime:
            if auth(auth_ip, user_name, user_password):
                logging.info(str(currentTime) + ' auth successed.')
            else:
                logging.info(str(currentTime) + ' auth failed.')
            
            nextTime = currentTime + timedelta(hours = internal_hours, minutes = internal_minutes)
            logging.info("{} is next time point".format(str(nextTime)))
        else:
            time.sleep(periodSecond)
            