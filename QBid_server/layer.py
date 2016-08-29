# -*- coding: utf-8 -*-
import os
import time

from django.core.wsgi import get_wsgi_application
from yowsup.common.tools                               import Jid                               #is writing, writing pause
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
from api.models import Team, Match, Player

#Log, but only creates the file and writes only if you kill by hand from the console (CTRL + C)
#import sys
#class Logger(object):
#    def __init__(self, filename="Default.log"):
#        self.terminal = sys.stdout
#        self.log = open(filename, "a")
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message)
#sys.stdout = Logger("/1.txt")
#print "Hello world !" # this is should be saved in yourlogfilename.txt
#------------#------------#------------#------------#------------#------------


name = "NAMEPRESENCE"
filelog = "/root/.yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(2)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(3)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody().lower()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity

        #For a break to use the character \n
        #The sleep you write so #time.sleep(1)

        if True:
            if message == 'qpl hi':
                answer = "Hi "+namemitt+" " 
                self.toLower(textmsg(answer, to = recipient ))
                print answer
            elif message == 'qpl developer':
                answer = "QPL Developers \n***************\n Thamshid (Backend) \n Vikas (Frontend) \n Vysagh (Designer)"
                self.toLower(textmsg(answer, to=recipient))
                print answer
            elif message == 'qpl help':
                answer = "QPL Help \n***************\n QPL HI\n QPL HELP \n QPL DEVELOPER\n QPL POINT\n QPL FIXTURE\n QPL TOPPERS"
                self.toLower(textmsg(answer, to=recipient))
                print answer
            elif message == 'qpl point':
                answer = "QPL Point Table\n******************\n"
                teams = Team.objects.all().order_by('-point', '-goal_fo', 'goal_against', 'game_played')
                for team in teams:
                    answer += team.name + '\nGP: ' + \
                              str(team.game_played) + '\n W: ' + str(team.win) +\
                              '\nL: ' + str(team.lost) + '\nD: ' + str(team.draw) + \
                              '\nGF: ' + str(team.goal_fo) + '\nGA: ' + str(team.goal_against) +\
                              "\nP: " + str(team.point) + '\n=================\n'
                self.toLower(textmsg(answer, to=recipient))
                print answer
            elif message == 'qpl fixture':
                answer = "QPL Fixture\n****************\n"
                matches = Match.objects.all().order_by('-date')
                for match in matches:
                    answer += str(match.date) + " " + str(match) + "\n"
                self.toLower(textmsg(answer, to=recipient))
                print answer
            elif message == 'qpl toppers':
                answer = "QPL Toppers\n*****************\n"
                players = Player.objects.filter(no_of_goals__gt=0).order_by('-no_of_goals')
                for player in players:
                    answer += str(player.name) + "   " + str(player.no_of_goals) + "\n"
                self.toLower(textmsg(answer, to=recipient))
                print answer


