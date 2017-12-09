#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import json

class AibrilIntent :
    def __init__(self) :
        self.intent = ""
        self.confidence = ""

    def __init__(self, intent, confidence) :
        self.intent = intent
        self.confidence = confidence


class AibrilResponse :
    def __init__(self):
        self.intents = []
        self.entities = []
        self.text = []
        self.context = ""
        self.input = ""

    @staticmethod
    def newInstance(aibrilResponse):
        instance = AibrilResponse()

        intents = aibrilResponse['intents']
        for intent in intents :
            aibrilIntent = AibrilIntent(intent['intent'], intent['confidence'])
            instance.intents.append(aibrilIntent)

        instance.entities = aibrilResponse['entities']
        instance.text = aibrilResponse['output']['text']
        instance.input = aibrilResponse['input']['text']
        instance.context = aibrilResponse['context']

        return instance