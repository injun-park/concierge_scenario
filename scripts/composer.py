#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import rospy
import json
from TTS import  TTS
from stt import SpeechRecognizer
from conversation.conversation import Conversation
from user_detection.msg import  UserDetectionMsg



class UserDetector :

    __THRESHOLD_POINT_COUNT = 30000

    def __init__(self):
        self.detected = False
        self.averageDistance = 0.0
        self.pointSize = 0

    def userDetectedCallback(self, data):
        # rospy.loginfo("data.detected : " + str(data.detected) +
        #               ", data.point_size : " + str(data.point_size) +
        #               ", data.average_distance : " + str(data.average_distance) )

        self.detected = True
        self.averageDistance = data.average_distance
        self.pointSize = data.point_size

    def isDetected(self):
        if self.averageDistance < 1.0 and self.pointSize > UserDetector.__THRESHOLD_POINT_COUNT :
            return True

        return False

    def startDetection(self):
        self._userDetectorSubscriber = rospy.Subscriber('/distance_filter/data', UserDetectionMsg, self.userDetectedCallback)
        return True

    def stopDetection(self):
        self._userDetectorSubscriber.unregister()


    def checkDetection(self):
        duration = rospy.Duration(0.05) # 20hz
        detected = False
        while not self.isDetected() :
            rospy.sleep(duration)
            continue

class CannotDetectUserException(Exception) :
    def __init__(self):
        self.value = "CannotDetecUserException"

    def __str__(self):
        return self.value


class ScenarioComposer :
    def __init__(self):
        self.userDetector = UserDetector()
        self.userDetector.startDetection()
        self.tts = TTS()


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
            result = self.stt.recognize()
            if result.success_flag == result.SUCCESS : break
            self.tts.speak("음성인식에 실패 하였습니다. 다시 말씀 해 주세요")
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
        self.conversation = Conversation()
        self.userDetector.checkDetection()
        rospy.loginfo("user detected")
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


