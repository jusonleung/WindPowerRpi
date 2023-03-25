#!/bin/bash

# Connect to AstroRelay
nohup /home/PolyuWindPower/arc/arc  > arc.log 2>&1 &

#ps aux | grep arc
#sudo kill <PID>

#sudo crontab -e
#add line at the end
#@reboot /home/PolyuWindPower/connectTunnel.sh > /dev/null 2>&1