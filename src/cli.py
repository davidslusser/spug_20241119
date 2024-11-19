#!/usr/bin/python

import argparse
import datetime
import logging
import time
import sys
import traceback


__doc__ = """this is a really great cli"""

__version__ = "0.0.3"


def get_opts():
    """Return an argparse object."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--verbose", default=logging.INFO, action="store_const", const=logging.DEBUG, help="enable debug logging")
    parser.add_argument("-v", "--version", action="version", version=__version__, help="show version and exit")
    parser.add_argument("-t", "--time", dest="time", action="store_true", help="include execution time")

    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def do_the_thing():
    logging.debug("starting the real work...")
    logging.info("mission accomplished!")


def main():
    try:
        opts = get_opts()
        if opts.time:
            start = datetime.datetime.now()
        
        # call function(s) to do work here
        do_the_thing()

        if opts.time:
            end = datetime.datetime.now()
            logging.info(f"script completed in: {end - start}")
    except Exception as err:
        logging.error(err)
        if opts.verbose == 10:
            traceback.print_exc()
        return 255


if __name__ == "__main__":
    sys.exit(main())
