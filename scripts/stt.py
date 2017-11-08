#-*- coding: utf-8 -*-
#!/usr/bin/python

import time
import rospy
import Queue
from concierge_scenario.srv import sr_result, sr_resultResponse, sr_resultRequest
import speech_recognition as sr


class SpeechResult :
    def __init__(self):
        self.FAIL = 0
        self.SUCCESS = 1
        self.TIMEOUT = 2
        self.REQUEST_ERROR = 3
        self.UNKNOWN_VALUE_ERROR = 4

        self.success_flag = 0
        self.sentence = ''


class SpeechRecognizer :
    def __init__(self):
        self.stopListening = None
        self.queue = Queue.Queue()
        self.TIMEOUT = 5.0

        #
        # self.service = rospy.Service('/stt', sr_result, self.handle_request)
    def handle_request(self, request):
        self.recognize()



    def speechCallback(self, recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            user_sentence = recognizer.recognize_google(audio, language='ko-KR')
            print("Google Speech Recognition thinks you said " + user_sentence)

            result = SpeechResult()
            result.success_flag = result.SUCCESS
            result.sentence = user_sentence.encode('utf8')
            self.queue.put(result)
            print "stt result pushed"

        except sr.UnknownValueError:

            result = SpeechResult()
            result.success_flag = result.UNKNOWN_VALUE_ERROR
            result.sentence = ''

            self.queue.put(result)
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            result = SpeechResult()
            result.success_flag = result.REQUEST_ERROR
            result.sentence = ''
            self.queue.put(result)
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def recognize(self):
        rospy.loginfo("speech recognizer triggered")

        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

            # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stopListening = r.listen_in_background(m, self.speechCallback)
            # `stop_listening` is now a function that, when called, stops background listening

        loop_count = 0
        LOOP_COUNT_LIMIT = 50
        sample_duration = rospy.Duration(self.TIMEOUT / LOOP_COUNT_LIMIT)
        while self.queue.empty() and loop_count < LOOP_COUNT_LIMIT :
            rospy.sleep(sample_duration)
            loop_count += 1
            rospy.loginfo("listening loop count : " + str(loop_count))
        self.stopListening()
        rospy.loginfo("stt:stoplistening triggered")
        if(self.queue.empty()) :
            rospy.logwarn("speech recognition time out")
            result = SpeechResult()
            result.success_flag = result.TIMEOUT
            result.result = ''
            self.queue.put(result)

        result = self.queue.get()
        self.stopListening()

        rospy.loginfo("SpeechRecognition : stopListening activated")

        return result


#
# just for testing
#
#
if __name__ == "__main__" :
    rospy.init_node("speech_recognizer", anonymous=True)
    ss = SpeechRecognizer()
    result = ss.recognize()
    print result.sentence
    rospy.spin()
