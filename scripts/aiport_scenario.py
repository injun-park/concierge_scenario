#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import rospy
import json
from TTS import  TTS
import stt_google
from conversation.conversation import Conversation
from user_detector import UserDetector
from user_detector import CannotDetectUserException
from ui_control import UI_Control


class RequestHandler :
    def __init__(self): pass

class AirportConcierge :
    def __init__(self):
        pass

    def initialize(self):
        self.tts = TTS()
        self.ui = UI_Control()
        self.conversation = Conversation(
            username='e4b29b57-c38e-47cd-b89d-c65485756d56',
            password='bHYBxAVxOW3l',
            workspace_id='b291e39c-254a-46f5-80d9-b3f63fa0c58f'
        )

    def main(self):
        self.handleInit()

        finished = False
        while finished is not True :
            response = self.getConversationResult()
            response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
            rospy.loginfo(response_formatted.encode('utf8'))
            self.checkShutdown(response)
            self.handleAibrilResponse(response)

    def handleInit(self):
        self.initialize()

        sentence = "안녕하세요. 만나서 반갑습니다. 저와 이야기 하고 싶으면 안녕 이라고 말씀해 주세요."
        self.ui.sendRobotMsg(unicode(sentence, 'utf-8'))
        self.tts.speak(sentence)


    def handleAibrilResponse(self, response):
        self.ui.sendAibrilMsg(response)
        text = None
        for text in response['output']['text'] :
            self.tts.speak(text)


    def getConversationResult(self):
        def mic_callback():

            self.ui.sendUserInputWating()

        #
        # speech callback function
        #
        def speech_callback(speech_result):
            # print('Confidence: {}'.format(speech_result.confidence))
            # print('Transcript: {}'.format(speech_result.transcript))
            # print "is_final : ", speech_result.isFinal
            self.ui.sendUserMsg(speech_result)
            print ""

            #self.ui.sendUserMsg(speech_result.transcript)

        speech_result = stt_google.recognize(mic_callback=mic_callback, sentence_callback=speech_callback)
        self.ui.sendUserMsg(speech_result)

        response = self.conversation.getResponse(speech_result)
        response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
        rospy.loginfo(response_formatted.encode('utf8'))

        #import  aibril_response
        #response = aibril_response.AibrilResponse.newInstance(response)
        return response

    def checkShutdown(self, response):
        entities = response['entities']
        for entity in entities:
            if entity['entity'] == "shutdown":
                self.tts.speak('프로그램을 종료 합니다.')
                sys.exit(1)


if __name__ == "__main__":
    rospy.init_node('dialogue_node', anonymous=True)
    scenario = AirportConcierge()
    scenario.main()
    rospy.spin()
