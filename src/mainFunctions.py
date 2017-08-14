#!/usr/bin/env python3
# Created on 04/08/2017. Version 0.0.2
from __future__ import unicode_literals

import getpass
import platform
import sys
import requests
from crunchyroll.apis.meta import MetaApi
from crunchyroll.apis.meta import ScraperApi
from crunchyroll.apis.errors import ApiLoginFailure

# User's OS ("Windows" or "Linux")
user_operating_system = platform.system()

# API and Starting variables
commandline_arguments = sys.argv
crunchyroll_meta_api = MetaApi()
crunchyroll_scraper_api = ScraperApi(connector=requests)


def login_to_crunchyroll(crunchyroll_username, crunchyroll_password):
    try:
        crunchyroll_meta_api.login(username=crunchyroll_username, password=crunchyroll_password)
    except ApiLoginFailure:
        print("Your login failed, please try again.")
        main()
    else:
        print("Your login succeeded.")
        return True


def print_user_queue():
    user_queue = crunchyroll_meta_api.list_queue()
    print("\nQueue Items:")
    user_queue_item_number = 1
    for user_queue_item in user_queue:
        print("{0}: {1}".format(user_queue_item_number, user_queue_item.name))
        user_queue_item_number += 1


def main():
    # Booleans
    login = False
    queue_argument = False
    was_login_successful = False

    for arguments in commandline_arguments[1:]:
        if arguments == "--simulate":
            simulate_download = True
        elif arguments == "--auth":
            login = True
        elif arguments == "--queue":
            login = True
            queue_argument = True
        # list_queue
        else:
            print("Unrecognised arguments, quitting.")
            quit()

    if login:
        input_username = input("Please enter your username: ")
        input_password = getpass.getpass("Crunchyroll Password: ")
        was_login_successful = login_to_crunchyroll(input_username, input_password)

        if queue_argument:

            if was_login_successful:
                print_user_queue()


main()
