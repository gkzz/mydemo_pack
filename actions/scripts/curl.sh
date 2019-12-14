#!/bin/bash

status=$(curl -I http://${HOST_IP} | grep -E "^HTTP/1.1 200 OK" | awk '{print $2}')
test=$(echo ${status:="unknown"})

if [ $test = "200" ]; then
  exit 0
elif [ $test = "unknown" ]; then
  echo "unknown"
  exit 201
else
  echo "status: $test"
fi

exit 1
