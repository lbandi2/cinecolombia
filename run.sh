#!/bin/bash

mkdir -p logs
cd /home/sergio/scripts/cinecolombia/
find logs -type f -mtime +30 -delete
. ./env/bin/activate
/home/sergio/scripts/cinecolombia/env/bin/python3 /home/sergio/scripts/cinecolombia/main.py >> logs/cinecolombia-"`date +"%Y-%m-%d_%H.%M.%S"`".log 2>&1
deactivate

