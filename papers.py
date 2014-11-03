#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Curtis and Dimitar'
__email__ = "curtis.mccordW@utoronto.ca"

__copyright__ = "Whatever"
__license__ = "Whatever"

__status__ = "Working on it"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open("countries.json", 'r') as countries_reader, open('watchlist.json', 'r') as watchlist_reader, \
            open('example_entries','r') as entries_reader:
        countries_contents = countries_reader.read()
        countries_json = json.loads(countries_contents)
        watchlist_contents = watchlist_reader.read()
        watchlist_json = json.loads(watchlist_contents)
        entries_contents = entries_reader.read()
        entries_json = json.loads(entries_contents)
    if check_quarantine(countries_json, entries_json) is False:
        return ["Quarantine"]
    elif check_valid_visa(countries_json, entries_json) is False:
        return ["Reject"]
    elif check_watchlist(watchlist_json, entries_json) is False:
        return ["Detain for Secondary Processing"]
    elif check_from_kanadia(entries_json) is True:
        return ["Accept. Welcome home, citizen."]
    else:
        return ["Accept."]


def check_quarantine(countries_list, persons_list):
    """
    Checks the passport "from" and "home" keys against the medical advisory list.

    :param countries_list: The name of a JSON formatted file with the medical advisories under key "medical_advisory"
    :param persons_list: The name of a JSON formatted file with person's "from" and "home" keys
    :return: a Boolean which is True when there is no quarantine and False when the subject must be quarantined
    """
    # if

def check_valid_visa(countries_list, persons_list):
    """
    Checks the entries agaist
    :param countries_list:
    :param persons_list:
    :return:
    """


def check_watchlist(watchlist, persons_list):
    """
    Checks the passport number and name of persons against the watchlist.

    :param watchlist: The name of a JSON formatted files with names and passport numbers for 'Secondary Processing'
    :param persons_list: The name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: a Bool which is True when someone is not on the watchlist and False when they must be detained.
    """

def check_from_kanadia(persons_list):
    """
    Checks whether a person is from Kanadia, and if they meet the other requirements, admits them home
    :param persons_list: the name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: A bool which is True if person is from Kanadia, False otherwise
    """

def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

