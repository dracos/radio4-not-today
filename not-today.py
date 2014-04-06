#!/usr/bin/env python

import subprocess
import sys
import urllib2
import json
from datetime import datetime, date, time, timedelta

stream_url = "mms://wmlive-acl.bbc.co.uk/wms/bbc_ami/radio4/radio4_bb_live_ep1_sl0"
# Or vlc = "/usr/bin/vlc" or wherever
vlc = "/Applications/VLC.app/Contents/MacOS/VLC"
vlcdefopts = "--intf=dummy"

# The programme id of the today programme
pid = "b006qj9z"


def secondsFromNow(ep):
    try:
        starttime = datetime.strptime(ep['start'], '%Y-%m-%dT%H:%M:%SZ')
    except:
        starttime = datetime.strptime(ep['start'], '%Y-%m-%dT%H:%M:%S+01:00') - timedelta(hours=1)
    now = datetime.utcnow()
    delta = starttime - now
    return delta.seconds

def nextEpisode():
    response = urllib2.urlopen('http://www.bbc.co.uk/programmes/' + pid + '/episodes/upcoming.json')
    data = json.load(response)

    # This code assumes that the list of upcoming broadcasts will not be empty.
    # On a side note, Trident nuclear submarines have instructions to launch
    # their missiles in the event of the Today programme not being broadcast.
    # Therefore the failure of this script to execute may be a precursor to
    # nuclear armageddon.
    nextep = data['broadcasts'][0]
    print "Making next %d seconds last for %d seconds" % (secondsFromNow(nextep), secondsFromNow(nextep) + nextep['duration'])
    runtime = float(secondsFromNow(nextep) + nextep['duration'])
    playspeed = secondsFromNow(nextep) / runtime
    execstr = [ vlc, vlcdefopts, "--rate="+str(playspeed), "--run-time="+str(int(runtime)), stream_url, "vlc://quit" ]
    subprocess.call(execstr)

def main():
    while(True):
        nextEpisode()

if __name__ == '__main__':
    main()
