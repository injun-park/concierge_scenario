#-*- coding: utf-8 -*-
#!/usr/bin/python

import time
import rospy
import Queue
from urllib2 import Request, urlopen, URLError, HTTPError
from concierge_scenario.srv import sr_result, sr_resultResponse, sr_resultRequest
import speech_recognition as sr

class STT_STATE :
    LISTENING_STARTED = 1
    RECORDING_FINISHED = 2
    RECOGNITION_FINISHED = 3

    LISTENING_TIMEOUT_ERROR = 11
    UNKNOWN_VALUE_ERROR = 12
    REQUEST_ERROR = 13

class STT_B :

    def __init__(self, callback = None):
        if(callback is None) :
            self.state_callback = self.ownCallback
        else :self.state_callback = callback

    def ownCallback(self, code, value): pass


    def recognize(self):
        r = sr.Recognizer()
        m = sr.Microphone()

        result = ''
        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
            # Speech recognition using Google Speech Recognition
            try:

                r.operation_timeout = 10
                self.state_callback(STT_STATE.LISTENING_STARTED, '')
                audio = r.listen(source, 5)
                self.state_callback(STT_STATE.RECORDING_FINISHED, '')
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                result = r.recognize_google(audio, language='ko-KR')
                self.state_callback(STT_STATE.RECOGNITION_FINISHED, '')
            except sr.WaitTimeoutError as e :
                self.state_callback(STT_STATE.LISTENING_TIMEOUT_ERROR, str(e))
                raise e
            except sr.UnknownValueError as e:
                self.state_callback(STT_STATE.UNKNOWN_VALUE_ERROR, "Google Speech Recognition could not understand audio")
                raise  e
            except sr.RequestError as e:
                self.state_callback(STT_STATE.REQUEST_ERROR, "Could not request results from Google Speech Recognition service; {0}".format(e))
                raise e

        rospy.loginfo("google speech result : " + str(result.encode('utf8')))
        return result

if __name__ == "__main__" :

    def speech_callback(code, value) :
        if code == STT_STATE.LISTENING_STARTED : print "listening started"
        elif code == STT_STATE.RECORDING_FINISHED : print "recording finished and request wav to google-cloud"
        elif code == STT_STATE.UNKNOWN_VALUE_ERROR : print value
        elif code == STT_STATE.LISTENING_TIMEOUT_ERROR : print value
        elif code == STT_STATE.REQUEST_ERROR : print value

    stt = STT_B(speech_callback)
    result = stt.recognize()
    print result