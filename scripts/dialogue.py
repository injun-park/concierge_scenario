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

    def handleInit(self):
        self.initialize()

        sentence = "안녕하세요. 만나서 반갑습니다. 저와 이야기 하고 싶으면 안녕~ 이라고 말씀해 주세요."
        self.ui.sendRobotMsg(sentence)
        self.tts.speak(sentence)


    def getConversationResult(self):
        def mic_callback():
            self.ui.sendUserInputWating()

        #
        # speech callback function
        #
        def speech_callback(speech_result):
            print('Confidence: {}'.format(speech_result.confidence))
            print('Transcript: {}'.format(speech_result.transcript))
            print "is_final : ", speech_result.isFinal
            print ""

            self.ui.sendUserMsg(speech_result.transcript)

        speech_result = stt_google.recognize(speech_callback, mic_callback)
        aibril_response = self.conversation.getResponse(speech_result.transcript)
        response_formatted = json.dumps(aibril_response, indent=2, ensure_ascii=False)
        rospy.loginfo(response_formatted.encode('utf8'))

        return aibril_response


    def recogSpeech(self):
        result = None
        RECOG_LIMIT = 3
        recogTrial = 0
        self.stt = SpeechRecognizer()
        while recogTrial < RECOG_LIMIT :
            if not self.userDetector.isDetected() :
                raise CannotDetectUserException()

            self.ui.sendUserInputWating()
            result = self.stt.recognize()
            if result.success_flag == result.SUCCESS : break
            self.tts.speak("음성인식에 실패 하였습니다. 다시 말씀 해 주세요")
            self.ui.sendRobotMsg("음성인식에 실패 하였습니다. 다시 말씀 해 주세요")
        self.ui.sendUserMsg("user sentence : " + str(result.sentence))
        rospy.loginfo("sentence : " + str(result.sentence) +", flag : " + str(result.success_flag))
        return result


if __name__ == "__main__":
    rospy.init_node('dialogue_node', anonymous=True)
    dialogue = Dialogue()
    dialogue.main()
    rospy.spin()
