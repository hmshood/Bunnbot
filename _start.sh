#!/bin/bash
check=`ps -ef|grep Main.py\$`
if [ -n "$check" ]; then `nohup python3 Main.py >> logs.txt`; else echo "Script is already running." ; fi
sleep 1800