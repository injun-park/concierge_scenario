#!/usr/bin/python
#-*- coding: utf-8 -*-

import rospy
import rospkg
from concierge_msgs.msg import ui_msg
from jinja2 import  Environment, select_autoescape, FileSystemLoader


class UI_Control :
    def __init__(self):
        self.publisher = rospy.Publisher("/ui_control", ui_msg, tcp_nodelay = True, queue_size=5)
        rospack = rospkg.RosPack()
        pkgpath = rospack.get_path('concierge_scenario')

        templatePath = pkgpath +"/ui/html"
        self.env = Environment(
            loader=FileSystemLoader(templatePath, encoding='utf-8'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def sendMsg(self, msg):
        self.publisher.publish(msg)

    def sendMsg(self, command, reserved, sentence):
        msg = ui_msg()
        ui_msg.command = command
        ui_msg.reserved = reserved
        ui_msg.sentence = sentence

        self.publisher.publish(msg)

    def sendAibrilMsg(self, aibril_response):
        response_examples = []
        intents = aibril_response['intents']
        for intent in intents :
            if intent['intent'] == 'hello' :
                response_examples.append(unicode('게이트안내', 'utf-8'))
                response_examples.append(unicode('편의시설안내', 'utf-8'))
                response_examples.append(unicode('운항정보 안내', 'utf-8'))
                response_examples.append(unicode('도착지 정보안내', 'utf-8'))
            elif intent['intent'] == 'convenient_facilities_guide' :
                response_examples.append(unicode('환전소', 'utf-8'))
                response_examples.append(unicode('은행', 'utf-8'))
                response_examples.append(unicode('커피숍', 'utf-8'))
                response_examples.append(unicode('편의점', 'utf-8'))
                response_examples.append(unicode('면세점', 'utf-8'))
                response_examples.append(unicode('식당', 'utf-8'))
                response_examples.append(unicode('로밍', 'utf-8'))
                response_examples.append(unicode('흡연실', 'utf-8'))
            elif intent['intent'] == 'gate_guide' :
                response_examples.append(unicode('1번 게이트 위치 알려주세요.', 'utf-8'))
                response_examples.append(unicode('5번 게이트 위치 알려주세요.', 'utf-8'))
                response_examples.append(unicode('12번 게이트 위치 알려주세요.', 'utf-8'))
                response_examples.append(unicode('기타등등 게이트 위치 알려주세요.', 'utf-8'))
            elif intent['intent'] == 'fiight_guide' :
                response_examples.append(unicode('<flight> [비행기|비행기에 대해] {정보|운항 정보} {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('<flight> 비행기에 대해 {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('<airline> <flight>[에 대해] [정보|운항 정보] {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('<city> {행|가는} <airline> [비행기|편|비행기에 대해|편에 대해] [정보|운항 정보] {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('<flight> [비행기|비행기에 대해] {정보|운항 정보} {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('<airport> [공항] {행|가는} <airline> [비행기|편|비행기에 대해|편에 대해] [정보|운항 정보] {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('[오전|오후] <hour> <minutes> [출발하는|떠나는] <airline> [비행기|편|비행기에 대해|편에 대해] [정보|운항 정보] {안내해 줘|보여줘|알려줘}', 'utf-8'))
                response_examples.append(unicode('[오전|오후] <hour> <minutes> [출발하는|떠나는] <airline> [비행기|편|비행기에 대해|편에 대해] [정보|운항 정보] {안내해 줘|보여줘|알려줘}', 'utf-8'))
            elif intent['intent'] == 'arrival_guide' :
                response_examples.append(unicode('하네다 공항 날씨 어때?', 'utf-8'))
                response_examples.append(unicode('상해 날씨 어때요?.', 'utf-8'))
                response_examples.append(unicode('간사히 공항 날씨 알려주세요.', 'utf-8'))
                response_examples.append(unicode('도쿄나 베이징 공항은 날씨가 어때요?', 'utf-8'))



        context = {
            'intents' : aibril_response['intents'],
            'entities' : aibril_response['entities'],
            'sentence' : aibril_response['output']['text'][0],
            'response_examples' : response_examples
        }


        template = self.env.get_template("robot_saying.html")
        merged = template.render(context)

        msg = ui_msg()
        msg.html = merged

        self.waitSubscribers()
        self.publisher.publish(msg)

    def sendRobotMsg(self, sentence):
        msg = ui_msg()
        # msg.reserved = 0
        # msg.command = msg.UI_ROBOT_SENTENCE
        # msg.sentence = sentence
        #sentence = unicode(sentence, 'utf-8')
        context = {
            'sentence' : sentence
        }

        template = self.env.get_template("robot_saying.html")
        merged = template.render(context)

        msg.html = merged

        self.waitSubscribers()
        self.publisher.publish(msg)

    def sendUserMsg(self, sentence):
        msg = ui_msg()
        msg.reserved = 0
        msg.command = msg.UI_USER_SENTENCE
        msg.sentence = sentence

        context = {
            "sentence" : sentence
        }
        template = self.env.get_template("user_saying.html")
        merged = template.render(context)
        msg.html = merged

        self.waitSubscribers()
        self.publisher.publish(msg)

    def sendUserInputWating(self):
        msg = ui_msg()
        msg.reserved = 0
        msg.command = msg.UI_WAIT_USER_INPUT
        msg.sentence = ''

        context = {}
        template = self.env.get_template("mic_animation.html")
        merged = template.render(context)
        msg.html = merged

        self.publisher.publish(msg)

    def waitSubscribers(self):
        count = 0
        rate = rospy.Rate(20)
        while count < 1 :
            count = self.publisher.get_num_connections()
            rate.sleep()

if __name__ == "__main__" :
    rospy.init_node('ui_controll', anonymous=True)

    ui = UI_Control()
    rate = rospy.Rate(10)

    for i in range(20) :
        ui.sendRobotMsg("안녕하세요. 만나서 반갑습니다.")
        rate.sleep()


