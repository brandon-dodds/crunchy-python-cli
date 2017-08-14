#!/usr/bin/env python3
# Created on 04/08/2017. Version 0.0.2
from __future__ import unicode_literals

import getpass
import platform
import sys

import requests
from crunchyroll.apis.errors import ApiLoginFailure
from crunchyroll.apis.meta import MetaApi
from crunchyroll.apis.meta import ScraperApi

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
        quit()

    else:
        print("Your login succeeded.")


def print_user_queue():
    user_queue = crunchyroll_meta_api.list_queue()
    print("\nQueue Items:")
    user_queue_item_number = 1
    for user_queue_item in user_queue:
        print("{0}: {1}".format(user_queue_item_number, user_queue_item.name))
        user_queue_item_number += 1


def show_search(user_show_search_string):
    user_show_result = False
    user_show_search_output = crunchyroll_meta_api.search_anime_series(user_show_search_string)
    if len(user_show_search_output) == 0:
        print("The show you are looking for is unavailable, please try again.")
        main()

    print("Here are your search results: \n")
    for show_number in range(len(user_show_search_output)):
        print("[{0}]: ".format(show_number + 1) + user_show_search_output[show_number].name)

    user_search_show_select = input("Please enter the number of the show you are trying to watch: ")
    try:
        user_show_result = int(user_search_show_select)  # Asks the user to input the show number.

    except:
        print("Number entered or their is an error, please try again.")
        main()

    confirmation = input("Are you sure that {0} is the anime you want to watch?: ".format(
        user_show_search_output[user_show_result - 1].name)).lower()

    if confirmation == "yes":
        return user_show_search_output[user_show_result - 1]


def main():
    # Booleans
    login = False
    queue_argument = False

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
        login_to_crunchyroll(input_username, input_password)

        if queue_argument:
            print_user_queue()

    user_show_search = input("Search for a show: ")
    user_show_choice = show_search(user_show_search)


main()
