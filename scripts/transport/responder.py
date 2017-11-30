#!/usr/bin/python
#-*- coding: utf-8 -*-
import json
from jinja2 import  Environment, select_autoescape, FileSystemLoader
from TTS import TTS
class Responder :
    def __init__(self):
        self.tts = TTS()

        path = "/home/ijpark/catkin_ws/src/concierge/concierge_scenario/ui/html"
        self.env = Environment(
            loader=FileSystemLoader(path),
            autoescape=select_autoescape(['html', 'xml'])
        )


    def responseTTS(self, text):
        self.tts.speak(text)

    def respondeUserSpeech(self, text):
        pass

    def respondAibril(self, aibrilResult):
        '''
        :param aibrilResult:

         {
  "entities": [
    {
      "confidence": 1,
      "location": [
        0,
        6
      ],
      "value": "학과사무실",
      "entity": "office"
    }
  ],
  "intents": [
    {
      "confidence": 0.7479507446289062,
      "intent": "bring_me"
    }
  ],
  "output": {
    "text": [
      "요청하신 장소로 이동 할까요?"
    ],
    "log_messages": [],
    "nodes_visited": [
      "node_9_1510031424884"
    ]
  },
  "context": {
    "conversation_id": "98ed3153-cbe8-4af3-8d71-1e24d11353b9",
    "system": {
      "dialog_turn_counter": 3,
      "dialog_stack": [
        {
          "dialog_node": "node_9_1510031424884"
        }
      ],
      "_node_output_map": {
        "node_5_1510029965963": [
          0
        ],
        "node_9_1510031424884": [
          0
        ],
        "node_1_1510029708308": [
          0
        ]
      },
      "dialog_request_counter": 3
    }
  },
  "input": {
    "text": "학과 사무실로 안내해 주세요"
  }
}

        :return:
        '''

        context = {}
        template = self.env.get_template("robot_saying.html")
        merged = template.render(context)