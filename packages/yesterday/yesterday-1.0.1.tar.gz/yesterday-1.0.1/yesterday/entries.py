import pyAesCrypt
import os
import json

from yesterday.Pretty import Pretty

bufferSize = 64 * 1024


def path_to_yesterday():
    home = os.path.expanduser('~')
    if not os.path.exists(home+'/yesterday'):
        os.mkdir(home+'/yesterday')
    return home + '/yesterday/'


def print_errors(message):
    print(Pretty.FAIL + message + Pretty.ENDC)


def check_if_user_exists():
    if os.path.isfile(path_to_yesterday() + "creds.json.aes"):
        return True
    else:
        return False

def delete_json(file_name):
    if os.path.isfile(path_to_yesterday() + file_name):
        os.remove(path_to_yesterday() + file_name)

def dump_json(file_name, json_data):
    try:
        if not os.path.exists(path_to_yesterday()+file_name):
            with open(path_to_yesterday() + file_name, 'w+') as outfile:
                json.dump(json_data, outfile)
    except IOError as io_exception:
        print_errors('Could not create ' + file_name + ' on disk , please raise this issue on the repository')
        raise IOError(str(io_exception))


def create_local_credentials(user, key):
    creds = {'user': []}
    creds['user'].append({
        'username': user,
        'key': key
    })
    dump_json('creds.json', creds)
    encrypt_json(key, 'creds.json')
    delete_json('creds.json')


def encrypt_json(key, filename):
    try:
        pyAesCrypt.encryptFile(path_to_yesterday() + filename, path_to_yesterday() + filename + '.aes', key,
                               bufferSize)
    except ValueError as value_exception:
        print_errors('Error on encryption, please raise this issue on the repository')
        raise ValueError(str(value_exception))


def read_and_decrypt(self, key, filename):
    try:
        pyAesCrypt.decryptFile(path_to_yesterday() + filename + '.aes', path_to_yesterday() + filename, key,
                               bufferSize)
    except ValueError as value_exception:
        print_errors('Could not decrypt, please raise this issue on the repository')
        raise ValueError(str(value_exception))
