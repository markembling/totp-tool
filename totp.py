#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import fileinput

# Import from 'dist' directory
curdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dist")
sys.path.append(curdir)

import onetimepass as otp

__author__ = "Mark Embling <mark@markembling.info>"
__version__ = "0.1"

def _get_data(options, args):
    '''Gets the raw secret data from either stdin or args'''
    data = ""
    if options.stdin:
        # Read first line from stdin
        data = sys.stdin.readline()
    else:
        if len(args) != 1:
            parser.error("no secret provided")
        data = args[0]
    return data

def _get_secret(input):
    '''Attempts to get the secret from the given string - either the whole
    string itself, or the secret from within an otpauth:// URI.
    '''
    input = input.strip()
    if input.startswith("otpauth://"):
        u = urlparse(input)
        q = parse_qs(u.query)
        return (q["secret"][0], u.hostname)
    return (input, None)


if __name__ == "__main__":
    parser = OptionParser()
    parser.description = "Prints the TOTP auth code for the given secret. Can be either the raw secret string or a otpauth:// URI; the script will attempt to auto-detect which is given."
    parser.usage = "%prog [options] secret OR %prog [options] --stdin < secret.txt"
    parser.epilog = "Copyright (c) Mark Embling 2013"

    parser.add_option("--stdin", dest="stdin", 
                      action="store_true", default=False,
                      help="Read the secret (raw secret or otpauth:// URI) from stdin [default: %default]")
    parser.add_option("--type", dest="type", 
                      choices=["TOTP", "HOTP"], default="TOTP", 
                      help="Token type (HOTP or TOTP). If a URI is provided, the type will be determined from there. [default: %default]")
    parser.add_option("--count", dest="count", 
                      type="int", default=1,
                      help="Counter for HOTP [default: %default]")
    # parser.add_option("-d", "--digits", dest="digits", 
    #                   choices=['6','8'], default='6',
    #                   help="Number of digits to display (6 or 8) [default: %default]")

    (options, args) = parser.parse_args()

    # Get the secret and type
    data = _get_data(options, args)
    (secret, type_) = _get_secret(data)
    if type_ is None:
        type_ = options.type

    # Get the token and print
    if type_.upper() == "HOTP":
        print(otp.get_hotp(secret, intervals_no=options.count))
    else:
        print(otp.get_totp(secret))
