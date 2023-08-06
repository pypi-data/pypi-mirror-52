# -*- coding: utf-8 -*-
import requests
# from strgen import StringGenerator

def test():
    url = "https://chat-public.one.th:8034"
    # url2 = "http://testchat.one.th:30003"
    # url = "http://localhost:3000/"+str(callfunction)
    # payload = data
    try:
        # return url
        response = requests.request("GET", url=url, verify=False)
        return response.text
    except Exception as strE:
        return strE.message
