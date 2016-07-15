#!/bin/bash

# Kill processes from nodes
for line in `cat /opt/hadoop-2.6.0/etc/hadoop/nodes2`;do
  if [[ $line =~ ^\# ]]; then
    continue
  fi
  echo $line
  scp -r /opt/hadoop-2.6.0/ $line:/opt/
done

