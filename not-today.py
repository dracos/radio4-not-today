#!/usr/bin/env python

import sys
from datetime import datetime, date, time, timedelta
import os

stream_url = "mms://wmlive-acl.bbc.co.uk/wms/bbc_ami/radio4/radio4_bb_live_ep1_sl0"
vlc = "/usr/bin/vlc"
vlcdefopts = "--intf=dummy"

schedule = [
    {'day':6, 'time':"19:02", 'duration':12.5}, # Sunday
    {'day':0, 'time':"14:02", 'duration':12.5}, # Monday repeat
    {'day':0, 'time':"19:02", 'duration':12.5}, # Monday
    {'day':1, 'time':"14:02", 'duration':12.5}, # Tuesday repeat
    {'day':1, 'time':"19:02", 'duration':12.5}, # Tuesday
    {'day':2, 'time':"14:02", 'duration':12.5}, # Wednesday repeat
    {'day':2, 'time':"19:02", 'duration':12.5}, # Wednesday
    {'day':3, 'time':"14:02", 'duration':12.5}, # Thursday repeat
    {'day':3, 'time':"19:02", 'duration':12.5}, # Thursday
    {'day':4, 'time':"14:02", 'duration':12.5}, # Friday repeat
    {'day':4, 'time':"19:02", 'duration':12.5}, # Friday
    {'day':6, 'time':"10:00", 'duration':75.0}  # Sunday bloody omnibus
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
