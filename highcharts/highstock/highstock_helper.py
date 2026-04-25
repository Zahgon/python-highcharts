# -*- coding: utf-8 -*-
from future.standard_library import install_aliases
install_aliases()
from past.builtins import basestring

from urllib.request import urlopen
import urllib

import json, os, sys
import datetime, re
from datetime import tzinfo


def jsonp_loader(url, prefix_regex=r'^(.*\()', suffix_regex=r'(\);)$', sub_d=None, sub_by=''):
    """jsonp_loader is to request (JSON) data from a server in a different domain (JSONP) 
    and covert to python readable data. 
    1. url is the url (https) where data is located
    2. "prefix_regex" and "suffix_regex" are regex patterns used to 
        remove JSONP specific prefix and suffix, such as callback header: "callback(" and end: ");", 
    3. "sub_d" is regex patterns for any unwanted string in loaded json data (will be replaced by sub_by). 
    4. "sub_by" is the string to replace any unwanted string defined by sub_d
    For function coverstion, such as Data.UTC to datetime.datetime, please check JSONPDecoder
    """
    pass

def interpolateRGB(lowRGB, highRGB, fraction):
    pass


class JSONPDecoder(json.JSONDecoder):
    """Customized JSON decoder. It is used to convert everything 
    that is python non-compatible (usually Javascript functions)
    to one that can be read by python. It needs to coordinate with 
    customized JSON encoder in main library, such as highcharts.py, 
    to convert back to Javascript-compatiable functions.
    For example: in _iterdecode, it checks if queried JSON has Data.UTC 
    and (if yes)converts it to datetime.datetime
    """

    def decode(self, json_string):
        """
        json_string is basicly string that you give to json.loads method
        """
        pass

    def _iterdecode_list(self, lst):
        pass

    def _iterdecode_dict(self, dct):
        pass

    def _iterdecode(self, obj):
        pass

    @staticmethod
    def is_js_date_utc(json):
        """Check if the string contains Date.UTC function 
        and return match group(s) if there is
        """
        pass

    @staticmethod
    def json2datetime(json):
        """Convert JSON representation to date or datetime object depending on
        the argument count. Requires UTC datetime representation.
        Raises ValueError if the string cannot be parsed.
        """
        pass


class UTC(tzinfo):
    """UTC"""

    ZERO=datetime.timedelta(0)
    
    def utcoffset(self, dt):
        pass
    
    def tzname(self, dt):
        pass
    
    def dst(self, dt):
        pass


