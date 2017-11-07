#-*- coding: utf-8 -*-
#!/usr/bin/python

import rospy
import json
from stt import SpeechRecognizer
from TTS import  TTS
from conversation.conversation import Conversation


def recogSpeech(tts, stt):
    result = None
    RECOG_LIMIT = 3
    recogTrial = 0
    while recogTrial < RECOG_LIMIT:
        result = stt.recognize()
        rospy.loginfo("sentence : " + str(result.sentence) + ", flag : " + str(result.success_flag))

        if result.success_flag == 1 : break
        else :
            tts.speak("구글 음성인식기 오류 입니다. 다시 말씀해 주세요.")
            recogTrial = recogTrial +  1


    rospy.loginfo("sentence : ---->" + str(result.sentence) + ", flag : " + str(result.success_flag))
    return result

def getConversationResult(tts, stt, conversation) :
    sr_result = recogSpeech(tts, stt)
    conv_result = conversation.getResponse(sr_result.sentence)
    response_sentences = conv_result['output']['text']
    for sentence in response_sentences :
        tts.speak(sentence)
    return conv_result



if __name__ == "__main__" :
    rospy.init_node("conversation_test", anonymous=True)
    conversation = Conversation()
    stt = SpeechRecognizer()
    tts = TTS()
    finish_flag = False

    tts.speak("안녕이라고 말씀해 주세요")
    while finish_flag is not True :
        response  = getConversationResult(tts, stt, conversation)
        response_formatted = json.dumps(response, indent=2, ensure_ascii=False)
        print response_formatted


    rospy.spin()