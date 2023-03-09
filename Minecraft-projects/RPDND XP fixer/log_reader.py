#!/usr/bin/env python3
"""log_reader.py: A simple script to read the logs from a minecraft server and calculate the playtime of each player,
from which it calculates the XP they should have gotten. Outputs this both as a print and as a json file.
Written for Kyazi's RPDND server, but should work for any server that logs in the same format.
"""

__author__ = "DWJ Straat"
__license__ = "MIT"

from tkinter import filedialog as fd
import re
from datetime import datetime
import json
import gzip

config = json.load(open('config.json.example', 'r'))

def get_file():
    """
    Opens a file dialog and returns the selected file.
    :return: The selected file
    """
    return fd.askopenfilename()


def auto_read(file):
    """
    Reads a file, automatically detecting if it is gzipped or not, and outputs the contents.
    :param file: The path to the file to be read
    :return: The contents of the file
    """
    return read_gz(file) if file.endswith('.gz') else read_file(file)


def read_file(file):
    """
    Reads a file.
    :param file: The path to the file to be read
    :return: the contents of the file
    """
    with open(file, 'r') as f:
        return f.read()


def read_gz(file):
    """
    Reads a gzipped file.
    :param file: The path to the file to be read
    :return: the contents of the file
    """
    with gzip.open(file, 'rt') as f:
        return f.read()


def get_data(string):
    """
    Gets the timestamp and name from a line of the log.
    :param string: The line of the log
    :return: The timestamp and name
    """
    splitline = string.split()
    timestamp = datetime.strptime(splitline[0][1:-1], "%H:%M:%S")
    name = splitline[3]
    return timestamp, name


def get_login_logout(logs):
    """
    Gets the login and logout times of each player from the log.
    :param logs: The log to be read
    :return: A dictionary of login and logout times for each player
    """
    logdict = {}
    for line in logs.splitlines():
        if re.search(".*joined the game$", line):
            timestamp, name = get_data(line)
            log = {'in': timestamp}
        elif re.search(".*left the game$", line):
            timestamp, name = get_data(line)
            log = {'out': timestamp}
        else:
            continue
        if name not in logdict:
            logdict[name] = [log]
        else:
            logdict[name].append(log)
    return logdict


def calculate_time(logdict):
    """
    Calculates the total playtime of each player.
    :param logdict: The dictionary containing the login and logout times of each player
    :return: The total playtime of each player
    """
    for name in logdict:
        total = datetime.strptime('00:00:00', "%H:%M:%S")
        for log in logdict[name]:
            if 'in' in log:
                in_time = log['in']
            elif 'out' in log:
                out_time = log['out']
                total += out_time - in_time
        logdict[name] = total
    return logdict


def get_day(logdict, days_dict={}):
    """
    Calculates the number of days each player has played at least 1 hour.
    :param logdict: A dictionary containing the total playtime of each player
    :param days_dict: A dictionary containing the number of days each player has played at least 1 hour.
    An empty dictionary is used if none is provided.
    :return: A dictionary containing the number of days each player has played at least 1 hour
    """
    for name in logdict:
        for day in logdict[name]:
            if day > datetime.strptime('01:00:00', "%H:%M:%S"):
                if name in days_dict:
                    days_dict[name] += 1
                else:
                    days_dict[name] = 1
    return days_dict


def save_xp(xp_dict):
    """
    Saves the xp dictionary to a json file.
    :param xp_dict: A dictionary containing the xp of each player
    """
    with open('xp.json', 'w') as f:
        json.dump(xp_dict, f)


def get_exp(days_dict, xp_dict = {}, XP_PER_DAY=400):
    """
    Calculates the xp each player should have gotten.
    :param days_dict: a dictionary containing the number of days each player has played at least 1 hour
    :param xp_dict: a dictionary containing the xp of each player, an empty dictionary is used if none is provided
    :param XP_PER_DAY: the amount of xp each player should get per day, defaults to 400
    :return: the xp dictionary
    """
    for name in days_dict:
        if name in xp_dict:
            xp_dict[name] += days_dict[name] * XP_PER_DAY
        else:
            xp_dict[name] = days_dict[name] * XP_PER_DAY
    return xp_dict


def multi_reader(files=[]):
    """
    Reads multiple files and outputs amount of xp each player should have gotten.
    :param files: the files to be read, if none are provided a file dialog will open
    :return: a dictionary containing the xp of each player
    """
    if not files:
        files = fd.askopenfilenames()
    print(files)
    day_log = {}
    playtime_log = {}
    for file in files:
        logs = auto_read(file)
        date = file.split('/')[-1].split('.')[0].split('-')[:3]
        date = '-'.join(date)
        logdict = get_login_logout(logs)
        if date not in day_log:
            day_log[date] = [logdict]
        else:
            for name in logdict:
                if name in day_log[date]:
                    day_log[date][0][name].append(logdict[name])
                else:
                    day_log[date][0][name] = logdict[name]
    for day in day_log:
        playtime = calculate_time(day_log[day][0])
        for name in playtime:
            if name not in playtime_log:
                playtime_log[name] = [playtime[name]]
            else:
                playtime_log[name].append(playtime[name])
    days_dict = get_day(playtime_log)
    return get_exp(days_dict, XP_PER_DAY=config['xp_per_day'])


a = multi_reader()
print(a)
save_xp(a)
