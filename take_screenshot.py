"""
Main routine for No Mans Sky screenshot addres decoder
"""
import sys
import time
import logging
import pyautogui

#
#
pyautogui.FAILSAFE = True
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

_loc01_ = ( 10, 1015, 32, 32) # Location 0
_loc02_ = ( 43, 1015, 32, 32) # Location 1
_loc03_ = ( 75, 1015, 32, 32) # Location 2
_loc04_ = (107, 1015, 32, 32) # Location 3
_loc05_ = (139, 1015, 32, 32) # Location 4
_loc06_ = (171, 1015, 32, 32) # Location 5
_loc07_ = (203, 1015, 32, 32) # Location 6
_loc08_ = (235, 1015, 32, 32) # Location 7
_loc09_ = (267, 1015, 32, 32) # Location 8
_loc10_ = (299, 1015, 32, 32) # Location 9
_loc11_ = (331, 1015, 32, 32) # Location 10
_loc12_ = (363, 1015, 32, 32) # Location 11



def take_shot(_region_):

    pyautogui.screenshot(region=_region_, imageFilename='screenshot.png')   

    
def main():

    take_shot(_loc04_)

if __name__ == "__main__":
    main()
