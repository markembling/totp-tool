#!/usr/bin/env python

import onetimepass as otp
from optparse import OptionParser
from urlparse import urlparse, parse_qs

__author__ = "Mark Embling <mark@markembling.info>"
__version__ = "0.1"

def _get_secret(input):
    '''Attempts to get the secret from the given string - either the whole
    string itself, or the secret from within an otpauth:// URI.
    '''
    if input.startswith("otpauth://"):
        u = urlparse(input)
        q = parse_qs(u.query)
        return (q["secret"][0], u.hostname)
    return (input, None)


if __name__ == "__main__":
    parser = OptionParser()
    parser.description = "Prints the TOTP auth code for the given secret. Can be either the raw secret string or a otpauth// URI; the script will attempt to auto-detect which is given."
    parser.usage = "%prog [options] secret"
    parser.epilog = "Copyright (c) Mark Embling 2013"

    parser.add_option("-t", "--type", dest="type", 
                      choices=["TOTP", "HOTP"], default="TOTP", 
                      help="Token type (HOTP or TOTP). If a URI is provided, the type will be determined from there. [default: %default]")
    parser.add_option("-d", "--digits", dest="digits", 
                      choices=[6,8], default=6,
                      help="Number of digits to display (6 or 8) [default: %default]")
    parser.add_option("-c", "--count", dest="count", 
                      type="int", default=1,
                      help="Counter for HOTP [default: %default]")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    # Determine the type and secret
    (secret, type_) = _get_secret(args[0])
    if type_ is None:
        type_ = options.type

    # Get the token and print
    if type_.upper() == "HOTP":
        print(otp.get_hotp(secret, intervals_no=options.count))
    else:
        print(otp.get_totp(secret))
