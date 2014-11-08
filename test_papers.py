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

'''
def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]
    # assert decide("test_valid_visa.json", "watchlist.json", "countries.json") == ["Reject", "Reject", "Accept"]
    # assert decide("test_date_format.json", "watchlist.json", "countries.json") == ["Reject", "Reject", "Accept"]
    # assert decide("test_req_keys.json", "watchlist.json", "countries.json") == \
          # ["Reject", "Reject", "Reject", "Reject", "Reject"]

def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")


# add functions for other tests
'''


def test_date_format():
    decide("test_date_format.json",  "watchlist.json", "countries.json")
