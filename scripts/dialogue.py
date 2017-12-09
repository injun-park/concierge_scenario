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

class Dialogue :
    def __init__(self):
        pass

    def initialize(self):
        self.tts = TTS()
        self.ui = UI_Control()
        self.conversation = Conversation()

    def main(self):
        self.handleInit()

        finished = False
        while finished is not True :
            response = self.getConversationResult()
            response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
            rospy.loginfo(response_formatted.encode('utf8'))
            self.handleAibrilResponse(response)
            self.checkShutdown(response)
            if self.checkFinishFlag(response):
                self.tts.speak(("현재 대화 세션을 종료 하고, 초기 상태로 돌아갑니다."))
                self.handleInit()

    def checkFinishFlag(self, response):
        try :
            finish_flag = response['output']['finish_flag']
            if finish_flag is not None and finish_flag == "true": return True
        except KeyError as e :
            return False

    def handleInit(self):
        self.initialize()

        sentence = "안녕하세요. 만나서 반갑습니다. 저와 이야기 하고 싶으면 안녕 이라고 말씀해 주세요."
        self.ui.sendRobotMsg(unicode(sentence, 'utf-8'))
        self.tts.speak(sentence)


    def handleAibrilResponse(self, response):
        self.ui.sendAibrilMsg(response)
        self.tts.speak(response['output']['text'][0])


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
                sys.exit(1)


if __name__ == "__main__":
    rospy.init_node('dialogue_node', anonymous=True)
    dialogue = Dialogue()
    dialogue.main()
    rospy.spin()
