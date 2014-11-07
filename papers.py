#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Curtis and Dimitar'
__email__ = "curtis.mccord@utoronto.ca"

__copyright__ = "Whatever"
__license__ = "Whatever"

__status__ = "Working on it"

# imports one per line
import re
import datetime
import json

#We need to make sure that Python doesn't get confused about the cases of its entries!!

key_category_list = ['']  # here we put the different keys that we compare in our check functions
decision_value_list = ['']
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

    try:
        with open(countries_file, 'r') as countries_reader, open(watchlist_file, 'r') as watchlist_reader, \
            open(input_file, 'r') as entries_reader:  # opens all of the necessary files
            countries_contents = countries_reader.read()
            countries_json = json.loads(countries_contents)
            watchlist_contents = watchlist_reader.read()
            watchlist_json = json.loads(watchlist_contents)
            entries_contents = entries_reader.read()
            entries_json = json.loads(entries_contents)
    except FileNotFoundError:
        raise FileNotFoundError

    list_of_checked_entrants = []

    for entrant in entries_json:
        valid_date_format(entrant)


        # if check_quarantine(countries_json, entries_json) is False:  # first priority check
            # decision_value_list.append('Quarantine')
            # continue
            #return ["Quarantine"]
        # elif check_valid_visa(countries_json, entries_json) is False:  # second priority check
            #return ["Reject"]

        if check_watchlist(watchlist_json, entrant) == "Secondary":
            list_of_checked_entrants.append("Secondary")
        elif check_watchlist(watchlist_json, entrant) == "Accept":
            list_of_checked_entrants.append("Accept")



        #if check_from_kan(entrant) is True: #fourth priority check
            #return ["Accept. Welcome home, citizen."]
        #else:
            #print('Accept')

    # print(list_of_checked_entrants)


def check_quarantine(countries_json, entrant):
    """
    Checks the passport "from" and "home" keys against the medical advisory list.

    :param countries_list: The name of a JSON formatted file with the medical advisories under key "medical_advisory"
    :param entrant: The name of a JSON formatted file with person's "from" and "home" keys
    :return: a Boolean which is True when there is no quarantine and False when the subject must be quarantined
    """
    for country in countries_json:
        if country['medical_advisory'] != "" and \
            entrant['country']['from'].upper() == country['code'] or \
            entrant['country']['via'].upper() == country['code']:
            return 'Quarantine'
        else:
            return 'Accept'



def check_valid_visa(countries_list, entrant):
    """
    Checks the entries agaist
    :param countries_list:
    :param entrant:
    :return:
    """


def check_watchlist(watchlist, entrant):
    """
    Checks the passport number and name of entrant against the watchlist by iterating over the entries file and
    comparing them with the watchlist files

    :param watchlist: The name of a JSON formatted files with names and passport numbers for 'Secondary Processing'
    :param entrant: The name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: a Bool which is True when someone is not on the watchlist and False when they must be detained.
    """

    for suspect in watchlist:

        if entrant["passport"].upper() == suspect["passport"].upper():
            return "Secondary"
        elif entrant['first_name'].upper() == suspect['first_name'].upper() and \
                suspect['last_name'].upper() == entrant['last_name'].upper():
            return "Secondary"
        else:
            return "Accept"


def check_from_kan(entrant):
    """
    Checks whether a person is from Kanadia, and if they meet the other requirements, admits them home
    :param entrant: the name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: A bool which is True if person is from Kanadia, False otherwise
    """
    for citizen in entrant:
        if citizen['from']['country'].upper == "KAN" and \
            entrant['entry_reason'] == 'returning':
            return 'Accept'

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


def valid_date_format(entrant):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """

    for word in entrant:
        if word == "visa":
            try:
                datetime.datetime.strptime(entrant[word]['date'], '%Y-%m-%d')
                return True
            except ValueError:
                raise ValueError



decide("test_date_format.json", "watchlist.json", "countries.json")