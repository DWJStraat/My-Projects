from tkinter import filedialog as fd
import re
import requests
import json


def read_file(file=None):
    """
    Reads a file.
    :param file: The path to the file to be read
    :return: the contents of the file
    """
    if file is None:
        file = fd.askopenfilename()
    with open(file, 'r') as f:
        return f.read()


def get_messages(logs):
    """
    Gets the messages from the log.
    :param logs: The log
    :return: A list of messages
    """
    message_list = {}
    header = re.findall(r'Migration Form Request!.*', logs)
    UUID = re.findall(r'- UUID:.*', logs)
    EXP = re.findall(r'- EXP:.*', logs)
    print(len(UUID))
    for id in range(len(UUID)):
        if re.match(r'Migration Form Request! .Accepted by .*', header[id]):
            UUID[id] = UUID[id].split(': ')[1]
            username = get_user(UUID[id])
            EXP[id] = int(EXP[id].split(': ')[1])
            message_list[username] = EXP[id]
    return message_list


def get_user(uuid):
    uuid = uuid.replace('-', '')
    r = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')

    return r.json()['name']


def save_json(data, file=None):
    """
    Saves data to a JSON file.
    :param data: The data to be saved
    :param file: The path to the file to be saved
    :return: None
    """
    if file is None:
        file = fd.asksaveasfilename()
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


a = read_file()
b = get_messages(a)
save_json(b, file=r'.\migration_log.json')
