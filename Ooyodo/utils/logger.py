import os
from time import strftime, gmtime, sleep
from zipfile import ZipFile


LOGDIR = os.sep + os.path.join(*__file__.split(os.sep)[:-2], 'log')
LOGNAME = 'ooyolog'
LOGFILE = os.path.join(LOGDIR, LOGNAME)
semaphor_counter = 0
log_length = 500


def log(level, functionname, message):
    global semaphor_counter

    semaphor_counter += 1

    while semaphor_counter > 1:
        semaphor_counter -= 1
        sleep(0.5)
        semaphor_counter += 1

    with open(LOGFILE, 'a') as logfile:
        date = strftime('%d %b %Y %H:%M:%S', gmtime())
        line = '[{}]\t{} {}: {}'.format(level, date, functionname, message)
        logfile.write(line + '\n')

    with open(LOGFILE, 'r') as logfile:
        if len(logfile.readlines()) >= log_length:
            logrotate()

    semaphor_counter -= 1

def logrotate():
    all_zip = [file for file in os.listdir(LOGDIR) if 'zip' in file]
    last = max([int(file.split('.')[2]) for file in all_zip] + [0])

    os.chdir(LOGDIR)

    with ZipFile('.'.join([LOGNAME, 'zip', str(last+1)]), 'x') as zippedlog:
        zippedlog.write(LOGNAME)

    os.chdir(os.sep + os.path.join(*__file__.split(os.sep)[:-1]))

    open(LOGFILE, 'w').close()
