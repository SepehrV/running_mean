#!/bin/sh
#starting the redis server
./usr/bin/redis-server --protected-mode no &


cd /code;
#starting a couple of workers
python3 worker.py &
python3 worker.py &

#starting the webserver
python3 entry.py 
