#!/bin/bash

# Start the FastAPI
cd /home/PolyuWindPower/Python_code/Done
nohup uvicorn main:app --host 127.0.0.1 --port 8000 > fastapi.log 2>&1 &

#ps aux | grep uvicorn
#sudo kill <PID>