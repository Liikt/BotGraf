#!/bin/bash

cd /home/liikt/discord/

git checkout Ooyodo
PULL=`git pull`

if [[ ${PULL} != 'Already up-to-date.' ]]; then
    cd Ooyodo
    ./kill.sh || true
    ./daemonize
    echo -e '\nRestarted Ooyodo\n----------------------------------\n' >> log/ooyolog
    echo 'restarted'
fi
