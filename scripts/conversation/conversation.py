#-*- coding: utf-8 -*-

import auth
import json
from watson_developer_cloud import ConversationV1

class Conversation :
    def __init__(self, **kwargs):

        self.username = ''
        self.password = ''
        self.workspaceId = ''
        self.version = '2017-05-26'
        self.url = auth.url

        try : self.username = kwargs['username']
        except KeyError as e : self.username = ''

        try : self.password = kwargs['password']
        except KeyError as e : self.password = ''

        try : self.workspace_id = kwargs['workspace_id']
        except KeyError as e : self.workspace_id=''



        self.conversatin = ConversationV1(
          username=self.username,
          password=self.password,
          version='2017-05-26',
          url = auth.url
        )

        self.context = {}


    def getResponse(self, input):
        response = self.conversatin.message(
            workspace_id = self.workspace_id,
            message_input = {'text' : input},
            context = self.context
        )
        self.context = response['context']
        return response


if __name__ == "__main__" :
    conv = Conversation()

    finish = False
    while not finish :
        input = raw_input("입력 : ")
        print "\n"
        response = conv.getResponse(input)
        response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
        print response_formatted


        try :
            finish_flag = response['output']['finish_flag']
        except KeyError as e :
            print e
            finish_flag = False

        if finish_flag == "true" : break;



