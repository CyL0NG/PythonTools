#! /usr/bin/python
# -*- coding: utf-8 -*-
import platform
import ctypes
class Console(object):

    def __init__(self):
        if platform.system() == "Windows":
            self.platform = "windows"
            self.color = {'danger': { 'color': 0x0c, 'symbol': '-'}, #red
                    'warning': { 'color': 0x0e, 'symbol': '-'}, #yellow
                    'success': { 'color': 0x0a, 'symbol': '+'}, #green
                    'info': {'color': 0x0f, 'symbol': '*'}  #white
                    }
            self.handler = ctypes.windll.kernel32.GetStdHandle(-11)
            self.process = self.printOnWindows
        else:
            self.color = {'danger': {'color': '\033[22;31m', 'symbol': '-'}, #red
                    'warning': {'color': '\033[01;33m', 'symbol': '-'}, #yellow
                    'success': {'color': '\033[22;32m', 'symbol': '+'}, #green
                    'info': {'color': '\033[01;37m', 'symbol': '*'}, #white
                    'default': {'color': '\033[0m', 'symbol': ''}#default
                    }
            self.process = self.printOnLinux
            
    def printOnWindows(self, msg, type):
        #set console color
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.handler, self.color[type]['color'])
        print '[%s] %s' % (self.color[type]['symbol'], msg)
        #reset color
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.handler, self.color['info']['color'])

    def printOnLinux(self, msg, type):
        print '[%s] %s%s%s' % (self.color[type]['symbol'], self.color[type]['color'], msg, self.color['default']['color'])

    def show(self, msg):
        self.process(msg, 'info')

    def showWarning(self, msg):
        self.process(msg, 'warning')

    def showDanger(self, msg):
        self.process(msg, 'danger')

    def showSuccess(self, msg):
        self.process(msg, 'success')
