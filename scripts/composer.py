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


class Composer :
    def __init__(self): pass

    def initialize(self):
        self.tts = TTS()
        self.ui = UI_Control()
        self.conversation = Conversation()
        self.user_detector = UserDetector()

        self.user_detector.startDetection()
        self.user_detector.checkDetection()

        sentence = "사용자가 감지 되었습니다. 저와 이야기 하고 싶으면 안녕이라고 말씀해주세요. "
        self.ui.sendRobotMsg(sentence)
        self.tts.speak(sentence)

    def main(self):
        is_shutdown = False
        while is_shutdown is not True :
            self.initialize()
            conversation_finish = False
            try:
                while conversation_finish is not True :

                    if not self.user_detector.isDetected() :
                        raise CannotDetectUserException()

                    conversation_result = self.get_converation_result()
                    response_sentences = conversation_result['output']['text'][0]
                    self.ui.sendRobotMsg(response_sentences)
                    self.tts.speak(response_sentences)

                    try:
                        finish_flag = conversation_result['output']['finish_flag']
                        if finish_flag is not None and finish_flag == "true": conversation_finish = True
                    except KeyError as e:
                        pass

                    try :
                        entities = conversation_result['entities']
                        for entity in entities :
                            if entity['entity'] == "shutdown" :
                                conversation_finish = True
                                is_shutdown = True
                    except KeyError as e :
                        pass

            except CannotDetectUserException as e :
                self.tts.speak("사용자가 사라졌습니다. 초기 상태로 돌아 갑니다.")

        rospy.loginfo("main loop finish")


    def get_converation_result(self):
        def mic_callback() :
            self.ui.sendUserInputWating()

        #
        # speech callback function
        #
        def speech_callback(speech_result) :
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



if __name__ == "__main__" :
    rospy.init_node('scenario_composer', anonymous=True)
    composer = Composer()
    composer.main()
    rospy.spin()

