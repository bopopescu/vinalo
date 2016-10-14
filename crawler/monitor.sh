#!/bin/bash
val=$(ps -fade | grep scra | grep -v grep | awk '{print $2}')
while [ "$val" -ge "0" ];
do
    sleep 1
    val=$(ps -fade | grep scra | grep -v grep | awk '{print $2}')
done

echo 'done'
sendmail darkangle0307@gmail.com  < /home/crawler/crawler/mail.txt