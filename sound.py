#import pygame
#pygame.init

#sound = pygame.mixer.Sound('sounds/R2D2a.wav')
#sound.play()

#pygame.time.wait(int(sound.get_length()) * 1000)
###############################################################################
# speech-test.py
#
# Author: electronut.in
#
# Description:
#
# Testing Raspberry Pi audio using pyttsx - Python Cross-platform
# text-to-speech wrapper
#
# test run:
#
# python speech-test.py "hello there"
###############################################################################

import sys
import pyttsx

# main() function
def main():
  # use sys.argv if needed
  print 'running speech-test.py...'
  engine = pyttsx.init()
  str = "I speak. Therefore. I am.  "
  if len(sys.argv) > 1:
    str = sys.argv[1]
  engine.say(str)
  engine.startLoop()
  engine.end()
  print "After loop"

# call main
if __name__ == '__main__':
  main()
