#-*- coding: utf-8 -*-

import rospy
from silbot3_msgs.srv import TTSMake
from silbot3_msgs.srv import TTSMakeRequest
from silbot3_msgs.srv import SoundPlay
from silbot3_msgs.srv import SoundPlayRequest

from std_msgs.msg import String
from std_msgs.msg import Empty

class TTS :
    def __init__(self):

        TTS_SRV_NAME = "/silbot3_tts/make"
        SOUND_SRV_NAME = "/silbot3_sound/play"

        # rospy.loginfo("wating for service" + TTS_SRV_NAME)
        # rospy.wait_for_service(TTS_SRV_NAME)
        # rospy.loginfo("service " + TTS_SRV_NAME + " detected")
        #
        # rospy.loginfo("wating for service" + SOUND_SRV_NAME)
        # rospy.wait_for_service(SOUND_SRV_NAME)
        # rospy.loginfo("service " + SOUND_SRV_NAME + " detected")

        self.__TMP_FILE_PATH = "/tmp/speak.wav"

        self.ttsSRV = rospy.ServiceProxy(TTS_SRV_NAME, TTSMake)
        self.soundSRV = rospy.ServiceProxy(SOUND_SRV_NAME, SoundPlay)

        self.playPub = rospy.Publisher("/silbot3_sound/play", String, queue_size=10)
        self.stopPub = rospy.Publisher("/silbot3_sound/stop", Empty, queue_size=10)

        # duration = rospy.Rate(10)
        # while not rospy.is_shutdown() and self.playPub.get_num_connections() < 1 :
        #     rospy.loginfo("wating sound player")
        #     duration.sleep()
        # rospy.loginfo("sound player detected")


    def makeWAV(self, text, filepath):
        req = TTSMakeRequest()
        req.text = text
        req.filepath = filepath
        self.ttsSRV(req)

    def playWAV(self, filepath):
        #self.playPub.publish(filepath)
        req = SoundPlayRequest()
        req.filepath = filepath
        self.soundSRV(req)


    def speak(self, sentence):
        self.makeWAV(sentence, self.__TMP_FILE_PATH)
        self.playWAV(self.__TMP_FILE_PATH)

if __name__ == "__main__" :
    rospy.init_node("tts", anonymous=True)
    tts = TTS()
    tts.speak('안녕하시렵니까.')
