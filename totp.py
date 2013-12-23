#!/usr/bin/env python

import onetimepass as otp
from optparse import OptionParser

__author__ = "Mark Embling <mark@markembling.info>"
__version__ = "0.1"

def _get_secret(input):
    '''Attempts to get the secret from the given string - either the whole
    string itself, or the secret from within an otp:// URI.
    '''
    if input.startswith("otp://"):
        raise NotImplementedError("TODO: otp:// URL support")
    return input


if __name__ == "__main__":
    parser = OptionParser()
    parser.description = "Prints the TOTP auth code for the given secret. Can be either the raw secret string or a otp:// URI. By default, the script will attempt to auto-detect which is given."
    parser.usage = "%prog [options] secret"
    parser.epilog = "Copyright (c) Mark Embling 2013"

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    secret = _get_secret(args[0])
    print(otp.get_totp(secret))
