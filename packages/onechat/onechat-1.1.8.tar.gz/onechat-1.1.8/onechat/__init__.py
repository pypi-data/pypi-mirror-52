# -*- coding: utf-8 -*-
import requests
# from strgen import StringGenerator
class BotOnechat:
    def __init__(self,bot_id,auth):
        self.bot_id = str(bot_id)
        self.auth = str(auth)

    def checkConnect(self):
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

    def sendTextMessage(self,message,one_id):
        url = 'https://chat-public.one.th:8034/api/v1/push_message'
        try:
            payload = {
                'bot_id':self.bot_id,
                'to':one_id,
                'type':'text',
                'message':message
            }
            headers = {
                'Content-Type': "application/json",
                'Authorization': self.auth,
                'cache-control': "no-cache"
            }
            response = requests.request("POST",url=url,json=payload,headers=headers,verify=False)
            return response.text
            # return self.bot_id
        except Exception as strE:
            return strE.message
    def sendTemplate(self,element,one_id):
        url = 'https://chat-public.one.th:8034/api/v1/push_message'
        try:
            # for i in element:
            #     if 'title' not in i or 'detail' not in i or 'choice' not in i:
            #         return {'status':'fail','message':'Some element missing parameter.'}
            #     if isinstance(i['title'],basestring) == False or isinstance(i['detail'],basestring) == False or isinstance(i['choice'], (list,)) == False:
            #         return {"status": "fail","message":"Value of parameter not support."}
            #     if len(i['choice']) > 4 or len(i['choice']) == 0:
            #         return {'status':'fail','message':'Error choice.'}
            #     if len(i['title']) > 80 or len(i['detail']) > 400:
            #         return {'status':'fail','message':'Error format detail or title.'}
            #     i['title'] = i['title'].encode('utf-8')
            #     i['detail'] = i['detail'].encode('utf-8')
            #     for x in i['choice']:
            #         if 'label' not in x or 'type' not in x:
            #             return {'status':'fail','message':'Wrong Format choice.'}
            #         if x['type'] not in ['text','link','webview','file']:
            #             return {'status':'fail','message':'Wrong Format choice.'}
            #         if x['type'] == 'webview':
            #             if 'size' not in x:
            #                 return {'status':'fail','message':'Undefined size for webview.'}
            #             if x['size'] not in ['compact','tall','full']:
            #                 return {'status':'fail','message':'Unknow parameter size.'}
            #         if len(x['label']) > 80:
            #             return {'status':'fail','message':'Out of range label.'}
            #         x['label'] = x['label'].encode('utf-8')
            #         if x['type'] == 'file':
            #             if 'file' not in x:
            #                 return {'status':'fail','message':'Not found file part.'}
            payload = {
                'bot_id':self.bot_id,
                'to':one_id,
                'type':'template',
                'element':element
            }
            headers = {
                'Content-Type': "application/json",
                'Authorization': self.auth,
                'cache-control': "no-cache"
            }
            response = requests.request("POST",url=url,json=payload,headers=headers,verify=False)
            return response.text
        except Exception as strE:
            return strE.message

    def getBotId(self):
        return self.bot_id
    def getAuth(self):
        return self.auth



def test22():
    url = "https://chat-public.one.th:8034"
    # url2 = "http://testchat.one.th:30003"
    # url = "http://localhost:3000/"+str(callfunction)
    # payload = data
    try:
        # return url
        response = requests.request("GET", url=url, verify=False)
        return response
    except Exception as strE:
        return strE.message
