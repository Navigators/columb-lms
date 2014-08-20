#!bin/bash

p=$PWD

touch $p/djangocron

touch $p/djangocron.log

echo "* * * * * python $p/manage.py mycommand > $p/djangocron.log 2>&1" > djangocron

crontab djangocron 

crontab -l
