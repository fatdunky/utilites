'''
Created on 22 Dec. 2017

@author: mcrick
'''
import requests


def simple_get_request_no_verify(url):
    return requests.get(url, verify=False)

def simple_get_request(url):
    return requests.get(url)