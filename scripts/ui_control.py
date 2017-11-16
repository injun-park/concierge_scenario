#!/usr/bin/python
#-*- coding: utf-8 -*-

import rospy
from concierge_msgs.msg import ui_msg


class UI_Control :
    def __init__(self):
        self.publisher = rospy.Publisher("/ui_control", ui_msg, queue_size=10)

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
        msg.reserved = 0
        msg.command = msg.UI_ROBOT_SENTENCE
        msg.sentence = sentence

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

if __name__ == "__main__" :
    rospy.init_node('ui_controll', anonymous=True)

    ui = UI_Control()
    rate = rospy.Rate(10)

    for i in range(20) :
        ui.sendRobotMsg("안녕하세요. 만나서 반갑습니다.")
        rate.sleep()


