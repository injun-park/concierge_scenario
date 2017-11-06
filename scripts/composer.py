#!/usr/bin/python
#-*- coding: utf-8 -*-


import rospy
from TTS import  TTS
from stt import SpeechRecognizer
from user_detection.msg import  UserDetectionMsg



class UserDetector :

    __THRESHOLD_POINT_COUNT = 70000

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
        self._userDetectorSubscriber = rospy.Subscriber('/distance_filter/data', UserDetectionMsg,
                                                        self.userDetectedCallback)

    def stopDetection(self):
        self._userDetectorSubscriber.unregister()


    def checkDetection(self):
        duration = rospy.Duration(0.05) # 20hz
        detected = False
        while not self.isDetected() :
            rospy.sleep(duration)
            continue


class ScenarioComposer :
    def __init__(self):
        self.userDetector = UserDetector()
        self.userDetector.startDetection()

        self.tts = TTS()
        self.stt = SpeechRecognizer()


    def initState(self):
        self.userDetector.checkDetection()
        self.tts.speak("사용자가 감지 되었습니다.")


    def welcomeStage(self):
        self.tts.speak("안녕하세요. 저는 안내로봇이라고 해요. 만나서 반갑습니다.")
        self.tts.speak("저와 이야기 하고 싶으면, '안녕' 이라고 말씀해 주세요.")
        result = self.recogSpeech()
        sentence = result.sentence.replace(' ', '')
        if(sentence == '안녕') :
            print "ok"
        self.tts.speak("저는 Navigation기능을 통해, 장소를 안내 할 수 있고, 장소에 대한 정보를 전달 할 수 있습니다.")
        self.tts.speak("장소 안내를 받고 싶으면 '장소안내' 라고 말씀해 주시고, 건물에 대한 정보를 알고 싶으면, '장소정보' 라고 말씀해 주세요")
        result = self.stt.recognize()
        rospy.loginfo("sentence : " + str(result.sentence) + ", flag : " + str(result.success_flag))


    def recogSpeech(self):
        result = None
        RECOG_LIMIT = 3
        recogTrial = 0
        while recogTrial < RECOG_LIMIT :
            result = self.stt.recognize()
            if result.success_flag == result.SUCCESS : break
            self.tts.speak("음성인식에 실패 하였습니다. 다시 말씀 해 주세요")
        rospy.loginfo("sentence : " + str(result.sentence) +", flag : " + str(result.success_flag))
        return result

if __name__ == "__main__" :
    rospy.init_node('scenario_composer', anonymous=True)
    s = ScenarioComposer()
    s.initState()
    s.welcomeStage()
    rospy.spin()


