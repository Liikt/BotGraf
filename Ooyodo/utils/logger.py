import os
from time import strftime, gmtime, sleep
from zipfile import ZipFile


# Global vars
LOGDIR = os.sep + os.path.join(*__file__.split(os.sep)[:-2], 'log')
LOGNAME = 'ooyolog'
LOGFILE = os.path.join(LOGDIR, LOGNAME)
semaphor_counter = 0
log_length = 500

"""
log is a function the writes a log message into a log file.

It takes a log level, the name of the function that the log has to write for and the message itself

return nothing
"""
def log(level, functionname, message):
    global semaphor_counter

    # Increase the counter because a function wants to write into the log
    semaphor_counter += 1

    # Check if a function is writing into the log already
    while semaphor_counter > 1:
        # If the log is in use currently decrease the counter again and wait
        semaphor_counter -= 1
        sleep(0.5)
        # Increase the counter again and check again
        semaphor_counter += 1

    # Open the logfile in append mode to either create a new file or append at the end
    with open(LOGFILE, 'a') as logfile:
        # Get the current date and time
        date = strftime('%d %b %Y %H:%M:%S', gmtime())
        # Format the line for the log: [level] date function: message
        line = '[{}]\t{} {}: {}'.format(level, date, functionname, message)
        # Write to the logfile
        logfile.write(line + '\n')

    # Open the logfile in read mode to count lines
    with open(LOGFILE, 'r') as logfile:
        # Check if a logrotate is necessary
        if len(logfile.readlines()) >= log_length:
            # If so logrotate
            logrotate()

    # Decrease the counter again because the log is not used anymore
    semaphor_counter -= 1


"""
logrotate is a function that takes the old log, zips it and clears the plaintext version. Every zip
ends with a number. The lower the number the older the logs.

It takes nothing as an argument

returns nothing
"""
def logrotate():
    # Find all files that contain 'zip' in there name in the logdir
    all_zip = [file for file in os.listdir(LOGDIR) if 'zip' in file]
    # Find the highest number of those logs
    last = max([int(file.split('.')[2]) for file in all_zip] + [0])

    # Change directories into the logdir because zipfile actually zips the entire path to the file
    os.chdir(LOGDIR)

    # Open the zipfile in x mode -> throw an error if the zip already exists
    with ZipFile('.'.join([LOGNAME, 'zip', str(last+1)]), 'x') as zippedlog:
        # Zip the old logfile
        zippedlog.write(LOGNAME)

    # Change directories back
    os.chdir(os.sep + os.path.join(*__file__.split(os.sep)[:-1]))
    # Clear the logfile
    open(LOGFILE, 'w').close()
