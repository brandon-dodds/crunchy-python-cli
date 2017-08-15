#!/usr/bin/env python3
# Created on 04/08/2017. Version 0.0.2
from __future__ import unicode_literals

import getpass
import platform
import sys

import requests
import youtube_dl
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


def episode_choice(user_show_choice_result, simulate_boolean):
    print("These are the list of episodes available to watch. \n")
    episodes_from_user_show = crunchyroll_meta_api.list_media(user_show_choice_result)
    amount_of_episodes = len(episodes_from_user_show)
    for x in episodes_from_user_show:
        print("[{0}] Episode {1}: {2}".format(amount_of_episodes, x.episode_number,
                                              x.name))  # Prints the available list of episodes.
        amount_of_episodes -= 1
    episode_id_input = input("Input the ID of the episode(s) that you would like to watch: ")
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
            print("Downloading multiple episodes.")
        if "-" or "," not in episode_id_input:
            selected_episode = episodes_from_user_show[len(episodes_from_user_show) - int(episode_id_input)]
            print("Downloading episode {0}".format(selected_episode.episode_number))
            episode_premium_only = not (bool(selected_episode.free_available))
            episode_media_id = selected_episode.media_id
            episode_url = selected_episode.url
        ydl_opts["playlist_items"] = episode_id_input
    the_url_for_the_show = user_show_choice_result.url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([the_url_for_the_show])


def main():
    # Booleans
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
    episode_choice(user_show_choice, simulate_download)


main()
