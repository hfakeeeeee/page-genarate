#!/bin/bash

pid="$1"

kill $(ps -aux | grep -- "node_modules/.bin/vite --port $pid" | grep -v grep | awk '{print $2}')
