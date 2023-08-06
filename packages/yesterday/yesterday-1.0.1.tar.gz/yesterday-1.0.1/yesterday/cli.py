import sys
import click
from yesterday import __version__ as VERSION
from yesterday.entries import *
from yesterday.Questionnaire import start_log
import pyfiglet
from yesterday.Pretty import Pretty
from datetime import datetime

__user__ = ""
key = ""

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("YESTERDAY", font='slant')
    print(ascii_banner)
    print(" === ======= ======= = ======= === ========= ========")
    print(" Quick Journals for Everyone ! ")
    print(" === ======= ======= = ======= === ========= ======== \n")


def register_new_user():
    print(Pretty.OKGREEN + 'Looks like you are a new user . Let\'s get you started !! \n ' + Pretty.ENDC)
    global __user__
    __user__ = click.prompt(Pretty.OKGREEN + "Please enter a user name  " + Pretty.ENDC)
    global key
    key = click.prompt(Pretty.OKGREEN + "Please enter a SECRET KEY  " + Pretty.ENDC)
    create_local_credentials(__user__, key)


def get_user_profile():
    # TODO
    __user__ = "Raiyan"


def start_log_session():
    pass


def get_file_name():
    now = datetime.now()
    timestamp = str(datetime.timestamp(now))+ '.json'
    return timestamp


@click.command()
@click.option('--version', is_flag=True, help="Gives the installed version of Today")
def main(version):
    print_banner()

    if version:
        print(VERSION)
        sys.exit()

    if check_if_user_exists():
        get_user_profile()
        print(Pretty.HEADER + 'Welcome back ' + __user__ + Pretty.ENDC)
        start_log()
    else:
        register_new_user()

        print(Pretty.OKBLUE + (
            ' \n Welcome to YESTERDAY {} , let\'s get started with your very first entry !! \n '.format(
                __user__)) + Pretty.ENDC)

        entries = start_log()

        timestamp_file_name = get_file_name()
        dump_json(timestamp_file_name, entries)
        encrypt_json(key, timestamp_file_name)
        delete_json(timestamp_file_name)
        print(Pretty.BOLD + Pretty.OKBLUE + "\n Entry Made !! Good Job !! \n" + Pretty.ENDC)


if __name__ == "__main__":
    main()
