#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import rospy
import json
from TTS import  TTS
from stt import SpeechRecognizer
from stt_block import STT_STATE
from stt_block import STT_B
from conversation.conversation import Conversation
from user_detector import UserDetector
from user_detector import CannotDetectUserException
from ui_control import UI_Control


class Composer :
    def __init__(self): pass

    def initState(self):
        self.userDetector = UserDetector()
        self.tts = TTS()
        self.ui = UI_Control()
        self.stt = STT_B()

        self.userDetector.startDetection()



class ScenarioComposer :
    def __init__(self):
        self.userDetector = UserDetector()
        self.userDetector.startDetection()
        self.tts = TTS()
        self.ui = UI_Control()

    def checkFinishFlag(self, response):
        try :
            finish_flag = response['output']['finish_flag']
            if finish_flag is not None and finish_flag == "true": return True
        except KeyError as e :
            return False

    def checkShutdown(self, response):
        entities = response['entities']
        for entity in entities:
            if entity['entity'] == "shutdown":
                sys.exit(1)


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

    def getConversationResult(self):
        try :
            sr_result = self.recogSpeech()
            conv_result = self.conversation.getResponse(sr_result.sentence)
            response_sentences = conv_result['output']['text']
            for sentence in response_sentences:
                self.tts.speak(sentence)
            return conv_result
        except CannotDetectUserException as e :
            raise e

    def initState(self):
        rospy.loginfo("init_state")
        self.ui.sendRobotMsg("대기상태 ... 사용자 감지 중입니다.")
        self.conversation = Conversation()
        self.userDetector.checkDetection()
        rospy.loginfo("user detected")

        self.ui.sendRobotMsg("사용자가 감지 되었습니다. 저와 이야기 하고 싶으면 안녕이라고 말씀해주세요.")
        self.tts.speak("사용자가 감지 되었습니다. 저와 이야기 하고 싶으면 안녕이라고 말씀해주세요.")

    def doScenario(self):
        rospy.loginfo("scenario started")
        self.initState()
        terminated = False
        while terminated is not True :
            try :
                response = self.getConversationResult()
                response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
                rospy.loginfo(response_formatted.encode('utf8'))

                self.checkShutdown(response)
                if self.checkFinishFlag(response) :
                    self.tts.speak(("현재 대화 세션을 종료 하고, 초기 상태로 돌아갑니다."))
                    self.initState()

            except CannotDetectUserException as e :
                self.tts.speak("사용자가 사라졌습니다. 초기 상태로 돌아갑니다.")
                self.initState()
                print e

        rospy.loginfo("application terminated")

if __name__ == "__main__" :
    rospy.init_node('scenario_composer', anonymous=True)
    s = ScenarioComposer()
    s.doScenario()
    rospy.spin()

