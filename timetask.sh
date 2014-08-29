#!bin/bash

p=$PWD

touch $p/djangocron

touch $p/djangocron.log

echo "0 0 * * * python $p/manage.py mycommand > $p/djangocron.log 2>&1" > djangocron

crontab djangocron 

crontab -l
