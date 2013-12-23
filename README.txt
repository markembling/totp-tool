TOTP Tool
=========

This is a tiny python tool for providing HOTP/TOTP one-time tokens.

The secret token must be provided to the tool as an argument or on stdin, and 
may be either the raw secret or an otpauth:// URI.

    totp.py [options] SECRET
    OR
    totp.py [options] --stdin < secret.txt

Secrets via stdin
-----------------

If the secret is provided via stdin, it must be the first line in the file.

The script also takes several other arguments. Full details can be seen by 
running with the help option:

    totp.py --help

Dependencies
------------

This script uses the following excellent libraries:

    - tadeck/onetimepass <https://github.com/tadeck/onetimepass>
    - six <https://pypi.python.org/pypi/six>

These are packaged within the 'dist' directory so that the entire thing can 
be placed on a USB stick or similar and used on any python-equipped machine.
