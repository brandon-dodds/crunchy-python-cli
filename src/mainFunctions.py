#!/usr/bin/env python2
# Created on 04/08/2017.
from __future__ import unicode_literals, print_function
__version__ = "0.0.2"

import getpass
import platform
import sys

import requests
from youtube_dl import YoutubeDL as YouTubeDL
from crunchyroll.apis.errors import ApiLoginFailure
from crunchyroll.apis.meta import MetaApi, ScraperApi
from termcolor import colored as colorize

# this script should have a noninteractive mode (hint: you should separate talking to the user with the rest of the
# code) as well as a mode accepting pipes to be useful

# User's OS ("Windows" or "Linux")
user_operating_system = platform.system()

# API and Starting variables
commandline_arguments = sys.argv  # use the argparse library instead.
crunchyroll_meta_api = MetaApi()
crunchyroll_scraper_api = ScraperApi(connector=requests)


def fail(obj):
    print(colorize(str(obj), color="red"))
    quit(1)  # error code 1 signifies failure


def login_to_crunchyroll(crunchyroll_username, crunchyroll_password):
    try:
        crunchyroll_meta_api.login(username=crunchyroll_username, password=crunchyroll_password)
    except ApiLoginFailure:
        fail("Invalid Username/Password combination.")
    else:
        print("Login successful.")


def print_user_queue():
    user_queue = crunchyroll_meta_api.list_queue()
    print("\nQueue Items:")
    for user_queue_item_number, user_queue_item in enumerate(user_queue, start=1):
        print("{0}: {1}".format(user_queue_item_number, user_queue_item.name))


def show_search(user_show_search_string):
    user_show_search_output = crunchyroll_meta_api.search_anime_series(user_show_search_string)
    if len(user_show_search_output) == 0:
        print("That show was not found in crunchyroll's directory.")
        return show_search(user_show_search_string)

    # this could be improved using GNU less
    for show_number in range(len(user_show_search_output)):
        print("[{0}]: ".format(show_number + 1) + user_show_search_output[show_number].name)

    while True:
        user_search_show_select = input("Enter the ID of the show you wish to watch: ")
        try:
            user_show_result = int(user_search_show_select)  # Asks the user to input the show number.
        except ValueError:
            print("Please enter a number.")
        else:
            break

    confirmation = input("Are you sure? (y/n): ").lower()
    if confirmation.startswith('y'):  # do it unix style
        return user_show_search_output[user_show_result - 1]
    else:
        return show_search(user_show_search_string)


def episode_choice(user_show_choice_result, simulate_boolean):
    print("Choose episode: \n")
    episodes_from_user_show = crunchyroll_meta_api.list_media(user_show_choice_result)
    amount_of_episodes = len(episodes_from_user_show)
    for x in episodes_from_user_show:
        print("[{0}] Episode {1}: {2}".format(amount_of_episodes, x.episode_number,
                                              x.name))  # Prints the available list of episodes.
        amount_of_episodes -= 1
    episode_id_input = input(
        "Select episode(s) with ID: ")  # there are libraries out there that let the user scroll the menu.
    ydl_opts = {
        "simulate": simulate_boolean,
        "subtitlesformat": "ass",
        "subtitleslangs": ["enUS"],
        "writesubtitles": True,
        "call_home": False,
        "outtmpl": "%(season)s - Episode %(episode_number)s: %(episode)s.%(ext)s",
    }

    if episode_id_input == "":
        print("Downloading all episodes.")
    else:
        if "-" or "," in episode_id_input:
            print("Downloading multiple episodes...")
        if "-" or "," not in episode_id_input:
            selected_episode = episodes_from_user_show[len(episodes_from_user_show) - int(episode_id_input)]
            print("Downloading episode {0}...".format(selected_episode.episode_number))
        ydl_opts["playlist_items"] = episode_id_input
    the_url_for_the_show = user_show_choice_result.url
    with YouTubeDL(ydl_opts) as ydl:
        ydl.download([the_url_for_the_show])


def main():
    # Booleans
    # these should be scanned for in a configuration file, such as ~/.crunchycli.ini
    simulate_download = False
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
        else:
            fail("Unrecognised arguments, quitting.")

    if login:
        input_username = input("Please enter your username: ")
        input_password = getpass.getpass("Crunchyroll Password: ")
        login_to_crunchyroll(input_username, input_password)

        if queue_argument:
            print_user_queue()

    user_show_search = input("Search for a show: ")
    user_show_choice = show_search(user_show_search)
    episode_choice(user_show_choice, simulate_download)


main()
