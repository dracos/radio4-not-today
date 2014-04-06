#!/usr/bin/env python

import sys
from datetime import datetime, date, time, timedelta
import os

stream_url = "mms://wmlive-acl.bbc.co.uk/wms/bbc_ami/radio4/radio4_bb_live_ep1_sl0"
vlc = "/usr/bin/vlc"
vlcdefopts = "--intf=dummy"

schedule = [
    # Monday to Friday
    { 'day':0, 'time':"06:00", 'duration':180 },
    { 'day':1, 'time':"06:00", 'duration':180 },
    { 'day':2, 'time':"06:00", 'duration':180 },
    { 'day':3, 'time':"06:00", 'duration':180 },
    { 'day':4, 'time':"06:00", 'duration':180 },
    # Saturday
    { 'day':5, 'time':"07:00", 'duration':120 },
]

def secondsFromNow(ep):
    now = datetime.now()
    daysfromnow = (ep['day'] - now.weekday()) % 7
    eptime = datetime.combine(now.date(), datetime.strptime(ep['time'], "%H:%M").time()) + timedelta(days=daysfromnow)
    secondsfromnow = (eptime - now).total_seconds()
    if (secondsfromnow < 0): # Today's episode already passed
        secondsfromnow = secondsfromnow + timedelta(weeks=1).total_seconds() 
    return secondsfromnow

def nextEpisode():
    nextep = schedule[0]
    for ep in schedule:
        if (secondsFromNow(ep) < secondsFromNow(nextep)):
            nextep = ep
    print "Making next %d seconds last for %d seconds" % (secondsFromNow(nextep), secondsFromNow(nextep) + (nextep['duration'] * 60))
    runtime = (secondsFromNow(nextep) + (nextep['duration'] * 60))
    playspeed = secondsFromNow(nextep) / runtime
    execstr = vlc + " " + vlcdefopts + " --rate="+str(playspeed) + " --run-time="+str(int(runtime)) + " " + stream_url + " vlc://quit"
    os.system(execstr)

def main():
    while(True):
        nextEpisode()

if __name__ == '__main__':
    main()
