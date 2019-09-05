#!/bin/bash
while true; do
    python3 bash.py
    curl -i -XPOST "http://xxx.xxx.xxx.xxx:8086/write?db=mydb" --data-binary @data.txt
    sleep 5s
done
