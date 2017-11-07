#-*- coding: utf-8 -*-

import auth
import json
from watson_developer_cloud import ConversationV1

class Conversation :
    def __init__(self):
        self.conversatin = ConversationV1(
          username="ee7353c0-8f48-49d3-b747-00057699ef18",
          password="ra8Z4w4qxrNd",
          version='2017-05-26',
          url = auth.url
        )

        self.workspace_id = auth.workspace_id
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



