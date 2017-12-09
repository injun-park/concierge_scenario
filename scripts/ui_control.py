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

    def sendRobotMsg(self, sentence):
        msg = ui_msg()
        # msg.reserved = 0
        # msg.command = msg.UI_ROBOT_SENTENCE
        # msg.sentence = sentence
        sentence = unicode(sentence, 'utf-8')
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

        self.publisher.publish(msg)

    def sendUserInputWating(self):
        msg = ui_msg()
        msg.reserved = 0
        msg.command = msg.UI_WAIT_USER_INPUT
        msg.sentence = ''

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


