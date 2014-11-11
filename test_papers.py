#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    # Tests that two KAN citizens are admitted
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    # Tests that a suspect on watchlist is detained for secondary processing
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    # Tests that someone from a medical advisory country is Quarantines
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]
    # Tests that if any necessary key is either missing or without value, the entrant is rejection
    # Note: this test tests ALL POSSIBLE failures individually
    assert decide("test_req_keys.json", "watchlist.json", "countries.json") == \
        ["Reject", "Reject", "Reject", "Reject", "Reject", "Reject", "Reject",
            "Reject", "Reject", "Reject", "Reject", "Reject", "Reject", "Reject"]
    # Tests that people without a transit visa, or with an expired visa are rejected
    assert decide("test_transit_visa.json", "watchlist.json", "countries.json") == ['Reject', 'Reject']
    # Tests that people without a visitor visa, or with an expired visa are rejected
    assert decide("test_visit_visa.json", "watchlist.json", "countries.json") == ['Reject', 'Reject']


def test_files(): # Tests a full truth-table of missing files
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
        decide("test_returning_citizen.json", "watchlist.json", "")
        decide("test_returning_citizen.json", "watchlist.json", "countries.json")
        decide("", "watchlist.json", "countries.json")
        decide("", "", "countries.json")
        decide("", "", "")
        decide("test_returning_citizen.json", "watchlist.json", "")
        decide("test_returning_citizen.json", "", "")


def test_format():
    #  Tests a case where the formats are not correct
    assert decide("test_date_format.json",  "watchlist.json", "countries.json") == ['Reject']
    assert decide("test_passport_format.json", "watchlist.json", "countries.json") == ['Accept', 'Reject']
