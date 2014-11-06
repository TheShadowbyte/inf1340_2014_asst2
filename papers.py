#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Curtis and Dimitar'
__email__ = "curtis.mccordW@utoronto.ca and jordanov@mail.utoronto.ca"

__copyright__ = "Whatever"
__license__ = "MIT License"

__status__ = "Working on it"

# imports one per line
import re
import datetime
import json

#We need to make sure that Python doesn't get confused about the cases of its entries!!

key_category_list = ['']  # here we put the different keys that we compare in our check functions
# we may need other lists


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
            open('example_entries.json', 'r') as entries_reader:  # opens all of the necessary files
        countries_contents = countries_reader.read()
        countries_json = json.loads(countries_contents)
        watchlist_contents = watchlist_reader.read()
        watchlist_json = json.loads(watchlist_contents)
        entries_contents = entries_reader.read()
        entries_json = json.loads(entries_contents)
    # if check_quarantine(countries_json, entries_json) is False:  # first priority check
        #return ["Quarantine"]
    # elif check_valid_visa(countries_json, entries_json) is False:  # second priority check
        #return ["Reject"]
    #if check_watchlist(watchlist_json, entries_json) is False:  # third priority check
        # return ["Detain for Secondary Processing"]
    if check_from_kan(entries_json) is True:  # fourth priority check
        return ["Accept. Welcome home, citizen."]
    # else:
        # print(["Accept"])


def check_quarantine(countries_list, persons_list):
    """
    Checks the passport "from" and "home" keys against the medical advisory list.

    :param countries_list: The name of a JSON formatted file with the medical advisories under key "medical_advisory"
    :param persons_list: The name of a JSON formatted file with person's "from" and "home" keys
    :return: a Boolean which is True when there is no quarantine and False when the subject must be quarantined
    """


def check_valid_visa(countries_list, persons_list):
    """
    Checks the entries agaist
    :param countries_list:
    :param persons_list:
    :return:
    """


def check_watchlist(watchlist, persons_list):
    """
    Checks the passport number and name of persons against the watchlist by iterating over the entries file and
    comparing them with the watchlist files

    :param watchlist: The name of a JSON formatted files with names and passport numbers for 'Secondary Processing'
    :param persons_list: The name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: a Bool which is True when someone is not on the watchlist and False when they must be detained.
    """
    for entrant in persons_list:
        for suspect in watchlist:
            if entrant["passport"].upper() == suspect['passport'].upper() or \
                entrant['first_name'] == suspect['first_name'] and suspect['last_name'] == entrant['last_name']:
                print(entrant["passport"].upper(), entrant['first_name'], entrant['last_name'], ["Secondary"])


def check_from_kan(persons_list):
    """
    Checks whether a person is from Kanadia, and if they meet the other requirements, admits them home
    :param persons_list: the name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: A bool which is True if person is from Kanadia, False otherwise
    """
    for citizen in persons_list:
        if citizen['from']['country'].upper == "KAN":
            print(citizen["first_name"], citizen['last_name'], ["Accept"])


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
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


decide("test_returning_citizen.json", "watchlist.json", "countries.json")