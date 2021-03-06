#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Curtis and Dimitar'
__email__ = "curtis.mccord@utoronto.ca and jordanov@mail.utoronto.ca"

__copyright__ = "2014 Curtis McCord and Dimitar Jordanov"
__license__ = "MIT Licence"

__status__ = "Right about done"

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

    try:
        with open(countries_file, 'r') as countries_reader, open(watchlist_file, 'r') as watchlist_reader, \
                open(input_file, 'r') as entries_reader:  # opens all of the necessary files
            countries_contents = countries_reader.read()
            countries_json = json.loads(countries_contents)
            watchlist_contents = watchlist_reader.read()
            watchlist_json = json.loads(watchlist_contents)
            entries_contents = entries_reader.read()
            entries_json = json.loads(entries_contents)
    except:
        raise FileNotFoundError

    list_of_checked_entrants = []
    # runs each person through the required immigration checks
    for entrant in entries_json:
        #checks if entrant should be quarantined... safety first!
        if send_to_quarantine(countries_json, entrant):
            list_of_checked_entrants.append("Quarantine")
            continue
        # checks if all required keys are present
        if check_req_keys(entrant) is False:
            list_of_checked_entrants.append("Reject")
            continue
        # checks for a valid visitors visa if needed
        if reason(entrant) == "Visit" and \
                check_valid_visa(entrant) is False and \
                visa_required(countries_json, entrant) is True:
            list_of_checked_entrants.append("Reject")
            continue
        # checks for a valid transit visa
        if reason(entrant) == "Transit" and \
                visa_required(countries_json, entrant) is True and \
                check_valid_visa(entrant) is False:
            list_of_checked_entrants.append("Reject")
            continue
        # checks passport and visa formats are genuine
        if valid_passport_format(entrant) is False or \
                valid_visa_format(entrant) is False:
            list_of_checked_entrants.append("Reject")
            continue
        # checks if entrant is an international criminal
        if check_watchlist(watchlist_json, entrant):
            list_of_checked_entrants.append("Secondary")
            continue
        # checks if entrants are from Kanadia
        if check_from_kan(entrant):
            list_of_checked_entrants.append("Accept")
            continue
        # lets everyone who passes above checks into Kanadia
        else:
            list_of_checked_entrants.append("Accept")

    return list_of_checked_entrants


def send_to_quarantine(countries_json, entrant):
    """
    Checks the passport "from" and "via" keys against the medical advisory list.

    :param countries_json: The name of a JSON formatted file with the medical advisories under key "medical_advisory"
    :param entrant: The name of a JSON formatted file with person's "from" and "via" keys
    :return: a Boolean which is True when the subject must be quarantined and False otherwise
    """
    list_of_countries_with_medical_advisory = []
    # loops through the countries and appends those with medical advisories
    for country in countries_json:
        if countries_json[country]['medical_advisory'] != "":
            list_of_countries_with_medical_advisory.append(country)
    # checks the list of quarantined countries against the entrants 'from' and 'via' countries
    if 'from' in entrant and entrant['from']['country'] in list_of_countries_with_medical_advisory:
        return True
    elif 'via' in entrant and entrant['via']['country'] in list_of_countries_with_medical_advisory:
        return True
    else:
        return False


def check_valid_visa(entrant):
    """
    Checks the entries if the keyword visa exists and then checks if they have a containing word date.
    Dates that are more than 2 years older than the current date are invalid.
    (dict) -> Bool
    :param entrant: The name of a JSON formatted file with person's "from" and "via" keys
    :return: a Boolean which is True when the visa is valid and False otherwise
    """
    # sets the variable to two years before current date
    visa_oldest_date = datetime.datetime.now() - datetime.timedelta(days=730)
    # checks if entrants have a visa, returning false if visa is missing or expired
    if 'visa' in entrant:
        if entrant['visa']['date'] > str(visa_oldest_date):
            return True
        else:
            return False
    else:
        return False


def check_watchlist(watchlist, entrant):
    """
    Checks the passport number and name of entrant against the watchlist by iterating over the entries file and
    comparing them with the watchlist files
    (dict, dict) -> Bool
    :param watchlist: The name of a JSON formatted files with names and passport numbers for 'Secondary Processing'
    :param entrant: The name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: a Bool which is True when someone is not on the watchlist and False when they must be detained.
    """
    # iterates over the names and passport numbers on the watchlist and compares to corresponding entrant information
    for suspect in watchlist:
        if entrant["passport"].upper() == suspect["passport"].upper():
            return True
        elif entrant['first_name'].upper() == suspect['first_name'].upper() and \
                suspect['last_name'].upper() == entrant['last_name'].upper():
            return True
    return False


