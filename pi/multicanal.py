#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pygame
import socket
import struct
import sys

from signal import alarm, signal, SIGALRM, SIGKILL

def initPyGame():

  # this section is an unbelievable nasty hack - for some reason Pygame
  # needs a keyboardinterrupt to initialise in some limited circs (second time running)
  class Alarm(Exception):
      pass
  def alarm_handler(signum, frame):
      raise Alarm
  signal(SIGALRM, alarm_handler)
  alarm(3)
  try:
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    DISPLAYSURFACE = pygame.display.set_mode((10, 10)) 
    alarm(0)
  except Alarm:
    raise KeyboardInterrupt

def buttonPressed():
  message = str(soundId)
  print '  -- Sending "%s"' % message
  sent = sock.sendto(message, multicast_group)
  pygame.mixer.music.load('data/mp3/sound_'+str(soundId)+'.mp3')
  pygame.mixer.music.play()

def buttonInterrupt(channel):
  global soundId
  newSoundId = 0
  if channel == 4:
    newSoundId = 1
  elif channel == 17:
    newSoundId = 2
  elif channel == 27:
    newSoundId = 3
  elif channel == 22:  
    newSoundId = 4
  if newSoundId != soundId:
    soundId = newSoundId
    buttonPressed()

# INIT SOUND ENGINE
print '-- Initialising Sound Engine'
initPyGame()

print '-- Adding Sound Ended Event'
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

soundId = 0

# INIT UDP
print '-- Initialising UDP'
multicast_group = ('224.0.0.1', 55056)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# INIT GPIO
print '-- Initialising GPIO'
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

print '-- GPIO interrupts' 
GPIO.add_event_detect(4, GPIO.RISING, callback=buttonInterrupt, bouncetime=100)
GPIO.add_event_detect(17, GPIO.RISING, callback=buttonInterrupt, bouncetime=100)
GPIO.add_event_detect(27, GPIO.RISING, callback=buttonInterrupt, bouncetime=100)
GPIO.add_event_detect(22, GPIO.RISING, callback=buttonInterrupt, bouncetime=100)

print '-- Starting'
try:
  while True:
    time.sleep(1);
    for event in pygame.event.get():
      if event.type == SONG_END:
        print 'song ended'
        soundId = 0

finally:
  GPIO.cleanup()
  sock.close()