def check_from_kan(entrant):
    """
    Checks whether a person is from Kanadia, and if they meet the other requirements, appends "Accept"
    (dict) -> Bool
    :param entrant: the name of a JSON formatted file with the names and passports of people entering Kanadia
    :return: A bool which is True if person is from Kanadia, False otherwise
    """
    if entrant['home']['country'].upper() == "KAN" and entrant['entry_reason'].upper() == 'RETURNING':
        return True
    else:
        return False


def valid_passport_format(entrant):
    """
    (dict) -> Bool
    Checks whether a passport number is five sets of five alpha-numeric characters separated by dashes.
    Rejects all whose passports do not conform to the general regular expression.
    :param passport_number: alpha-numeric string
    :return: Boolean True if the format is valid, False otherwise
    """
    # sets the general regular expression and matches to entrant passport
    if re.match('^.{5}-.{5}-.{5}-.{5}-.{5}$', entrant['passport']) is not None:
        return True
    else:
        return False


def valid_visa_format(entrant):
    """
    (Dict) -> Bool
    Checks that the Visa for an entrant is in the correct alpha-numeric format
    Returns False for non-conforming documents
    :param entrant: individual entrant's JSON fetched from for loop in decide()
    :return: Boolean True if the format is valid, False otherwise
    """
    # looks for visas in entrant file and checks the correspondence to the regular general expression
    for word in entrant:
        if word == "visa":
            if re.match('^.{5}-.{5}$', entrant['visa']['code']) is not None:
                return True
            else:
                return False


def valid_date_format(entrant):
    """
    (dict) -> Bool
    Checks whether a date has the format YYYY-mm-dd in numbers, and returns false for non-conforming dates
    :param entrant: individual entrant's JSON fetched from for loop in decide()
    :return: Boolean True if the format is valid, False otherwise
    """
    # looks through the entrants files for visas
    for word in entrant:
        if word == "visa":
            # The first regular expression in the following conditional conjunction checks if the provided date is
            # correct length (YYYY-MM-DD), whereas the second regular expression checks if the values are integers.
            if re.match('^.{4}-.{2}-.{2}$', entrant[word]['date']) is not None and \
                    re.match('^-?[0-9]+-?[0-9]+-?[0-9]+$', entrant[word]['date']) is not None:
                return True
            else:
                return False


def visa_required(countries, entrant):
    """
    (dict, dict) -> Bool
    Checks whether the country requires a visa or not, returning True if visa is required,
    and False otherwise
    :param countries: the JSON that knows if a visa is needed for an entrant
    :param entrant: individual entrant's dictionary fetched from for loop in decide()
    :return: Boolean True if a visit or transit visa is required and False if it is not required.
    """
    # creates two lists for two types of visas
    list_of_countries_requiring_visitor_visas = []
    list_of_countries_requiring_transit_visas = []
    # populates above lists based on visa requirements
    for country in countries:
        if countries[country]['visitor_visa_required'] == "1":
            list_of_countries_requiring_visitor_visas.append(country)
        elif countries[country]['transit_visa_required'] == "1":
            list_of_countries_requiring_transit_visas.append(country)
    # checks if entrants 'via' and 'from' countries require visas
    if entrant['from']['country'] in list_of_countries_requiring_visitor_visas:
            return True
    elif 'via' in entrant and entrant['via']['country'] in list_of_countries_requiring_transit_visas:
            return True
    else:
        return False


def reason(entrant):
    """
    (dict) -> str
    Checks the entrant's motive for travelling, to determine what checks need to be implemented.
    :param: entrant: individual entrant's dictionary fetched from for loop in decide()
    :return: a string to be passed to other functions in decide()
    """
    if entrant['entry_reason'] == "visit":
        return "Visit"
    elif entrant['entry_reason'] == "transit":
        return "Transit"
    elif entrant['entry_reason'] == "returning":
        return "Returning"


def check_req_keys(entrant):
    """
   (dict key) -> Bool
   Looks through the entrants keys to see if they are all present,
   then checks to make sure they all have populated values.
   :param entrant: The dictionary of entrants to be looped over
   :return: Returns a Bool that is False iff a required json key is omitted
   """
    # first checks all keys are present
    if 'first_name' not in entrant or \
            'last_name' not in entrant or \
            'passport' not in entrant or \
            'birth_date' not in entrant or\
            'home' not in entrant or \
            'from' not in entrant or \
            'entry_reason'not in entrant:
        return False
    else:  # then checks all keys are not empty strings
            if entrant['first_name'] == "" or \
                    entrant['last_name'] == "" or \
                    entrant['passport'] == "" or \
                    entrant['birth_date'] == "" or \
                    entrant['home']['city'] == "" or \
                    entrant['home']['region'] == "" or \
                    entrant['home']['country'] == "" or \
                    entrant['from']['city'] == "" or \
                    entrant['from']['region'] == "" or \
                    entrant['from']['country'] == "" or \
                    entrant['entry_reason'] == "":
                return False
            else:
                return True
